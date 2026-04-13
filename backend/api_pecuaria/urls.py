from django.urls import path
from .views import RegistrarEventoView 
from .views import DetalheBovinoView
from .views import BovinoListCreateView

urlpatterns = [
    path('bovinos/', BovinoListCreateView.as_view(), name='bovino-create-list'),

    path('bovinos/<str:rfid_tag>/', DetalheBovinoView.as_view(), name='bovino-detail-view'),

    path('historicos/', RegistrarEventoView.as_view(), name='historico-list-create'),
]