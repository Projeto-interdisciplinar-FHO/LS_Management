<template>
  <AppShell>
    <div class="page page--wide development">
      <PageHeader
        titulo="Desenvolvimento"
        descricao="Acompanhe a evolução de peso dos animais a partir das pesagens registradas."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <p v-if="error" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ error }}</span>
      </p>
      <p v-if="notice" class="alert alert--ok" role="status">
        <AppIcon name="check-circle" :size="16" />
        <span>{{ notice }}</span>
      </p>

      <section class="card development__selection">
        <div class="card__body development__selection-body">
          <div class="field">
            <label class="field__label" for="development-animal">Animal acompanhado</label>
            <select
              id="development-animal"
              v-model="selectedAnimalId"
              class="select"
              :disabled="loading || !animals.length"
            >
              <option value="" disabled>Selecione um animal...</option>
              <option v-for="animal in animals" :key="animal.id" :value="String(animal.id)">
                {{ animal.name || 'Sem nome' }} · #{{ animal.register_number }}
              </option>
            </select>
          </div>
          <div v-if="selectedAnimal" class="development__animal-facts">
            <span><small>Nascimento</small><strong>{{ birthDate ? formatDate(birthDate) : 'Não informado' }}</strong></span>
            <span><small>Pesagens</small><strong>{{ selectedWeights.length }}</strong></span>
            <span><small>Último peso</small><strong>{{ latestWeight ? `${latestWeight.weight} kg` : 'Sem registro' }}</strong></span>
          </div>
          <span v-else-if="loading" class="text-muted" role="status">Carregando animais...</span>
          <span v-else-if="!animals.length" class="text-muted">Nenhum animal cadastrado.</span>
        </div>
      </section>

      <div v-if="selectedAnimal" class="development__content">
        <section class="card development__chart-card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Curva de desenvolvimento</h2>
              <p class="card__desc">Histórico real de pesagens para {{ selectedAnimal.name || 'este animal' }}.</p>
            </div>
            <span v-if="weightChange !== null" class="badge" :class="weightChange >= 0 ? 'badge--ok' : 'badge--warn'">
              {{ weightChange > 0 ? '+' : '' }}{{ formatNumber(weightChange) }} kg desde a pesagem anterior
            </span>
          </header>
          <div v-if="loadingWeights" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando histórico...</div>
          <div v-else-if="!selectedWeights.length" class="empty">
            <AppIcon name="chart" :size="28" />
            <p class="empty__title">Sem pesagens para exibir</p>
            <p class="empty__desc">Registre uma pesagem para iniciar o acompanhamento deste animal.</p>
          </div>
          <div v-else class="development__chart">
            <Line :data="chartData" :options="chartOptions" aria-label="Curva de peso do animal" />
          </div>
        </section>

        <section class="card development__entry-card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Registrar pesagem</h2>
              <p class="card__desc">O novo registro será vinculado ao animal selecionado.</p>
            </div>
            <span class="icon-tile icon-tile--accent"><AppIcon name="scale" :size="17" /></span>
          </header>
          <form class="card__body stack" @submit.prevent="saveWeight">
            <div class="field">
              <label class="field__label" for="development-date">Data da pesagem</label>
              <input id="development-date" v-model="form.weighing_date" class="input" type="date" required :disabled="saving">
            </div>
            <div class="field">
              <label class="field__label" for="development-weight">Peso (kg)</label>
              <input
                id="development-weight"
                v-model.number="form.weight"
                class="input"
                type="number"
                min="0.01"
                step="0.01"
                placeholder="Ex.: 485.50"
                required
                :disabled="saving"
              >
            </div>
            <footer class="row row--between">
              <span class="text-muted">Animal #{{ selectedAnimal.register_number }}</span>
              <button type="submit" class="btn btn--primary" :disabled="saving || !form.weight">
                {{ saving ? 'Salvando...' : 'Salvar pesagem' }}
              </button>
            </footer>
          </form>
        </section>
      </div>

      <section v-if="selectedAnimal" class="card development__history">
        <header class="card__head">
          <div>
            <h2 class="card__title">Histórico de pesagens</h2>
            <p class="card__desc">Registros vinculados a #{{ selectedAnimal.register_number }}.</p>
          </div>
          <span class="badge">{{ selectedWeights.length }}</span>
        </header>
        <div v-if="!loadingWeights && !selectedWeights.length" class="empty">
          <p class="empty__desc">As pesagens registradas serão exibidas nesta lista.</p>
        </div>
        <div v-else-if="loadingWeights" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando pesagens...</div>
        <div v-else class="table-wrap">
          <table class="table">
            <thead><tr><th>Data</th><th>Peso</th></tr></thead>
            <tbody>
              <tr v-for="record in selectedWeightsNewestFirst" :key="record.id">
                <td class="mono nowrap">{{ formatDate(record.weighing_date) }}</td>
                <td class="mono cell-strong">{{ formatNumber(record.weight) }} kg</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </AppShell>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
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
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { painelDoPapel } from '@/services/auth';
import { idRelacao } from '@/utils/animalMovementUtils';
import { apiErrorMessage } from '@/utils/apiError';

ChartJS.register(CategoryScale, LinearScale, LineController, LineElement, PointElement, Tooltip);

const painel = computed(() => painelDoPapel());
const animals = ref([]);
const births = ref([]);
const weights = ref([]);
const selectedAnimalId = ref('');
const loading = ref(true);
const loadingWeights = ref(false);
const saving = ref(false);
const error = ref('');
const notice = ref('');
const form = ref({ weighing_date: todayIso(), weight: null });

