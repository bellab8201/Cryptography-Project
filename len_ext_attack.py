#!/usr/bin/python3

import sys
from urllib.parse import quote, urlparse
from pymd5 import md5, padding


##########################
# Example URL parsing code:
res = urlparse('https://project1.ecen4133.org/test/lengthextension/api?token=41bd1ccd26a75c282922c2b39cc3bb0a&command=Test1')
# res.query returns everything after '?' in the URL:
assert(res.query == 'token=41bd1ccd26a75c282922c2b39cc3bb0a&command=Test1')

###########################
# Example using URL quoting
# This is URL safe: a URL with %00 will be valid and interpreted as \x00
assert(quote('\x00\x01\x02') == '%00%01%02')

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print(f"usage: {sys.argv[0]} URL_TO_EXTEND", file=sys.stderr)
        sys.exit(-1)

    # Get url from command line argument (argv)
    url = sys.argv[1]

    #url = 'https://project1.ecen4133.org/autograder/lengthextension/api?token=f1bb7d2c97b5bfb207bc2fcaf961e76c&command=Test1&command=GradeProject&command=NoOp'

    #################################
    # Your length extension code here
    url_parse = urlparse(url) 


    token = url_parse.query # This is the portion of the URL from 'token=' and onwards
    scheme = url_parse.scheme
    netloc = url_parse.netloc
    path = url_parse.path


    commands = token.split('&', 1)
    concat_commands = commands[1]+"&command=UnlockSafes"



    length_of_m = len(commands[1]) + 8
    bits = (length_of_m + len(padding(length_of_m*8)))*8

    original_token = token.split('&')[0]
    original_token = original_token.split('=')[1]

    
    pad = quote(padding(length_of_m*8))
    
    # Initialize the hash object
    h = md5(state=bytes.fromhex(original_token), count=bits)
    # Compression function appending UnlockSafes to the original token
    h.update("&command=UnlockSafes")
    # Generate new token that includes the command UnlockSafes
    new_token = h.hexdigest()
    # Add padding to url in order to ...
    print(scheme + "://" + netloc + path + "?" + "token=" + new_token + "&" + commands[1] + pad + "&command=UnlockSafes")
