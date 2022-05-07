from django.db import models


# Create your models here.
class EtherVerified(models.Model):
    id = models.AutoField(primary_key=True)
    add = models.CharField(max_length=100, null=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    compiler = models.CharField(max_length=100, null=True)
    version = models.CharField(max_length=100, null=True)
    verified_time = models.CharField(max_length=20, null=True)
    url = models.CharField(max_length=100, null=True)
    fpath = models.CharField(max_length=100, null=True)
