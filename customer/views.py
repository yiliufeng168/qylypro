from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Min
from django.db.models import F
from django.db import transaction
from django.db.models import Count
from django.utils import timezone
# Create your views here.


import json
import requests
import uuid

from .models import Tourist,Order,Reserve
from management.models import User
from merchant.models import Business,Goods,Sell
from MyUtil.myUtil import pageUtil

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
            print(tourist.sessionid)
            tourist.save()
            context.update({
                'status':'OK',
                'msg':'登录成功',
            })

    jre = JsonResponse(context)
    if context.get('status')=='OK':
        jre.set_cookie('session_id',tourist.sessionid.hex)
    else:
        print('cookie set false')
    return jre

def showbusiness(request):
    try:
        page = int(request.GET.get('page', 1))
        pagecount = int(request.GET.get('pagecount', 10))
        startdatetime=request.GET.get('startdatetime')
        enddatetime=request.GET.get('enddatetime')
        icontains=request.GET.get('icontains')
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
    if icontains!=None:
        buss=buss.filter(name__icontains=icontains)
    Sell.objects.filter(goods__in=Goods.objects.filter(business__in=buss))
    bus_list=[]
    for bus in buss:
        b=bus.get_data_dic()
        golist=Goods.objects.filter(business=bus)
        sells=Sell.objects.filter(goods__in=golist)
        if startdatetime!=None:
            sells=sells.filter(startdatetime__lte=startdatetime).filter(enddatetime__gte=enddatetime)
        goods=sells.aggregate(Min('price'))
        if goods['price__min']!=None:
            b['minprice']=goods['price__min']
            bus_list.append(b)
    context = {'status': 'OK',}
    context.update(pageUtil(page,pagecount,bus_list))
    return JsonResponse(context)

def showgoods(request):
    try:
        page = int(request.GET.get('page', 1))
        pagecount = int(request.GET.get('pagecount', 10))
        startdatetime=request.GET.get('startdatetime')
        enddatetime=request.GET.get('enddatetime')
        bus_id = request.GET.get('business_id')
    except:
        return JsonResponse({
            'status': 'false',
            'msg': '参数不正确',
        })

    goodss=Goods.objects.filter(business_id=bus_id)
    print('len(goodss)',len(goodss))
    sells=Sell.objects.filter(goods__id__in=goodss)
    if startdatetime!=None:
        sells=sells.filter(startdatetime__lte=startdatetime).filter(enddatetime__gte=enddatetime)
    print('len(sells),',len(sells))
    se_list=[]
    for se in sells:
        god=se.goods.getdatadic()
        god.update(se.getdatadic())
        se_list.append(god)
    context={'status':"OK"}
    context.update(pageUtil(page,pagecount,se_list))
    return JsonResponse(context)

def sendorder(request):
    try:
        jsdata=json.loads(request.body)
        bus_id=jsdata['business']
        order_list=jsdata['order_list']
    except:
        return JsonResponse({'status':'false','msg':'参数错误'})
    try:
        bus=User.objects.get(id=bus_id)
    except Business.DoesNotExist:
        return JsonResponse({'status': 'false', 'msg': '商户不存在'})
    if bus.status!=User.STATUS_ONLINE:
        return JsonResponse({'status': 'false', 'msg': '商户已下线'})
    try:
        order=Order()
        order.id=uuid.uuid4()
        order.receiver=jsdata['receiver']
        order.phone=jsdata['phone']
        order.address=jsdata['address']
        order.remarks=jsdata['remarks']
        order.business=bus.business
        order.tourist=Tourist.objects.get(sessionid=request.COOKIES['session_id'])
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'false', 'msg': '请填写正确的订单信息'})
    totalprice = 0
    try:
        with transaction.atomic():
            for item in order_list:
                sell=Sell.objects.get(id=item['sell_id'])
                print('1')
                totalprice = totalprice + item['count'] * sell.price
                if sell.surplus-item['count']>=0:
                    sell.surplus=F('surplus')-item['count']
                    sell.save()
                else:
                    print(sell.id)
                    raise Exception

    except Exception as e:
        print(e)
        return JsonResponse({'status':'false','msg':"商品已售完"})
    print('2')
    order.totalprice=totalprice
    order.save()
    print('3')
    for item in order_list:
        reserve = Reserve()
        reserve.order = order
        print('3')
        reserve.id=uuid.uuid4()
        sell=Sell.objects.get(id=item['sell_id'])
        gd=sell.goods
        reserve.goods=gd

        reserve.goods_name=gd.name
        reserve.goods_price=sell.price
        reserve.goods_pic=gd.pic
        reserve.goods_count=item['count']
        reserve.startdatetime=sell.startdatetime
        reserve.enddatetime=sell.enddatetime
        reserve.save()
    return JsonResponse({'status':'OK'})

