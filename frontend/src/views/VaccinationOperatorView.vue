<template>
  <div class="page-wrapper">
    <header class="page-header">
      <button @click="$router.back()" class="btn-back">← Voltar</button>
      <div class="header-content">
        <h1>Vacinação de Animais</h1>
        <p>Registre vacinações individuais ou em lote por Estábulo.</p>
      </div>
    </header>

    <div class="cards-grid">
      <section class="form-card">
        <header class="card-header">
          <h2>Vacinação Individual</h2>
          <span class="badge">Um por Um</span>
        </header>
        
        <form @submit.prevent="submitIndividual" class="data-form">
          <div class="input-group">
            <label>Selecione o Animal</label>
            <select v-model="individualForm.animal" required>
              <option value="" disabled>Escolha um animal...</option>
              <option v-for="animal in animalsList" :key="animal.id" :value="animal.id">
                {{ animal.name || 'Sem nome' }} (Brinco: #{{ animal.register_number }})
              </option>
            </select>
          </div>
          <div class="input-group mt-3">
            <label>Vacina Aplicada</label>
            <select v-model="individualForm.vaccine" required>
              <option value="" disabled>Selecione uma vacina...</option>
              <option v-for="vaccine in vaccinesList" :key="vaccine.id" :value="vaccine.id">
                {{ vaccine.name }}
              </option>
            </select>
          </div>
          <div class="input-group mt-3">
            <label>Dosagem Aplicada</label>
            <input v-model="individualForm.dosage" type="text" placeholder="Ex: 5 ml" required>
          </div>
          <div class="input-group mt-3">
            <label>Data de Aplicação</label>
            <input v-model="individualForm.date" type="date" required>
          </div>
          <button type="submit" class="btn-primary mt-4 w-100" :disabled="loadingInd">
            {{ loadingInd ? 'Salvando...' : 'Registrar Vacina' }}
          </button>
        </form>
      </section>

      <section class="form-card highlight-card">
        <header class="card-header">
          <h2>Vacinação por Estábulo</h2>
          <span class="badge highlight-badge">Lote Completo</span>
        </header>
        
        <form @submit.prevent="submitBatch" class="data-form">
          <div class="input-group">
            <label>Selecione o Estábulo</label>
            <select v-model="batchForm.quadrant" required>
              <option value="" disabled>Escolha um estábulo...</option>
              <option v-for="stable in stablesList" :key="stable.id" :value="stable.id">
                {{ stable.name || stable.nome_quadrante || `Estábulo ${stable.id}` }}
              </option>
            </select>
          </div>
          <div class="input-group mt-3">
            <label>Vacina Aplicada</label>
            <select v-model="batchForm.vaccine" required>
              <option value="" disabled>Selecione uma vacina...</option>
              <option v-for="vaccine in vaccinesList" :key="vaccine.id" :value="vaccine.id">
                {{ vaccine.name }}
              </option>
            </select>
          </div>
          <div class="input-group mt-3">
            <label>Dosagem Aplicada</label>
            <input v-model="batchForm.dosage" type="text" placeholder="Ex: 5 ml" required>
          </div>
          <div class="input-group mt-3">
            <label>Data de Aplicação</label>
            <input v-model="batchForm.date" type="date" required>
          </div>
          <button type="submit" class="btn-primary mt-4 w-100" :disabled="loadingBatch">
            {{ loadingBatch ? 'Processando Lote...' : 'Vacinar Lote Inteiro' }}
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const loadingInd = ref(false);
const loadingBatch = ref(false);

const vaccinesList = ref([]);
const stablesList = ref([]);
const animalsList = ref([]); // Nova lista para o dropdown de animais

const individualForm = ref({ 
  animal: '', 
  vaccine: '',
  dosage: '',
  date: new Date().toISOString().split('T')[0]
});

const batchForm = ref({ 
  quadrant: '', 
  vaccine: '', 
  dosage: '',
  date: new Date().toISOString().split('T')[0] 
});

onMounted(() => {
  fetchDropdownData();
});

const fetchDropdownData = async () => {
  try {
    // 1. Busca os animais para o novo dropdown
    api.get('animals/').then(res => {
      // Trata tanto a resposta paginada do Django quanto a direta
      animalsList.value = res.data.results || res.data;
    }).catch(e => console.error("Erro ao carregar animais", e));

    // 2. Busca as vacinas
    api.get('vaccines/').then(res => {
      vaccinesList.value = res.data.results || res.data;
    }).catch(() => {
      // Mock de segurança caso a rota não exista no backend ainda
      vaccinesList.value = [
        { id: 1, name: 'Febre Aftosa' }, 
        { id: 2, name: 'Brucelose' }, 
        { id: 3, name: 'Raiva' }
      ];
    });

    // 3. Busca os estábulos
    api.get('quadrants/').then(res => {
      stablesList.value = res.data.results || res.data;
    }).catch(() => {
      stablesList.value = [
        { id: 1, name: 'Estábulo Principal' }, 
        { id: 2, name: 'Estábulo Sul' }
      ];
    });
  } catch (e) {
    console.error(e);
  }
};

const submitIndividual = async () => {
  loadingInd.value = true;
  try {
    const payload = {
      animal: individualForm.value.animal,
      vaccine: individualForm.value.vaccine,
      vaccination_date: individualForm.value.date,
      dosage: individualForm.value.dosage
    };

    await api.post('vaccinations/', payload);
    
    alert("Vacina individual registrada com sucesso!");
    individualForm.value.animal = '';
    individualForm.value.vaccine = '';
    individualForm.value.dosage = '';
  } catch (error) {
    console.error(error);
    alert("Erro ao registrar a vacina. Verifique a conexão com o servidor.");
  } finally {
    loadingInd.value = false;
  }
};

const submitBatch = async () => {
  loadingBatch.value = true;
  try {
    const payload = {
      quadrant_id: batchForm.value.quadrant,
      vaccine_id: batchForm.value.vaccine,
      vaccination_date: batchForm.value.date,
      dosage: batchForm.value.dosage
    };

    await api.post('vaccinations/batch/', payload);
    
    alert("Lote vacinado com sucesso!");
    batchForm.value.quadrant = '';
    batchForm.value.vaccine = '';
    batchForm.value.dosage = '';
  } catch (error) {
    console.error(error);
    alert("Erro ao vacinar o lote no servidor.");
  } finally {
    loadingBatch.value = false;
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

.cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; max-width: 1000px; }
.form-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
.highlight-card { border-color: #cbd5e1; background: #f8fafc; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; }
.card-header h2 { font-size: 1.25rem; font-weight: 600; margin: 0; }
.badge { background: #f1f5f9; color: #475569; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
.highlight-badge { background: #dcfce7; color: #166534; }

.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #475569; }
input, select { padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; outline: none; transition: 0.2s; background: white; }
input:focus, select:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1); }

.mt-3 { margin-top: 16px; }
.mt-4 { margin-top: 24px; }
.w-100 { width: 100%; }

.btn-primary { background: #16a34a; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { background: #15803d; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
</style>