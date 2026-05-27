<template>
  <div class="detail-wrapper" v-if="animal && !loading">
    <header class="detail-header">
      <div class="nav-actions">
        <button @click="goBackToDashboard" class="btn-back">← Voltar para a Lista</button>
        <button @click="deleteAnimal" class="btn-danger">🗑 Excluir Registro</button>
      </div>
      <div class="animal-title-section">
        <h1>Ficha Individual: {{ animal.name || 'Sem Nome' }}</h1>
        <span class="tag-brinco">Brinco #{{ animal.register_number }}</span>
      </div>
    </header>

    <div class="tabs-control">
      <button 
        @click="activeTab = 'geral'" 
        :class="{ 'tab-active': activeTab === 'geral' }"
        class="tab-btn"
      >
        📋 Informações Gerais
      </button>
      <button 
        @click="activeTab = 'leite'" 
        :class="{ 'tab-active': activeTab === 'leite' }"
        class="tab-btn"
      >
        🥛 Registro de Leite
      </button>
      <button 
        @click="activeTab = 'peso'" 
        :class="{ 'tab-active': activeTab === 'peso' }"
        class="tab-btn"
      >
        ⚖️ Histórico de Pesos
      </button>
      <button 
        @click="activeTab = 'vacinas'" 
        :class="{ 'tab-active': activeTab === 'vacinas' }"
        class="tab-btn"
      >
        ✛ Vacinas Aplicadas
      </button>
    </div>

    <div class="tab-content">
      
      <div v-if="activeTab === 'geral'" class="grid-two-columns">
        
        <div class="data-card editable-card">
          <div class="card-header-inline">
            <h3>Informações do Animal</h3>
            <button @click="toggleEdit" class="btn-edit-toggle">
              {{ isEditing ? '📁 Cancelar' : '✎ Editar Informações' }}
            </button>
          </div>

          <div v-if="!isEditing" class="data-rows">
            <div class="data-row">
              <span class="label">Peso Atual</span>
              <span class="value font-bold">{{ animal.weight }} kg</span>
            </div>
            <div class="data-row">
              <span class="label">Data de Nascimento</span>
              <span class="value">{{ formatDate(animal.birth_date) }}</span>
            </div>
            <div class="data-row">
              <span class="label">Sexo</span>
              <span class="value">{{ animal.sex === 'm' || animal.sex === 'M' ? 'Macho' : 'Fêmea' }}</span>
            </div>
            <div class="data-row">
              <span class="label">Status do Rebanho</span>
              <span class="value badge" :class="animal.active ? 'badge-active' : 'badge-inactive'">
                {{ animal.active ? 'Ativo' : 'Inativo' }}
              </span>
            </div>
          </div>

          <form v-else @submit.prevent="updateAnimalInfo" class="edit-form">
            <div class="form-group">
              <label>Nome / Apelido</label>
              <input v-model="editData.name" type="text" required>
            </div>
            <div class="form-group">
              <label>Peso (kg)</label>
              <input v-model="editData.weight" type="number" step="0.01" required>
            </div>
            <div class="form-group">
              <label>Data de Nascimento</label>
              <input v-model="editData.birth_date" type="date" required>
            </div>
            <div class="form-group">
              <label>Sexo</label>
              <select v-model="editData.sex">
                <option value="m">Macho</option>
                <option value="f">Fêmea</option>
              </select>
            </div>
            <div class="form-group">
              <label>Status</label>
              <select v-model="editData.active">
                <option :value="true">Ativo</option>
                <option :value="false">Inativo</option>
              </select>
            </div>
            <button type="submit" class="btn-save-inside" :disabled="saving">
              {{ saving ? 'Salvando...' : '💾 Salvar Alterações' }}
            </button>
          </form>
        </div>

        <div class="data-card complement-card">
          <h3>Classificação e Localização</h3>
          <div class="data-rows">
            <div class="data-row">
              <span class="label">Espécie</span>
              <span class="value highlight-text">{{ animal.specie_name || 'Bovino' }}</span>
            </div>
            <div class="data-row">
              <span class="label">Raça</span>
              <span class="value highlight-text">{{ animal.breed_name || 'Holandês' }}</span>
            </div>
            <div class="data-row">
              <span class="label">Estábulo / Setor</span>
              <span class="value highlight-text">{{ animal.stable_name || animal.quadrant_name || 'Estábulo Principal' }}</span>
            </div>
          </div>
          <div class="info-lock-notice">
            🔒 Dados estruturais gerenciados apenas no cadastro base do sistema.
          </div>
        </div>

      </div>

      <div v-if="activeTab === 'leite'" class="data-card table-card">
        <div class="card-header-inline">
          <h3>Histórico de Produção de Leite</h3>
          <span class="records-count">{{ milkHistory.length }} Coletas registradas</span>
        </div>

        <div v-if="milkHistory.length === 0" class="empty-history">
          <p>Nenhuma ordenha lançada para este animal até o momento.</p>
        </div>

        <table v-else class="history-table">
          <thead>
            <tr>
              <th>Data da Coleta</th>
              <th>Quantidade Coletada</th>
              <th>Unidade</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in milkHistory" :key="record.id">
              <td>{{ formatDate(record.production_date || record.date_collected || record.date) }}</td>
              <td class="font-bold text-green">{{ record.milk_production || record.milk_quantity || record.quantity }} L</td>
              <td class="text-muted">Litros</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="activeTab === 'peso'" class="data-card table-card">
        <div class="card-header-inline">
          <h3>Histórico de Pesagens</h3>
          <span class="records-count">{{ weightHistory.length }} Pesagens registradas</span>
        </div>

        <div v-if="weightHistory.length === 0" class="empty-history">
          <p>Nenhuma pesagem registrada para este animal até o momento.</p>
        </div>

        <table v-else class="history-table">
          <thead>
            <tr>
              <th>Data da Pesagem</th>
              <th>Peso (kg)</th>
              <th>Unidade</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in weightHistory" :key="record.id">
              <td>{{ formatDate(record.weighing_date || record.date || record.date_weighed) }}</td>
              <td class="font-bold text-green">{{ record.weight }} kg</td>
              <td class="text-muted">kg</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="activeTab === 'vacinas'" class="data-card table-card">
        <div class="card-header-inline">
          <h3>Histórico de Vacinação Sanitária</h3>
          <span class="records-count">{{ vaccineHistory.length }} Aplicações</span>
        </div>

        <div v-if="vaccineHistory.length === 0" class="empty-history">
          <p>Nenhuma vacina aplicada registrada para este animal.</p>
        </div>

        <table v-else class="history-table">
          <thead>
            <tr>
              <th>Data de Aplicação</th>
              <th>Nome da Vacina / Medicamento</th>
              <th>Status Sanitário</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="vaccine in vaccineHistory" :key="vaccine.id">
              <td>{{ formatDate(vaccine.vaccination_date || vaccine.date || vaccine.date_applied) }}</td>
              <td class="font-bold">{{ vaccine.vaccine_name || vaccine.name }}</td>
              <td><span class="badge badge-active">Protegido</span></td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>

  <div v-else class="loading-state-fullscreen">
    <div class="spinner"></div>
    <p>Carregando registros integrados da ficha do animal...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import { notify } from '@/services/notificationService';

