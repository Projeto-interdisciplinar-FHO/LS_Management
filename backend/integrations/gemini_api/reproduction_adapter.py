"""
Adapter para integração com a API do Google Gemini voltado à validação genealógica e reprodutiva.
Segue o padrão de projeto Adapter adotado na arquitetura do LS. Management.
"""

import os
import json
import re
from typing import Dict, Any, Optional
from google import genai
from dotenv import load_dotenv

from .reproduction_builder import ReproductionPromptBuilder

load_dotenv()


class GeminiReproductionAdapter:
    """Adapta o cliente Gemini ao contrato de validação genealógica e reprodutiva."""

    MODEL = "gemini-2.5-flash"

    def __init__(self, client=None):
        api_key = os.getenv("API_KEY")
        self.client = client or (genai.Client(api_key=api_key) if api_key else None)

    def validar_reproducao(
        self,
        dados_femea: Dict[str, Any],
        dados_macho: Dict[str, Any],
        observacoes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envia a árvore genealógica de ambos os animais para análise do Gemini
        e retorna o diagnóstico estruturado sobre consanguinidade e viabilidade reprodutiva.
        """
        if not self.client:
            return {
                "apto": False,
                "status": "ERRO_CONFIGURACAO",
                "nivel_risco_consanguinidade": "DESCONHECIDO",
                "geracao_parentesco_detectada": None,
                "ancestrais_comuns": [],
                "analise_genealogica": "Análise indisponível: Chave de API (API_KEY) do Gemini não configurada no ambiente.",
                "analise_zootecnica_complementar": "",
                "veredito_final": "Configurar a API_KEY no arquivo .env para executar a validação por IA."
            }

        prompt = (
            ReproductionPromptBuilder()
            .com_femea(dados_femea)
            .com_macho(dados_macho)
            .com_observacoes(observacoes or "Avaliação pré-inseminação")
            .build()
        )

        try:
            response = self.client.models.generate_content(
                model=self.MODEL,
                contents=prompt,
            )

            raw_text = response.text or ""
            return self._parse_json_response(raw_text)

        except Exception as error:
            return {
                "apto": False,
                "status": "ERRO_PROCESSAMENTO_IA",
                "nivel_risco_consanguinidade": "DESCONHECIDO",
                "geracao_parentesco_detectada": None,
                "ancestrais_comuns": [],
                "analise_genealogica": f"Falha na comunicação com o Gemini: {str(error)}",
                "analise_zootecnica_complementar": "",
                "veredito_final": "Não foi possível concluir a análise de consanguinidade por IA."
            }

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Limpa e converte a resposta do Gemini para dicionário Python."""
        clean_text = text.strip()

        # Remove delimitadores de código markdown caso o modelo tenha incluído
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]

        clean_text = clean_text.strip()

        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            # Fallback usando Regex caso haja texto antes ou depois do JSON
            match = re.search(r"(\{.*\})", clean_text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except Exception:
                    pass

            # Fallback caso não seja possível decodificar JSON
            return {
                "apto": False,
                "status": "RESPOSTA_NAO_ESTRUTURADA",
                "nivel_risco_consanguinidade": "ALERTA",
                "geracao_parentesco_detectada": None,
                "ancestrais_comuns": [],
                "analise_genealogica": clean_text,
                "analise_zootecnica_complementar": "",
                "veredito_final": "A IA retornou um parecer em formato de texto livre."
            }

