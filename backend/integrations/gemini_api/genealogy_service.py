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
        id_femea: int,
        id_macho: int,
        observacoes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executa o processo completo de validação genealógica para reprodução:
        - Consulta o banco de dados real em profundidade (até a 3ª geração: bisavós).
        - Envia a árvore completa ao Gemini para análise de consanguinidade e risco genético.
        - Retorna o veredito estruturado.
        """
        # Etapa 1: Captura os dados reais do banco de dados externo
        dados_arvore = self.extractor.extrair_arvore_completa(
            id_femea=id_femea,
            id_macho=id_macho
        )

        # Etapa 2: Executa a validação zootécnica e genealógica via Gemini
        veredito = self.adapter.validar_reproducao(
            dados_femea=dados_arvore.get("femea", {}),
            dados_macho=dados_arvore.get("macho", {}),
            observacoes=observacoes
        )

        # Anexa os dados extraídos de entrada para auditoria/rastreabilidade
        veredito["dados_consultados"] = dados_arvore

        return veredito


_reproduction_service = GenealogyReproductionService()


def validar_genealogia_reproducao(
    id_femea: int,
    id_macho: int,
    observacoes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Função Facade de entrada rápida para ser consumida diretamente pelo sistema.
    Uso:
        resultado = validar_genealogia_reproducao(id_femea=10, id_macho=25)
    """
    return _reproduction_service.validar_cruzamento(
        id_femea=id_femea,
        id_macho=id_macho,
        observacoes=observacoes
    )

