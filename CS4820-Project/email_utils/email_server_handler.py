from smtplib import SMTP
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class EmailHandler:
    domain = ''
    port = None
    smtp_server = ''
    from_name = ''
    sender = ''
    receiver = ''
    subject = ''
    body = ''

    def __init__(self, smtp_server, port, from_name, sender, domain, subject, body):
        self.smtp_server = smtp_server
        self.port = port
        self.from_name = from_name
        self.sender = sender
        self.domain = domain
        self.subject = subject
        self.body = body

    def set_sender(self, sender):
        if sender.endswith(self.domain):
            self.sender = sender
        elif "@" not in sender:
            self.sender = sender + self.domain

    def set_receiver(self, receiver):
        if "@" not in receiver:
            self.receiver = receiver + self.domain
        else:
            self.receiver = receiver

    def set_subject(self, subject):
        self.subject = subject

    def set_body(self, body):
        self.body = body

    def send(self, file_array):
        if self.receiver == "":
            print("There is no specified receiver")
            return
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = self.from_name + " <" + self.sender + ">"
        msg['To'] = self.receiver
        body = self.body
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
        with SMTP(self.smtp_server, self.port) as server:
            server.ehlo()
            print("Sending message...")
            server.sendmail(self.sender, self.receiver, msg.as_string())
            print("Message sent")
