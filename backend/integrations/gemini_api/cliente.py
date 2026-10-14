import os
from dotenv import load_dotenv

from .reproduction_builder import ReproductionPromptBuilder
from .reproduction_adapter import GeminiReproductionAdapter
from .genealogy_extractor import GenealogyExtractor
from .genealogy_service import (
    GenealogyReproductionService,
    validar_genealogia_reproducao,
)

load_dotenv()

# Instância padrão para o serviço de reprodução e genealogia
_reproduction_adapter = GeminiReproductionAdapter()
_reproduction_service = GenealogyReproductionService(adapter=_reproduction_adapter)


def validar_reproducao(id_femea: int, id_macho: int, observacoes: str = None):
    """
    Ponto de entrada centralizado para a validação genealógica de reprodução por IA.
    Delega diretamente para o serviço genealógico.
    """
    return _reproduction_service.validar_cruzamento(
        id_femea=id_femea,
        id_macho=id_macho,
        observacoes=observacoes
    )


# Mantido apenas como stub para evitar quebras caso algum arquivo externo importe o método legado
def gerar_alerta_nutricional(*args, **kwargs):
    """Módulo de IA para nutrição descontinuado em prol da validação genealógica."""
    return "Módulo nutricional descontinuado. O foco da IA é exclusivamente a validação genealógica."
from .genealogy_service import validar_genealogia_reproducao  # noqa: E402