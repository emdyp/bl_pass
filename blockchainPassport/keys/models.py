from django.db import models


class key(models.Model):
    key_file = models.FileField(upload_to='privKeys')
    public_key = models.FileField(upload_to='publicKeys')
    atributes = models.TextField(default='2048 RSA openSSH PKCS1_v1_5',
                                 max_length=50)
    fingerprint = models.CharField(default='', max_length=50)
    keyStatus = (('on', 'active'),
                 ('off', 'disabled'))
    status = models.CharField(max_length=3, choices=keyStatus, default='off')

    def __unicode__(self):
        return self.fingerprint
