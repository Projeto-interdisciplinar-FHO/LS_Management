<template>
  <AppShell>
    <div class="page page--wide milk-page">
      <header class="milk-page__header">
        <div>
          <p class="milk-page__eyebrow">Produção do rebanho</p>
          <h1 class="page__title">Ordenha</h1>
          <p class="page__desc">Acompanhe os registros e a produção geral de leite.</p>
        </div>

        <div class="milk-page__header-actions">
          <button
            type="button"
            class="btn btn--primary milk-page__register-button"
            @click="abrirModal('register')"
          >
            <AppIcon name="plus" :size="16" />
            Registrar ordenha
          </button>
        </div>
      </header>

      <p v-if="loadError" class="alert alert--danger milk-page__alert" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ loadError }}</span>
        <button type="button" class="btn btn--sm" @click="carregarDados">Tentar novamente</button>
      </p>

      <section class="milk-page__metrics" aria-label="Resumo da produção de leite">
        <article class="card milk-metric">
          <span class="milk-metric__icon milk-metric__icon--accent"><AppIcon name="milk" :size="18" /></span>
          <div>
            <span class="milk-metric__label">Produção no período</span>
            <strong>{{ formatarNumero(totalPeriodo) }} <small>L</small></strong>
          </div>
        </article>
        <article class="card milk-metric">
          <span class="milk-metric__icon milk-metric__icon--blue"><AppIcon name="clipboard" :size="18" /></span>
          <div>
            <span class="milk-metric__label">Ordenhas registradas</span>
            <strong>{{ registrosNoPeriodo.length }}</strong>
          </div>
        </article>
        <article class="card milk-metric">
          <span class="milk-metric__icon milk-metric__icon--green"><AppIcon name="animal" :size="18" /></span>
          <div>
            <span class="milk-metric__label">Animais ordenhados</span>
            <strong>{{ animaisOrdenhados }}</strong>
          </div>
        </article>
      </section>

      <section class="milk-page__averages" aria-label="Médias diárias de produção">
        <article class="card milk-average">
          <span class="milk-page__eyebrow">Média diária · últimos 10 dias</span>
          <strong>{{ mediaDeProducao(10) }} <small>L/dia</small></strong>
        </article>
        <article class="card milk-average">
          <span class="milk-page__eyebrow">Média diária · mês atual</span>
          <strong>{{ mediaDoMes }} <small>L/dia</small></strong>
        </article>
        <article class="card milk-average">
          <span class="milk-page__eyebrow">Média diária · ano atual</span>
          <strong>{{ mediaDoAno }} <small>L/dia</small></strong>
        </article>
      </section>

      <section class="card milk-chart-card" aria-labelledby="milk-chart-title">
        <header class="card__head milk-chart-card__head">
          <div>
            <h2 id="milk-chart-title" class="card__title">Produção geral de leite</h2>
            <p class="card__desc">Total de litros registrados por dia.</p>
          </div>
          <label class="milk-page__period">
            <span class="sr-only">Período do gráfico</span>
            <select v-model="periodo" class="select">
              <option value="7">Últimos 7 dias</option>
              <option value="30">Últimos 30 dias</option>
              <option value="90">Últimos 90 dias</option>
              <option value="todos">Todo o histórico</option>
            </select>
          </label>
        </header>

        <div v-if="loading" class="milk-chart-card__state">
          <span class="spinner" aria-hidden="true"></span>
          Carregando dados da ordenha...
        </div>
        <div v-else-if="!producaoPorDia.length" class="milk-chart-card__state milk-chart-card__state--empty">
          <AppIcon name="chart" :size="28" />
          <strong>Sem ordenhas neste período</strong>
          <span>Registre uma ordenha para acompanhar a produção no gráfico.</span>
        </div>
        <div v-else class="milk-chart-card__plot">
          <Line :data="chartData" :options="chartOptions" aria-label="Gráfico geral de litros de leite por dia" />
        </div>
      </section>

    </div>

    <AppModal
      v-if="modal === 'register'"
      titulo="Registrar uma ordenha"
      @fechar="fecharModal"
    >
      <form class="milk-form" @submit.prevent="registrarOrdenha">
        <div class="field">
          <label class="field__label" for="milk-stable">Estábulo (contexto)</label>
          <select id="milk-stable" v-model="form.quadrant" class="select" :disabled="loadingQuadrants || submitting">
            <option value="">Não selecionado</option>
            <option v-for="quadrant in quadrants" :key="quadrant.id" :value="quadrant.id">
              {{ quadrant.name || quadrant.tipo || `Estábulo ${quadrant.id}` }}
            </option>
          </select>
            <span v-if="quadrantLoadError" class="field__hint" role="alert">{{ quadrantLoadError }}</span>
        </div>
        <div class="field">
          <label class="field__label" for="milk-animal">Animal</label>
          <select
            id="milk-animal"
            v-model="form.animal"
            class="select"
            required
            :disabled="loadingAnimals || !animals.length || submitting"
          >
            <option value="" disabled>
              {{ loadingAnimals ? 'Carregando animais...' : 'Selecione um animal...' }}
            </option>
            <option v-for="animal in animals" :key="animal.id" :value="animal.id">
              {{ animal.name || 'Sem nome' }} — brinco #{{ animal.register_number }}
            </option>
          </select>
          <span v-if="animalLoadError" class="field__hint" role="alert">{{ animalLoadError }}</span>
        </div>

        <div class="milk-form__row">
          <div class="field">
            <label class="field__label" for="milk-quantity">Quantidade (litros)</label>
            <input
              id="milk-quantity"
              v-model="form.milk_production"
              class="input"
              type="number"
              inputmode="decimal"
              min="0.01"
              step="0.01"
              placeholder="Ex.: 15,5"
              required
              :disabled="submitting"
            >
          </div>
          <div class="field">
            <label class="field__label" for="milk-date">Data da ordenha</label>
            <input
              id="milk-date"
              v-model="form.production_date"
              class="input"
              type="date"
              required
              :disabled="submitting"
            >
          </div>
        </div>

        <div class="milk-form__row">
          <div class="field">
            <label class="field__label" for="milk-start-time">Horário de início</label>
            <input id="milk-start-time" v-model="form.start_time" class="input" type="time" required :disabled="submitting">
          </div>
          <div class="field">
            <label class="field__label" for="milk-end-time">Horário de término</label>
            <input id="milk-end-time" v-model="form.end_time" class="input" type="time" required :disabled="submitting">
          </div>
        </div>

        <p class="alert alert--warn" role="status">
          <AppIcon name="info" :size="16" />
          <span>
            A API atual não vincula o registro a um estábulo nem informa carência sanitária.
            O estábulo é apenas contexto; confirme a liberação do animal antes da ordenha.
          </span>
        </p>

        <p v-if="formMessage" class="alert" :class="formSuccess ? 'alert--ok' : 'alert--danger'" :role="formSuccess ? 'status' : 'alert'">
          <AppIcon :name="formSuccess ? 'check-circle' : 'alert'" :size="16" />
          <span>{{ formMessage }}</span>
        </p>

        <footer class="milk-form__actions">
          <button type="button" class="btn" :disabled="submitting" @click="fecharModal">Cancelar</button>
          <button type="submit" class="btn btn--primary" :disabled="submitting || loadingAnimals || !animals.length || !form.start_time || !form.end_time">
            {{ submitting ? 'Salvando...' : 'Registrar ordenha' }}
          </button>
        </footer>
      </form>
    </AppModal>
  </AppShell>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import {
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LineController,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip,
} from 'chart.js';
import { Line } from 'vue-chartjs';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppModal from '@/components/ui/AppModal.vue';
import { apiErrorMessage } from '@/utils/apiError';

