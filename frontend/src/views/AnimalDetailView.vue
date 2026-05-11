<template>
  <div class="detail-wrapper" v-if="animal && !loading">
    <header class="detail-header">
      <div class="nav-actions">
        <button @click="$router.back()" class="btn-back">← Voltar para a Lista</button>
      </div>
      <div class="animal-hero">
        <h1>{{ animal.name }}</h1>
        <span class="reg-number">Registro: {{ animal.register_number }}</span>
      </div>
    </header>

    <div class="detail-content">
      <section class="info-card">
        <div class="card-title">Dados Gerais</div>
        <div class="data-grid">
          <div class="data-item">
            <span class="label">Data de Nascimento</span>
            <span class="value">{{ new Date(animal.birth_date).toLocaleDateString('pt-BR') }}</span>
          </div>
          <div class="data-item">
            <span class="label">Sexo</span>
            <span class="value">{{ animal.sex === 'm' || animal.sex === 'M' ? 'Macho' : 'Fêmea' }}</span>
          </div>
          <div class="data-item">
            <span class="label">Peso</span>
            <span class="value">{{ animal.weight }} kg</span>
          </div>
          <div class="data-item">
            <span class="label">Status Atual</span>
            <span class="value status-badge" :class="{ 'active': animal.active }">
              {{ animal.active ? 'Ativo' : 'Inativo' }}
            </span>
          </div>
        </div>
      </section>

      <section class="info-card">
        <div class="card-title">Informações Cadastrais</div>
        <div class="data-grid">
          <div class="data-item">
            <span class="label">Espécie (ID)</span>
            <span class="value">{{ animal.specie }}</span>
          </div>
          <div class="data-item">
            <span class="label">Raça (ID)</span>
            <span class="value">{{ animal.breed || 'N/A' }}</span>
          </div>
          <div class="data-item">
            <span class="label">Quadrante (ID)</span>
            <span class="value">{{ animal.quadrant }}</span>
          </div>
          <div class="data-item">
            <span class="label">Tipo de Propósito (ID)</span>
            <span class="value">{{ animal.purpose }}</span>
          </div>
        </div>
      </section>

      <section class="info-card side-card">
        <div class="card-title">Ações</div>
        <div class="manejo-info">
          <p>Monitoramento de produção e vacinação sincronizados com a ficha individual.</p>
          <button class="btn-action">Registrar Ordenha</button>
        </div>
      </section>
    </div>
  </div>
  
  <div v-else class="loading-state">
    <div class="spinner"></div>
    <p>Carregando ficha do animal...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/services/api';

const route = useRoute();
const animal = ref(null);
const loading = ref(true);

const fetchAnimalDetails = async () => {
  const id = route.params.id;
  console.log("Buscando animal com ID:", id);
  try {
    const response = await api.getAnimalById(parseInt(id));
    console.log("Resposta recebida:", response.data);
    animal.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar detalhes do animal:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchAnimalDetails();
});
</script>

<style scoped>
.detail-wrapper {
  padding: 40px;
  background-color: #0d1117;
  min-height: 100vh;
  color: #e6edf3;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #0d1117;
  gap: 20px;
  color: #8b949e;
}

.spinner {
  border: 3px solid #30363d;
  border-top: 3px solid #58a6ff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.detail-header {
  margin-bottom: 40px;
}

.nav-actions {
  margin-bottom: 20px;
}

.btn-back {
  background: transparent;
  border: 1px solid #30363d;
  color: #8b949e;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-back:hover {
  border-color: #58a6ff;
  color: #58a6ff;
}

.animal-hero { 
  margin-bottom: 40px; 
}

.animal-hero h1 { 
  font-size: 2.5rem; 
  color: #3fb950; 
  margin-bottom: 5px; 
}

.reg-number { 
  color: #58a6ff; 
  font-family: monospace; 
}

.detail-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.info-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 24px;
}

.info-card.side-card {
  grid-column: 1 / -1;
}

.card-title {
  font-size: 0.9rem;
  text-transform: uppercase;
  color: #8b949e;
  letter-spacing: 1px;
  margin-bottom: 25px;
  border-bottom: 1px solid #30363d;
  padding-bottom: 10px;
}

.data-grid { 
  display: grid; 
  grid-template-columns: 1fr 1fr; 
  gap: 25px; 
}

.data-item { 
  display: flex; 
  flex-direction: column; 
  gap: 5px; 
}

.data-item .label { 
  color: #484f58; 
  font-size: 0.8rem; 
}

.data-item .value { 
  font-size: 1.1rem; 
  font-weight: 500; 
  color: #e6edf3;
}

.status-badge { 
  color: #f85149; 
  font-weight: bold; 
}

.status-badge.active { 
  color: #3fb950; 
}

.manejo-info {
  padding: 15px 0;
}

.manejo-info p {
  margin: 0 0 15px 0;
  color: #8b949e;
  font-size: 0.95rem;
}

.btn-action {
  width: 100%;
  padding: 12px;
  background: rgba(88, 166, 255, 0.1);
  border: 1px solid #58a6ff;
  color: #58a6ff;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-action:hover {
  background: rgba(88, 166, 255, 0.2);
  box-shadow: 0 0 10px rgba(88, 166, 255, 0.3);
}

@media (max-width: 768px) {
  .detail-content {
    grid-template-columns: 1fr;
  }
  
  .animal-hero h1 {
    font-size: 1.8rem;
  }
  
  .data-grid {
    grid-template-columns: 1fr;
  }
}
</style>