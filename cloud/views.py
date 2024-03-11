from django.shortcuts import render, get_object_or_404 ,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from  fidia.models import *
from django.forms.models import model_to_dict
import  datetime
from django.conf import settings

def index(request):   
	 return redirect('/cloud/login') 
	  
def  login(request):    
	    if bool(request.session.get('cloud_logged_in', False))==True:  
	       return redirect('/cloud/dashboard')
          
	    return render(request, 'cloud/login.html') 

def  loginauth(request): 
        login_error=""
        if request.POST.get("username","")=="":
          login_error=login_error+"Username required" 
        if request.POST.get("password","")=="":
          login_error=login_error+"Password required" 
		
        if login_error!="": 		    
           return render(request, 'cloud/login.html'); 
        else: 
           cloud=True  
           cloud= Cloud.objects.filter(username=request.POST['username'],password=hashlib.md5(bytes(request.POST['password'], 'utf-8')).hexdigest()).first()
		    
           if cloud: 
                cloud=model_to_dict(cloud)
                cloud['cloud_logged_in']=True 
                keys=list(request.session.keys())
                for key  in keys:
                   if request.session[key]:
                      del request.session[key] 
                for key,val in cloud.items():
                    request.session[key]=str(val)            
                return redirect('/cloud/dashboard')  
           else: 
                data={'login_error':"Mismatched Login Credentials<br/>"};  
                return render(request, 'cloud/login.html', data);         

def  dashboard(request):   
	    if request.session.get('cloud_logged_in', "")=="":  
	      return redirect('/cloud/login') 
           
	    data={}  
	    data['total']=Auditrequest.objects.all().count()
	    data['senttotpa']=Auditrequest.objects.filter(tpastatus=0,cloudstatus=0).count()
	    data['senttocloud']=Auditrequest.objects.filter(tpastatus=1,cloudstatus=0).count()
	    data['sentfromcloud']=Auditrequest.objects.filter(tpastatus=1,cloudstatus=1).count()
	    data['tpaaudited']=Auditrequest.objects.filter(tpaverification=1).count()
	    data['useraudited']=Auditrequest.objects.filter(userverification=1).count()
	    return render(request, 'cloud/dashboard.html', data); 
        
def  sendproof(request):   
	    if request.session.get('cloud_logged_in', "")=="":  
	      return redirect('/cloud/login') 
           
	    data={}  
	    files=Auditrequest.objects.filter(tpastatus=1,cloudstatus=0).order_by('-id')   
	    data={'files':[]}
	    for f in files:
	        fileobj=Fileuploads.objects.get(id=f.fileid)
	        username=User.objects.get(id=fileobj.userid).fullname  
	        data['files'].append({'id':fileobj.id,'username':username,'requestid':f.id,'filename':fileobj.filename,'requestedtpa':f.creationDate,'requestedcloud':f.tpaat})
         
	    return render(request, 'cloud/sendproof.html', data);           


def sendresponse(request,id):
	    if request.session.get('cloud_logged_in', "")=="":  
	      return redirect('/cloud/login') 
          
	    data=model_to_dict(Auditrequest.objects.filter(id=id).first())
	    data['file']=model_to_dict(Fileuploads.objects.get(id=data['fileid']))         
	    data['username']=User.objects.get(id=data['userid']).fullname         
	    return render(request, 'cloud/sendresponse.html', data); 

def decompressfile(request,id):
	    if request.session.get('cloud_logged_in', "")=="":  
	      return redirect('/cloud/login') 
          
	    obj=Auditrequest.objects.filter(id=id).first()   
	    fobj=Fileuploads.objects.get(id=obj.fileid)
	    moddecompressfile(settings.CLOUD_DIRS[0]+"/"+fobj.cloudname+"/"+str(fobj.id))
        
	    return HttpResponse("ok")          

def decryptfile(request,id):
	    if request.session.get('cloud_logged_in', "")=="":  
	      return redirect('/cloud/login') 
          
	    obj=Auditrequest.objects.filter(id=id).first()   
	    fobj=Fileuploads.objects.get(id=obj.fileid)
	    moddecryptfile(settings.CLOUD_DIRS[0]+"/"+fobj.cloudname+"/"+str(fobj.id),fobj.key)
        
	    return HttpResponse("ok")           

def gensign(request,id):
	    if request.session.get('cloud_logged_in', "")=="":  
	      return redirect('/cloud/login') 
           
	    obj=Auditrequest.objects.filter(id=id).first()   
	    fobj=Fileuploads.objects.get(id=obj.fileid)           
	    obj.cloudhashresult=modfilesignature(settings.CLOUD_DIRS[0]+"/"+fobj.cloudname+"/"+str(fobj.id))
	    obj.save()
        
	    return HttpResponse("ok")     


def sendresponsedb(request):
	    if request.session.get('cloud_logged_in', "")=="":  
	      return redirect('/cloud/login') 
          
	    obj=Auditrequest.objects.filter(id=request.POST['requestid']).first()   
	    fobj=Fileuploads.objects.get(id=obj.fileid)
	    obj.cloudstatus=1  
	    obj.cloudauditat= datetime.datetime.now() 
	    obj.save()
        
	    return redirect('/cloud/sendproof')         
      
