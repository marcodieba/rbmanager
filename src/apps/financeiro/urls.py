from django.urls import path
from .views import financeiro, relfinanceiro, editar_movimento, excluir_movimento
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'fazenda', FazendaViewSet)


urlpatterns = [
    path('financeiro/', financeiro, name='financeiro'),
    path('relfinanceiro/', relfinanceiro, name='relfinanceiro'),
    path('editar/<int:id>/', editar_movimento, name='editar_movimento'),
    path('excluir/<int:id>/', excluir_movimento, name='excluir_movimento'),
    # url(r'^', include(router.urls), name='fazenda'),
]
