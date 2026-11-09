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
                  <small>Carregar vários registros por CSV</small>
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

        <p v-if="formMessage" class="alert" :class="formSuccess ? 'alert--ok' : 'alert--danger'" :role="formSuccess ? 'status' : 'alert'">
          <AppIcon :name="formSuccess ? 'check-circle' : 'alert'" :size="16" />
          <span>{{ formMessage }}</span>
        </p>

        <footer class="milk-form__actions">
          <button type="button" class="btn" :disabled="submitting" @click="fecharModal">Cancelar</button>
          <button type="submit" class="btn btn--primary" :disabled="submitting || loadingAnimals || !animals.length">
            {{ submitting ? 'Salvando...' : 'Registrar ordenha' }}
          </button>
        </footer>
      </form>
    </AppModal>

    <AppModal
      v-if="modal === 'import'"
      titulo="Importar ordenhas por CSV"
      largo
      @fechar="fecharModal"
    >
      <div class="milk-import">
        <div class="milk-import__instructions">
          <div>
            <strong>Prepare seu arquivo CSV</strong>
            <p>Use as colunas <code>numero_do_brinco</code>, <code>litros</code> e <code>data</code>. A data pode estar em DD/MM/AAAA ou AAAA-MM-DD.</p>
          </div>
          <button type="button" class="btn btn--sm" @click="baixarModelo">
            <AppIcon name="download" :size="14" />
            Baixar modelo
          </button>
        </div>

        <label class="milk-import__dropzone" :class="{ 'milk-import__dropzone--loaded': csvFileName }">
          <input type="file" accept=".csv,text/csv" :disabled="importing" @change="selecionarArquivo">
          <AppIcon :name="csvFileName ? 'check-circle' : 'upload'" :size="24" />
          <strong>{{ csvFileName || 'Escolha um arquivo CSV' }}</strong>
          <span>Clique para procurar no computador</span>
        </label>

        <p v-if="csvError" class="alert alert--danger" role="alert">
          <AppIcon name="alert" :size="16" />
          <span>{{ csvError }}</span>
        </p>

        <template v-if="csvRows.length">
          <div class="milk-import__summary">
            <strong>{{ csvRows.length }} linhas encontradas</strong>
            <span v-if="csvInvalidRows.length" class="milk-import__invalid">
              {{ csvInvalidRows.length }} {{ csvInvalidRows.length === 1 ? 'linha precisa' : 'linhas precisam' }} de correção
            </span>
            <span v-else class="milk-import__valid">Arquivo pronto para importar</span>
          </div>
          <div class="milk-import__preview">
            <table class="table">
              <thead>
                <tr><th>Linha</th><th>Brinco</th><th>Animal</th><th>Data</th><th>Litros</th><th>Validação</th></tr>
              </thead>
              <tbody>
                <tr v-for="row in csvRows.slice(0, 8)" :key="row.line">
                  <td>{{ row.line }}</td>
                  <td>#{{ row.registerNumber }}</td>
                  <td>{{ row.animal?.name || '—' }}</td>
                  <td>{{ row.displayDate || '—' }}</td>
                  <td>{{ row.displayQuantity || '—' }}</td>
                  <td :class="row.error ? 'milk-import__row-error' : 'milk-import__row-valid'">
                    {{ row.error || 'Pronta' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <ul v-if="csvInvalidRows.length" class="milk-import__errors" aria-label="Linhas com erro">
            <li v-for="row in csvInvalidRows.slice(0, 10)" :key="`erro-${row.line}`">
              Linha {{ row.line }}: {{ row.error }}
            </li>
          </ul>
          <p v-if="csvRows.length > 8" class="milk-import__more">
            Mostrando 8 de {{ csvRows.length }} linhas. Todas serão validadas antes da importação.
          </p>
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
            :disabled="importing || !csvRows.length || csvInvalidRows.length > 0"
            @click="importarOrdenhas"
          >
            {{ importing ? `Importando ${importProgress}/${csvRows.length}...` : `Importar ${csvRows.length || ''} ordenhas` }}
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
const submitting = ref(false);
const importing = ref(false);
const loadError = ref('');
const animalLoadError = ref('');
const animals = ref([]);
const registros = ref([]);
const periodo = ref('30');
const formMessage = ref('');
const formSuccess = ref(false);
const importMessage = ref('');
const importSuccess = ref(false);
const csvFileName = ref('');
const csvError = ref('');
const csvRows = ref([]);
const importProgress = ref(0);

const form = ref({
  animal: '',
  milk_production: '',
  production_date: dataLocalHoje(),
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
  submitting.value = true;
  formMessage.value = '';
  try {
    await api.post('milk_production_history/', {
      animal: Number(form.value.animal),
      milk_production: Number(form.value.milk_production),
      production_date: form.value.production_date,
    });
    formSuccess.value = true;
    formMessage.value = 'Ordenha registrada com sucesso.';
    form.value = { animal: '', milk_production: '', production_date: dataLocalHoje() };
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

function parseCsv(text) {
  const primeiraLinha = text.split(/\r?\n/, 1)[0] || '';
  const delimitador = (primeiraLinha.match(/;/g) || []).length > (primeiraLinha.match(/,/g) || []).length
    ? ';'
    : ',';
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (char === '"') {
      if (quoted && text[index + 1] === '"') {
        cell += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === delimitador && !quoted) {
      row.push(cell);
      cell = '';
    } else if ((char === '\n' || char === '\r') && !quoted) {
      row.push(cell);
      if (row.some((value) => value.trim())) rows.push(row);
      row = [];
      cell = '';
      if (char === '\r' && text[index + 1] === '\n') index += 1;
    } else {
      cell += char;
    }
  }

  if (quoted) throw new Error('O CSV tem aspas sem fechamento.');
  row.push(cell);
  if (row.some((value) => value.trim())) rows.push(row);
  return rows;
}

function normalizarCabecalho(value) {
  return value
    .replace(/^\uFEFF/, '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[_\s-]+/g, ' ')
    .trim();
}

function dataCsv(value) {
  const entrada = value.trim();
  let ano;
  let mes;
  let dia;
  let partes = entrada.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
  if (partes) {
    [, ano, mes, dia] = partes;
  } else {
    partes = entrada.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
    if (!partes) return null;
    [, dia, mes, ano] = partes;
  }

  const iso = `${ano}-${String(mes).padStart(2, '0')}-${String(dia).padStart(2, '0')}`;
  const date = new Date(`${iso}T00:00:00`);
  const dataValida = !Number.isNaN(date.getTime())
    && date.getFullYear() === Number(ano)
    && date.getMonth() + 1 === Number(mes)
    && date.getDate() === Number(dia);
  return dataValida ? iso : null;
}

function quantidadeCsv(value) {
  const entrada = value.trim().replace(/\s/g, '');
  const temVirgula = entrada.includes(',');
  const temPonto = entrada.includes('.');
  let normalizada = entrada;
  if (temVirgula && temPonto) {
    normalizada = entrada.lastIndexOf(',') > entrada.lastIndexOf('.')
      ? entrada.replace(/\./g, '').replace(',', '.')
      : entrada.replace(/,/g, '');
  } else if (temVirgula) {
    normalizada = entrada.replace(',', '.');
  }
  const quantidade = Number(normalizada);
  return Number.isFinite(quantidade) && quantidade > 0 ? quantidade : null;
}

function validarCsv(text) {
  const rows = parseCsv(text);
  if (rows.length < 2) throw new Error('O arquivo precisa ter cabeçalho e pelo menos uma ordenha.');
  const headers = rows[0].map(normalizarCabecalho);
  const indexOfHeader = (names) => headers.findIndex((header) => names.includes(header));
  const brincoIndex = indexOfHeader(['numero do brinco', 'brinco', 'register number']);
  const litrosIndex = indexOfHeader(['litros', 'quantidade', 'milk production']);
  const dataIndex = indexOfHeader(['data', 'date', 'production date']);

  if ([brincoIndex, litrosIndex, dataIndex].some((index) => index < 0)) {
    throw new Error('Cabeçalhos obrigatórios: numero_do_brinco, litros e data.');
  }

  return rows.slice(1).map((cells, index) => {
    const line = index + 2;
    const registerNumber = cells[brincoIndex]?.trim() || '';
    const quantity = quantidadeCsv(cells[litrosIndex] || '');
    const date = dataCsv(cells[dataIndex] || '');
    const animal = animals.value.find((item) => String(item.register_number) === registerNumber);
    const issues = [];

    if (!registerNumber) issues.push('Brinco ausente');
    else if (!animal) issues.push('Animal não encontrado');
    if (!quantity) issues.push('Litros inválidos');
    if (!date) issues.push('Data inválida');

    return {
      line,
      registerNumber,
      animal,
      quantity,
      date,
      displayDate: date ? formatarData(date) : cells[dataIndex]?.trim(),
      displayQuantity: quantity ? `${formatarNumero(quantity)} L` : cells[litrosIndex]?.trim(),
      error: issues.join(' · '),
    };
  });
}

async function selecionarArquivo(event) {
  const input = event.currentTarget;
  const file = input.files?.[0];
  limparImportacao();
  if (!file) return;
  input.value = '';
  csvFileName.value = file.name;
  if (!/\.csv$/i.test(file.name)) {
    csvError.value = 'Selecione um arquivo com extensão .csv.';
    return;
  }

  try {
    csvRows.value = validarCsv(await file.text());
  } catch (error) {
    csvError.value = error instanceof Error ? error.message : 'Não foi possível ler o arquivo CSV.';
  }
}

function limparImportacao() {
  csvFileName.value = '';
  csvError.value = '';
  csvRows.value = [];
  importMessage.value = '';
  importSuccess.value = false;
  importProgress.value = 0;
}

const csvInvalidRows = computed(() => csvRows.value.filter((row) => row.error));

async function importarOrdenhas() {
  if (!csvRows.value.length || csvInvalidRows.value.length) return;
  importing.value = true;
  importProgress.value = 0;
  let importadas = 0;
  const falhas = [];

  for (const row of csvRows.value) {
    try {
      await api.post('milk_production_history/', {
        animal: row.animal.id,
        milk_production: row.quantity,
        production_date: row.date,
      });
      importadas += 1;
    } catch (error) {
      console.error(`Erro ao importar ordenha da linha ${row.line}:`, error);
      falhas.push(row.line);
    } finally {
      importProgress.value += 1;
    }
  }

  importSuccess.value = falhas.length === 0;
  importMessage.value = falhas.length
    ? `${importadas} de ${csvRows.value.length} registros importados. Falha nas linhas ${falhas.join(', ')}.`
    : `${importadas} ordenhas importadas com sucesso.`;

  if (importadas) await carregarDados();
  importing.value = false;
}

function baixarModelo() {
  const csv = `\uFEFFnumero_do_brinco,litros,data\r\n1090,15.5,${dataLocalHoje()}\r\n`;
  const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'modelo-ordenhas.csv';
  link.click();
  URL.revokeObjectURL(url);
}

onMounted(() => {
  document.addEventListener('pointerdown', aoClicarFora);
  carregarDados();
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
.milk-metric { display: flex; align-items: center; gap: 13px; padding: 17px; }
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
.milk-metric > div { display: grid; gap: 4px; min-width: 0; }
.milk-metric__label { color: var(--text-3); font-size: var(--fs-xs); }
.milk-metric strong { color: var(--text); font-size: 1.35rem; line-height: 1.2; }
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
