#!/usr/bin/python
 
# Import smtplib for the actual sending function
import smtplib
 
# For guessing MIME type
import mimetypes

import socket
 
# Import the email modules we'll need
import email
import email.mime.application
 
#Import sys to deal with command line arguments
import sys

import ConfigParser

config = ConfigParser.ConfigParser()
config.read("/home/pi/Surveillance/uploader-no-ip.cfg")

#gmail account credentials
username = config.get('gmail', 'user')
password = config.get('gmail', 'password')


# Create a text/plain message
msg = email.mime.Multipart.MIMEMultipart()
msg['Subject'] = 'Message from the Raspberry PI'
msg['From'] = username
msg['To'] = 'c.alvarezquiroga@gmail.com'
 
# The main body is just another attachment
body = email.mime.Text.MIMEText("The Raspberry PI has just booted. Connected to internet using IP " + sys.argv[1])
msg.attach(body)

# send via Gmail server
# NOTE: my ISP, Centurylink, seems to be automatically rewriting
# port 25 packets to be port 587 and it is trashing port 587 packets.
# So, I use the default port 25, but I authenticate.
s = smtplib.SMTP('smtp.gmail.com:587')
s.starttls()
s.login('trasdeairasc@gmail.com', password)
s.sendmail(username,'c.alvarezquiroga@gmail.com', msg.as_string())
s.quit()
