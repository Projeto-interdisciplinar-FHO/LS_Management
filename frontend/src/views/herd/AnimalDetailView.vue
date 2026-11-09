<template>
  <AppShell>
    <div v-if="animal && !loading" class="page page--wide animal-detail">
      <nav class="animal-breadcrumb" aria-label="Caminho da página">
        <RouterLink to="/animais">Lista de Animais</RouterLink>
        <AppIcon name="chevron-right" :size="14" />
        <span>Ficha #{{ animal.register_number }}</span>
      </nav>

      <section class="animal-summary card" aria-label="Resumo do bovino">
        <div class="animal-summary__main">
          <div class="animal-summary__identity">
            <span class="animal-summary__mark"><AppIcon name="animal" :size="26" /></span>
            <div class="animal-summary__name">
              <strong class="animal-summary__register">#{{ animal.register_number }}</strong>
              <span>{{ animal.name || 'Sem nome' }}</span>
            </div>
          </div>
          <div class="animal-summary__facts">
            <div class="animal-summary__fact">
              <span>Estábulo atual</span>
              <strong>{{ rotulos.quadrant }}</strong>
            </div>
            <div class="animal-summary__fact">
              <span>Raça</span>
              <strong>{{ rotulos.breed }}</strong>
            </div>
            <div class="animal-summary__fact">
              <span>Status reprodutivo</span>
              <strong :class="animal.reproductive_status ? 'animal-summary__value--active' : ''">
                {{ animal.reproductive_status ? 'Ativo' : 'Inativo' }}
              </strong>
            </div>
          </div>
          <div class="animal-summary__actions">
            <span class="badge" :class="badgeSituacao(animal.status)">
              <span class="badge__dot"></span>
              {{ rotuloSituacao(animal.status) }}
            </span>
            <button class="btn btn--icon" :disabled="isEditing" aria-label="Editar ficha" title="Editar ficha" @click="toggleEdit">
              <AppIcon name="edit" :size="16" />
            </button>
            <button class="btn btn--icon" aria-label="Imprimir ficha" title="Imprimir ficha" @click="imprimirFicha">
              <AppIcon name="report" :size="16" />
            </button>
            <button class="btn btn--icon is-danger" :disabled="deleting" aria-label="Excluir animal" title="Excluir animal" @click="deleteAnimal">
              <AppIcon name="trash" :size="16" />
            </button>
          </div>
        </div>
      </section>

      <nav class="tabs animal-detail__tabs" aria-label="Seções da ficha">
        <button
          v-for="aba in abasVisiveis"
          :key="aba.id"
          type="button"
          class="tabs__item"
          :class="[`animal-tab--${aba.cor}`, { 'is-active': activeTab === aba.id }]"
          @click="selecionarAba(aba.id)"
        >
          <AppIcon :name="aba.icone" :size="15" />
          {{ aba.rotulo }}
        </button>
      </nav>

      <div class="conteudo">
        <!-- GERAL -->
        <div v-if="activeTab === 'geral'" class="grid grid--2 animal-detail__general">
          <section class="card">
            <header class="card__head">
              <div>
                <h2 class="card__title">Estado do bovino</h2>
                <p class="card__desc">Situação atual e informações reprodutivas registradas.</p>
              </div>
            </header>

            <div v-if="!isEditing" class="card__body">
              <div class="kv">
                <div class="kv__row">
                  <span class="kv__key">Situação</span>
                  <span class="kv__val"><span class="badge" :class="badgeSituacao(animal.status)">{{ rotuloSituacao(animal.status) }}</span></span>
                </div>
                <div class="kv__row"><span class="kv__key">Status reprodutivo</span><span class="kv__val">{{ animal.reproductive_status ? 'Ativo' : 'Inativo' }}</span></div>
                <div class="kv__row"><span class="kv__key">Escore</span><span class="kv__val mono">{{ animal.score ?? '—' }}</span></div>
                <div class="kv__row"><span class="kv__key">Última movimentação</span><span class="kv__val mono">{{ latestMovement ? formatDate(latestMovement.movement_date) : 'Sem movimentação' }}</span></div>
                <div class="kv__row"><span class="kv__key">Tipo da movimentação</span><span class="kv__val">{{ latestMovement ? nomeEm(movementTypes, latestMovement.movement_type) : '—' }}</span></div>
              </div>
            </div>

            <form v-else @submit.prevent="updateAnimalInfo">
              <div class="card__body stack">
                <p v-if="editError" class="alert alert--danger" role="alert">
                  <AppIcon name="alert" :size="16" />
                  <span>{{ editError }}</span>
                </p>
                <div class="field">
                  <label class="field__label" for="ed-nome">Nome / apelido</label>
                  <input id="ed-nome" v-model="editData.name" class="input" type="text" required>
                </div>
                <div class="grid grid--2">
                  <div class="field">
                    <label class="field__label" for="ed-escore">Escore</label>
                    <input id="ed-escore" v-model.number="editData.score" class="input" type="number" min="0" step="0.01" required>
                  </div>
                  <div class="field">
                    <label class="field__label" for="ed-situacao">Situação</label>
                    <select id="ed-situacao" v-model="editData.status" class="select">
                      <option v-for="s in SITUACOES" :key="s.valor" :value="s.valor">{{ s.rotulo }}</option>
                    </select>
                  </div>
                  <label class="field field--check">
                    <input v-model="editData.reproductive_status" type="checkbox">
                    <span class="field__label">Status reprodutivo ativo</span>
                  </label>
                </div>
              </div>
              <footer class="card__foot">
                <button type="button" class="btn" @click="toggleEdit">Cancelar</button>
                <button type="submit" class="btn btn--primary" :disabled="saving">
                  {{ saving ? 'Salvando...' : 'Salvar alterações' }}
                </button>
              </footer>
            </form>
          </section>

          <section class="card">
            <header class="card__head">
              <div>
                <h2 class="card__title">Identificação e nascimento</h2>
                <p class="card__desc">Dados disponíveis no cadastro do bovino e no registro de nascimento.</p>
              </div>
            </header>
            <div class="card__body">
              <div class="kv">
                <div class="kv__row"><span class="kv__key">Nome</span><span class="kv__val">{{ animal.name || '—' }}</span></div>
                <div class="kv__row"><span class="kv__key">Número de registro</span><span class="kv__val mono">#{{ animal.register_number }}</span></div>
                <div class="kv__row"><span class="kv__key">Raça</span><span class="kv__val">{{ rotulos.breed }}</span></div>
                <div class="kv__row"><span class="kv__key">Estábulo atual</span><span class="kv__val">{{ rotulos.quadrant }}</span></div>
                <div class="kv__row"><span class="kv__key">Data de nascimento</span><span class="kv__val mono">{{ birthData ? formatDate(birthData.date) : 'Não vinculada' }}</span></div>
                <div v-if="birthData" class="kv__row"><span class="kv__key">Peso ao nascer</span><span class="kv__val mono">{{ birthData.weight }} kg</span></div>
                <div v-if="birthData" class="kv__row"><span class="kv__key">Ocorrência do nascimento</span><span class="kv__val">{{ nomeEm(ocorrenciasNascimento, birthData.occurrence) }}</span></div>
              </div>
            </div>
          </section>
        </div>

        <!-- HISTÓRICOS EM TABELA -->
        <section v-else-if="abaAtual && abaAtual.tabela" class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">{{ abaAtual.titulo }}</h2>
              <p v-if="abaAtual.descricao" class="card__desc">{{ abaAtual.descricao }}</p>
            </div>
            <span class="badge">{{ activeTab === 'leite' ? leiteNoPeriodo.length : abaAtual.registros.length }}</span>
          </header>

          <div v-if="abaAtual.registros.length === 0" class="empty">
            <AppIcon :name="abaAtual.icone" :size="30" />
            <p class="empty__title">Sem registros</p>
            <p class="empty__desc">{{ abaAtual.vazio }}</p>
          </div>

          <div v-else-if="activeTab === 'leite'" class="milk-history">
            <div class="milk-history__filters">
              <label class="field__label" for="filtro-periodo-ordenha">Período do gráfico</label>
              <select id="filtro-periodo-ordenha" v-model="periodoOrdenha" class="select">
                <option value="7">Últimos 7 dias</option>
                <option value="30">Últimos 30 dias</option>
                <option value="60">Últimos 60 dias</option>
                <option value="todos">Todo o histórico</option>
              </select>
            </div>
            <div class="history-chart__plot milk-history__plot">
              <Line
                :key="`ordenha-${periodoOrdenha}-${leiteNoPeriodo.length}`"
                :data="milkChartData"
                :options="milkChartOptions"
                aria-label="Gráfico de produção de leite ao longo do tempo"
              />
            </div>
            <ol
              ref="milkListElement"
              class="milk-history__list"
              aria-label="Registros de ordenha"
            >
              <li
                v-for="record in registrosOrdenhaPagina"
                :key="record.id"
                class="milk-history__item"
              >
                <span class="milk-history__date">{{ formatDate(dataOrdenha(record)) }}</span>
                <strong>{{ valorOrdenha(record) }} L</strong>
              </li>
              <li v-if="!leiteNoPeriodo.length" class="milk-history__empty">
                Nenhum registro de ordenha encontrado neste período.
              </li>
            </ol>
            <nav v-if="leiteNoPeriodo.length" class="history-pagination" aria-label="Paginação do histórico de ordenha">
              <span class="history-pagination__status">
                Página {{ paginaOrdenha }} de {{ totalPaginasOrdenha }} · {{ leiteNoPeriodo.length }} registros
              </span>
              <div class="history-pagination__actions">
                <button
                  type="button"
                  class="btn btn--sm"
                  :disabled="paginaOrdenha <= 1"
                  @click="mudarPaginaOrdenha(paginaOrdenha - 1)"
                >
                  Anterior
                </button>
                <button
                  type="button"
                  class="btn btn--sm"
                  :disabled="paginaOrdenha >= totalPaginasOrdenha"
                  @click="mudarPaginaOrdenha(paginaOrdenha + 1)"
                >
                  Próxima
                </button>
              </div>
            </nav>
          </div>

          <div v-else-if="activeTab === 'peso'" class="history-chart">
            <div class="history-chart__plot">
              <Line
                :data="weightChartData"
                :options="weightChartOptions"
                aria-label="Gráfico de peso do animal ao longo do tempo"
              />
            </div>
            <ol class="history-chart__records">
              <li
                v-for="record in pesagensOrdenadas"
                :key="record.id"
                class="history-chart__record"
              >
                <span class="history-chart__date">{{ formatDate(dataPesagem(record)) }}</span>
                <strong>{{ record.weight }} kg</strong>
              </li>
            </ol>
          </div>

          <div v-else class="history-list">
            <template v-if="activeTab === 'nutricao'">
              <article
                v-for="record in feedings"
                :key="record.id || `${record.feeding_time}-${record.animal}`"
                class="history-list__item"
              >
                <span class="history-list__icon"><AppIcon name="feed" :size="17" /></span>
                <div class="history-list__content">
                  <strong>{{ record.feed_name || record.food?.name || 'Alimentação registrada' }}</strong>
                  <p>{{ formatDate(record.date_fed || record.feeding_time) }} · {{ record.quantity ? `${record.quantity} kg` : record.meal_weight ? `${record.meal_weight} kg` : 'Quantidade não informada' }}</p>
                  <p v-if="record.notes || record.description">{{ record.notes || record.description }}</p>
                </div>
              </article>
            </template>

            <template v-else-if="activeTab === 'veterinario'">
              <article
                v-for="record in healthRecords"
                :key="record.id || `${record.consultation_date}-${record.veterinarian}`"
                class="history-list__item"
              >
                <span class="history-list__icon"><AppIcon name="stethoscope" :size="17" /></span>
                <div class="history-list__content">
                  <strong>{{ record.consultation_reason || 'Atendimento veterinário' }}</strong>
                  <p>{{ formatDate(record.consultation_date) }} · Veterinário: {{ record.veterinarian || 'Não informado' }}</p>
                  <p v-if="record.consultation_solution">{{ record.consultation_solution }}</p>
                </div>
                <button class="btn btn--sm" @click="selectHealthRecord(record)">
                  {{ selectedHealthRecord === record ? 'Fechar' : 'Detalhes' }}
                </button>
              </article>
            </template>

            <template v-else-if="activeTab === 'vacinas'">
              <article
                v-for="record in vaccineHistory"
                :key="record.id"
                class="history-list__item"
              >
                <span class="history-list__icon"><AppIcon name="syringe" :size="17" /></span>
                <div class="history-list__content">
                  <strong>{{ record.vaccine_name || record.name || record.vaccine?.name || 'Vacinação registrada' }}</strong>
                  <p>{{ formatDate(record.vaccination_date || record.date || record.date_applied) }}</p>
                  <p v-if="record.next_vaccination_date">Próxima aplicação: {{ formatDate(record.next_vaccination_date) }}</p>
                  <p v-if="record.notes || record.description">{{ record.notes || record.description }}</p>
                </div>
              </article>
            </template>
          </div>

          <div v-if="activeTab === 'veterinario' && selectedHealthRecord" class="descritivo">
            <div class="row--between">
              <h3 class="card__title">Descritivo da consulta</h3>
              <div class="row">
                <button class="btn btn--sm btn--danger" @click="deleteHealthRecord(selectedHealthRecord)">Excluir</button>
                <button class="btn btn--sm" @click="selectedHealthRecord = null">Fechar</button>
              </div>
            </div>
            <div class="kv">
              <div class="kv__row"><span class="kv__key">Motivo</span><span class="kv__val">{{ selectedHealthRecord.consultation_reason || '—' }}</span></div>
              <div class="kv__row"><span class="kv__key">Tratativa</span><span class="kv__val">{{ selectedHealthRecord.consultation_solution || '—' }}</span></div>
              <div class="kv__row"><span class="kv__key">Veterinário</span><span class="kv__val">{{ selectedHealthRecord.veterinarian || '—' }}</span></div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <div v-else class="page">
      <div class="card">
        <div v-if="loading" class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Carregando a ficha do animal...
        </div>
        <!-- Se a busca falha, `animal` fica nulo: antes o spinner girava para
             sempre, sem dizer que tinha dado errado. -->
        <div v-else class="empty">
          <AppIcon name="alert" :size="30" />
          <p class="empty__title">Ficha não carregada</p>
          <p class="empty__desc">
            Não foi possível buscar este animal. Ele pode ter sido excluído,
            ou o servidor não respondeu.
          </p>
          <div class="row">
            <button class="btn" @click="loadCompleteAnimalData">Tentar de novo</button>
            <button class="btn btn--primary" @click="$router.push('/animais')">Ver lista de animais</button>
          </div>
        </div>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  CategoryScale,
  Chart as ChartJS,
  LinearScale,
  LineController,
  LineElement,
  PointElement,
  Tooltip,
} from 'chart.js';
import { Line } from 'vue-chartjs';
import api from '@/services/api';
import { confirmar } from '@/services/confirmService';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import { SITUACOES, badgeSituacao, rotuloSituacao } from '@/utils/statusUtils';
import { apiErrorMessage } from '@/utils/apiError';
import { idRelacao, nomeEstabulo, ultimaMovimentacaoPorAnimal } from '@/utils/animalMovementUtils';

