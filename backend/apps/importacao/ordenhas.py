"""
Endpoint e regras de negócio para Importação e Exportação de Ordenhas via Planilha Excel (.xlsx).

Garante colunas e campos totalmente separados no Excel, com suporte a:
1. Ordenha individual por animal (Número do Brinco).
2. Ordenha coletiva por lote/estábulo (Estábulo), com rateio da produção entre as vacas ativas do estábulo.
"""

import datetime
from decimal import Decimal
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.herd.cattle.models import Cow
from apps.herd.quadrants.models import Quadrant
from apps.movements.animal_movements.models import AnimalMovement
from apps.production.milk_production_history.models import Milking

from .excel_utils import (
    CELL_ALIGN_CENTER,
    CELL_ALIGN_LEFT,
    CELL_ALIGN_RIGHT,
    HEADER_FILL_SECONDARY,
    carregar_planilha_xlsx,
    criar_workbook_formatado,
    mapear_colunas,
    normalizar_cabecalho,
    parse_data,
    parse_decimal,
    parse_horario,
    parse_inteiro,
)


CAMPOS_ORDENHA = {
    'numero_do_brinco': {
        'titulo': 'Número do Brinco',
        'aliases': [
            'numero_do_brinco', 'numero_brinco', 'brinco', 'registro',
            'numero_registro', 'animal', 'identificacao', 'tag',
            'ear_tag', 'register_number'
        ],
        'obrigatorio': False,  # Opcional caso seja informada ordenha por estábulo
        'largura': 20,
        'alinhamento': CELL_ALIGN_CENTER,
        'formato': 'inteiro',
        'exemplo': 1001,
        'descricao': 'Número do brinco do animal (opcional se informado o Estábulo).'
    },
    'estabulo': {
        'titulo': 'Estábulo da Ordenha',
        'aliases': [
            'estabulo', 'quadrante', 'lote', 'piquete', 'quadrant',
            'localizacao', 'nome_estabulo', 'id_estabulo',
            'estabulo_da_ordenha'
        ],
        'obrigatorio': False,  # Opcional caso seja informado o brinco individual
        'largura': 26,
        'alinhamento': CELL_ALIGN_LEFT,
        'formato': 'texto',
        'exemplo': 'Estábulo A - Lactação',
        'descricao': 'Nome ou ID do estábulo. Permite registrar a ordenha por lote para todas as vacas ativas alocadas.'
    },
    'litros': {
        'titulo': 'Produção (Litros) *',
        'aliases': [
            'litros', 'litro', 'producao', 'producao_leite', 'producao_litros',
            'producao_em_litros', 'quantidade', 'volume', 'milk_production'
        ],
        'obrigatorio': True,
        'largura': 22,
        'alinhamento': CELL_ALIGN_RIGHT,
        'formato': 'decimal',
        'exemplo': 15.50,
        'descricao': 'Quantidade de leite produzida em litros (número positivo).'
    },
    'data': {
        'titulo': 'Data da Ordenha *',
        'aliases': [
            'data', 'data_ordenha', 'data_da_ordenha', 'data_producao',
            'data_da_producao', 'dia', 'date', 'production_date'
        ],
        'obrigatorio': True,
        'largura': 18,
        'alinhamento': CELL_ALIGN_CENTER,
        'formato': 'data',
        'exemplo': datetime.date.today().strftime('%d/%m/%Y'),
        'descricao': 'Data da ordenha (formato DD/MM/AAAA ou AAAA-MM-DD).'
    },
    'hora_inicio': {
        'titulo': 'Horário de Início',
        'aliases': [
            'hora_inicio', 'horario_inicio', 'horario_de_inicio', 'hora_de_inicio',
            'inicio', 'start_time', 'start'
        ],
        'obrigatorio': False,
        'largura': 18,
        'alinhamento': CELL_ALIGN_CENTER,
        'formato': 'texto',
        'exemplo': '05:30',
        'descricao': 'Horário de início da ordenha (opcional, formato HH:MM).'
    },
    'hora_fim': {
        'titulo': 'Horário de Término',
        'aliases': [
            'hora_fim', 'horario_fim', 'horario_de_termino', 'horario_de_fim',
            'fim', 'termino', 'end_time', 'end'
        ],
        'obrigatorio': False,
        'largura': 18,
        'alinhamento': CELL_ALIGN_CENTER,
        'formato': 'texto',
        'exemplo': '06:15',
        'descricao': 'Horário de término da ordenha (opcional, formato HH:MM).'
    },
    'rateio_estabulo': {
        'titulo': 'Rateio Estábulo',
        'aliases': [
            'rateio_estabulo', 'rateio', 'tipo_rateio', 'distribuicao', 'modo_estabulo'
        ],
        'obrigatorio': False,
        'largura': 20,
        'alinhamento': CELL_ALIGN_CENTER,
        'formato': 'texto',
        'exemplo': 'Total',
        'descricao': 'Para ordenha por estábulo: "Total" (divide a produção igualmente entre as vacas) ou "Por Vaca" (aplica os litros para cada vaca). Padrão: Total.'
    },
}


