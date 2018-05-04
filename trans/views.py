# coding:utf-8
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from trans import models
from trans.change.readtrans import getAllTrans, getUse
from trans.models import TransInfo
from django.forms.models import model_to_dict
import json
import requests
import ast


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

pos=u'''
{
    "actionCard": {
        "title": "%s",
         "text": "%s",
        "hideAvatar": "0",
        "btnOrientation": "0",
        "singleTitle" : "下载地址",
        "singleURL" : "%s"
    },
    "msgtype": "actionCard"
}
'''

url = 'https://oapi.dingtalk.com/robot/send?access_token=af42bec477aeee14b5e47e0bb3f1d6aca103f4477dc1aaebf1616b833c007e82'
# url = 'https://oapi.dingtalk.com/robot/send?access_token=eba1d9124acf2ae08cff6f65e053cff6e15caa02c9e4dcf2acf59e872ba0eafd'
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}

@csrf_exempt
def pgyWebHook(request):
    if request.method == 'POST':
        body=str(request.body,encoding = "utf-8")
        response = requests.post(url, data=changePosBody(body), headers=header_dict)
        return HttpResponse(response.text)
    else:
        return HttpResponse(request.method)

def changePosBody(body):
    dirct_body = eval(body)
    title='小豚当家有新版本了（%s）' % dirct_body.get('os_version','null')
    text='![](http://7xp6ld.com1.z0.glb.clouddn.com/ic_upgrad_head.png)\n\n### 小豚当家有新版本了（%s）\n\n ##### 更新内容：\n\n\n\n  %s' % (dirct_body['os_version'],dirct_body['notes'])
    link=dirct_body.get('link','https://www.pgyer.com/wanzen')
    posBody=pos % (title,text,link)
    print (posBody)
    return posBody.encode('utf-8')
