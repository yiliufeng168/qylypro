from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

from .models import Business,Goods,Sell
from customer.models import Reserve,Order
from .forms import EditBusinessInfoForm,GoodsForm,SellForm,EditGoodsForm
from MyUtil.myUtil import pageUtil

import json
# Create your views here.

def editBusinessInfo(request):
    context={'status':'false'}
    user=request.session.get('user')
    try:
        business=Business.objects.get(user_id=user['id'])
    except Business.DoesNotExist:
        business=Business()
        business.user_id=user['id']
        business.save()

    info=EditBusinessInfoForm(request.POST)
    if info.is_valid():
        cleaned_data=info.cleaned_data
        business.name=cleaned_data['name']
        business.location=cleaned_data['location']
        business.pic.delete(True)
        business.pic=request.FILES.get('pic')
        business.star=cleaned_data['star']
        business.type=cleaned_data['type']
        business.introduct=cleaned_data['introduct']
        business.save()
        context['status']='OK'
    else:
        context['msg']=info.errors.get_json_data()
    return JsonResponse(context)

def getBusinessInfo(request):
    context={'status':'OK'}
    user=request.session.get('user')
    try:
        business=Business.objects.get(user_id=user['id'])
    except Business.DoesNotExist:
        business=Business()
        business.user_id=user['id']
        business.save()
    try:
        picurl=business.pic.url
    except ValueError:
        picurl=""

    context['business']={
        'name':business.name,
        'location':business.location,
        'pic':picurl,
        'star':business.star,
        'introduct':business.introduct,
        'score':business.score,
        'type':business.type,
    }

    return JsonResponse(context)



def addgoods(request):
    context={'status':'OK'}
    form=GoodsForm(request.POST)
    if form.is_valid():
        cleaned_data=form.cleaned_data
        goods=Goods()
        goods.name=cleaned_data['name']
        goods.pic=request.FILES.get('pic')
        goods.introduct=cleaned_data['introduct']

        uid=user_id=request.session.get('user')['id']
        try:
            bus=Business.objects.get(user_id=uid)
        except Business.DoesNotExist:
            bus = Business()
            bus.user_id = uid
            bus.save()
        goods.business = bus
        goods.save()
    else:
        context.update({
            'status':'false',
            'msg':'表单错误',
            'formerr':form.errors.get_json_data(),
        })
    return JsonResponse(context)

def addsell(request):
    context={'status':"OK"}
    form=SellForm(request.POST)
    if form.is_valid():
        cleaned_data=form.cleaned_data

        if cleaned_data['goods'].business_id.hex!=request.session.get('user')['id']:
            return JsonResponse({
                'status':'false',
                'msg':'商家没有该商品'
            })
        sell = Sell()
        sell.goods = cleaned_data['goods']
        sell.total=cleaned_data['total']
        sell.surplus=sell.total
        sell.price=cleaned_data['price']
        if cleaned_data['startdatetime']!=None and cleaned_data['enddatetime']!=None :
            if cleaned_data['enddatetime']<timezone.now():
                return JsonResponse({'status':"false","msg":'不能发售截止日期在今天之前的商品'})
            sell.startdatetime=cleaned_data['startdatetime']
            sell.enddatetime=cleaned_data['enddatetime']
        sell.save()
    else:
        context['status']="false",
        context['formerr']=form.errors.get_json_data(),
    return JsonResponse(context)

def showsells(request):
    try:
        page = int(request.GET.get('page', 1))
        pagecount = int(request.GET.get('pagecount', 10))
        goods_id=request.GET.get('goods')
        sellout=int(request.GET.get('sellout'),0)
    except:
        return JsonResponse({
            'status': 'false',
            'msg': '参数不正确',
        })
    sslist=Sell.objects.filter(goods=goods_id)
    if sellout==1:
        sslist=sslist.filter(surplus__gt=0)
    elif sellout==2:
        sslist=sslist.filter(surplus=0)
    selllist = sslist.order_by('startdatetime')

    selist=[]
    for se in selllist:
        # if se.enddatetime!=None:
        #     print(se.enddatetime)
        #     print(se.enddatetime>timezone.now())
        #     print(timezone.now())
        #     if timezone.now()>se.enddatetime:
        #         se.delete()
        #         continue
        selist.append(se.getdatadic())
    context={'status':'OK'}
    context.update(pageUtil(page,pagecount,selist))
    return JsonResponse(context)

def showgoodslist(request):
    try:
        page = int(request.GET.get('page', 1))
        pagecount = int(request.GET.get('pagecount', 10))
    except:
        return JsonResponse({
            'status': 'false',
            'msg': '参数不正确',
        })
    goodslist = Goods.objects.filter(business=request.session.get('user')['id']).order_by('-name')
    gdlist=[]
    for gd in goodslist:
        gdlist.append(gd.getdatadic())
    context={"status":"OK"}
    context.update(pageUtil(page,pagecount,gdlist))
    return JsonResponse(context)

