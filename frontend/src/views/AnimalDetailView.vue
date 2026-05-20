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
            <div class="value" style="display: flex; align-items: center;">
              <StatusBadge :status="animal.status || 'inativo'" size="md" />
            </div>
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

      <!-- SEÇÃO 3.1 e 3.2 - HISTÓRICO DE PRODUÇÃO DE LEITE -->
      <section class="info-card production-card" v-if="animal.purpose === 1">
        <div class="card-title">🥛 Histórico de Produção de Leite</div>
        
        <!-- Resumo - Requisito 3.1 -->
        <div v-if="productionResumo" class="production-resume">
          <div class="resume-item">
            <span class="resume-label">Última Ordenha</span>
            <span class="resume-value">{{ productionResumo.ultima_ordenha?.milk_production || '0' }} L</span>
            <span class="resume-date" v-if="productionResumo.ultima_ordenha">
              {{ new Date(productionResumo.ultima_ordenha.production_date).toLocaleDateString('pt-BR') }}
            </span>
          </div>
          <div class="resume-item">
            <span class="resume-label">Total na Semana</span>
            <span class="resume-value">{{ productionResumo.total_semana }} L</span>
          </div>
          <div class="resume-item">
            <span class="resume-label">Total no Mês</span>
            <span class="resume-value">{{ productionResumo.total_mes }} L</span>
          </div>
          <div class="resume-item">
            <span class="resume-label">Total Geral</span>
            <span class="resume-value">{{ productionResumo.total_geral }} L</span>
          </div>
        </div>

        <!-- Carregando -->
        <div v-if="loadingProduction" class="loading-mini">
          <div class="spinner-mini"></div>
          <p>Carregando histórico de produção...</p>
        </div>

        <!-- Histórico - Requisito 3.2 -->
        <div v-else-if="productionResumo && productionResumo.historico.length > 0" class="production-history">
          <h4 style="margin-top: 20px; margin-bottom: 10px; color: #e6edf3;">Histórico Completo</h4>
          <div class="history-table">
            <div class="table-header">
              <div class="col-date">Data</div>
              <div class="col-amount">Quantidade (L)</div>
            </div>
            <div v-for="producao in productionResumo.historico" :key="producao.id" class="table-row">
              <div class="col-date">{{ new Date(producao.production_date).toLocaleDateString('pt-BR') }}</div>
              <div class="col-amount">{{ producao.milk_production }} L</div>
            </div>
          </div>
        </div>

        <!-- Vazio -->
        <div v-else-if="!loadingProduction" class="empty-production">
          <p>Nenhum registro de produção encontrado para este animal.</p>
        </div>
      </section>

      <!-- SEÇÃO 4.3 - HISTÓRICO DE PESO -->
      <section class="info-card weight-card">
        <div class="card-title">⚖️ Histórico de Pesagem</div>
        
        <!-- Resumo - Requisito 4.3 -->
        <div v-if="weightResumo" class="weight-resume">
          <div class="resume-item">
            <span class="resume-label">Última Pesagem</span>
            <span class="resume-value">{{ weightResumo.ultima_pesagem?.weight || '0' }} kg</span>
            <span class="resume-date" v-if="weightResumo.ultima_pesagem">
              {{ new Date(weightResumo.ultima_pesagem.weighing_date).toLocaleDateString('pt-BR') }}
            </span>
          </div>
          <div class="resume-item">
            <span class="resume-label">Peso Médio</span>
            <span class="resume-value">{{ (weightResumo.peso_medio).toFixed(1) }} kg</span>
          </div>
          <div class="resume-item">
            <span class="resume-label">Maior Peso</span>
            <span class="resume-value">{{ (weightResumo.peso_maximo).toFixed(1) }} kg</span>
          </div>
          <div class="resume-item">
            <span class="resume-label">Menor Peso</span>
            <span class="resume-value">{{ (weightResumo.peso_minimo).toFixed(1) }} kg</span>
          </div>
          <div class="resume-item">
            <span class="resume-label">Total de Pesagens</span>
            <span class="resume-value">{{ weightResumo.total_pesagens }}</span>
          </div>
          <div class="resume-item" v-if="weightResumo.ganho_peso_recente !== 0">
            <span class="resume-label">Ganho Recente</span>
            <span class="resume-value" :class="{ 'positive': weightResumo.ganho_peso_recente > 0, 'negative': weightResumo.ganho_peso_recente < 0 }">
              {{ (weightResumo.ganho_peso_recente > 0 ? '+' : '') }}{{ (weightResumo.ganho_peso_recente).toFixed(1) }} kg
            </span>
          </div>
        </div>

        <!-- Carregando -->
        <div v-if="loadingWeight" class="loading-mini">
          <div class="spinner-mini"></div>
          <p>Carregando histórico de peso...</p>
        </div>

        <!-- Histórico - Requisito 4.3 -->
        <div v-else-if="weightResumo && weightResumo.historico.length > 0" class="weight-history">
          <h4 style="margin-top: 20px; margin-bottom: 10px; color: #e6edf3;">Histórico Completo</h4>
          <div class="history-table">
            <div class="table-header">
              <div class="col-date">Data</div>
              <div class="col-amount">Peso (kg)</div>
            </div>
            <div v-for="pesagem in weightResumo.historico" :key="pesagem.id" class="table-row">
              <div class="col-date">{{ new Date(pesagem.weighing_date).toLocaleDateString('pt-BR') }}</div>
              <div class="col-amount">{{ pesagem.weight }} kg</div>
            </div>
          </div>
        </div>

        <!-- Vazio -->
        <div v-else-if="!loadingWeight" class="empty-production">
          <p>Nenhum registro de pesagem encontrado para este animal.</p>
        </div>

        <!-- Gráfico de Evolução - Requisito 4.2 -->
        <WeightEvolutionChart 
          v-if="weightResumo && weightResumo.historico.length > 1" 
          :data="weightResumo.historico"
          title="📊 Evolução de Peso"
        />
      </section>

      <!-- SEÇÃO 6.2 - HISTÓRICO DE VACINAÇÃO (REQUISITO 6.2) -->
      <VaccinationHistory :animal-id="parseInt(route.params.id)" />

      <!-- SEÇÃO 7 - BIOMETRIA E SENSORES (REQUISITO 7) -->
      <section class="info-card biometric-section">
        <div class="card-title">📡 Sensores / Biometria (IoT Colares)</div>
        <BiometricCard :animal-id="parseInt(route.params.id)" />
      </section>

      <!-- SEÇÃO 7.2 - GRÁFICOS DE ANÁLISE (REQUISITO 7.2) -->
      <section class="info-card charts-section">
        <div class="card-title">📊 Análise de Saúde (Gráficos Históricos)</div>
        <BiometricCharts :animal-id="parseInt(route.params.id)" :days="7" />
      </section>

      <section class="info-card side-card">
        <div class="card-title">Ações</div>
        <div class="action-buttons">
          <button class="btn-edit" @click="goToEdit">✏️ Editar Animal</button>
          <button class="btn-delete" @click="deleteAnimalFromDetail">🗑️ Deletar Animal</button>
        </div>
        <div class="manejo-info" style="margin-top: 15px;">
          <p>Monitoramento de saúde e produção.</p>
          <button v-if="animal.status !== 'doente'" class="btn-warning" @click="quickReportSick" style="margin-bottom: 10px;">⚠️ Reportar Doente</button>
          <button v-else class="btn-success" @click="quickMarkHealthy">✓ Marcar como Saudável</button>
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
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import WeightEvolutionChart from '@/components/WeightEvolutionChart.vue';
import StatusBadge from '@/components/StatusBadge.vue';
import VaccinationHistory from '@/components/VaccinationHistory.vue';
import BiometricCard from '@/components/BiometricCard.vue';
import BiometricCharts from '@/components/BiometricCharts.vue';

