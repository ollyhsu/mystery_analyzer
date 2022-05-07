from django.db import models


# Create your models here.
class SolUpload(models.Model):
    id = models.AutoField(primary_key=True)
    sol = models.FileField(upload_to='vul_upload/')
    fname = models.CharField(max_length=100, null=True)
    fpath = models.CharField(max_length=100, null=True)
    result = models.CharField(max_length=100, null=True)
