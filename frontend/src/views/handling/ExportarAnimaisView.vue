<template>
  <AppShell>
    <div class="page page--wide">
      <PageHeader
        :titulo="`Exportar ${tipoLabel.toLowerCase()}`"
        descricao="Escolha os dados, o estábulo e os campos que deseja incluir no CSV."
        voltar-rotulo="Painel"
        voltar-para="/dashboard-adm"
      />

      <p v-if="error" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ error }}</span>
      </p>

      <section class="card export-panel">
        <div class="card__body stack">
          <div class="grid grid--2">
            <div class="field">
              <label class="field__label" for="tipo-exportacao">O que deseja exportar?</label>
              <select id="tipo-exportacao" v-model="selectedType" class="select" :disabled="loading || exporting" @change="changeType">
                <option value="animais">Animais</option>
                <option value="ordenha">Ordenha</option>
                <option value="pesagem">Pesagem</option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="estabulo-exportacao">Estábulo atual</label>
              <select id="estabulo-exportacao" v-model="quadrantId" class="select" :disabled="loading || exporting">
                <option value="all">Todos os estábulos</option>
                <option v-for="quadrant in quadrants" :key="quadrant.id" :value="String(quadrant.id)">
                  {{ quadrant.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="export-fields-head">
            <div>
              <h2 class="card__title">Campos do arquivo</h2>
              <p class="card__desc">Marque apenas as informações necessárias.</p>
            </div>
            <span class="badge">{{ selectedFields.length }} de {{ fields.length }} selecionados</span>
          </div>

          <div class="export-tools">
            <label class="export-search">
              <AppIcon name="search" :size="15" />
              <input v-model="fieldSearch" type="search" class="export-search__input" placeholder="Filtrar campos">
            </label>
            <div class="row">
              <button type="button" class="btn btn--sm" :disabled="loading || exporting" @click="selectVisible">Selecionar exibidos</button>
              <button type="button" class="btn btn--sm" :disabled="loading || exporting" @click="selectedFields = []">Limpar</button>
            </div>
          </div>

          <div v-if="loading" class="loading">
            <span class="spinner" aria-hidden="true"></span>
            Carregando opções...
          </div>

          <div v-else-if="!fields.length" class="empty">
            <p class="empty__desc">Não há campos disponíveis para este tipo de exportação.</p>
          </div>

          <div v-else class="export-groups">
            <details v-for="group in visibleGroups" :key="group.name" class="export-group" :open="Boolean(fieldSearch) || group.name === 'Identificação'">
              <summary class="export-group__summary">
                <span>{{ group.name }}</span>
                <span class="text-muted">{{ countSelected(group.fields) }}/{{ group.fields.length }}</span>
              </summary>
              <div class="export-group__fields">
                <label v-for="field in group.fields" :key="field.key" class="export-field">
                  <input v-model="selectedFields" type="checkbox" :value="field.key" :disabled="exporting">
                  <span>{{ field.label }}</span>
                </label>
              </div>
            </details>
            <p v-if="!visibleGroups.length" class="text-muted">Nenhum campo corresponde à busca.</p>
          </div>
        </div>

        <footer class="card__foot row--between export-footer">
          <span class="text-muted">A exportação contém {{ selectedFields.length }} campo(s).</span>
          <button type="button" class="btn btn--primary" :disabled="loading || exporting || selectedFields.length === 0" @click="exportCsv">
            <AppIcon name="download" :size="15" />
            {{ exporting ? 'Gerando CSV...' : 'Baixar CSV' }}
          </button>
        </footer>
      </section>
    </div>
  </AppShell>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { apiErrorMessage } from '@/utils/apiError';
import { idRelacao, ultimaMovimentacaoPorAnimal } from '@/utils/animalMovementUtils';

const route = useRoute();
const router = useRouter();
const quadrants = ref([]);
const quadrantId = ref('all');
const loading = ref(true);
const exporting = ref(false);
const error = ref('');
const fieldSearch = ref('');
const selectedFields = ref([]);
const animalFields = ref([]);
const selectedType = ref(validType(route.query.tipo));
const tipoLabel = computed(() => ({ animais: 'Animais', ordenha: 'Ordenha', pesagem: 'Pesagem' })[selectedType.value]);

const historyFields = {
  ordenha: [
    { key: 'id', label: 'ID do registro', group: 'Identificação' },
    { key: 'animal_id', label: 'ID do animal', group: 'Identificação' },
    { key: 'animal_name', label: 'Nome do animal', group: 'Identificação' },
    { key: 'register_number', label: 'Número de registro', group: 'Identificação' },
    { key: 'production_date', label: 'Data da ordenha', group: 'Medição' },
    { key: 'milk_production', label: 'Produção (litros)', group: 'Medição' },
    { key: 'start_time', label: 'Início', group: 'Medição' },
    { key: 'end_time', label: 'Fim', group: 'Medição' },
  ],
  pesagem: [
    { key: 'id', label: 'ID do registro', group: 'Identificação' },
    { key: 'animal_id', label: 'ID do animal', group: 'Identificação' },
    { key: 'animal_name', label: 'Nome do animal', group: 'Identificação' },
    { key: 'register_number', label: 'Número de registro', group: 'Identificação' },
    { key: 'weighing_date', label: 'Data da pesagem', group: 'Medição' },
    { key: 'weight', label: 'Peso (kg)', group: 'Medição' },
  ],
};

function validType(type) {
  return ['animais', 'ordenha', 'pesagem'].includes(type) ? type : 'animais';
}

function listFromResponse(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  throw new Error('A API retornou um formato de lista inesperado.');
}

async function fetchAll(endpoint) {
  const rows = [];
  let url = endpoint;
  while (url) {
    const response = await api.get(url);
    if (Array.isArray(response.data)) {
      rows.push(...response.data);
      break;
    }
    if (!Array.isArray(response.data?.results)) throw new Error('A API retornou uma lista em formato inesperado.');
    rows.push(...response.data.results);
    url = response.data.next;
  }
  return rows;
}

async function loadOptions(type = selectedType.value) {
  loading.value = true;
  error.value = '';
  selectedFields.value = [];
  fieldSearch.value = '';
  try {
    const [quadrantResponse, fieldsResponse] = await Promise.all([
      api.getQuadrants(),
      type === 'animais' ? api.get('animals/export-fields/') : Promise.resolve(null),
    ]);
    quadrants.value = listFromResponse(quadrantResponse.data);
    if (type === 'animais') {
      animalFields.value = listFromResponse(fieldsResponse.data).map((field) => ({ ...field, group: animalFieldGroup(field.key) }));
      selectedFields.value = animalFields.value.map((field) => field.key);
    } else {
      selectedFields.value = historyFields[type].map((field) => field.key);
    }
  } catch (loadError) {
    console.error('Erro ao carregar configuração da exportação:', loadError);
    error.value = apiErrorMessage(loadError, 'Não foi possível carregar as opções de exportação.');
  } finally {
    loading.value = false;
  }
}

function animalFieldGroup(key) {
  if (['id', 'name', 'register_number', 'status', 'reproductive_status', 'score'].includes(key)) return 'Identificação';
  if (key.startsWith('breed_')) return 'Raça';
  if (key.startsWith('birth_')) return 'Nascimento';
  if (key.includes('quadrant') || key.includes('movement')) return 'Localização e movimentação';
  if (key.includes('weight') || key.includes('weighing')) return 'Pesagens';
  if (key.includes('milk') || key.includes('milking')) return 'Ordenha';
  if (key.includes('vaccin')) return 'Vacinação';
  if (key.includes('feed')) return 'Alimentação';
  if (key.includes('health')) return 'Saúde';
  if (key.includes('insemination')) return 'Reprodução';
  return 'Outros dados';
}

const fields = computed(() => selectedType.value === 'animais' ? animalFields.value : historyFields[selectedType.value]);
const visibleGroups = computed(() => {
  const search = fieldSearch.value.trim().toLocaleLowerCase('pt-BR');
  const groups = new Map();
  for (const field of fields.value) {
    if (search && !field.label.toLocaleLowerCase('pt-BR').includes(search)) continue;
    if (!groups.has(field.group)) groups.set(field.group, []);
    groups.get(field.group).push(field);
  }
  return [...groups].map(([name, groupFields]) => ({ name, fields: groupFields }));
});

function countSelected(groupFields) {
  return groupFields.filter((field) => selectedFields.value.includes(field.key)).length;
}

function selectVisible() {
  const selected = new Set(selectedFields.value);
  visibleGroups.value.flatMap((group) => group.fields).forEach((field) => selected.add(field.key));
  selectedFields.value = [...selected];
}

function changeType() {
  router.replace({ query: { ...route.query, tipo: selectedType.value } });
  loadOptions(selectedType.value);
}

watch(() => route.query.tipo, (type) => {
  const nextType = validType(type);
  if (selectedType.value !== nextType) {
    selectedType.value = nextType;
    loadOptions(nextType);
  }
});

function downloadCsv(filename, rows) {
  const csv = `\uFEFF${rows.map((row) => row.map(csvValue).join(',')).join('\r\n')}`;
  const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8;' }));
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function csvValue(value) {
  const text = value === null || value === undefined ? '' : String(value);
  return `"${text.replace(/"/g, '""')}"`;
}

async function exportAnimals() {
  const response = await api.get('animals/export/', {
    params: { quadrant_id: quadrantId.value, fields: selectedFields.value.join(',') },
    responseType: 'blob',
  });
  const disposition = response.headers['content-disposition'] || '';
  const filename = disposition.match(/filename="?([^";]+)"?/i)?.[1] || 'animais.csv';
  const url = URL.createObjectURL(response.data);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function exportHistory() {
  const endpoint = selectedType.value === 'ordenha' ? 'milk_production_history/' : 'weight_history/';
  const [records, animals, movements] = await Promise.all([
    fetchAll(endpoint),
    fetchAll('animals/'),
    quadrantId.value === 'all' ? Promise.resolve([]) : fetchAll('animal_movements/'),
  ]);
  const animalById = new Map(animals.map((animal) => [String(animal.id), animal]));
  const latestMovement = ultimaMovimentacaoPorAnimal(movements);
  const selectedRecords = records.filter((record) => {
    if (quadrantId.value === 'all') return true;
    const animalId = idRelacao(record.animal);
    return String(idRelacao(latestMovement.get(String(animalId))?.quadrant)) === quadrantId.value;
  });
  const header = selectedFields.value.map((key) => fields.value.find((field) => field.key === key)?.label || key);
  const rows = selectedRecords.map((record) => selectedFields.value.map((key) => {
    const animalId = idRelacao(record.animal);
    const animal = animalById.get(String(animalId));
    if (key === 'animal_id') return animalId;
    if (key === 'animal_name') return animal?.name;
    if (key === 'register_number') return animal?.register_number;
    return record[key];
  }));
  downloadCsv(`${selectedType.value}.csv`, [header, ...rows]);
}

async function exportCsv() {
  if (exporting.value || selectedFields.value.length === 0) return;
  exporting.value = true;
  error.value = '';
  try {
    if (selectedType.value === 'animais') await exportAnimals();
    else await exportHistory();
  } catch (requestError) {
    console.error('Erro ao exportar dados:', requestError);
    error.value = await exportErrorMessage(requestError);
  } finally {
    exporting.value = false;
  }
}

async function exportErrorMessage(requestError) {
  const data = requestError?.response?.data;
  if (data instanceof Blob) {
    try {
      const parsed = JSON.parse(await data.text());
      if (parsed.detail) return parsed.detail;
    } catch (parseError) {
      console.error('Não foi possível interpretar o erro da exportação:', parseError);
    }
  }
  return apiErrorMessage(requestError, 'Não foi possível gerar o CSV.');
}

onMounted(() => loadOptions());
</script>

<style scoped>
.export-panel { max-width: 100%; }
.export-fields-head,
.export-tools {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.export-fields-head { padding-top: 6px; border-top: 1px solid var(--line); }
.export-tools { flex-wrap: wrap; }
.export-search {
  display: flex;
  align-items: center;
  gap: 8px;
  width: min(100%, 340px);
  height: 36px;
  padding: 0 10px;
  border: 1px solid var(--line-strong);
  border-radius: var(--r);
  color: var(--text-3);
}

.export-search__input {
  width: 100%;
  border: 0;
  outline: 0;
  background: transparent;
  color: var(--text);
  font: inherit;
}

.export-groups { display: grid; gap: 8px; }
.export-group { border: 1px solid var(--line); border-radius: var(--r); }
.export-group__summary {
  display: flex;
  justify-content: space-between;
  padding: 11px 13px;
  cursor: pointer;
  font-size: var(--fs-sm);
  font-weight: 600;
  list-style-position: inside;
}

.export-group__fields {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 4px 12px;
  padding: 0 13px 12px 30px;
}

.export-field {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  padding: 5px 0;
  color: var(--text-2);
  font-size: var(--fs-sm);
}

.export-footer { justify-content: space-between; flex-wrap: wrap; }

@media (max-width: 720px) {
  .export-group__fields { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 520px) {
  .export-fields-head,
  .export-tools { align-items: flex-start; flex-direction: column; }
  .export-search { width: 100%; }
  .export-group__fields { grid-template-columns: 1fr; }
}
</style>
