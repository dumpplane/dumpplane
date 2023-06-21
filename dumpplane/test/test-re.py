#!/usr/bin/python3

import re

s = 'tutorialspoint is a great platform to enhance your skills'
result = re.search(r'\w+$', s)
print(result.group())

a = "mongodb://mongodb0.example.com:27017"
b = "mongodb+srv://server.example.com/"
c = "mongodb://mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl"

re.match(r'(ftp|http)://.*\.(jpg|png)$', a)
