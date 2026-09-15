from django.urls import include, path

# Sem prefixo: o app atende users/, api/token/ e authentication/token/.
urlpatterns = [
    path('', include('apps.accounts.authentication.urls')),
]
