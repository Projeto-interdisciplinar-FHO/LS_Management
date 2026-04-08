from rest_framework.views import APIView
from rest_framework.response import Response
from gestao.models import Bovino, Historico
from .serializers import AnaliseCompletaSerializer

class RegistrarEventoView(APIView):
    def post(self, request):
        rfid = request.data.get('rfid')
        tipo = request.data.get('tipo')
        valor = request.data.get('valor')
        sintomas = request.data.get('sintomas', "")

        try:
            boi = Bovino.objects.get(rfid_tag=rfid)

            Historico.objects.create(animal=boi, tipo=tipo, valor=valor, sintomas=sintomas)
            return Response({"sucesso": "Registrado com sucesso!"})

        except Bovino.DoesNotExist:
            return Response({"erro": "Boi não encontrado"}, status=404)
        
class DetalheBovinoView(APIView):
    def get(self, request, rfid, format=None): 
        try:
            boi = Bovino.objects.get(rfid_tag=rfid)
            serializer = AnaliseCompletaSerializer(boi)
            return Response(serializer.data)
        except Bovino.DoesNotExist:
            return Response({"erro": "Não achei esse boi"}, status=404)