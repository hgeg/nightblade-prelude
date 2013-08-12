import os,hashlib,base64
from random import randint;

def create_uid(): return hashlib.md5(os.urandom(128)).hexdigest()

def generate_token(): return base64.b64encode(hashlib.md5(os.urandom(128)).hexdigest())

def roll(sides=6, num=1): return sum((randint(1,sides) for e in xrange(num)))