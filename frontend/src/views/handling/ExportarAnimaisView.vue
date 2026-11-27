<template>
  <AppShell>
    <div class="page page--wide">
      <PageHeader
        titulo="Exportação / Importação"
        descricao="Exporte relatórios em CSV ou importe planilhas de vacas e ordenhas em um só lugar."
        voltar-rotulo="Painel"
        voltar-para="/dashboard-adm"
      />

      <AppTabs
        v-model="abaAtiva"
        :tabs="abas"
        label="Exportação e importação"
        id-base="export-import"
      />

      <p v-if="error" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ error }}</span>
      </p>

      <section
        v-if="abaAtiva === 'exportar'"
        id="export-import-panel-exportar"
        role="tabpanel"
        aria-labelledby="export-import-tab-exportar"
        class="card export-panel"
      >
        <div class="card__body stack">
          <div class="export-section-head">
            <div>
              <h2 class="card__title">Filtros básicos</h2>
              <p class="card__desc">Defina o tipo de dado e o estábulo da exportação.</p>
            </div>
          </div>
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

          <details class="export-advanced">
            <summary class="export-advanced__summary">
              <span>
                <strong>Opções avançadas</strong>
                <span class="text-muted"> — campos e personalização do CSV</span>
              </span>
              <span class="badge">{{ selectedFields.length }} campo(s)</span>
            </summary>
            <div class="export-advanced__content stack">
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
                  <input v-model="fieldSearch" type="search" class="export-search__input" placeholder="Filtrar campos" aria-label="Filtrar campos">
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

              <details class="export-layout">
                <summary class="export-layout__summary">Personalizar ordem, rótulos e layouts salvos</summary>
                <div class="export-layout__content">
                  <header class="export-fields-head">
                    <div>
                      <h2 class="card__title">Ordem e rótulos das colunas</h2>
                      <p class="card__desc">A ordem abaixo será usada no CSV; os rótulos são personalizados neste navegador.</p>
                    </div>
                  </header>

                  <div v-if="!selectedFields.length" class="empty">
                    <p class="empty__desc">Selecione campos para organizar as colunas.</p>
                  </div>
                  <ol v-else class="export-layout__fields">
                    <li v-for="(key, index) in selectedFields" :key="key" class="export-layout__field">
                      <span class="export-layout__default">{{ defaultFieldLabel(key) }}</span>
                      <label class="export-layout__label">
                        <span class="sr-only">Rótulo para {{ defaultFieldLabel(key) }}</span>
                        <input v-model="customLabels[key]" class="input" type="text" maxlength="80" :placeholder="defaultFieldLabel(key)">
                      </label>
                      <div class="row">
                        <button type="button" class="btn btn--sm" :disabled="index === 0" :aria-label="`Mover ${defaultFieldLabel(key)} para cima`" @click="moveField(index, -1)">↑</button>
                        <button type="button" class="btn btn--sm" :disabled="index === selectedFields.length - 1" :aria-label="`Mover ${defaultFieldLabel(key)} para baixo`" @click="moveField(index, 1)">↓</button>
                      </div>
                    </li>
                  </ol>

                  <div class="grid grid--2 export-layout__saved">
                    <div class="field">
                      <label class="field__label" for="layout-name">Nome do layout</label>
                      <input id="layout-name" v-model="layoutName" class="input" type="text" maxlength="80" placeholder="Ex.: Rebanho mensal">
                    </div>
                    <div class="field">
                      <label class="field__label" for="saved-layout">Layouts salvos neste navegador</label>
                      <select id="saved-layout" v-model="selectedLayoutId" class="select">
                        <option value="">Selecione um layout...</option>
                        <option v-for="layout in layoutsForType" :key="layout.id" :value="layout.id">
                          {{ layout.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <div class="row export-layout__actions">
                    <button type="button" class="btn btn--sm" :disabled="!layoutName.trim() || !selectedFields.length" @click="saveLayout">
                      {{ selectedLayoutId ? 'Atualizar layout' : 'Salvar layout' }}
                    </button>
                    <button type="button" class="btn btn--sm" :disabled="!selectedLayoutId" @click="applyLayout">Aplicar</button>
                    <button type="button" class="btn btn--sm btn--danger" :disabled="!selectedLayoutId" @click="deleteLayout">Excluir</button>
                  </div>
                  <p v-if="layoutError" class="alert alert--danger" role="alert">
                    <AppIcon name="alert" :size="16" />
                    <span>{{ layoutError }}</span>
                  </p>

                  <div class="export-preview" aria-label="Prévia do cabeçalho do CSV">
                    <strong>Prévia do cabeçalho</strong>
                    <div class="table-wrap">
                      <table class="table">
                        <thead>
                          <tr><th v-for="key in selectedFields" :key="key">{{ fieldLabel(key) }}</th></tr>
                        </thead>
                        <tbody>
                          <tr><td :colspan="selectedFields.length || 1" class="text-muted">Os registros serão carregados na geração do arquivo.</td></tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                  <p class="text-muted">Layouts ficam salvos apenas neste navegador; não são compartilhados nem enviados ao servidor.</p>
                </div>
              </details>
            </div>
          </details>
        </div>

        <footer class="card__foot row--between export-footer">
          <span class="text-muted">A exportação contém {{ selectedFields.length }} campo(s).</span>
          <button type="button" class="btn btn--primary" :disabled="loading || exporting || selectedFields.length === 0" @click="exportCsv">
            <AppIcon name="download" :size="15" />
            {{ exporting ? 'Gerando CSV...' : 'Baixar CSV' }}
          </button>
        </footer>
      </section>

      <section
        v-else
        id="export-import-panel-importar"
        role="tabpanel"
        aria-labelledby="export-import-tab-importar"
        class="card export-panel"
      >
        <div class="card__body stack">
          <div class="export-section-head">
            <div>
              <h2 class="card__title">Importar planilha Excel (.xlsx)</h2>
              <p class="card__desc">Baixe o modelo padrão, preencha os dados e envie o arquivo para importar em lote.</p>
            </div>
          </div>

          <div class="grid grid--2">
            <div class="field">
              <label class="field__label" for="tipo-importacao">O que deseja importar?</label>
              <select id="tipo-importacao" v-model="importType" class="select" :disabled="importing">
                <option value="vacas">Animais (vacas)</option>
                <option value="ordenhas">Ordenhas (produção de leite)</option>
              </select>
            </div>

            <div class="field">
              <label class="field__label">Planilha modelo</label>
              <div>
                <button type="button" class="btn" :disabled="downloadingTemplate || importing" @click="downloadTemplate">
                  <AppIcon name="download" :size="15" />
                  {{ downloadingTemplate ? 'Baixando modelo...' : `Baixar modelo de ${importType === 'vacas' ? 'animais' : 'ordenhas'} (.xlsx)` }}
                </button>
              </div>
            </div>
          </div>

          <label class="import-dropzone" :class="{ 'import-dropzone--loaded': importFileName }">
            <input
              ref="importFileInput"
              type="file"
              accept=".xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
              :disabled="importing"
              @change="onSelectImportFile"
            >
            <AppIcon :name="importFileName ? 'check-circle' : 'upload'" :size="24" />
            <strong>{{ importFileName || 'Escolha uma planilha .xlsx' }}</strong>
            <span>Clique para selecionar o arquivo no computador</span>
          </label>

          <p v-if="importError" class="alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ importError }}</span>
          </p>
          <p v-if="importSuccess" class="alert alert--ok" role="status">
            <AppIcon name="check-circle" :size="16" />
            <span>{{ importSuccess }}</span>
          </p>
        </div>

        <footer class="card__foot row--between export-footer">
          <span class="text-muted">Formato aceito: planilha Excel (.xlsx) no modelo do sistema.</span>
          <button
            type="button"
            class="btn btn--primary"
            :disabled="importing || !importFile"
            @click="submitImport"
          >
            <AppIcon name="upload" :size="15" />
            {{ importing ? 'Importando...' : 'Importar planilha' }}
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
import { confirmar } from '@/services/confirmService';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppTabs from '@/components/ui/AppTabs.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { apiErrorMessage } from '@/utils/apiError';
import { idRelacao, ultimaMovimentacaoPorAnimal } from '@/utils/animalMovementUtils';

const route = useRoute();
const router = useRouter();
const abaAtiva = ref(route.query.aba === 'importar' ? 'importar' : 'exportar');
const abas = [
  { id: 'exportar', label: 'Exportar', icon: 'download' },
  { id: 'importar', label: 'Importar', icon: 'upload' },
];
const importType = ref('vacas');
const importFile = ref(null);
const importFileName = ref('');
const importFileInput = ref(null);
const importing = ref(false);
const downloadingTemplate = ref(false);
const importError = ref('');
const importSuccess = ref('');
const quadrants = ref([]);
const quadrantId = ref('all');
const loading = ref(true);
const exporting = ref(false);
const error = ref('');
const fieldSearch = ref('');
const selectedFields = ref([]);
const animalFields = ref([]);
const selectedType = ref(validType(route.query.tipo));
const savedLayouts = ref([]);
const selectedLayoutId = ref('');
const layoutName = ref('');
const customLabels = ref({});
const layoutError = ref('');
const LAYOUTS_STORAGE_KEY = 'ls-management-export-layouts';
const tipoLabel = computed(() => ({ animais: 'Animais', ordenha: 'Ordenha', pesagem: 'Pesagem' })[selectedType.value]);
const layoutsForType = computed(() => savedLayouts.value.filter((layout) => layout.type === selectedType.value));
const selectedLayout = computed(() => layoutsForType.value.find((layout) => layout.id === selectedLayoutId.value) || null);

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
  selectedLayoutId.value = '';
  layoutName.value = '';
  customLabels.value = {};
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

function defaultFieldLabel(key) {
  return fields.value.find((field) => field.key === key)?.label || key;
}

function fieldLabel(key) {
  return String(customLabels.value[key] || '').trim() || defaultFieldLabel(key);
}

function moveField(index, offset) {
  const nextIndex = index + offset;
  if (nextIndex < 0 || nextIndex >= selectedFields.value.length) return;
  const reordered = [...selectedFields.value];
  [reordered[index], reordered[nextIndex]] = [reordered[nextIndex], reordered[index]];
  selectedFields.value = reordered;
}

function loadLayouts() {
  layoutError.value = '';
  try {
    const stored = localStorage.getItem(LAYOUTS_STORAGE_KEY);
    const parsed = stored ? JSON.parse(stored) : [];
    if (!Array.isArray(parsed)) throw new Error('O conteúdo salvo não é uma lista de layouts.');
    savedLayouts.value = parsed.filter((layout) =>
      layout && typeof layout.id === 'string' && typeof layout.name === 'string'
      && Array.isArray(layout.fields) && typeof layout.type === 'string'
    );
  } catch (loadError) {
    console.error('Não foi possível carregar os layouts locais de exportação:', loadError);
    layoutError.value = 'Não foi possível carregar os layouts deste navegador.';
  }
}

function persistLayouts(layouts) {
  try {
    localStorage.setItem(LAYOUTS_STORAGE_KEY, JSON.stringify(layouts));
    savedLayouts.value = layouts;
    return true;
  } catch (saveError) {
    console.error('Não foi possível salvar os layouts locais de exportação:', saveError);
    layoutError.value = 'Não foi possível salvar o layout neste navegador.';
    return false;
  }
}

function saveLayout() {
  const name = layoutName.value.trim();
  if (!name || !selectedFields.value.length) return;
  layoutError.value = '';
  const id = selectedLayout.value?.id || `layout-${Date.now()}`;
  const layout = {
    id,
    name,
    type: selectedType.value,
    fields: [...selectedFields.value],
    labels: { ...customLabels.value },
    quadrantId: quadrantId.value,
  };
  const layouts = [
    ...savedLayouts.value.filter((item) => item.id !== id),
    layout,
  ];
  if (persistLayouts(layouts)) selectedLayoutId.value = id;
}

function applyLayout() {
  const layout = selectedLayout.value;
  if (!layout) return;
  const validKeys = new Set(fields.value.map((field) => field.key));
  selectedFields.value = layout.fields.filter((key) => validKeys.has(key));
  customLabels.value = { ...layout.labels };
  quadrantId.value = layout.quadrantId || 'all';
  layoutName.value = layout.name;
}

async function deleteLayout() {
  if (!selectedLayout.value) return;
  const confirmed = await confirmar({
    titulo: 'Excluir layout de exportação?',
    texto: `O layout “${selectedLayout.value.name}” será removido deste navegador.`,
    acao: 'Excluir layout',
  });
  if (!confirmed) return;
  layoutError.value = '';
  if (persistLayouts(savedLayouts.value.filter((item) => item.id !== selectedLayout.value.id))) {
    selectedLayoutId.value = '';
    layoutName.value = '';
  }
}

async function exportAnimals() {
  const response = await api.get('animals/export/', {
    params: { quadrant_id: quadrantId.value, fields: selectedFields.value.join(',') },
    responseType: 'blob',
  });
  const disposition = response.headers['content-disposition'] || '';
  const filename = disposition.match(/filename="?([^";]+)"?/i)?.[1] || 'animais.csv';
  const content = await response.data.text();
  const headerEnd = content.indexOf('\n');
  const rest = headerEnd >= 0 ? content.slice(headerEnd + 1) : '';
  const bom = content.startsWith('\uFEFF') ? '\uFEFF' : '';
  const csv = `${bom}${selectedFields.value.map((key) => csvValue(fieldLabel(key))).join(',')}\r\n${rest}`;
  const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8;' }));
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
  const header = selectedFields.value.map(fieldLabel);
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

function onSelectImportFile(event) {
  const file = event.target?.files?.[0] || null;
  importFile.value = file;
  importFileName.value = file ? file.name : '';
  importError.value = '';
  importSuccess.value = '';
}

async function downloadTemplate() {
  downloadingTemplate.value = true;
  importError.value = '';
  try {
    const endpoint = importType.value === 'vacas' ? 'api/importacao/vacas/' : 'api/importacao/ordenhas/';
    const response = await api.get(endpoint, { responseType: 'blob' });
    const url = URL.createObjectURL(response.data);
    const link = document.createElement('a');
    link.href = url;
    link.download = `modelo_importacao_${importType.value}.xlsx`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  } catch (err) {
    console.error('Erro ao baixar modelo:', err);
    importError.value = apiErrorMessage(err, 'Não foi possível baixar a planilha modelo.');
  } finally {
    downloadingTemplate.value = false;
  }
}

async function submitImport() {
  if (!importFile.value || importing.value) return;
  importing.value = true;
  importError.value = '';
  importSuccess.value = '';
  try {
    const formData = new FormData();
    formData.append('arquivo', importFile.value);
    const endpoint = importType.value === 'vacas' ? 'api/importacao/vacas/' : 'api/importacao/ordenhas/';
    const response = await api.post(endpoint, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    const data = response.data || {};
    importSuccess.value = data.mensagem || data.detail || 'Planilha importada com sucesso.';
    importFile.value = null;
    importFileName.value = '';
    if (importFileInput.value) importFileInput.value.value = '';
  } catch (err) {
    console.error('Erro ao importar planilha:', err);
    importError.value = apiErrorMessage(err, 'Não foi possível importar a planilha. Verifique o formato e tente novamente.');
  } finally {
    importing.value = false;
  }
}

onMounted(async () => {
  await loadOptions();
  loadLayouts();
});
</script>

<style scoped>
.export-panel { max-width: 100%; }
.export-section-head { padding-bottom: 4px; }
.export-advanced { border: 1px solid var(--line); border-radius: var(--r); }
.export-advanced__summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 13px;
  cursor: pointer;
  list-style-position: inside;
}
.export-advanced__content { padding: 0 13px 13px; }
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
.export-layout { border-top: 1px solid var(--line); }
.export-layout__summary { padding: 12px 0; cursor: pointer; font-size: var(--fs-sm); font-weight: 600; }
.export-layout__content { display: grid; gap: 12px; padding: 0 0 4px; }
.export-layout__fields { display: grid; gap: 8px; margin: 0; padding: 0; list-style: none; }
.export-layout__field { display: grid; grid-template-columns: minmax(120px, 0.8fr) minmax(180px, 1fr) auto; align-items: center; gap: 10px; }
.export-layout__default { color: var(--text-2); font-size: var(--fs-sm); }
.export-layout__label { min-width: 0; }
.export-layout__actions { flex-wrap: wrap; }
.export-preview { display: grid; gap: 8px; min-width: 0; }
.export-preview .table-wrap { max-width: 100%; }

.import-dropzone {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 28px 20px;
  border: 1.5px dashed var(--line-strong);
  border-radius: var(--r-md);
  background: var(--surface-2);
  color: var(--text-2);
  text-align: center;
  cursor: pointer;
  transition: border-color var(--dur) var(--ease), background var(--dur) var(--ease);
}

.import-dropzone:hover {
  border-color: var(--accent);
  background: var(--accent-soft);
}

.import-dropzone--loaded {
  border-color: var(--ok-line);
  background: var(--ok-soft);
}

.import-dropzone input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.import-dropzone strong { color: var(--text); font-size: var(--fs-md); }
.import-dropzone span { font-size: var(--fs-xs); color: var(--text-3); }

@media (max-width: 720px) {
  .export-group__fields { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .export-layout__field { grid-template-columns: minmax(100px, 1fr) 2fr auto; }
}

@media (max-width: 520px) {
  .export-fields-head,
  .export-tools { align-items: flex-start; flex-direction: column; }
  .export-search { width: 100%; }
  .export-group__fields { grid-template-columns: 1fr; }
  .export-layout__field { grid-template-columns: 1fr auto; }
  .export-layout__default { grid-column: 1 / -1; }
}
</style>
