<template>
  <div class="pesagem-wrapper">
    <header class="page-header">
      <div class="header-content">
        <h1>Registro de Peso</h1>
        <p>Lance o peso do animal após a pesagem na balança (Regra RN09)</p>
      </div>
    </header>

    <div class="pesagem-container">
      <!-- FORMULÁRIO DE LANÇAMENTO -->
      <section class="glass-card entry-card">
        <header class="card-header">
          <span class="icon">⚖️</span>
          <h2>Nova Pesagem</h2>
        </header>

        <form @submit.prevent="handleSubmit" class="pesagem-form">
          <div class="form-grid">
            <div class="input-group">
              <label>ID do Animal (Brinco)</label>
              <input 
                v-model="formData.animal" 
                type="number" 
                placeholder="Ex: 142" 
                required
              >
            </div>

            <div class="input-group">
              <label>Peso (kg)</label>
              <input 
                v-model="formData.weight" 
                type="number" 
                step="0.1" 
                placeholder="0.0" 
                required
              >
            </div>

            <div class="input-group">
              <label>Data da Pesagem</label>
              <input 
                v-model="formData.weighing_date" 
                type="date" 
                required
              >
            </div>
          </div>

          <div class="form-footer">
            <p v-if="error" class="error-msg">{{ error }}</p>
            <button type="submit" class="btn-primary" :disabled="loading">
              {{ loading ? 'Salvando...' : 'Registrar Peso' }}
            </button>
          </div>
        </form>
      </section>

      <!-- RESUMO RÁPIDO DA ÚLTIMA PESAGEM -->
      <section class="glass-card summary-card">
        <h3>Última Pesagem</h3>
        <div class="total-display">
          <span class="amount">{{ lastWeightValue }}</span>
          <span class="unit">kg</span>
        </div>
        <p v-if="lastWeightDate" class="summary-date">{{ lastWeightDate }}</p>
        <div class="rule-box">
          <span class="rule-tag">RN09</span>
          <p>Pesagem permitida apenas para animais com status "Ativo".</p>
        </div>
      </section>
    </div>

    <!-- FEEDBACK TOAST -->
    <transition name="slide-up">
      <div v-if="success" class="toast-success">
        ✓ Peso registrado com sucesso!
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api';

const loading = ref(false);
const success = ref(false);
const error = ref(null);
const lastWeightValue = ref('0.0');
const lastWeightDate = ref(null);

const formData = ref({
  animal: null,
  weight: null,
  weighing_date: new Date().toISOString().split('T')[0]
});

const handleSubmit = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    // Consome a API do backend
    await api.registrarPeso(formData.value);
    
    success.value = true;
    lastWeightValue.value = formData.value.weight;
    lastWeightDate.value = new Date(formData.value.weighing_date).toLocaleDateString('pt-BR');
    
    // Limpa apenas o ID e o peso após sucesso
    formData.value.animal = null;
    formData.value.weight = null;
    
    setTimeout(() => success.value = false, 3000);
  } catch (err) {
    error.value = "Erro: Animal deve estar ATIVO ou ID não encontrado.";
    console.error('Erro ao registrar peso:', err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.pesagem-wrapper {
  padding: 40px;
  background-color: #0d1117;
  min-height: 100vh;
  color: #e6edf3;
}

.page-header {
  margin-bottom: 40px;
}

.page-header h1 {
  color: #3fb950;
  font-size: 2rem;
  margin-bottom: 10px;
}

.page-header p {
  color: #8b949e;
  margin-bottom: 20px;
}

.pesagem-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  max-width: 1200px;
}

.glass-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 30px;
}

.card-header .icon {
  font-size: 1.5rem;
}

.card-header h2 {
  font-size: 1.2rem;
  color: #e6edf3;
}

.pesagem-form {
  display: flex;
  flex-direction: column;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group label {
  font-size: 0.85rem;
  color: #8b949e;
  margin-bottom: 8px;
  font-weight: 600;
  text-transform: uppercase;
}

.input-group input {
  padding: 10px 12px;
  background-color: #0d1117;
  border: 1px solid #30363d;
  border-radius: 8px;
  color: #e6edf3;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.input-group input:focus {
  outline: none;
  border-color: #3fb950;
  box-shadow: 0 0 0 3px rgba(63, 185, 80, 0.1);
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.error-msg {
  color: #f85149;
  font-size: 0.9rem;
}

.btn-primary {
  padding: 12px 24px;
  background-color: #238636;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2ea043;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.summary-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.summary-card h3 {
  color: #8b949e;
  font-size: 0.9rem;
  text-transform: uppercase;
  margin-bottom: 15px;
}

.total-display {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 10px;
  margin-bottom: 10px;
}

.amount {
  font-size: 2.5rem;
  font-weight: bold;
  color: #3fb950;
}

.unit {
  font-size: 1rem;
  color: #8b949e;
}

.summary-date {
  font-size: 0.85rem;
  color: #8b949e;
  margin-bottom: 20px;
}

.rule-box {
  background-color: rgba(63, 185, 80, 0.1);
  border-left: 3px solid #3fb950;
  padding: 15px;
  border-radius: 4px;
  margin-top: 20px;
}

.rule-tag {
  font-weight: 700;
  color: #3fb950;
  font-size: 0.8rem;
}

.rule-box p {
  margin-top: 8px;
  font-size: 0.85rem;
  color: #8b949e;
}

.toast-success {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #238636;
  color: #ffffff;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(35, 134, 54, 0.3);
  z-index: 1000;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from {
  transform: translateX(-50%) translateY(30px);
  opacity: 0;
}

.slide-up-leave-to {
  transform: translateX(-50%) translateY(30px);
  opacity: 0;
}

@media (max-width: 768px) {
  .pesagem-wrapper {
    padding: 20px;
  }

  .pesagem-container {
    grid-template-columns: 1fr;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }
}
</style>
