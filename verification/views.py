from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
# Create your views here.

from customer.models import Reserve,Order
from .models import Vofficer

def writeoff(request):
    res_id=request.GET.get('res_id')
    vcode=request.GET.get('vcode')
    print(res_id)
    try:
        res=Reserve.objects.get(Q(id=res_id)&Q(virtualcode=vcode))
    except Reserve.DoesNotExist:
        return JsonResponse({"status":"false",'msg':'二维码无效'})
    user=request.session.get('user')

    try:
        Vofficer.objects.get(Q(vuser=user['id'])&Q(business=res.order.business))
    except Vofficer.DoesNotExist:
        return JsonResponse({'status':'false','msg':'核销员无法核销其他商户的二维码'})

    if res.usingstatus==Reserve.USINGSTATUS_USING:
        return JsonResponse({"status":"false",'msg':'已使用'})
    if res.startdatetime>timezone.now():
        return JsonResponse({"status":"false",'msg':'未到使用时间'})
    if res.enddatetime<timezone.now():
        res.usingstatus=Reserve.USINGSTATUS_OVERDUE
        res.save()
        return JsonResponse({"status":"false",'msg':'已过期'})
    res.usingstatus=Reserve.USINGSTATUS_USING
    res.save()
    return JsonResponse({"status":"OK"})