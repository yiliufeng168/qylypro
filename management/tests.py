from django.test import TestCase,Client

from .models import User
from customer.models import Reserve
from verification.models import Vofficer

class T(TestCase):
    vos=Vofficer.objects.all()
    volist=[]
    for vo in vos:
        volist.append(vo.vuser_id)
    vuser = User.objects.filter(type=User.TYPE_VERIFICATION)
    kuser=vuser.exclude(id__in=volist)