const route = useRoute();
const router = useRouter();
const animal = ref(null);
const loading = ref(true);
const loadingProduction = ref(true);
const loadingWeight = ref(true);
const productionResumo = ref(null);
const weightResumo = ref(null);

const fetchAnimalDetails = async () => {
  const id = route.params.id;
  console.log("Buscando animal com ID:", id);
  try {
    const response = await api.getAnimalById(parseInt(id));
    console.log("Resposta recebida:", response.data);
    animal.value = response.data;
    
    // Buscar produção de leite após carregar animal
    await fetchProductionHistory(id);
    
    // Buscar histórico de peso após carregar animal
    await fetchWeightHistory(id);
  } catch (error) {
    console.error("Erro ao buscar detalhes do animal:", error);
  } finally {
    loading.value = false;
  }
};

const fetchProductionHistory = async (animalId) => {
  loadingProduction.value = true;
  try {
    console.log("Buscando histórico de produção para animal ID:", animalId);
    const response = await api.getMilkProductionByAnimal(animalId);
    console.log("Histórico de produção:", response.data);
    productionResumo.value = response.data.resumo;
    productionResumo.value.historico = response.data.historico;
  } catch (error) {
    console.error("Erro ao buscar histórico de produção:", error);
    productionResumo.value = null;
  } finally {
    loadingProduction.value = false;
  }
};

