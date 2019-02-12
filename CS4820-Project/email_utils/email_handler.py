import smtplib, ssl
from email.message import EmailMessage


class EmailHandler:
    port = 465
    smtp_server = "smtp.gmail.com"
    valid_sender = False


    def set_sender(self):
        self.sender = input("Enter the account of the sender: ")
        self.password = input("Please enter a password: ")
        # try logging in to test
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, self.port)
            server.login(self.sender, self.password)
            self.valid_sender = True
        except smtplib.SMTPAuthenticationError:
            print("The supplied address or password is incorect.")
            self.valid_sender = False

    def is_valid_sender(self):
        return self.valid_sender;

    def send(self):
        if not self.valid_sender:
            print("Can not send an email without a valid sender")
            return
        receiver = input("Who should I send this message to? ")
        with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
            server.ehlo()
            print("Logging in...")
            server.login(self.sender, self.password)
            print("Sending message...")
            server.sendmail(self.sender, receiver, 'Hello World')
        print("Message sent")
