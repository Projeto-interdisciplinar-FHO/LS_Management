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
          <RouterLink
            v-if="ehAdmin"
            to="/exportar-animais?tipo=ordenha"
            class="btn milk-page__export-button"
          >
            <AppIcon name="download" :size="15" />
            Exportar ordenhas
          </RouterLink>
          <div ref="registerMenuElement" class="milk-page__register">
            <button
              type="button"
              class="btn btn--primary milk-page__register-button"
              aria-haspopup="menu"
              :aria-expanded="menuAberto"
              @click="menuAberto = !menuAberto"
            >
              <AppIcon name="plus" :size="16" />
              Registrar
              <AppIcon name="chevron-down" :size="15" />
            </button>
            <div v-if="menuAberto" class="milk-page__register-menu" role="menu">
              <button type="button" role="menuitem" @click="abrirModal('register')">
                <AppIcon name="milk" :size="16" />
                <span>
                  <strong>Registrar uma ordenha</strong>
                  <small>Lançar a produção de um animal</small>
                </span>
              </button>
              <button type="button" role="menuitem" @click="abrirModal('import')">
                <AppIcon name="upload" :size="16" />
                <span>
                  <strong>Importar uma ordenha</strong>
                  <small>Carregar registros por planilha Excel (.xlsx)</small>
                </span>
              </button>
            </div>
          </div>
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

    <AppModal
      v-if="modal === 'import'"
      titulo="Importar ordenhas por planilha Excel (.xlsx)"
      largo
      @fechar="fecharModal"
    >
      <div class="milk-import">
        <div class="milk-import__instructions">
          <div>
            <strong>Planilha oficial de ordenhas</strong>
            <p>
              Preencha <code>Número do Brinco</code> (individual) ou <code>Estábulo</code> (lote coletivo),
              junto com <code>litros</code> e <code>data</code>.
            </p>
          </div>
          <button type="button" class="btn btn--sm" @click="baixarModelo">
            <AppIcon name="download" :size="14" />
            Baixar modelo (XLSX)
          </button>
        </div>

        <label class="milk-import__dropzone" :class="{ 'milk-import__dropzone--loaded': selectedFileName }">
          <input type="file" accept=".xlsx,.xls,.csv" :disabled="importing" @change="selecionarArquivo">
          <AppIcon :name="selectedFileName ? 'check-circle' : 'upload'" :size="24" />
          <strong>{{ selectedFileName || 'Escolha um arquivo Excel (.xlsx) ou CSV' }}</strong>
          <span>Clique para procurar no computador</span>
        </label>

        <p v-if="importError" class="alert alert--danger" role="alert">
          <AppIcon name="alert" :size="16" />
          <span>{{ importError }}</span>
        </p>

        <template v-if="importPreview">
          <div class="milk-import__summary">
            <strong>{{ importPreview.total_linhas_processadas }} linha(s) analisada(s)</strong>
            <span v-if="importPreview.total_falhas" class="milk-import__invalid">
              {{ importPreview.total_falhas }} {{ importPreview.total_falhas === 1 ? 'linha precisa' : 'linhas precisam' }} de correção
            </span>
            <span v-else class="milk-import__valid">Pronto para importar</span>
          </div>

          <div v-if="importPreview.exemplos_importados?.length" class="milk-import__preview">
            <table class="table">
              <thead>
                <tr><th>Linha</th><th>Tipo</th><th>Identificação</th><th>Data</th><th>Litros</th><th>Horário</th></tr>
              </thead>
              <tbody>
                <tr v-for="item in importPreview.exemplos_importados" :key="item.linha">
                  <td>{{ item.linha }}</td>
                  <td>
                    <span class="badge" :class="item.tipo === 'estabulo' ? 'badge--blue' : ''">
                      {{ item.tipo === 'estabulo' ? 'Estábulo (Lote)' : 'Individual' }}
                    </span>
                  </td>
                  <td>
                    <span v-if="item.tipo === 'estabulo'">{{ item.estabulo }} ({{ item.vacas_atendidas }} vacas)</span>
                    <span v-else>#{{ item.brinco }} · {{ item.nome_animal }}</span>
                  </td>
                  <td>{{ item.data }}</td>
                  <td>
                    <span v-if="item.tipo === 'estabulo'">{{ formatarNumero(item.litros_total) }} L ({{ formatarNumero(item.litros_por_vaca) }} L/vaca)</span>
                    <span v-else>{{ formatarNumero(item.litros) }} L</span>
                  </td>
                  <td>{{ item.inicio ? `${item.inicio} - ${item.fim || ''}` : '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <ul v-if="importPreview.erros?.length" class="milk-import__errors" aria-label="Linhas com erro">
            <li v-for="err in importPreview.erros" :key="`erro-${err.linha}`">
              <strong>Linha {{ err.linha }}:</strong> {{ err.erros?.join(' · ') || err.erro }}
            </li>
          </ul>
        </template>

        <p v-if="importMessage" class="alert" :class="importSuccess ? 'alert--ok' : 'alert--danger'" :role="importSuccess ? 'status' : 'alert'">
          <AppIcon :name="importSuccess ? 'check-circle' : 'alert'" :size="16" />
          <span>{{ importMessage }}</span>
        </p>

        <footer class="milk-form__actions">
          <button type="button" class="btn" :disabled="importing" @click="fecharModal">Fechar</button>
          <button
            type="button"
            class="btn btn--primary"
            :disabled="importing || !selectedFile || (importPreview && importPreview.total_importados === 0)"
            @click="importarOrdenhas"
          >
            {{ importing ? 'Importando ordenhas...' : 'Confirmar importação' }}
          </button>
        </footer>
      </div>
    </AppModal>
  </AppShell>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import {
  CategoryScale,
  Chart as ChartJS,
  LineController,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip,
} from 'chart.js';
import { Line } from 'vue-chartjs';
import api from '@/services/api';
import { ehAdministrador } from '@/services/auth';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppModal from '@/components/ui/AppModal.vue';
import { apiErrorMessage } from '@/utils/apiError';

ChartJS.register(CategoryScale, LinearScale, LineController, LineElement, PointElement, Tooltip);

const ehAdmin = computed(() => ehAdministrador());
const menuAberto = ref(false);
const registerMenuElement = ref(null);
const modal = ref('');
const loading = ref(true);
const loadingAnimals = ref(true);
const loadingQuadrants = ref(true);
const submitting = ref(false);
const importing = ref(false);
const loadError = ref('');
const animalLoadError = ref('');
const animals = ref([]);
const quadrants = ref([]);
const quadrantLoadError = ref('');
const registros = ref([]);
const periodo = ref('30');
const formMessage = ref('');
const formSuccess = ref(false);
const importMessage = ref('');
const importSuccess = ref(false);
const selectedFile = ref(null);
const selectedFileName = ref('');
const importError = ref('');
const importPreview = ref(null);

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

const chartData = computed(() => ({
  labels: producaoPorDia.value.map(({ data }) => formatarData(data)),
  datasets: [{
    label: 'Produção total (L)',
    data: producaoPorDia.value.map(({ litros }) => litros),
    borderColor: chartColor('--accent'),
    backgroundColor: chartColor('--accent-soft'),
    pointBackgroundColor: chartColor('--accent'),
    pointBorderColor: chartColor('--surface'),
    pointBorderWidth: 2,
    pointRadius: producaoPorDia.value.length > 60 ? 1 : 4,
    pointHoverRadius: 6,
    borderWidth: 3,
    tension: 0.3,
    fill: true,
  }],
}));

function chartColor(token) {
  return getComputedStyle(document.documentElement).getPropertyValue(token).trim();
}

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { intersect: false, mode: 'index' },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context) => ` ${formatarNumero(context.raw)} L`,
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: {
        color: chartColor('--text-3'),
        maxRotation: 0,
        autoSkip: true,
        maxTicksLimit: 10,
      },
    },
    y: {
      beginAtZero: true,
      grid: { color: chartColor('--line') },
      ticks: {
        color: chartColor('--text-3'),
        callback: (value) => `${formatarNumero(value)} L`,
      },
    },
  },
}));

