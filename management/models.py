from django.core.serializers import serialize
from django.db import models


import hashlib
import uuid
# Create your models here.



class User(models.Model):
    STATUS_ONLINE = 2
    STATUS_OFFLINE = 1
    STATUS_DELETE=0
    STATUS_ITEMS=(
        (STATUS_DELETE, '禁用'),
        (STATUS_OFFLINE,'离线'),
        (STATUS_ONLINE, '在线'),
    )


    TYPE_ADMIN=0
    TYPE_VERIFICATION=1
    TYPE_BUSINESS=2
    TYPE_ITEMS=(
        (TYPE_ADMIN, '管理员'),
        (TYPE_VERIFICATION,'核销员'),
        (TYPE_BUSINESS, '商户'),
    )
    id=models.UUIDField(verbose_name='ID',db_index=True,primary_key=True,default=uuid.uuid4,editable=False)
    username=models.CharField(max_length=50,verbose_name='用户名',unique=True)
    password=models.CharField(max_length=50,verbose_name='密码')
    phone=models.CharField(max_length=20,verbose_name='手机号')
    email=models.EmailField(verbose_name='邮箱')
    type=models.PositiveIntegerField(default=TYPE_VERIFICATION,choices=TYPE_ITEMS,verbose_name='类型')
    status=models.PositiveIntegerField(default=STATUS_OFFLINE,choices=STATUS_ITEMS,verbose_name='状态')

    def register_save(self,clean_data):
        self.username=clean_data['username']
        self.password=hashlib.md5(clean_data['password'].encode(encoding='UTF-8')).hexdigest()
        self.phone=clean_data['phone']
        self.email=clean_data['email']
        self.type=clean_data['type']
        return super(User,self).save()


    def __str__(self):
        user={
            'username': self.username,
            'phone': self.phone,
            'email': self.email,
            'type': self.type,
            'status': self.status,
        }
        return user

    def to_dic(self):
        user = {
            'id': self.id.hex,
            'username': self.username,
            'phone': self.phone,
            'email': self.email,
            'type': self.type,
            'status': self.status,
        }
        return user
    # 14e1b600b1fd579f47433b88e8d85291
    # e10adc3949ba59abbe56e057f20f883e

    @classmethod
    def get_byUName_and_PWord(cls,username,password):
        try:
            qs_user=cls.objects.get(username=username,password=hashlib.md5(password.encode(encoding='UTF-8')).hexdigest())
            # user={
            #     'id':qs_user.id.hex,
            #     'username':qs_user.username,
            #     'phone':qs_user.phone,
            #     'email':qs_user.email,
            #     'type':qs_user.type,
            #     'status':qs_user.status,
            # }
        except cls.DoesNotExist:
            qs_user=None
        return qs_user

    class Meta:
        verbose_name=verbose_name_plural='用户'