ChartJS.register(CategoryScale, LinearScale, LineController, LineElement, PointElement, Tooltip);

const route = useRoute();
const router = useRouter();

const animal = ref(null);
const loading = ref(true);
const saving = ref(false);
const deleting = ref(false);
const editError = ref('');
const abasPermitidas = ['geral', 'leite', 'peso', 'nutricao', 'veterinario', 'vacinas'];
const abaInicial = typeof route.query.tab === 'string' && abasPermitidas.includes(route.query.tab)
  ? route.query.tab
  : 'geral';
const activeTab = ref(abaInicial);
const isEditing = ref(false);

watch(() => route.query.tab, (tab) => {
  if (typeof tab === 'string' && abasPermitidas.includes(tab)) activeTab.value = tab;
});

const selecionarAba = (tab) => {
  activeTab.value = tab;
  router.replace({
    query: { ...route.query, tab: tab === 'geral' ? undefined : tab },
  });
};

const showMilkTab = computed(() => Boolean(animal.value));

const milkHistory = ref([]);
const milkListElement = ref(null);
const paginaOrdenha = ref(1);
const registrosPorPaginaOrdenha = 10;
const periodoOrdenha = ref('todos');
const vaccineHistory = ref([]);
const weightHistory = ref([]);
const feedings = ref([]);
const healthRecords = ref([]);
const selectedHealthRecord = ref(null);
const birthData = ref(null);
const latestMovement = ref(null);
const ocorrenciasNascimento = ref([]);
const movementTypes = ref([]);

