from django.urls import path

from .views import login,showgoods,showbusiness,sendorder,showorderlist,showorderdetails,delreserve,showrecommend


urlpatterns=[
    path('login/',login),
    path('showrecommend/',showrecommend),
    path('showgoods/',showgoods),
    path('showbusiness/',showbusiness),
    # 下列页面需要登陆后才能访问

    path('tourist/sendorder/',sendorder),
    path('tourist/showorderlist/',showorderlist),
    path('tourist/showorderdetails/',showorderdetails),
    path('tourist/delreserve/',delreserve),

]
