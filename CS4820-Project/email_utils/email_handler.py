import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


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
            print("The supplied address or password is incorrect.")
            self.valid_sender = False

    def is_valid_sender(self):
        return self.valid_sender

    def send(self, file_array):
        if not self.valid_sender:
            print("Can not send an email without a valid sender")
            return
        receiver = input("Who should I send this message to? ")
        msg = MIMEMultipart()
        msg['Subject'] = "Attachment test"
        msg['From'] = self.sender
        msg['To'] = receiver
        body = "This is a test email. Its purpose is to test attachments"
        msg.attach(MIMEText(body, "plain"))
        # Read the supplied file
        for file_path in file_array:
            fp = open(file_path, "rb")
            attachment = MIMEBase("text", "csv")
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=file_path)
            msg.attach(attachment)

        with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
            server.ehlo()
            print("Logging in...")
            server.login(self.sender, self.password)
            print("Sending message...")
            server.sendmail(self.sender, receiver, msg.as_string())
        print("Message sent")
