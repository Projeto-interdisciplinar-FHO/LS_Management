import os
from dotenv import load_dotenv

from .reproduction_builder import ReproductionPromptBuilder
from .reproduction_adapter import GeminiReproductionAdapter
from .genealogy_extractor import GenealogyExtractor
from .genealogy_service import (
    GenealogyReproductionService,
    validar_genealogia_reproducao,
    _reproduction_service
)

load_dotenv()


def validar_reproducao(*args, **kwargs):
    """
    Ponto de entrada centralizado para a validação genealógica de reprodução por IA.
    Aceita:
        validar_reproducao(id_femea=2, id_macho=1)
        validar_reproducao(cow_id=2, bull_id=1)
        validar_reproducao(mother_id=2, father_id=1)
    """
    return validar_genealogia_reproducao(*args, **kwargs)


# Mantido apenas como stub para evitar quebras caso algum arquivo externo importe o método legado
def gerar_alerta_nutricional(*args, **kwargs):
    """Módulo de IA para nutrição descontinuado em prol da validação genealógica."""
    return "Módulo nutricional descontinuado. O foco da IA é exclusivamente a validação genealógica."
