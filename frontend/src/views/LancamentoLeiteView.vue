<template>
  <div class="production-wrapper">
    <header class="page-header">
      <div class="header-content">
        <h1>Registro de Ordenha</h1>
        <p>Lance a produção diária individual por animal (Regra RN08)</p>
      </div>
    </header>

    <div class="production-container">
      <!-- FORMULÁRIO DE LANÇAMENTO -->
      <section class="glass-card entry-card">
        <header class="card-header">
          <span class="icon">🥛</span>
          <h2>Nova Entrada</h2>
        </header>

        <form @submit.prevent="handleSubmit" class="production-form">
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
              <label>Quantidade (Litros)</label>
              <input 
                v-model="formData.milk_quantity" 
                type="number" 
                step="0.1" 
                placeholder="0.0" 
                required
              >
            </div>

            <div class="input-group">
              <label>Data da Coleta</label>
              <input 
                v-model="formData.date" 
                type="date" 
                required
              >
            </div>
          </div>

          <div class="form-footer">
            <p v-if="error" class="error-msg">{{ error }}</p>
            <button type="submit" class="btn-primary" :disabled="loading">
              {{ loading ? 'Salvando...' : 'Registrar Produção' }}
            </button>
          </div>
        </form>
      </section>

      <!-- RESUMO RÁPIDO DO DIA -->
      <section class="glass-card summary-card">
        <h3>Total da Última Ordenha</h3>
        <div class="total-display">
          <span class="amount">{{ totalToday }}</span>
          <span class="unit">Litros</span>
        </div>
        <div class="rule-box">
          <span class="rule-tag">RN08</span>
          <p>Produção permitida apenas para animais com status "Ativo".</p>
        </div>
      </section>
    </div>

    <!-- FEEDBACK TOAST -->
    <transition name="slide-up">
      <div v-if="success" class="toast-success">
        ✓ Lançamento realizado com sucesso!
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import animalService from '@/services/animalService';

const loading = ref(false);
const success = ref(false);
const error = ref(null);
const totalToday = ref(0); // Mock ou calculado via API futuramente

const formData = ref({
  animal: null,
  milk_quantity: null,
  date: new Date().toISOString().split('T')[0]
});

const handleSubmit = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    // Consome a API do seu backend[cite: 17, 27]
    await animalService.registrarProducaoLeite(formData.value);
    
    success.value = true;
    totalToday.value += parseFloat(formData.value.milk_quantity);
    
    // Limpa apenas o ID e a quantidade após sucesso
    formData.value.animal = null;
    formData.value.milk_quantity = null;
    
    setTimeout(() => success.value = false, 3000);
  } catch (err) {
    error.value = "Erro: Animal deve estar ATIVO ou ID não encontrado.";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.production-wrapper {
  padding: 40px;
  background-color: #0d1117; /* Fundo Dark Tech */
  min-height: 100vh;
  color: #e6edf3;
}

.page-header h1 { color: #3fb950; font-size: 2rem; margin-bottom: 10px; }
.page-header p { color: #8b949e; margin-bottom: 40px; }

.production-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  max-width: 1200px;
}

.glass-card {
  background: #161b22;
  border: 1px solid #30363d; /* Bordas sutis[cite: 13] */
  border-radius: 16px;
  padding: 30px;
}

.card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 30px; }
.card-header .icon { font-size: 1.5rem; }

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.85rem; color: #8b949e; font-weight: 600; }

input {
  background: #0d1117;
  border: 1px solid #30363d;
  color: white;
  padding: 12px;
  border-radius: 8px;
  outline: none;
}

input:focus { border-color: #3fb950; }

.btn-primary {
  background: #238636;
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s;
}

.btn-primary:hover { background: #2ea043; }

.total-display { text-align: center; margin: 30px 0; }
.total-display .amount { font-size: 4rem; font-weight: 800; color: #3fb950; display: block; }
.total-display .unit { color: #8b949e; text-transform: uppercase; }

.rule-box {
  background: rgba(88, 166, 255, 0.1);
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #58a6ff;
}

.rule-tag { font-weight: 800; font-size: 0.7rem; color: #58a6ff; display: block; margin-bottom: 5px; }
.rule-box p { font-size: 0.8rem; color: #c9d1d9; }

.error-msg { color: #f85149; font-size: 0.85rem; margin-bottom: 10px; }

.toast-success {
  position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
  background: #238636; color: white; padding: 12px 24px; border-radius: 50px;
  font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}
</style>