"""
Rotas de Importação e Exportação de Dados em formato XLSX (Excel).
Fornece endpoints isolados para vacas e ordenhas com total compatibilidade.
"""

from django.urls import path
from .ordenhas import ImportacaoOrdenhasView
from .vacas import ImportacaoVacasView

urlpatterns = [
    # Rota de importação e exportação de ordenhas (GET para modelo/exportação, POST para importação)
    path('ordenhas/', ImportacaoOrdenhasView.as_view(), name='importar-ordenhas-xlsx'),

    # Rota de importação e exportação de cadastro de vacas (GET para modelo/exportação, POST para importação)
    path('vacas/', ImportacaoVacasView.as_view(), name='importar-vacas-xlsx'),
]
