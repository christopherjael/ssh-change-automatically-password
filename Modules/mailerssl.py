"""
Created on Thu Nov  3 15:31:48 2022

@author: Christopher Montero
"""

from email.message import EmailMessage
import ssl
import smtplib
from datetime import date

def sendemail(email_receiver, newpassword):
    email_sender='from@fromdomain.com'
    email_password = '<yourpassword>'
    
    subjet = f'Your new password - {date.today()}'
    body = f"""
    Your new password is: {newpassword}
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subjet
    em.set_content(body)
    
    context = ssl.create_default_context()

    with smtplib.SMTP('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        print ("Successfully sent email")
        