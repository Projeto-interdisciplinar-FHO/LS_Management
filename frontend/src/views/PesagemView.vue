<template>
  <div class="taxonomy-page">
    <header class="page-header">
      <div class="header-copy">
        <button @click="goHome" class="btn-back">← Voltar ao Dashboard</button>
        <h1>Registro de peso</h1>
        <p>Acompanhe e registre a evolução de peso dos animais.</p>
      </div>
    </header>

    <section class="content-card">
      <div class="section-header">
        <div>
          <h2>Nova pesagem</h2>
          <p>Registre o peso de um animal com os dados técnicos do acompanhamento.</p>
        </div>
        <span class="count-badge">Formulário ativo</span>
      </div>

      <form @submit.prevent="handleSubmit" class="taxonomy-form">
        <div class="input-grid">
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
            <label>Data da pesagem</label>
            <input v-model="formData.weighing_date" type="date" required>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? 'Salvando...' : 'Confirmar peso' }}
          </button>
        </div>
      </form>

      <p v-if="message" :class="['form-status', isSuccess ? 'success' : 'error']">
        {{ message }}
      </p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

const goHome = () => {
  const role = localStorage.getItem('user_role');
  if (role === 'op') router.push('/dashboard-op');
  else router.push('/dashboard-adm');
};
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
    setTimeout(() => {
      message.value = '';
    }, 4000);
  }
};

onMounted(loadAnimals);
</script>

<style scoped>
.taxonomy-page {
  min-height: 100vh;
  background: #f8fafc;
  color: #0f172a;
  font-family: 'Lexend', sans-serif;
  padding: 32px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}

.header-copy h1 {
  margin: 12px 0 8px;
  font-size: 2rem;
}

.header-copy p {
  margin: 0;
  color: #64748b;
}

.btn-back {
  background: transparent;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  color: #64748b;
  padding: 8px 12px;
  cursor: pointer;
}

.content-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
  max-width: 860px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0 0 6px;
  font-size: 1.25rem;
}

.section-header p {
  margin: 0;
  color: #64748b;
}

.count-badge {
  background: #f0fdf4;
  color: #16a34a;
  border-radius: 999px;
  padding: 6px 16px;
  font-weight: 700;
  font-size: 0.95rem;
}

.taxonomy-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 18px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #475569;
}

input,
select {
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
  transition: 0.2s;
  background: #fff;
}

input:focus,
select:focus {
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  background: #16a34a;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 12px 18px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #15803d;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-status {
  margin-top: 12px;
  font-weight: 600;
}

.form-status.success {
  color: #16a34a;
}

.form-status.error {
  color: #ef4444;
}
</style>