const editData = ref({
  name: '',
  score: 0,
  status: 'active',
  reproductive_status: true
});

const cadastros = ref({ breeds: [], quadrants: [] });

const nomeEm = (lista, valor) => {
  const id = idRelacao(valor);
  if (id === null || id === undefined || id === '') return '—';
  const achado = lista.find((item) => String(item.id) === String(id));
  return achado?.name || achado?.tipo || '—';
};

const rotulos = computed(() => ({
  breed: nomeEm(cadastros.value.breeds, animal.value?.breed),
  quadrant: latestMovement.value
    ? nomeEstabulo(cadastros.value.quadrants, latestMovement.value.quadrant)
    : 'Sem lotação',
}));

const carregarCadastros = async () => {
  const lista = (resposta) => resposta.data?.results || resposta.data || [];
  const vazio = { data: [] };
  const [br, qd, occ, mov] = await Promise.all([
    api.get('breeds/').catch(() => vazio),
    api.get('quadrants/').catch(() => vazio),
    api.get('birth_occurrences/').catch(() => vazio),
    api.get('movement_types/').catch(() => vazio),
  ]);
  cadastros.value = {
    breeds: lista(br), quadrants: lista(qd),
  };
  ocorrenciasNascimento.value = lista(occ);
  movementTypes.value = lista(mov);
};

