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
#cors setup
CORS(app, origins=["http://localhost:3000"])
#adding bcrypt to encrypt passwords and decrypting
bcrypt = Bcrypt(app)

#secret key for jwt (used to hash the key based on email)
app.config["JWT_SECRET_KEY"] = "catmeow" 
#token expires once an hour
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
#adding jwt finally to the app
#used for knowing if a user is logged in etc(useful for not allowing not logged in users to access certain locations)
jwt = JWTManager(app)

#sql setup(used xampp)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # No password for default XAMPP setup
app.config['MYSQL_DB'] = 'website'  

#defining my sql connection creator
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

#route to update profile Bio and date of birth for now
    #want to add ( usernames for games such as valorant(when i get api key(if)),fortnite, apex, csgo, ) and add to database
#post because we are getting values and sending them back
@app.route("/profile/update", methods=["POST"])
#user needs to be logged in to use
@jwt_required()
def update():
    #getting the identity of user
    current_user_email = get_jwt_identity()
    data = request.get_json()
    Bio = data.get("Bio")
    DOB = data.get("DOB")  

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
                #commiting the execute
                conn.commit()
                #closing the cursor
                cursor.close()
                return jsonify({"msg": "User updated"}), 200
            else:
                return jsonify({"error": "User not found"}), 404

        except mysql.connector.Error as err:
            print("Error occurred: ", err)
            conn.rollback()
            return jsonify({"error": "An error occurred"}), 500

        finally:
            #closing connection
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

#logout function 
@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.after_request
def refresh_expiring_jwts(response):
    try:
        #retrieve expiration time of token
        exp_timestamp = get_jwt()["exp"]
        #calculate current time zone in utc
        now = datetime.now(timezone.utc)
        #set time stamp 30 minutes ahead of current time
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        #check if token close to expiring (within 30 minutes)
        if target_timestamp > exp_timestamp:
            #create new access token
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
#register page
@app.route("/register", methods=["POST"])
def register():
    # Parse the incoming JSON data
    data = request.get_json()
    #setting variables from json
    user = data.get("username")
    email = data.get("email")
    password = data.get("password")
    #hashing the password
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')  # Hash the password
    
    # Connect to the database
    conn = get_mysql_connection()
    #if connection is avaliable
    if conn is not None:
        #try this
        try:
            #creating cursor
            cursor = conn.cursor()
            # Check if user or email already exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (user, email))
            existing_user = cursor.fetchone()

            if existing_user:
                #close cursor
                cursor.close()
                #tell the frontend that user or email is taken
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

#login
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

#testing database (might change this to view all users profiles and their stats)
@app.route('/dbtest')
def db_test():
    conn = get_mysql_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * from users")  # getting all users test database connection
        users = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"users": users})
    else:
        return jsonify({"error": "Database connection failed"})

#Profile route using get
    #might add stuff like their fortnite username and their stats here soon
    #want to add more but i dont have an api key 
@app.route("/profile", methods=["GET"])
#required to be a user
@jwt_required()
def profile():
    #getting users identity
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

    #getting users fortnite stats from fortnite api
    #this needs a bit of changing i think logic is a little wrong 
    #fixed temporarily to get the api to work
    #will soon add so that it gets the data and adds to database so i can display on profile
@app.route("/Fnstats")
#@jwt_required
def fnstats():
    #getting api key from .env file to make it more secure
    fn_api_key = os.getenv("FN_API_KEY")
    #getting fornite username
    fn_username = request.args.get('username') or None
    #optional to be logged in if username is in database will get from there other wise can take input.
    verify_jwt_in_request(optional=True)
    #getting users identity
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
    #fortnite api request
    url = f"https://fortnite-api.com/v2/stats/br/v2?name={fn_username}"
    headers = {
        "Authorization": fn_api_key 
    }
    response = requests.get(url, headers=headers)#sending the request
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "error": "Failed to fetch data from Fortnite API",
            "status_code": response.status_code
        }), response.status_code

#testing apex, worked before but they revoked api keys because some people messed to much around with the api key
    #talking to developer about getting my api key to work(on another note waiting for api key from valorant (have one for league of legends but its a lot of statistics))
@app.route("/testapex")
def testapex():
    api_key = "" #add later when key is available and working
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
        print(f"Response content: {response.text}")  
        return jsonify({
            "error": "Failed to fetch data from tracker.gg",
            "status_code": response.status_code,
            "details": response.json()  # This will show the error details from tracker.gg
        }), response.status_code

# this is the chatbot based on OPENAI using their api 
#works but currently debugging want to also send that users stats
    # to do this i will add an sql statement that gets their stats once i send then to the database
@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        
        # Extracting the JSON data from the request
        data = request.json
        user_message = data['message']
        print(user_message)
        
        # Use the client to create a chat completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        
        # Extract and return the response
        response_text = response.choices[0].message['content']
        return jsonify({'response': response_text})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/users')
def getUsers():
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT User_ID, Username FROM users")
    users = [{"User_ID": row[0], "Username": row[1]} for row in cursor.fetchall()]    
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route('/users/<int:userId>')
def get_user(userId):
    conn = None
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to return data as a dictionary

        query = """
        SELECT 
            u.Username, 
            inf.Bio, 
            inf.Age, 
            ud.fn_username 
        FROM 
            users u 
        LEFT JOIN 
            user_information inf ON u.User_ID = inf.User_ID 
        LEFT JOIN 
            user_data ud ON u.User_ID = ud.User_ID
        WHERE 
            u.User_ID = %s;
        """
        
        cursor.execute(query, (userId,))

        user = cursor.fetchone()
        if user:
            print(user)
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

#base route
@app.route('/')
def index():
    return render_template('index.html')

#first ever test
@app.route('/api')
def api():
    return jsonify(message="Hello from Flask!")

#getting time for front page
@app.route('/time')
def get_current_time():
    return {'time': datetime.now()}

if __name__ == '__main__':
    app.run(debug=True)

