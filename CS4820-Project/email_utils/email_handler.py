import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class EmailHandler:
    port = 465
    smtp_server = "smtp.gmail.com"
    sender = ""
    password = ""
    receiver = ""
    valid_sender = False

    def set_sender(self, sender, password):
        self.sender = sender
        self.password = password
        # try logging in to test
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, self.port)
            server.login(self.sender, self.password)
            self.valid_sender = True
        except smtplib.SMTPAuthenticationError:
            self.valid_sender = False

    def set_receiver(self, receiver):
        self.receiver = receiver

    def is_valid_sender(self):
        return self.valid_sender

    def send(self, file_array):
        if not self.valid_sender:
            print("Can not send an email without a valid sender")
            return
        if self.receiver == "":
            print("There is no specified receiver")
            return
        msg = MIMEMultipart()
        msg['Subject'] = "Reality Check Finished"
        msg['From'] = 'UPEI REALITY CHECK SYSTEM'
        msg['To'] = self.receiver
        body = "Reality Check System finished. There are two files attached\n"
        msg.attach(MIMEText(body, "plain"))
        # Read the supplied file
        for file_path in file_array:
            fp = open(file_path, "rb")
            attachment = MIMEBase("text", "csv")
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
            f_name = file_path.split('/')[-1]  # get only the name.csv
            attachment.add_header("Content-Disposition", "attachment", filename=f_name)
            msg.attach(attachment)
        with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
            server.ehlo()
            print("Logging in...")
            server.login(self.sender, self.password)
            print("Sending message...")
            server.sendmail(self.sender, self.receiver, msg.as_string())
        print("Message sent")
