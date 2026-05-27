<template>
  <div class="page-wrapper">
    <header class="page-header">
      <button @click="$router.back()" class="btn-back">← Voltar</button>
      <div class="header-content">
        <h1>Registro de Peso</h1>
        <p>Acompanhe e registre a evolução de peso dos animais.</p>
      </div>
    </header>

    <div class="content-container">
      <section class="form-card">
        <header class="card-header">
          <span class="icon">⚖️</span>
          <h2>Nova Pesagem</h2>
        </header>

        <form @submit.prevent="handleSubmit" class="data-form">
          <div class="form-grid">
            <div class="input-group">
              <label>Animal</label>
              <select v-model.number="formData.animal" required>
                <option value="" disabled>Selecione um animal...</option>
                <option v-for="animal in animals" :key="animal.id" :value="animal.id">
                  {{ animal.name || 'Sem nome' }} (Brinco: #{{ animal.register_number }})
                </option>
              </select>
            </div>
            <div class="input-group">
              <label>Peso (kg)</label>
              <input v-model="formData.weight" type="number" step="0.1" placeholder="Ex: 450.5" required>
            </div>
            <div class="input-group">
              <label>Data da Pesagem</label>
              <input v-model="formData.weighing_date" type="date" required>
            </div>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="loading">
              {{ loading ? 'Salvando...' : 'Confirmar Peso' }}
            </button>
          </div>
        </form>
        <p v-if="message" :class="{'msg-success': isSuccess, 'msg-error': !isSuccess}">
          {{ message }}
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const loading = ref(false);
const message = ref('');
const isSuccess = ref(false);
const animals = ref([]);

const formData = ref({
  animal: '',
  weight: '',
  weighing_date: new Date().toISOString().split('T')[0]
});

const loadAnimals = async () => {
  try {
    const response = await api.getAnimals();
    animals.value = response.data.results || response.data;
  } catch (error) {
    console.error('Erro ao carregar animais:', error);
    animals.value = [];
  }
};

const handleSubmit = async () => {
  loading.value = true;
  message.value = '';
  try {
    const payload = {
      animal: parseInt(formData.value.animal, 10),
      weight: parseFloat(formData.value.weight),
      weighing_date: formData.value.weighing_date
    };
    await api.registrarPeso(payload);
    isSuccess.value = true;
    message.value = 'Pesagem registrada com sucesso!';
    formData.value.animal = '';
    formData.value.weight = '';
    formData.value.weighing_date = new Date().toISOString().split('T')[0];
  } catch (error) {
    console.error('Erro ao salvar pesagem:', error.response?.data || error);
    isSuccess.value = false;
    message.value = 'Erro ao registrar pesagem. Verifique os dados.';
  } finally {
    loading.value = false;
    setTimeout(() => { message.value = ''; }, 4000);
  }
};

onMounted(loadAnimals);
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.page-wrapper { padding: 40px; background-color: #f8fafc; min-height: 100vh; font-family: 'Inter', sans-serif; color: #0f172a; }
.page-header { margin-bottom: 32px; }
.btn-back { background: transparent; border: 1px solid #e2e8f0; color: #64748b; padding: 8px 16px; border-radius: 8px; cursor: pointer; margin-bottom: 16px; font-weight: 500; transition: 0.2s; }
.btn-back:hover { background: #f1f5f9; color: #0f172a; }
.header-content h1 { font-size: 2rem; font-weight: 700; margin-bottom: 8px; }
.header-content p { color: #64748b; }
.content-container { max-width: 800px; }
.form-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
.card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; }
.card-header h2 { font-size: 1.25rem; font-weight: 600; }
.icon { font-size: 1.5rem; }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 24px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #475569; }
input { padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; outline: none; transition: 0.2s; }
input:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1); }
.form-actions { display: flex; justify-content: flex-end; }
.btn-primary { background: #16a34a; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { background: #15803d; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.msg-success { color: #16a34a; margin-top: 16px; font-weight: 500; }
.msg-error { color: #ef4444; margin-top: 16px; font-weight: 500; }
</style>