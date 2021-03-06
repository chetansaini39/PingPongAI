#!/usr/bin/python
from subprocess import Popen, PIPE
import smtplib
import  socket
import string

# This script attepts to retrieve the IP address of a specified interface.
# If successful it then emails the retrieved IP to a specified email address

#	FILL OUT THE VALUES BETWEEN THE COMMENT BLOCKS
#######################################################################
# Specify the sender credentials and recipient email address here
SENDER = {}
SENDER['addr'] = 'midtest7133@gmail.com'
SENDER['pass'] = 'nokia#1234'
SENDER['serv'] = 'smtp.gmail.com'
SENDER['port'] = 465  # SSL default GMAIL SMTP port
# SENDER['port'] = 587  # TLS default GMAIL SMTP port

RECEIVER = {}
RECEIVER['addr'] = ['chetansaini39@gmail.com'];
# Note: RECEIVER['addr']  must be a list (ie don't delete the brackets)!
# This allows the specification of a list of addresses ['me@addr.com', 'you@addr.com', 'them@addr.com']

# specify the interface to query
INTERFACE = 'eth0'  # default interface for a Raspberry Pi

# specify the name of the computer to display in the email
HOSTNAME = Popen(['hostname'], stdout=PIPE).communicate()[0].replace('\n', '')

#######################################################################

# Execute the call to ifconfig
# Use AWK to remove everything but the IP Address
try:
    p1 = Popen(['ifconfig', INTERFACE], stdout=PIPE)
    p2 = Popen(['awk', "/inet/ {split ($2,A,\":\"); print A[2]}"], stdout=PIPE, stdin=p1.stdout)

    the_ip = socket.gethostbyname(socket.gethostname())
except:
    the_ip = 'FAILED'

if the_ip == '':
    the_ip = 'no address found'

SUBJECT = "%s's IP:%s on:%s" % (HOSTNAME, socket.gethostbyname(socket.gethostname()), INTERFACE)

# Construct the Email
TO = RECEIVER['addr']
FROM = SENDER['addr']
BODY = string.join((
    'From: %s' % FROM,
    'To: %s' % TO,
    'Subject: %s' % SUBJECT,
    '',
    ''
), '\r\n')
print BODY
# Try to send the email
try:
    server = smtplib.SMTP_SSL(SENDER['serv'], SENDER['port'])  # NOTE:  This is the GMAIL SSL port.
    server.login(SENDER['addr'], SENDER['pass'])
    server.sendmail(FROM, TO, BODY)
    server.quit()

except smtplib.SMTPAuthenticationError:
    print "Error, authentication failed! Please check your username and password."
