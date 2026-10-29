"""
Módulo de Fachada (Facade) para a Validação Genealógica e Reprodutiva por IA.
Orquestra o ciclo de vida completo:
1. Extração dos dados e genealogia real no banco de dados externo (GenealogyExtractor).
2. Construção do contexto e envio ao modelo Gemini (GeminiReproductionAdapter).
3. Entrega do veredito estruturado (Apto / Inapto, grau de risco e parecer zootécnico).
"""

from typing import Dict, Any, Optional
from .genealogy_extractor import GenealogyExtractor
from .reproduction_adapter import GeminiReproductionAdapter


class GenealogyReproductionService:
    """Fachada unificada para o serviço de validação reprodutiva por IA."""

    def __init__(self, extractor: Optional[GenealogyExtractor] = None, adapter: Optional[GeminiReproductionAdapter] = None):
        self.extractor = extractor or GenealogyExtractor()
        self.adapter = adapter or GeminiReproductionAdapter()

    def validar_cruzamento(
        self,
        id_femea: Optional[int] = None,
        id_macho: Optional[int] = None,
        cow_id: Optional[int] = None,
        bull_id: Optional[int] = None,
        mother_id: Optional[int] = None,
        father_id: Optional[int] = None,
        observacoes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executa o processo completo de validação genealógica para reprodução:
        - Aceita tanto id_femea/id_macho quanto cow_id/bull_id e mother_id/father_id.
        - Consulta o banco de dados real em profundidade (até a 3ª geração: bisavós).
        - Envia a árvore completa ao Gemini para análise de consanguinidade e risco genético.
        - Retorna o veredito estruturado.
        """
        femea_id = id_femea or cow_id or mother_id
        macho_id = id_macho or bull_id or father_id

        if not femea_id or not macho_id:
            return {
                "apto": False,
                "status": "ERRO_PARAMETROS",
                "nivel_risco_consanguinidade": "DESCONHECIDO",
                "geracao_parentesco_detectada": None,
                "ancestrais_comuns": [],
                "analise_genealogica": "É obrigatório fornecer o ID da fêmea (vaca/matriz) e do macho (touro/reprodutor).",
                "analise_zootecnica_complementar": "",
                "veredito_final": "Forneça os IDs da vaca e do touro para validação genealógica."
            }

        # Etapa 1: Captura os dados reais do banco de dados (modelos Cow, Bull, Birth, Insemination)
        dados_arvore = self.extractor.extrair_arvore_completa(
            id_femea=int(femea_id),
            id_macho=int(macho_id)
        )

        parentesco_direto = dados_arvore.get("parentesco_direto_detectado")

        # Etapa 2: Executa a validação zootécnica e genealógica via Gemini com fail-safe
        veredito = self.adapter.validar_reproducao(
            dados_femea=dados_arvore.get("femea", {}),
            dados_macho=dados_arvore.get("macho", {}),
            parentesco_direto=parentesco_direto,
            observacoes=observacoes
        )

        # Anexa os dados extraídos de entrada para auditoria/rastreabilidade
        veredito["dados_consultados"] = dados_arvore

        return veredito


_reproduction_service = GenealogyReproductionService()


def validar_genealogia_reproducao(*args, **kwargs) -> Dict[str, Any]:
    """
    Função Facade de entrada rápida para ser consumida diretamente pelo sistema.
    Aceita múltiplos formatos de argumentos:
        validar_genealogia_reproducao(id_femea=2, id_macho=1)
        validar_genealogia_reproducao(cow_id=2, bull_id=1)
        validar_genealogia_reproducao(mother_id=2, father_id=1)
    """
    if len(args) == 2:
        return _reproduction_service.validar_cruzamento(id_femea=args[0], id_macho=args[1], **kwargs)
    return _reproduction_service.validar_cruzamento(**kwargs)
