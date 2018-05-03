# coding:utf-8
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse

from trans import models
from trans.change.readtrans import getAllTrans, getUse
from trans.models import TransInfo
from django.forms.models import model_to_dict


def createTestData():
    result=getAllTrans()
    use=getUse()
    try:
        for tran in result.keys():
            info = TransInfo(zh=tran, en=result[tran],useType=0)
            if tran in use:
                info.useType=1
            else:
                info.useType=0
            saveInfo(info)

        for notTrans in use-result.keys():
            info = TransInfo(zh=notTrans, en="",useType=2)
            saveInfo(info)
    except Exception:
        print("save info error")

def saveInfo(info):
    try:
        info.save()
    except:
        print(info.zh)

def index(request):
    return HttpResponse(u'i love android')

def home(request):
    # createTestData()
    type=request.GET.get('type',1)
    yyy=TransInfo.objects.filter(useType=type)
    return render(request,'trans/home.html',{'yyy':yyy})

def downloadAllFile(request):
    def file_iterator(file_name,chunk_size=512):
        with open(file_name) as f:
            while True:
                c=f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_filename='all.xls'
    response=StreamingHttpResponse(file_iterator(the_filename))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="{0}"'.format(the_filename)
    return response