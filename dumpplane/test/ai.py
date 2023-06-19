#!/usr/bin/python3

import re

string = "# configuration file /etc/nginx/nginx.conf:"
pattern = r'\s+\S+.conf:'
match = re.match(pattern, string)
if match:
    print(match.group(0))
    print(match.group(1))
