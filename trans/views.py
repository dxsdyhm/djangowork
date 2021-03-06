# coding:utf-8
import hashlib

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
from wechatpy import parse_message
from wechatpy.replies import TextReply,EmptyReply
from wechatpy import WeChatClient
from wechatpy import create_reply
# client = WeChatClient('wx86de7887993d7c0d', '9b7e9acdda2145d0b5d9bef7f13d6422')
client = WeChatClient('wx65f9f2332760c43d', '9bd1a29396531fb4b7ae4ede9ee6e0a6')

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
    client.customservice.add_account('a@wx65f9f2332760c43d', '小精灵', 'qwe123')
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

# url = 'https://oapi.dingtalk.com/robot/send?access_token=af42bec477aeee14b5e47e0bb3f1d6aca103f4477dc1aaebf1616b833c007e82'
# 正式
url = 'https://oapi.dingtalk.com/robot/send?access_token=f5675f20956bedfc2459385e570a12aa6c82457b18150791d0ce144775f448a1'
# url = 'https://oapi.dingtalk.com/robot/send?access_token=eba1d9124acf2ae08cff6f65e053cff6e15caa02c9e4dcf2acf59e872ba0eafd'
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}

@csrf_exempt
def pgyWebHook(request):
    if request.method == 'POST':
        body=str(request.body,encoding = "utf-8")
        response = requests.post(url, data=changePosBody(body), headers=header_dict)
        return HttpResponse(response.text)
    else:
        res="method:%s,test:%s"
        return HttpResponse(res % (request.method,"2"))

def changePosBody(body):
    dirct_body = eval(body)
    title='小豚当家有新版本啦（%s）' % dirct_body.get('os_version','null')
    text='![update](http://ww1.sinaimg.cn/large/72fc1a27gy1fyej670h3tj20eq095aad.jpg)\n\n### 小豚当家有新版本了（%s）\n\n ##### 更新内容：\n\n\n\n  %s' % (dirct_body['os_version'],dirct_body['notes'])
    link=dirct_body.get('link','https://www.pgyer.com/wanzen')
    posBody=pos % (title,text,link)
    return posBody.encode('utf-8')

# wxurl_getToken='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx146d06d152af3d07&secret=6e4b87f16ab21f6eeaa56a9648a5dad4'
wxurl_getToken='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxcaf33ba1733ae02f&secret=a73e91f6826b8fcb2f4783179a9a877f'
wxurl_sendMessage='https://api.weixin.qq.com/cgi-bin/message/template/subscribe?access_token=%s'
wx_sendMessage_post=u'''
{
  "touser": "%s",
  "template_id": "%s",
  "url":"https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU3NjA4MTc2Mg==&scene=116#wechat_redirect",
  "scene": "%s",
  "title": "一键订阅测试",
  "data": {
    "content": {
      "value": "这是一次测试44",
      "color": "#ff0000"
    }
  }
}
'''
def getSendPost(userid,scen,templid='_dxyQ9KpIPEcLKUxuoQWg37HPGK46oMMR9WS7KGdUx4'):
    SendPos= wx_sendMessage_post % (userid,templid,scen)
    return SendPos.encode('utf-8')

# 一键关注公众号模拟接口
@csrf_exempt
def wxOpenTest(request):
    if request.method == 'POST':
        user_openid=request.POST.get('ftouser','')
        temple_id='w9tvnQj8dy0Bi7210U41rbV8qG5kx9aEAcqw-R4aacs'
        scen=request.POST.get('fscene','')
        resGetToken=requests.get(wxurl_getToken,headers=header_dict)
        if resGetToken.status_code==200:
            token=resGetToken.json()['access_token']
            resSend = requests.post(wxurl_sendMessage % token, data=getSendPost(user_openid,scen,temple_id), headers=header_dict)
            return HttpResponse(resSend.text)
        else:
            return HttpResponse("sdsds")
    else:
        return HttpResponse('request method error need POST but now is %s' % request.method)

# 一键关注公众号模拟接口
@csrf_exempt
def wxUrlTest(request):
    if request.method == 'GET':
        token=request.GET.get('token','')
        timestamp=request.GET.get('timestamp','')
        nonce=request.GET.get('nonce','')
        echostr=request.GET.get('echostr','')
        return HttpResponse(echostr)
    elif request.method == 'POST':
        # 回复空消息
        msg = parse_message(request.body)
        if msg.type == 'text':
            print(msg)
            client.message.send_text(msg.source, '客服消息测试')
        return HttpResponse(EmptyReply().render())


pos_lanhu=u'''
{
     "msgtype": "text",
     "text": {
         "content": "%s"
     },
     "at": {
         "atMobiles": [
             "%s"
         ],
         "isAtAll": false
     }
 }
'''

pos_lanhu_link=u'''
{
     "msgtype": "markdown",
     "markdown": {"title":"%s",
     "text":"%s"
     },
     "at": {
        "atMobiles": [
            "%s"
        ],
        "isAtAll": true
    }
 }
'''
lanhu_markdown=u'''
### %s
> %s
>
>\n\n
[查看详情](%s)
'''

lanhu_url="https://oapi.dingtalk.com/robot/send?access_token=eba1d9124acf2ae08cff6f65e053cff6e15caa02c9e4dcf2acf59e872ba0eafd"
@csrf_exempt
def lanhuAt(request):
    if request.method == 'POST':
        title=request.POST.get('title','')
        text=request.POST.get('text','')
        url_link=request.POST.get('url','')
        at=request.POST.get('at','')
        response = requests.post(lanhu_url, data=changeLanhuPosDataLink(title,text,url_link,at), headers=header_dict)
        return HttpResponse(response.text)
    else:
        return HttpResponse(request.method)

def changeLanhuPosData(title,text,url_link,at):
    test=lanhu_markdown % (title,text,url_link)
    posBody = pos_lanhu % (test,at)
    return posBody.encode('utf-8')

def changeLanhuPosDataLink(title,text,url_link,at):
    tex=lanhu_markdown % (title,text,url_link)
    posbody= pos_lanhu_link % (title,tex,at)
    return posbody.encode('utf-8')


@csrf_exempt
def firimWebHook(request):
    if request.method == 'POST':
        body=str(request.body,encoding = "utf-8")
        return HttpResponse(request.method)
    else:
        return HttpResponse(request.method)

@csrf_exempt
def weixin(request):
    if request.method == 'POST':
        msg=parse_message(request.body)
        if msg.type=='text':
            replay=TextReply(content=msg.content,message=msg)
            return HttpResponse(replay.render())
        return HttpResponse(TextReply(content="hah"))
    elif request.method == 'GET':
        print(request.GET)
        return HttpResponse(request.GET.get('echostr',default='110'))
