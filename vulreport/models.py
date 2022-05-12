from django.db import models
from vulscan.models import SolAddList


# Create your models here.


class VulDeatilList(models.Model):
    id = models.AutoField(primary_key=True)
    rid = models.IntegerField(null=True)
    swcid = models.IntegerField(null=True)
    title = models.CharField(max_length=100, null=True)
    impact = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)
    lines = models.CharField(max_length=100, null=True)
    fname = models.CharField(max_length=100, null=True)
    add = models.CharField(max_length=100, null=True)
    fpath = models.CharField(max_length=100, null=True)
    scantype = models.CharField(max_length=100, null=True)

