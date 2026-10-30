"""Índice de rotas do projeto.

Cada módulo (apps/<modulo>/urls.py) define os prefixos dos seus apps, e cada
app (apps/<modulo>/<app>/urls.py) define as próprias rotas.
"""
from django.contrib import admin
from django.urls import include, path

from integrations.gemini_api.views import ValidarGenealogiaIAView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.api.urls')),
    path('', include('apps.accounts.urls')),

    # -------------------------------------------------------------------------
    # ROTAS DE INTELIGÊNCIA ARTIFICIAL - VALIDAÇÃO GENEALÓGICA E REPRODUÇÃO
    # -------------------------------------------------------------------------

    # Rota 1: Endpoint Padrão da API REST (/api/reproducao/validar-genealogia/)
    path('api/reproducao/validar-genealogia/', ValidarGenealogiaIAView.as_view(), name='validar-genealogia-ia'),
    # DESCRIÇÃO DE USO:
    # Avalia a compatibilidade genética entre uma vaca e um touro para prevenir cruzamentos consanguíneos
    # até a 3ª geração (pais, avós e bisavós), analisando também ECC (score) e regras da Fazenda Colorado.
    #
    # 1. Requisição via GET (ideal para consultas em tempo real no Frontend e testes rápidos no navegador/Postman):
    #    -> URL: GET /api/reproducao/validar-genealogia/?cow_id=2&bull_id=1
    #    -> Parâmetros aceitos na URL: cow_id (ou id_femea) e bull_id (ou id_macho)
    #
    # 2. Requisição via POST (ideal para envio de payloads JSON a partir de formulários):
    #    -> URL: POST /api/reproducao/validar-genealogia/
    #    -> Headers: Content-Type: application/json
    #    -> Body JSON: { "cow_id": 2, "bull_id": 1, "observacoes": "Opcional" }
    #
    # 3. Resposta esperada (JSON):
    #    -> 'apto': boolean (True se aprovado, False se houver parentesco ou inconformidade)
    #    -> 'status': string ("APROVADO", "REPROVADO_CONSANGUINIDADE", etc.)
    #    -> 'nivel_risco_consanguinidade': string ("NENHUM", "BAIXO", "MEDIO", "ALTO", "CRITICO")
    #    -> 'geracao_parentesco_detectada': int ou null (1 = Pais, 2 = Avós, 3 = Bisavós)
    #    -> 'ancestrais_comuns': lista de ancestrais identificados
    #    -> 'veredito_final': parecer técnico detalhado para o produtor

    # Rota 2: Atalho Direto (/reproducao/validar-genealogia/)
    path('reproducao/validar-genealogia/', ValidarGenealogiaIAView.as_view(), name='validar-genealogia-ia-short'),
    # DESCRIÇÃO DE USO:
    # Rota idêntica à Rota 1 acima, funcionando como um alias direto sem o prefixo '/api/' para dar
    # flexibilidade total à equipe de Frontend conforme as convenções adotadas no projeto.
]
