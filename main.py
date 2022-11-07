# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 10:38:09 2022

@author: Christopher Montero
"""

import wexpect

from getpass import getpass
from datetime import date
from os import path

import Modules.cryptography as cryptog
from Modules.mailer import sendemail

#====================Change Password==========================
def change_password(child, user, oldpassword, newpassword):
    child.sendline('passwd')
    child.expect('Enter existing login password: ')
    child.sendline(oldpassword)
    child.expect('New Password: ')
    child.sendline(newpassword)
    child.expect('Re-enter new Password: ')
    child.sendline(newpassword)
    print('\n Password change succesfull')
    child.kill()
    return
#=========================================


#=====================Main==========================
def main():
    passgen = cryptog.generate_password()
    
    logfile = open ('./logs.log','a')
    logfile.write(f'\nPasswords generated on {date.today()}\n')
    
    with open('./emails.mail') as f:
        lineas = f.readlines()
        for linea in lineas:
            passgen = cryptog.generate_password()
            logfile.write(passgen+'\n')
            print(passgen)
            print(linea.strip('\n'))
            sendemail(linea.strip('\n'), passgen)
    logfile.close()
    
    host = str(input('Hostname|IP: '))
    user = str(input("Username: "))
    oldpassword = getpass("Password: ")
    newpassword = getpass("New Password: ")
    child = wexpect.spawn('cmd.exe')
    child.expect('>')
    child.sendline(f"ssh {user}@{host}")
    r = child.expect(['Password: ', '(yes/no/[fingerprint])? '])
    if r == 1:
        child.sendline('yes')
        child.expect('Password: ')
    child.sendline(oldpassword)
    child.expect('[#\$]')
    change_password(child, user, oldpassword, newpassword)
#================================================


if(path.exists('keys.key')):
    key = cryptog.loadkey()
    cryptog.desencrypt('./logs.log', key)
    main()
    cryptog.encrypt('./logs.log', key)
else:
    cryptog.keygen()
    key = cryptog.loadkey()
    main()
    cryptog.encrypt('./logs.log', key)
    
    
    