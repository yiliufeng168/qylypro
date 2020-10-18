from django.db import models

import uuid

from management.models import User
from merchant.models import Goods,Business


# Create your models here.

class Tourist(models.Model):
    openid=models.CharField(max_length=32,primary_key=True,verbose_name='openid')
    sessionid=models.UUIDField(default=uuid.uuid4(),verbose_name='sessionid')
    session_key=models.CharField(max_length=32,verbose_name='session_key')

class Order(models.Model):
    ORDER_STATUS_NOT_DELIVERED = 0
    ORDER_STATUS_DELIVERED = 1
    ORDER_STATUS_ERROR = 2
    ORDER_STATUS_CLOSE=3
    ORDER_STATUS_ITEMS = (
        (ORDER_STATUS_NOT_DELIVERED, '未发货'),
        (ORDER_STATUS_DELIVERED, '已发货'),
        (ORDER_STATUS_ERROR, '异常'),
        (ORDER_STATUS_CLOSE,'关闭')
    )

    id=models.UUIDField(verbose_name='订单ID',primary_key=True,default=uuid.uuid4())
    order_time=models.DateTimeField(auto_now_add=True,verbose_name='下单时间')
    receiver=models.CharField(max_length=40,verbose_name='收货人')
    phone=models.CharField(max_length=20,verbose_name="手机号")
    address=models.CharField(max_length=128,verbose_name="地址")
    remarks=models.CharField(max_length=200,verbose_name='备注')
    totalprice=models.FloatField(verbose_name='总价')
    business=models.ForeignKey(Business,on_delete=models.DO_NOTHING,verbose_name='商家')
    orderstatus=models.PositiveIntegerField(default=ORDER_STATUS_NOT_DELIVERED,choices=ORDER_STATUS_ITEMS,verbose_name='订单状态')
    tourist= models.ForeignKey(Tourist, on_delete=models.DO_NOTHING, verbose_name='游客ID')




class Reserve(models.Model):
    USINGSTATUS_NOUSING = 0
    USINGSTATUS_USING = 1
    USINGSTATUS_OVERDUE=2
    USINGSTATUS_ITEMS = (
        (USINGSTATUS_NOUSING, '未使用'),
        (USINGSTATUS_USING, '已使用'),
        (USINGSTATUS_OVERDUE,'已过期'),
    )
    id=models.UUIDField(verbose_name='订单详细ID',primary_key=True,default=uuid.uuid4())
    order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='订单ID')
    goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, verbose_name='商品ID')
    virtualcode = models.URLField(verbose_name='虚拟码')
    usingstatus = models.PositiveIntegerField(default=USINGSTATUS_NOUSING, choices=USINGSTATUS_ITEMS, verbose_name='使用状态')

    #冗余属性

    goods_name = models.CharField(max_length=50, verbose_name='商品名')
    goods_pic = models.ImageField( verbose_name='图片地址', blank=True)
    goods_price = models.FloatField(verbose_name='价格')
    goods_count = models.PositiveIntegerField(verbose_name='数量')
    startdatetime = models.DateTimeField(verbose_name='开始时间')
    enddatetime = models.DateTimeField(verbose_name='结束时间')

    def getdatadic(self):
        data={}
        data['id']=self.id.hex
        data['virtualcode']=self.virtualcode
        data['usingstatus']=self.usingstatus
        data['goods_name']=self.goods_name
        data['goods_pic']=self.goods_pic.url
        data['goods_price']=self.goods_price
        data['goods_count']=self.goods_count
        data['startdatetime']=self.startdatetime
        data['enddatetime']=self.enddatetime
        data['goods_id']=self.goods_id.hex
        return data


