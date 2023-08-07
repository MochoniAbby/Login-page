import Student
import bcrypt
import pyotp

# Connect to the MySQL database (replace the parameters with your database credentials)
conn = Student.connect(host='localhost', user='your_username', passwd='your_password', db_name='Student')
cursor = conn.cursor()

# Function to hash the password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to verify the password
def verify_password(entered_password, hashed_password):
    return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password)

# Function to add a new user to the database
def add_user(email, password):
    hashed_password = hash_password(password)
    cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, hashed_password))
    conn.commit()

# Function to retrieve user data from the database based on email
def get_user_details_by_email(email):
    cursor.execute('SELECT * FROM users WHERE email = %s', (email))
    return cursor.fetchone()

# Function to implement OTP (using pyotp library)
def generate_otp():
    totp = pyotp.TOTP('your_secret_key')  # Replace 'your_secret_key' with your secret key
    return totp.now()

# Sample usage
if __name__ == '__main__':
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    user = get_user_by_email(email)
    if user and verify_password(password, user[2]):
        # Password is correct
        otp = generate_otp()
        print("OTP:", otp)
        # Additional logic to send OTP (via SMS or other methods) and verify it
        # Implement further multifactor authentication checks here if desired

    else:
        print("Invalid email or password")

# Remember to close the database connection when done
conn.close()
