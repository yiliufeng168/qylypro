from django.test import TestCase
from django.db.models import Count

from merchant.models import Sell
from .models import Reserve
# Create your tests here.
import uuid
class TGG(TestCase):
    goods_insell = Sell.objects.all().values('goods').distinct()
    goods_inreserve = Reserve.objects.all().values('goods').distinct()
    res=Reserve.objects.filter(goods__in=goods_inreserve.intersection(goods_insell))
    print(res.annotate(count=Count('goods')).values('goods','goods_count').distinct().order_by('-goods_count'))



