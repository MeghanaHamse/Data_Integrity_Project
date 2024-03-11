from django.shortcuts import render, get_object_or_404 ,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from  fidia.models import *
import hashlib
from django.forms.models import model_to_dict
import random
import os	
from django.conf import settings
import json
import base64
import datetime

def index(request):   
	 return redirect('/user/login') 
	
def  login(request):   
	    if request.session.get('user_logged_in', "")=="":  
	      return render(request, 'user/login.html')
	    return redirect('/user/dashboard')  

def verifylogin(request):
  	if request.session.get('user_logged_in', "")=="":  
	      return redirect('/user/login')  
    
  	if int(request.session.get('status', 0))!=1:  
	      return render(request, 'user/verify.html')     

  	return False
    
def  login(request):    
	      if bool(request.session.get('user_logged_in', False))==True:  
	        return redirect('/user/dashboard')
	      return render(request, 'user/login.html') 

def  loginauth(request): 
        login_error=""
        if request.POST.get("emailid","")=="":
          login_error=login_error+"Emailid required" 
        if request.POST.get("password","")=="":
          login_error=login_error+"Password required" 
		
        if login_error!="": 		    
           return render(request, 'user/login.html'); 
        else: 
           user=True  
           user= User.objects.filter(email=request.POST['emailid'],password=hashlib.md5(bytes(request.POST['password'], 'utf-8')).hexdigest()).first()
		    
           if user: 
                user=model_to_dict(user)
                user['user_logged_in']=True 
                keys=list(request.session.keys())
                for key  in keys:
                   if request.session[key]:
                      del request.session[key]                
                for key,val in user.items():
                    request.session[key]=str(val)            
                return redirect('/user/dashboard')  
           else: 
                data={'login_error':"Mismatched Login Credentials<br/>"};  
                return render(request, 'user/login.html', data);         

def  dashboard(request):   
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
           
	    data={}  
	    data['total']=Fileuploads.objects.filter(userid=request.session['id']).count()
	    data['auditrequests']=Auditrequest.objects.filter(userid=request.session['id']).count()
	    data['tpaaudited']=Auditrequest.objects.filter(userid=request.session['id'],tpaverification=1).count()
	    data['useraudited']=Auditrequest.objects.filter(userid=request.session['id'],userverification=1).count()
	    return render(request, 'user/dashboard.html', data);                     

def  changepassword(request):   
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
           
	    data={}   
	    return render(request, 'user/changepassword.html', data); 

def  updatepassword(request):   
	    updatepassword_errors=""
	    if request.POST.get("password","")=="":
	      updatepassword_errors=updatepassword_errors+ "Current password required<br/>" 
	    if len(request.POST.get("newpassword",""))<6:
	      updatepassword_errors=updatepassword_errors+"New password of minimum 6 chars required<br/>" 
	    else:  
	      if request.POST['newpassword']!=request.POST.get("confirmpassword",False):
	         updatepassword_errors=updatepassword_errors+"Confirm password required<br/>" 
        
	    data={}
	    user= User.objects.filter(id=request.session["id"],password=hashlib.md5(bytes(request.POST['password'], 'utf-8')).hexdigest()).first()         
	    if user:	      
	      if updatepassword_errors=="": 
	        obj=User.objects.filter(id=request.session["id"]).first()
	        obj.password=hashlib.md5(bytes(request.POST['newpassword'], 'utf-8')).hexdigest()
	        obj.save()
	        data['updatepassword_success']="Your password Updated successfull";	 
	      else:
	        data['updatepassword_errors']=updatepassword_errors        
	    else:
	        updatepassword_errors=updatepassword_errors+"Wrong Current password<br/>"    
	        data['updatepassword_errors']=updatepassword_errors            
	    return render(request, 'user/changepassword.html', data); 
        
def  fileupload(request):   
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify 
          
	    data={}   
	    return render(request, 'user/fileupload.html', data);         

