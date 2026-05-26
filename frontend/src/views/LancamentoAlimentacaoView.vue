<template>
  <div class="page-wrapper">
    <header class="page-header">
      <button @click="$router.back()" class="btn-back">← Voltar</button>
      <div class="header-content">
        <h1>Registro de Trato Nutricional</h1>
        <p>Lance o consumo diário de ração ou suplementos por animal.</p>
      </div>
    </header>

    <div class="content-container">
      <section class="form-card">
        <header class="card-header">
          <span class="icon">🌾</span>
          <h2>Nova Entrada de Alimentação</h2>
        </header>

        <form @submit.prevent="handleSubmit" class="data-form">
          <div class="form-grid">
            <div class="input-group">
              <label>Selecione o Animal</label>
              <select v-model="formData.animal" required>
                <option value="" disabled>Escolha um animal...</option>
                <option v-for="animal in animalsList" :key="animal.id" :value="animal.id">
                  {{ animal.name || 'Sem nome' }} (Brinco: #{{ animal.register_number }})
                </option>
              </select>
            </div>

            <div class="input-group">
              <label>Tipo de Alimento / Ração</label>
              <select v-model="formData.feed_type_id" required>
                <option value="" disabled>Selecione o alimento...</option>
                <option v-for="feed in feedTypesList" :key="feed.id" :value="feed.id">
                  {{ feed.name }}
                </option>
              </select>
            </div>

            <div class="input-group">
              <label>Quantidade Fornecida (kg)</label>
              <input v-model="formData.quantity" type="number" step="0.01" placeholder="Ex: 4.50" required>
            </div>

            <div class="input-group">
              <label>Data do Trato</label>
              <input v-model="formData.date_fed" type="date" required>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="loading">
              {{ loading ? 'Salvando...' : 'Confirmar Alimentação' }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const loading = ref(false);
const animalsList = ref([]);
const feedTypesList = ref([]);

const formData = ref({
  animal: '',
  feed_type_id: '',
  quantity: '',
  date_fed: new Date().toISOString().split('T')[0]
});

onMounted(() => {
  fetchData();
});

const fetchData = async () => {
  try {
    // Busca animais cadastrados
    const animRes = await api.get('animals/');
    animalsList.value = animRes.data.results || animRes.data;

    // Busca os tipos de alimentos cadastrados no backend
    const feedRes = await api.get('feeds/');
    feedTypesList.value = feedRes.data.results || feedRes.data;
  } catch (error) {
    console.error("Erro ao carregar dados do formulário nutricional:", error);
    // Fallback de segurança para testes
    feedTypesList.value = [
      { id: 1, name: 'Ração Concentrada 22%' },
      { id: 2, name: 'Silagem de Milho' },
      { id: 3, name: 'Suplemento Mineral' }
    ];
  }
};

const handleSubmit = async () => {
  loading.value = true;
  try {
    // Envia o registro do trato para o histórico do Django
    await api.post('historico-alimentacao/', formData.value);
    alert('Trato alimentar registrado com sucesso!');
    
    // Reseta o formulário mantendo apenas a data
    formData.value.animal = '';
    formData.value.feed_type_id = '';
    formData.value.quantity = '';
  } catch (error) {
    console.error(error);
    alert('Erro ao registrar alimentação no servidor.');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.page-wrapper { padding: 40px; background-color: #f8fafc; min-height: 100vh; font-family: 'Inter', sans-serif; color: #0f172a; }
.page-header { margin-bottom: 32px; }
.btn-back { background: transparent; border: 1px solid #e2e8f0; color: #64748b; padding: 8px 16px; border-radius: 8px; cursor: pointer; margin-bottom: 16px; font-weight: 500; transition: 0.2s; }
.btn-back:hover { background: #f1f5f9; color: #0f172a; }
.header-content h1 { font-size: 2rem; font-weight: 700; margin-bottom: 8px; }
.header-content p { color: #64748b; }

.content-container { max-width: 900px; }
.form-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
.card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; }
.card-header h2 { font-size: 1.25rem; font-weight: 600; }
.icon { font-size: 1.5rem; }

.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 24px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #475569; }
input, select { padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; outline: none; transition: 0.2s; background: white; font-family: inherit; }
input:focus, select:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1); }

.form-actions { display: flex; justify-content: flex-end; }
.btn-primary { background: #16a34a; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { background: #15803d; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
</style>