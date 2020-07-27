#!/usr/bin/python3
import os
import ssl
import smtplib
import csv
import random

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class email_sender:
    def __init__(self, port, smtp_server, sender, password):
        self.sender = sender
        self.port = port
        self.smtp_server = smtp_server
        self.password = password
        context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL(smtp_server, port, context=context)
        self.server.login(sender, password)

    def send_mail(self, master_email, master_path):
        x=0
        master = ""
        while x < self.num_player-1:
            msg = MIMEMultipart()
            msg['Subject'] = "Secret Santa Testing"
            msg['From'] = self.sender
            msg['To'] = self.emails[self.targets[x]]
            text = "{},\r\nFor Secret Santa this year, you have {}.  Happy Gifting!".format(self.names[self.targets[x]], self.names[self.targets[x+1]])
            mtext = MIMEText(text)
            master = master + self.names[self.targets[x]] + " has " + self.names[self.targets[x+1]] + "\r\n" 
            msg.attach(mtext)
            self.server.sendmail(self.sender, self.emails[self.targets[x]], msg.as_string())
            if (master_path != ""):
                mstFile = open(master_path + self.names[self.targets[x]] + ".txt", "w")
                mstFile.write(text)
                mstFile.close()
            x=x+1
        msg = MIMEMultipart()
        msg['Subject'] = "Secret Santa Testing"
        msg['From'] = self.sender
        msg['To'] = self.emails[self.targets[x]]
        master = master + self.names[self.targets[x]] + " has " + self.names[self.targets[0]] + "\r\n"      
        text = "{},\r\nFor Secret Santa this year, you have {}.  Happy Gifting!".format(self.names[self.targets[x]], self.names[self.targets[0]])
        mtext = MIMEText(text)       
        msg.attach(mtext)
        self.server.sendmail(self.sender, self.emails[self.targets[x]], msg.as_string())
        if (master_path != ""):
            mstFile = open(master_path + self.names[self.targets[x]] + ".txt", "w")
            mstFile.write(text)
            mstFile.close()

        if (master_email != ""):
            msg = MIMEMultipart()
            msg['Subject'] = "Secret Santa Master Testing"
            msg['From'] = self.sender
            msg['To'] = master_email
            text = MIMEText(master)
            msg.attach(text)
            self.server.sendmail(self.sender, master_email, msg.as_string())


    def close_connection(self):
        self.server.close()

    def readfile(self, filename):
        csvfile = open(filename)
        reader = csv.reader(csvfile, delimiter=',')
        count = 0  
        self.names = []
        self.emails = []   
        for row in reader: 
            #print(count)
            #print(row[0])
            self.names.append(row[0])
            self.emails.append(row[1])
            count = count + 1
        self.num_player = count

    def randomize(self):
        x = 0
        self.targets= [x for x in range(self.num_player)]
        random.shuffle(self.targets)
        random.shuffle(self.targets)
        random.shuffle(self.targets)
        random.shuffle(self.targets)
        random.shuffle(self.targets)

def run():
    sender_email = ""
    password = ""
    file_path = ""
    master_email = "" # use "" if no master email
    master_path = "" # use "" if no master text files
    es = email_sender(465, "smtp.gmail.com", sender_email, password)  
    es.readfile(file_path) 
    es.randomize()
    es.send_mail(master_email, master_path)
    es.close_connection()

if __name__ == '__main__':
    run()