// As abas eram seis blocos de marcação repetida, cada um com o seu cabeçalho
// e o seu estado vazio copiado. Aqui viram dados; a marcação sobrou uma vez.
const abas = computed(() => [
  { id: 'geral', rotulo: 'Visão Geral', icone: 'info', cor: 'accent' },
  {
    id: 'leite',
    rotulo: 'Ordenha',
    icone: 'milk',
    cor: 'milk',
    tabela: true,
    titulo: 'Histórico de produção de leite',
    vazio: 'Nenhuma ordenha lançada para este animal.',
    registros: milkHistory.value,
    somenteFemea: true,
  },
  {
    id: 'peso',
    rotulo: 'Pesagens',
    icone: 'scale',
    cor: 'weight',
    tabela: true,
    titulo: 'Histórico de pesagens',
    vazio: 'Nenhuma pesagem registrada para este animal.',
    registros: weightHistory.value,
  },
  {
    id: 'vacinas',
    rotulo: 'Vacinação',
    icone: 'syringe',
    cor: 'health',
    tabela: true,
    titulo: 'Histórico de vacinação',
    vazio: 'Nenhuma vacina aplicada registrada.',
    registros: vaccineHistory.value,
  },
  {
    id: 'nutricao',
    rotulo: 'Alimentação',
    icone: 'feed',
    cor: 'nutrition',
    tabela: true,
    titulo: 'Registro de alimentação',
    descricao: 'Rações e suplementos fornecidos ao animal.',
    vazio: 'Nenhum registro de alimentação encontrado.',
    registros: feedings.value,
  },
  {
    id: 'veterinario',
    rotulo: 'Veterinário',
    icone: 'stethoscope',
    cor: 'veterinary',
    tabela: true,
    titulo: 'Atendimentos veterinários',
    descricao: 'Consultas, medicamentos e tratativas aplicadas.',
    vazio: 'Nenhum atendimento veterinário encontrado.',
    registros: healthRecords.value,
  },
]);

const abasVisiveis = computed(() => abas.value.filter((aba) => !aba.somenteFemea || showMilkTab.value));
const abaAtual = computed(() => abas.value.find((aba) => aba.id === activeTab.value));

// Pesagens da mais recente para a mais antiga, para calcular a variação.
const dataOrdenha = (registro) => registro.production_date || registro.date_collected || registro.date;
const valorOrdenha = (registro) => registro.milk_production ?? registro.milk_quantity ?? registro.quantity ?? 0;
const dataPesagem = (registro) => registro.weighing_date || registro.date || registro.date_weighed;
const pesoNumerico = (registro) => parseFloat(registro?.weight) || 0;

const pesagensOrdenadas = computed(() =>
  [...weightHistory.value].sort((a, b) => new Date(dataPesagem(b) || 0) - new Date(dataPesagem(a) || 0))
);

