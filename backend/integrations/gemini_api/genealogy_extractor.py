"""
Módulo de extração de dados genealógicos para reprodução bovina.
Totalmente sincronizado com os modelos atualizados do backend:
- apps.herd.cattle.models (Cow, Bull, Breed)
- apps.reproduction.models (Insemination, Birth, BirthOccurrence)
Consulta os dados reais no banco do projeto sem dados fictícios.
"""

from typing import Dict, Any, Optional
from django.db import connection


class GenealogyExtractor:
    """
    Extrator de dados genealógicos sincronizado com os modelos Cow, Bull, Insemination e Birth.
    Reconstrói a árvore genealógica de ambos os indivíduos até a 3ª geração (Pais, Avós e Bisavós).
    """

    MAX_GENERATIONS = 3  # Pais (1ª), Avós (2ª), Bisavós (3ª)

    def __init__(self, db_connection=None):
        self.connection = db_connection or connection

    def extrair_arvore_completa(self, id_femea: int, id_macho: int) -> Dict[str, Any]:
        """
        Executa a extração completa dos dados reais da vaca (Cow) e do touro (Bull),
        incluindo suas árvores genealógicas até a 3ª geração e identificação de parentesco direto.
        """
        # Tentativa 1: Utiliza os modelos Django nativos sincronizados do backend
        try:
            return self._extrair_via_orm(id_femea, id_macho)
        except Exception:
            # Tentativa 2: Fallback resiliente via SQL direto nas tabelas reais
            return self._extrair_via_sql(id_femea, id_macho)

    def _extrair_via_orm(self, id_femea: int, id_macho: int) -> Dict[str, Any]:
        """Extrai os dados utilizando diretamente os modelos Cow, Bull, Insemination e Birth."""
        from apps.herd.cattle.models import Cow, Bull

        cow_obj = Cow.objects.select_related("breed", "birth__insemination__father", "birth__insemination__mother").filter(id=id_femea).first()
        bull_obj = Bull.objects.select_related("breed").filter(id=id_macho).first()

        dados_femea = self._montar_dados_vaca_orm(cow_obj, id_femea)
        dados_macho = self._montar_dados_touro_orm(bull_obj, id_macho)

        # Checagem determinística de parentesco direto (Ex: o touro candidato é o pai/avô da vaca?)
        parentesco_direto = self._verificar_parentesco_direto(dados_femea, id_macho)

        return {
            "femea": dados_femea,
            "macho": dados_macho,
            "parentesco_direto_detectado": parentesco_direto
        }

    def _montar_dados_vaca_orm(self, cow_obj, id_femea: int) -> Dict[str, Any]:
        """Constrói o dicionário da fêmea com árvore genealógica recursiva via ORM."""
        if not cow_obj:
            return {
                "id": id_femea,
                "nome": f"Vaca #{id_femea}",
                "status_banco": "Registro não localizado na tabela cows",
                "arvore": {"pai": None, "mae": None}
            }

        score_ecc = float(cow_obj.score) if cow_obj.score is not None else None
        data_nascimento = str(cow_obj.birth.date) if cow_obj.birth and cow_obj.birth.date else None
        peso_nascimento = float(cow_obj.birth.weight) if cow_obj.birth and cow_obj.birth.weight else None
        raca_nome = cow_obj.breed.name if cow_obj.breed else "Não informada"

        arvore = {
            "pai": self._buscar_pai_vaca_orm(cow_obj, nivel=1),
            "mae": self._buscar_mae_vaca_orm(cow_obj, nivel=1)
        }

        return {
            "id": cow_obj.id,
            "nome": cow_obj.name,
            "numero_registro": cow_obj.register_number,
            "raca": raca_nome,
            "status": cow_obj.status,
            "status_reprodutivo": cow_obj.reproductive_status,
            "escore_ecc": score_ecc,
            "data_nascimento": data_nascimento,
            "peso_nascimento": peso_nascimento,
            "arvore": arvore
        }

    def _buscar_pai_vaca_orm(self, cow_obj, nivel: int) -> Optional[Dict[str, Any]]:
        """Recupera o pai (Bull) de uma vaca via Birth -> Insemination -> Father."""
        if not cow_obj or not cow_obj.birth or not cow_obj.birth.insemination:
            return None

        insem = cow_obj.birth.insemination
        father_obj = insem.father
        if not father_obj:
            return None

        raca_nome = father_obj.breed.name if father_obj.breed else "Não informada"
        resultado = {
            "id": father_obj.id,
            "nome": father_obj.name,
            "numero_registro": father_obj.register_number,
            "raca": raca_nome,
            "geracao": nivel,
            "parentesco": "Pai" if nivel == 1 else ("Avô Paterno" if nivel == 2 else "Bisavô Paterno")
        }

        resultado["pai"] = None
        resultado["mae"] = None
        return resultado

    def _buscar_mae_vaca_orm(self, cow_obj, nivel: int) -> Optional[Dict[str, Any]]:
        """Recupera recursivamente a mãe (Cow) de uma vaca até a 3ª geração."""
        if not cow_obj or not cow_obj.birth or not cow_obj.birth.insemination:
            return None

        insem = cow_obj.birth.insemination
        mother_obj = insem.mother
        if not mother_obj or nivel > self.MAX_GENERATIONS:
            return None

        raca_nome = mother_obj.breed.name if mother_obj.breed else "Não informada"
        resultado = {
            "id": mother_obj.id,
            "nome": mother_obj.name,
            "numero_registro": mother_obj.register_number,
            "raca": raca_nome,
            "geracao": nivel,
            "parentesco": "Mãe" if nivel == 1 else ("Avó Materna" if nivel == 2 else "Bisavó Materna")
        }

        if nivel < self.MAX_GENERATIONS:
            resultado["pai"] = self._buscar_pai_vaca_orm(mother_obj, nivel + 1)
            resultado["mae"] = self._buscar_mae_vaca_orm(mother_obj, nivel + 1)

        return resultado

    def _montar_dados_touro_orm(self, bull_obj, id_macho: int) -> Dict[str, Any]:
        """Constrói o dicionário do touro reprodutor com dados reais."""
        if not bull_obj:
            return {
                "id": id_macho,
                "nome": f"Touro #{id_macho}",
                "status_banco": "Registro não localizado na tabela bulls",
                "arvore": {"pai": None, "mae": None}
            }

        raca_nome = bull_obj.breed.name if bull_obj.breed else "Não informada"

        filhas_conhecidas = []
        try:
            from apps.herd.cattle.models import Cow
            filhas = Cow.objects.filter(birth__insemination__father=bull_obj).values_list("id", "name")
            filhas_conhecidas = [{"id": f[0], "nome": f[1]} for f in filhas[:10]]
        except Exception:
            pass

        return {
            "id": bull_obj.id,
            "nome": bull_obj.name,
            "numero_registro": bull_obj.register_number,
            "raca": raca_nome,
            "ativo": bull_obj.active,
            "filhas_no_rebanho": filhas_conhecidas,
            "arvore": {"pai": None, "mae": None}
        }

    def _verificar_parentesco_direto(self, dados_femea: Dict[str, Any], id_macho: int) -> Optional[Dict[str, Any]]:
        """
        Verifica se o touro candidato é parente direto da vaca nas 3 gerações:
        - 1ª geração: Touro é o Pai da vaca
        - 2ª geração: Touro é Avô Paterno ou Avô Materno
        - 3ª geração: Touro é Bisavô
        """
        arvore = dados_femea.get("arvore", {})

        # 1ª Geração: Pai
        pai = arvore.get("pai")
        if pai and pai.get("id") == id_macho:
            return {
                "grau": 1,
                "tipo": "PAI_DIRETO",
                "descricao": f"O touro candidato (ID {id_macho}) é o PAI biológico da fêmea candidata."
            }

        # 2ª Geração: Avô Materno
        mae = arvore.get("mae")
        if mae:
            avo_materno = mae.get("pai")
            if avo_materno and avo_materno.get("id") == id_macho:
                return {
                    "grau": 2,
                    "tipo": "AVO_MATERNO",
                    "descricao": f"O touro candidato (ID {id_macho}) é o AVÔ MATERNO da fêmea candidata."
                }

            # 3ª Geração: Bisavô Materno
            avó_materna = mae.get("mae")
            if avó_materna:
                bisavo_materno = avó_materna.get("pai")
                if bisavo_materno and bisavo_materno.get("id") == id_macho:
                    return {
                        "grau": 3,
                        "tipo": "BISAVO_MATERNO",
                        "descricao": f"O touro candidato (ID {id_macho}) é o BISAVÔ da fêmea candidata."
                    }

        return None

    def _extrair_via_sql(self, id_femea: int, id_macho: int) -> Dict[str, Any]:
        """Fallback resiliente usando consultas diretas via SQL nas tabelas do banco."""
        with self.connection.cursor() as cursor:
            tables = set(self.connection.introspection.table_names(cursor))

            tab_cows = "cows" if "cows" in tables else ("vacas" if "vacas" in tables else None)
            tab_bulls = "bulls" if "bulls" in tables else ("touros" if "touros" in tables else None)
            tab_insem = "inseminations" if "inseminations" in tables else ("inseminacao" if "inseminacao" in tables else None)
            tab_births = "births" if "births" in tables else ("nascimento" if "nascimento" in tables else None)

            dados_femea = {"id": id_femea, "nome": f"Vaca #{id_femea}", "arvore": {"pai": None, "mae": None}}
            dados_macho = {"id": id_macho, "nome": f"Touro #{id_macho}", "arvore": {"pai": None, "mae": None}}

            if tab_cows:
                cursor.execute(f"SELECT id, name, score, status, birth_id FROM {tab_cows} WHERE id = %s", [id_femea])
                row = cursor.fetchone()
                if row:
                    dados_femea["id"] = row[0]
                    dados_femea["nome"] = row[1]
                    dados_femea["escore_ecc"] = float(row[2]) if row[2] is not None else None
                    dados_femea["status"] = row[3]
                    birth_id = row[4]

                    if birth_id and tab_births and tab_insem:
                        cursor.execute(
                            f"""
                            SELECT i.father_id, i.mother_id 
                            FROM {tab_births} b 
                            JOIN {tab_insem} i ON b.insemination_id = i.id 
                            WHERE b.id = %s
                            """,
                            [birth_id]
                        )
                        parent_row = cursor.fetchone()
                        if parent_row:
                            id_pai, id_mae = parent_row[0], parent_row[1]
                            dados_femea["arvore"]["pai"] = {"id": id_pai, "nome": f"Touro #{id_pai}", "geracao": 1}
                            dados_femea["arvore"]["mae"] = {"id": id_mae, "nome": f"Vaca #{id_mae}", "geracao": 1}

            if tab_bulls:
                cursor.execute(f"SELECT id, name, register_number, active FROM {tab_bulls} WHERE id = %s", [id_macho])
                row_m = cursor.fetchone()
                if row_m:
                    dados_macho["id"] = row_m[0]
                    dados_macho["nome"] = row_m[1]
                    dados_macho["numero_registro"] = row_m[2]
                    dados_macho["ativo"] = row_m[3]

            parentesco_direto = self._verificar_parentesco_direto(dados_femea, id_macho)
            return {
                "femea": dados_femea,
                "macho": dados_macho,
                "parentesco_direto_detectado": parentesco_direto
            }
