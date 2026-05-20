from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BiometricReadingViewSet, AnimalAlertViewSet

router = DefaultRouter()
router.register(r'biometric-readings', BiometricReadingViewSet, basename='biometric-reading')
router.register(r'animal-alerts', AnimalAlertViewSet, basename='animal-alert')

urlpatterns = [
    path('', include(router.urls)),
]
