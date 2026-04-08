from django.contrib import admin
from .models import Bovino, Historico

@admin.register(Bovino)
class BovinoAdmin(admin.ModelAdmin):
    list_display = ('rfid_tag', 'nome', 'status')
    search_fields = ('rfid_tag', 'nome')
    list_filter = ('status',)

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('animal', 'tipo', 'valor', 'data')
    list_filter = ('tipo', 'data')

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['animal'].queryset = Bovino.objects.exclude(status__iexact='vendido')
        return super().render_change_form(request, context, *args, **kwargs)