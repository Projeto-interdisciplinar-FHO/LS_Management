"""
Módulo de Integrações do Google Gemini para o LS. Management.
Foco exclusivo na validação genealógica e viabilidade reprodutiva bovina (prevenção de consanguinidade).
"""

from .gemini_api.reproduction_builder import ReproductionPromptBuilder
from .gemini_api.reproduction_adapter import GeminiReproductionAdapter
from .gemini_api.genealogy_extractor import GenealogyExtractor
from .gemini_api.genealogy_service import (
    GenealogyReproductionService,
    validar_genealogia_reproducao,
)
from .gemini_api.cliente import validar_reproducao
from .gemini_api.views import ValidarGenealogiaIAView

__all__ = [
    "ReproductionPromptBuilder",
    "GeminiReproductionAdapter",
    "GenealogyExtractor",
    "GenealogyReproductionService",
    "validar_genealogia_reproducao",
    "validar_reproducao",
    "ValidarGenealogiaIAView",
]
