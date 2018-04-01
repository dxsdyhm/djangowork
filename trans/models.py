from django.db import models

maxLen=512

class TransInfo(models.Model):
    zh=models.CharField(max_length=maxLen,unique=True)
    en=models.CharField(max_length=maxLen)
    useType=models.IntegerField()
