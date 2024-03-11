from django.db import models  
from django.db import connection 
from datetime import datetime 
import hashlib
from django.core.mail import send_mail
from cryptography.fernet import Fernet
import os
import gzip
import shutil 
from django.conf import settings
import requests
import json  

def addBlock(transaction,block_type):
    apiurl=settings.BCAPI_URL
    req=requests.post(apiurl+'add_block/', data = {'transaction':json.dumps(transaction),'block_type':block_type})    
    return json.loads(req.text)  

def getBlock(index):
    apiurl=settings.BCAPI_URL
    req=requests.get(apiurl+'get_block/'+str(index))    
    return json.loads(req.text)  
    
def validateBlock(index,transaction):
    apiurl=settings.BCAPI_URL
    req=requests.post(apiurl+'validate_block/', data = {'transaction':json.dumps(transaction),'index':index})    
    return json.loads(req.text)["valid"]

def validateBlockchain():
    apiurl=settings.BCAPI_URL
    req=requests.get(apiurl+'is_chain_valid')    
    return req.text
    
def getBlockchain():
    apiurl=settings.BCAPI_URL
    req=requests.get(apiurl+'get_chain')  
    return json.loads(req.text)    

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()

def encfile(filename,key):
    f = Fernet(key)

    with open(filename, 'rb') as original_file:
       original = original_file.read()

    encrypted = gzip.compress(f.encrypt(original))
    
    with open(filename, 'wb') as filetowrite:
        filetowrite.write(encrypted)
        
    return True 

def moddecompressfile(filename):
  try:  
    with open(filename, 'rb') as original_file:
       original = gzip.decompress(original_file.read())
       
    with open(filename+".decomp", 'wb') as filetowrite:
        filetowrite.write(original)  
  except:
    with open(filename+".decomp", 'wb') as filetowrite:
        filetowrite.write(bytes('Error in decompressing','UTF-8'))     
    return True
   
def moddecryptfile(filename,key):
  try:  
    f = Fernet(key)     
    
    with open(filename+".decomp", 'rb') as original_file:
       original = f.decrypt(original_file.read())
    
    with open(filename+".dec", 'wb') as filetowrite:
       filetowrite.write(original)    
    
    os.remove(filename+".decomp")  
  except:
    with open(filename+".dec", 'wb') as filetowrite:
        filetowrite.write(bytes('Unable to generate Hashcode','UTF-8'))  
    return True
    
def modfilesignature(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename+".dec", 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    os.remove(filename+".dec")        
    return h.hexdigest()
    
    
def sha256sumencfile(filename,key):
    f = Fernet(key)

    with open(filename, 'rb') as original_file:
       original = gzip.decompress(original_file.read())

    with open(filename+".dec", 'wb') as filetowrite:
        filetowrite.write(f.decrypt(original)) 
    
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename+".dec", 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    os.remove(filename+".dec")        
    return h.hexdigest()        
    
def sendmail(to,subject,msg):
  send_mail(
    subject,
    msg,
    'kgc@fidia.com',
    to,
    fail_silently=True,
  )    
            
class User(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    birthdate = models.DateField() 
    password = models.CharField(max_length=200) 
    country=models.CharField(max_length=200) 
    city=models.CharField(max_length=200) 
    biometricimage=models.TextField()
    privatekey=models.TextField(null=True) 
    status=models.IntegerField(default=0)
    creationDate = models.DateTimeField(auto_now_add=True)
    UpdationDate = models.DateTimeField(auto_now=True, null=True) 
 

          
class KGC(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)         

class TPA(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)    
    
class Cloud(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)    
    
    
class Fileuploads(models.Model):
    id = models.AutoField(primary_key=True)
    userid=models.IntegerField()
    filename=models.CharField(max_length=200)
    hashcode=models.TextField() 
    key=models.BinaryField() 
    cloudname= models.CharField(max_length=200)  
    creationDate = models.DateTimeField(auto_now_add=True)
    UpdationDate = models.DateTimeField(auto_now=True, null=True)   

class Auditrequest(models.Model):    
    id = models.AutoField(primary_key=True)
    userid=models.IntegerField()
    fileid=models.IntegerField()
    tpastatus=models.IntegerField(default=0)
    tpaat=models.DateTimeField(null=True)
    cloudstatus=models.IntegerField(default=0)
    cloudauditat=models.DateTimeField(null=True)
    cloudhashresult=models.TextField(null=True) 
    tpaverification=models.IntegerField(default=0)
    tpaverifiedat=models.DateTimeField(null=True)
    userverification=models.IntegerField(default=0)
    userverifiedat=models.DateTimeField(null=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    UpdationDate = models.DateTimeField(auto_now=True, null=True)    