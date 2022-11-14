# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:49:39 2022

@author: Christopher Montero
"""

import Modules.cryptography as crypto


filename = input('filename: ')
key = crypto.loadkey()
option = input('Option (en)crypt | (des)encrypt: ')

if option == 'en':
    crypto.encrypt(filename, key)
    print('Encrypter complete')
elif option == 'des':
    crypto.desencrypt(filename, key)
    print('Desncrypter complete')