const leiteOrdenado = computed(() =>
  [...milkHistory.value].sort((a, b) => new Date(dataOrdenha(a) || 0) - new Date(dataOrdenha(b) || 0))
);

function hojeLocalIso() {
  const hoje = new Date();
  return new Date(hoje.getTime() - hoje.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

const leiteNoPeriodo = computed(() => {
  if (periodoOrdenha.value === 'todos') return leiteOrdenado.value;

  const dias = Number(periodoOrdenha.value);
  const limite = new Date(`${hojeLocalIso()}T00:00:00`);
  limite.setDate(limite.getDate() - (dias - 1));
  const limiteIso = [
    limite.getFullYear(),
    String(limite.getMonth() + 1).padStart(2, '0'),
    String(limite.getDate()).padStart(2, '0'),
  ].join('-');

  return leiteOrdenado.value.filter((registro) => {
    const data = String(dataOrdenha(registro) || '').slice(0, 10);
    return data >= limiteIso && data <= hojeLocalIso();
  });
});

const leiteMaisRecentePrimeiro = computed(() => [...leiteNoPeriodo.value].reverse());
const totalPaginasOrdenha = computed(() =>
  Math.max(1, Math.ceil(leiteMaisRecentePrimeiro.value.length / registrosPorPaginaOrdenha))
);
const registrosOrdenhaPagina = computed(() => {
  const inicio = (paginaOrdenha.value - 1) * registrosPorPaginaOrdenha;
  return leiteMaisRecentePrimeiro.value.slice(inicio, inicio + registrosPorPaginaOrdenha);
});

watch(milkHistory, () => {
  paginaOrdenha.value = 1;
});

watch(periodoOrdenha, () => {
  paginaOrdenha.value = 1;
});

async function mudarPaginaOrdenha(pagina) {
  paginaOrdenha.value = Math.min(Math.max(1, pagina), totalPaginasOrdenha.value);
  await nextTick();
  if (milkListElement.value) milkListElement.value.scrollTop = 0;
}

const pesoCronologico = computed(() => [...pesagensOrdenadas.value].reverse());
const chartToken = (token) => getComputedStyle(document.documentElement).getPropertyValue(token).trim();
const chartAccent = () => chartToken('--accent');
const chartText = () => chartToken('--text-3');
const chartGrid = () => chartToken('--line');
const chartSurface = () => chartToken('--surface');
const chartTooltipBackground = () => chartToken('--text');
const chartTooltipText = () => chartToken('--surface');

function fundoGrafico(context) {
  const { chart } = context;
  const { ctx, chartArea } = chart;
  if (!chartArea) return chartAccent();

  const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
  gradient.addColorStop(0, chartAccent());
  gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
  return gradient;
}

const milkChartData = computed(() => ({
  labels: leiteNoPeriodo.value.map((record) => formatDate(dataOrdenha(record))),
  datasets: [{
    label: 'Produção de leite (L)',
    data: leiteNoPeriodo.value.map((record) => Number(valorOrdenha(record))),
    borderColor: chartAccent(),
    backgroundColor: fundoGrafico,
    pointBackgroundColor: chartAccent(),
    pointBorderColor: chartSurface(),
    pointBorderWidth: 2,
    pointRadius: leiteNoPeriodo.value.length > 60 ? 2 : 4,
    pointHoverRadius: 7,
    borderWidth: 3,
    fill: true,
    tension: 0.35,
  }],
}));

const weightChartData = computed(() => ({
  labels: pesoCronologico.value.map((record) => formatDate(dataPesagem(record))),
  datasets: [{
    label: 'Peso (kg)',
    data: pesoCronologico.value.map((record) => Number(record.weight)),
    borderColor: chartAccent(),
    backgroundColor: chartAccent(),
    pointBackgroundColor: chartAccent(),
    pointBorderColor: chartAccent(),
    pointRadius: 4,
    pointHoverRadius: 6,
    borderWidth: 2,
    tension: 0.3,
  }],
}));

const criarOpcoesGrafico = (unidade, iniciarEmZero) => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { intersect: false, mode: 'nearest' },
  animation: { duration: 450, easing: 'easeOutQuart' },
  plugins: {
    legend: { display: false },
    tooltip: {
      displayColors: false,
      backgroundColor: chartTooltipBackground(),
      titleColor: chartTooltipText(),
      bodyColor: chartTooltipText(),
      padding: 12,
      cornerRadius: 10,
      callbacks: {
        label: (context) => `${context.parsed.y} ${unidade}`,
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      border: { display: false },
      ticks: { color: chartText(), maxRotation: 0, autoSkip: true, maxTicksLimit: 10 },
    },
    y: {
      beginAtZero: iniciarEmZero,
      border: { display: false, dash: [4, 4] },
      grid: { color: chartGrid(), drawTicks: false },
      ticks: { color: chartText() },
    },
  },
});

const milkChartOptions = criarOpcoesGrafico('L', true);
const weightChartOptions = criarOpcoesGrafico('kg', false);

const variacao = (indice) => {
  const anterior = pesagensOrdenadas.value[indice + 1];
  if (!anterior) return '—';
  const delta = pesoNumerico(pesagensOrdenadas.value[indice]) - pesoNumerico(anterior);
  if (!delta) return '0,0 kg';
  return `${delta > 0 ? '+' : '−'}${Math.abs(delta).toFixed(1)} kg`;
};

const classeVariacao = (indice) => {
  const anterior = pesagensOrdenadas.value[indice + 1];
  if (!anterior) return 'text-subtle';
  const delta = pesoNumerico(pesagensOrdenadas.value[indice]) - pesoNumerico(anterior);
  if (delta > 0) return 'variacao--ganho';
  if (delta < 0) return 'variacao--perda';
  return 'text-subtle';
};

onMounted(async () => {
  carregarCadastros();
  await loadCompleteAnimalData();
});

const loadCompleteAnimalData = async () => {
  loading.value = true;
  const id = route.params.id;
  try {
    const response = await api.get(`animals/${id}/`);
    animal.value = response.data;
    editData.value = {
      name: response.data.name || '',
      score: Number(response.data.score || 0),
      status: response.data.status || 'active',
      reproductive_status: Boolean(response.data.reproductive_status),
    };

    const [movementResult, birthResult] = await Promise.allSettled([
      api.get(`animal_movements/?animal_id=${id}`),
      response.data.birth ? api.get(`births/${idRelacao(response.data.birth)}/`) : Promise.resolve({ data: null }),
    ]);
    if (movementResult.status === 'fulfilled') {
      const movements = movementResult.value.data?.results || movementResult.value.data || [];
      latestMovement.value = ultimaMovimentacaoPorAnimal(movements).get(String(id)) || null;
    } else {
      throw movementResult.reason;
    }
    if (birthResult.status === 'fulfilled') {
      birthData.value = birthResult.value.data;
    } else {
      console.error('Erro ao carregar nascimento vinculado ao bovino:', birthResult.reason);
      birthData.value = null;
    }

    try {
      const milkRes = await api.getMilkProductionByAnimal(id);
      const data = milkRes.data.historico || milkRes.data.results || milkRes.data;
      milkHistory.value = Array.isArray(data)
        ? data.filter((record) => String(idRelacao(record.animal ?? record.animal_id)) === String(id))
        : [];
    } catch (e) { milkHistory.value = []; }

    try {
      const weightRes = await api.getWeightHistoryByAnimal(id);
      const data = weightRes.data.historico || weightRes.data.results || weightRes.data;
      weightHistory.value = Array.isArray(data)
        ? data.filter((record) => String(idRelacao(record.animal ?? record.animal_id)) === String(id))
        : [];
    } catch (e) { weightHistory.value = []; }

    try {
      const feedingRes = await api.getFeedingsByAnimal(id);
      const data = feedingRes.data.results || feedingRes.data;
      feedings.value = Array.isArray(data) ? data : [];
    } catch (e) { feedings.value = []; }

    try {
      const vaccineRes = await api.getVaccinationsByAnimal(id);
      const data = vaccineRes.data.results || vaccineRes.data;
      vaccineHistory.value = Array.isArray(data) ? data : [];
    } catch (e) { vaccineHistory.value = []; }

    try {
      const healthRes = await api.getVeterinaryRecords(id);
      const data = healthRes.data.results || healthRes.data;
      healthRecords.value = Array.isArray(data) ? data : [];
    } catch (e) { healthRecords.value = []; }

  } catch (error) {
    console.error("Erro ao carregar dados:", error);
  } finally {
    loading.value = false;
  }
};

const selectHealthRecord = (record) => {
  selectedHealthRecord.value = selectedHealthRecord.value === record ? null : record;
};

const deleteHealthRecord = async (record) => {
  if (!record?.id) return;
  const ok = await confirmar({
    titulo: 'Excluir este atendimento?',
    texto: 'O registro sai da ficha do animal e do histórico veterinário.',
    acao: 'Excluir',
  });
  if (!ok) return;
  try {
    await api.deleteVeterinaryRecord(record.id);
    healthRecords.value = healthRecords.value.filter(item => item.id !== record.id);
    selectedHealthRecord.value = null;
  } catch (error) {
  }
};

const toggleEdit = () => {
  isEditing.value = !isEditing.value;
  editError.value = '';
  if (!isEditing.value && animal.value) {
    editData.value = { ...animal.value };
  }
};

function imprimirFicha() {
  window.print();
}

const updateAnimalInfo = async () => {
  saving.value = true;
  editError.value = '';
  try {
    const dados = {
      name: editData.value.name,
      score: Number(editData.value.score),
      status: editData.value.status,
      reproductive_status: Boolean(editData.value.reproductive_status),
    };
    await api.patch(`animals/${animal.value.id}/`, dados);
    animal.value = { ...animal.value, ...dados };
    isEditing.value = false;
  } catch (error) {
    editError.value = apiErrorMessage(error, 'Não foi possível atualizar os dados do animal. Confira os campos e tente novamente.');
  } finally {
    saving.value = false;
  }
};

const deleteAnimal = async () => {
  if (deleting.value) return;
  const ok = await confirmar({
    titulo: `Excluir ${animal.value?.name || 'este animal'}?`,
    texto: 'A ficha e todo o histórico de pesagem, ordenha e vacinação são removidos.',
    acao: 'Excluir registro',
  });
  if (ok) {
    deleting.value = true;
    try {
      await api.deleteAnimal(animal.value.id);
      router.push('/animais');
    } catch (error) {
      // "Erro ao excluir registro" nao dizia nada. O backend devolve o motivo
      // no corpo da resposta; mostrar isso e a diferenca entre a pessoa
      // entender o que houve e abrir um chamado.
    } finally {
      deleting.value = false;
    }
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
};

/** Extrai o motivo que o backend mandou; cai no padrão quando não há um. */
function motivoDoErro(erro, padrao) {
  const status = erro?.response?.status;
  if (status >= 500) {
    return 'O servidor falhou ao excluir este animal. Avise o suporte técnico.';
  }
  const dados = erro?.response?.data;
  if (!dados) return padrao;
  if (typeof dados === 'string') return dados;
  if (dados.detail) return dados.detail;
  const campos = Object.entries(dados)
    .map(([campo, msgs]) => `${campo}: ${[].concat(msgs).join(' ')}`)
    .join(' · ');
  return campos || padrao;
}
</script>

<style scoped>
.conteudo { margin-top: 20px; }

.animal-detail__actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-wrap: wrap;
  gap: 8px;
}

.animal-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 18px 22px;
}

