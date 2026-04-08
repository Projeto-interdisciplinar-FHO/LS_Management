from django.urls import path
from .views import RegistrarEventoView 
from .views import DetalheBovinoView

urlpatterns = [
    path('registrar/', RegistrarEventoView.as_view(), name='registrar-evento'),
    path('detalhe/<str:rfid>/', DetalheBovinoView.as_view()),
]