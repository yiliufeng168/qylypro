from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.utils import IntegrityError


from .models import User
from .forms import LoginUserForm,AddUserForm,ModifySelfInfoForm


import hashlib
import json

# Create your views here.
def index(request):
    return HttpResponse("ok")

class SessionUtil():
    def getSession(session,key):
        return session.get(key)
    def setSession(session,key,value):
        session[key]=value

def login(request):
    session=request.session
    if request.method=='GET':
        user=SessionUtil.getSession(session, 'user')
        return JsonResponse(user)
    else:
        context={
            'msg':"用户名或密码错误",
            'status':"false",
        }
        form=LoginUserForm(request.POST)
        if form.is_valid():
            user=User.get_byUName_and_PWord(form.cleaned_data['username'],form.cleaned_data['password'])
            if user!=None:
                if user.status==User.STATUS_DELETE:
                    context.update({
                        'msg':'该用户被禁止登陆',
                        'status':'false',
                    })
                else:
                    user_dict = user.to_dic()
                    print(json.dumps(user_dict))
                    SessionUtil.setSession(session, 'user',user_dict)
                    print(json.dumps(session.get('user')))
                    us=user_dict.copy()
                    us.pop('id')
                    print(json.dumps(session.get('user')))
                    context.update({
                        'msg':'login success',
                        "user":us,
                        'status':'OK',
                    })
        return JsonResponse(context)

def loginout(request):
    request.session.delete('session_key')
    request.session.clear()
    return JsonResponse({
        'status':'OK',
        'msg':'已退出'
    })
    pass

def addUser(request):
    context={
        'status':"false",
    }
    form=AddUserForm(request.POST)
    if form.is_valid():
        cleaned_data=form.cleaned_data
        user=User()
        user.register_save(cleaned_data)
        context['msg'] = '添加成功',
        context['status'] = 'OK'
    else:
        context['form_err']=form.errors.get_json_data()
    return JsonResponse(context)

def addadmin(request):
    admins= User.objects.filter(type=0)
    if len(admins)==0:
        context = {
            'status': "false",
        }
        form = AddUserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['type']=0
            user = User()
            user.register_save(cleaned_data)
            context['msg'] = '添加成功',
            context['status'] = 'OK'
        else:
            context['form_err'] = form.errors.get_json_data()
        return JsonResponse(context)
    else:
        return JsonResponse({
            'status':'false',
            'msg':'管理员注册端口已关闭'
        })

def showUserList(request):
    try:
        page=int(request.GET.get('page',1))
        pagecount=int(request.GET.get('pagecount',10))
    except:
        return JsonResponse({
            'status':'false',
            'msg':'参数不正确',
        })
    user_list=User.objects.filter(~Q(type=0)).order_by('username')
    paginator=Paginator(user_list,pagecount)
    page_num=paginator.num_pages
    page_user_list=paginator.page(page)
    page_user_list_tolist=[]
    for us in list(page_user_list.object_list):
        page_user_list_tolist.append(us.__str__())
    if page_user_list.has_next():
        next_page=page+1
    else:
        next_page=page
    if page_user_list.has_previous():
        previous_page=page-1
    else:
        previous_page=page
    context = {
        'status':'OK',
        'user_list': page_user_list_tolist,
        'curr_page': page,
        'previous_page': previous_page,
        'next_page': next_page,
        'total_page':page_num,
    }
    return JsonResponse(context)

def modifyUserStatus(request):
    username_lsit=request.GET.get('username_list')
    status = request.GET.get('status')
    if username_lsit==None or status==None:
        return JsonResponse({
            'status':'false',
            'msg':'参数不正确'
        })

    context={"status":'OK'}
    users=User.objects.filter(username__in=username_lsit.split(',')).filter(~Q(type=0))
    for us in users:
        us.status=status
        us.save()
    return JsonResponse(context)

def modifySelfInfo(request):
    context={
        'status':'false',
    }
    form=ModifySelfInfoForm(request.POST)
    if form.is_valid():
        cleaned_data=form.cleaned_data
        user_id=SessionUtil.getSession(request.session,'user')['id']
        my_user=User.objects.get(id=user_id)
        my_user.username=cleaned_data['username']
        my_user.phone=cleaned_data['phone']
        my_user.email=cleaned_data['email']
        my_user.status=cleaned_data['status']
        try:
            my_user.save()
            SessionUtil.setSession(request.session,'user',my_user.to_dic())
            context['status'] ='OK'
            context['msg'] = '修改成功'

        except IntegrityError:
            context['form_err']={
                'username':[
                    {
                        'message':'该用户名已存在',
                        'code':'invalid',
                    }
                ]
            }
    else:
        context['form_err'] = form.errors.get_json_data()
    return JsonResponse(context)

def modifyPassword(request):
    context={
        'status':'false'
    }
    if request.method=='POST':
        oldpwd=request.POST.get('oldpwd')
        newpwd=request.POST.get('newpwd')
        if oldpwd!=None and newpwd!=None:
            # hashlib.md5(clean_data['password'].encode(encoding='UTF-8')).hexdigest()
            user=User.objects.get(id=request.session.get('user')['id'])
            if hashlib.md5(oldpwd.encode(encoding='UTF-8')).hexdigest()==user.password:
                user.password=hashlib.md5(newpwd.encode(encoding='UTF-8')).hexdigest()
                user.save()
                context['msg']='修改成功'
                context['status']='OK'
            else:
                context['msg']='原始密码不正确'
        else:
            context.update({
                'msg':'表单错误',
            })
    else:
        context.update({
            'msg':'请使用POST方法',
        })
    return JsonResponse(context)

def setstatus(request):
    context={'status':"OK"}
    online=request.GET.get('online')
    nowuser=request.session.get('user')
    user=User.objects.get(id=nowuser['id'])
    if user.status!=0:
        if online=="true":
            user.status=User.STATUS_ONLINE
        else:
            user.status=User.STATUS_OFFLINE
        user.save()
    else:
        context['status']='false'
        context['msg']='用户没有权限'
    return JsonResponse(context)