# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 15:31:48 2022

@author: Christopher Montero
"""

from email.message import EmailMessage
import smtplib
from datetime import date

def sendemail(email_receiver, newpassword):
    email_sender='from@fromdomain.com'
    
    subjet = f'New Password - {date.today()}'
    
    body = f"""
    Your new password is: {newpassword}
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subjet
    em.set_content(body)
    
    try:
        with smtplib.SMTP('smtp-server-name') as smtp:
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            print ("Successfully sent email")
    except smtplib.SMTPException:
        print ("Error to sent email")

    