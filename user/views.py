from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from .models import UserProfile
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class MenuItem(dict):
    def __init__(self, id, name, path=None):
        super().__init__()
        self['id'] = id
        self['name'] = name
        self['path'] = path  # 告诉前端静态路由
        self['children'] = []

    def append(self, subitem):
        self['children'].append(subitem)
        return self


@api_view()
def menulist_view(request):
    menulist = []
    if request.user.is_superuser:
        item = MenuItem(1, '用户管理')  # 管理员权限
        item.append(MenuItem(101, '用户列表', '/users'))
        item.append(MenuItem(102, '角色列表', '/users/roles'))
        item.append(MenuItem(103, '权限列表', '/users/perms'))

        menulist.append(item)

    return Response(menulist)
