#!/usr/bin/python3

import re

s = 'tutorialspoint is a great platform to enhance your skills'
result = re.search(r'\w+$', s)
print(result.group())


