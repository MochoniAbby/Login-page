from flask import Flask, request, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)

#Hashing the password
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

#Comparing the hashed password and the one in the database
def verify_password(password, hashed_password):
    return bcrypt.check_password_hash(password, hashed_password.encode('utf-8'))

def get_db_conn():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/index.html')
def redirecting():
    return redirect(url_for('login'))

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
                    if password == passcode:
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
    return render_template("registration.html")

if __name__ == '__main__':
    app.run(debug=True)