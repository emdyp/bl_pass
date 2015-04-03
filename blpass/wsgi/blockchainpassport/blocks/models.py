from django.db import models


class block(models.Model):
    """register blocks of blockchain"""
    index = models.IntegerField()
    merkele = models.CharField(default='', max_length=100)
    hashId = models.CharField(default='', max_length=100)
    creationTime = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return str(self.index)
