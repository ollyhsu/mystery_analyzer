from django.db import models


# Create your models here.
class SolAddList(models.Model):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100, null=True)
    fpath = models.CharField(max_length=100, null=True)
    add = models.CharField(max_length=100, null=True, unique=True)
    scantype = models.CharField(max_length=100, null=True)
    result = models.CharField(max_length=1000, null=True)
    time = models.CharField(max_length=100, null=True, unique=True)
    uid = models.IntegerField(null=True)