function abrirModal(tipo) {
  menuAberto.value = false;
  modal.value = tipo;
  if (tipo === 'register') {
    formMessage.value = '';
    formSuccess.value = false;
  } else {
    limparImportacao();
  }
}

function fecharModal() {
  if (submitting.value || importing.value) return;
  modal.value = '';
}

function aoClicarFora(event) {
  if (!registerMenuElement.value?.contains(event.target)) menuAberto.value = false;
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

function limparImportacao() {
  selectedFile.value = null;
  selectedFileName.value = '';
  importError.value = '';
  importPreview.value = null;
  importMessage.value = '';
  importSuccess.value = false;
  importing.value = false;
}

async function selecionarArquivo(event) {
  const input = event.currentTarget;
  const file = input.files?.[0];
  limparImportacao();
  if (!file) return;
  input.value = '';
  selectedFile.value = file;
  selectedFileName.value = file.name;

  if (!/\.(xlsx|xls|csv)$/i.test(file.name)) {
    importError.value = 'Selecione um arquivo Excel (.xlsx, .xls) ou CSV.';
    return;
  }

  try {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('importacao/ordenhas/?dry_run=true', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    importPreview.value = response.data;
  } catch (err) {
    console.error('Erro na validação da planilha de ordenhas:', err);
    importError.value = apiErrorMessage(err, 'Não foi possível validar o arquivo.');
  }
}

async function importarOrdenhas() {
  if (!selectedFile.value || importing.value) return;
  importing.value = true;
  importMessage.value = '';
  importError.value = '';

  try {
    const formData = new FormData();
    formData.append('file', selectedFile.value);
    const response = await api.post('importacao/ordenhas/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    importSuccess.value = response.data.sucesso || response.data.total_importados > 0;
    importMessage.value = response.data.mensagem || `${response.data.total_importados} ordenha(s) importada(s) com sucesso.`;
    if (response.data.total_importados > 0) {
      await carregarDados();
    }
  } catch (err) {
    console.error('Erro ao importar ordenhas:', err);
    importSuccess.value = false;
    importMessage.value = apiErrorMessage(err, 'Falha ao importar registros de ordenha.');
  } finally {
    importing.value = false;
  }
}

function baixarModelo() {
  const link = document.createElement('a');
  link.href = '/modelos/modelo_importacao_ordenhas.xlsx';
  link.download = 'modelo_importacao_ordenhas.xlsx';
  document.body.appendChild(link);
  link.click();
  link.remove();
}

onMounted(() => {
  document.addEventListener('pointerdown', aoClicarFora);
  carregarDados();
  carregarEstabulos();
});

onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', aoClicarFora);
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
.milk-page__register { position: relative; z-index: 3; }
.milk-page__register-button { gap: 8px; }
.milk-page__register-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  z-index: 10;
  width: min(290px, calc(100vw - 32px));
  padding: 6px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface);
  box-shadow: var(--shadow-md);
}
.milk-page__register-menu button {
  display: flex;
  width: 100%;
  align-items: flex-start;
  gap: 11px;
  padding: 10px;
  border: 0;
  border-radius: var(--r);
  background: transparent;
  color: var(--text-2);
  text-align: left;
  cursor: pointer;
}
.milk-page__register-menu button:hover { background: var(--surface-2); color: var(--accent); }
.milk-page__register-menu button > svg { flex: none; margin-top: 2px; }
.milk-page__register-menu span { display: grid; gap: 3px; }
.milk-page__register-menu strong { color: var(--text); font-size: var(--fs-sm); }
.milk-page__register-menu small { color: var(--text-3); font-size: var(--fs-xs); }
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
.milk-import { display: grid; gap: 16px; }
.milk-import__instructions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface-2);
}
.milk-import__instructions strong { color: var(--text); font-size: var(--fs-sm); }
.milk-import__instructions p { margin-top: 5px; color: var(--text-2); font-size: var(--fs-xs); line-height: 1.6; }
.milk-import__instructions code { color: var(--accent); }
.milk-import__dropzone {
  position: relative;
  display: grid;
  min-height: 145px;
  place-content: center;
  justify-items: center;
  gap: 7px;
  border: 1px dashed var(--line-strong);
  border-radius: var(--r-md);
  color: var(--text-3);
  cursor: pointer;
  transition: border-color .15s, background .15s;
}
.milk-import__dropzone:hover,
.milk-import__dropzone--loaded { border-color: var(--accent); background: var(--accent-soft); }
.milk-import__dropzone svg { color: var(--accent); }
.milk-import__dropzone strong { max-width: 90%; overflow: hidden; color: var(--text); text-overflow: ellipsis; white-space: nowrap; }
.milk-import__dropzone span { font-size: var(--fs-xs); }
.milk-import__dropzone input { position: absolute; width: 1px; height: 1px; opacity: 0; }
.milk-import__summary { display: flex; flex-wrap: wrap; align-items: center; gap: 9px; color: var(--text); font-size: var(--fs-sm); }
.milk-import__valid { color: var(--ok); font-size: var(--fs-xs); }
.milk-import__invalid { color: var(--danger); font-size: var(--fs-xs); }
.milk-import__preview { max-height: 270px; overflow: auto; border: 1px solid var(--line); border-radius: var(--r-md); }
.milk-import__preview .table { min-width: 650px; }
.milk-import__row-error { color: var(--danger); }
.milk-import__row-valid { color: var(--ok); }
.milk-import__more { color: var(--text-3); font-size: var(--fs-xs); }
.milk-import__errors { display: grid; gap: 4px; padding-left: 18px; color: var(--danger); font-size: var(--fs-xs); }
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
  .milk-import__instructions { align-items: flex-start; flex-direction: column; }
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
