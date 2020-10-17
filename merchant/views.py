from django.http import JsonResponse
from django.utils import timezone

from .models import Business,Goods,Sell
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
    except:
        return JsonResponse({
            'status': 'false',
            'msg': '参数不正确',
        })
    selllist = Sell.objects.filter(goods=goods_id).order_by('startdatetime')
    for sl in selllist:
        if sl.enddatetime!=None:
            if timezone.now().__gt__(sl.enddatetime):
                sl.delete()
                continue
    selist=[]
    for se in selllist:
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
        'status':'ok'
    }
    del_list=request.GET.get('del_list')
    if del_list.endswith(','):
        del_list=del_list[:-1]
    del_list=del_list.split(',')
    user=request.session.get('user')
    for se in del_list:
        try:
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
        'status':'ok'
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
        goods.price = cleaned_data['price']
        goods.save()
    else:
        context.update({
            'status': 'false',
            'msg': '表单错误',
            'formerr': form.errors.get_json_data(),
        })
    return JsonResponse(context)


def editsell(request):
    pass


