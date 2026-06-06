<template>
  <div :class="['ls-detail-page-container', { 'ls-dark-active': isDark }]" v-if="animal && !loading">
    <header class="ls-detail-header">
      <div class="ls-detail-nav-actions">
        <button @click="goBackToDashboard" class="ls-detail-btn-back">← Voltar para a Lista</button>
        <button @click="deleteAnimal" :disabled="deleting" class="ls-detail-btn-danger">🗑 Excluir Registro</button>
      </div>
      <div class="ls-detail-animal-title-section">
        <h1 class="ls-detail-main-title">Ficha Individual: {{ animal.name || 'Sem Nome' }}</h1>
        <span class="ls-detail-tag-brinco">Brinco #{{ animal.register_number }}</span>
      </div>
    </header>

    <!-- ABAS CONTROL -->
    <div class="ls-detail-tabs-control">
      <button 
        @click="activeTab = 'geral'" 
        :class="['ls-detail-tab-btn', 'ls-dt-tab-geral', { 'ls-dt-tab-active': activeTab === 'geral' }]"
      >
        📋 Informações Gerais
      </button>
      <button 
        v-if="showMilkTab"
        @click="activeTab = 'leite'" 
        :class="['ls-detail-tab-btn', 'ls-dt-tab-leite', { 'ls-dt-tab-active': activeTab === 'leite' }]"
      >
        🥛 Registro de Leite
      </button>
      <button 
        @click="activeTab = 'peso'" 
        :class="['ls-detail-tab-btn', 'ls-dt-tab-peso', { 'ls-dt-tab-active': activeTab === 'peso' }]"
      >
        ⚖️ Histórico de Pesos
      </button>
      <button 
        @click="activeTab = 'nutricao'" 
        :class="['ls-detail-tab-btn', 'ls-dt-tab-nutricao', { 'ls-dt-tab-active': activeTab === 'nutricao' }]"
      >
        🍽️ Registro de Alimentação
      </button>
      <button 
        @click="activeTab = 'veterinario'" 
        :class="['ls-detail-tab-btn', 'ls-dt-tab-veterinario', { 'ls-dt-tab-active': activeTab === 'veterinario' }]"
      >
        🩺 Atendimento Veterinário
      </button>
      <button 
        @click="activeTab = 'vacinas'" 
        :class="['ls-detail-tab-btn', 'ls-dt-tab-vacinas', { 'ls-dt-tab-active': activeTab === 'vacinas' }]"
      >
        ✛ Vacinas Aplicadas
      </button>
    </div>

    <div class="ls-detail-tab-content">
      
      <!-- ABA: INFORMAÇÕES GERAIS -->
      <div v-if="activeTab === 'geral'" class="ls-detail-grid-two-columns">
        
        <div class="ls-detail-data-card">
          <div class="ls-detail-card-header-inline">
            <h3 class="ls-detail-card-title">Informações do Animal</h3>
            <button @click="toggleEdit" class="ls-detail-btn-edit-toggle">
              {{ isEditing ? '📁 Cancelar' : '✎ Editar Informações' }}
            </button>
          </div>

          <div v-if="!isEditing" class="ls-detail-data-rows">
            <div class="ls-detail-data-row">
              <span class="ls-detail-label">Peso Atual</span>
              <span class="ls-detail-value ls-dt-font-bold">{{ animal.weight }} kg</span>
            </div>
            <div class="ls-detail-data-row">
              <span class="ls-detail-label">Data de Nascimento</span>
              <span class="ls-detail-value">{{ formatDate(animal.birth_date) }}</span>
            </div>
            <div class="ls-detail-data-row">
              <span class="ls-detail-label">Sexo</span>
              <span class="ls-detail-value">{{ animal.sex === 'm' || animal.sex === 'M' ? 'Macho' : 'Fêmea' }}</span>
            </div>
            <div class="ls-detail-data-row">
              <span class="ls-detail-label">Status do Rebanho</span>
              <span class="ls-detail-badge" :class="animal.active ? 'ls-dt-badge-active' : 'ls-dt-badge-inactive'">
                {{ animal.active ? 'Ativo' : 'Inativo' }}
              </span>
            </div>
          </div>

          <form v-else @submit.prevent="updateAnimalInfo" class="ls-detail-edit-form">
            <div class="ls-detail-form-group">
              <label class="ls-detail-form-label">Nome / Apelido</label>
              <input v-model="editData.name" type="text" class="ls-detail-form-input" required>
            </div>
            <div class="ls-detail-form-group">
              <label class="ls-detail-form-label">Peso (kg)</label>
              <input v-model="editData.weight" type="number" step="0.01" class="ls-detail-form-input" required>
            </div>
            <div class="ls-detail-form-group">
              <label class="ls-detail-form-label">Data de Nascimento</label>
              <input v-model="editData.birth_date" type="date" class="ls-detail-form-input" required>
            </div>
            <div class="ls-detail-form-group">
              <label class="ls-detail-form-label">Sexo</label>
              <select v-model="editData.sex" class="ls-detail-form-select">
                <option value="m">Macho</option>
                <option value="f">Fêmea</option>
              </select>
            </div>
            <div class="ls-detail-form-group">
              <label class="ls-detail-form-label">Status</label>
              <select v-model="editData.active" class="ls-detail-form-select">
                <option :value="true">Ativo</option>
                <option :value="false">Inativo</option>
              </select>
            </div>
            <button type="submit" class="ls-detail-btn-save-inside" :disabled="saving">
              {{ saving ? 'Salvando...' : '💾 Salvar Alterações' }}
            </button>
          </form>
        </div>

        <div class="ls-detail-data-card">
          <h3 class="ls-detail-card-title">Classificação e Localização</h3>
          <div class="ls-detail-data-rows">
            <div class="ls-detail-data-row">
              <span class="ls-detail-label">Espécie</span>
              <span class="ls-detail-value ls-dt-highlight-text">{{ animal.specie_name || 'Bovino' }}</span>
            </div>
            <div class="ls-detail-data-row">
              <span class="ls-detail-label">Raça</span>
              <span class="ls-detail-value ls-dt-highlight-text">{{ animal.breed_name || 'Holandês' }}</span>
            </div>
            <div class="ls-detail-data-row">
              <span class="ls-detail-label">Estábulo / Setor</span>
              <span class="ls-detail-value ls-dt-highlight-text">{{ animal.stable_name || animal.quadrant_name || 'Estábulo Principal' }}</span>
            </div>
          </div>
          <div class="ls-detail-info-lock-notice">
            🔒 Dados estruturais gerenciados apenas no cadastro base do sistema.
          </div>
        </div>

      </div>

      <!-- ABA: HISTÓRICO DE LEITE -->
      <div v-if="showMilkTab && activeTab === 'leite'" class="ls-detail-data-card">
        <div class="ls-detail-card-header-inline">
          <h3 class="ls-detail-card-title">Histórico de Produção de Leite</h3>
          <span class="ls-detail-records-count">{{ milkHistory.length }} Coletas</span>
        </div>
        <div v-if="milkHistory.length === 0" class="ls-detail-empty-history">
          <p>Nenhuma ordenha lançada para este animal até o momento.</p>
        </div>
        <div v-else class="ls-detail-table-responsive">
          <table class="ls-detail-history-table">
            <thead>
              <tr>
                <th>Data da Coleta</th>
                <th>Quantidade Coletada</th>
                <th>Unidade</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in milkHistory" :key="record.id">
                <td class="ls-dt-date-cell">{{ formatDate(record.production_date || record.date_collected || record.date) }}</td>
                <td class="ls-dt-font-bold ls-dt-text-milk">{{ record.milk_production || record.milk_quantity || record.quantity }} L</td>
                <td class="ls-dt-text-muted">Litros</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ABA: HISTÓRICO DE PESO -->
      <div v-if="activeTab === 'peso'" class="ls-detail-data-card">
        <div class="ls-detail-card-header-inline">
          <h3 class="ls-detail-card-title">Histórico de Pesagens</h3>
          <span class="ls-detail-records-count">{{ weightHistory.length }} Pesagens</span>
        </div>
        <div v-if="weightHistory.length === 0" class="ls-detail-empty-history">
          <p>Nenhuma pesagem registrada para este animal até o momento.</p>
        </div>
        <div v-else class="ls-detail-table-responsive">
          <table class="ls-detail-history-table">
            <thead>
              <tr>
                <th>Data da Pesagem</th>
                <th>Peso (kg)</th>
                <th>Unidade</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in weightHistory" :key="record.id">
                <td class="ls-dt-date-cell">{{ formatDate(record.weighing_date || record.date || record.date_weighed) }}</td>
                <td class="ls-dt-font-bold ls-dt-text-weight">{{ record.weight }} kg</td>
                <td class="ls-dt-text-muted">kg</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ABA: REGISTRO DE ALIMENTAÇÃO -->
      <div v-if="activeTab === 'nutricao'" class="ls-detail-data-card">
        <div class="ls-detail-card-header-inline">
          <div>
            <h3 class="ls-detail-card-title">Registro de Alimentação</h3>
            <p class="ls-detail-subheader-text">Histórico de rações e suplementos fornecidos ao animal.</p>
          </div>
        </div>
        <div v-if="feedings.length === 0" class="ls-detail-empty-history">
          <p>Nenhum registro de alimentação encontrado para este animal.</p>
        </div>
        <div v-else class="ls-detail-table-responsive">
          <table class="ls-detail-history-table">
            <thead>
              <tr>
                <th>Data</th>
                <th>Alimento / Ração</th>
                <th>Qtd.</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in feedings" :key="record.id || record.feeding_time + record.animal">
                <td class="ls-dt-date-cell">{{ formatDate(record.date_fed || record.feeding_time) }}</td>
                <td class="ls-dt-text-ellipsis">{{ record.feed_name || record.food?.name || '—' }}</td>
                <td class="ls-dt-font-bold ls-dt-text-nutrition">{{ record.quantity ? `${record.quantity} kg` : record.meal_weight ? `${record.meal_weight} kg` : '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ABA: ATENDIMENTO VETERINÁRIO -->
      <div v-if="activeTab === 'veterinario'" class="ls-detail-data-card">
        <div class="ls-detail-card-header-inline">
          <div>
            <h3 class="ls-detail-card-title">Atendimentos Veterinários</h3>
            <p class="ls-detail-subheader-text">Histórico de consultas, medicamentos e soluções aplicadas.</p>
          </div>
        </div>
        <div v-if="healthRecords.length === 0" class="ls-detail-empty-history">
          <p>Nenhum atendimento veterinário encontrado para este animal.</p>
        </div>
        <div v-else class="ls-detail-table-responsive">
          <table class="ls-detail-history-table">
            <thead>
              <tr>
                <th>Data</th>
                <th>Motivo</th>
                <th>Solução</th>
                <th>Veterinário</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in healthRecords" :key="record.id || record.consultation_date + record.veterinarian">
                <td class="ls-dt-date-cell">{{ formatDate(record.consultation_date) }}</td>
                <td class="ls-dt-text-ellipsis" :title="record.consultation_reason || '—'">{{ record.consultation_reason || '—' }}</td>
                <td class="ls-dt-text-ellipsis" :title="record.consultation_solution || '—'">{{ record.consultation_solution || '—' }}</td>
                <td class="ls-dt-font-bold">{{ record.veterinarian || '—' }}</td>
                <td>
                  <button class="ls-detail-btn-view-details" @click="selectHealthRecord(record)">
                    Ver Descritivo
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="selectedHealthRecord" class="ls-detail-vet-detail-card">
          <div class="ls-detail-panel-header">
            <h4 class="ls-detail-panel-title">Descritivo da Consulta</h4>
            <div class="ls-detail-panel-actions">
              <button class="ls-detail-btn-delete-detail" @click="deleteHealthRecord(selectedHealthRecord)">Excluir</button>
              <button class="ls-detail-btn-close-detail" @click="selectedHealthRecord = null">Fechar</button>
            </div>
          </div>
          <div class="ls-detail-panel-line"><span>Motivo:</span> <span>{{ selectedHealthRecord.consultation_reason || '—' }}</span></div>
          <div class="ls-detail-panel-line"><span>Solução:</span> <span>{{ selectedHealthRecord.consultation_solution || '—' }}</span></div>
          <div class="ls-detail-panel-line"><span>Veterinário:</span> <span>{{ selectedHealthRecord.veterinarian || '—' }}</span></div>
        </div>
      </div>

      <!-- ABA: HISTÓRICO DE VACINAS -->
      <div v-if="activeTab === 'vacinas'" class="ls-detail-data-card">
        <div class="ls-detail-card-header-inline">
          <h3 class="ls-detail-card-title">Histórico de Vacinação Sanitária</h3>
          <span class="ls-detail-records-count">{{ vaccineHistory.length }} Aplicações</span>
        </div>
        <div v-if="vaccineHistory.length === 0" class="ls-detail-empty-history">
          <p>Nenhuma vacina aplicada registrada para este animal.</p>
        </div>
        <div v-else class="ls-detail-table-responsive">
          <table class="ls-detail-history-table">
            <thead>
              <tr>
                <th>Data de Aplicação</th>
                <th>Nome da Vacina / Medicamento</th>
                <th>Status Sanitário</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="vaccine in vaccineHistory" :key="vaccine.id">
                <td class="ls-dt-date-cell">{{ formatDate(vaccine.vaccination_date || vaccine.date || vaccine.date_applied) }}</td>
                <td class="ls-dt-font-bold">{{ vaccine.vaccine_name || vaccine.name }}</td>
                <td><span class="ls-detail-status-badge-secure">Protegido</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>

  <div v-else class="ls-detail-loading-fullscreen">
    <div class="ls-detail-spinner"></div>
    <p>Carregando registros integrados da ficha do animal...</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import { notify } from '@/services/notificationService';

const route = useRoute();
const router = useRouter();

const animal = ref(null);
const loading = ref(true);
const saving = ref(false);
const deleting = ref(false);
const activeTab = ref('geral');
const isEditing = ref(false);

const isDark = ref(false);
let themeObserver = null;

const isFemaleAnimal = (animalData) => String(animalData?.sex || '').toLowerCase() === 'f';
const showMilkTab = computed(() => animal.value ? isFemaleAnimal(animal.value) : false);

const milkHistory = ref([]);
const vaccineHistory = ref([]);
const weightHistory = ref([]);
const feedings = ref([]);
const healthRecords = ref([]);
const selectedHealthRecord = ref(null);

const editData = ref({
  name: '',
  weight: '',
  birth_date: '',
  sex: '',
  active: true
});

const checkGlobalTheme = () => {
  const root = document.documentElement;
  const body = document.body;
  isDark.value = root.classList.contains('dark') || 
                 root.classList.contains('theme-dark') || 
                 body.classList.contains('dark') || 
                 body.classList.contains('theme-dark');
};

onMounted(async () => {
  await loadCompleteAnimalData();
  checkGlobalTheme();

  themeObserver = new MutationObserver(() => {
    checkGlobalTheme();
  });
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  themeObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });
});

