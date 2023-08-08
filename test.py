import random; import string

def generate_otp():
    letters = string.ascii_letters
    code = ''.join(random.sample(letters, 5))
    return code

print(generate_otp())