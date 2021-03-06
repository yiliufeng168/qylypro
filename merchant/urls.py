from django.urls import path

from .views import (editBusinessInfo, getBusinessInfo,
                    addgoods, addsell, showgoodslist,
                    showsells, delsells, delgoods, editgoods,
                    showorders, showorderdetails, processorders)

urlpatterns=[
    # business/目录下的地址需要商家权限,或登录
    path('business/editBusinessInfo/',editBusinessInfo),
    path('business/getBusinessInfo/', getBusinessInfo),


    path('business/addgoods/',addgoods),
    path('business/delgoods/', delgoods),
    path('business/showgoodslist/', showgoodslist),
    path('business/editgoods/',editgoods),

    path('business/addsell/',addsell),
    path('business/showsells/',showsells),
    path('business/delsells/',delsells),

    path('business/showorders/',showorders),
    path('business/showorderdetails/',showorderdetails),
    path('business/processorders/', processorders),
]