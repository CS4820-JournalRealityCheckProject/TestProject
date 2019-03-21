from smtplib import SMTP
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class EmailHandler:
    port = 25
    smtp_server = "internal-smtp.upei.ca"
    receiver = ""

    def set_receiver(self, receiver):
        self.receiver = receiver

    def send(self, file_array):
        if self.receiver == "":
            print("There is no specified receiver")
            return
        msg = MIMEMultipart()
        msg['Subject'] = "Results"
        msg['From'] = "Program"
        msg['To'] = self.receiver
        body = "These are the results of the script"
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
        with SMTP(self.smtp_server, self.port) as server:
            server.ehlo()
            print("Sending message...")
            server.sendmail(self.receiver, self.receiver, msg.as_string())
            print("Message sent")
