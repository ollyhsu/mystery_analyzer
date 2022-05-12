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
    status = models.CharField(max_length=100, null=True)
    result = models.TextField(blank=True, null=True)
    runtime = models.TextField(blank=True, null=True)
    cfg = models.CharField(max_length=100, null=True)
    check_time = models.CharField(max_length=100, null=True, unique=True)


class EtherDeatilList(models.Model):
    id = models.AutoField(primary_key=True)
    rid = models.IntegerField(null=True)
    swcid = models.IntegerField(null=True)
    title = models.CharField(max_length=100, null=True)
    impact = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)
    lines = models.CharField(max_length=100, null=True)

