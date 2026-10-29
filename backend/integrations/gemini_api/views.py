"""
View para consulta e validação de compatibilidade genealógica via API REST.
Suporta tanto requisições GET (via query params) quanto POST (via JSON body),
oferecendo flexibilidade total para testes no Postman e integração no Frontend.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .cliente import validar_reproducao


class ValidarGenealogiaIAView(APIView):
    """
    Endpoint para validação genealógica e prevenção de consanguinidade por IA.
    
    Formatos suportados:
    1. GET (ideal para consultas em tempo real e testes rápidos no navegador/Postman):
       Ex: GET /api/reproducao/validar-genealogia/?cow_id=2&bull_id=1
       ou  GET /api/reproducao/validar-genealogia/?id_femea=2&id_macho=1
       
    2. POST (ideal para envio de payloads JSON a partir de formulários):
       Ex: POST /api/reproducao/validar-genealogia/
       Body: { "cow_id": 2, "bull_id": 1, "observacoes": "Opcional" }
    """
    permission_classes = [AllowAny]

    def _obter_dados_requisicao(self, request):
        """Extrai parâmetros de query string (GET) ou payload body (POST)."""
        if request.method == "GET":
            source = request.query_params
        else:
            source = request.data if isinstance(request.data, dict) else {}

        id_femea = (
            source.get("cow_id")
            or source.get("id_femea")
            or source.get("cow")
            or source.get("mother_id")
            or source.get("mother")
            or source.get("id_vaca")
        )
        id_macho = (
            source.get("bull_id")
            or source.get("id_macho")
            or source.get("bull")
            or source.get("father_id")
            or source.get("father")
            or source.get("id_touro")
        )
        observacoes = source.get("observacoes")

        return id_femea, id_macho, observacoes

    def _processar_validacao(self, request):
        id_femea, id_macho, observacoes = self._obter_dados_requisicao(request)

        if not id_femea or not id_macho:
            return Response(
                {
                    "erro": "É obrigatório fornecer a fêmea e o macho para validação.",
                    "parametros_femea_aceitos": ["cow_id", "id_femea", "mother_id", "id_vaca"],
                    "parametros_macho_aceitos": ["bull_id", "id_macho", "father_id", "id_touro"],
                    "exemplo_get": "/api/reproducao/validar-genealogia/?cow_id=2&bull_id=1",
                    "exemplo_post": {"cow_id": 2, "bull_id": 1}
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            id_femea_int = int(id_femea)
            id_macho_int = int(id_macho)
        except (ValueError, TypeError):
            return Response(
                {"erro": "Os IDs devem ser numéricos inteiros."},
                status=status.HTTP_400_BAD_REQUEST
            )

        resultado = validar_reproducao(
            id_femea=id_femea_int,
            id_macho=id_macho_int,
            observacoes=observacoes
        )

        return Response(resultado, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        """Consulta rápida via GET."""
        return self._processar_validacao(request)

    def post(self, request, *args, **kwargs):
        """Validação via POST com JSON."""
        return self._processar_validacao(request)
