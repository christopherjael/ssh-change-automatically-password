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
    
    subjet = f'Nueva contraseña - {date.today()}'
    
    body = f"""
    Tu nueva contraseña de acceso es: {newpassword}
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subjet
    em.set_content(body)
    
    try:
        with smtplib.SMTP('mail.smtp.com') as smtp:
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            print ("Successfully sent email")
    except smtplib.SMTPException:
        print ("Error to sent email")

    