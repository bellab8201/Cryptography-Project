#!/usr/bin/python3
# coding: latin-1

blob = """             y�Ɔf�6�;G��k���	P�(0��)Q�������\W���`��y
�]�I"-�u�+�[, !9���ڡ��?1et���'�&�~���ge��z�Y7Oɨ<7:4���&[����|(
"""
good = "Use SHA-256 instead!"
evil = "MD5 is perfectly secure!"
from hashlib import sha256
from urllib.parse import quote
x = len(quote(blob))
if x == 303:
    print(good)
else:
    print(evil)