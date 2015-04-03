from setuptools import setup

setup(name='blockchainpassport',
      version='1.0.0',
      description='partial implementation of worldcitizenship for id creation based on blockchain',
      author='emdyp',
      author_email='myuser@emdyp.me',
      url='http://api.emdyp.me',
      install_requires=['Django>=1.7.3', 'argparse>=1.2.1',
                        'django-extensions>=1.4.9', 'html5lib>=0.999',
                        'django-grappelli>=2.6.3', 'PyPDF2>=1.24', 'xhtml2pdf>=0.0.6',
                        'pycrypto>=2.6.1', 'wsgiref>=0.1.2', 'reportlab>=3.1.44',
                        'six>=1.9.0', 'bootstrap-admin>=0.3.3', 'Pillow>=2.7.0'],
     )