const fetchWeightHistory = async (animalId) => {
  loadingWeight.value = true;
  try {
    console.log("Buscando histórico de peso para animal ID:", animalId);
    const response = await api.getWeightHistoryByAnimal(animalId);
    console.log("Histórico de peso:", response.data);
    weightResumo.value = response.data.resumo;
    weightResumo.value.historico = response.data.historico;
  } catch (error) {
    console.error("Erro ao buscar histórico de peso:", error);
    weightResumo.value = null;
  } finally {
    loadingWeight.value = false;
  }
};

const goToEdit = () => {
  router.push({ name: 'animal-edit', params: { id: animal.value.id } });
};

const quickReportSick = async () => {
  const confirm = window.confirm("Reportar este animal como DOENTE?");
  if (!confirm) return;
  
  try {
    const updatedAnimal = { ...animal.value, status: 'doente' };
    await api.updateAnimal(animal.value.id, updatedAnimal);
    animal.value.status = 'doente';
    alert("✓ Animal marcado como DOENTE. Atenção será necessária!");
  } catch (error) {
    console.error("Erro ao reportar animal doente:", error);
    alert("Erro ao atualizar status do animal.");
  }
};

const quickMarkHealthy = async () => {
  const confirm = window.confirm("Marcar este animal como ATIVO (Saudável)?");
  if (!confirm) return;
  
  try {
    const updatedAnimal = { ...animal.value, status: 'ativo' };
    await api.updateAnimal(animal.value.id, updatedAnimal);
    animal.value.status = 'ativo';
    alert("✓ Animal marcado como ATIVO.");
  } catch (error) {
    console.error("Erro ao marcar animal como saudável:", error);
    alert("Erro ao atualizar status do animal.");
  }
};

