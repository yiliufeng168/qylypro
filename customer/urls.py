from django.urls import path

from .views import login,showgoods,showbusiness
urlpatterns=[
    path('login/',login),

    # 下列页面需要登陆后才能访问
    path('tourist/showgoods/',showgoods),
    path('tourist/showbusiness/',showbusiness),

]
