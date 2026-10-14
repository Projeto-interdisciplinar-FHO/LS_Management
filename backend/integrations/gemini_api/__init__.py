"""
Módulo de Integrações do Google Gemini para o LS. Management.
Foco exclusivo na validação genealógica e viabilidade reprodutiva bovina (prevenção de consanguinidade).
"""

from .reproduction_builder import ReproductionPromptBuilder
from .reproduction_adapter import GeminiReproductionAdapter
from .genealogy_extractor import GenealogyExtractor
from .genealogy_service import (
    GenealogyReproductionService,
    validar_genealogia_reproducao,
)
from .cliente import validar_reproducao
from .views import ValidarGenealogiaIAView

__all__ = [
    "ReproductionPromptBuilder",
    "GeminiReproductionAdapter",
    "GenealogyExtractor",
    "GenealogyReproductionService",
    "validar_genealogia_reproducao",
    "validar_reproducao",
    "ValidarGenealogiaIAView",
]
