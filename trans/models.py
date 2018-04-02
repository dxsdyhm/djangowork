from django.db import models

maxLen=512

class TransInfo(models.Model):
    zh=models.CharField(max_length=maxLen,unique=True)
    en=models.CharField(max_length=maxLen)
    useType=models.IntegerField()

    def __str__(self):
        return '%s(%s)' % (self.zh,self.en)