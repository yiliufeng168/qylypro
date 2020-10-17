from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

import os
import uuid


from management.models import User
# Create your models here.

#商户图片保存地址
def pic_path(instance,filename):
    base_path=''
    if type(instance)==Business:
        base_path=instance.TYPE_ITEMS[instance.type][1]
    else:
        business=instance.business
        base_path=os.path.join(business.TYPE_ITEMS[business.type][1],instance.name)
    ext=filename.split('.')[-1]
    filename='{}.{}'.format('img/'+uuid.uuid4().hex,ext)

    return os.path.join(base_path,filename)

# CASCADE
    # 删除级联，当父表的记录删除时，子表中与其相关联的记录也会删除。即：当一个老师被删除时，关联该老师的学生也会被删除。
    # PROTECT
    # 子表记录所关联的父表记录被删除时，会报ProtectedError异常。即：当一个学生所关联的老师被删除时，会报ProtectedError异常。
    # SET_NULL
    # 子表记录所关联的父表记录被删除时，将子表记录中的关联字段设为NULL，注意：需要允许数据表的该字段为NULL。
    # SET_DEFAULT
    # 子表记录所关联的父表记录被删除时，将子表记录中的关联字段设为一个给定的默认值。
    # DO_NOTHING
    # 子表记录所关联的父表记录被删除时，什么也不做。
    # SET()
    # 设置为一个传递给SET()
    # 的值或者一个回调函数的返回值，该参数用得相对较少。

class Business(models.Model):

    STAR_LEVEL0=0
    STAR_LEVEL1=1
    STAR_LEVEL2=2
    STAR_LEVEL3=3
    STAR_LEVEL4=4
    STAR_LEVEL5=5

    TYPE_HOTEL=0
    TYPE_SCENIC_SPOT=1
    TYPE_ITEMS=(
        (TYPE_HOTEL,'酒店'),
        (TYPE_SCENIC_SPOT,'景区'),
    )


    user=models.OneToOneField(User,verbose_name='ID',on_delete=models.CASCADE,primary_key=True)
    name=models.CharField(max_length=50,verbose_name='商家名')
    location=models.CharField(max_length=128,verbose_name='地址')
    pic=models.ImageField(upload_to=pic_path,verbose_name='图片地址',blank=True)
    star=models.PositiveIntegerField(default=STAR_LEVEL0,choices=((i,i) for i in range(0,6)),verbose_name='星级')
    introduct=models.CharField(max_length=1000,verbose_name='简介')

    #评分由管理员修改
    score=models.DecimalField(max_digits=2,decimal_places=1,default=0,verbose_name='评分')
    type=models.PositiveIntegerField(default=TYPE_HOTEL,choices=TYPE_ITEMS,verbose_name='类型')

    def get_data_dic(self):
        bus={
            'id':self.user_id.hex,
            'name':self.name,
            'location':self.location,
            'pic':self.pic.url,
            'star':self.star,
            'introduct':self.introduct,
            'score':self.score,
            'type':self.type,
        }
        return bus


    class Meta:
        verbose_name=verbose_name_plural='商户'

class Goods(models.Model):
    id=models.UUIDField(verbose_name='商品编号',default=uuid.uuid4,primary_key=True)

    name=models.CharField(max_length=50,verbose_name='商品名')
    pic=models.ImageField(upload_to=pic_path,verbose_name='图片地址',blank=True)
    introduct=models.CharField(max_length=500,verbose_name='简介',null=True)
    business=models.ForeignKey(Business,verbose_name='所属商家',on_delete=models.CASCADE)

    def getdatadic(self):
        picurl=''
        if self.pic!='':
            picurl=self.pic.url
        goods={
            'goods_id':self.id.hex,
            'name':self.name,
            'pic':picurl,
            'introduct':self.introduct,
        }
        return goods

@receiver(pre_delete,sender=Goods)
def goods_delete(sender,instance,**kwargs):
    # 后续修改
    print('*'*50)
    print('待reserve表完成后修改： 图片删除时，判断reserve是否还有该图，无则删除')
    print('*'*50)
    instance.pic.delete(False)

class Sell(models.Model):
    total=models.PositiveIntegerField(verbose_name='发售数量')
    surplus = models.PositiveIntegerField(default=total, verbose_name='剩余数量')
    #商品有效期
    startdatetime = models.DateTimeField(verbose_name='开始时间',blank=True,null=True)
    enddatetime = models.DateTimeField(verbose_name='结束时间',blank=True,null=True)
    goods=models.ForeignKey(Goods,verbose_name='所指的的商品',on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='价格',default=999)
    def getdatadic(self):
        sell={
            'total':self.total,
            'surplus':self.surplus,
            'startdatetime':self.startdatetime,
            'enddatetime':self.enddatetime,
            'price': self.price,
            'sell_id':self.id,
        }
        return sell






