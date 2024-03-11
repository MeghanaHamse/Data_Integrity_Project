from django.shortcuts import render, get_object_or_404 ,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from  fidia.models import *
import json
from django.conf import settings

def index(request):   
	      return render(request, 'home.html')  

def register(request):   
	      return render(request, 'register.html')            

def adduserdb(request):
        if request.session.get('admin_logged_in', "")=="": 
           redirect("/login")  
        docfiles=[] 
 
        error=""
        if request.POST.get("fullname","")=="":
           error+="Full Name required<br/>"    
        if request.POST.get("mobile","")=="":
           error+="Mobile required<br/>"  
        if request.POST.get("city","")=="":
           error+="City required<br/>"
        if request.POST.get("country","")=="":
           error+="Country required<br/>"  
        if request.POST.get("dob","")=="":
           error+="Date of birth required<br/>" 
        if User.objects.filter(mobile=request.POST["mobile"]).first(): 
           error+="Mobile Already Exists<br/>" 
        if request.POST.get("emailid","")!="":
           if User.objects.filter(email=request.POST["emailid"]).first(): 
             error+="Email Already Exists<br/>"          
        else:
             error+="Email required<br/>"    
        if request.POST.get("gender","")=="":
           error+="Gender required<br/>"               
        if len(request.POST.get("password",""))>6:
           if request.POST["password"]!=request.POST.get("cpassword",""): 
             error+="Confirm Password should match with password<br/>"          
        else:
             error+="Password of min 6 chars required<br/>" 
        if request.FILES.get("bimage","")=="":
           error+="Biometric Image required<br/>"
             
        if error!="":
            return HttpResponse(json.dumps({"success":0,"message":error}), content_type='application/json')  
        else: 
           #dob = datetime.strptime(request.POST['dob'],"%d-%m-%Y") 
           obj=User()
           obj.fullname=request.POST['fullname'] 
           obj.birthdate=request.POST['dob']	#dob.strftime("%Y-%m-%d")  
           obj.mobile=	request.POST['mobile']
           obj.email=	request.POST['emailid'] 
           obj.city=	request.POST['city']
           obj.country=	request.POST['country'] 
           obj.gender=	request.POST['gender']
           obj.password=hashlib.md5(bytes(request.POST['password'], 'utf-8')).hexdigest() 
           file=request.FILES['bimage']
           fname=file.name.split(".")
           ext=fname[len(fname)-1]  
           obj.save()                 
           obj.biometricimage=str(obj.id)+"."+ext           
           dest = open(settings.STATICFILES_DIRS[0]+"/uploads/bimages/"+str(obj.id)+"."+ext, 'wb')
           dest.write(file.read())
           dest.close()
           obj.save() 
           chainstatus=addBlock({'type':'User','id':obj.id,'name':obj.fullname,'email':obj.email,'mobile':obj.mobile,'city':obj.city,'country':obj.country},'Create user');            
           return HttpResponse(json.dumps({"success":1,"message":"User Added Successfully<br/>"+chainstatus['message']}), content_type='application/json') 
 
def  logout(request):   
         keys=list(request.session.keys())
         for key  in keys:
           if request.session[key]:
             del request.session[key]
         return redirect('/')    