onBeforeUnmount(() => {
  if (themeObserver) themeObserver.disconnect();
});

const loadCompleteAnimalData = async () => {
  loading.value = true;
  const id = route.params.id;
  try {
    const response = await api.get(`animals/${id}/`);
    animal.value = response.data;
    editData.value = { ...response.data };

    try {
      const milkRes = await api.getMilkProductionByAnimal(id);
      const data = milkRes.data.historico || milkRes.data.results || milkRes.data;
      milkHistory.value = Array.isArray(data) ? data : [];
    } catch (e) { milkHistory.value = []; }

    try {
      const weightRes = await api.getWeightHistoryByAnimal(id);
      const data = weightRes.data.historico || weightRes.data.results || weightRes.data;
      weightHistory.value = Array.isArray(data) ? data : [];
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
  if (!confirm('Deseja realmente excluir este registro?')) return;
  try {
    await api.deleteVeterinaryRecord(record.id);
    healthRecords.value = healthRecords.value.filter(item => item.id !== record.id);
    selectedHealthRecord.value = null;
    notify('Registro excluído com sucesso.', 'success');
  } catch (error) {
    notify('Erro ao excluir o registro.', 'error');
  }
};

const toggleEdit = () => {
  isEditing.value = !isEditing.value;
  if (!isEditing.value && animal.value) {
    editData.value = { ...animal.value };
  }
};

const updateAnimalInfo = async () => {
  saving.value = true;
  try {
    await api.patch(`animals/${animal.value.id}/`, editData.value);
    animal.value = { ...animal.value, ...editData.value };
    isEditing.value = false;
    notify("Informações atualizadas com sucesso!", 'success');
  } catch (error) {
    notify("Erro ao salvar alterações.", 'error');
  } finally {
    saving.value = false;
  }
};

const deleteAnimal = async () => {
  if (deleting.value) return;
  if (confirm(`Remover permanentemente o animal?`)) {
    deleting.value = true;
    try {
      await api.deleteAnimal(animal.value.id);
      notify('Animal excluído com sucesso.', 'success');
      router.push('/animais');
    } catch (error) {
      notify('Erro ao excluir registro.', 'error');
    } finally {
      deleting.value = false;
    }
  }
};

const goBackToDashboard = () => { router.back(); };
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
};
</script>

<style scoped>
/* ==========================================================================
   TEMA CLARO BASE
   ========================================================================== */
.ls-detail-page-container {
  padding: 40px;
  background-color: #f8fafc;
  min-height: 100vh;
  font-family: 'Lexend', sans-serif;
  color: #0f172a;
  transition: background-color 0.2s, color 0.2s;
  box-sizing: border-box;
}

.ls-detail-header { border-bottom: 1px solid #e2e8f0; padding-bottom: 24px; margin-bottom: 32px; }
.ls-detail-nav-actions { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.ls-detail-btn-back { background: #ffffff; border: 1px solid #e2e8f0; color: #64748b; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 600; }
.ls-detail-btn-danger { background: #fef2f2; border: 1px solid #fca5a5; color: #ef4444; padding: 10px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; }
.ls-detail-main-title { font-size: 2.2rem; font-weight: 800; margin: 0 0 8px 0; letter-spacing: -0.5px; }
.ls-detail-tag-brinco { background: #0f172a; color: #ffffff; padding: 6px 14px; border-radius: 6px; font-family: monospace; font-weight: 700; font-size: 1rem; }

/* ABAS EM MODO CLARO */
.ls-detail-tabs-control { display: flex; flex-wrap: wrap; gap: 8px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; margin-bottom: 32px; }
.ls-detail-tab-btn { border: 1px solid transparent; padding: 12px 20px; font-size: 0.95rem; font-weight: 700; color: #475569; cursor: pointer; border-radius: 10px 10px 0 0; font-family: inherit; transition: all 0.2s; }

.ls-dt-tab-geral { background: #eef2ff; border-color: #c7d2fe; }
.ls-dt-tab-leite { background: #dbeafe; border-color: #93c5fd; }
.ls-dt-tab-peso { background: #dcfce7; border-color: #86efac; }
.ls-dt-tab-nutricao { background: #fef9c3; border-color: #facc15; }
.ls-dt-tab-veterinario { background: #e0e7ff; border-color: #a5b4fc; }
.ls-dt-tab-vacinas { background: #fbcfe8; border-color: #f472b6; }

.ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-geral { background: #c7d2fe; border-color: #4338ca; color: #0f172a; }
.ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-leite { background: #bfdbfe; border-color: #2563eb; color: #0f172a; }
.ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-peso { background: #bbf7d0; border-color: #16a34a; color: #0f172a; }
.ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-nutricao { background: #fde68a; border-color: #d97706; color: #0f172a; }
.ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-veterinario { background: #c7d2fe; border-color: #4f46e5; color: #0f172a; }
.ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-vacinas { background: #fecdd3; border-color: #db2777; color: #0f172a; }

/* CONTAINER E DATA CARDS CLAROS */
.ls-detail-grid-two-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.ls-detail-data-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03); }
.ls-detail-card-title { font-size: 1.25rem; font-weight: 700; margin: 0 0 24px 0; color: #0f172a; }
.ls-detail-card-header-inline { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; }
.ls-detail-card-header-inline .ls-detail-card-title { margin-bottom: 0; }

.ls-detail-data-rows { display: flex; flex-direction: column; gap: 16px; }
.ls-detail-data-row { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #e2e8f0; padding-bottom: 12px; }
.ls-detail-data-row:last-child { border-bottom: none; }
.ls-detail-label { color: #64748b; font-size: 0.95rem; font-weight: 600; }
.ls-detail-value { font-weight: 700; color: #0f172a; font-size: 1.05rem; }
.ls-dt-font-bold { font-weight: 800; }
.ls-dt-highlight-text { color: #16a34a; font-weight: 700; }

/* BADGES MODO CLARO */
.ls-detail-badge { padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; }
.ls-dt-badge-active { background: #dcfce7; color: #166534; }
.ls-dt-badge-inactive { background: #f1f5f9; color: #475569; }

.ls-detail-btn-edit-toggle { background: #0f172a; border: none; color: #ffffff; padding: 8px 14px; border-radius: 6px; font-weight: 600; cursor: pointer; }
.ls-detail-btn-save-inside { background: #16a34a; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 700; cursor: pointer; width: 100%; margin-top: 12px; font-family: inherit; }
.ls-detail-form-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
.ls-detail-form-label { font-size: 0.85rem; font-weight: 700; color: #475569; }
.ls-detail-form-input, .ls-detail-form-select { padding: 10px 14px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; outline: none; font-family: inherit; }

.ls-detail-info-lock-notice { margin-top: 32px; padding: 12px; background: #0f172a; border-radius: 8px; text-align: center; font-size: 0.85rem; color: #ffffff; font-weight: 600; }
.ls-detail-records-count { font-size: 0.85rem; background: #f1f5f9; color: #102a43; padding: 6px 12px; border-radius: 6px; font-weight: 700; }
.ls-detail-subheader-text { margin: 4px 0 0; color: #475569; font-size: 0.9rem; font-weight: 500; }

/* TABELAS */
.ls-detail-table-responsive { width: 100%; overflow-x: auto; }
.ls-detail-history-table { width: 100%; border-collapse: collapse; text-align: left; }
.ls-detail-history-table th { background: #f8fafc; padding: 14px; font-size: 0.85rem; text-transform: uppercase; color: #64748b; font-weight: 700; border-bottom: 1px solid #e2e8f0; }
.ls-detail-history-table td { padding: 14px; border-bottom: 1px solid #e2e8f0; font-size: 0.95rem; color: #334155; }

.ls-dt-date-cell { color: #64748b; font-weight: 600; }
.ls-dt-text-milk { color: #1d4ed8; font-weight: 700; }
.ls-dt-text-weight { color: #16a34a; font-weight: 700; }
.ls-dt-text-nutrition { color: #d97706; font-weight: 700; }
.ls-dt-text-muted { color: #94a3b8; font-size: 0.85rem; }
.ls-detail-status-badge-secure { background: #ecfdf5; color: #166534; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; }
.ls-detail-empty-history { text-align: center; padding: 48px; color: #64748b; font-style: italic; }

.ls-detail-btn-view-details { background: #2563eb; color: #ffffff; border: none; padding: 8px 14px; border-radius: 8px; cursor: pointer; font-weight: 700; font-family: inherit; }
.ls-detail-vet-detail-card { margin-top: 20px; background: #0f172a; border-radius: 12px; padding: 20px; color: #ffffff; }
.ls-detail-panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.ls-detail-panel-title { margin: 0; font-size: 1rem; font-weight: 700; color: #ffffff; }
.ls-detail-panel-actions { display: flex; gap: 8px; }
.ls-detail-btn-close-detail, .ls-detail-btn-delete-detail { padding: 6px 12px; border-radius: 6px; cursor: pointer; font-weight: 600; font-family: inherit; border: 1px solid #374151; }
.ls-detail-btn-close-detail { background: #374151; color: #ffffff; }
.ls-detail-btn-delete-detail { background: #fee2e2; color: #b91c1c; border-color: #fca5a5; }
.ls-detail-panel-line { margin-bottom: 8px; font-size: 0.95rem; }
.ls-detail-panel-line span:first-child { font-weight: 700; color: #9ca3af; display: inline-block; width: 100px; }

.ls-detail-loading-fullscreen { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; color: #64748b; }
.ls-detail-spinner { width: 40px; height: 40px; border: 4px solid #e2e8f0; border-top-color: #16a34a; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 16px; }
@keyframes spin { 100% { transform: rotate(360deg); } }

/* ==========================================================================
   BLINDAGEM DO TEMA ESCURO AUTOMÁTICO (ATIVADO DINAMICAMENTE POR CLASSE VUE)
   ========================================================================== */
.ls-detail-page-container.ls-dark-active {
  background-color: #000000 !important; /* Fundo 100% Preto */
}

/* Data Cards Sólidos e Elementos de Interação */
.ls-detail-page-container.ls-dark-active .ls-detail-data-card,
.ls-detail-page-container.ls-dark-active .ls-detail-vet-detail-card {
  background-color: #111827 !important;
  border-color: #1f2937 !important;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6) !important;
}

/* Alinhamento do Cabeçalho da Tabela e Linhas do Tema Escuro */
.ls-detail-page-container.ls-dark-active .ls-detail-history-table th {
  background-color: #1f2937 !important;
  color: #ffffff !important;
  border-bottom-color: #374151 !important;
}
.ls-detail-page-container.ls-dark-active .ls-detail-history-table td {
  background-color: #111827 !important;
  border-color: #1f2937 !important;
  color: #e5e7eb !important;
}
.ls-detail-page-container.ls-dark-active .ls-detail-history-table tr:hover td {
  background-color: #1f2937 !important;
}

.ls-detail-page-container.ls-dark-active .ls-detail-header,
.ls-detail-page-container.ls-dark-active .ls-detail-card-header-inline,
.ls-detail-page-container.ls-dark-active .ls-detail-data-row {
  border-color: #1f2937 !important;
}

.ls-detail-page-container.ls-dark-active .ls-detail-btn-back,
.ls-detail-page-container.ls-dark-active .ls-detail-form-input,
.ls-detail-page-container.ls-dark-active .ls-detail-form-select {
  background-color: #1f2937 !important;
  border-color: #374151 !important;
  color: #ffffff !important;
}
.ls-detail-page-container.ls-dark-active .ls-detail-btn-edit-toggle,
.ls-detail-page-container.ls-dark-active .ls-detail-info-lock-notice {
  background-color: #1f2937 !important;
  color: #ffffff !important;
}

/* CORREÇÃO DO ERRO 2: RECALIBRAÇÃO COMPLETA DAS BADGES EM TEMA ESCURO (MÁXIMO CONTRASTE) */
.ls-detail-page-container.ls-dark-active .ls-dt-badge-active,
.ls-detail-page-container.ls-dark-active .ls-detail-status-badge-secure {
  background-color: #064e3b !important; /* Verde Escuro Sólido */
  color: #ffffff !important; /* Fonte Branca Pura */
  border: 1px solid #059669 !important;
}
.ls-detail-page-container.ls-dark-active .ls-dt-badge-inactive {
  background-color: #374151 !important;
  color: #ffffff !important;
  border: 1px solid #4b5563 !important;
}

/* CORREÇÃO DO ERRO 1: CORES DAS ABAS INATIVAS JÁ ATIVAS E VISÍVEIS NO ESCURO */
.ls-detail-page-container.ls-dark-active .ls-detail-tabs-control { border-color: #1f2937 !important; }

/* Estilo Base Permanente para Abas Não Selecionadas (Fundo escuro com Borda e Texto Temático) */
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-geral { background-color: #111827 !important; border-color: #1e40af !important; color: #3b82f6 !important; }
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-leite { background-color: #111827 !important; border-color: #0369a1 !important; color: #0ea5e9 !important; }
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-peso { background-color: #111827 !important; border-color: #14532d !important; color: #22c55e !important; }
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-nutricao { background-color: #111827 !important; border-color: #78350f !important; color: #eab308 !important; }
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-veterinario { background-color: #111827 !important; border-color: #4c1d95 !important; color: #a855f7 !important; }
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-vacinas { background-color: #111827 !important; border-color: #831843 !important; color: #ec4899 !important; }

/* Sobrescrita de Preenchimento Total Quando a Aba for Clicada/Selecionada */
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-geral { background-color: #2563eb !important; border-color: #1d4ed8 !important; color: #ffffff !important; }
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-leite { background-color: #0ea5e9 !important; border-color: #0284c7 !important; color: #ffffff !important; }
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-peso { background-color: #16a34a !important; border-color: #15803d !important; color: #ffffff !important; }
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-nutricao { background-color: #d97706 !important; border-color: #b45309 !important; color: #ffffff !important; }
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-veterinario { background-color: #7c3aed !important; border-color: #6d28d9 !important; color: #ffffff !important; }
.ls-detail-page-container.ls-dark-active .ls-detail-tab-btn.ls-dt-tab-active.ls-dt-tab-vacinas { background-color: #db2777 !important; border-color: #be185d !important; color: #ffffff !important; }

/* Forçamento das Fontes e Títulos em Branco Puro */
.ls-detail-page-container.ls-dark-active .ls-detail-main-title,
.ls-detail-page-container.ls-dark-active .ls-detail-card-title,
.ls-detail-page-container.ls-dark-active .ls-detail-value,
.ls-detail-page-container.ls-dark-active .ls-detail-form-label {
  color: #ffffff !important;
}

/* Legendas e Textos Modificados para Alta Visibilidade */
.ls-detail-page-container.ls-dark-active .ls-detail-label,
.ls-detail-page-container.ls-dark-active .ls-detail-subheader-text,
.ls-detail-page-container.ls-dark-active .ls-dt-date-cell,
.ls-detail-page-container.ls-dark-active .ls-detail-empty-history {
  color: #f3f4f6 !important;
}

.ls-detail-page-container.ls-dark-active .ls-detail-records-count {
  background-color: #1f2937 !important;
  color: #38bdf8 !important;
  border: 1px solid #374151 !important;
}
</style>