.animal-summary__identity {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 180px;
}

.animal-summary__mark {
  display: grid;
  width: 48px;
  height: 48px;
  place-items: center;
  flex: none;
  border-radius: 14px;
  background: var(--surface-2);
  color: var(--accent);
}

.animal-summary__eyebrow,
.animal-summary__fact span {
  display: block;
  color: var(--text-3);
  font-size: var(--fs-xs);
}

.animal-summary__register {
  display: block;
  margin-top: 3px;
  color: var(--text);
  font-size: var(--fs-lg);
}

.animal-summary__facts {
  display: grid;
  grid-template-columns: repeat(4, minmax(100px, 1fr));
  flex: 1;
  gap: 16px;
}

.animal-summary__fact {
  min-width: 0;
  padding-left: 16px;
  border-left: 1px solid var(--line);
}

.animal-summary__fact strong {
  display: block;
  overflow: hidden;
  margin-top: 5px;
  color: var(--text);
  font-size: var(--fs-sm);
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.animal-detail__tabs { margin-top: 18px; }
.animal-detail__general { align-items: start; }
.animal-detail__general > .card { min-width: 0; }
.animal-detail__edit-actions { justify-content: flex-end; }

.history-chart { padding: 18px 20px 20px; }

.history-chart__plot {
  position: relative;
  min-height: 280px;
}

.history-chart__records {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 8px;
  padding: 16px 0 0;
  margin: 16px 0 0;
  border-top: 1px solid var(--line);
  list-style: none;
}

.milk-history {
  padding: 4px 20px 18px;
}

.milk-history__filters {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  margin-bottom: 12px;
}

.milk-history__filters .field__label {
  margin: 0;
  white-space: nowrap;
}

.milk-history__filters .select {
  width: min(220px, 100%);
}

.milk-history__plot {
  height: 320px;
  min-height: 0;
  padding: 16px 18px 12px;
  border: 1px solid color-mix(in srgb, var(--accent) 18%, var(--line));
  border-radius: var(--r-md);
  background: linear-gradient(
    160deg,
    color-mix(in srgb, var(--accent) 10%, var(--surface)),
    var(--surface) 72%
  );
}

.milk-history__list {
  display: flex;
  max-height: 360px;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
  padding: 8px 10px 8px 28px;
  margin: 0;
  list-style: decimal;
  overscroll-behavior: contain;
  scrollbar-color: var(--text-3) var(--surface-2);
  scrollbar-width: thin;
}

.milk-history__item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex: none;
  padding: 10px 12px;
  border: 1px solid var(--line);
  border-radius: var(--r);
  background: var(--surface-2);
  font-size: var(--fs-sm);
}