class ImportacaoOrdenhasView(APIView):
    """
    Endpoint para importação e exportação de ordenhas em planilha XLSX.
    Suporta tanto ordenha individual (por Brinco) quanto ordenha por lote (por Estábulo).
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        if request.query_params.get('formato') == 'json':
            estabulos_disponiveis = list(Quadrant.objects.values('id', 'name'))
            return Response({
                'modulo': 'Importação de Ordenhas',
                'formato_arquivo': 'xlsx',
                'descricao': 'Importação por colunas em Excel. Suporta ordenha por animal (Brinco) ou por lote (Estábulo).',
                'estabulos_cadastrados': estabulos_disponiveis,
                'campos': {
                    chave: {
                        'titulo_coluna': meta['titulo'],
                        'obrigatorio': meta['obrigatorio'],
                        'tipo': meta['formato'],
                        'exemplo': meta['exemplo'],
                        'descricao': meta['descricao'],
                        'aliases_aceitos': meta['aliases'],
                    }
                    for chave, meta in CAMPOS_ORDENHA.items()
                }
            })

        if request.query_params.get('exportar') == 'true':
            return self._gerar_exportacao_xlsx(request)

        return self._gerar_modelo_xlsx()

    def post(self, request):
        arquivo = request.FILES.get('file') or request.FILES.get('arquivo')
        if not arquivo:
            return Response(
                {'erro': 'Nenhum arquivo enviado. Envie o arquivo Excel no campo "file" ou "arquivo".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        nome_arquivo = arquivo.name.lower()
        if not (nome_arquivo.endswith('.xlsx') or nome_arquivo.endswith('.xls') or nome_arquivo.endswith('.csv')):
            return Response(
                {'erro': 'Formato inválido. O arquivo deve ser uma planilha Excel (.xlsx) ou CSV.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        dry_run = request.query_params.get('dry_run', '').lower() in ('true', '1') or \
                  str(request.data.get('dry_run', '')).lower() in ('true', '1')
        abortar_em_erro = request.query_params.get('abortar_se_houver_erros', '').lower() in ('true', '1') or \
                          str(request.data.get('abortar_se_houver_erros', '')).lower() in ('true', '1')

        try:
            cabecalhos, linhas_dados = carregar_planilha_xlsx(arquivo)
        except ValueError as e:
            return Response({'erro': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Mapear colunas do cabeçalho
        indice_para_campo, campos_faltantes = mapear_colunas(cabecalhos, CAMPOS_ORDENHA)

        # Validação estrutural de cabeçalho: precisa ter data, litros e pelo menos brinco OU estábulo
        campos_identificados = set(indice_para_campo.values())
        if 'litros' not in campos_identificados or 'data' not in campos_identificados:
            return Response(
                {
                    'erro': 'A planilha precisa conter as colunas "Produção (Litros)" e "Data da Ordenha".',
                    'colunas_encontradas': [c for c in cabecalhos if c],
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if 'numero_do_brinco' not in campos_identificados and 'estabulo' not in campos_identificados:
            return Response(
                {
                    'erro': 'A planilha precisa conter ao menos uma coluna de identificação: "Número do Brinco" ou "Estábulo".',
                    'colunas_encontradas': [c for c in cabecalhos if c],
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cache de vacas e estábulos
        todas_vacas = list(Cow.objects.select_related('breed').all())
        vacas_por_brinco = {vaca.register_number: vaca for vaca in todas_vacas}
        vacas_por_id = {vaca.id: vaca for vaca in todas_vacas}

        estabulos = list(Quadrant.objects.all())
        estabulos_por_nome = {normalizar_cabecalho(e.name): e for e in estabulos}
        estabulos_por_id = {e.id: e for e in estabulos}

        # Mapear vacas ativas em cada estábulo (pela movimentação mais recente)
        vacas_por_estabulo = {e.id: [] for e in estabulos}
        for cow in todas_vacas:
            if cow.status == 'active':
                ult_mov = cow.movements.order_by('-movement_date', '-id').first()
                if ult_mov and ult_mov.quadrant_id in vacas_por_estabulo:
                    vacas_por_estabulo[ult_mov.quadrant_id].append(cow)

        registros_para_salvar = []
        relatorio_sucessos = []
        relatorio_erros = []

        hoje = timezone.localdate()

        for num_linha, linha in linhas_dados:
            dados_linha = {}
            for idx, chave in indice_para_campo.items():
                dados_linha[chave] = linha[idx] if idx < len(linha) else None

            erros_da_linha = []

            brinco_bruto = dados_linha.get('numero_do_brinco')
            estabulo_bruto = dados_linha.get('estabulo')

            tem_brinco = brinco_bruto not in (None, "") and str(brinco_bruto).strip() != ""
            tem_estabulo = estabulo_bruto not in (None, "") and str(estabulo_bruto).strip() != ""

            if not tem_brinco and not tem_estabulo:
                erros_da_linha.append("Informe o Número do Brinco ou o Estábulo para a ordenha.")
                relatorio_erros.append({
                    'linha': num_linha,
                    'brinco': None,
                    'estabulo': None,
                    'erros': erros_da_linha
                })
                continue

            vaca_especifica = None
            vacas_do_lote = []
            estabulo_obj = None

            # 1. Resolver Estábulo (se informado)
            if tem_estabulo:
                try:
                    est_id = int(float(str(estabulo_bruto).strip()))
                    estabulo_obj = estabulos_por_id.get(est_id)
                except (ValueError, TypeError):
                    estabulo_obj = None
                
                if not estabulo_obj:
                    est_norm = normalizar_cabecalho(estabulo_bruto)
                    estabulo_obj = estabulos_por_nome.get(est_norm)

                if not estabulo_obj:
                    estabulos_disp = ", ".join([e.name for e in estabulos])
                    erros_da_linha.append(f"Estábulo '{estabulo_bruto}' não encontrado. Disponíveis: {estabulos_disp}.")
                else:
                    vacas_do_lote = vacas_por_estabulo.get(estabulo_obj.id, [])

            # 2. Resolver Vaca Específica (se informado brinco)
            brinco_num = None
            if tem_brinco:
                try:
                    brinco_num = parse_inteiro(brinco_bruto, positivo=True)
                    vaca_especifica = vacas_por_brinco.get(brinco_num) or vacas_por_id.get(brinco_num)
                    if not vaca_especifica:
                        erros_da_linha.append(f"Vaca com brinco/registro {brinco_num} não encontrada no rebanho.")
                except ValueError as e:
                    erros_da_linha.append(str(e))
            elif tem_estabulo and estabulo_obj:
                # Caso ordenha por estábulo sem brinco
                if not vacas_do_lote:
                    erros_da_linha.append(
                        f"O {estabulo_obj.name} não possui nenhuma vaca ativa alocada no momento para registrar ordenha."
                    )

            # 3. Validação dos Litros
            litros_bruto = dados_linha.get('litros')
            litros = None
            if litros_bruto in (None, "") or str(litros_bruto).strip() == "":
                erros_da_linha.append("A quantidade de litros é obrigatória.")
            else:
                try:
                    litros = parse_decimal(litros_bruto, positivo=True)
                    if litros <= 0:
                        erros_da_linha.append("A quantidade de litros deve ser maior que zero.")
                except ValueError as e:
                    erros_da_linha.append(str(e))

            # 4. Validação da Data
            data_bruta = dados_linha.get('data')
            data_ordenha = None
            if data_bruta in (None, "") or str(data_bruta).strip() == "":
                erros_da_linha.append("A data da ordenha é obrigatória.")
            else:
                try:
                    data_ordenha = parse_data(data_bruta)
                    if data_ordenha > hoje:
                        erros_da_linha.append(f"A data da ordenha ({data_ordenha.strftime('%d/%m/%Y')}) não pode ser futura.")
                except ValueError as e:
                    erros_da_linha.append(str(e))

            # 5. Validação de Horários
            hora_inicio_bruta = dados_linha.get('hora_inicio')
            hora_fim_bruta = dados_linha.get('hora_fim')
            dt_inicio = None
            dt_fim = None

            if hora_inicio_bruta not in (None, ""):
                try:
                    h_ini = parse_horario(hora_inicio_bruta)
                    if data_ordenha:
                        dt_inicio = timezone.make_aware(datetime.datetime.combine(data_ordenha, h_ini))
                except ValueError as e:
                    erros_da_linha.append(f"Horário de início: {str(e)}")

            if hora_fim_bruta not in (None, ""):
                try:
                    h_fim = parse_horario(hora_fim_bruta)
                    if data_ordenha:
                        dt_fim = timezone.make_aware(datetime.datetime.combine(data_ordenha, h_fim))
                except ValueError as e:
                    erros_da_linha.append(f"Horário de término: {str(e)}")

            if dt_inicio and dt_fim and dt_fim <= dt_inicio:
                erros_da_linha.append("O horário de término deve ser posterior ao horário de início.")

            # Se houve erro nesta linha
            if erros_da_linha:
                relatorio_erros.append({
                    'linha': num_linha,
                    'brinco': brinco_num if brinco_num is not None else str(brinco_bruto or ''),
                    'estabulo': estabulo_obj.name if estabulo_obj else str(estabulo_bruto or ''),
                    'erros': erros_da_linha
                })
                continue

            # Construir objetos de Milking
            if vaca_especifica:
                # Caso A: Ordenha Individual por Vaca
                milking_obj = Milking(
                    animal=vaca_especifica,
                    milk_production=litros,
                    production_date=data_ordenha,
                    start_time=dt_inicio,
                    end_time=dt_fim
                )
                registros_para_salvar.append(milking_obj)
                relatorio_sucessos.append({
                    'linha': num_linha,
                    'tipo': 'individual',
                    'brinco': vaca_especifica.register_number,
                    'nome_animal': vaca_especifica.name,
                    'estabulo': estabulo_obj.name if estabulo_obj else None,
                    'litros': float(litros),
                    'data': data_ordenha.strftime('%d/%m/%Y'),
                    'inicio': dt_inicio.strftime('%H:%M') if dt_inicio else None,
                    'fim': dt_fim.strftime('%H:%M') if dt_fim else None,
                })
            elif vacas_do_lote:
                # Caso B: Ordenha por Estábulo (Lote)
                modo_rateio = str(dados_linha.get('rateio_estabulo') or 'total').strip().lower()
                qtd_vacas = len(vacas_do_lote)

                if modo_rateio in ('por_vaca', 'individual', 'cada'):
                    litros_por_vaca = litros
                else:
                    # Rateio igualitário do total informado no lote
                    litros_por_vaca = Decimal(str(round(float(litros) / qtd_vacas, 2)))

                for cow in vacas_do_lote:
                    milking_obj = Milking(
                        animal=cow,
                        milk_production=litros_por_vaca,
                        production_date=data_ordenha,
                        start_time=dt_inicio,
                        end_time=dt_fim
                    )
                    registros_para_salvar.append(milking_obj)

                relatorio_sucessos.append({
                    'linha': num_linha,
                    'tipo': 'estabulo',
                    'estabulo': estabulo_obj.name,
                    'vacas_atendidas': qtd_vacas,
                    'litros_total': float(litros),
                    'litros_por_vaca': float(litros_por_vaca),
                    'brincos': [c.register_number for c in vacas_do_lote],
                    'data': data_ordenha.strftime('%d/%m/%Y'),
                })

        # Verifica política de abortar se houver qualquer erro
        if abortar_em_erro and relatorio_erros:
            return Response(
                {
                    'sucesso': False,
                    'mensagem': f'Importação abortada: {len(relatorio_erros)} linha(s) possuem inconsistências.',
                    'total_linhas': len(linhas_dados),
                    'importados': 0,
                    'erros': relatorio_erros
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Salva registros válidos se não for simulação (dry_run)
        total_salvos = 0
        if not dry_run and registros_para_salvar:
            with transaction.atomic():
                Milking.objects.bulk_create(registros_para_salvar)
                total_salvos = len(registros_para_salvar)
        elif dry_run:
            total_salvos = len(registros_para_salvar)

        msg = (
            f"[Simulação] {total_salvos} registro(s) de ordenha validado(s) com sucesso."
            if dry_run else
            f"{total_salvos} registro(s) de ordenha importado(s) com sucesso."
        )
        if relatorio_erros:
            msg += f" {len(relatorio_erros)} linha(s) tiveram erros e foram ignoradas."

        return Response({
            'sucesso': len(relatorio_erros) == 0,
            'dry_run': dry_run,
            'mensagem': msg,
            'total_linhas_processadas': len(linhas_dados),
            'total_importados': total_salvos,
            'total_falhas': len(relatorio_erros),
            'erros': relatorio_erros,
            'exemplos_importados': relatorio_sucessos[:10]
        }, status=status.HTTP_201_CREATED if total_salvos > 0 and not dry_run else status.HTTP_200_OK)

    def _gerar_modelo_xlsx(self):
        """Gera a planilha modelo oficial (.xlsx) formatada para ordenhas (por brinco ou estábulo)."""
        colunas = [
            {
                'titulo': CAMPOS_ORDENHA['numero_do_brinco']['titulo'],
                'largura': 20,
                'alinhamento': CELL_ALIGN_CENTER,
                'formato': 'inteiro'
            },
            {
                'titulo': CAMPOS_ORDENHA['estabulo']['titulo'],
                'largura': 26,
                'alinhamento': CELL_ALIGN_LEFT,
                'formato': 'texto'
            },
            {
                'titulo': CAMPOS_ORDENHA['litros']['titulo'],
                'largura': 22,
                'alinhamento': CELL_ALIGN_RIGHT,
                'formato': 'decimal'
            },
            {
                'titulo': CAMPOS_ORDENHA['data']['titulo'],
                'largura': 20,
                'alinhamento': CELL_ALIGN_CENTER,
                'formato': 'data'
            },
            {
                'titulo': CAMPOS_ORDENHA['hora_inicio']['titulo'],
                'largura': 18,
                'alinhamento': CELL_ALIGN_CENTER,
                'formato': 'texto'
            },
            {
                'titulo': CAMPOS_ORDENHA['hora_fim']['titulo'],
                'largura': 18,
                'alinhamento': CELL_ALIGN_CENTER,
                'formato': 'texto'
            },
            {
                'titulo': CAMPOS_ORDENHA['rateio_estabulo']['titulo'],
                'largura': 20,
                'alinhamento': CELL_ALIGN_CENTER,
                'formato': 'texto'
            },
        ]

        vacas_exemplo = list(Cow.objects.all()[:2])
        estabulos = list(Quadrant.objects.all()[:2])
        est_nome = estabulos[0].name if estabulos else 'Estábulo A - Lactação'

        hoje = datetime.date.today()
        ontem = hoje - datetime.timedelta(days=1)

        linhas_exemplo = []
        # Linha 1: Ordenha individual por brinco
        brinco_1 = vacas_exemplo[0].register_number if vacas_exemplo else 1001
        linhas_exemplo.append([brinco_1, '', 16.50, hoje, '05:30', '06:15', ''])

        # Linha 2: Ordenha coletiva por estábulo (rateio total do lote)
        linhas_exemplo.append(['', est_nome, 80.00, hoje, '06:00', '07:00', 'Total'])

        # Linha 3: Ordenha individual com estábulo informado
        if len(vacas_exemplo) > 1:
            linhas_exemplo.append([vacas_exemplo[1].register_number, est_nome, 18.25, ontem, '05:45', '06:30', ''])
        else:
            linhas_exemplo.append([1002, est_nome, 18.25, ontem, '05:45', '06:30', ''])

        buffer = criar_workbook_formatado(
            titulo_aba="Importação de Ordenhas",
            colunas=colunas,
            dados_linhas=linhas_exemplo,
            cor_cabecalho=HEADER_FILL_SECONDARY
        )

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename="modelo_importacao_ordenhas.xlsx"'
        return response

    def _gerar_exportacao_xlsx(self, request):
        """Exporta registros de ordenha existentes para XLSX com colunas organizadas."""
        queryset = Milking.objects.select_related('animal', 'animal__breed').order_by('-production_date', '-id')

        # Buscar estábulo atual de cada animal
        ultimas_movs = {
            m.animal_id: m
            for m in AnimalMovement.objects.select_related('quadrant').order_by('animal_id', 'movement_date', 'id')
        }

        colunas = [
            {'titulo': 'ID Registro', 'largura': 14, 'alinhamento': CELL_ALIGN_CENTER, 'formato': 'inteiro'},
            {'titulo': 'Número do Brinco', 'largura': 18, 'alinhamento': CELL_ALIGN_CENTER, 'formato': 'inteiro'},
            {'titulo': 'Nome da Vaca', 'largura': 24, 'alinhamento': CELL_ALIGN_LEFT},
            {'titulo': 'Raça', 'largura': 20, 'alinhamento': CELL_ALIGN_LEFT},
            {'titulo': 'Estábulo Atual', 'largura': 26, 'alinhamento': CELL_ALIGN_LEFT},
            {'titulo': 'Produção (Litros)', 'largura': 20, 'alinhamento': CELL_ALIGN_RIGHT, 'formato': 'decimal'},
            {'titulo': 'Data da Ordenha', 'largura': 18, 'alinhamento': CELL_ALIGN_CENTER, 'formato': 'data'},
            {'titulo': 'Início', 'largura': 16, 'alinhamento': CELL_ALIGN_CENTER},
            {'titulo': 'Término', 'largura': 16, 'alinhamento': CELL_ALIGN_CENTER},
        ]

        dados = []
        for m in queryset:
            mov = ultimas_movs.get(m.animal_id)
            estabulo_nome = mov.quadrant.name if mov and mov.quadrant else 'Não alocado'
            inicio_str = m.start_time.strftime('%H:%M') if m.start_time else ''
            fim_str = m.end_time.strftime('%H:%M') if m.end_time else ''
            dados.append([
                m.id,
                m.animal.register_number,
                m.animal.name,
                m.animal.breed.name if m.animal.breed else '',
                estabulo_nome,
                float(m.milk_production),
                m.production_date,
                inicio_str,
                fim_str
            ])

        buffer = criar_workbook_formatado(
            titulo_aba="Histórico de Ordenhas",
            colunas=colunas,
            dados_linhas=dados,
            cor_cabecalho=HEADER_FILL_SECONDARY
        )

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        data_hoje = datetime.date.today().strftime('%Y%m%d')
        response['Content-Disposition'] = f'attachment; filename="ordenhas_exportadas_{data_hoje}.xlsx"'
        return response
