import smtplib, ssl
from email.message import EmailMessage


class EmailHandler:
    port = 465
    smtp_server = "smtp.gmail.com"

    def __init__(self):
        self.sender = input("Enter the account of the sender: ")
        self.password = input("Please enter a password: ")

    def send(self):
        receiver = input("Who should I send this message to? ")
        with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
            server.ehlo()
            print("Logging in...")
            server.login(self.sender, self.password)
            print("Sending message...")
            server.sendmail(self.sender, receiver, 'Hello World')
        print("Message sent")
