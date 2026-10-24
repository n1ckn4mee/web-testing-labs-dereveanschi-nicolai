from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import json,os,secrets,threading,time
from http.cookies import SimpleCookie
ROOT=Path(__file__).parent;SESS={};LOCK=threading.Lock();PWD=os.environ['LAB_TEST_PASSWORD']
ITEMS=[{'id':s,'name':n,'price':p} for s,n,p in [('sauce-labs-backpack','Sauce Labs Backpack',29.99),('sauce-labs-bike-light','Sauce Labs Bike Light',9.99),('sauce-labs-bolt-t-shirt','Sauce Labs Bolt T-Shirt',15.99),('sauce-labs-fleece-jacket','Sauce Labs Fleece Jacket',49.99),('sauce-labs-onesie','Sauce Labs Onesie',7.99),('test-allthethings-t-shirt','Test AllTheThings T-Shirt',15.99)]]
class H(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def session(self):
  c=SimpleCookie();c.load(self.headers.get('Cookie',''));t=c.get('session');return SESS.get(t.value) if t else None
 def send(self,data,status=200,cookie=None):
  raw=json.dumps(data,ensure_ascii=False).encode() if isinstance(data,(dict,list)) else data
  self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8' if isinstance(data,(dict,list)) else 'text/html; charset=utf-8');self.send_header('Content-Length',str(len(raw)))
  if cookie:self.send_header('Set-Cookie',cookie)
  self.end_headers();self.wfile.write(raw)
  with LOCK:
   with (ROOT/'http-clean.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps({'time':time.time(),'method':self.command,'path':self.path.split('?')[0],'status':status,'session_present':self.session() is not None})+'\n')
 def do_GET(self):
  if self.path.startswith('/api/state'):
   s=self.session();self.send({'authenticated':bool(s),'items':ITEMS,'cart':s['cart'] if s else []});return
  self.send((ROOT/'index.html').read_bytes())
 def do_POST(self):
  data=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))) or '{}')
  if self.path=='/api/login':
   u=data.get('user','');p=data.get('password','')
   msg=('Epic sadface: Username is required' if not u else 'Epic sadface: Sorry, this user has been locked out.' if u=='locked_out_user' else 'Epic sadface: Username and password do not match any user in this service' if u!='standard_user' or p!=PWD else '')
   if msg:self.send({'error':msg},401);return
   t=secrets.token_hex(24);SESS[t]={'cart':[]};self.send({'ok':True},cookie='session='+t+'; HttpOnly; SameSite=Lax; Path=/');return
  s=self.session()
  if not s:self.send({'error':'Unauthorized'},401);return
  if self.path=='/api/cart':
   if data['action']=='add' and data['id'] not in s['cart']:s['cart'].append(data['id'])
   elif data['action']=='remove' and data['id'] in s['cart']:s['cart'].remove(data['id'])
   self.send({'cart':s['cart']});return
  if self.path=='/api/checkout':
   for key,msg in [('first','First Name'),('last','Last Name'),('code','Postal Code')]:
    if not data.get(key):self.send({'error':'Error: '+msg+' is required'},400);return
   self.send({'ok':True});return
  if self.path=='/api/finish':s['cart']=[];self.send({'ok':True});return
  self.send({'error':'Unknown'},404)
print('Local Study Shop 2.0 listening on 127.0.0.1:8010',flush=True)
ThreadingHTTPServer(('127.0.0.1',8010),H).serve_forever()
