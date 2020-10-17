from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse,JsonResponse

from .models import Tourist

class PowerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        #此模块用于各种权限过滤
        # 第一层过滤
        # 在/merchant下，未登录用户只能访问login
        url_d=request.path[1:].split('/')

        # url一级目录为management
        if url_d[0]=='customer':
            # 二级url如果为business
            # 则需验证登录
            if url_d[1]=='tourist':
                session_id = request.COOKIES['session_id']
                if session_id==None :
                    return JsonResponse({
                        "msg":'请先登录',
                        'status':'false'
                    })
                else:
                    try:
                        Tourist.objects.get(sessionid=session_id)
                    except Tourist.DoesNotExist:
                        return JsonResponse({
                            "msg": '登陆过期，请重新登陆',
                            'status': 'false'
                        })





    def process_response(self,request, response):#基于请求响应
        # print("md1  process_response 方法！", id(request)) #在视图之后
        return response

    def process_view(self,request, view_func, view_args, view_kwargs):
        # print("md1  process_view 方法！") #在视图之前执行 顺序执行
        #return view_func(request)
        pass


    def process_exception(self, request, exception):#引发错误 才会触发这个方法
        # print("md1  process_exception 方法！")
        # return HttpResponse(exception) #返回错误信息
        pass