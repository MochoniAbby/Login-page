from flask import Flask, request, render_template
from flask_bcrypt import Bcrypt

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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)