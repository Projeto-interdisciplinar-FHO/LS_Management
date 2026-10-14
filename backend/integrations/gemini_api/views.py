"""
View opcional (Plus) para consulta avulsa de compatibilidade genealógica via API REST.
Permite que o frontend consulte previamente a IA sem necessariamente registrar a inseminação.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .cliente import validar_reproducao


class ValidarGenealogiaIAView(APIView):
    """
    Endpoint dedicado (recurso 'plus'):
    Recebe 'id_femea' e 'id_macho' via POST e retorna a análise genealógica da Fazenda Colorado.
    
    Exemplo de payload de entrada:
    {
        "id_femea": 10,
        "id_macho": 25,
        "observacoes": "Opcional: avaliação prévia de sêmen"
    }
    """
    # Pode ser ajustado conforme a política de segurança do projeto (ex: IsAuthenticated)
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        id_femea = request.data.get("id_femea")
        id_macho = request.data.get("id_macho")
        observacoes = request.data.get("observacoes")

        if not id_femea or not id_macho:
            return Response(
                {
                    "erro": "Os parâmetros 'id_femea' e 'id_macho' são obrigatórios.",
                    "exemplo_esperado": {"id_femea": 10, "id_macho": 25}
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            id_femea_int = int(id_femea)
            id_macho_int = int(id_macho)
        except (ValueError, TypeError):
            return Response(
                {"erro": "Os IDs 'id_femea' e 'id_macho' devem ser números inteiros."},
                status=status.HTTP_400_BAD_REQUEST
            )

        resultado = validar_reproducao(
            id_femea=id_femea_int,
            id_macho=id_macho_int,
            observacoes=observacoes
        )

        return Response(resultado, status=status.HTTP_200_OK)

