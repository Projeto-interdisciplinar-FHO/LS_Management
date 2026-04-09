from django.urls import path
from .views import RegistrarEventoView 
from .views import DetalheBovinoView
from .views import BovinoListCreateView

urlpatterns = [
    path('registrar/', RegistrarEventoView.as_view(), name='registrar-evento'),
    path('detalhe/<str:rfid>/', DetalheBovinoView.as_view()),

    path('bovinos/', BovinoListCreateView.as_view(), name='bovino-create-list'),
    path('bovinos/<str:rfid_tag>/', DetalheBovinoView.as_view(), name='bovino-detail-view'),
    path('eventos/', RegistrarEventoView.as_view(), name='evento-create-list'),
]