const deleteAnimalFromDetail = async () => {
  const confirm = window.confirm("Tem certeza que deseja deletar este animal? Esta ação não pode ser desfeita.");
  if (!confirm) return;

  loading.value = true;
  try {
    console.log("Deletando animal com ID:", animal.value.id);
    await api.deleteAnimal(animal.value.id);
    console.log("Animal deletado com sucesso");
    
    alert("Animal deletado com sucesso!");
    router.push({ name: 'animal-list' });
  } catch (error) {
    console.error("Erro ao deletar animal:", error);
    
    let errorMessage = "Erro ao deletar animal";
    if (error.response?.data) {
      if (typeof error.response.data === 'object') {
        const errors = Object.entries(error.response.data)
          .map(([field, msgs]) => {
            const msgArray = Array.isArray(msgs) ? msgs : [msgs];
            return `${field}: ${msgArray.join(', ')}`;
          })
          .join('\n');
        errorMessage = errors || error.response.data.detail || errorMessage;
      } else if (error.response.data.detail) {
        errorMessage = error.response.data.detail;
      }
    }
    
    alert(errorMessage);
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

.action-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.btn-edit,
.btn-delete {
  flex: 1;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid;
  font-weight: bold;
  transition: 0.2s;
  font-size: 0.9rem;
}

.btn-edit {
  background: transparent;
  border-color: #3fb950;
  color: #3fb950;
}

.btn-edit:hover {
  background: rgba(63, 185, 80, 0.1);
}

.btn-delete {
  background: transparent;
  border-color: #f85149;
  color: #f85149;
}

.btn-delete:hover {
  background: rgba(248, 81, 73, 0.1);
}

.btn-warning {
  width: 100%;
  padding: 12px;
  background: rgba(210, 153, 34, 0.1);
  border: 1px solid #d29922;
  color: #d29922;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  font-size: 0.9rem;
  animation: pulse 2s infinite;
}

.btn-warning:hover {
  background: rgba(210, 153, 34, 0.2);
  box-shadow: 0 0 10px rgba(210, 153, 34, 0.3);
}

.btn-success {
  width: 100%;
  padding: 12px;
  background: rgba(63, 185, 80, 0.1);
  border: 1px solid #3fb950;
  color: #3fb950;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  font-size: 0.9rem;
}

.btn-success:hover {
  background: rgba(63, 185, 80, 0.2);
  box-shadow: 0 0 10px rgba(63, 185, 80, 0.3);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
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

/* Estilos para Seção de Produção */
.production-card {
  background: #161b22;
  border: 1px solid #30363d;
}

.production-resume {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin: 20px 0;
  padding: 20px;
  background: rgba(63, 185, 80, 0.08);
  border-radius: 8px;
  border: 1px solid rgba(63, 185, 80, 0.3);
}

.resume-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 15px;
  background: #0d1117;
  border-radius: 6px;
  border: 1px solid #30363d;
}

.resume-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #8b949e;
  font-weight: bold;
  letter-spacing: 0.5px;
}

.resume-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #3fb950;
}

.resume-date {
  font-size: 0.8rem;
  color: #8b949e;
}

.production-history {
  margin-top: 20px;
}

.history-table {
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 8px;
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  background: #161b22;
  border-bottom: 2px solid #30363d;
  padding: 12px;
  font-weight: bold;
  color: #3fb950;
  text-transform: uppercase;
  font-size: 0.8rem;
}

.table-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  padding: 12px;
  border-bottom: 1px solid #30363d;
  align-items: center;
  color: #e6edf3;
}

.table-row:hover {
  background: rgba(63, 185, 80, 0.05);
}

.table-row:last-child {
  border-bottom: none;
}

.col-date {
  font-size: 0.9rem;
  color: #8b949e;
}

.col-amount {
  font-size: 0.95rem;
  font-weight: bold;
  color: #3fb950;
  text-align: right;
  padding-right: 10px;
}

.empty-production {
  padding: 30px;
  text-align: center;
  color: #8b949e;
  background: #0d1117;
  border-radius: 8px;
  border: 1px dashed #30363d;
  margin-top: 20px;
}

.loading-mini {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 20px;
  color: #8b949e;
}

.spinner-mini {
  width: 20px;
  height: 20px;
  border: 2px solid #30363d;
  border-top-color: #3fb950;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

/* Estilos para Seção de Peso */
.weight-card {
  background: #161b22;
  border: 1px solid #30363d;
}

.weight-resume {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin: 20px 0;
  padding: 20px;
  background: rgba(88, 166, 255, 0.08);
  border-radius: 8px;
  border: 1px solid rgba(88, 166, 255, 0.3);
}

.weight-history {
  margin-top: 20px;
}

.resume-value.positive {
  color: #3fb950;
}

.resume-value.negative {
  color: #f85149;
}

@media (max-width: 768px) {
  .production-resume {
    grid-template-columns: 1fr 1fr;
  }

  .table-header,
  .table-row {
    grid-template-columns: 1fr 1fr;
  }

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