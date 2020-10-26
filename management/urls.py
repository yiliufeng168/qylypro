from django.urls import path

from .views import (index,login,loginout,
                    addUser,showUserList,
                    modifyUserStatus,modifySelfInfo,
                    modifyPassword,setstatus,addadmin,
                    addvofficers,showvofficers,showallvofficers,
                    delvofficers,delPackages,addPackage,
                    editPackage)

urlpatterns=[
    path('index/',index),
    path('login/',login),

    path('login/addadmin/',addadmin),
    path('loginout/',loginout),
    path('modifySelfInfo/',modifySelfInfo),
    path('modifyPassword/',modifyPassword),
    path('setstatus/',setstatus),

    # 下列需要管理员权限
    path('admin/addUser/',addUser),
    path('admin/showUserList/',showUserList),
    path('admin/modifyUserStatus/',modifyUserStatus),

    path('admin/addPackage/',addPackage),
    path('admin/editPackage/',editPackage),
    path('admin/delPackages/',delPackages),


    # 下列需商家权限
    path('business/addvofficers/',addvofficers),
    path('business/showvofficers/',showvofficers),
    path('business/showallvofficers/',showallvofficers),
    path('business/delvofficers/',delvofficers),
]