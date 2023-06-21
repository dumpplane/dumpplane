#!/usr/bin/python3

import base64

with open("test.conf", 'r') as file:
    content = file.read()
    encoded_bytes = base64.b64encode(bytes(content,'utf-8'))
    print(encoded_bytes.decode())
