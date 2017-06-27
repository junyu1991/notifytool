#!/usr/bin/env python
#!encoding:utf-8
#date:2017-05-10
#email_tool.py

'''
Email tools
'''


import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import os
import traceback

__emailencoding='utf-8'

class EmailTool:

    def __init__(self,mail_host,sender,password,receivers,mail_port,**args):

        self.mail_host=mail_host
        self.sender=sender
        self.password=password
        self.receivers=receivers
        self.args=args
        self.mail_port=mail_port

    def send_text(self,message,subject):
        send_text(self.mail_host,self.sender,self.password,self.receivers,message,subject,self.mail_port)

    def send_email_with_attachment(self,send_file,message,subject):
        send_email_with_attachment(self.mail_host,self.sender,self.password,self.receivers,send_file,message,subject,self.mail_port)



def send_text(mail_host,sender,password,receivers,message='',Subject='Send text',mail_port=25):
    '''
    Just send normal email. 2017-05-10
    param:mail_host str,sender str,password str,receivers list,message str,Subject str,mail_port int
    return:None
    '''
    message=MIMEText(message,'plain',__emailencoding)
    message['From']=Header(sender,__emailencoding)
    message['To']=Header(receivers[0],__emailencoding)

    message['Subject']=Header(Subject,__emailencoding)
    smtpObject=make_smtpObject(mail_host,sender,password,mail_port)
    if smtpObject:
        try:
            smtpObject.sendmail(sender,receivers,message.as_string())
            print "Send Email from %s to %s success" % (sender,receivers)
        except Exception,e:
            print str(e)
            traceback.print_exc()
            print "Send Email fail"
        finally:
            smtpObject.close()
    else:
        print "Send Email fail"

def make_smtpObject(mail_host,login_name,password,mail_port=25):
    try:
        #print (mail_host,login_name,password,mail_port)
        smtpObject=smtplib.SMTP(host=mail_host,port=int(mail_port),timeout=25)
        smtpObject.starttls()
        smtpObject.login(login_name,password)
        return smtpObject
    except Exception,e:
        traceback.print_exc()
        return None

def send_email_with_attachment(mail_host,sender,password,receivers,send_file,message_s='send file',Subject='send file',mail_port=25):
    '''
    Send email with attachment 2017-05-10
    param:mail_host str,sender str,password str,receivers list,send_file list,message str,Subjcet str,mail_port int
    return: None
    '''
    message=MIMEMultipart()
    message['From']=Header(sender,__emailencoding)
    message['To']=Header(receivers[0],__emailencoding)
    message['Subject']=Header(Subject,__emailencoding)

    text_msg=MIMEText(message_s,'plain',__emailencoding)
    message.attach(text_msg)
    for s_file in send_file:
        if os.path.exists(s_file):
            att=MIMEText(open(s_file,'rb').read(),'base64',__emailencoding)
            att['Content-Type']='application/octet-stream'
            att['Content-Disposition']='attachment; filename="%s"' % str(s_file)
            message.attach(att)

    smtpObject=make_smtpObject(mail_host,sender,password,mail_port)
    if smtpObject:
        try:
            smtpObject.sendmail(sender,receivers,message.as_string())
            print "Send Email with file success"
        except Exception,e:
            traceback.print_exc()
            print "Send email fail"
            print str(e)
        finally:
            smtpObject.close()
    else:
        print "Send email fail"

