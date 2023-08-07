from flask import Flask, request, render_template
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

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            query = "SELECT username, pass_word FROM student where name = ?;"
            cur.execute(query, (username, ))

            if password == password:
                return render_template('welcome.html')
            
        except sqlite3.Error as error:
            print('Error occurred - ', error)

        finally:
            cur.close()
            conn.close()
    
    return render_template("index.html")
            

if __name__ == '__main__':
    app.run(debug=True)