ChartJS.register(CategoryScale, LinearScale, LineController, LineElement, PointElement, Filler, Legend, Tooltip);

const modal = ref('');
const loading = ref(true);
const loadingAnimals = ref(true);
const loadingQuadrants = ref(true);
const submitting = ref(false);
const loadError = ref('');
const animalLoadError = ref('');
const animals = ref([]);
const quadrants = ref([]);
const quadrantLoadError = ref('');
const registros = ref([]);
const periodo = ref('todos');
const formMessage = ref('');
const formSuccess = ref(false);

const form = ref({
  animal: '',
  quadrant: '',
  milk_production: '',
  production_date: dataLocalHoje(),
  start_time: '',
  end_time: '',
});

function dataLocalHoje() {
  const hoje = new Date();
  return new Date(hoje.getTime() - hoje.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

function listaDaResposta(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  throw new Error('A API retornou um formato inesperado para a lista.');
}

async function consultarTodos(endpoint) {
  const itens = [];
  let url = endpoint;
  const visitadas = new Set();

  while (url) {
    if (visitadas.has(url)) throw new Error(`A paginação de ${endpoint} retornou uma página repetida.`);
    visitadas.add(url);
    const resposta = await api.get(url);
    const data = resposta.data;
    itens.push(...listaDaResposta(data));
    url = Array.isArray(data) ? null : data.next || null;
  }

  return itens;
}

async function carregarDados() {
  loading.value = true;
  loadError.value = '';
  try {
    const [historico] = await Promise.all([
      consultarTodos('milk_production_history/'),
      carregarAnimais(),
    ]);
    registros.value = historico;
  } catch (error) {
    console.error('Erro ao carregar dados da ordenha:', error);
    loadError.value = apiErrorMessage(error, 'Não foi possível carregar os dados da ordenha.');
  } finally {
    loading.value = false;
  }
}

async function carregarAnimais() {
  loadingAnimals.value = true;
  animalLoadError.value = '';
  try {
    animals.value = await consultarTodos('animals/');
  } catch (error) {
    console.error('Erro ao carregar animais para ordenha:', error);
    animals.value = [];
    animalLoadError.value = apiErrorMessage(error, 'Não foi possível carregar os animais.');
    throw error;
  } finally {
    loadingAnimals.value = false;
  }
}

async function carregarEstabulos() {
  loadingQuadrants.value = true;
  quadrantLoadError.value = '';
  try {
    const response = await api.getQuadrants();
    quadrants.value = listaDaResposta(response.data);
  } catch (error) {
    console.error('Erro ao carregar estábulos para a ordenha:', error);
    quadrants.value = [];
    quadrantLoadError.value = apiErrorMessage(error, 'Não foi possível carregar os estábulos.');
  } finally {
    loadingQuadrants.value = false;
  }
}

function dataRegistro(registro) {
  const valor = String(registro.production_date || '').slice(0, 10);
  const data = new Date(`${valor}T00:00:00`);
  return Number.isNaN(data.getTime()) ? null : data;
}

const registrosNoPeriodo = computed(() => {
  if (periodo.value === 'todos') return registros.value;
  const limite = new Date();
  limite.setHours(0, 0, 0, 0);
  limite.setDate(limite.getDate() - (Number(periodo.value) - 1));
  return registros.value.filter((registro) => {
    const data = dataRegistro(registro);
    return data && data >= limite && data <= new Date();
  });
});

const totalPeriodo = computed(() => registrosNoPeriodo.value.reduce(
  (total, registro) => total + (Number(registro.milk_production) || 0),
  0
));

const animaisOrdenhados = computed(() => new Set(
  registrosNoPeriodo.value.map((registro) => idAnimal(registro.animal)).filter(Boolean)
).size);

function mediaNoIntervalo(inicio, dias) {
  const registrosNoIntervalo = registros.value.filter((record) => {
    const date = String(record.production_date || '').slice(0, 10);
    return date >= inicio && date <= dataLocalHoje();
  });
  if (!registrosNoIntervalo.length) return '—';
  const total = registrosNoIntervalo.reduce((sum, record) => sum + (Number(record.milk_production) || 0), 0);
  return formatarNumero(total / dias);
}

function mediaDeProducao(days) {
  const today = new Date(`${dataLocalHoje()}T00:00:00`);
  today.setDate(today.getDate() - days + 1);
  const start = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  return mediaNoIntervalo(start, days);
}

const mediaDoMes = computed(() => {
  const today = new Date(`${dataLocalHoje()}T00:00:00`);
  const start = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-01`;
  return mediaNoIntervalo(start, today.getDate());
});

const mediaDoAno = computed(() => {
  const today = new Date(`${dataLocalHoje()}T00:00:00`);
  const start = `${today.getFullYear()}-01-01`;
  const days = Math.floor((Date.UTC(today.getFullYear(), today.getMonth(), today.getDate()) - Date.UTC(today.getFullYear(), 0, 1)) / 86400000) + 1;
  return mediaNoIntervalo(start, days);
});

function idAnimal(value) {
  return value && typeof value === 'object' ? value.id : value;
}

function formatarNumero(value) {
  return Number(value || 0).toLocaleString('pt-BR', { maximumFractionDigits: 2 });
}

function formatarData(value) {
  if (!value) return '—';
  const data = new Date(`${String(value).slice(0, 10)}T00:00:00`);
  return Number.isNaN(data.getTime()) ? '—' : data.toLocaleDateString('pt-BR');
}

const producaoPorDia = computed(() => {
  const totais = new Map();
  for (const registro of registrosNoPeriodo.value) {
    const data = String(registro.production_date || '').slice(0, 10);
    if (!dataRegistro(registro)) continue;
    totais.set(data, (totais.get(data) || 0) + (Number(registro.milk_production) || 0));
  }
  return [...totais.entries()]
    .sort(([dataA], [dataB]) => dataA.localeCompare(dataB))
    .map(([data, litros]) => ({ data, litros }));
});

const mediaDiariaPeriodo = computed(() => {
  if (!producaoPorDia.value.length) return 0;
  const soma = producaoPorDia.value.reduce((acc, item) => acc + item.litros, 0);
  return soma / producaoPorDia.value.length;
});

function gradientArea(context) {
  const { ctx, chartArea } = context.chart;
  const accent = chartColor('--accent') || '#2f6b46';
  if (!chartArea) return accent;
  const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
  gradient.addColorStop(0, `${accent}42`);
  gradient.addColorStop(0.65, `${accent}14`);
  gradient.addColorStop(1, `${accent}00`);
  return gradient;
}

const chartData = computed(() => {
  const accent = chartColor('--accent') || '#2f6b46';
  const surface = chartColor('--surface') || '#ffffff';
  const warn = chartColor('--warn') || '#b47418';
  const valores = producaoPorDia.value.map(({ litros }) => litros);
  const media = Number(mediaDiariaPeriodo.value.toFixed(2));

  return {
    labels: producaoPorDia.value.map(({ data }) => formatarData(data)),
    datasets: [
      {
        label: 'Produção diária (L)',
        data: valores,
        borderColor: accent,
        backgroundColor: gradientArea,
        pointBackgroundColor: accent,
        pointBorderColor: surface,
        pointBorderWidth: 2.5,
        pointHoverBackgroundColor: surface,
        pointHoverBorderColor: accent,
        pointHoverBorderWidth: 3,
        pointRadius: producaoPorDia.value.length > 60 ? 2 : 5,
        pointHoverRadius: 7,
        borderWidth: 3,
        tension: 0.36,
        fill: true,
      },
      ...(valores.length > 1
        ? [{
            label: `Média do período (${formatarNumero(media)} L)`,
            data: valores.map(() => media),
            borderColor: warn,
            borderWidth: 1.75,
            borderDash: [6, 5],
            pointRadius: 0,
            pointHoverRadius: 0,
            fill: false,
            tension: 0,
          }]
        : []),
    ],
  };
});

function chartColor(token) {
  return getComputedStyle(document.documentElement).getPropertyValue(token).trim();
}

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: { left: 2, right: 12 } },
  interaction: { intersect: false, mode: 'index' },
  plugins: {
    legend: {
      display: true,
      position: 'top',
      align: 'end',
      labels: {
        usePointStyle: true,
        pointStyle: 'circle',
        boxWidth: 8,
        boxHeight: 8,
        padding: 16,
        color: chartColor('--text-2') || '#525b53',
        font: { size: 12, weight: '500' },
      },
    },
    tooltip: {
      backgroundColor: 'rgba(20, 26, 22, 0.92)',
      titleColor: '#ffffff',
      bodyColor: '#e9eee9',
      borderColor: 'rgba(255, 255, 255, 0.12)',
      borderWidth: 1,
      cornerRadius: 10,
      padding: 12,
      displayColors: true,
      callbacks: {
        label: (context) => ` ${context.dataset.label.split(' (')[0]}: ${formatarNumero(context.raw)} L`,
      },
    },
  },
  scales: {
    x: {
      offset: false,
      border: { display: false },
      grid: { display: false },
      ticks: {
        padding: 8,
        color: chartColor('--text-3'),
        font: { size: 11 },
        maxRotation: 0,
        autoSkip: true,
        maxTicksLimit: 10,
      },
    },
    y: {
      beginAtZero: true,
      grace: '12%',
      border: { display: false, dash: [4, 4] },
      grid: {
        color: chartColor('--line'),
        tickLength: 0,
      },
      ticks: {
        padding: 10,
        color: chartColor('--text-3'),
        font: { size: 11 },
        callback: (value) => `${formatarNumero(value)} L`,
      },
    },
  },
}));

function abrirModal(tipo) {
  modal.value = tipo;
  formMessage.value = '';
  formSuccess.value = false;
}

function fecharModal() {
  if (submitting.value) return;
  modal.value = '';
}

async function registrarOrdenha() {
  if (form.value.end_time <= form.value.start_time) {
    formSuccess.value = false;
    formMessage.value = 'O horário de término deve ser posterior ao horário de início.';
    return;
  }
  submitting.value = true;
  formMessage.value = '';
  try {
    await api.post('milk_production_history/', {
      animal: Number(form.value.animal),
      milk_production: Number(form.value.milk_production),
      production_date: form.value.production_date,
      start_time: new Date(`${form.value.production_date}T${form.value.start_time}:00`).toISOString(),
      end_time: new Date(`${form.value.production_date}T${form.value.end_time}:00`).toISOString(),
    });
    formSuccess.value = true;
    formMessage.value = 'Ordenha registrada. Horários enviados; o vínculo com o estábulo não é armazenado pela API atual.';
    form.value = { animal: '', quadrant: '', milk_production: '', production_date: dataLocalHoje(), start_time: '', end_time: '' };
    await carregarDados();
    window.setTimeout(() => {
      if (modal.value === 'register') modal.value = '';
    }, 900);
  } catch (error) {
    console.error('Erro ao registrar ordenha:', error);
    formSuccess.value = false;
    formMessage.value = apiErrorMessage(error, 'Não foi possível registrar a ordenha. Confira os dados informados.');
  } finally {
    submitting.value = false;
  }
}

onMounted(() => {
  carregarDados();
  carregarEstabulos();
});
</script>

<style scoped>
.milk-page { display: grid; gap: 18px; }
.milk-page__header { display: flex; align-items: flex-end; justify-content: space-between; gap: 20px; }
.milk-page__eyebrow {
  margin-bottom: 5px;
  color: var(--accent);
  font-size: var(--fs-xs);
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.milk-page__header-actions { display: flex; align-items: center; gap: 9px; }
.milk-page__register-button { gap: 8px; }
.milk-page__alert { margin: 0; }
.milk-page__alert .btn { margin-left: auto; }

.milk-page__metrics { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.milk-page__averages { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.milk-average { display: grid; justify-items: center; gap: 7px; padding: 16px; text-align: center; }
.milk-average strong { display: inline-flex; align-items: baseline; justify-content: center; gap: 4px; color: var(--text); font-size: 1.3rem; }
.milk-average small { color: var(--text-3); font-size: var(--fs-sm); font-weight: 500; }
.milk-metric { display: grid; justify-items: center; gap: 10px; padding: 17px; text-align: center; }
.milk-metric__icon {
  display: grid;
  width: 42px;
  height: 42px;
  flex: none;
  place-items: center;
  border-radius: var(--r-md);
}
.milk-metric__icon--accent { background: var(--accent-soft); color: var(--accent); }
.milk-metric__icon--blue { background: var(--info-soft); color: var(--info); }
.milk-metric__icon--green { background: var(--ok-soft); color: var(--ok); }
.milk-metric > div { display: grid; justify-items: center; gap: 4px; min-width: 0; }
.milk-metric__label { color: var(--text-3); font-size: var(--fs-xs); }
.milk-metric strong { display: inline-flex; align-items: baseline; justify-content: center; gap: 4px; color: var(--text); font-size: 1.35rem; line-height: 1.2; }
.milk-metric strong small { color: var(--text-3); font-size: var(--fs-sm); font-weight: 500; }

.milk-chart-card { min-width: 0; overflow: hidden; }
.milk-chart-card__head { align-items: center; }
.milk-page__period { width: auto; }
.milk-page__period .select { min-width: 155px; }
.milk-chart-card__plot { position: relative; height: 330px; padding: 8px 20px 20px; }
.milk-chart-card__state {
  display: flex;
  min-height: 180px;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: var(--text-3);
  font-size: var(--fs-sm);
}
.milk-chart-card__state--empty { flex-direction: column; gap: 7px; padding: 24px; text-align: center; }
.milk-chart-card__state--empty svg { margin-bottom: 4px; color: var(--accent); }
.milk-chart-card__state--empty strong { color: var(--text); }
.milk-form { display: grid; gap: 18px; }
.milk-form__row { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.milk-form__actions { display: flex; justify-content: flex-end; gap: 9px; }
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  clip-path: inset(50%);
}

@media (max-width: 720px) {
  .milk-page__header { align-items: flex-start; }
  .milk-page__header-actions { flex-wrap: wrap; }
  .milk-page__metrics { grid-template-columns: 1fr; gap: 9px; }
  .milk-page__averages { grid-template-columns: 1fr; gap: 9px; }
  .milk-metric { padding: 13px; }
  .milk-chart-card__plot { height: 260px; padding: 8px 10px 14px; }
  .milk-form__row { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  .milk-page__header { align-items: stretch; flex-direction: column; }
  .milk-page__header-actions { align-items: flex-start; }
  .milk-chart-card__head { align-items: flex-start; flex-direction: column; }
  .milk-page__period, .milk-page__period .select { width: 100%; }
  .milk-form__actions { flex-direction: column-reverse; }
  .milk-form__actions .btn { width: 100%; }
}
</style>
