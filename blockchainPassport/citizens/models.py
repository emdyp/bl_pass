from django.db import models


class citizen(models.Model):
    name = models.CharField(default='', max_length=50)
    lastname = models.CharField(default='', max_length=50)
    photo = models.FileField(upload_to='photos')
    social = models.CharField(default='', max_length=100,
                              blank=True, null=True)

    def __unicode__(self):
        return u'{:} {:}'.format(self.name, self.lastname)
