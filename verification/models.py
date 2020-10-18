from django.db import models

from merchant.models import Business
from management.models import User
# Create your models here.

class Vofficer(models.Model):
    vuser = models.OneToOneField(User, verbose_name='核销员id', on_delete=models.CASCADE, primary_key=True)
    business=models.ForeignKey(Business,on_delete=models.CASCADE,verbose_name='商户id')
