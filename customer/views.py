from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.


import json
import requests
import uuid

from .models import Tourist
from management.models import User
from merchant.models import Business,Goods


APPID='wx1a3241e73216cd5a'
APPSECRET='adee9dc7060fcd943ec80542d744437f'
LOGIN_URL='https://api.weixin.qq.com/sns/jscode2session?appid='+ APPID + '&secret='+ APPSECRET + '&js_code={}&grant_type=authorization_code'

req_sess=requests.session()

def login(request):
    context={
        'status':'false',
        'msg':'登录失败',
    }
    code=request.POST.get('code')
    if code!=None:
        url=LOGIN_URL.format(code)
        res=req_sess.get(url)
        print(res.text)
        r=json.loads(res.text)
        # {"errcode": 40029, "errmsg": "invalid code, hints: [ req_id: uHgEgP.Ce-H8C1Va ]"}
        # {"session_key":"XfCJith6amDms1bN0bJgXQ==","openid":"oEqMx5fHK7GNGcgZF4dFFsDBeXXs"}
        if r.get('openid')==None:
            context.update(r)
        else:
            try:
                tourist=Tourist.objects.get(openid=r.get('openid'))
            except Tourist.DoesNotExist:
                tourist=Tourist()
                tourist.openid=r.get('openid')
            tourist.sessionid=uuid.uuid4()
            tourist.session_key=r.get('session_key')
            tourist.save()
            context.update({
                'status':'OK',
                'msg':'登录成功',
            })

    jre = JsonResponse(context)
    if context.get('status')=='OK':
        jre.set_cookie('sessionid',tourist.sessionid.hex)
    else:
        print('cookie set false')
    return jre

def showbusiness(request):
    online_users=User.objects.filter(status=User.STATUS_ONLINE).filter(type=User.TYPE_BUSINESS)
    buss=Business.objects.filter(user_id__in=online_users)
    context={}
    bus_list=[]
    for bus in buss:
        bus_list.append(bus.get_data_dic())
    context['status']="OK"
    context['bus_list']=bus_list
    return JsonResponse(context)

def showgoods(request):
    return JsonResponse({'status':'OK'})