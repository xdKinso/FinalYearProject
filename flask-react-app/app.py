from flask import Flask, render_template, jsonify
import mysql.connector  
import time

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # No password for default XAMPP setup
app.config['MYSQL_DB'] = 'website'  # Replace with your actual database name


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
    
#connection = get_mysql_connection()


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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api():
    return jsonify(message="Hello from Flask!")

@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == '__main__':
    app.run(debug=True)