const route = useRoute();
const router = useRouter();

const animal = ref(null);
const loading = ref(true);
const saving = ref(false);
const activeTab = ref('geral'); // Controle das abas secundárias
const isEditing = ref(false);   // Controle de edição do card de infos

// Históricos sincronizados vindos das outras páginas
const milkHistory = ref([]);
const vaccineHistory = ref([]);
const weightHistory = ref([]);

// Dados reativos para o formulário de edição interna
const editData = ref({
  name: '',
  weight: '',
  birth_date: '',
  sex: '',
  active: true
});

onMounted(async () => {
  await loadCompleteAnimalData();
});

const loadCompleteAnimalData = async () => {
  loading.value = true;
  const id = route.params.id;
  try {
    // 1. Carrega dados do animal
    const response = await api.get(`animals/${id}/`);
    animal.value = response.data;
    
    // Prepara dados de edição
    editData.value = { ...response.data };

    // 2. Busca histórico de leite direto do backend por animal
    try {
      const milkRes = await api.getMilkProductionByAnimal(id);
      const data = milkRes.data.historico || milkRes.data.results || milkRes.data;
      milkHistory.value = Array.isArray(data) ? data : [];
    } catch (e) {
      console.warn("Erro ao buscar histórico de leite do animal:", e);
      milkHistory.value = [];
    }

    // 3. Busca histórico de peso direto do backend por animal
    try {
      const weightRes = await api.getWeightHistoryByAnimal(id);
      const data = weightRes.data.historico || weightRes.data.results || weightRes.data;
      weightHistory.value = Array.isArray(data) ? data : [];
    } catch (e) {
      console.warn("Erro ao buscar histórico de peso do animal:", e);
      weightHistory.value = [];
    }

    // 4. Busca histórico de vacinas direto do backend por animal
    try {
      const vaccineRes = await api.getVaccinationsByAnimal(id);
      const data = vaccineRes.data.results || vaccineRes.data;
      vaccineHistory.value = data;
    } catch (e) {
      console.warn("Erro ao buscar histórico de vacinas do animal:", e);
      vaccineHistory.value = [];
    }

  } catch (error) {
    console.error("Erro ao carregar dados integrados:", error);
  } finally {
    loading.value = false;
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
    notify("Informações do animal atualizadas com sucesso!", 'success');
  } catch (error) {
    console.error("Erro ao atualizar animal:", error.response?.data || error);
    notify("Erro ao salvar alterações. Verifique o console para mais detalhes.", 'error');
  } finally {
    saving.value = false;
  }
};

