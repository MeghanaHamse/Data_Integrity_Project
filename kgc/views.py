from django.shortcuts import render, get_object_or_404 ,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from  fidia.models import *
import hashlib
from django.forms.models import model_to_dict
from django.conf import settings

def index(request):   
	 return redirect('/kgc/login') 
	
def  login(request):   
	    if request.session.get('kgc_logged_in', "")=="":  
	      return render(request, 'kgc/login.html')
	    return redirect('/kgc/dashboard')  

def verifylogin(request):
  	if request.session.get('kgc_logged_in', "")=="":  
	      return redirect('/kgc/login') 
          
  	return False
    
def  login(request):    
	      if bool(request.session.get('kgc_logged_in'))==True:  
	         return redirect('/kgc/dashboard')
	      return render(request, 'kgc/login.html') 

def  loginauth(request): 
        login_error=""
        if request.POST.get("username","")=="":
          login_error=login_error+"Username required" 
        if request.POST.get("password","")=="":
          login_error=login_error+"Password required" 
		
        if login_error!="": 		    
           return render(request, 'kgc/login.html'); 
        else: 
           kgc=KGC.objects.filter(username=request.POST['username'],password=hashlib.md5(bytes(request.POST['password'], 'utf-8')).hexdigest()).first()
		    
           if kgc: 
                kgc=model_to_dict(kgc)
                kgc['kgc_logged_in']=True 
                keys=list(request.session.keys())
                for key  in keys:
                   if request.session[key]:
                      del request.session[key]
                for key,val in kgc.items():
                    request.session[key]=str(val)            
                return redirect('/kgc/dashboard')  
           else: 
                data={'login_error':"Mismatched Login Credentials<br/>"};  
                return render(request, 'kgc/login.html', data);         

def  dashboard(request):   
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
           
	    data={}
	    total=User.objects.all()
	    data['total']=total.count()
	    data['waiting']=total.filter(status=0,privatekey=None).count()
	    data['rejected']=total.filter(status=2).count()
	    data['accepted']=total.filter(status=1).count()      
	    return render(request, 'kgc/dashboard.html', data);                     
        
        
def  keyrequest(request):   
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
           
	    data={} 
	    data['waiting']=User.objects.filter(status=0,privatekey=None)
	    return render(request, 'kgc/keyrequest.html', data);  

def acceptkeyreq(request,id):
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
        
	    obj=User.objects.get(id=id)
	    privatekey=sha256sum(settings.STATICFILES_DIRS[0]+"/uploads/bimages/"+str(obj.biometricimage))        
	    obj.privatekey=privatekey
	    obj.status=1
	    obj.save()
	    chainstatus=addBlock({'userid':obj.id},'Private Key Generation');    
        
	    sendmail([obj.email],'FIDIA:Your Private key.','Your Private Key :'+privatekey);
	    return redirect('/kgc/keyrequest')  
          
def rejectkeyreq(request,id):
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify

	    obj=User.objects.get(id=id)    
	    obj.status=2
	    obj.save()
	    return redirect('/kgc/keyrequest')
           
def  users(request):   
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
           
	    data={}
	    data['total']=User.objects.all() 
	    return render(request, 'kgc/users.html', data);          
        
def  changepassword(request):   
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify  
           
	    data={}   
	    return render(request, 'kgc/changepassword.html', data); 

def  updatepassword(request):   
	    verify=verifylogin(request)
	    if verify!=False:
	       return verify
           
	    updatepassword_errors=""
	    if request.POST.get("password","")=="":
	      updatepassword_errors=updatepassword_errors+ "Current password required<br/>" 
	    if len(request.POST.get("newpassword",""))<6:
	      updatepassword_errors=updatepassword_errors+"New password of minimum 6 chars required<br/>" 
	    else:  
	      if request.POST['newpassword']!=request.POST.get("confirmpassword",False):
	         updatepassword_errors=updatepassword_errors+"Confirm password required<br/>" 
        
	    data={}
	    kgc= KGC.objects.filter(id=request.session["id"],password=hashlib.md5(bytes(request.POST['password'], 'utf-8')).hexdigest()).first()         
	    if kgc:	      
	      if updatepassword_errors=="": 
	        obj=KGC.objects.filter(id=request.session["id"]).first()
	        obj.password=hashlib.md5(bytes(request.POST['newpassword'], 'utf-8')).hexdigest()
	        obj.save()
	        data['updatepassword_success']="Your password Updated successfull";	 
	      else:
	        data['updatepassword_errors']=updatepassword_errors        
	    else:
	        updatepassword_errors=updatepassword_errors+"Wrong Current password<br/>"    
	        data['updatepassword_errors']=updatepassword_errors            
	    return render(request, 'kgc/changepassword.html', data);         