.milk-history__date {
  color: var(--text-2);
}

.milk-history__item strong {
  color: var(--accent);
  font-family: var(--font-mono);
  white-space: nowrap;
}

.milk-history__empty {
  padding: 16px;
  color: var(--text-3);
  text-align: center;
  list-style: none;
}

.history-pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-top: 12px;
  margin-top: 12px;
  border-top: 1px solid var(--line);
}

.history-pagination__status {
  color: var(--text-3);
  font-size: var(--fs-sm);
}

.history-pagination__actions {
  display: flex;
  gap: 8px;
}

.history-chart__record {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 10px;
  border-radius: var(--r);
  background: var(--surface-2);
  font-size: var(--fs-sm);
}

.history-chart__date { color: var(--text-3); }
.history-chart__record strong { color: var(--text); white-space: nowrap; }

.history-list { padding: 4px 20px; }

.history-list__item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 0;
  border-bottom: 1px solid var(--line);
}

.history-list__item:last-child { border-bottom: 0; }

.history-list__icon {
  display: grid;
  width: 36px;
  height: 36px;
  place-items: center;
  flex: none;
  border-radius: 50%;
  background: var(--surface-3);
  color: var(--accent);
}

.history-list__content { min-width: 0; flex: 1; }
.history-list__content strong { display: block; color: var(--text); font-size: var(--fs-md); }
.history-list__content p { margin-top: 4px; color: var(--text-2); font-size: var(--fs-sm); }

