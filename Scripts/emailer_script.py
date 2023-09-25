# Taken from: https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development

import smtplib, ssl

port = 465  # For SSL
password = input("Type your password and press enter: ")
sender_email = "finboys.news@gmail.com"
receiver_email = "finboys.news@gmail.com"
message = """\
Subject: email test

Est-ce que ca marche?"""

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("finboys.news@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message)