def showorderlist(request):
    try:
        page = int(request.GET.get('page', 1))
        pagecount = int(request.GET.get('pagecount', 10))
        order_staus=request.GET.get("order_status")
    except:
        return JsonResponse({
            'status': 'false',
            'msg': '参数不正确',
        })
    tourist=Tourist.objects.get(sessionid=request.COOKIES.get('session_id'))
    ords=Order.objects.filter(tourist=tourist).order_by('-order_time',)
    if order_staus!=None:
        ords=ords.filter(orderstatus=order_staus)
    ordlist=[]
    for ord in ords:
        a_ord={}
        a_ord['order_id']=ord.id.hex
        a_ord['order_time']=ord.order_time
        a_ord['business']=ord.business.user_id.hex
        a_ord['business_name']=ord.business.name
        a_ord['totalprice']=ord.totalprice
        a_ord['order_status']=ord.orderstatus
        goods_list=[]
        goodss=Reserve.objects.filter(order=ord)
        for res in goodss:
            mres={}
            mres['name']=res.goods_name
            mres['price']=res.goods_price
            mres['count']=res.goods_count
            mres['pic']=res.goods_pic.url
            goods_list.append(mres)
        a_ord['good_list']=goods_list
        ordlist.append(a_ord)
    context = {
        'status': 'OK',
    }
    context.update(pageUtil(page,pagecount,ordlist))
    return JsonResponse(context)

def showorderdetails(request):

    orderid=request.GET.get('orderid')
    if orderid==None:
        return JsonResponse({'status':'false','msg':'请输入正确的订单编号'})
    try:
        order=Order.objects.get(id=orderid)
    except Order.DoesNotExist:
        return JsonResponse({'status':'false','msg':'订单不存在'})
    print('2')
    context={
        'status': "OK",
        'orderid':orderid,
        'receiver':order.receiver,
        'phone':order.phone,
        'address':order.address,
        'totalprice':order.totalprice,
        'ordertime':order.order_time,
        'business_id':order.business_id.hex,
        'business_name':order.business.name,
        'orderstatus':order.orderstatus,
    }
    rlist=[]
    reslist=Reserve.objects.filter(order=order)
    for res in reslist:
        re={}
        re['res_id']=res.id.hex
        re['name']=res.goods_name
        re['price']=res.goods_price
        re['count']=res.goods_count
        re['startdatetime']=res.startdatetime
        re['enddatetime']=res.enddatetime
        re['goods_id']=res.goods_id.hex
        re['virtualcode']=res.virtualcode
        re['usingstatus']=res.usingstatus
        rlist.append(re)
    context.update({
        "rlist":rlist
    })
    return JsonResponse(context)

def showrecommend(request):
    try:
        page = int(request.GET.get('page', 1))
        pagecount = int(request.GET.get('pagecount', 10))
    except:
        return JsonResponse({
            'status': 'false',
            'msg': '参数不正确',
        })
    goods_insell=Sell.objects.all().values('goods').distinct()
    goods_inreserve=Reserve.objects.all().values('goods').distinct()
    res=Reserve.objects.filter(goods__in=goods_inreserve.intersection(goods_insell))
    tuijian_list=res.annotate(count=Count('goods')).values('goods', 'goods_count').distinct().order_by('-goods_count')
    tjgoods=[]
    for i in tuijian_list:
        tjgoods.append(i['goods'])
    print(tjgoods)
    tjgoods_list=Goods.objects.filter(id__in=tjgoods)
    tjgoods_list=tjgoods_list.annotate(min=Min('sell__price'))
    tjlist=[]
    for tj in tjgoods_list:
        tjdic={}
        tjdic.update(tj.getdatadic())
        tjdic.update({'minprice':tj.min})
        tjlist.append(tjdic)

    context={'status':"OK",}
    context.update(pageUtil(page,pagecount,tjlist))
    return JsonResponse(context)

def showgoodsdetail(request):
    goods_id=request.GET.get('goods_id')
    goods=Goods.objects.get(id=goods_id)
    sells=Sell.objects.filter(goods=goods)
    slist=[]
    for se in sells:
        sedic={}
        sedic.update(se.getdatadic())
        slist.append(sedic)

    return JsonResponse({'status':'OK','slist':slist})

def delreserve(request):
    orderid=request.GET.get('orderid')
    if orderid==None:
        return JsonResponse({'status': 'false', 'msg': '请填写正确的订单id'})
    try:
        order=Order.objects.get(id=orderid)
    except Order.DoesNotExist:
        return JsonResponse({'status': 'false', 'msg': '订单不存在'})
    try:
        tourist=Tourist.objects.get(sessionid=request.COOKIES.get('session_id'))
    except Tourist.DoesNotExist:
        print('未登录')
    if tourist.openid!=order.tourist_id:
        return JsonResponse({'status': 'false', 'msg': '订单不存在'})
    order.delete()
    return JsonResponse({'status':'OK'})


def getvcode(request):
    res_id=request.GET.get("res_id")
    try:
        res=Reserve.objects.get(id=uuid.UUID(res_id).hex)
    except Reserve.DoesNotExist:
        return JsonResponse({"status":"false",'msg':'res not exist'})
    if res.order.tourist_id!=Tourist.objects.get(sessionid=request.COOKIES.get('session_id')).openid:
        return JsonResponse({"status": "false", 'msg': '你没有这件宝贝'})
    if res.order.orderstatus!=Order.ORDER_STATUS_DELIVERED:
        return JsonResponse({"status": "false", 'msg': '未发货'})
    res.virtualcode=uuid.uuid4()
    res.save()



    return JsonResponse({"status":'OK','vcode':res.virtualcode.hex})