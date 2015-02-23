import os
import re
import json
import datetime
import subprocess as sub
from urllib2 import Request, urlopen, URLError

from django.db import models
from django.db.models import Max
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from django.dispatch import receiver
from django.db.models.signals import post_save
from blockchainPassport.settings import MEDIA_ROOT

from citizens.models import citizen
from keys.models import key
from blocks.models import block

lastrequest = datetime.datetime.now()
lastopened = 1


class register(models.Model):
    reg_citizen = models.OneToOneField(citizen)
    reg_block = models.ForeignKey(block)
    reg_key = models.ForeignKey(key)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=True)
    register_json = models.TextField(blank=True, null=True)
    signature_json = models.FileField(upload_to='signatures_json',
                                      blank=True, null=True)
    signature_imag = models.FileField(upload_to='signatures_img',
                                      blank=True, null=True)

    def registerCitizen(self, **kwargs):
        if 'reg_citizen' in kwargs:
            self.reg_citizen = kwargs['reg_citizen']
        if 'reg_block'in kwargs:
            self.reg_block = kwargs['reg_block']
        if 'reg_key'in kwargs:
            self.reg_key = kwargs['reg_key']
        self.register_json = self.getJSON()
        self.signature_json = self.getSign(self.register_json, src='json')
        self.signature_imag = self.getSign(self.reg_citizen.photo,
                                           'file', src='img')

    def __unicode__(self):
        return '{:} at {:}'.format(self.reg_citizen, self.reg_block)

    #AUXILIAR FUNCTIONS
    def getJSON(self):
        """returns a json with register data in it, to be signed and to
           build id view"""
        #number of blocks of id valitude
        eventSpan = 50
        print'la fecha es {:}'.format(self.timestamp.isoformat())
        #build citizen info hash
        citizen_info = {'name': self.reg_citizen.name,
                        'lastname': self.reg_citizen.lastname,
                        'social': self.reg_citizen.social}
        citizen_json = json.dumps(citizen_info)
        h = SHA.new(citizen_json)
        citizen_hash = h.hexdigest()
        #build rest of the data info
        print self.reg_block.index
        print self.reg_block.index + eventSpan
        data = {'register_time': self.timestamp.isoformat(),
                'blockindex': self.reg_block.index,
                'blockexpiration': self.reg_block.index + eventSpan,
                'blockmerkele': self.reg_block.merkele,
                'key_fingerprint': self.reg_key.fingerprint,
                'key_details': self.reg_key.atributes,
                'photo': self.reg_citizen.photo.__unicode__(),
                'citizen_hash': citizen_hash}
        for item in citizen_info:
            data[item] = citizen_info[item]
        jsondata = json.dumps(data)
        return jsondata

    def getSign(self, data, *args, **kwargs):
        """get cryptographic sign as file"""
        #check if you get a file as input, otherwise is a string value
        if 'file' in args:
            data.open()
            message = data.read()
            data.close()
        else:
            message = data
        #gets the type of signature, img or json
        if 'src' in kwargs:
            dataType = kwargs['src']
        else:
            dataType = 'json'
        # retrive private key
        self.reg_key.key_file.open()
        privkey = RSA.importKey(self.reg_key.key_file.read())
        self.reg_key.key_file.close()
        #sign message
        h = SHA.new(message)
        signer = PKCS1_v1_5.new(privkey)
        signature = signer.sign(h)
        #check if folder exists
        signFolder = checkFolder(os.path.join(MEDIA_ROOT,
                                              'signatures_{:}'.format(dataType)))
        #save to folder
        timemark = datetime.datetime.utcnow().isoformat()
        signatureDir = os.path.join(signFolder,
                                    '{:}_{:}'.format(dataType, timemark))
        signatureFile = open(signatureDir, 'w')
        signatureFile.write(signature)
        signatureFile.close()
        return signatureDir

################################################################
# EVENT HANDLER
################################################################


@receiver(post_save, sender=citizen)
def onSave(sender, **kwargs):
    """handler of post_save signal from citizen model"""
    # recover citizen data saved
    registeredCitizen = kwargs['instance']
    # get active key
    activekey = key.objects.get(status='on')
    # get last block
    lastblock = getLastBlock()
    # create register
    citizenRegister = register(reg_citizen=registeredCitizen,
                               reg_block=lastblock,
                               reg_key=activekey)
    citizenRegister.save()
    citizenRegister.registerCitizen()
    citizenRegister.save()
    #print 'this is register:\n{:}'.format(citizenRegister)


@receiver(post_save, sender=register)
def onSaveRegister(sender, **kwargs):
    """handler of post_save signal from register model"""
    global lastopened
    savedRegister = kwargs['instance']
    registerId = savedRegister.pk
    if registerId != lastopened:
        idRender = 'http://localhost:8000/id/{:}'.format(registerId)
        sub.Popen(['firefox', '-new-tab', idRender])
        lastopened = registerId

################################################################
# API FUNCTIONS
################################################################


def consultAPI(url, *args):
    """consult api by url and the names of data you want to get
       returns a dicionary of var_name and its value"""
    print(('checking {:}\ncalling blockchain api'.format(url)))
    request = Request(url)
    try:
        response = urlopen(request)
        responseText = response.read()
        dicResponse = json.loads(responseText)
        returnDict = {}
        for item in args:
            returnDict[item] = dicResponse[item]
    except URLError as e:
        print(('Sry dude, you got an error code:', e))
    print(returnDict)
    return returnDict


def getMerkele(blockhash):
    """gets Merkele root from a block given its index"""
    apiUrl = 'https://blockchain.info/block/{:}'.format(blockhash)
    request = Request(apiUrl)
    try:
        response = urlopen(request)
        responseText = response.read()
        #download a blockchain webpage to get merkle root because api is slow
        merkle = re.findall('<td class="hash-link">.+<', responseText)[0][22:-1]
        return merkle
    except:
        print 'lanzar view para meter dato manual'


def getLastBlock():
    """check last block in btc blockchain, if there is a new block,
       it is registered."""
    global lastrequest
    requestRate = datetime.timedelta(0, 60)
    #get db last block
    lastblock = block.objects.all().aggregate(Max('index')).values()[0]
    #check if there is a block, if there is an error because of lastrequest is
    #None, give timefromLast a value that makes condition false
    try:
        timefromLast = datetime.datetime.now() - lastrequest
    except:
        timefromLast = datetime.timedelta(0, 190)
    #check api if there is not a block, check api if a minute has pased after
    #the last time api was consulted
    #logic table is p=>q, so here there is not p or q
    if lastblock is not None or timefromLast > requestRate:
        #consult api
        apiUrl = 'https://blockchain.info/latestblock'
        blockInfo = consultAPI(apiUrl, 'block_index', 'hash')
        #register consult time
        lastrequest = datetime.datetime.now()
        #if lastblock in database, return that value, otherwise, create a new
        #block
        try:
            currentBlock = block.objects.get(index=blockInfo['block_index'])
            return currentBlock
        except:
            newBlock = block(index=blockInfo['block_index'],
                             merkele=getMerkele(blockInfo['hash']),
                             hashId=blockInfo['hash'],
                             creationTime=datetime.datetime.now())
            newBlock.save()
            return newBlock
    else:
        return lastblock

################################################################
# AUXILIAR FUNCTIONS
################################################################


def checkFolder(folder):
    """check if folder exists, if dont, then create the folder"""
    if not os.path.exists(folder):
            os.mkdir(folder)
    return folder
