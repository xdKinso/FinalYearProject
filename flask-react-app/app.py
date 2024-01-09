from flask import Flask, render_template, jsonify, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import mysql.connector  
from datetime import datetime, timedelta,timezone
import time
import json
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required,JWTManager,get_jwt,unset_jwt_cookies,verify_jwt_in_request



app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
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

@app.route("/profile/update", methods=["POST"])
@jwt_required()
def update():
    current_user_email = get_jwt_identity()
    data = request.get_json()
    Bio = data.get("Bio")
    DOB = data.get("DOB")  # Ensure this key matches what you're sending from the front-end

    conn = get_mysql_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # Fetch the user ID based on the email from JWT token
            cursor.execute("SELECT User_ID FROM users WHERE Email = %s", (current_user_email,))
            user_result = cursor.fetchone()
            if user_result:
                user_id = user_result[0]

                # Update the user_information table
                cursor.execute("UPDATE user_information SET Bio = %s, Age = %s WHERE User_ID = %s", 
                               (Bio, DOB, user_id))
                conn.commit()
                cursor.close()
                return jsonify({"msg": "User updated"}), 200
            else:
                return jsonify({"error": "User not found"}), 404

        except mysql.connector.Error as err:
            print("Error occurred: ", err)
            conn.rollback()
            return jsonify({"error": "An error occurred"}), 500

        finally:
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

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
            cursor.execute("INSERT INTO user_data (User_ID, fn_username) VALUES(%s, %s)",(user_id,None))

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

@app.route("/profile", methods=["GET"])
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

@app.route("/Fnstats")
def fnstats():
    fn_api_key = os.getenv("FN_API_KEY")
    fn_username = request.args.get('username') or None
    verify_jwt_in_request(optional=True)
    current_user_email = get_jwt_identity()

    if current_user_email and not fn_username:
        conn = get_mysql_connection()
        if conn is not None:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT user_data.fn_username
                    FROM user_data
                    INNER JOIN users ON user_data.User_ID = users.User_ID
                    WHERE users.Email = %s
                """, (current_user_email,))
                result = cursor.fetchone()
                if result and result[0]:
                    fn_username = result[0]

    if not fn_username:
        return jsonify({"error": "Please provide or set a Fortnite username"}), 400
    
    url = f"https://fortnite-api.com/v2/stats/br/v2?name={fn_username}"
    headers = {
        "Authorization": fn_api_key 
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
def testapex():
    api_key = 'c41a910c-b062-439b-8d27-95528ff94338'
    url = f"https://public-api.tracker.gg/v2/apex/standard/profile/origin/UnityisLife"
    headers = {
        "TRN-Api-Key": api_key
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        # Log the response status code and response body for debugging
        print(f"Failed with status code: {response.status_code}")
        print(f"Response content: {response.text}")  # Assuming the response is a JSON string
        return jsonify({
            "error": "Failed to fetch data from tracker.gg",
            "status_code": response.status_code,
            "details": response.json()  # This will show the error details from tracker.gg
        }), response.status_code

@app.route('/chatbot', methods=['POST'])
def chatbot():
    client = OpenAI()
    data = request.json
    user_message = data['message']
    print(user_message)
    # Use the client to create a chat completion
    #stream = client.chat.completions.create(
     #   model="gpt-3.5-turbo",
      #  messages=[{"role": "help players improve their fortnite gameplay using their stats", "content": user_message}],
       # stream=True,
    #)

    # Collect the response from the stream
    #response_text = ""
    #for chunk in stream:
     #   if chunk.choices[0].delta.content is not None:
      #      response_text += chunk.choices[0].delta.content

    return user_message#jsonify({'response': response_text})

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

