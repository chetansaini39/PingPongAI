import smtplib
import socket
import time

REMOTE_SERVER = "www.google.com"

def main():

    if(is_connected()==True):
        try:
            print 'Connected to internet\nTrying to send Email'
            GMAIL_USERID = 'midtest7133@gmail.com'
            GMAIL_PASS = 'nokia#1234'
            GMAIL_RECIPIENT = 'chetansaini39@gmail.com'
            smtp_session = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_session.ehlo()
            smtp_session.starttls()
            smtp_session.login(GMAIL_USERID, GMAIL_PASS)
            content = 'IP address: %s', socket.gethostbyname(socket.gethostname())  # ouputs tuple/list
            smtp_session.sendmail(GMAIL_USERID, GMAIL_RECIPIENT, 'IP Address of Pi ' + content[1])
            print 'Email sent'
        except smtplib.SMTPException:
            print "Error, authentication failed! Please check your username and password."
    else:
        print 'System not Connected to Internet, retrying in 5 seconds'
        time.sleep(5) # sleep the thread for 5 seconds
        main()

def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)

    return True
  except:
     pass
  return False

if __name__ == '__main__':
    main()
