from django.shortcuts import render, get_object_or_404 ,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from  fidia.models import *
from django.forms.models import model_to_dict
import  datetime

def index(request):   
	 return redirect('/tpa/login') 
	  
def  login(request):    
	    if bool(request.session.get('tpa_logged_in', False))==True:  
	       return redirect('/tpa/dashboard')
          
	    return render(request, 'tpa/login.html') 

def  loginauth(request): 
        login_error=""
        if request.POST.get("username","")=="":
          login_error=login_error+"Username required" 
        if request.POST.get("password","")=="":
          login_error=login_error+"Password required" 
		
        if login_error!="": 		    
           return render(request, 'tpa/login.html'); 
        else: 
           tpa=True  
           tpa= TPA.objects.filter(username=request.POST['username'],password=hashlib.md5(bytes(request.POST['password'], 'utf-8')).hexdigest()).first()
		    
           if tpa: 
                tpa=model_to_dict(tpa)
                tpa['tpa_logged_in']=True 
                keys=list(request.session.keys())
                for key  in keys:
                   if request.session[key]:
                      del request.session[key]                
                for key,val in tpa.items():
                    request.session[key]=str(val)            
                return redirect('/tpa/dashboard')  
           else: 
                data={'login_error':"Mismatched Login Credentials<br/>"};  
                return render(request, 'tpa/login.html', data);         

def  dashboard(request):   
	    if request.session.get('tpa_logged_in', "")=="":  
	      return redirect('/tpa/login')
           
	    data={}  
	    data['total']=Auditrequest.objects.all().count()
	    data['senttotpa']=Auditrequest.objects.filter(tpastatus=0,cloudstatus=0).count()
	    data['senttocloud']=Auditrequest.objects.filter(tpastatus=1,cloudstatus=0).count()
	    data['sentfromcloud']=Auditrequest.objects.filter(tpastatus=1,cloudstatus=1).count()
	    data['tpaaudited']=Auditrequest.objects.filter(tpaverification=1).count()
	    data['useraudited']=Auditrequest.objects.filter(userverification=1).count()
	    return render(request, 'tpa/dashboard.html', data); 
        
def  auditrequest(request):   
	    if request.session.get('tpa_logged_in', "")=="":  
	       return redirect('/tpa/login')
           
	    data={}  
	    files=Auditrequest.objects.filter(tpastatus=0,cloudstatus=0).order_by('-id')   
	    data={'files':[]}
	    for f in files:
	        fileobj=Fileuploads.objects.get(id=f.fileid)
	        username=User.objects.get(id=fileobj.userid).fullname  
	        data['files'].append({'id':fileobj.id,'username':username,'requestid':f.id,'filename':fileobj.filename,'requestedAt':f.creationDate})
         
	    return render(request, 'tpa/auditrequest.html', data);          

def sendarequesttocloud(request,id):
	    if request.session.get('tpa_logged_in', "")=="":  
	       return redirect('/tpa/login')  
          
	    obj=Auditrequest.objects.filter(id=id).first()   
	    obj.tpastatus=1  
	    obj.tpaat= datetime.datetime.now()
	    obj.save()
	    return redirect('/tpa/requestcloud')         
        
def  requestcloud(request):   
	    if request.session.get('tpa_logged_in', "")=="":  
	       return redirect('/tpa/login')
           
	    data={}  
	    files=Auditrequest.objects.filter(tpastatus=1,cloudstatus=0).order_by('-id')   
	    data={'files':[]}
	    for f in files:
	        fileobj=Fileuploads.objects.get(id=f.fileid)
	        username=User.objects.get(id=fileobj.userid).fullname  
	        data['files'].append({'id':fileobj.id,'username':username,'requestid':f.id,'filename':fileobj.filename,'requestedtpa':f.creationDate,'requestedcloud':f.tpaat})
         
	    return render(request, 'tpa/requestcloud.html', data);   

def  proofcheck(request):   
	    if request.session.get('tpa_logged_in', "")=="":  
	       return redirect('/tpa/login')
           
	    data={}  
	    files=Auditrequest.objects.filter(tpastatus=1,cloudstatus=1,tpaverification=0).order_by('-id')   
	    data={'files':[]}
	    for f in files:
	        fileobj=Fileuploads.objects.get(id=f.fileid)
	        username=User.objects.get(id=fileobj.userid).fullname  
	        data['files'].append({'id':fileobj.id,'username':username,'requestid':f.id,'filename':fileobj.filename,'requestedtpa':f.creationDate,'requestedcloud':f.tpaat,'cloudresponseat':f.cloudauditat})
         
	    return render(request, 'tpa/proofcheck.html', data);        
        
def verifyaudit(request,id):
	    if request.session.get('tpa_logged_in', "")=="":  
	       return redirect('/tpa/login') 
          
	    data=model_to_dict(Auditrequest.objects.filter(id=id).first())
	    data['file']=model_to_dict(Fileuploads.objects.get(id=data['fileid']))     
	    data['username']=User.objects.get(id=data['file']['userid']).fullname          
	    return render(request, 'tpa/verifyaudit.html', data);   
        
def verifyauditdb(request):
	    if request.session.get('tpa_logged_in', "")=="":  
	        return redirect('/tpa/login')
          
	    if request.POST.get("requestid","")=="":
	       return HttpResponse("Request ID required") 
	    
	    obj=Auditrequest.objects.filter(id=request.POST['requestid']).first()   
	    obj.tpaverification=1  
	    obj.tpaverifiedat= datetime.datetime.now()
	    obj.save()
	    return redirect('/tpa/proofcheck')              
        
        
def  changepassword(request):   
	    if request.session.get('tpa_logged_in', "")=="":  
	       return redirect('/tpa/login') 
           
	    data={}   
	    return render(request, 'tpa/changepassword.html', data); 

def  updatepassword(request):   
	    if request.session.get('tpa_logged_in', "")=="":  
	       return redirect('/tpa/login') 
           
	    updatepassword_errors=""
	    if request.POST.get("password","")=="":
	      updatepassword_errors=updatepassword_errors+ "Current password required<br/>" 
	    if len(request.POST.get("newpassword",""))<6:
	      updatepassword_errors=updatepassword_errors+"New password of minimum 6 chars required<br/>" 
	    else:  
	      if request.POST['newpassword']!=request.POST.get("confirmpassword",False):
	         updatepassword_errors=updatepassword_errors+"Confirm password required<br/>" 
        
	    data={}
	    tpa= TPA.objects.filter(id=request.session["id"],password=hashlib.md5(bytes(request.POST['password'], 'utf-8')).hexdigest()).first()         
	    if tpa:	      
	      if updatepassword_errors=="": 
	        obj=TPA.objects.filter(id=request.session["id"]).first()
	        obj.password=hashlib.md5(bytes(request.POST['newpassword'], 'utf-8')).hexdigest()
	        obj.save()
	        data['updatepassword_success']="Your password Updated successfull";	 
	      else:
	        data['updatepassword_errors']=updatepassword_errors        
	    else:
	        updatepassword_errors=updatepassword_errors+"Wrong Current password<br/>"    
	        data['updatepassword_errors']=updatepassword_errors            
	    return render(request, 'tpa/changepassword.html', data);         