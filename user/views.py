from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.contrib.auth.models import User,AnonymousUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view, permission_classes

class MenuItem(dict):
    def __init__(self, id, name, path=None):
        super().__init__()
        self['id'] = id
        self['name'] = name
        self['path'] = path # 告诉前端静态路由
        self['children'] = []

    def append(self, subitem):
        self['children'].append(subitem)
        return self

@api_view()
def menulist_view(request):
    print(request.user) # User实例
    print(request.auth)
    # 菜单数据哪里来
    # 1、数据库里存着，反复拿这个不怎么变化的菜单
    # 2、写死
    menulist = []

    if request.user.is_superuser:
        item = MenuItem(1, '用户管理') # 管理员权限
        item.append(MenuItem(101, '用户列表', '/users'))
        item.append(MenuItem(102, '角色列表', '/users/roles'))
        item.append(MenuItem(103, '权限列表', '/users/perms'))

        menulist.append(item)

    return Response(menulist)