def filetocloud(request):
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify

	    if request.FILES.get("file","")=="": 
	       return HttpResponse(json.dumps({"success":0,"message":"File required"}), content_type='application/json')
          
	    file=request.FILES['file']
	    clouds = [d for d in os.listdir(settings.CLOUD_DIRS[0]) if os.path.isdir(os.path.join(settings.CLOUD_DIRS[0], d))]
	    obj=Fileuploads()
	    obj.userid=request.session['id']
	    obj.filename=file.name 
	    obj.cloudname=clouds[random.randint(0, len(clouds)-1)]
	    obj.save() 
	    dest = open(settings.CLOUD_DIRS[0]+"/"+obj.cloudname+"/"+str(obj.id), 'wb')
	    dest.write(file.read())
	    dest.close()
	    chainstatus=addBlock({'id':obj.id,'userid':obj.userid,'cloudname':obj.cloudname,'filename':obj.filename},'File upload');            
	    return HttpResponse(json.dumps({"success":1,'id':obj.id,"message":"File Uploaded Successfully<br/>"+chainstatus['message']}), content_type='application/json')  

def encryptfile(request,id):
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
          
	    obj=Fileuploads.objects.get(id=id)   
	    obj.key=Fernet.generate_key()
	    obj.hashcode=sha256sum(settings.CLOUD_DIRS[0]+"/"+obj.cloudname+"/"+str(obj.id))
	    obj.save() 
	    encfile(settings.CLOUD_DIRS[0]+"/"+obj.cloudname+"/"+str(obj.id),obj.key)        
	    return HttpResponse("ok")  
        
def  myfiles(request):   
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
           
	    files=Fileuploads.objects.filter(userid=request.session['id'])   
	    data={'files':[]}
	    for f in files:
	        lastaudited=Auditrequest.objects.filter(fileid=f.id,tpaverification=1).first()
	        if lastaudited:
	           lastaudited=lastaudited.tpaverifiedat 
	        else:
	           lastaudited="Not Audited"
               
	        data['files'].append({'id':f.id,'filename':f.filename,'creationDate':f.creationDate,'hashcode':f.hashcode,'lastaudited':lastaudited})
            
	    return render(request, 'user/myfiles.html', data);  

def  auditrequest(request):   
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
           
	    files=Fileuploads.objects.filter(userid=request.session['id'])   
	    data={'files':[]}
	    for f in files:
	        lastaudited=Auditrequest.objects.filter(fileid=f.id,tpaverification=1).first()
	        if lastaudited:
	           lastaudited=lastaudited.tpaverifiedat 
	        else:
	           lastaudited="Not Audited"
               
	        data['files'].append({'id':f.id,'filename':f.filename,'creationDate':f.creationDate,'hashcode':f.hashcode,'lastaudited':lastaudited})
            
	    return render(request, 'user/auditrequest.html', data);     

def requesttpaaudit(request,id):
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
          
	    obj=Fileuploads.objects.get(id=id)  
	    reqobj=Auditrequest()
	    reqobj.fileid=id
	    reqobj.userid=request.session['id'] 
	    reqobj.save()
	    return redirect('/user/proofcheck')  
        
def  proofcheck(request):   
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
           
	    files=Auditrequest.objects.filter(userid=request.session['id'],userverification=0).order_by('-id')   
	    data={'files':[]}
	    for f in files:
	        fileobj=Fileuploads.objects.get(id=f.fileid) 
	        status=''
	        if f.tpastatus==0:
	           status='Waiting at TPA'
	        elif f.tpastatus==1 and f.cloudstatus==0:
	           status='Waiting at Cloud'
	        elif f.tpastatus==1 and f.cloudstatus==1:
	           status='Cloud sent response'   
	        if f.tpastatus==1 and f.cloudstatus==1 and f.userverification==1:
	           status='You Audited and verified'
	        if f.tpastatus==1 and f.cloudstatus==1 and f.tpaverification==1:
	           status='TPA Audited and verified'
                              
	        data['files'].append({'id':fileobj.id,'requestid':f.id,'filename':fileobj.filename,'requestedAt':f.creationDate,'hashcode':fileobj.hashcode,'status':status,'cloudhashresult':f.cloudhashresult})
             
	    return render(request, 'user/proofcheck.html', data);          
        
def verifyaudit(request,id):
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify   
          
	    data=model_to_dict(Auditrequest.objects.filter(id=id).first())
	    data['file']=model_to_dict(Fileuploads.objects.get(id=data['fileid']))         
	    return render(request, 'user/verifyaudit.html', data);   
        
def verifyauditdb(request):
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify   
          
	    if request.POST.get("requestid","")=="":
	       return HttpResponse("Request ID required") 
	    
	    obj=Auditrequest.objects.filter(id=request.POST['requestid']).first()   
	    obj.userverification=1  
	    obj.userverifiedat= datetime.datetime.now()
	    obj.save()
	    return redirect('/user/proofcheck')          