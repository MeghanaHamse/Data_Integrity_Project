from django.http import JsonResponse, HttpResponse, HttpRequest
from   .models import *
from django.views.decorators.csrf import csrf_exempt #New
     
# Adding a new block to the Blockchain
@csrf_exempt
def add_block(request): #New
    if request.method == 'POST': 
        error=""
        if request.POST.get("transaction","")=="":
           error+="Transaction details required<br/>"   
        if request.POST.get("block_type","")=="":
           error+="Block type details required<br/>"      
        if error=="":
           index=Block.create_block(request.POST["transaction"],request.POST["block_type"])
           response={'success':1,'message':"Transaction Added as Block to Blockchain(Index:#"+str(index)+")",'index':index}     
        else:
          response={'success':0,'message':error}        
    return JsonResponse(response)     

# Validate transaction with the Blockchain
@csrf_exempt
def validate_block(request): #New
    if request.method == 'POST': 
        error=""
        if request.POST.get("transaction","")=="":
           error+="Transaction details required<br/>"   
        if request.POST.get("index","")=="":
           error+="Block index   required<br/>"      
        if error=="":
           valid=Block.validate_block(request.POST['index'],request.POST['transaction'])
           response={'success':1,'valid':valid}     
        else:
          response={'success':0,'message':error}        
    return JsonResponse(response) 

# Getting the full Blockchain
def get_block(request,index):
    if request.method == 'GET':
        block=Block.get_block(index)
        response = {'prevblock':block[0],'block': block[1],'nextblock':block[2] }
    return JsonResponse(response) 
    
# Getting the full Blockchain
def get_chain(request):
    if request.method == 'GET':
        chain=Block.get_blockchain()
        response = {'chain': chain,
                    'length': len(chain)}
    return JsonResponse(response)
 
# Checking if the Blockchain is valid
def is_chain_valid(request):
    if request.method == 'GET':
        is_valid = Block.is_chain_valid()
        if is_valid:
            response = {'message': 'All good. The Blockchain is valid.'}
        else:
            response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return JsonResponse(response)   