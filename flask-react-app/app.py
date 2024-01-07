from flask import Flask, render_template, jsonify, request
from flask_bcrypt import Bcrypt
import mysql.connector  
from datetime import datetime, timedelta,timezone
import time
import json
import requests
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required,JWTManager,get_jwt,unset_jwt_cookies



app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config["JWT_SECRET_KEY"] = "catmeow" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # No password for default XAMPP setup
app.config['MYSQL_DB'] = 'website'  


def get_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL: ", err)
        return None
    

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

#connection = get_mysql_connection()
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = data.get("username")
    email = data.get("email")
    password = data.get("password")
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')  # Hash the password
    
    conn = get_mysql_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Check if user or email already exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (user, email))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                return jsonify({"msg": "Username or email already taken"}), 409
            
            # Insert into website_users table
            cursor.execute("INSERT INTO users (Username, Password, Email) VALUES (%s, %s, %s)", 
                           (user, password_hash, email))
            user_id = cursor.lastrowid  # Retrieve the last inserted ID

            # Insert into website_user_information table with NULL values for Bio and Age
            cursor.execute("INSERT INTO user_information (User_ID, Bio, Age) VALUES (%s, %s, %s)", 
                           (user_id, None, None))

            conn.commit()  # Commit the transaction
            cursor.close()
            return jsonify({"msg": "User created"}), 200
        
        except mysql.connector.Error as err:
            print("Error occurred: ", err)
            conn.rollback()  # Rollback in case of error
            return jsonify({"error": "An error occurred"}), 500
        
        finally:
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500


@app.route("/login", methods=["POST"])
def login():
    # Parse the incoming JSON data
    data = request.get_json()

    # Extract email and password from the parsed JSON
    email = data.get('email')
    password = data.get('password')

    # Logic to validate credentials against the database
    #(added bcrypt during register (adding bcrypt later to login))
    conn = get_mysql_connection()
    if conn is not None:
        cursor = conn.cursor()
        # Replace the query with your actual query to validate credentials
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        #print("storedhash:", user[3])
        if user and bcrypt.check_password_hash(user[3],password):
            # User is valid, create an access token and return it
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token)
        else:
            # User is invalid
            return jsonify({"msg": "Bad username or password"}), 401
    else:
        return jsonify({"error": "Database connection failed"})


@app.route('/dbtest')
def db_test():
    conn = get_mysql_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * from users")  # Sample query to test database connection
        users = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"users": users})
    else:
        return jsonify({"error": "Database connection failed"})

@app.route("/profile")
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    
    conn = get_mysql_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to get column names
        cursor.execute("SELECT users.User_ID, users.Username, users.Email, user_information.* FROM users INNER JOIN user_information ON users.User_ID = user_information.User_ID WHERE users.email = %s" , (current_user,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            if user_data["Age"]:
                user_data["Age"] = user_data["Age"].strftime("%Y-%m-%d")
            #print(user_data)
            return jsonify(user_data), 200
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"error": "Database connection failed"}), 500


@app.route("/test")
def test():
    player_name = request.args.get('xdkry')

    #if not player_name:
       # return jsonify({"error": "Missing player name parameter"}), 400
    
    url = f"https://fortnite-api.com/v2/stats/br/v2?name=xdkry"

    headers = {
        "Authorization": "c71b25f4-bda9-4a42-b301-495d7d0a7459"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "error": "Failed to fetch data from Fortnite API",
            "status_code": response.status_code
        }), response.status_code

@app.route("/testapex")
def test2():
    player_name = request.args.get('player_name')
    platform = request.args.get('platform')
    api_key = 'c41a910c-b062-439b-8d27-95528ff94338'  
    
    #if not player_name or not platform:
    #    return jsonify({"error": "Missing player name or platform parameter"}), 400
    
    url = f"https://public-api.tracker.gg/v2/apex/standard/profile/psn/Daltoosh"
    headers = {
        "TRN-Api-Key": api_key
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data from tracker.gg"}), response.status_code
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api():
    return jsonify(message="Hello from Flask!")

@app.route('/time')
def get_current_time():
    return {'time': datetime.now()}

if __name__ == '__main__':
    app.run(debug=True)