def delsells(request):
    context={
        'status':'OK'
    }
    del_list=request.GET.get('del_list')
    if del_list.endswith(','):
        del_list=del_list[:-1]
    del_list=del_list.split(',')
    user=request.session.get('user')
    for se in del_list:
        try:
            print(se)
            print(Sell.objects.get(id=se).goods.business.user_id.hex)
            print(user['id'])
            if Sell.objects.get(id=se).goods.business.user_id.hex != user['id']:
                return JsonResponse({
                    "msg": '用户没有删除该sell权限',
                    'status': 'false'
                })
        except Sell.DoesNotExist:
            return JsonResponse({
                "msg": 'sellid不存在',
                'status': 'false'
            })
    for se in del_list:
        sell=Sell.objects.get(id=se)
        sell.delete()
    return JsonResponse(context)

def delgoods(request):
    context={
        'status':'OK'
    }
    del_list=request.GET.get('del_list')
    if del_list.endswith(','):
        del_list=del_list[:-1]
    del_list=del_list.split(',')
    user = request.session.get('user')
    for go in del_list:
        if Goods.objects.get(id=go).business.user_id.hex!=user['id']:
            return JsonResponse({
                "msg": '用户没有删除该商品权限',
                'status': 'false',
                'goods_id':go,
            })
    for go in del_list:
        sell=Goods.objects.get(id=go)
        sell.delete()
    return JsonResponse(context)

def editgoods(request):
    context = {'status': 'OK'}
    print('edit')
    form = EditGoodsForm(request.POST)
    print('for')
    if form.is_valid():
        cleaned_data = form.cleaned_data
        try:
            goods = Goods.objects.get(id=cleaned_data['id'])
            if goods.business.user_id.hex!=request.session.get('user')['id']:
                return JsonResponse({'status':'false','msg':'用户没有权限'})
        except Goods.DoesNotExist:
            return JsonResponse({'status':'false','msg':'商品不存在'})
        goods.name = cleaned_data['name']
        goods.pic.delete(True)
        goods.pic = request.FILES.get('pic')
        goods.introduct=cleaned_data['introduct']
        goods.save()
    else:
        context.update({
            'status': 'false',
            'msg': '表单错误',
            'formerr': form.errors.get_json_data(),
        })
    return JsonResponse(context)

def showorders(request):
    try:
        page = int(request.GET.get('page', 1))
        pagecount = int(request.GET.get('pagecount', 10))
        order_status=request.GET.get('order_status')
    except:
        return JsonResponse({
            'status': 'false',
            'msg': '参数不正确',
        })
    user=request.session.get('user')
    orders=Order.objects.filter(business_id=user['id']).order_by('-order_time')
    if order_status!=None:
        orders=orders.filter(orderstatus=order_status)
    olist=[]
    for od in orders:
        odic={}
        odic['order_id']=od.id.hex
        odic['order_time']=od.order_time
        odic['receiver']=od.receiver
        odic['phone']=od.phone
        odic['address']=od.address
        odic['remarks']=od.remarks
        odic['orderstatus']=od.orderstatus
        olist.append(odic)
    context={
        'status':"OK"
    }
    context.update(pageUtil(page,pagecount,olist))
    return JsonResponse(context)

def showorderdetails(request):
    orderid=request.GET.get('order_id')
    user=request.session.get('user')
    try:
        order=Order.objects.get(Q(id=orderid)&Q(business_id=user['id']))
    except Order.DoesNotExist:
        return JsonResponse({"status":'false','msg':'订单不存在'})
    odic = {}
    odic['order_id'] = order.id.hex
    odic['order_time'] = order.order_time
    odic['receiver'] = order.receiver
    odic['phone'] = order.phone
    odic['address'] = order.address
    odic['remarks'] = order.remarks
    odic['orderstatus'] = order.orderstatus
    ress=Reserve.objects.filter(order=order)
    print(ress)
    reslist=[]
    for r in ress:
        print('1')
        reslist.append(r.getdatadic())
    context = {
        'status': "OK",
        'relist':reslist
    }
    context.update(odic)
    return JsonResponse(context)

def processorders(request):
    jsdata=json.loads(request.body)
    if jsdata['orderstatus']==0:
        return JsonResponse({"status": "false",'msg':'参数错误'})
    user=request.session.get('user')
    ods=Order.objects.filter(id__in=jsdata['order_ids']).filter(business_id=user['id'])
    if len(ods)==0:
        return JsonResponse({"status": "false",'msg':'订单不存在'})
    if len(ods)!=len(jsdata['order_ids']):
        return JsonResponse({"status": "false",'msg':'订单id有误'})
    for od in ods:
        od.orderstatus=jsdata['orderstatus']
        od.save()
    return JsonResponse({"status":"OK"})
