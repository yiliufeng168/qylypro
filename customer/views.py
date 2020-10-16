from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Min
from django.utils import timezone
# Create your views here.


import json
import requests
import uuid

from .models import Tourist
from management.models import User
from merchant.models import Business,Goods,Sell


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
    try:
        page = int(request.GET.get('page', 1))
        pagecount = int(request.GET.get('pagecount', 10))
        startdatetime=request.GET.get('startdatetime')
        enddatetime=request.GET.get('enddatetime')
    except:
        return JsonResponse({
            'status': 'false',
            'msg': '参数不正确',
        })
    online_users=User.objects.filter(status=User.STATUS_ONLINE).filter(type=User.TYPE_BUSINESS)
    buss=Business.objects.filter(user_id__in=online_users)
    type=request.GET.get('type')
    if type!=None:
        buss=buss.filter(type=type)
    Sell.objects.filter(goods__in=Goods.objects.filter(business__in=buss))
    bus_list=[]
    for bus in buss:
        b=bus.get_data_dic()
        golist=Goods.objects.filter(business=bus)
        sells=Sell.objects.filter(goods__in=golist)
        if startdatetime!=None:
            print(startdatetime)
            print(enddatetime)
            sells=sells.filter(startdatetime__lte=startdatetime).filter(enddatetime__gte=enddatetime)
        goods=sells.aggregate(Min('price'))
        if goods['price__min']!=None:
            b['minprice']=goods['price__min']
            bus_list.append(b)
    paginator = Paginator(bus_list, pagecount)
    page_num = paginator.num_pages
    page_bus_list = paginator.page(page)
    page_user_list_tolist = []
    # for sl in list(page_bus_list.object_list):
    #     if sl.enddatetime != None:
    #         if timezone.now().__gt__(sl.enddatetime):
    #             sl.delete()
    #             continue
    #     page_user_list_tolist.append(sl.getdatadic())
    if page_bus_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_bus_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page
    context = {
        'status': 'OK',
        'user_list': page_bus_list.object_list,
        'curr_page': page,
        'previous_page': previous_page,
        'next_page': next_page,
        'total_page': page_num,
        'total_bus':len(page_bus_list),
    }

    return JsonResponse(context)

def showgoods(request):
    return JsonResponse({'status':'OK'})