def files(request):
	    if request.session.get('cloud_logged_in', "")=="":  
	      return redirect('/cloud/login')  

	    files=Fileuploads.objects.all().order_by('-id')   
	    data={'files':[]}
	    for f in files:
	        lastaudited=Auditrequest.objects.filter(fileid=f.id,tpaverification=1).first()
	        if lastaudited:
	           lastaudited=lastaudited.tpaverifiedat 
	        else:
	           lastaudited="Not Audited"
	        username=User.objects.get(id=f.userid).fullname     
	        data['files'].append({'id':f.id,'username':username,'filename':f.filename,'creationDate':f.creationDate,'lastaudited':lastaudited})
            
	    return render(request, 'cloud/files.html', data);           
        
def  changepassword(request):   
	    if request.session.get('cloud_logged_in', "")=="":  
	       return redirect('/cloud/login') 
           
	    data={}   
	    return render(request, 'cloud/changepassword.html', data); 

def  updatepassword(request):   
	    if request.session.get('cloud_logged_in', "")=="":  
	       return redirect('/cloud/login') 
           
	    updatepassword_errors=""
	    if request.POST.get("password","")=="":
	      updatepassword_errors=updatepassword_errors+ "Current password required<br/>" 
	    if len(request.POST.get("newpassword",""))<6:
	      updatepassword_errors=updatepassword_errors+"New password of minimum 6 chars required<br/>" 
	    else:  
	      if request.POST['newpassword']!=request.POST.get("confirmpassword",False):
	         updatepassword_errors=updatepassword_errors+"Confirm password required<br/>" 
        
	    data={}
	    cloud= Cloud.objects.filter(id=request.session["id"],password=hashlib.md5(bytes(request.POST['password'], 'utf-8')).hexdigest()).first()         
	    if cloud:	      
	      if updatepassword_errors=="": 
	        obj=Cloud.objects.filter(id=request.session["id"]).first()
	        obj.password=hashlib.md5(bytes(request.POST['newpassword'], 'utf-8')).hexdigest()
	        obj.save()
	        data['updatepassword_success']="Your password Updated successfull";	 
	      else:
	        data['updatepassword_errors']=updatepassword_errors        
	    else:
	        updatepassword_errors=updatepassword_errors+"Wrong Current password<br/>"    
	        data['updatepassword_errors']=updatepassword_errors            
	    return render(request, 'cloud/changepassword.html', data);     
        
        
def tracechained(request,index):
    if request.session.get('cloud_logged_in', "")=="":  
	       return redirect('/cloud/login') 
           
    chain=getBlock(index)
    chain=[chain['prevblock'],chain['block'],chain['nextblock']]
    strhtml=""
    for k,c in enumerate(chain): 
           clss="block-"+str(k)
           if c:
              block="<tr><td>Date : </td><td>"+c['created_at']+"</td></tr>" 
              block+="<tr><td>Block Type : </td><td>"+c['block_type']+"</td></tr>"
              block+="<tr><td>Stored Hash : </td><td title='"+c['hash']+"'>"+c['hash'][0:5]+"...</td></tr>"
              block+="<tr><td>Previous Hash : </td><td title='"+c['previous_hash']+"'>"+c['previous_hash'][0:5]+"...</td></tr>" 
              strhtml+="<div  class='trace "+clss+"  m-auto "+("col-4 border-primary" if k==1 else "col-3")+" "+("hasprev" if c['previous_hash']!='0' else "")+"'><table class='table table-bordered mt-3 mb-3'><thead class='thead-dark'>"+block+"</thead></table></div>"
           else:
              strhtml+="<div  class='trace   m-auto "+("col-4 border-primary" if k==1 else "col-3")+"'> </div>"
             
        
    strhtml="<div class='w-100'>"+strhtml+"</div>"
    data={'strhtml':strhtml}    
    return render(request, 'cloud/tracechained.html', data) 
           
def blockchain(request): 
        if request.session.get('cloud_logged_in', "")=="":  
           return redirect('/cloud/login') 
            
        data={}
        return render(request, 'cloud/blockchain.html', data)  
        
        
def validatechain(request): 
        if request.session.get('cloud_logged_in', "")=="":  
           return redirect('/cloud/login') 
	 
        return HttpResponse(validateBlockchain())  

def getchain(request): 
	    if request.session.get('cloud_logged_in', "")=="":  
	       return redirect('/cloud/login') 
           
	    chain=getBlockchain() 
	    length=chain['length']
	    chain=chain['chain']
	    strhtml=""
	    for c in chain: 
	       block="<span class='hashcode float-left'>Date : </span><span class='hashcode'>"+c['created_at']+"</span>" 
	       block+="<br/><span class='hashcode float-left'>Block Type : </span><span class='hashcode'>"+c['block_type']+"</span>"
	       block+="<br/><span class='hashcode float-left'>Stored Hash : </span><span class='hashcode' title='"+c['hash']+"'>"+c['hash'][0:5]+"...</span>"
	       block+="<br/><span class='hashcode float-left'>Previous Hash : </span><span class='hashcode' title='"+c['previous_hash']+"'>"+c['previous_hash'][0:5]+"...</span>"
	       strhtml+="<div  class='validation col-10 m-auto'><table class='table mt-3 mb-3'><thead class='thead-dark'><tr><td class='h4'  rowspan='2'><div class='float-left w-100'>"+block+"</div></td><td class='alert-info h5 text-center'>STATUS</td></tr><tr><td class='text-center'>"+c['status']+"</td></tr></thead></table></div>"
        
	    strhtml="<div class='w-100'>"+strhtml+"</div>"        
	    return HttpResponse(strhtml)                             