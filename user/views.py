from django.http.response import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action
from .models import UserProfile
from .serializers import UserSerializer
from utils.exceptions import InvalidPassword


class UserViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    # 指定在哪些字段模糊搜索
    search_fields = ['username', 'email', 'phone']

    # 剔除不要更新的字段
    def update(self, request, *args, **kwargs):
        request.data.pop('username', None)
        request.data.pop('id', None)
        request.data.pop('password', None)
        return super().update(request, *args, **kwargs)

    def get_object(self):
        if self.request.method.lower() != 'get':
            pk = self.kwargs.get('pk')
            if pk == '1' or pk == 1:
                raise Http404
        return super().get_object()

    @action(['GET'], detail=False, url_path='whoami')
    def whoami(self, request):
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username
            }
        })

    @action(['PATCH'], detail=True, url_path='setpwd')
    def setpwd(self, request, pk=None):
        user:UserProfile = request.user
        if user.check_password(request.data.get('oldPassword', '')):
            user.set_password(request.data.get('password', ''))
            user.save()
            return Response(status=201)
        else:
            raise InvalidPassword


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
