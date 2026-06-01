<template>
  <div class="page-wrapper">
    <header class="page-header">
      <button @click="$router.back()" class="btn-back">← Voltar</button>
      <div class="header-content">
        <h1>Registro de Ordenha</h1>
        <p>Lance a produção diária de leite individual do rebanho.</p>
      </div>
    </header>

    <div class="content-container">
      <section class="form-card">
        <header class="card-header">
          <span class="icon">🥛</span>
          <h2>Nova Entrada de Leite</h2>
        </header>

        <form @submit.prevent="handleSubmit" class="data-form">
          <div class="form-grid">
            <div class="input-group">
              <label>Animal</label>
              <select v-model.number="formData.animal" required :disabled="femaleAnimals.length === 0">
                <option value="" disabled>
                  {{ femaleAnimals.length > 0 ? 'Selecione um animal...' : 'Nenhuma fêmea cadastrada disponível' }}
                </option>
                <option v-for="animal in femaleAnimals" :key="animal.id" :value="animal.id">
                  {{ animal.name || 'Sem nome' }} (Brinco: #{{ animal.register_number }})
                </option>
              </select>
            </div>
            <div class="input-group">
              <label>Quantidade (Litros)</label>
              <input v-model="formData.milk_production" type="number" step="0.1" placeholder="Ex: 15.5" required>
            </div>
            <div class="input-group">
              <label>Data da Coleta</label>
              <input v-model="formData.production_date" type="date" required>
            </div>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="loading || femaleAnimals.length === 0">
              {{ loading ? 'Salvando...' : 'Registrar Ordenha' }}
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
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';

const loading = ref(false);
const message = ref('');
const isSuccess = ref(false);
const animals = ref([]);

const isFemaleAnimal = (animalData) => String(animalData?.sex || '').toLowerCase() === 'f';
const femaleAnimals = computed(() => animals.value.filter(isFemaleAnimal));

const formData = ref({
  animal: '',
  milk_production: '',
  production_date: new Date().toISOString().split('T')[0]
});

onMounted(async () => {
  try {
    const res = await api.get('animals/');
    animals.value = (res.data.results || res.data).filter(isFemaleAnimal);
  } catch (error) {
    console.error('Erro ao carregar animais para ordenha:', error);
    animals.value = [];
  }
});

const handleSubmit = async () => {
  loading.value = true;
  message.value = '';
  try {
    const payload = {
      animal: parseInt(formData.value.animal),
      milk_production: parseFloat(formData.value.milk_production),
      production_date: formData.value.production_date
    };
    await api.post('milk_production_history/', payload);
    isSuccess.value = true;
    message.value = 'Ordenha registrada com sucesso!';
    formData.value.animal = '';
    formData.value.milk_production = '';
    formData.value.production_date = new Date().toISOString().split('T')[0];
  } catch (error) {
    console.error('Erro ao salvar ordenha:', error);
    console.error('Resposta do servidor:', error.response?.data);
    isSuccess.value = false;
    message.value = 'Erro ao registrar ordenha. Verifique os dados.';
  } finally {
    loading.value = false;
    setTimeout(() => { message.value = ''; }, 4000);
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
.content-container { max-width: 800px; }
.form-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
.card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; }
.card-header h2 { font-size: 1.25rem; font-weight: 600; }
.icon { font-size: 1.5rem; }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 24px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #475569; }
input, select { padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; outline: none; transition: 0.2s; background: white; font-family: inherit; color: #0f172a; }
input:focus, select:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1); }
select option { background: white; color: #0f172a; }
.form-actions { display: flex; justify-content: flex-end; }
.btn-primary { background: #16a34a; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { background: #15803d; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.msg-success { color: #16a34a; margin-top: 16px; font-weight: 500; }
.msg-error { color: #ef4444; margin-top: 16px; font-weight: 500; }
</style>