from django.test import TestCase
from django.db.models import Count,Min

from merchant.models import Sell,Goods
from .models import Reserve
# Create your tests here.
import uuid
class TGG(TestCase):
    # goods_insell = Sell.objects.all().values('goods').distinct()
    # goods_inreserve = Reserve.objects.all().values('goods').distinct()
    # res=Reserve.objects.filter(goods__in=goods_inreserve.intersection(goods_insell))
    # tuijian_list=res.annotate(count=Count('goods')).values('goods', 'goods_count').distinct().order_by('-goods_count')
    # print(tuijian_list)
    # tj_list=[]
    # for g in tuijian_list:
    #     tj_list.append(g['goods'])
    # se=Sell.objects.filter(goods__in=tuijian_list)
    se=Sell.objects.all().aggregate(min=Min('price'))
    print(se)
    for s in se:
        print(type(s))
        print(s)
    goods=Goods.objects.annotate(min=Min('sell__price'))
    for g in goods:
        print(g.name,g.min)

class Tggg(TestCase):
    res=Reserve.objects.get(id=uuid.UUID('729b9090a6cb4e4e8d4313ae1644ba0e'))
    print(res)



