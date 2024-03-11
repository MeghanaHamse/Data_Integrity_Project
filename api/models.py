from django.db import models  
from django.db import connection  
import hashlib     
from django.forms.models import model_to_dict
import json

def sha256sum(block):  
    return  hashlib.sha256(block.encode('utf-8')).hexdigest()
     
class Block(models.Model):
    index=models.AutoField(primary_key=True)
    hash = models.TextField(unique=True) 
    transaction=models.TextField() 
    block_type = models.TextField()
    previous_hash = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def detail(self):
        return {
            'previous_hash': self.previous_hash,
            'hash': self.hash,
            'transaction':self.transaction,
            'block_type': self.block_type,
            'created_at': str(self.created_at),
        }

    @staticmethod
    def create_block(data, block_type):
        last_block = Block.objects.last()
        if not last_block:
            last_hash = '0' 
        else:
            last_hash = last_block.hash 
        block=Block.objects.create(previous_hash=last_hash, hash=sha256sum(data), block_type=block_type,transaction=data)
        return  block.index
     
    @staticmethod
    def create_genesis_block():
        Block.create_block('First Block', 'Genesis block')
 
    @classmethod
    def get_block(self,index):
        blk = Block.objects.get(index=index)
        block=model_to_dict(blk)
        block['created_at']=str(blk.created_at.strftime("%b %d, %Y %H:%M:%S"))
        blk  = Block.objects.filter(hash=blk.previous_hash).first()
        nextblock={}   
        prevblock={}      
        if blk: 
          prevblock= model_to_dict(blk)
          prevblock['created_at']=str(blk.created_at.strftime("%b %d, %Y %H:%M:%S"))
          prevblock['transaction']='' 
          
        blk = Block.objects.filter(previous_hash=block['previous_hash']).first()
        if blk:
           nextblock= model_to_dict(blk) 
           nextblock['created_at']=str(blk.created_at.strftime("%b %d, %Y %H:%M:%S"))      
           nextblock['transaction']='' 
           
        block['transaction']=''
        return [prevblock,block,nextblock]
        
    @classmethod
    def validate_block(self,index,data):
        blk = Block.objects.get(index=index)
        newhash=sha256sum(data)
        if blk.hash == newhash:
           return True
        else:
           return False        
    
 
    @classmethod
    def get_blockchain(self):
        chain=self.objects.all().order_by('index');
        blockchain=[]
        for blk in chain:
            newblk=model_to_dict(blk)
            #newblk['new_hash']=sha256sum(blk.transaction 
            newblk['created_at']=str(blk.created_at.strftime("%b %d, %Y %H:%M:%S"))
            newblk['type']= blk.block_type
            blockchain.append(newblk);
            
        previous_block = blockchain[0]
        blockchain[0]['status']="Ok"        
        block_index = 1
        while block_index < len(blockchain):
            block = blockchain[block_index]
            
            if block['previous_hash'] != previous_block['hash']:
                blockchain[block_index]['status']="Invalid Hash"
            else:
                blockchain[block_index]['status']="Ok"
             
            previous_hash=sha256sum(previous_block['transaction'])              
            if block['previous_hash'] != previous_hash:
                blockchain[block_index]['status']="Invalid Data Hash"
                
            previous_block = block
            blockchain[block_index-1]['transaction']=''
            blockchain[block_index]['block_type']=block['block_type']
            block_index += 1         
            
        return blockchain
        
    @classmethod
    def is_chain_valid(self):
        chain=self.objects.all().order_by('index') 
        blockchain=[]
        for blk in chain:
            blockchain.append(model_to_dict(blk));
            
        previous_block = blockchain[0]    
        block_index = 1
        while block_index < len(blockchain):
            block = blockchain[block_index]
            if block['previous_hash'] != sha256sum(previous_block['transaction']):
                return False 
            previous_block = block
            block_index += 1
        return True