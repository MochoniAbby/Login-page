#importing libraries
from flask import Flask, request, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
import sqlite3
import random; import string

#Initializing application
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
    error = None
    
    #Acquiring input taken from the form
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == '' or password == '':
            error = "Missing details. Enter details"
        else:
            #connecting to the database then do exception handling for connection operations(try.. except.. finally)
            conn = get_db_conn()

            try:
                cur = conn.cursor()
                query = "SELECT pass_word, otp_code FROM student WHERE username = ?;"
                result = cur.execute(query, (username, ))
                row = result.fetchone()

                if row:
                    passcode = row['pass_word']
                    otp_code = row['otp_code']
                    
                    if verify_password(password, passcode.encode('utf-8')):
                        return render_template('welcome.html')
                        
                    elif password == otp_code:
                        return render_template('welcome.html')
                    else:
                        code = generate_otp()
                        update_query = "UPDATE student SET otp_code = ? WHERE username = ?;"
                        cur.execute(update_query, (code, username))
                        conn.commit()
                        error = "Either username or password is incorrect. Your OTP code is {}".format(code)
                else:
                    return "Username not found"

            except sqlite3.Error as e:
                error = "Database error: {}".format(str(e))

            finally:
                cur.close()
                conn.close()

    return render_template("index.html", error=error)

#Registration route (methods are almost the same as those above)
@app.route('/register', methods = ["GET", "POST"])
def registration():
    error = None
    
    #Acquiring input taken from the form
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if username == '' or password == '' or email == '':
            error = "Missing details. Input missing details"
        else:
            conn = get_db_conn()    #connecting to the database
            
            #Exception handling for database operations
            try:
                cur = conn.cursor()
                query = "SELECT COUNT(*) FROM student WHERE username = ?;"
                count = cur.execute(query, (username,)) 
                existing_user_count = count.fetchone()[0]

                if existing_user_count > 0:
                    error = "Username already exists. Try a different username."
                else:
                    #generating code and updating to the database for easy login using the code
                    code = generate_otp()
                    hashed_password = hash_password(password)
                    update_query = "INSERT INTO student (username, email, pass_word, otp_code) VALUES (?, ?, ?, ?);"
                    cur.execute(update_query, (username, email, hashed_password, code))
                    conn.commit()
            
            except sqlite3.Error as e:
                error = "Database Error: {}".format(str(e))

            finally:
                cur.close()
                conn.close()

    return render_template("registration.html", error=error)

if __name__ == '__main__':
    app.run(debug=True)