#!/usr/bin/env python3

import smtplib, random, string

# Function to generate a random OTP
def generate_otp(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to send OTP via email
def send_otp_email(receiver_email, otp):
    sender_email = "ac8600772211"  # Replace with your email
    sender_password = ""     # Replace with your email password

    message = f"Subject: Your OTP\n\nYour OTP is: {otp}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message)
    server.quit()



# Store the OTP value in a variable
otp = generate_otp()
receiver_email = "aniketchavan2211@gmail.com"
send_otp_email(receiver_email, otp)
print("OTP sent to the recipient's email.")

# Prompt the user to enter the OTP
user_entered_otp = input("Enter the OTP you received via email: ")

# Compare the user's input with the stored OTP
if user_entered_otp == otp:
    print("OTP verification successful. Proceed with the next steps.")
    # You can add your desired logic here for successful verification
else:
    print("OTP verification failed. Please try again.")
    # You can handle the failure scenario here
