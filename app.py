from flask import Flask, request, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
import sqlite3
import random; import string

app = Flask(__name__)
bcrypt = Bcrypt(app)

#Generate otp_code using defined function
def generate_otp():
    letters = string.ascii_letters
    code = ''.join(random.sample(letters, 5))
    return code

#Hashing the password
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

#Comparing the hashed password and the one in the database
#Password to compare comes second. This prevents 'Invalid salt' error
def verify_password(password, hashed_password):
    return bcrypt.check_password_hash(hashed_password, password)

#Establishing connection to SQLite3 database
def get_db_conn():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#Redirection for backroute(going backwards one step in the browser) to login page
@app.route('/index.html')
def redirecting():
    return redirect(url_for('login'))

#Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == '' or password == '':
            print("Missing details")
        else:
            conn = get_db_conn()

            try:
                cur = conn.cursor()
                query = "SELECT pass_word FROM student WHERE username = ?;"
                result = cur.execute(query, (username, ))
                row = result.fetchone()

                if row:
                    passcode = row['pass_word']
                    if verify_password(password, passcode.encode('utf-8')):
                        return render_template('welcome.html')
                    else:
                        print("Wrong password")
                else:
                    return "Username not found"

            except sqlite3.Error as error:
                print('Error occured - ', error)

            finally:
                cur.close()
                conn.close()

    return render_template("index.html")

@app.route('/register', methods = ["GET", "POST"])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if username == '' or password == '' or email == '':
            print("Missing details")
        else:
            conn = get_db_conn()

            try:
                cur = conn.cursor()
                query = "SELECT COUNT(*) FROM student WHERE username = ?;"
                count = cur.execute(query, (username,)) 
                existing_user = count.fetchone()[0]

                if existing_user > 0:
                    print("Username already exists. Try a different username.")
                else:
                    code = generate_otp()
                    hashed_password = hash_password(password)
                    update_query = "INSERT INTO student (username, email, pass_word, otp_code) VALUES (?, ?, ?, ?);"
                    cur.execute(update_query, (username, email, hashed_password, code))
                    conn.commit()
                    return render_template('index.html')
            
            except sqlite3.Error as error:
                print("Database Error - ", error)

            finally:
                cur.close()
                conn.close()

    return render_template("registration.html")

if __name__ == '__main__':
    app.run(debug=True)