from django.urls import path
from .views import financeiro, relfinanceiro
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'fazenda', FazendaViewSet)


urlpatterns = [
    path('financeiro/', financeiro, name='financeiro'),
    path('relfinanceiro/', relfinanceiro, name='relfinanceiro'),
    # url(r'^', include(router.urls), name='fazenda'),
]
