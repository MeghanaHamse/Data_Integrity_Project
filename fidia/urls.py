from django.urls import path,include
from . import views
from user import views as uviews
from kgc import views as kviews
from tpa import views as tviews
from cloud import views as cviews

urlpatterns = [
    path('', views.index), 
    path('register', views.register), 
    path('adduserdb', views.adduserdb), 
    path('logout', views.logout),     
    path('user', uviews.index),
    path('user/login', uviews.login), 
    path('user/loginauth', uviews.loginauth),
    path('user/changepassword', uviews.changepassword),
    path('user/updatepassword', uviews.updatepassword),    
    path('user/dashboard', uviews.dashboard),   
    path('user/fileupload', uviews.fileupload),   
    path('user/myfiles', uviews.myfiles),   
    path('user/auditrequest', uviews.auditrequest),   
    path('user/proofcheck', uviews.proofcheck),  
    path('user/filetocloud', uviews.filetocloud), 
    path('user/encryptfile/<int:id>', uviews.encryptfile),    
    path('user/requesttpaaudit/<int:id>', uviews.requesttpaaudit),        
    path('user/verifyaudit/<int:id>', uviews.verifyaudit), 
    path('user/verifyauditdb', uviews.verifyauditdb),      
    path('kgc', kviews.index),
    path('kgc/login', kviews.login), 
    path('kgc/loginauth', kviews.loginauth),
    path('kgc/dashboard', kviews.dashboard), 
    path('kgc/keyrequest', kviews.keyrequest),
    path('kgc/acceptkeyreq/<int:id>', kviews.acceptkeyreq),
    path('kgc/rejectkeyreq/<int:id>', kviews.rejectkeyreq),    
    path('kgc/users', kviews.users),     
    path('kgc/changepassword', kviews.changepassword),
    path('kgc/updatepassword', kviews.updatepassword),      
    path('tpa', tviews.index),
    path('tpa/login', tviews.login), 
    path('tpa/loginauth', tviews.loginauth), 
    path('tpa/dashboard', tviews.dashboard),
    path('tpa/auditrequest', tviews.auditrequest),
    path('tpa/sendarequesttocloud/<int:id>', tviews.sendarequesttocloud),
    path('tpa/requestcloud', tviews.requestcloud),
    path('tpa/proofcheck', tviews.proofcheck),    
    path('tpa/verifyaudit/<int:id>', tviews.verifyaudit), 
    path('tpa/verifyauditdb', tviews.verifyauditdb),   
    path('tpa/changepassword', tviews.changepassword),
    path('tpa/updatepassword', tviews.updatepassword),     
    path('cloud', cviews.index),
    path('cloud/login', cviews.login),  
    path('cloud/loginauth', cviews.loginauth), 
    path('cloud/dashboard', cviews.dashboard),
    path('cloud/sendproof', cviews.sendproof),  
    path('cloud/sendresponse/<int:id>', cviews.sendresponse),      
    path('cloud/decompressfile/<int:id>', cviews.decompressfile),  
    path('cloud/decryptfile/<int:id>', cviews.decryptfile),  
    path('cloud/gensign/<int:id>', cviews.gensign),  
    path('cloud/sendresponsedb', cviews.sendresponsedb),      
    path('cloud/files', cviews.files),   
    path('cloud/changepassword', cviews.changepassword),
    path('cloud/updatepassword', cviews.updatepassword),    
    path('cloud/blockchain',cviews.blockchain,name="blockchain"), 
    path('cloud/validatechain',cviews.validatechain,name="validatechain"),
    path('cloud/getchain',cviews.getchain,name="getchain"),   
    path('cloud/tracechained/<int:index>',cviews.tracechained,name="tracechained"),      
    path('attacks/', include('attacks.urls')),
    path('api/', include('api.urls')),
]