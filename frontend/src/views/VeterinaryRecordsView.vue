<template>
  <div class="page-wrapper">
    <header class="page-header">
      <button @click="$router.back()" class="btn-back">← Voltar</button>
      <div class="header-content">
        <h1>Registro Veterinário</h1>
        <p>Cadastrar e consultar atendimentos veterinários por animal.</p>
      </div>
    </header>

    <section class="form-card">
      <header class="card-header">
        <h2>Novo Registro de Consulta</h2>
      </header>

      <form @submit.prevent="submitRecord" class="data-form">
        <div class="form-grid">
          <div class="input-group">
            <label>Animal</label>
            <select v-model="formData.animal" required>
              <option value="" disabled>Selecione um animal...</option>
              <option v-for="animal in animalsList" :key="animal.id" :value="animal.id">
                {{ animal.name || 'Sem nome' }} (Brinco: #{{ animal.register_number }})
              </option>
            </select>
          </div>

          <div class="input-group">
            <label>Veterinário</label>
            <input v-model="formData.veterinarian" type="text" placeholder="Nome do veterinário" required />
          </div>

          <div class="input-group">
            <label>Data da Consulta</label>
            <input v-model="formData.consultation_date" type="date" required />
          </div>

          <div class="input-group full-width">
            <label>Motivo da Consulta</label>
            <textarea v-model="formData.consultation_reason" rows="3" placeholder="Descreva o motivo da consulta" required></textarea>
          </div>

          <div class="input-group full-width">
            <label>Tratativa / Solução</label>
            <textarea v-model="formData.consultation_solution" rows="4" placeholder="Descreva a solução, tratamento e acompanhamento" required></textarea>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="saving">
            {{ saving ? 'Salvando...' : 'Registrar Consulta' }}
          </button>
        </div>
      </form>
    </section>

    <section class="report-card" v-if="records.length > 0">
      <header class="card-header-inline">
        <h2>Consultas Registradas</h2>
        <span class="badge">{{ records.length }} registros</span>
      </header>

      <div class="table-responsive">
        <table class="data-table">
          <thead>
            <tr>
              <th>Data</th>
              <th>Animal</th>
              <th>Veterinário</th>
              <th>Motivo</th>
              <th>Solução</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in records" :key="record.id">
              <td>{{ formatDate(record.consultation_date) }}</td>
              <td>#{{ record.animal }} - {{ record.animal_name || 'Sem nome' }}</td>
              <td>{{ record.veterinarian }}</td>
              <td>{{ record.consultation_reason }}</td>
              <td>{{ record.consultation_solution }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <div v-if="loading && records.length === 0" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando histórico veterinário...</p>
    </div>

    <div v-if="!loading && records.length === 0" class="empty-state">
      <p>Nenhum registro veterinário encontrado ainda.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const loading = ref(true);
const saving = ref(false);
const animalsList = ref([]);
const records = ref([]);

const formData = ref({
  animal: '',
  veterinarian: '',
  consultation_date: new Date().toISOString().split('T')[0],
  consultation_reason: '',
  consultation_solution: ''
});

const loadAnimals = async () => {
  try {
    const response = await api.getAnimals();
    animalsList.value = response.data.results || response.data;
  } catch (error) {
    console.error('Erro ao carregar animais:', error);
    animalsList.value = [];
  }
};

const loadRecords = async () => {
  loading.value = true;
  try {
    const response = await api.getVeterinaryRecords();
    records.value = response.data.results || response.data;
  } catch (error) {
    console.error('Erro ao carregar registros veterinários:', error);
    records.value = [];
  } finally {
    loading.value = false;
  }
};

const submitRecord = async () => {
  saving.value = true;
  try {
    await api.createVeterinaryRecord(formData.value);
    alert('Consulta veterinária registrada com sucesso!');
    formData.value = {
      animal: '',
      veterinarian: '',
      consultation_date: new Date().toISOString().split('T')[0],
      consultation_reason: '',
      consultation_solution: ''
    };
    await loadRecords();
  } catch (error) {
    console.error('Erro ao salvar registro:', error);
    alert('Erro ao salvar consulta veterinária.');
  } finally {
    saving.value = false;
  }
};

const formatDate = (value) => {
  if (!value) return 'N/A';
  return new Date(value).toLocaleDateString('pt-BR');
};

onMounted(async () => {
  await Promise.all([loadAnimals(), loadRecords()]);
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700;800&display=swap');

.page-wrapper { padding: 40px; background-color: #f8fafc; min-height: 100vh; font-family: 'Lexend', sans-serif; color: #0f172a; }
.page-header { margin-bottom: 32px; display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; }
.header-content h1 { font-size: 2rem; margin: 0 0 8px; }
.header-content p { color: #64748b; margin: 0; }
.btn-back { background: transparent; border: 1px solid #e2e8f0; color: #64748b; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 500; }
.btn-back:hover { background: #f1f5f9; color: #0f172a; }

.form-card, .report-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 32px; }
.card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
.card-header h2 { font-size: 1.25rem; margin: 0; }

.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group.full-width { grid-column: 1 / -1; }
label { font-size: 0.95rem; color: #475569; font-weight: 600; }
input, textarea, select { width: 100%; padding: 12px 14px; border: 1px solid #cbd5e1; border-radius: 10px; font-family: inherit; font-size: 0.95rem; outline: none; }
input:focus, textarea:focus, select:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22,163,74,0.12); }

.form-actions { display: flex; justify-content: flex-end; margin-top: 20px; }
.btn-primary { background: #16a34a; color: white; border: none; padding: 12px 24px; border-radius: 10px; font-weight: 700; cursor: pointer; }
.btn-primary:disabled { opacity: 0.65; cursor: not-allowed; }

.table-responsive { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th, .data-table td { padding: 16px; border-bottom: 1px solid #e2e8f0; }
.data-table th { background: #f8fafc; color: #64748b; font-size: 0.8rem; text-transform: uppercase; }
.badge { background: #f1f5f9; color: #475569; padding: 6px 12px; border-radius: 999px; font-size: 0.82rem; font-weight: 600; }

.loading-state, .empty-state { text-align: center; padding: 40px; color: #64748b; }
.spinner { width: 32px; height: 32px; border: 4px solid #e2e8f0; border-top-color: #16a34a; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 18px; }
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>
