#!/usr/bin/python
import hashlib,json,sys,time,urllib2,shelve

BASE_URL = "http://localhost:8282/prelude/api/v0_2/"
API_KEY 
API_SECRET
USERNAME
PASSWORD

def auth():
  c = shelve.open('client')
  try:
    op = sys.argv[2]
    url = BASE_URL + "auth/"
  except: return "Invalid arguments."
  timestamp = int(time.time())
  try:
    access_token = c['access_token']
  except: return "Cannot find access token! Try running auth first."
  signature = hashlib.md5("%s&%s&%s&%s"%(USERNAME,PASSWORD,timestamp,API_SECRET)).hexdigest()
  data = str(json.dumps({'access_token':access_token,'timestamp':timestamp,'signature':signature}))
  headers = {'Content-Type':'application/json; charset=utf-8'}
  opener = urllib2.build_opener(urllib2.HTTPHandler)
  req = urllib2.Request(url,data,headers)
  req.get_method = lambda: 'POST'
  raw = opener.open(req).read()
  c.close()

def request():
  c = shelve.open('client')
  try:
    op = sys.argv[2]
    su = sys.argv[4]
    xt = sys.argv[6]
    url = BASE_URL + op + ":" + su + "/"
  except: return "Invalid arguments."

  timestamp = int(time.time())
  try:
    access_token = c['access_token']
  except: return "Cannot find access token! Try running auth first."
  signature = hashlib.md5("%d&%s"%(timestamp,access_token)).hexdigest()

  dct = {'access_token':access_token,'timestamp':timestamp,'signature':signature}
  dct.update(json.loads(xt))
  data = str(json.dumps(dct))
  headers = {'Content-Type':'application/json; charset=utf-8'}
  opener = urllib2.build_opener(urllib2.HTTPHandler)
  req = urllib2.Request(url,data,headers)
  req.get_method = lambda: 'POST'
  raw = opener.open(req).read()
  c.close()