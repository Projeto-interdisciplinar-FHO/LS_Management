<template>
  <div class="stables-wrapper">
    <header class="page-header">
      <div class="header-info">
        <button @click="$router.push('/dashboard-adm')" class="btn-back">← Voltar ao Início</button>
        <h1>Gestão de Estábulos</h1>
        <p>Controle de lotação, movimentação de rebanho e finalidade das instalações.</p>
      </div>
      <button @click="openCreateModal" class="btn-primary">
        + Novo Estábulo
      </button>
    </header>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Sincronizando instalações e lotação de animais...</p>
    </div>

    <div v-else class="content-container">
      
      <div class="stables-grid">
        <div 
          v-for="stable in stables" 
          :key="stable.id" 
          class="stable-card"
          :class="{ 'stable-overpopulated': getStableAnimalCount(stable.id) > stable.capacity }"
        >
          <header class="stable-card-header">
            <div class="stable-title-area">
              <span class="stable-icon">☖</span>
              <div>
                <h3>{{ stable.name || `Estábulo ${stable.id}` }}</h3>
                <span class="stable-type-tag">{{ stable.purpose || 'Manejo Geral' }}</span>
              </div>
            </div>
            <div class="stable-actions-top">
              <button @click="editStable(stable)" class="btn-icon-action" title="Editar Instalação">✎</button>
              <button @click="deleteStable(stable.id)" class="btn-icon-action btn-icon-danger" title="Excluir Instalação">✕</button>
            </div>
          </header>

          <div class="capacity-section">
            <div class="capacity-labels">
              <span class="label">Taxa de Ocupação</span>
              <span class="value font-mono">
                {{ getStableAnimalCount(stable.id) }} / {{ stable.capacity }} cabeças
              </span>
            </div>
            <div class="progress-bar-bg">
              <div 
                class="progress-bar-fill" 
                :style="{ width: getCapacityPercentage(stable.id, stable.capacity) + '%' }"
                :class="getProgressBarClass(stable.id, stable.capacity)"
              ></div>
            </div>
          </div>

          <button 
            @click="toggleStableExpansion(stable.id)" 
            class="btn-toggle-animals"
          >
            {{ expandedStables.includes(stable.id) ? '▲ Ocultar Animais' : '▼ Listar Animais deste Estábulo' }}
          </button>

          <transition name="expand">
            <div v-if="expandedStables.includes(stable.id)" class="animals-sub-table-wrapper">
              <table class="animals-sub-table">
                <thead>
                  <tr>
                    <th>Registro</th>
                    <th>Nome</th>
                    <th>Peso</th>
                    <th class="text-right">Ações de Manejo</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="animal in getAnimalsInStable(stable.id)" :key="animal.id">
                    <td class="font-mono">#{{ animal.register_number }}</td>
                    <td class="font-bold">{{ animal.name || 'Sem nome' }}</td>
                    <td>{{ animal.weight }} kg</td>
                    <td class="actions-cell-inline">
                      <select 
                        @change="moveAnimal(animal, $event)" 
                        class="select-move-inline"
                        title="Transferir animal para outra instalação"
                      >
                        <option value="" disabled selected>Transferir...</option>
                        <option 
                          v-for="target in stables" 
                          :key="target.id" 
                          :value="target.id"
                          :disabled="target.id === stable.id"
                        >
                          Para: {{ target.name }}
                        </option>
                      </select>

                      <button 
                        @click="removeAnimalFromStable(animal)" 
                        class="btn-text-action text-red"
                        title="Desalocar animal desta instalação"
                      >
                        Desalocar
                      </button>

                      <button 
                        @click="$router.push(`/animais/editar/${animal.id}`)" 
                        class="btn-text-action text-green"
                        title="Editar ficha básica"
                      >
                        Editar
                      </button>
                    </td>
                  </tr>
                  <tr v-if="getAnimalsInStable(stable.id).length === 0">
                    <td colspan="4" class="empty-stable-row">
                      Nenhum animal alojado neste estábulo atualmente.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </transition>
        </div>
      </div>

    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content">
        <header class="modal-header">
          <h2>{{ isEditingStable ? 'Editar Instalação' : 'Novo Estábulo' }}</h2>
          <button @click="showModal = false" class="btn-close">✕</button>
        </header>
        <form @submit.prevent="saveStable" class="modal-form">
          <div class="input-group">
            <label>Nome do Estábulo</label>
            <input v-model="stableForm.name" type="text" placeholder="Ex: Estábulo de Ordenha B" required>
          </div>
          <div class="input-group mt-3">
            <label>Capacidade Máxima de Cabeças</label>
            <input v-model="stableForm.capacity" type="number" min="1" placeholder="Ex: 50" required>
          </div>
          <div class="input-group mt-3">
            <label>Propósito / Tipo de Manejo</label>
            <select v-model="stableForm.purpose" required>
              <option value="" disabled>Selecione uma finalidade...</option>
              <option value="Ordenha Higiênica">Ordenha Higiênica</option>
              <option value="Maternidade / Crias">Maternidade / Crias</option>
              <option value="Engorda / Confinamento">Engorda / Confinamento</option>
              <option value="Tratamento Veterinário">Tratamento Veterinário</option>
              <option value="Manejo Geral">Manejo Geral</option>
            </select>
          </div>
          <button type="submit" class="btn-primary mt-4" :disabled="savingStable">
            {{ savingStable ? 'Processando...' : 'Confirmar Instalação' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import { notify } from '@/services/notificationService';

const stables = ref([]);
const animals = ref([]);
const loading = ref(true);
const showModal = ref(false);
const isEditingStable = ref(false);
const savingStable = ref(false);
const expandedStables = ref([]);

const stableForm = ref({
  id: null,
  name: '',
  capacity: '',
  purpose: ''
});

onMounted(() => {
  loadData();
});

const loadData = async () => {
  loading.value = true;
  try {
    const stablesRes = await api.get('quadrants/');
    stables.value = stablesRes.data.results || stablesRes.data;

    if (stables.value.length === 0) {
      stables.value = [
        { id: 1, name: 'Estábulo Principal A', capacity: 40, purpose: 'Ordenha Higiênica' },
        { id: 2, name: 'Piquete Sul Maternidade', capacity: 15, purpose: 'Maternidade / Crias' }
      ];
    }

    const animalsRes = await api.get('animals/');
    animals.value = animalsRes.data.results || animalsRes.data;

  } catch (error) {
    console.error("Erro ao sincronizar dados de instalações:", error);
  } finally {
    loading.value = false;
  }
};

const getAnimalQuadrantId = (animal) => {
  if (animal && animal.quadrant && typeof animal.quadrant === 'object') {
    return animal.quadrant.id || animal.quadrant;
  }
  return animal.quadrant;
};

const getAnimalsInStable = (stableId) => {
  return animals.value.filter(animal => String(getAnimalQuadrantId(animal)) === String(stableId));
};

const getStableAnimalCount = (stableId) => {
  return getAnimalsInStable(stableId).length;
};

const getCapacityPercentage = (stableId, maxCapacity) => {
  const current = getStableAnimalCount(stableId);
  const percent = (current / maxCapacity) * 100;
  return percent > 100 ? 100 : percent;
};

const getProgressBarClass = (stableId, maxCapacity) => {
  const current = getStableAnimalCount(stableId);
  if (current >= maxCapacity) return 'bar-red';
  if (current >= maxCapacity * 0.8) return 'bar-orange';
  return 'bar-green';
};

const toggleStableExpansion = (stableId) => {
  if (expandedStables.value.includes(stableId)) {
    expandedStables.value = expandedStables.value.filter(id => id !== stableId);
  } else {
    expandedStables.value.push(stableId);
  }
};

const moveAnimal = async (animal, event) => {
  const targetStableId = Number(event.target.value);
  if (!targetStableId) return;

  try {
    await api.patch(`animals/${animal.id}/`, { quadrant: targetStableId });
    notify(`Animal ${animal.name || ''} transferido com sucesso!`, 'success');
    loadData();
  } catch (error) {
    console.error(error);
    notify('Falha ao processar movimentação do animal.', 'error');
  } finally {
    event.target.value = '';
  }
};

const removeAnimalFromStable = async (animal) => {
  notify('A desalocação direta não é suportada pelo cadastro atual. Transfira o animal para outro estábulo.', 'warning');
};

const openCreateModal = () => {
  isEditingStable.value = false;
  stableForm.value = { id: null, name: '', capacity: '', purpose: '' };
  showModal.value = true;
};

const editStable = (stable) => {
  isEditingStable.value = true;
  stableForm.value = { ...stable };
  showModal.value = true;
};

const saveStable = async () => {
  savingStable.value = true;
  try {
    if (isEditingStable.value) {
      await api.put(`quadrants/${stableForm.value.id}/`, stableForm.value);
      notify('Instalação atualizada com sucesso!', 'success');
    } else {
      await api.post('quadrants/', stableForm.value);
      notify('Novo estábulo cadastrado no sistema!', 'success');
    }
    showModal.value = false;
    loadData();
  } catch (error) {
    console.error(error);
    notify('Erro ao salvar instalação técnica.', 'error');
  } finally {
    savingStable.value = false;
  }
};

const deleteStable = async (stableId) => {
  if (confirm('Deseja realmente remover este estábulo? Os animais alocados nele ficarão desalocados automaticamente.')) {
    try {
      await api.delete(`quadrants/${stableId}/`);
      notify('Estábulo excluído com sucesso.', 'success');
      loadData();
    } catch (error) {
      console.error(error);
      notify('Falha ao excluir estábulo.', 'error');
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stables-wrapper { padding: 40px; background-color: #f8fafc; min-height: 100vh; color: #0f172a; font-family: 'Inter', sans-serif; }

.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 32px; border-bottom: 1px solid #e2e8f0; padding-bottom: 24px; }
.btn-back { background: transparent; border: 1px solid #e2e8f0; color: #64748b; padding: 8px 16px; border-radius: 8px; cursor: pointer; margin-bottom: 16px; font-weight: 500; transition: 0.2s; }
.btn-back:hover { background: #f1f5f9; color: #0f172a; }
.page-header h1 { font-size: 2rem; font-weight: 700; margin: 0 0 8px 0; }
.page-header p { color: #64748b; font-size: 1rem; margin: 0; }

.btn-primary { background: #16a34a; color: #ffffff; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; font-family: inherit; }
.btn-primary:hover:not(:disabled) { background: #15803d; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

.stables-grid { display: flex; flex-direction: column; gap: 24px; }
.stable-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); transition: border-color 0.2s; }
.stable-card:hover { border-color: #cbd5e1; }
.stable-overpopulated { border-color: #fca5a5 !important; background: #fff8f8; }

.stable-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.stable-title-area { display: flex; align-items: center; gap: 16px; }
.stable-icon { font-size: 2rem; color: #16a34a; background: #f0fdf4; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; border-radius: 10px; }
.stable-card-header h3 { font-size: 1.25rem; font-weight: 700; margin: 0 0 4px 0; }
.stable-type-tag { font-size: 0.8rem; background: #f1f5f9; color: #475569; padding: 4px 10px; border-radius: 6px; font-weight: 600; }

.stable-actions-top { display: flex; gap: 4px; }
.btn-icon-action { background: transparent; border: none; font-size: 1rem; color: #64748b; padding: 6px 10px; border-radius: 6px; cursor: pointer; transition: 0.2s; }
.btn-icon-action:hover { background: #f1f5f9; color: #0f172a; }
.btn-icon-danger:hover { background: #fef2f2; color: #ef4444; }

.capacity-section { margin-bottom: 20px; }
.capacity-labels { display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 8px; font-weight: 500; }
.capacity-labels .label { color: #64748b; }
.capacity-labels .value { color: #0f172a; font-weight: 600; }
.font-mono { font-family: monospace; font-size: 0.95rem; }

.progress-bar-bg { background: #e2e8f0; height: 8px; border-radius: 10px; overflow: hidden; }
.progress-bar-fill { height: 100%; transition: width 0.4s ease; border-radius: 10px; }
.bar-green { background: #16a34a; }
.bar-orange { background: #f97316; }
.bar-red { background: #ef4444; }

.btn-toggle-animals { width: 100%; text-align: center; background: #f8fafc; border: 1px solid #e2e8f0; padding: 10px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; color: #475569; cursor: pointer; transition: 0.2s; }
.btn-toggle-animals:hover { background: #f1f5f9; color: #0f172a; border-color: #cbd5e1; }

.animals-sub-table-wrapper { margin-top: 16px; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; background: #ffffff; }
.animals-sub-table { width: 100%; border-collapse: collapse; text-align: left; }
.animals-sub-table th { background: #f8fafc; padding: 12px 16px; font-size: 0.8rem; text-transform: uppercase; color: #64748b; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.animals-sub-table td { padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-size: 0.9rem; color: #334155; }
.animals-sub-table tr:last-child td { border-bottom: none; }
.font-bold { font-weight: 600; }

.actions-cell-inline { display: flex; align-items: center; justify-content: flex-end; gap: 16px; }
.select-move-inline { padding: 6px 12px; font-size: 0.85rem; border: 1px solid #cbd5e1; border-radius: 6px; background: #fff; color: #475569; outline: none; }
.select-move-inline:focus { border-color: #16a34a; }
.btn-text-action { background: transparent; border: none; font-size: 0.85rem; font-weight: 600; cursor: pointer; padding: 4px; }
.btn-text-action:hover { text-decoration: underline; }
.text-red { color: #ef4444; }
.text-green { color: #16a34a; }
.empty-stable-row { text-align: center; padding: 24px !important; color: #94a3b8; font-style: italic; }

.modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15, 23, 42, 0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(4px); }
.modal-content { background: #ffffff; border-radius: 12px; width: 100%; max-width: 400px; padding: 24px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; }
.modal-header h2 { font-size: 1.25rem; font-weight: 600; color: #0f172a; margin: 0; }
.btn-close { background: transparent; border: none; font-size: 1.2rem; color: #64748b; cursor: pointer; }
.btn-close:hover { color: #ef4444; }

.modal-form { display: flex; flex-direction: column; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #475569; }
.input-group input, .input-group select { padding: 12px 16px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; color: #0f172a; outline: none; background: #fff; font-family: inherit; }
.input-group input:focus, .input-group select:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1); }
.mt-3 { margin-top: 16px; }
.mt-4 { margin-top: 24px; }

.loading-state { text-align: center; padding: 100px; color: #64748b; }
.spinner { width: 40px; height: 40px; border: 4px solid #e2e8f0; border-top-color: #16a34a; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 16px; }
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>