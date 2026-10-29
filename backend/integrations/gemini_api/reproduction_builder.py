"""
Builder para a construção de prompts de validação genealógica e reprodução bovina.
Segue o padrão de projeto Builder adotado na integração com o Gemini.
Sincronizado com os campos de Cow (score/ECC, reproductive_status, breed) e Bull (register_number, breed).
"""

import json
from typing import Dict, Any, Optional


class ReproductionPromptBuilder:
    """Builder do prompt genealógico e reprodutivo enviado ao Gemini."""

    def __init__(self):
        self._femea: Optional[Dict[str, Any]] = None
        self._macho: Optional[Dict[str, Any]] = None
        self._parentesco_direto: Optional[Dict[str, Any]] = None
        self._observacoes: Optional[str] = None

    def com_femea(self, femea: Dict[str, Any]) -> "ReproductionPromptBuilder":
        self._femea = femea
        return self

    def com_macho(self, macho: Dict[str, Any]) -> "ReproductionPromptBuilder":
        self._macho = macho
        return self

    def com_parentesco_direto(self, parentesco: Optional[Dict[str, Any]]) -> "ReproductionPromptBuilder":
        self._parentesco_direto = parentesco
        return self

    def com_observacoes(self, observacoes: str) -> "ReproductionPromptBuilder":
        self._observacoes = observacoes
        return self

    def build(self) -> str:
        dados_reproducao = {
            "femea_candidata": self._femea or {},
            "macho_candidato": self._macho or {},
            "parentesco_direto_identificado_no_banco": self._parentesco_direto or "Nenhum parentesco direto detectado",
            "observacoes_adicionais": self._observacoes or "Avaliação prévia de acasalamento"
        }

        arvore_json = json.dumps(dados_reproducao, ensure_ascii=False, indent=2)

        alerta_parentesco = ""
        if self._parentesco_direto:
            alerta_parentesco = (
                f"\n\n[ALERTA CRÍTICO DO SISTEMA]\n"
                f"O banco de dados detectou parentesco direto entre os dois animais: "
                f"{self._parentesco_direto.get('descricao', '')} (Grau: {self._parentesco_direto.get('grau')}ª geração). "
                f"Este cruzamento DEVE ser reprovado por consanguinidade.\n"
            )

        return (
            "Você é um Zootecnista Ph.D. especialista em Genética e Melhoramento de Gado Leiteiro "
            "da Fazenda Colorado. Sua responsabilidade é avaliar se o acasalamento (Inseminação Artificial ou TE) "
            "entre os dois animais candidatos abaixo é seguro e geneticamente viável.\n\n"
            "DADOS DOS CANDIDATOS E ÁRVORES GENEALÓGICAS (ATÉ 3 GERAÇÕES - PAIS, AVÓS, BISAVÓS):\n"
            f"```json\n{arvore_json}\n```"
            f"{alerta_parentesco}\n\n"
            "DIRETRIZES TÉCNICAS E REGRAS DE NEGÓCIO DA FAZENDA COLORADO:\n"
            "1. REGRA ESTREITA DE NÃO-CONSANGUINIDADE: É expressamente proibido o cruzamento entre animais aparentados. "
            "Verifique cuidadosamente se o touro candidato é o pai ou avô da vaca, ou se há qualquer nó em comum nas árvores "
            "genealógicas (Paterna e Materna) de ambos os animais até a 3ª geração "
            "(1ª geração: Pais; 2ª geração: Avós; 3ª geração: Bisavós).\n"
            "2. Se for detectado QUALQUER ancestral em comum (mesmo ID ou mesmo nome de pai, mãe, avô, avó, bisavô ou bisavó) "
            "em até 3 gerações, o cruzamento deve ser marcado como 'apto': false, identificando a geração do conflito e os nomes dos ancestrais.\n"
            "3. Explique os riscos zootécnicos do cruzamento (ex: depressão endogâmica, risco de fixação de alelos deletérios recessivos, "
            "redução na longevidade e produção de leite).\n"
            "4. Avalie o Escore (ECC/Score) da vaca (escore_ecc): comente a adequação para inseminação e o status reprodutivo.\n"
            "5. Se NÃO houver nenhum ancestral em comum até a 3ª geração, marque 'apto': true, com 'nivel_risco_consanguinidade': 'NENHUM'.\n\n"
            "FORMATO OBRIGATÓRIO DE RESPOSTA:\n"
            "Responda EXCLUSIVAMENTE em formato JSON puro (sem marcação markdown externa extra se possível), contendo a seguinte estrutura:\n"
            "{\n"
            '  "apto": true ou false,\n'
            '  "status": "APROVADO" ou "REPROVADO_CONSANGUINIDADE" ou "ALERTA_ZOOTECNICO",\n'
            '  "nivel_risco_consanguinidade": "NENHUM" ou "BAIXO" ou "MEDIO" ou "ALTO" ou "CRITICO",\n'
            '  "geracao_parentesco_detectada": 1, 2, 3 ou null,\n'
            '  "ancestrais_comuns": [\n'
            '    {\n'
            '      "id": 0,\n'
            '      "nome": "Nome do Ancestral",\n'
            '      "parentesco_na_femea": "Ex: Avô Paterno ou Pai",\n'
            '      "parentesco_no_macho": "Ex: O próprio touro ou Avô"\n'
            '    }\n'
            '  ],\n'
            '  "analise_genealogica": "Explicação detalhada sobre a compatibilidade das linhagens e verificação de parentesco.",\n'
            '  "analise_zootecnica_complementar": "Parecer sobre o ECC (score), raça e status reprodutivo da fêmea.",\n'
            '  "veredito_final": "Conclusão objetiva e recomendação técnica para o produtor da Fazenda Colorado."\n'
            "}"
        )
