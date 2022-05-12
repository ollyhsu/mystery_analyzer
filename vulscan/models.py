from django.db import models


# Create your models here.
class SolAddList(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(null=True)
    scantype = models.CharField(max_length=100, null=True)
    fname = models.CharField(max_length=100, null=True)
    add = models.CharField(max_length=100, null=True)
    fpath = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True, unique=True)
    status = models.CharField(max_length=100, null=True)
    result = models.TextField(blank=True, null=True)
    runtime = models.TextField(blank=True, null=True)
    check_time = models.CharField(max_length=100, null=True, unique=True)