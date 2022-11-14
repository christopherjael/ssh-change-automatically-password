# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 09:22:23 2022

@author: Christopher Montero
"""

import csv
from os import path
from Modules.cryptography import generate_password

def readcsv(filename):
    data = []
    with open(filename) as File:  
        reader = csv.DictReader(File)
        for row in reader:
            data.append(row)
        File.close()
        return data


def writecsv(data, filename):
    if(not path.exists(filename)):
        open(filename, 'a').close()
        
    with open(filename, 'w') as File:
        fieldnames = ['name', 'password', 'email']
        writer = csv.DictWriter(File, fieldnames=fieldnames)
        writer.writeheader()
        for r in data:
            writer.writerow(r)
        File.close()

def changepassswordusers():
    users = []
    for user in readcsv('users.csv'):
        passw = generate_password()
        user['password'] = passw
        users.append(user)
    writecsv(users, 'users_temp.csv')
    print('Users file changed succesfuly')