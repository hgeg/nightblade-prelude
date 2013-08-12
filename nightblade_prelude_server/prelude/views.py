# Create your views here.
from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from prelude.models import *
import json,time,helpers,hashlib

API_TOKENS = {'debfc0f39c6cea44e540':'39029904c984344b2518e9abd3be6c1ab76a99ac'}

def jsonResponse(data,status=200):
  return HttpResponse(json.dumps(data),'application/json',status)

def validate_request(request,auth=False):
  if request.method == 'POST':
    if not auth: return 0
    if 'access_token' not in request.POST: return -2
    if 'signature' not in request.POST: return -3
    return 0
  else:
    return -1

def validate_authentication(request):
  body = request.POST
  if 'access_token' not in body: return jsonResponse({'error':True,'data':{'msg':'Access token not found.'}},403)
  access_token   = body['access_token']

  if 'timestamp' not in body: return [jsonResponse({'error':True,'data':{'msg':'Timestamp not found.'}},403),1]
  timestamp = body['timestamp']
  if int(time.time()) - int(timestamp) > 3600: return [jsonResponse({'error':True,'data':{'msg':'Request too old.'}},403),1]
  
  user = Author.objects.filter(access_token=access_token)[0]
  if not user and int(user.last_access)>int(time.time())-86400: return [jsonResponse({'error':True,'data':{'msg':'Invalid access_token.'}},404),1]

  signature = body['signature']
  server_signature = hashlib.md5("%s&%s"%(user.access_token,timestamp)).hexdigest()
  if signature != server_signature:
    return [jsonResponse({'error':True,'data':{'msg':'Cannot verify the signature.'}},404),1]
  return [user,0]

@csrf_exempt
def authenticate(request):
  v = validate_request(request)
  if v==0:
    body = request.POST

    if 'api_key' not in body: return jsonResponse({'error':True,'data':{'msg':'API key not found.'}},403)
    api_key = body['api_key']
    if api_key not in API_TOKENS: return jsonResponse({'error':True,'data':{'msg':'Invalid API key.'}},403)

    
    if 'timestamp' not in body: return jsonResponse({'error':True,'data':{'msg':'Timestamp not found.'}},403) 
    timestamp = body['timestamp']
    if int(time.time()) - int(timestamp) > 3600: return jsonResponse({'error':True,'data':{'msg':'Invalid timestamp.'}},403)

    if 'username' not in body: return jsonResponse({'error':True,'data':{'msg':'Username not found.'}},403) 
    username  = body['username']
    try: user = Author.objects.filter(username=username)[0]
    except: return jsonResponse({'error':True,'data':{'msg':'User does not exist.'}},404)

    signature = body['signature']
    print "%s&%s&%s&%s"%(user.username,user.password,timestamp,API_TOKENS[api_key])
    server_signature = hashlib.md5("%s&%s&%s&%s"%(user.username,user.password,timestamp,API_TOKENS[api_key])).hexdigest()
    if signature != server_signature:
      return jsonResponse({'error':True,'data':{'msg':'Cannot verify the signature.'}},404)
    access_token = helpers.generate_token()
    user.access_token = access_token
    user.save()
    return jsonResponse({'error':False,'data':{'msg':'Successfully authenticated','access_token':access_token}},200)
  elif v==-1:
    return jsonResponse({'error':True,'data':{'msg':'All requests must be POST.'}},403)
  else:
    return jsonResponse({'error':True,'data':{'msg':'Invalid signature.'}},403)

@csrf_exempt
def main(request):
  return jsonResponse({'error':False,'data':{'msg':'Welcome to Nightblade: Prelude API.'}},200)

@csrf_exempt
def character(request,query):
  v = validate_request(request,True)
  if v==0:
    v = validate_authentication(request)
    if v[1]: return v[0]
    author = v[0]
    c = author.character
    body = request.POST
    if query=='info':
      if c:
        return jsonResponse({'error':False,'data':{'character':c.data()}},200)
      else: return jsonResponse({'error':True,'data':{'msg':'You don\'t have a character. Create one first.'}},200)
    elif query == 'inventory':
      return jsonResponse({'error':True,'data':{'msg':'Not implemented.'}},200)
    elif query == 'create':
      if not c or ('override' in body and body['override']=='yes'):
        if 'name' not in body: 
          return jsonResponse({'error':True,'data':{'msg':'Invalid parameters.'}},403)
        st,dx,iq,ht = (roll(6) for i in xrange(4))
        c = Character.objects.create(uid=helpers.create_uid(),name=body['name'],place=Place.objects.get(uid='9fe1414c6e6de144dcd4dfdde3b51b0c'),st=st,dx=dx,iq=iq,ht=ht,hp=ht+st,)
        author.character = c
        author.save()
        return jsonResponse({'error':False,'data':{'msg':'Successfully created a new character','character':c.data()}},200)
      else:
        return jsonResponse({'error':True,'data':{'msg':'You already have a character. In order to replace it, add override=yes parameter to your POST body.'}},200)

  elif v==-1:
    return jsonResponse({'error':True,'data':{'msg':'All requests must be POST.'}},403)
  elif v==-2:
    return jsonResponse({'error':True,'data':{'msg':'Invalid access token.'}},403)
  else:
    return jsonResponse({'error':True,'data':{'msg':'Invalid signature.'}},403)

def redirect(request):
  return HttpResponseRedirect('/prelude/api/v0_2/')

@csrf_exempt
def location(request,query): return NotImplemented

@csrf_exempt
def action(request,query): return NotImplemented
