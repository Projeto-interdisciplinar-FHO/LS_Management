"""
Utilitários para manipulação, geração de modelos, leitura e exportação
de planilhas Excel (.xlsx) usando openpyxl.

Garante que os dados sejam lidos e gravados por colunas/células separadas,
evitando os problemas de agrupamento em uma única célula típicos do CSV.
"""

import io
import re
import datetime
from decimal import Decimal, InvalidOperation
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


# Estilos padrão para planilhas profissionais
HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
HEADER_FILL_PRIMARY = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")  # Azul escuro
HEADER_FILL_SECONDARY = PatternFill(start_color="2E7D32", end_color="2E7D32", fill_type="solid") # Verde escuro
CELL_FONT = Font(name="Calibri", size=10, color="000000")
CELL_ALIGN_LEFT = Alignment(horizontal="left", vertical="center")
CELL_ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
CELL_ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")

THIN_BORDER_SIDE = Side(border_style="thin", color="D3D3D3")
CELL_BORDER = Border(
    left=THIN_BORDER_SIDE,
    right=THIN_BORDER_SIDE,
    top=THIN_BORDER_SIDE,
    bottom=THIN_BORDER_SIDE
)


def normalizar_cabecalho(texto):
    """
    Normaliza cabeçalhos removendo acentos, pontuações, espaços extras
    e convertendo para minúsculas com underscores.
    Ex: 'Número do Brinco *' -> 'numero_do_brinco'
    """
    if not texto:
        return ""
    s = str(texto).strip().lower()
    # Remove acentos
    mapa_acentos = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }
    for orig, dest in mapa_acentos.items():
        s = s.replace(orig, dest)
    # Remove caracteres especiais (como *, :, (, ))
    s = re.sub(r'[^a-z0-9_ ]', '', s)
    # Substitui múltiplos espaços ou hífens por underscore
    s = re.sub(r'[\s\-]+', '_', s)
    return s.strip('_')


def mapear_colunas(cabecalhos_planilha, definicoes_campos):
    """
    Mapeia os índices de coluna da planilha para as chaves canônicas do sistema.
    
    cabecalhos_planilha: lista de strings lidas na linha 1 da planilha
    definicoes_campos: dict com a estrutura:
        {
            'chave_campo': {
                'titulo': 'Nome da Coluna *',
                'aliases': ['alias1', 'alias2', ...],
                'obrigatorio': True/False
            }
        }
    
    Retorna: (indice_para_campo, campos_faltantes)
    """
    indice_para_campo = {}
    campos_encontrados = set()

    for idx, cabecalho_bruto in enumerate(cabecalhos_planilha):
        if not cabecalho_bruto:
            continue
        cab_norm = normalizar_cabecalho(cabecalho_bruto)
        for chave, def_campo in definicoes_campos.items():
            aliases = set(def_campo.get('aliases', []))
            if 'titulo' in def_campo:
                aliases.add(normalizar_cabecalho(def_campo['titulo']))
            # Também aceita sem preposições (ex: data_da_ordenha -> data_ordenha)
            cab_sem_prep = re.sub(r'_(da|de|do)_', '_', cab_norm)
            if cab_norm in aliases or cab_sem_prep in aliases:
                indice_para_campo[idx] = chave
                campos_encontrados.add(chave)
                break

    campos_faltantes = [
        chave for chave, def_campo in definicoes_campos.items()
        if def_campo.get('obrigatorio') and chave not in campos_encontrados
    ]

    return indice_para_campo, campos_faltantes


