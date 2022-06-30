from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import menulist_view, UserViewSet

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
                  path('menulist/', menulist_view)
              ] + router.urls
