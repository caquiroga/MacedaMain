#!/usr/bin/python
'''
Created on 6 Jun 2012
@author: Jeremy Blythe; updated by CAQ in August 2013
Motion Uploader - upload one file to FTP
'''
# Import smtplib for the actual sending function
import smtplib

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime.application

#Import sys to deal with command line arguments
import sys

import logging
import time

from datetime import datetime
import os
import os.path
import gdata.data
import gdata.docs.data
import gdata.docs.client
import ConfigParser
import ftplib
import shutil
import traceback
from subprocess import call

 
class MotionUploader:
    def __init__(self, config_file_path):
        # Load config
        config = ConfigParser.ConfigParser()
        config.read(config_file_path)

        # FTP account credentials
        self.ftp_username = config.get('ftp', 'user')
        self.ftp_password = config.get('ftp', 'password')
        self.ftp_name = config.get('ftp', 'name')
        # Folder where you want the videos to go
        self.folder = config.get('ftp', 'folder')
         
        # GMail account credentials
        self.username = config.get('gmail', 'user')
        self.password = config.get('gmail', 'password')
        self.from_name = config.get('gmail', 'name')
        self.sender = config.get('gmail', 'sender')
        # Recipient email address (could be same as from_addr)
        self.recipient = config.get('gmail', 'recipient')        
        # Subject line for email
        self.subject = config.get('gmail', 'subject')
         

	# Threshold to be be used for reporting relevant motion
	self.v_threshold = int(config.get('motion', 'v_threshold'))
        self.vh_threshold = int(config.get('motion', 'vh_threshold'))
        self.hl_threshold = int(config.get('motion', 'hl_threshold'))
        self.hh_threshold = int(config.get('motion', 'hh_threshold'))
        

        # Options
        self.delete_after_upload = config.getboolean('options', 'delete-after-upload')
        self.send_email = config.getboolean('options', 'send-email')         
	
     
    def _send_email(self,file_path, x_mov, y_mov, x_w, y_h):
	try:
		logging.info("Start of SMTP transaction.")

		# Create a text/plain message
		msg = email.mime.Multipart.MIMEMultipart()
		msg['Subject'] = self.subject
		msg['From'] = self.from_name
		msg['To'] = self.recipient

		# The main body is just another attachmen
		body = email.mime.Text.MIMEText(" Movement detected at" + str(x_mov) + "," + str(y_mov) + "["+ str(x_w) +"," + str(y_h) + "]")
		msg.attach(body)

		# Attachment block code
		directory=file_path

		# Split de directory into fields separated by / to substract filename
		spl_dir=directory.split('/')

		# We attach the name of the file to filename by taking the last
		# position of the fragmented string, which is, indeed, the name
		# of the file we've selected
		filename=spl_dir[len(spl_dir)-1]
		# We'll do the same but this time to extract the file format (pdf, epub, docx...)
		spl_type=directory.split('.')
		type=spl_type[len(spl_type)-1]
		logging.info("Preparing the attachment " + directory + " ...")
		fp=open(directory,'rb')
		att = email.mime.application.MIMEApplication(fp.read(),_subtype=type)
		fp.close()
		att.add_header('Content-Disposition','attachment',filename=filename)
		msg.attach(att)
                logging.info("Login to the smtp server...")

		s = smtplib.SMTP('smtp.gmail.com:587')
		s.starttls()
		s.login(self.username,self.password)

		logging.info("Sending the e-mail...")
		s.sendmail(self.sender,self.recipient, msg.as_string())
		s.quit()

		logging.info("E-mail successfully sent.")
	        logging.info("End of SMTP transaction.")
	except:
		traceback.print_exc()

    def _upload_ftp(self, video_file_path):
        '''Upload the file'''
        logging.info("Start of FTP transaction.")
	logging.info("Logging in the FTP server...")
	try:
		ftp = ftplib.FTP()
		ftp.connect(self.ftp_name)
		logging.info(ftp.getwelcome())
		try:
		        ftp.login(self.ftp_username, self.ftp_password)
       		 	ftp.cwd(self.folder)
		        # move to the desired upload directory
		        logging.info("Currently in:" + ftp.pwd())
		        logging.info("Uploading file to the FTP server..." + video_file_path)
	        	fullname = video_file_path
		        name = os.path.split(fullname)[1]
			logging.info("Deleting file ..." + name);
			logging.info("Opening file locally..." + fullname)
		        file = open(fullname, "rb") #open in normal read mode
			logging.info("Transferring file..." + name);
		        ftp.storbinary('STOR %s' % name, file)
	                logging.info("Closing file..." + name);
		        file.close()
		        logging.info("Successfully uploaded.")

                        if self.delete_after_upload:
                                time.sleep(5)
                                os.remove(file_path)
		finally:
		        logging.info("Leaving FTP server...")
	  		ftp.quit()
			logging.info("End of FTP transaction.")	
	except:
		logging.exception('Got exception on upload_ftp')


    def report_picture(self, file_path, x_mov, y_mov, x_w, y_h):
        " If the picture is a periodic snapshot, transfer it to the FTP server; Otherwise, send an e-mail with the attached picture"
 	try:
	       	log_filename = '/home/pi/Surveillance/tmp/surveillance.log'
        	logging.basicConfig(filename=log_filename ,format='%(asctime)s %(message)s',level=logging.INFO)

		if ((x_mov>self.hl_threshold) and (x_mov<self.hh_threshold) and (y_mov>self.v_threshold) and (y_mov<self.vh_threshold)):
                        # Send the e-mail with the picture
			if(self.connect_3G()): self._send_email(file_path, x_mov, y_mov, x_w,y_h)
                elif ((x_mov==0) and (y_mov==0)):
			# Upload the snapshot to the FTP server
			if(self.connect_3G()): self._upload_ftp(file_path)
			# if(self.connect_3G()): self._send_email(file_path, x_mov, y_mov, x_w,y_h)
 
        except:
                traceback.print_exc()



    def connect_3G(self):
	try:
		# check status of 3G connection
		logging.info('Checking 3G connection...')
        	if (call(['/usr/bin/modem3g/sakis3g', 'status'])== 6):
			logging.info('3G connection not stablished.')
			logging.info('Connecting to 3G...')	
                	if(call(['/usr/bin/modem3g/sakis3g', '--sudo', 'start'])==0):
				logging.info('3G connected.')
				return True
			else:
				logging.info('3G connection not accessible.')
				call(['/usr/bin/modem3g/sakis3g', '--sudo', 'stop'])
				return False
		else: 
			logging.info('3G connection already stablished.')
			return True	
        except:
                traceback.print_exc()



 
if __name__ == '__main__':         
    try:
        if len(sys.argv) < 3:
            exit('On Motion Event Script \n Modified from Jeremy Blythe (http://jeremyblythe.blogspot.com)\n\n   Usage: on_motion_event.py {config-file-path} {video-file-path}')
        cfg_path = sys.argv[1]
        file_path = sys.argv[2]
	x_motion = int(sys.argv[3])
	y_motion = int(sys.argv[4])
	if(len(sys.argv) <= 5):
		x_width = 0
		y_height = 0
	else:
		x_width = int(sys.argv[5])	
		y_height = int(sys.argv[6])

	print x_motion, y_motion
	print x_width, y_height
	logging.info("Sending " + file_path);

        if not os.path.exists(cfg_path):
        	exit('Config file does not exist [%s]' % cfg_path)    
        if not os.path.exists(file_path):
        	exit('File to be reported does not exist [%s]' % file_path)
	
        MotionUploader(cfg_path).report_picture(file_path, x_motion, y_motion, x_width,y_height) 

    except gdata.client.BadAuthentication:
        exit('Invalid user credentials given.')
    except gdata.client.Error:
        exit('Login Error')
    except Exception as e:
        exit('Error: [%s]' % e)