const selectedAnimal = computed(() =>
  animals.value.find((animal) => String(animal.id) === selectedAnimalId.value) || null
);
const birthDate = computed(() => {
  const birthId = idRelacao(selectedAnimal.value?.birth);
  return births.value.find((birth) => String(birth.id) === String(birthId))?.date || null;
});
const selectedWeights = computed(() => weights.value
  .filter((record) => String(idRelacao(record.animal)) === selectedAnimalId.value)
  .sort((a, b) => String(a.weighing_date).localeCompare(String(b.weighing_date)))
);
const selectedWeightsNewestFirst = computed(() => [...selectedWeights.value].reverse());
const latestWeight = computed(() => selectedWeightsNewestFirst.value[0] || null);
const weightChange = computed(() => {
  if (selectedWeights.value.length < 2) return null;
  const current = Number(selectedWeights.value.at(-1).weight);
  const previous = Number(selectedWeights.value.at(-2).weight);
  return Number.isFinite(current - previous) ? current - previous : null;
});

function todayIso() {
  const date = new Date();
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

function listFromResponse(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  throw new Error('A API retornou um formato de lista inesperado.');
}

async function consultarTodos(endpoint) {
  let url = endpoint;
  const items = [];
  const pages = new Set();
  while (url) {
    if (pages.has(url)) throw new Error(`A paginação de ${endpoint} retornou uma página repetida.`);
    pages.add(url);
    const response = await api.get(url);
    items.push(...listFromResponse(response.data));
    url = Array.isArray(response.data) ? null : response.data.next || null;
  }
  return items;
}

function formatDate(value) {
  if (!value) return '—';
  return new Date(`${value}T00:00:00`).toLocaleDateString('pt-BR');
}

function formatNumber(value) {
  return Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
}

const chartToken = (token) => getComputedStyle(document.documentElement).getPropertyValue(token).trim();
const chartData = computed(() => ({
  labels: selectedWeights.value.map((record) => formatDate(record.weighing_date)),
  datasets: [{
    label: 'Peso (kg)',
    data: selectedWeights.value.map((record) => Number(record.weight)),
    borderColor: chartToken('--accent'),
    backgroundColor: chartToken('--accent-soft'),
    pointBackgroundColor: chartToken('--accent'),
    pointBorderColor: chartToken('--surface'),
    pointBorderWidth: 2,
    pointRadius: 4,
    pointHoverRadius: 6,
    borderWidth: 2,
    fill: true,
    tension: 0.3,
  }],
}));
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { callbacks: { label: (context) => ` ${formatNumber(context.raw)} kg` } },
  },
  scales: {
    x: { grid: { display: false }, ticks: { color: chartToken('--text-2') } },
    y: {
      beginAtZero: false,
      grid: { color: chartToken('--line') },
      ticks: { color: chartToken('--text-3'), callback: (value) => `${value} kg` },
    },
  },
}));

watch(selectedAnimalId, () => {
  error.value = '';
  notice.value = '';
});

async function loadData() {
  loading.value = true;
  error.value = '';
  try {
    const [animalsResponse, weightRecords, birthRecords] = await Promise.all([
      api.getAnimals(),
      consultarTodos('weight_history/'),
      consultarTodos('births/'),
    ]);
    animals.value = listFromResponse(animalsResponse.data);
    weights.value = weightRecords;
    births.value = birthRecords;
    if (animals.value.length) selectedAnimalId.value = String(animals.value[0].id);
  } catch (loadError) {
    console.error('Erro ao carregar o desenvolvimento dos animais:', loadError);
    error.value = apiErrorMessage(loadError, 'Não foi possível carregar os dados de desenvolvimento.');
  } finally {
    loading.value = false;
  }
}

async function saveWeight() {
  if (!selectedAnimal.value || saving.value) return;
  saving.value = true;
  error.value = '';
  notice.value = '';
  try {
    const response = await api.post('weight_history/', {
      animal: selectedAnimal.value.id,
      weight: form.value.weight,
      weighing_date: form.value.weighing_date,
    });
    weights.value = [...weights.value, response.data];
    form.value = { weighing_date: todayIso(), weight: null };
    notice.value = 'Pesagem registrada com sucesso.';
  } catch (saveError) {
    console.error('Erro ao registrar pesagem:', saveError);
    error.value = apiErrorMessage(saveError, 'Não foi possível registrar a pesagem.');
  } finally {
    saving.value = false;
  }
}

onMounted(loadData);
</script>

<style scoped>
.development__selection { margin-bottom: 16px; }
.development__selection-body { display: flex; align-items: flex-end; gap: 20px; }
.development__selection-body .field { width: min(360px, 100%); margin: 0; }
.development__animal-facts { display: flex; flex: 1; justify-content: flex-end; gap: 24px; }
.development__animal-facts span { display: grid; gap: 3px; }
.development__animal-facts small { color: var(--text-3); font-size: var(--fs-xs); }
.development__animal-facts strong { color: var(--text); font-size: var(--fs-sm); }
.development__content { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(280px, 1fr); align-items: start; gap: 16px; }
.development__chart-card,
.development__entry-card,
.development__history { min-width: 0; }
.development__chart { position: relative; height: 320px; padding: 18px; }
.development__history { margin-top: 16px; }

@media (max-width: 900px) {
  .development__content { grid-template-columns: 1fr; }
  .development__selection-body { align-items: stretch; flex-direction: column; }
  .development__selection-body .field { width: 100%; }
  .development__animal-facts { justify-content: flex-start; flex-wrap: wrap; }
}

@media (max-width: 520px) {
  .development__animal-facts { gap: 14px; }
  .development__chart { height: 250px; padding: 12px; }
}
</style>
