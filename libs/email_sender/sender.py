# -*- coding: utf-8 -*-

import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class EmailSender(object):


    def __init__(self, sender, password, receiver, host='smtp.163.com'):
        self.sender = sender
        self.sender_email = sender + '@' + '.'.join(host.split('.')[1:])
        self.password = password
        self.host = host
        if isinstance(receiver, str):
            receiver = [receiver]
        self.receiver = receiver

    def send(self, msg):
        try:
            server = smtplib.SMTP()
            server.connect(self.host)
            server.login(self.sender, self.password)
            server.sendmail(self.sender_email, self.receiver, msg.as_string())
            server.quit()
            print('DONE')
        except Exception as e:
            print(e)

    def make_msg(self, subject, date, content):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = self.receiver[0]
        msg['Date'] = date
        msg.attach(MIMEText(content, 'html', 'utf-8'))
        return msg

    def make_msg_with_zipfile(self, subject, date, content, dirname, filename):
        msg = self.make_msg(subject, date, content)
        zf = open(os.path.join(dirname, filename), 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(zf.read())
        zf.close()
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="Homework.zip"')
        msg.attach(part)
        return msg
