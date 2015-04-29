import stagnatingIssues

import smtplib

import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#########################################################
# Receiver's email + GMail sender's account information #
#########################################################
receiver = ''
sender = ''
sender_username = '@gmail.com'
sender_password = ''
msg = MIMEMultipart('alternative')
msg['Subject'] = "Stagnating Issues Reminder"
msg['From'] = sender
msg['To'] = receiver

##############################
# Sifter account information #
##############################
account_name = ''
assignee_email = ''
token = ''
stagnating_threshold_days = 90
include_archived_issues = False

#########################################################

html = stagnatingIssues.get_stagnatingIssues(account_name, assignee_email, token, include_archived_issues, stagnating_threshold_days)

if html != '0':
	html_to_attach = MIMEText(html, 'html')
	msg.attach(html_to_attach)
	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()
	mail.login(sender_username, sender_password)
	mail.sendmail(sender, receiver, msg.as_string())
	mail.quit()
else:
	sys.exit()
