# from django.conf.urls import  include
from django.urls import path
from .views import rebanho, relrebanho
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'fazenda', FazendaViewSet)


urlpatterns = [
    path('rebanho/', rebanho, name='rebanho'),
    path('relrebanho/', relrebanho, name='relrebanho'),
    # url(r'^', include(router.urls), name='fazenda'),
]
