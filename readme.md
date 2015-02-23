#bl_pass - Documentation files

#1 GENERAL

bl_pass is a partial implementation of World-Citizenship protocol 
find it here: https://github.com/MrChrisJ/World-Citizenship, 
for id generation over bitcoin blockchain.

its purpose is originally help meetings like coinfest to register
attendees by using an automated platform to generate ids, but
could be a start point to continue the development of stronger tools
like the ones proposed by Bitnation.

Disclaimer: there is not warranty about the safety of this software
still needs more work to be put on production environments and could
crash with medium or high traffic

#2 USAGE AND FEATURES

bl_pass has the follow features, this start version is coded to work
in linux-OSX computers only, uses calls to Mozilla firefox in order
to show render ids, it is recommended have a tablet device for register
attendees connected trough wireless private network to computer that
runs software as server, the computer must have internet access in order
to consume blockchain api in order to get data such as last block, index
hash, merkle.

the computer can, then, print to document and send by email, use a printer
and get id cards, and if attendee requires, use notary services like 
http://www.cryptograffiti.info, recommended work with electrum wallet to
that.

bl_pass features are:

* responsive admin interface
* register attendee data
* automated register generation(json file, signatures, timestamp, blockchain information, hash generation to publish in blockchain)
* html5 id render 

features to develop:

* id verification system
* improve id cryptographic management
* digital signature management
* multi key support
* automated publication into notary services
* production environments support
* show id render without call firefox using subprocess

###requirements

* Django==1.7.4
* Naked==0.1.30
* PyYAML==3.11
* argparse==1.2.1
* blockchain==1.1.2
* bootstrap-admin==0.3.4
* django-extensions==1.5.0
* django-grappelli==2.6.3
* pycrypto==2.6.1
* python-gnupg==0.3.7
* requests==2.5.1
* six==1.9.0
* wsgiref==0.1.2

#3 ABOUT US

Emdyp.me developed this software, we are a start-up that works with technology and 
language services, visit us at http://emdyp.me, you can write us at mailbox@emdyp.me 
or follow us at @emdyp.

every comment, help or donation is wellcome, you can support us by helping with the development,
designing cool id templates, giving us your feedback.

###Donations
* bitcoin: 1DHxhFbyWFe59yCzuFeumN6UBFz6qPZhPX
* vericoin: VVNkwZrUnDNwYyz89fNdMhCFh2h3tFfWiT

we support bogota coinfest 2015, even in blockchain :) http://www.cryptograffiti.info/?txnr=2238
