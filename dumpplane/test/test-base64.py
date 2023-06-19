#!/usr/bin/python3

import base64

a = "Hello"
encoding = base64.b64encode(a.encode())
print(encoding)

