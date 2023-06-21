#!/usr/bin/python3

'''
bash example:

 % echo "Hello World NGINX" | base64 
SGVsbG8gV29ybGQgTkdJTlgK

% echo SGVsbG8gV29ybGQgTkdJTlgK | base64 --decode
Hello World NGINX
'''

import base64

print()

origin = "Hello World NGINX"
origin_bytes = bytes(origin,'utf-8')
print(origin)
print(origin_bytes)
print()

encoded_bytes = base64.b64encode(origin_bytes)
encoding = encoded_bytes.decode()
print(encoded_bytes)
print(encoding)
print()

encoding_bytes = bytes(encoding,'utf-8') 
decoding_bytes = base64.b64decode(encoding_bytes)
decoding = decoding_bytes.decode() 
print(decoding_bytes)
print(decoding)
print()
