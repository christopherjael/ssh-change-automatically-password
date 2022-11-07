# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 10:29:29 2022

@author: Christopher Montero
"""

from cryptography.fernet import Fernet
import string
import secrets
from random import SystemRandom, randint


def keygen():
    clave = Fernet.generate_key()
    with open('keys.key', 'wb') as f:
        f.write(clave)

def loadkey():
    return open('keys.key','rb').read()

def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, 'rb') as file:
        file_content = file.read()
    encrypted_file = f.encrypt(file_content)
    with open(filename, 'wb') as file:
        file.write(encrypted_file)
        
def desencrypt(filename, key):
    f = Fernet(key)
    with open(filename, 'rb') as file:
        file_content = file.read()
    desencrypt_file = f.decrypt(file_content)
    with open(filename, 'wb') as file:
        file.write(desencrypt_file)


def generate_password():
    alf = string.ascii_lowercase
    alf_upper = string.ascii_uppercase
    num = string.digits
    especial = string.punctuation
    cryptogen = SystemRandom()
    p = ""
    f = ""
    for r in range(2):
        p = p +cryptogen.choice(num)

    for r in range(2):
        p = p +cryptogen.choice(alf)

    for r in range(2):
        p = p +cryptogen.choice(alf_upper)


    for r in range(2):
        p = p +cryptogen.choice(especial)
    
    t = len(p)
    list1 = []
    list1[:0] = p
    for r in range(t):
        ri = randint(0, int(len(list1)-1))
        
        f = f + list1[ri]
        list1.pop(ri)
    return f

def generate_password_secrets():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) <= 2):
            break
    
    return password
    