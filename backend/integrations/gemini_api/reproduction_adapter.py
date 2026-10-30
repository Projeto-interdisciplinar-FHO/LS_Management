"""
Adapter para integração com a API do Google Gemini voltado à validação genealógica e reprodutiva.
Segue o padrão de projeto Adapter adotado na arquitetura do LS. Management.
Possui camada de fail-safe determinística para garantir 100% de segurança genética.
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
        parentesco_direto: Optional[Dict[str, Any]] = None,
        observacoes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envia a árvore genealógica de ambos os animais para análise do Gemini
        e retorna o diagnóstico estruturado sobre consanguinidade e viabilidade reprodutiva.
        """
        # Se não há API_KEY configurada, mas detectamos parentesco direto no banco, já emitimos a reprovação segura!
        if not self.client:
            if parentesco_direto:
                return {
                    "apto": False,
                    "status": "REPROVADO_CONSANGUINIDADE",
                    "nivel_risco_consanguinidade": "CRITICO" if parentesco_direto.get("grau") == 1 else "ALTO",
                    "geracao_parentesco_detectada": parentesco_direto.get("grau"),
                    "ancestrais_comuns": [
                        {
                            "id": dados_macho.get("id"),
                            "nome": dados_macho.get("nome"),
                            "parentesco_na_femea": parentesco_direto.get("tipo"),
                            "parentesco_no_macho": "O próprio reprodutor"
                        }
                    ],
                    "analise_genealogica": parentesco_direto.get("descricao"),
                    "analise_zootecnica_complementar": f"ECC da vaca: {dados_femea.get('escore_ecc')}.",
                    "veredito_final": f"Cruzamento reprovado: {parentesco_direto.get('descricao')} (API do Gemini não configurada para análise textual expandida)."
                }

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
            .com_parentesco_direto(parentesco_direto)
            .com_observacoes(observacoes or "Avaliação pré-inseminação")
            .build()
        )

        try:
            response = self.client.models.generate_content(
                model=self.MODEL,
                contents=prompt,
            )

            raw_text = response.text or ""
            resultado = self._parse_json_response(raw_text)

            # Fail-safe determinístico: se o banco identificou parentesco direto, 'apto' NUNCA pode ser True
            if parentesco_direto:
                resultado["apto"] = False
                resultado["status"] = "REPROVADO_CONSANGUINIDADE"
                if not resultado.get("geracao_parentesco_detectada"):
                    resultado["geracao_parentesco_detectada"] = parentesco_direto.get("grau")

            return resultado

        except Exception as error:
            # Em caso de falha de conexão com a IA, mas havendo parentesco no banco, garante a segurança
            if parentesco_direto:
                return {
                    "apto": False,
                    "status": "REPROVADO_CONSANGUINIDADE",
                    "nivel_risco_consanguinidade": "CRITICO",
                    "geracao_parentesco_detectada": parentesco_direto.get("grau"),
                    "ancestrais_comuns": [{"id": dados_macho.get("id"), "nome": dados_macho.get("nome")}],
                    "analise_genealogica": parentesco_direto.get("descricao"),
                    "analise_zootecnica_complementar": "",
                    "veredito_final": f"Reprovado: {parentesco_direto.get('descricao')}"
                }

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
            match = re.search(r"(\{.*\})", clean_text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except Exception:
                    pass

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
