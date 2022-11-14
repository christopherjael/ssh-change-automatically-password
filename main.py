# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 10:38:09 2022

@author: Christopher Montero
"""

import wexpect
from datetime import date
from os import path, remove
import sys

import Modules.cryptography as cryptog
from Modules.mailer import sendemail
from Modules.csvreader import readcsv, writecsv

#====================Change Password==========================
def change_password(child, oldpassword, newpassword):
    child.sendline('passwd')
    child.expect('[Enter existing login password: /(current) UNIX password: /Current password]')
    child.sendline(oldpassword)
    child.expect('[New Password: /Enter new UNIX password: ]')
    child.sendline(newpassword)
    child.expect('[Re-enter new Password: /Retype new UNIX password: ]')
    child.sendline(newpassword)
    child.kill()
    print('\nPassword change succesfull')
#=========================================

def updatelogfile(users):
    logfile = open ('./logs.log','a')
    logfile.write(f'\nPasswords generated on {date.today()}\n')
    for user in users:
        logfile.write(user['password'])
    logfile.close()


def notifybyemail(users):
    for user in users:
        sendemail(user['email'], user['password'])
    print('Notificacion Completada Exitosamente')


#=====================Main==========================
def main():

    userswithnewpassword = []
    for user in readcsv('users.csv'):
        #passw = cryptog.generate_password()
        user['password'] = '1cdlinterf'
        userswithnewpassword.append(user)
    
    writecsv(userswithnewpassword, 'users_temp.csv')
    
    for server in readcsv('./servers.csv'):
        for newuser, olduser in zip(userswithnewpassword, readcsv('users.csv')):
            host = server['host']
            user = olduser['name']
            oldpassword = olduser['password']
            newpassword = newuser['password']	
            child = wexpect.spawn('cmd.exe')
            print(f'Logining with User: {user} Host: {host}')
            child.expect('>')
            child.sendline(f"ssh {user}@{host}")
            r = child.expect(['Password: ', '(yes/no/[fingerprint])? '])
            if r == 1:
                child.sendline('yes')
                child.expect('[password: /Password: ]')
            child.sendline(oldpassword)
            child.expect('[#\$]')
            change_password(child, oldpassword, newpassword)
    
    writecsv(readcsv('users_temp.csv'), 'users.csv')
    remove('users_temp.csv')
    updatelogfile(readcsv('users.csv'))
    notifybyemail(readcsv('users.csv'))
    
#================================================


if __name__ == '__main__':
    if(not path.exists('users.csv') and not path.exists('servers.csv')):
        print('Se necesita los archivo (users.csv y servers.csv) en la carpeta raiz')
        sys.exit()

    if(path.exists('keys.key')):
        key = cryptog.loadkey()
        try:
            print('keygen')
            cryptog.desencrypt('./logs.log', key)
            cryptog.desencrypt('./servers.csv', key)
            cryptog.desencrypt('./users.csv', key)
            main()
        except Exception as err:
            print('Error al ejecturar el main\n', err)
        finally:
            cryptog.encrypt('./logs.log', key)
            cryptog.encrypt('./servers.csv', key)
            cryptog.encrypt('./users.csv', key)
    else:
        print('Keygen')
        cryptog.keygen()
        key = cryptog.loadkey()
        try:
            main()
        except Exception as err:
            print('erro al ejectuar el main\n',err)
        finally:
            cryptog.encrypt('./logs.log', key)
            cryptog.encrypt('./servers.csv', key)
            cryptog.encrypt('./users.csv', key)
    
    