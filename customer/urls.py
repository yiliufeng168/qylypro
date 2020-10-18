from django.urls import path

from .views import (login,showgoods,showbusiness,
                    sendorder,showorderlist,showorderdetails,
                    delreserve,showrecommend,showgoodsdetail,
                    getvcode)


urlpatterns=[
    path('login/',login),
    path('showrecommend/',showrecommend),
    path('showgoods/',showgoods),
    path('showbusiness/',showbusiness),
    path('showgoodsdetail/',showgoodsdetail),

    # 下列页面需要登陆后才能访问

    path('tourist/sendorder/',sendorder),
    path('tourist/showorderlist/',showorderlist),
    path('tourist/showorderdetails/',showorderdetails),
    path('tourist/delreserve/',delreserve),
    path('tourist/getvcode/',getvcode),
]
