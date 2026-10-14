"""
Módulo de extração de dados genealógicos para reprodução bovina.
Responsável por consultar o banco de dados real (via conexão Django)
e reconstruir as árvores genealógicas da fêmea e do macho até a 3ª geração (bisavós).
Nenhum dado fictício é criado; consome as tabelas reais do banco de dados externo.
"""

from typing import Dict, Any, Optional
from django.db import connection


class GenealogyExtractor:
    """
    Extrator dinâmico de dados genealógicos no banco de dados ativo do projeto.
    Suporta tanto esquemas relacionais dedicados (vacas, touros, inseminacao, nascimento)
    quanto modelos padrão do rebanho, inspecionando as tabelas reais sem mock.
    """

    MAX_GENERATIONS = 3  # Pais (1ª), Avós (2ª), Bisavós (3ª)

    def __init__(self, db_connection=None):
        self.connection = db_connection or connection

    def _get_existing_tables(self, cursor) -> set:
        """Obtém os nomes de todas as tabelas existentes no banco ativo."""
        try:
            return set(self.connection.introspection.table_names(cursor))
        except Exception:
            return set()

    def _get_table_columns(self, cursor, table_name: str) -> set:
        """Obtém as colunas de uma tabela específica."""
        try:
            description = self.connection.introspection.get_table_description(cursor, table_name)
            return {col.name.lower() for col in description}
        except Exception:
            return set()

    def extrair_arvore_completa(self, id_femea: int, id_macho: int) -> Dict[str, Any]:
        """
        Executa a extração completa dos dados da fêmea e do macho,
        incluindo suas árvores genealógicas até a 3ª geração.
        """
        with self.connection.cursor() as cursor:
            tables = self._get_existing_tables(cursor)

            dados_femea = self._extrair_femea(cursor, tables, id_femea)
            dados_macho = self._extrair_macho(cursor, tables, id_macho)

            return {
                "femea": dados_femea,
                "macho": dados_macho
            }

    def _extrair_femea(self, cursor, tables: set, id_femea: int) -> Dict[str, Any]:
        """Extrai os dados da matriz/fêmea e sua árvore genealógica."""
        # Cenário 1: Tabela dedicada 'vacas' do diagrama do banco externo
        if "vacas" in tables:
            cols = self._get_table_columns(cursor, "vacas")
            col_list = ["id", "nome"]
            if "escore_ecc" in cols:
                col_list.append("escore_ecc")
            if "status_reproducao" in cols:
                col_list.append("status_reproducao")
            if "data_nasci" in cols:
                col_list.append("data_nasci")
            if "id_pai" in cols:
                col_list.append("id_pai")
            if "id_mae" in cols:
                col_list.append("id_mae")

            query = f"SELECT {', '.join(col_list)} FROM vacas WHERE id = %s"
            cursor.execute(query, [id_femea])
            row = cursor.fetchone()

            if not row:
                return {
                    "id": id_femea,
                    "nome": f"Fêmea #{id_femea}",
                    "status_banco": "Registro não localizado no banco externo",
                    "arvore": {"pai": None, "mae": None}
                }

            row_dict = dict(zip(col_list, row))
            id_pai = row_dict.get("id_pai")
            id_mae = row_dict.get("id_mae")

            # Se não tem id_mae direto na tabela vacas, busca na tabela nascimento/inseminacao
            if not id_mae and "nascimento" in tables and "inseminacao" in tables:
                id_mae = self._buscar_mae_por_nascimento(cursor, tables, id_femea)

            arvore = {
                "pai": self._buscar_ancestral_macho(cursor, tables, id_pai, nivel=1) if id_pai else None,
                "mae": self._buscar_ancestral_femea(cursor, tables, id_mae, nivel=1) if id_mae else None
            }

            return {
                "id": id_femea,
                "nome": row_dict.get("nome") or f"Vaca #{id_femea}",
                "escore_ecc": row_dict.get("escore_ecc"),
                "status_reproducao": row_dict.get("status_reproducao"),
                "data_nascimento": str(row_dict.get("data_nasci")) if row_dict.get("data_nasci") else None,
                "arvore": arvore
            }

        # Cenário 2: Tabela padrão 'animals_animal' do Django
        if "animals_animal" in tables:
            cursor.execute("SELECT id, name, birth_date, sex, status FROM animals_animal WHERE id = %s", [id_femea])
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "nome": row[1],
                    "data_nascimento": str(row[2]) if row[2] else None,
                    "sexo": row[3],
                    "status": row[4],
                    "arvore": {"pai": None, "mae": None}
                }

        return {
            "id": id_femea,
            "nome": f"Fêmea #{id_femea}",
            "arvore": {"pai": None, "mae": None}
        }

    def _extrair_macho(self, cursor, tables: set, id_macho: int) -> Dict[str, Any]:
        """Extrai os dados do reprodutor/touro e sua árvore genealógica."""
        # Cenário 1: Tabela dedicada 'touros' do diagrama do banco externo
        if "touros" in tables:
            cols = self._get_table_columns(cursor, "touros")
            col_list = ["id", "nome"]
            if "id_pai" in cols:
                col_list.append("id_pai")
            if "id_mae" in cols:
                col_list.append("id_mae")

            query = f"SELECT {', '.join(col_list)} FROM touros WHERE id = %s"
            cursor.execute(query, [id_macho])
            row = cursor.fetchone()

            if not row:
                return {
                    "id": id_macho,
                    "nome": f"Macho/Touro #{id_macho}",
                    "status_banco": "Registro não localizado no banco externo",
                    "arvore": {"pai": None, "mae": None}
                }

            row_dict = dict(zip(col_list, row))
            id_pai = row_dict.get("id_pai")
            id_mae = row_dict.get("id_mae")

            arvore = {
                "pai": self._buscar_ancestral_macho(cursor, tables, id_pai, nivel=1) if id_pai else None,
                "mae": self._buscar_ancestral_femea(cursor, tables, id_mae, nivel=1) if id_mae else None
            }

            return {
                "id": id_macho,
                "nome": row_dict.get("nome") or f"Touro #{id_macho}",
                "arvore": arvore
            }

        # Cenário 2: Tabela padrão 'animals_animal' do Django
        if "animals_animal" in tables:
            cursor.execute("SELECT id, name, birth_date, sex, status FROM animals_animal WHERE id = %s", [id_macho])
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "nome": row[1],
                    "data_nascimento": str(row[2]) if row[2] else None,
                    "sexo": row[3],
                    "status": row[4],
                    "arvore": {"pai": None, "mae": None}
                }

        return {
            "id": id_macho,
            "nome": f"Macho #{id_macho}",
            "arvore": {"pai": None, "mae": None}
        }

    def _buscar_mae_por_nascimento(self, cursor, tables: set, id_vaca: int) -> Optional[int]:
        """Tenta descobrir a mãe biológica através do registro de nascimento/inseminação."""
        cols_nasc = self._get_table_columns(cursor, "nascimento")
        cols_insem = self._get_table_columns(cursor, "inseminacao")

        # Verifica se 'nascimento' possui coluna referenciando a vaca ou se foi gerada por inseminacao
        if "id_vaca" in cols_nasc and "id_inseminacao" in cols_nasc and "id_vaca_mae" in cols_insem:
            cursor.execute(
                """
                SELECT i.id_vaca_mae 
                FROM nascimento n 
                JOIN inseminacao i ON n.id_inseminacao = i.id 
                WHERE n.id_vaca = %s
                """,
                [id_vaca]
            )
            res = cursor.fetchone()
            if res:
                return res[0]
        return None

    def _buscar_ancestral_macho(self, cursor, tables: set, id_pai: int, nivel: int) -> Optional[Dict[str, Any]]:
        """Busca recursivamente ancestrais machos até a 3ª geração (bisavós)."""
        if not id_pai or nivel > self.MAX_GENERATIONS:
            return None

        nome = f"Touro #{id_pai}"
        id_proximo_pai = None
        id_proxima_mae = None

        if "touros" in tables:
            cols = self._get_table_columns(cursor, "touros")
            col_list = ["id", "nome"]
            if "id_pai" in cols:
                col_list.append("id_pai")
            if "id_mae" in cols:
                col_list.append("id_mae")

            cursor.execute(f"SELECT {', '.join(col_list)} FROM touros WHERE id = %s", [id_pai])
            row = cursor.fetchone()
            if row:
                row_dict = dict(zip(col_list, row))
                nome = row_dict.get("nome") or nome
                id_proximo_pai = row_dict.get("id_pai")
                id_proxima_mae = row_dict.get("id_mae")

        resultado = {
            "id": id_pai,
            "nome": nome,
            "geracao": nivel
        }

        if nivel < self.MAX_GENERATIONS:
            resultado["pai"] = self._buscar_ancestral_macho(cursor, tables, id_proximo_pai, nivel + 1) if id_proximo_pai else None
            resultado["mae"] = self._buscar_ancestral_femea(cursor, tables, id_proxima_mae, nivel + 1) if id_proxima_mae else None

        return resultado

    def _buscar_ancestral_femea(self, cursor, tables: set, id_mae: int, nivel: int) -> Optional[Dict[str, Any]]:
        """Busca recursivamente ancestrais fêmeas até a 3ª geração (bisavós)."""
        if not id_mae or nivel > self.MAX_GENERATIONS:
            return None

        nome = f"Vaca #{id_mae}"
        id_proximo_pai = None
        id_proxima_mae = None

        if "vacas" in tables:
            cols = self._get_table_columns(cursor, "vacas")
            col_list = ["id", "nome"]
            if "id_pai" in cols:
                col_list.append("id_pai")
            if "id_mae" in cols:
                col_list.append("id_mae")

            cursor.execute(f"SELECT {', '.join(col_list)} FROM vacas WHERE id = %s", [id_mae])
            row = cursor.fetchone()
            if row:
                row_dict = dict(zip(col_list, row))
                nome = row_dict.get("nome") or nome
                id_proximo_pai = row_dict.get("id_pai")
                id_proxima_mae = row_dict.get("id_mae")

        resultado = {
            "id": id_mae,
            "nome": nome,
            "geracao": nivel
        }

        if nivel < self.MAX_GENERATIONS:
            resultado["pai"] = self._buscar_ancestral_macho(cursor, tables, id_proximo_pai, nivel + 1) if id_proximo_pai else None
            resultado["mae"] = self._buscar_ancestral_femea(cursor, tables, id_proxima_mae, nivel + 1) if id_proxima_mae else None

        return resultado