def parse_data(val):
    """
    Converte múltiplos formatos de data (Excel date nativo, serial, string DD/MM/AAAA ou AAAA-MM-DD)
    para datetime.date.
    """
    if val is None or val == "":
        return None
    if isinstance(val, datetime.datetime):
        return val.date()
    if isinstance(val, datetime.date):
        return val
    if isinstance(val, (int, float)):
        # Número de série do Excel (dias desde 30/12/1899)
        try:
            return (datetime.datetime(1899, 12, 30) + datetime.timedelta(days=float(val))).date()
        except Exception:
            raise ValueError(f"Data serial do Excel inválida: {val}")
    
    s = str(val).strip()
    # Tenta formatos comuns
    formatos = ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y", "%d.%m.%Y")
    for fmt in formatos:
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Formato de data inválido ('{val}'). Use o formato DD/MM/AAAA ou AAAA-MM-DD.")


def parse_horario(val):
    """
    Converte horário (datetime.time, datetime.datetime, string HH:MM ou HH:MM:SS)
    para datetime.time.
    """
    if val is None or val == "":
        return None
    if isinstance(val, datetime.time):
        return val
    if isinstance(val, datetime.datetime):
        return val.time()
    if isinstance(val, (int, float)):
        # Fração do dia no Excel (ex: 0.25 = 06:00:00)
        segundos = int(float(val) * 86400)
        horas = (segundos // 3600) % 24
        minutos = (segundos % 3600) // 60
        segs = segundos % 60
        return datetime.time(horas, minutos, segs)
    
    s = str(val).strip()
    formatos = ("%H:%M:%S", "%H:%M", "%I:%M %p")
    for fmt in formatos:
        try:
            return datetime.datetime.strptime(s, fmt).time()
        except ValueError:
            pass
    raise ValueError(f"Formato de horário inválido ('{val}'). Use o formato HH:MM (ex: 06:30).")


def parse_decimal(val, positivo=True):
    """
    Converte valor para Decimal aceitando ponto, vírgula e sufixos como 'L' ou 'kg'.
    """
    if val is None or val == "":
        return None
    if isinstance(val, Decimal):
        d = val
    elif isinstance(val, (int, float)):
        d = Decimal(str(val))
    else:
        s = str(val).strip()
        # Remove sufixos não numéricos exceto separadores
        s = re.sub(r'[^\d,\.-]', '', s)
        s = s.replace(',', '.')
        try:
            d = Decimal(s)
        except InvalidOperation:
            raise ValueError(f"Valor numérico inválido: '{val}'")
    
    if positivo and d < 0:
        raise ValueError(f"O valor não pode ser negativo: {d}")
    return d


def parse_inteiro(val, positivo=True):
    """
    Converte valor para inteiro garantindo validação.
    """
    if val is None or val == "":
        return None
    try:
        # Se for float equivalente a int (ex: 1090.0 lido do Excel)
        i = int(float(str(val).strip()))
    except (ValueError, TypeError):
        raise ValueError(f"Valor inteiro inválido: '{val}'")
    
    if positivo and i <= 0:
        raise ValueError(f"O valor deve ser um número inteiro positivo: {i}")
    return i


def parse_booleano(val, default=True):
    """
    Converte valores para booleano aceitando 'sim', 'nao', 'true', 'false', 1, 0, etc.
    """
    if val is None or val == "":
        return default
    if isinstance(val, bool):
        return val
    s = str(val).strip().lower()
    if s in ('sim', 's', 'true', '1', 'ativo', 'apta', 'sim/apta', 'yes', 'y'):
        return True
    if s in ('nao', 'não', 'n', 'false', '0', 'inativo', 'inapta', 'no'):
        return False
    return default


def carregar_planilha_xlsx(arquivo):
    """
    Abre e lê uma planilha Excel (.xlsx / .xls) ou CSV como fallback, retornando:
    (cabecalhos, linhas_dados)
    onde linhas_dados é uma lista de tuplas contendo os valores de cada linha.
    """
    nome = getattr(arquivo, 'name', '').lower()
    if nome.endswith('.csv'):
        import csv
        conteudo = arquivo.read()
        if isinstance(conteudo, bytes):
            try:
                texto = conteudo.decode('utf-8-sig')
            except UnicodeDecodeError:
                texto = conteudo.decode('latin-1')
        else:
            texto = str(conteudo)
        
        linhas_texto = [l for l in texto.splitlines() if l.strip()]
        if not linhas_texto:
            raise ValueError("O arquivo CSV está completamente vazio.")
        
        primeira = linhas_texto[0]
        delim = ';' if primeira.count(';') > primeira.count(',') else ','
        reader = csv.reader(linhas_texto, delimiter=delim)
        rows = list(reader)
    else:
        try:
            wb = openpyxl.load_workbook(arquivo, data_only=True)
        except Exception as e:
            raise ValueError(f"Não foi possível abrir o arquivo Excel (.xlsx): {str(e)}")
        
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise ValueError("A planilha está completamente vazia.")
    
    # Primeira linha: cabeçalhos
    cabecalhos = [str(c).strip() if c is not None else "" for c in rows[0]]
    if not any(cabecalhos):
        raise ValueError("A primeira linha da planilha não contém nenhum cabeçalho válido.")
    
    linhas_dados = []
    for num_linha, linha in enumerate(rows[1:], start=2):
        # Ignora linhas totalmente vazias
        if not any(c is not None and str(c).strip() != "" for c in linha):
            continue
        linhas_dados.append((num_linha, linha))
        
    return cabecalhos, linhas_dados


def criar_workbook_formatado(titulo_aba, colunas, dados_linhas, cor_cabecalho=HEADER_FILL_PRIMARY):
    """
    Gera um workbook openpyxl com cabeçalhos estilizados, larguras automáticas
    e bordas em cada célula. Retorna io.BytesIO pronto para resposta HTTP.
    
    colunas: lista de dicts [{'titulo': 'Número do Brinco', 'largura': 20, 'alinhamento': CELL_ALIGN_CENTER}, ...]
    dados_linhas: lista de listas com os dados correspondentes
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = titulo_aba
    ws.views.sheetView[0].showGridLines = True

    # 1. Escrever Cabeçalho
    for col_idx, col_info in enumerate(colunas, start=1):
        cell = ws.cell(row=1, column=col_idx, value=col_info['titulo'])
        cell.font = HEADER_FONT
        cell.fill = cor_cabecalho
        cell.alignment = col_info.get('alinhamento', CELL_ALIGN_CENTER)
        cell.border = CELL_BORDER

    ws.row_dimensions[1].height = 26

    # 2. Escrever Linhas de Dados
    for row_idx, linha in enumerate(dados_linhas, start=2):
        ws.row_dimensions[row_idx].height = 20
        for col_idx, valor in enumerate(linha, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=valor)
            cell.font = CELL_FONT
            cell.border = CELL_BORDER
            col_info = colunas[col_idx - 1] if col_idx - 1 < len(colunas) else {}
            cell.alignment = col_info.get('alinhamento', CELL_ALIGN_LEFT)

            # Formatação numérica ou de data na célula do Excel
            if isinstance(valor, (int, float, Decimal)):
                if col_info.get('formato') == 'decimal':
                    cell.number_format = '#,##0.00'
                elif col_info.get('formato') == 'inteiro':
                    cell.number_format = '#,##0'
            elif isinstance(valor, datetime.date):
                cell.number_format = 'DD/MM/YYYY'

    # 3. Ajustar largura das colunas
    for col_idx, col_info in enumerate(colunas, start=1):
        col_letter = get_column_letter(col_idx)
        largura_sugerida = col_info.get('largura')
        if not largura_sugerida:
            max_len = len(str(col_info['titulo']))
            for row in range(2, len(dados_linhas) + 2):
                val = ws.cell(row=row, column=col_idx).value
                if val is not None:
                    max_len = max(max_len, len(str(val)))
            largura_sugerida = max(max_len + 4, 12)
        ws.column_dimensions[col_letter].width = largura_sugerida

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
