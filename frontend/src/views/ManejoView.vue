<template>
  <div class="manejo-wrapper">
    <header class="page-header">
      <h1>Registro de Manejo</h1>
      <p>Lance os dados coletados diretamente no campo</p>
    </header>

    <div class="manejo-grid">
      <!-- CARD DE PESAGEM -->
      <section class="action-card">
        <div class="card-icon weight-icon">⊡</div>
        <h2>Registrar Pesagem</h2>
        <p class="description">Informe o brinco do animal e o peso atual medido na balança.</p>
        
        <form @submit.prevent="handleWeight" class="manejo-form">
          <div class="form-group">
            <label>ID do Animal (Brinco)</label>
            <input v-model="weightData.animal" type="number" placeholder="Ex: 142" required>
          </div>
          <div class="form-group">
            <label>Peso (kg)</label>
            <input v-model="weightData.weight" type="number" step="0.01" placeholder="000.00" required>
          </div>
          <button type="submit" class="btn-submit weight-btn" :disabled="loading">
            {{ loading ? 'Salvando...' : 'Confirmar Peso' }}
          </button>
        </form>
      </section>

      <!-- CARD DE VACINAÇÃO (REQUISITO 6.1) -->
      <section class="action-card">
        <div class="card-icon vaccine-icon">✛</div>
        <h2>Aplicar Vacina</h2>
        <p class="description">Registre a aplicação de uma vacina com data da próxima dose.</p>
        
        <form @submit.prevent="handleVaccine" class="manejo-form">
          <div class="form-group">
            <label>ID do Animal (Brinco) *</label>
            <input v-model.number="vaccineData.animal" type="number" placeholder="Ex: 142" required>
          </div>
          
          <div class="form-group">
            <label>Nome da Vacina *</label>
            <select v-model="vaccineData.vaccine" required>
              <option value="">Selecione a vacina...</option>
              <option v-for="vaccine in vaccines" :key="vaccine.id" :value="vaccine.id">
                {{ vaccine.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Data da Aplicação *</label>
            <input v-model="vaccineData.vaccination_date" type="date" required>
          </div>

          <div class="form-group">
            <label>Data da Próxima Dose *</label>
            <input v-model="vaccineData.next_vaccination_date" type="date" required>
          </div>

          <div class="form-group">
            <label>Dosagem (mL) *</label>
            <input v-model.number="vaccineData.dosage" type="number" step="0.01" placeholder="Ex: 5.00" required>
          </div>

          <button type="submit" class="btn-submit vaccine-btn" :disabled="loading">
            {{ loading ? 'Registrando...' : 'Registrar Vacinação' }}
          </button>
        </form>
      </section>
    </div>

    <!-- Feedback de Sucesso/Erro -->
    <transition name="fade">
      <div v-if="feedback.show" :class="['alert-toast', feedback.type]">
        {{ feedback.message }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import manejoService from '@/services/manejoService';
import api from '@/services/api';

const loading = ref(false);
const plans = ref([]);
const vaccines = ref([]);
const feedback = ref({ show: false, message: '', type: '' });

const weightData = ref({ 
  animal: null, 
  weight: null, 
  date: new Date().toISOString().split('T')[0] 
});

const vaccineData = ref({ 
  animal: null, 
  vaccine: '',
  vaccination_date: new Date().toISOString().split('T')[0],
  next_vaccination_date: '',
  dosage: null,
  vaccination_plan: '',
  date: new Date().toISOString().split('T')[0]
});

onMounted(async () => {
  try {
    const [resPlans, resVaccines] = await Promise.all([
      manejoService.getPlanosVacina(),
      api.getVaccines()
    ]);
    plans.value = resPlans.data || [];
    vaccines.value = resVaccines.data || [];
  } catch (error) {
    console.error("Erro ao buscar dados:", error);
  }
});

const showFeedback = (msg, type) => {
  feedback.value = { show: true, message: msg, type: type };
  setTimeout(() => feedback.value.show = false, 3000);
};

const handleWeight = async () => {
  loading.value = true;
  try {
    await manejoService.registrarPeso(weightData.value);
    showFeedback("Peso registrado com sucesso!", "success");
    weightData.value = { animal: null, weight: null, date: new Date().toISOString().split('T')[0] };
  } catch (error) {
    showFeedback("Erro ao registrar peso. Verifique o ID.", "error");
  } finally {
    loading.value = false;
  }
};

const handleVaccine = async () => {
  // Validação
  if (!vaccineData.value.animal || !vaccineData.value.vaccine || !vaccineData.value.vaccination_date || !vaccineData.value.next_vaccination_date || !vaccineData.value.dosage) {
    showFeedback("Preencha todos os campos obrigatórios!", "error");
    return;
  }

  loading.value = true;
  try {
    const payload = {
      animal: vaccineData.value.animal,
      vaccine: vaccineData.value.vaccine,
      vaccination_date: vaccineData.value.vaccination_date,
      next_vaccination_date: vaccineData.value.next_vaccination_date,
      dosage: vaccineData.value.dosage,
      vaccination_status: true
    };
    
    await api.createVaccination(payload);
    showFeedback("Vacinação registrada com sucesso!", "success");
    vaccineData.value = { 
      animal: null, 
      vaccine: '',
      vaccination_date: new Date().toISOString().split('T')[0],
      next_vaccination_date: '',
      dosage: null,
      vaccination_plan: '',
      date: new Date().toISOString().split('T')[0]
    };
  } catch (error) {
    console.error("Erro ao registrar vacina:", error);
    showFeedback("Erro ao registrar vacinação. Verifique os dados.", "error");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.manejo-wrapper {
  padding: 40px;
  background-color: #0d1117; /* Fundo Dark Tech[cite: 13] */
  min-height: 100vh;
  color: #e6edf3;
}

.page-header { margin-bottom: 40px; }
.page-header h1 { color: #58a6ff; font-size: 2rem; margin-bottom: 10px; }
.page-header p { color: #8b949e; }

.manejo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  max-width: 1200px;
}

.action-card {
  background: #161b22; /* Fundo do card[cite: 13] */
  border: 1px solid #30363d; /* Borda solicitada */
  border-radius: 16px;
  padding: 30px;
  transition: transform 0.3s ease;
}

.action-card:hover { border-color: #58a6ff; }

.card-icon {
  font-size: 2rem;
  margin-bottom: 20px;
}
.weight-icon { color: #3fb950; }
.vaccine-icon { color: #f85149; }

.description { color: #8b949e; font-size: 0.9rem; margin-bottom: 25px; line-height: 1.5; }

.manejo-form { display: flex; flex-direction: column; gap: 20px; }

.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { font-size: 0.85rem; font-weight: 600; color: #c9d1d9; }

input, select {
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 12px;
  color: white;
  outline: none;
}

input:focus, select:focus { border-color: #58a6ff; box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.2); }

.btn-submit {
  padding: 14px;
  border-radius: 8px;
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s;
  margin-top: 10px;
}

.weight-btn { background: #238636; color: white; }
.weight-btn:hover { background: #2ea043; }

.vaccine-btn { background: #f85149; color: white; }
.vaccine-btn:hover { background: #da3633; }

.alert-toast {
  position: fixed; bottom: 30px; right: 40px;
  padding: 15px 30px; border-radius: 8px;
  font-weight: bold; z-index: 10000;
}
.success { background: #238636; color: white; }
.error { background: #f85149; color: white; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.5s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>