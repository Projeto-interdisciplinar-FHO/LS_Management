<template>
  <div class="page-wrapper">
    <header class="page-header">
      <button @click="goHome" class="btn-back">← Painel Geral</button>
      <div class="header-main-row">
        <div class="header-content">
          <h1>Dashboard Nutricional</h1>
          <p>Controle do estoque de insumos alimentares e auditoria de consumo por animal.</p>
        </div>
        <button @click="showAddFeedModal = true" class="btn-primary">
          + Novo Tipo de Alimento
        </button>
      </div>
    </header>

    <div class="reports-grid" v-if="!loading">
      <section class="report-card">
        <header class="card-header-inline">
          <h2>Alimentos / Insumos Cadastrados</h2>
          <span class="badge">{{ foodsList.length }} Tipos</span>
        </header>

        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>Nome / Descrição</th>
                <th>Fabricante ou Composição</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="food in foodsList" :key="food.id">
                <td class="font-bold">{{ food.name }}</td>
                <td>{{ food.description || '—' }}</td>
              </tr>
              <tr v-if="foodsList.length === 0">
                <td colspan="2" class="text-center text-muted">Nenhum alimento cadastrado ainda.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <div v-else class="loading-state">
      <div class="spinner"></div>
      <p>Buscando dados de auditoria alimentar...</p>
    </div>

    <div v-if="showAddFeedModal" class="modal-overlay" @click.self="showAddFeedModal = false">
      <div class="modal-content">
        <header class="modal-header">
          <h2>Adicionar Insumo / Ração</h2>
          <button @click="showAddFeedModal = false" class="btn-close">✕</button>
        </header>
        <form @submit.prevent="submitNewFeed" class="modal-form">
          <div class="input-group">
            <label>Nome Comercial / Descrição</label>
            <input v-model="newFeedForm.name" type="text" placeholder="Ex: Ração Lactação Premium" required>
          </div>
          <div class="input-group mt-3">
            <label>Fabricante ou Tipo de Fibra</label>
            <input v-model="newFeedForm.description" type="text" placeholder="Ex: Milho e Soja com minerais">
          </div>
          <button type="submit" class="btn-primary mt-4" :disabled="savingFeed">
            {{ savingFeed ? 'Salvando...' : 'Cadastrar Alimento' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import { useRouter } from 'vue-router';

const router = useRouter();
const goHome = () => {
  const role = localStorage.getItem('user_role');
  if (role === 'op') router.push('/dashboard-op');
  else router.push('/dashboard-adm');
};

const loading = ref(true);
const savingFeed = ref(false);
const showAddFeedModal = ref(false);

const foodsList = ref([]);
const newFeedForm = ref({ name: '', description: '' });

onMounted(() => {
  loadFoodsList();
});

const loadFoodsList = async () => {
  loading.value = true;
  try {
    const historyRes = await api.get('foods/');
    foodsList.value = historyRes.data.results || historyRes.data;
  } catch (error) {
    console.error("Erro ao puxar dados alimentares:", error);
  } finally {
    loading.value = false;
  }
};

const submitNewFeed = async () => {
  savingFeed.value = true;
  try {
    await api.post('foods/', newFeedForm.value);
    alert('Novo alimento adicionado com sucesso ao estoque!');
    showAddFeedModal.value = false;
    newFeedForm.value = { name: '', description: '' };
    loadFoodsList();
  } catch (error) {
    console.error(error);
    alert('Erro ao cadastrar novo insumo.');
  } finally {
    savingFeed.value = false;
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A';
  return new Date(dateStr).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.page-wrapper { padding: 40px; background-color: #f8fafc; min-height: 100vh; font-family: 'Inter', sans-serif; color: #0f172a; }
.page-header { margin-bottom: 32px; border-bottom: 1px solid #e2e8f0; padding-bottom: 24px; }
.btn-back { background: transparent; border: 1px solid #e2e8f0; color: #64748b; padding: 8px 16px; border-radius: 8px; cursor: pointer; margin-bottom: 16px; font-weight: 500; }
.btn-back:hover { background: #f1f5f9; color: #0f172a; }

.header-main-row { display: flex; justify-content: space-between; align-items: flex-end; }
.header-content h1 { font-size: 2rem; font-weight: 700; margin: 0 0 8px 0; }
.header-content p { color: #64748b; margin: 0; }

.btn-primary { background: #16a34a; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; font-family: inherit; }
.btn-primary:hover { background: #15803d; }

.report-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
.card-header-inline { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.card-header-inline h2 { font-size: 1.25rem; font-weight: 600; margin: 0; }
.badge { background: #f1f5f9; color: #475569; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }

.table-responsive { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th { background: #f8fafc; padding: 16px; font-size: 0.85rem; text-transform: uppercase; color: #64748b; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 16px; border-bottom: 1px solid #e2e8f0; font-size: 0.95rem; }
.text-right { text-align: right; }
.text-center { text-align: center; }
.text-muted { color: #94a3b8; font-style: italic; }
.font-bold { font-weight: 600; }
.text-green { color: #16a34a; }
.feed-tag { background: #eff6ff; color: #1d4ed8; padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; font-weight: 500; }

/* MODAL */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15, 23, 42, 0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(4px); }
.modal-content { background: #ffffff; border-radius: 12px; width: 100%; max-width: 400px; padding: 24px; }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; }
.modal-header h2 { font-size: 1.25rem; font-weight: 600; margin: 0; }
.btn-close { background: transparent; border: none; font-size: 1.2rem; color: #64748b; cursor: pointer; }

.modal-form { display: flex; flex-direction: column; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #475569; }
.input-group input { padding: 12px 16px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; outline: none; }
.input-group input:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1); }
.mt-3 { margin-top: 16px; }
.mt-4 { margin-top: 24px; }

.loading-state { text-align: center; padding: 60px; color: #64748b; }
.spinner { width: 40px; height: 40px; border: 4px solid #e2e8f0; border-top-color: #16a34a; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 16px; }
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>