"""
Endpoint e regras de negócio para Importação e Exportação de Vacas (Bovinos) via Planilha Excel (.xlsx).

Garante que o cadastro de bovinos seja feito com colunas e campos totalmente separados no Excel,
com validação de campos obrigatórios, raça, brinco único, data de nascimento (Birth),
peso inicial (WeightHistory) e registro de movimentação inicial opcional.
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

from apps.herd.breeds.models import Breed
from apps.herd.cattle.models import Cow
from apps.herd.quadrants.models import Quadrant
from apps.movements.animal_movements.models import AnimalMovement
from apps.movements.movement_types.models import MovementType
from apps.production.weight_history.models import WeightHistory
from apps.reproduction.models import Birth, BirthOccurrence

from .excel_utils import (
    CELL_ALIGN_CENTER,
    CELL_ALIGN_LEFT,
    CELL_ALIGN_RIGHT,
    HEADER_FILL_PRIMARY,
    carregar_planilha_xlsx,
    criar_workbook_formatado,
    mapear_colunas,
    normalizar_cabecalho,
    parse_booleano,
    parse_data,
    parse_decimal,
    parse_inteiro,
)


CAMPOS_VACA = {
    'numero_do_brinco': {
        'titulo': 'Número do Brinco *',
        'aliases': [
            'numero_do_brinco', 'numero_brinco', 'brinco', 'registro',
            'numero_registro', 'register_number', 'tag', 'ear_tag'
        ],
        'obrigatorio': True,
        'largura': 20,
        'alinhamento': CELL_ALIGN_CENTER,
        'formato': 'inteiro',
        'exemplo': 2001,
        'descricao': 'Número de registro do brinco (único, número inteiro positivo).'
    },
    'nome': {
        'titulo': 'Nome do Bovino *',
        'aliases': [
            'nome', 'nome_do_bovino', 'nome_bovino', 'nome_animal',
            'identificacao', 'name', 'animal_name'
        ],
        'obrigatorio': True,
        'largura': 26,
        'alinhamento': CELL_ALIGN_LEFT,
        'formato': 'texto',
        'exemplo': 'Mimosa',
        'descricao': 'Nome de identificação do animal (obrigatório, até 100 caracteres).'
    },
    'raca': {
        'titulo': 'Raça *',
        'aliases': [
            'raca', 'nome_raca', 'id_raca', 'breed', 'breed_name'
        ],
        'obrigatorio': True,
        'largura': 22,
        'alinhamento': CELL_ALIGN_LEFT,
        'formato': 'texto',
        'exemplo': 'Holandesa',
        'descricao': 'Nome ou ID da raça (ex: Holandesa, Girolando, Jersey, Guzerá).'
    },
    'data_nascimento': {
        'titulo': 'Data de Nascimento',
        'aliases': [
            'data_nascimento', 'data_de_nascimento', 'nascimento', 'birth_date',
            'data_nasc', 'dt_nascimento'
        ],
        'obrigatorio': False,
        'largura': 20,
        'alinhamento': CELL_ALIGN_CENTER,
        'formato': 'data',
        'exemplo': '15/03/2023',
        'descricao': 'Data de nascimento do animal (formato DD/MM/AAAA ou AAAA-MM-DD). Cria o registro de nascimento (Birth).'
    },
    'peso': {
        'titulo': 'Peso do Bovino (kg)',
        'aliases': [
            'peso', 'peso_kg', 'peso_atual', 'peso_corporal', 'peso_inicial',
            'peso_do_bovino_kg', 'weight', 'last_weight'
        ],
        'obrigatorio': False,
        'largura': 18,
        'alinhamento': CELL_ALIGN_RIGHT,
        'formato': 'decimal',
        'exemplo': 480.50,
        'descricao': 'Peso corporal do bovino em kg (número decimal). Cria o registro de pesagem (WeightHistory).'
    },
    'situacao': {
        'titulo': 'Situação',
        'aliases': [
            'situacao', 'status', 'estado', 'condicao'
        ],
        'obrigatorio': False,
        'largura': 18,
        'alinhamento': CELL_ALIGN_CENTER,
        'formato': 'texto',
        'exemplo': 'Ativo',
        'descricao': 'Situação do animal: Ativo, Inativo, Vendido ou Morto (padrão: Ativo).'
    },
    'escore': {
        'titulo': 'Escore (ECC)',
        'aliases': [
            'escore', 'score', 'ecc', 'escore_corporal', 'condicao_corporal'
        ],
        'obrigatorio': False,
        'largura': 18,
        'alinhamento': CELL_ALIGN_RIGHT,
        'formato': 'decimal',
        'exemplo': 3.50,
        'descricao': 'Escore de Condição Corporal ECC (opcional, número decimal, padrão: 0.0).'
    },
    'status_reprodutivo': {
        'titulo': 'Apta Reprodução',
        'aliases': [
            'status_reprodutivo', 'reprodutivo', 'apta_reproducao',
            'reproducao', 'reproductive_status', 'apta'
        ],
        'obrigatorio': False,
        'largura': 18,
        'alinhamento': CELL_ALIGN_CENTER,
        'formato': 'texto',
        'exemplo': 'Sim',
        'descricao': 'Status reprodutivo: Sim ou Não (padrão: Sim).'
    },
    'estabulo': {
        'titulo': 'Estábulo Inicial',
        'aliases': [
            'estabulo', 'quadrante', 'lote', 'piquete',
            'quadrant', 'localizacao', 'estabulo_inicial'
        ],
        'obrigatorio': False,
        'largura': 26,
        'alinhamento': CELL_ALIGN_LEFT,
        'formato': 'texto',
        'exemplo': 'Estábulo A - Lactação',
        'descricao': 'Nome ou ID do estábulo para lotação inicial do animal (opcional).'
    },
    'data_entrada': {
        'titulo': 'Data de Entrada',
        'aliases': [
            'data_entrada', 'data_movimentacao', 'data_lotacao',
            'movement_date', 'data'
        ],
        'obrigatorio': False,
        'largura': 18,
        'alinhamento': CELL_ALIGN_CENTER,
        'formato': 'data',
        'exemplo': datetime.date.today().strftime('%d/%m/%Y'),
        'descricao': 'Data de entrada no estábulo (opcional, padrão: data atual).'
    },
    'motivo_movimentacao': {
        'titulo': 'Motivo da Lotação',
        'aliases': [
            'motivo_movimentacao', 'motivo', 'movement_reason'
        ],
        'obrigatorio': False,
        'largura': 26,
        'alinhamento': CELL_ALIGN_LEFT,
        'formato': 'texto',
        'exemplo': 'Lotação inicial',
        'descricao': 'Motivo da entrada/movimentação (opcional, padrão: "Lotação inicial").'
    },
}

MAPA_STATUS = {
    'ativo': 'active',
    'active': 'active',
    'inativo': 'inactive',
    'inactive': 'inactive',
    'vendido': 'sold',
    'sold': 'sold',
    'morto': 'deceased',
    'falecido': 'deceased',
    'deceased': 'deceased'
}


class ImportacaoVacasView(APIView):
    """
    Endpoint para importação e exportação do cadastro de vacas (bovinos) em planilha XLSX.
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        if request.query_params.get('formato') == 'json':
            racas_disponiveis = list(Breed.objects.values('id', 'name'))
            estabulos_disponiveis = list(Quadrant.objects.values('id', 'name'))
            return Response({
                'modulo': 'Importação de Cadastro de Vacas',
                'formato_arquivo': 'xlsx',
                'descricao': 'Importação de bovinos com colunas estruturadas em Excel.',
                'racas_cadastradas': racas_disponiveis,
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
                    for chave, meta in CAMPOS_VACA.items()
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
        indice_para_campo, campos_faltantes = mapear_colunas(cabecalhos, CAMPOS_VACA)
        if campos_faltantes:
            nomes_faltantes = [CAMPOS_VACA[c]['titulo'] for c in campos_faltantes]
            return Response(
                {
                    'erro': 'A planilha não contém todas as colunas obrigatórias.',
                    'colunas_faltantes': nomes_faltantes,
                    'colunas_encontradas': [c for c in cabecalhos if c],
                    'colunas_esperadas': [meta['titulo'] for meta in CAMPOS_VACA.values() if meta['obrigatorio']]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        brincos_existentes = set(Cow.objects.values_list('register_number', flat=True))
        brincos_na_planilha = {}

        racas = list(Breed.objects.all())
        racas_por_nome = {normalizar_cabecalho(r.name): r for r in racas}
        racas_por_id = {r.id: r for r in racas}

        estabulos = list(Quadrant.objects.all())
        estabulos_por_nome = {normalizar_cabecalho(e.name): e for e in estabulos}
        estabulos_por_id = {e.id: e for e in estabulos}

        tipo_mov_entrada = MovementType.objects.filter(name__icontains='Entrada').first() or MovementType.objects.first()
        parto_ocorrencia = BirthOccurrence.objects.filter(description__icontains='normal').first() or BirthOccurrence.objects.first()

        vacas_para_criar = []
        relatorio_sucessos = []
        relatorio_erros = []

        hoje = timezone.localdate()

        for num_linha, linha in linhas_dados:
            dados_linha = {}
            for idx, chave in indice_para_campo.items():
                dados_linha[chave] = linha[idx] if idx < len(linha) else None

            erros_da_linha = []

            # 1. Validação do Número do Brinco
            brinco_bruto = dados_linha.get('numero_do_brinco')
            brinco_num = None
            if brinco_bruto is None or str(brinco_bruto).strip() == "":
                erros_da_linha.append("Número do brinco é obrigatório.")
            else:
                try:
                    brinco_num = parse_inteiro(brinco_bruto, positivo=True)
                    if brinco_num in brincos_existentes:
                        erros_da_linha.append(f"O brinco {brinco_num} já está cadastrado no sistema.")
                    elif brinco_num in brincos_na_planilha:
                        erros_da_linha.append(
                            f"Brinco {brinco_num} repetido nesta planilha (linha anterior: {brincos_na_planilha[brinco_num]})."
                        )
                    else:
                        brincos_na_planilha[brinco_num] = num_linha
                except ValueError as e:
                    erros_da_linha.append(str(e))

            # 2. Validação do Nome do Animal
            nome_bruto = dados_linha.get('nome')
            nome = None
            if nome_bruto is None or str(nome_bruto).strip() == "":
                erros_da_linha.append("Nome do bovino é obrigatório.")
            else:
                nome = str(nome_bruto).strip()
                if len(nome) > 100:
                    erros_da_linha.append("Nome do bovino excede o limite máximo de 100 caracteres.")

            # 3. Validação da Raça
            raca_bruta = dados_linha.get('raca')
            raca_obj = None
            if raca_bruta is None or str(raca_bruta).strip() == "":
                erros_da_linha.append("Raça é obrigatória.")
            else:
                try:
                    raca_id = int(float(str(raca_bruta).strip()))
                    raca_obj = racas_por_id.get(raca_id)
                except (ValueError, TypeError):
                    raca_id = None
                
                if not raca_obj:
                    raca_norm = normalizar_cabecalho(raca_bruta)
                    raca_obj = racas_por_nome.get(raca_norm)

                if not raca_obj:
                    racas_disp = ", ".join([r.name for r in racas])
                    erros_da_linha.append(
                        f"Raça '{raca_bruta}' não encontrada. Raças disponíveis: {racas_disp}."
                    )

            # 4. Data de Nascimento (Opcional)
            data_nasc_bruta = dados_linha.get('data_nascimento')
            data_nasc = None
            if data_nasc_bruta not in (None, ""):
                try:
                    data_nasc = parse_data(data_nasc_bruta)
                    if data_nasc > hoje:
                        erros_da_linha.append(f"Data de nascimento ({data_nasc.strftime('%d/%m/%Y')}) não pode ser futura.")
                except ValueError as e:
                    erros_da_linha.append(f"Data de nascimento: {str(e)}")

            # 5. Peso Corporal (Opcional)
            peso_bruto = dados_linha.get('peso')
            peso = None
            if peso_bruto not in (None, ""):
                try:
                    peso = parse_decimal(peso_bruto, positivo=True)
                    if peso <= 0:
                        erros_da_linha.append("O peso deve ser maior que zero.")
                except ValueError as e:
                    erros_da_linha.append(f"Peso: {str(e)}")

            # 6. Situação / Status (Opcional, default: active)
            situacao_bruta = dados_linha.get('situacao')
            if situacao_bruta in (None, ""):
                status_vaca = 'active'
            else:
                sit_norm = str(situacao_bruta).strip().lower()
                status_vaca = MAPA_STATUS.get(sit_norm, 'active')

            # 7. Escore ECC (Opcional, default: 0.0)
            escore_bruto = dados_linha.get('escore')
            if escore_bruto in (None, ""):
                escore = Decimal('0.00')
            else:
                try:
                    escore = parse_decimal(escore_bruto, positivo=True)
                except ValueError as e:
                    erros_da_linha.append(f"Escore: {str(e)}")
                    escore = Decimal('0.00')

            # 8. Status Reprodutivo (Opcional, default: True)
            reprodutivo_bruto = dados_linha.get('status_reprodutivo')
            status_reprodutivo = parse_booleano(reprodutivo_bruto, default=True)

            # 9. Estábulo Inicial (Opcional)
            estabulo_bruto = dados_linha.get('estabulo')
            estabulo_obj = None
            if estabulo_bruto not in (None, ""):
                try:
                    est_id = int(float(str(estabulo_bruto).strip()))
                    estabulo_obj = estabulos_por_id.get(est_id)
                except (ValueError, TypeError):
                    est_id = None
                
                if not estabulo_obj:
                    est_norm = normalizar_cabecalho(estabulo_bruto)
                    estabulo_obj = estabulos_por_nome.get(est_norm)
                
                if not estabulo_obj:
                    estabulos_disp = ", ".join([e.name for e in estabulos])
                    erros_da_linha.append(
                        f"Estábulo '{estabulo_bruto}' não encontrado. Estabulos disponíveis: {estabulos_disp}."
                    )

            # 10. Data de Entrada / Movimentação
            data_entrada_bruta = dados_linha.get('data_entrada')
            if data_entrada_bruta in (None, ""):
                data_mov = hoje
            else:
                try:
                    data_mov = parse_data(data_entrada_bruta)
                except ValueError as e:
                    erros_da_linha.append(f"Data de entrada: {str(e)}")
                    data_mov = hoje

            motivo_mov = str(dados_linha.get('motivo_movimentacao') or "Lotação inicial via importação XLSX").strip()

            if erros_da_linha:
                relatorio_erros.append({
                    'linha': num_linha,
                    'brinco': brinco_num if brinco_num is not None else str(brinco_bruto),
                    'nome': nome or str(nome_bruto),
                    'erros': erros_da_linha
                })
            else:
                vaca_obj = Cow(
                    name=nome,
                    breed=raca_obj,
                    register_number=brinco_num,
                    status=status_vaca,
                    score=escore,
                    reproductive_status=status_reprodutivo
                )
                vacas_para_criar.append((vaca_obj, data_nasc, peso, estabulo_obj, data_mov, motivo_mov))
                relatorio_sucessos.append({
                    'linha': num_linha,
                    'brinco': brinco_num,
                    'nome': nome,
                    'raca': raca_obj.name,
                    'nascimento': data_nasc.strftime('%d/%m/%Y') if data_nasc else None,
                    'peso': float(peso) if peso else None,
                    'status': status_vaca,
                    'escore': float(escore),
                    'reprodutivo': status_reprodutivo,
                    'estabulo': estabulo_obj.name if estabulo_obj else 'Sem estábulo inicial'
                })

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

        total_salvos = 0
        if not dry_run and vacas_para_criar:
            with transaction.atomic():
                for vaca_obj, data_nasc, peso, estabulo_obj, data_mov, motivo_mov in vacas_para_criar:
                    # 1. Se informada data de nascimento, cria o registro de nascimento (Birth)
                    if data_nasc:
                        peso_nasc = peso if (peso and peso < Decimal('100.00')) else Decimal('35.00')
                        birth_obj = Birth.objects.create(
                            date=data_nasc,
                            weight=peso_nasc,
                            occurrence=parto_ocorrencia
                        )
                        vaca_obj.birth = birth_obj

                    vaca_obj.save()
                    total_salvos += 1

                    # 2. Se informado peso, cria o histórico de pesagem inicial (WeightHistory)
                    if peso:
                        WeightHistory.objects.create(
                            animal=vaca_obj,
                            weight=peso,
                            weighing_date=data_mov or data_nasc or hoje
                        )

                    # 3. Se informado estábulo inicial, registra a lotação (AnimalMovement)
                    if estabulo_obj and tipo_mov_entrada:
                        AnimalMovement.objects.create(
                            animal=vaca_obj,
                            quadrant=estabulo_obj,
                            movement_type=tipo_mov_entrada,
                            movement_date=data_mov,
                            movement_reason=motivo_mov
                        )
        elif dry_run:
            total_salvos = len(vacas_para_criar)

        msg = (
            f"[Simulação] {total_salvos} bovino(s) validado(s) com sucesso."
            if dry_run else
            f"{total_salvos} bovino(s) cadastrado(s) com sucesso via importação."
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
        """Gera a planilha modelo oficial (.xlsx) formatada para cadastro de bovinos."""
        colunas = [
            {
                'titulo': CAMPOS_VACA['numero_do_brinco']['titulo'],
                'largura': 22,
                'alinhamento': CELL_ALIGN_CENTER,
                'formato': 'inteiro'
            },
            {
                'titulo': CAMPOS_VACA['nome']['titulo'],
                'largura': 26,
                'alinhamento': CELL_ALIGN_LEFT
            },
            {
                'titulo': CAMPOS_VACA['raca']['titulo'],
                'largura': 22,
                'alinhamento': CELL_ALIGN_LEFT
            },
            {
                'titulo': CAMPOS_VACA['data_nascimento']['titulo'],
                'largura': 22,
                'alinhamento': CELL_ALIGN_CENTER,
                'formato': 'data'
            },
            {
                'titulo': CAMPOS_VACA['peso']['titulo'],
                'largura': 18,
                'alinhamento': CELL_ALIGN_RIGHT,
                'formato': 'decimal'
            },
            {
                'titulo': CAMPOS_VACA['situacao']['titulo'],
                'largura': 18,
                'alinhamento': CELL_ALIGN_CENTER
            },
            {
                'titulo': CAMPOS_VACA['escore']['titulo'],
                'largura': 18,
                'alinhamento': CELL_ALIGN_RIGHT,
                'formato': 'decimal'
            },
            {
                'titulo': CAMPOS_VACA['status_reprodutivo']['titulo'],
                'largura': 18,
                'alinhamento': CELL_ALIGN_CENTER
            },
            {
                'titulo': CAMPOS_VACA['estabulo']['titulo'],
                'largura': 28,
                'alinhamento': CELL_ALIGN_LEFT
            },
            {
                'titulo': CAMPOS_VACA['data_entrada']['titulo'],
                'largura': 20,
                'alinhamento': CELL_ALIGN_CENTER,
                'formato': 'data'
            },
            {
                'titulo': CAMPOS_VACA['motivo_movimentacao']['titulo'],
                'largura': 26,
                'alinhamento': CELL_ALIGN_LEFT
            },
        ]

        racas = list(Breed.objects.all()[:3])
        raca_1 = racas[0].name if len(racas) > 0 else 'Girolando'
        raca_2 = racas[1].name if len(racas) > 1 else 'Guzerá'
        raca_3 = racas[2].name if len(racas) > 2 else 'Holandesa'

        estabulos = list(Quadrant.objects.all()[:2])
        est_1 = estabulos[0].name if len(estabulos) > 0 else 'Estábulo A - Lactação'
        est_2 = estabulos[1].name if len(estabulos) > 1 else 'Estábulo B - Pré-parto'

        hoje = datetime.date.today()
        nasc_1 = hoje - datetime.timedelta(days=365 * 3) # 3 anos
        nasc_2 = hoje - datetime.timedelta(days=365 * 4) # 4 anos
        nasc_3 = hoje - datetime.timedelta(days=365 * 2) # 2 anos

        linhas_exemplo = [
            [3001, 'Mimosa', raca_1, nasc_1, 480.50, 'Ativo', 3.50, 'Sim', est_1, hoje, 'Lotação inicial'],
            [3002, 'Estrela', raca_2, nasc_2, 510.00, 'Ativo', 3.75, 'Sim', est_1, hoje, 'Lotação inicial'],
            [3003, 'Canela', raca_3, nasc_3, 465.00, 'Ativo', 3.25, 'Sim', est_2, hoje, 'Lotação inicial'],
        ]

        buffer = criar_workbook_formatado(
            titulo_aba="Cadastro de Vacas",
            colunas=colunas,
            dados_linhas=linhas_exemplo,
            cor_cabecalho=HEADER_FILL_PRIMARY
        )

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename="modelo_importacao_vacas.xlsx"'
        return response

    def _gerar_exportacao_xlsx(self, request):
        """Exporta registros de bovinos existentes para XLSX com colunas organizadas."""
        queryset = Cow.objects.select_related('breed', 'birth').prefetch_related('weight_history').order_by('register_number')

        ultimas_movs = {
            m.animal_id: m
            for m in AnimalMovement.objects.select_related('quadrant').order_by('animal_id', 'movement_date', 'id')
        }

        colunas = [
            {'titulo': 'ID', 'largura': 12, 'alinhamento': CELL_ALIGN_CENTER, 'formato': 'inteiro'},
            {'titulo': 'Número do Brinco', 'largura': 18, 'alinhamento': CELL_ALIGN_CENTER, 'formato': 'inteiro'},
            {'titulo': 'Nome do Bovino', 'largura': 24, 'alinhamento': CELL_ALIGN_LEFT},
            {'titulo': 'Raça', 'largura': 20, 'alinhamento': CELL_ALIGN_LEFT},
            {'titulo': 'Data de Nascimento', 'largura': 20, 'alinhamento': CELL_ALIGN_CENTER, 'formato': 'data'},
            {'titulo': 'Último Peso (kg)', 'largura': 18, 'alinhamento': CELL_ALIGN_RIGHT, 'formato': 'decimal'},
            {'titulo': 'Situação', 'largura': 16, 'alinhamento': CELL_ALIGN_CENTER},
            {'titulo': 'Escore (ECC)', 'largura': 16, 'alinhamento': CELL_ALIGN_RIGHT, 'formato': 'decimal'},
            {'titulo': 'Apta Reprodução', 'largura': 16, 'alinhamento': CELL_ALIGN_CENTER},
            {'titulo': 'Estábulo Atual', 'largura': 26, 'alinhamento': CELL_ALIGN_LEFT},
            {'titulo': 'Última Movimentação', 'largura': 20, 'alinhamento': CELL_ALIGN_CENTER, 'formato': 'data'},
        ]

        dados = []
        for cow in queryset:
            mov = ultimas_movs.get(cow.id)
            estabulo_nome = mov.quadrant.name if mov and mov.quadrant else 'Não alocado'
            data_mov = mov.movement_date if mov else None
            reprodutivo_str = 'Sim' if cow.reproductive_status else 'Não'

            # Obter último peso registrado
            pesos = list(cow.weight_history.order_by('-weighing_date', '-id'))
            ultimo_peso = float(pesos[0].weight) if pesos else (float(cow.birth.weight) if cow.birth else None)
            data_nasc = cow.birth.date if cow.birth else None

            dados.append([
                cow.id,
                cow.register_number,
                cow.name,
                cow.breed.name if cow.breed else '',
                data_nasc,
                ultimo_peso,
                cow.get_status_display() if hasattr(cow, 'get_status_display') else cow.status,
                float(cow.score),
                reprodutivo_str,
                estabulo_nome,
                data_mov
            ])

        buffer = criar_workbook_formatado(
            titulo_aba="Rebanho Bovino",
            colunas=colunas,
            dados_linhas=dados,
            cor_cabecalho=HEADER_FILL_PRIMARY
        )

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        data_hoje = datetime.date.today().strftime('%Y%m%d')
        response['Content-Disposition'] = f'attachment; filename="rebanho_vacas_{data_hoje}.xlsx"'
        return response
