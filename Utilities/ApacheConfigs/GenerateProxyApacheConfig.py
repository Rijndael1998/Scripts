#!/bin/python

import json
from os import system
from sys import argv


if len(argv) != 2:
    print("Incorrect number of arguments. Use one argument to specify the output folder.")
    quit(1)

folderLocation = argv[1]
print("dumping into:", folderLocation)

try:
    with open("proxy-websites.json") as f:
        config = json.loads(f.read())

except FileNotFoundError:
    with open("proxy-websites.json.sample") as f:
        config = json.loads(f.read())


for website in config:
    domain = website["domain"]
    reverse = website["reverse"]
    keys = website["keys"]

    print("Processing:", domain)

    system("./CreateSecureRedirect.sh \"{}\" > \"{}\"".format(
        domain, 
        "{}/{}.conf".format(
            folderLocation, 
            domain
        )
    ))

    system("./CreateSSLReverseProxy.sh \"{}\" \"{}\" \"{}\" > \"{}\"".format(
        domain,
        reverse,
        keys,
        "{}/{}-le-ssl.conf".format(
            folderLocation, 
            domain
        )
    ))