.nota {
  align-items: flex-start;
  justify-content: flex-start;
  gap: 9px;
  color: var(--text-3);
  font-size: var(--fs-sm);
}

.nota svg { flex: none; }

.variacao--ganho { color: var(--ok); }
.variacao--perda { color: var(--danger); }

.descritivo {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 18px 20px;
  border-top: 1px solid var(--line);
  background: var(--surface-2);
  border-radius: 0 0 var(--r-lg) var(--r-lg);
}

@media (max-width: 520px) {
  .history-chart { padding: 14px; }
  .history-chart__plot { min-height: 220px; }
  .milk-history { padding: 4px 14px 14px; }
  .milk-history__plot { height: 250px; padding: 12px 8px 8px; }
  .milk-history__filters { align-items: flex-start; flex-direction: column; gap: 6px; }
  .milk-history__filters .select { width: 100%; }
  .milk-history__list { padding-left: 24px; }
  .history-pagination { align-items: flex-start; flex-direction: column; }
  .history-pagination__actions { width: 100%; }
  .history-pagination__actions .btn { flex: 1; }
  .history-list { padding: 4px 14px; }
  .history-list__item { flex-wrap: wrap; }
  .history-list__item > .btn { margin-left: 48px; }
}

@media (max-width: 800px) {
  .animal-summary {
    align-items: stretch;
    flex-direction: column;
    gap: 18px;
  }

  .animal-summary__facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }

  .animal-summary__fact:nth-child(odd) { padding-left: 0; border-left: 0; }
}

@media (max-width: 520px) {
  .animal-detail__actions { justify-content: flex-start; }
  .animal-summary { padding: 16px; }
  .animal-summary__facts { gap: 14px 10px; }
  .animal-summary__fact { padding-left: 10px; }
}
</style>

<style scoped>
.animal-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
  color: var(--text-2);
  font-size: var(--fs-sm);
}

.animal-breadcrumb svg { color: var(--text-3); }
.animal-breadcrumb span { color: var(--text); font-weight: 600; }

.animal-summary { padding: 20px 22px; }
.animal-summary__main { display: flex; width: 100%; align-items: center; gap: 22px; }
.animal-summary__identity { min-width: 195px; }
.animal-summary__mark { background: var(--accent-soft); color: var(--accent); }
.animal-summary__name { display: flex; align-items: baseline; flex-wrap: wrap; gap: 7px; }
.animal-summary__register { margin: 0; font-size: var(--fs-3xl); line-height: 1; }
.animal-summary__name > span { color: var(--text-2); font-size: var(--fs-lg); font-weight: 600; }
.animal-summary__facts { grid-template-columns: repeat(3, minmax(90px, 1fr)); gap: 12px; }
.animal-summary__fact:first-child { padding-left: 0; border-left: 0; }
.animal-summary__value--active { color: var(--ok) !important; }
.animal-summary__actions { display: flex; align-items: center; gap: 4px; margin-left: auto; }
.animal-summary__actions .badge { margin-right: 4px; }

.animal-detail__tabs .tabs__item { display: inline-flex; align-items: center; gap: 7px; }
.animal-detail__tabs .tabs__item svg { color: var(--text-3); }
.animal-detail__tabs .animal-tab--milk.is-active,
.animal-detail__tabs .animal-tab--milk.is-active svg { color: var(--accent); }
.animal-detail__tabs .animal-tab--weight.is-active,
.animal-detail__tabs .animal-tab--weight.is-active svg { color: var(--info); }
.animal-detail__tabs .animal-tab--health.is-active,
.animal-detail__tabs .animal-tab--health.is-active svg,
.animal-detail__tabs .animal-tab--veterinary.is-active,
.animal-detail__tabs .animal-tab--veterinary.is-active svg { color: var(--danger); }
.animal-detail__tabs .animal-tab--nutrition.is-active,
.animal-detail__tabs .animal-tab--nutrition.is-active svg { color: var(--warn); }
.animal-detail__tabs .animal-tab--accent.is-active,
.animal-detail__tabs .animal-tab--accent.is-active svg { color: var(--accent); }
.animal-detail__tabs .tabs__item.is-active::after { background: currentColor; }

@media (max-width: 980px) {
  .animal-summary__main { flex-wrap: wrap; }
  .animal-summary__facts { flex-basis: calc(100% - 210px); }
  .animal-summary__actions { margin-left: auto; }
}

@media (max-width: 700px) {
  .animal-summary__facts { flex-basis: 100%; }
  .animal-summary__fact:nth-child(odd) { padding-left: 0; border-left: 0; }
  .animal-summary__actions { width: 100%; justify-content: flex-end; }
}

@media (max-width: 520px) {
  .animal-summary { padding: 16px; }
  .animal-summary__main { gap: 16px; }
  .animal-summary__facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .animal-summary__register { font-size: var(--fs-2xl); }
  .animal-summary__name > span { font-size: var(--fs-md); }
  .animal-summary__actions { justify-content: flex-start; }
  .animal-detail__tabs .tabs__item { padding-inline: 10px; }
}

@media print {
  :global(.sidebar),
  :global(.bar),
  .animal-breadcrumb,
  .animal-summary__actions { display: none !important; }
  :global(.shell__main) { margin: 0 !important; }
  .animal-detail { max-width: none; padding: 0; }
}
</style>