const deleteAnimal = async () => {
  if (confirm(`Remover permanentemente o animal ${animal.value.name || ''} do sistema?`)) {
    try {
      await api.delete(`animals/${animal.value.id}/`);
      router.back();
    } catch (error) {
      notify("Erro ao excluir registro.", 'error');
    }
  }
};

const goBackToDashboard = () => {
  router.back();
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.detail-wrapper { padding: 40px; background-color: #f8fafc; min-height: 100vh; font-family: 'Inter', sans-serif; color: #0f172a; }

/* CABEÇALHO */
.detail-header { border-bottom: 1px solid #e2e8f0; padding-bottom: 24px; margin-bottom: 32px; }
.nav-actions { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.btn-back { background: transparent; border: 1px solid #e2e8f0; color: #64748b; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 500; transition: 0.2s; }
.btn-back:hover { background: #f1f5f9; color: #0f172a; }
.btn-danger { background: #fef2f2; border: 1px solid #fca5a5; color: #ef4444; padding: 10px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-danger:hover { background: #fee2e2; }
.animal-title-section h1 { font-size: 2.2rem; font-weight: 700; margin: 0 0 8px 0; letter-spacing: -0.5px; }
.tag-brinco { background: #0f172a; color: #ffffff; padding: 6px 14px; border-radius: 6px; font-family: monospace; font-weight: 700; font-size: 1rem; }

/* ABAS CONTROL */
.tabs-control { display: flex; gap: 8px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; margin-bottom: 32px; }
.tab-btn { background: transparent; border: none; padding: 12px 24px; font-size: 1rem; font-weight: 600; color: #64748b; cursor: pointer; border-radius: 8px; transition: 0.2s; }
.tab-btn:hover { background: #f1f5f9; color: #0f172a; }
.tab-active { background: #f0fdf4; color: #16a34a; }

/* CARDS DE CONTEÚDO */
.grid-two-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.data-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
.data-card h3 { font-size: 1.2rem; font-weight: 700; margin-top: 0; margin-bottom: 24px; color: #0f172a; }

.card-header-inline { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; }
.card-header-inline h3 { margin: 0; }

/* INFORMAÇÕES ALINHADAS */
.data-rows { display: flex; flex-direction: column; gap: 16px; }
.data-row { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #e2e8f0; padding-bottom: 12px; }
.data-row:last-child { border-bottom: none; }
.label { color: #64748b; font-size: 0.95rem; font-weight: 500; }
.value { font-weight: 600; color: #0f172a; font-size: 1.05rem; }
.highlight-text { color: #16a34a; font-weight: 700; }
.font-bold { font-weight: 700; }

/* BADGES */
.badge { padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
.badge-active { background: #dcfce7; color: #166534; }
.badge-inactive { background: #f1f5f9; color: #475569; }

/* FORMULÁRIO DE EDIÇÃO INTERNA */
.edit-form { display: flex; flex-direction: column; gap: 16px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 0.85rem; font-weight: 600; color: #475569; }
.edit-form input, .edit-form select { padding: 10px 14px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; outline: none; background: #fff; font-family: inherit; }
.edit-form input:focus, .edit-form select:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1); }
.btn-edit-toggle { background: #f1f5f9; border: none; color: #475569; padding: 8px 14px; border-radius: 6px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-edit-toggle:hover { background: #e2e8f0; color: #0f172a; }
.btn-save-inside { background: #16a34a; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; margin-top: 10px; font-family: inherit; }
.btn-save-inside:hover { background: #15803d; }

.info-lock-notice { margin-top: 32px; padding: 12px; background: #f8fafc; border-radius: 6px; text-align: center; font-size: 0.85rem; color: #94a3b8; font-weight: 500; }

/* TABELAS DE HISTÓRICO (NÃO EDITÁVEIS) */
.records-count { font-size: 0.85rem; background: #f1f5f9; color: #475569; padding: 6px 12px; border-radius: 6px; font-weight: 600; }
.history-table { width: 100%; border-collapse: collapse; text-align: left; }
.history-table th { background: #f8fafc; padding: 14px; font-size: 0.85rem; text-transform: uppercase; color: #64748b; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.history-table td { padding: 14px; border-bottom: 1px solid #e2e8f0; font-size: 0.95rem; }
.history-table tr:last-child td { border-bottom: none; }
.text-green { color: #16a34a; }
.text-muted { color: #94a3b8; font-size: 0.85rem; }
.empty-history { text-align: center; padding: 48px; color: #64748b; font-style: italic; }

/* LOADING STATES */
.loading-state-fullscreen { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background: #f8fafc; color: #64748b; }
.spinner { width: 40px; height: 40px; border: 4px solid #e2e8f0; border-top-color: #16a34a; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 16px; }
@keyframes spin { 100% { transform: rotate(360deg); } }

@media (max-width: 1024px) {
  .grid-two-columns { grid-template-columns: 1fr; }
}
</style>