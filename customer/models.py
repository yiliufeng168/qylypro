from django.db import models

import uuid

from management.models import User
from merchant.models import Goods,Business


# Create your models here.



class Order(models.Model):
    id=models.UUIDField(verbose_name='订单ID',primary_key=True)
    order_time=models.DateTimeField(auto_now_add=True,verbose_name='下单时间')
    receiver=models.CharField(max_length=20,verbose_name='收货人')
    phone=models.CharField(max_length=20,verbose_name="手机号")
    address=models.CharField(max_length=128,verbose_name="地址")
    remarks=models.CharField(max_length=200,verbose_name='备注')

class Reserve(models.Model):
    ORDER_STATUS_NOT_DELIVERED = 0
    ORDER_STATUS_DELIVERED = 1
    ORDER_STATUS_ERROR = 2
    ORDER_STATUS_ITEMS = (
        (ORDER_STATUS_NOT_DELIVERED, '未发货'),
        (ORDER_STATUS_DELIVERED, '已发货'),
        (ORDER_STATUS_ERROR, '异常'),
    )

    USINGSTATUS_NOUSING = 0
    USINGSTATUS_USING = 1
    USINGSTATUS_OVERDUE=2
    USINGSTATUS_ITEMS = (
        (USINGSTATUS_NOUSING, '未使用'),
        (USINGSTATUS_USING, '已使用'),
        (USINGSTATUS_OVERDUE,'已过期'),
    )
    order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='订单ID')
    goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, verbose_name='商品ID')

    tourist_id=models.CharField(max_length=36,verbose_name="游客ID")
    orderstatus=models.PositiveIntegerField(default=ORDER_STATUS_NOT_DELIVERED,choices=ORDER_STATUS_ITEMS,verbose_name='订单状态')
    virtualcode = models.URLField(verbose_name='虚拟码')
    usingstatus = models.PositiveIntegerField(default=USINGSTATUS_NOUSING, choices=USINGSTATUS_ITEMS, verbose_name='使用状态')

    #冗余属性
    business_name=models.CharField(max_length=50,verbose_name='商家名')
    business_location=models.CharField(max_length=128,verbose_name='地址')
    business_pic=models.ImageField(verbose_name='图片地址',blank=True)
    goods_name = models.CharField(max_length=50, verbose_name='商品名')
    goods_pic = models.ImageField( verbose_name='图片地址', blank=True)
    goods_price = models.FloatField(verbose_name='价格')
    goods_count = models.PositiveIntegerField(verbose_name='数量')
    startdatetime = models.DateTimeField(verbose_name='开始时间')
    enddatetime = models.DateTimeField(verbose_name='结束时间')


class Tourist(models.Model):
    openid=models.CharField(max_length=32,primary_key=True,verbose_name='openid')
    sessionid=models.UUIDField(default=uuid.uuid4(),verbose_name='sessionid')
    session_key=models.CharField(max_length=32,verbose_name='session_key')
