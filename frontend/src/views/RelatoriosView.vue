<template>
  <div class="reports-wrapper">
    <header class="page-header">
      <div class="header-content">
        <h1>Relatórios de Gestão</h1>
        <p>Análise e evolução dos dados do rebanho</p>
      </div>
    </header>

    <div class="reports-container">
      <!-- TABS DE SELEÇÃO DE RELATÓRIO -->
      <section class="tabs-section">
        <div class="tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="{ 'active': activeTab === tab.id }"
            class="tab-button"
          >
            {{ tab.icon }} {{ tab.label }}
          </button>
        </div>
      </section>

      <!-- RELATÓRIO 1: EVOLUÇÃO DE PESO POR ANIMAL -->
      <section v-if="activeTab === 'weight_individual'" class="reports-section">
        <div class="glass-card report-card">
          <header class="card-header">
            <span class="icon">⚖️</span>
            <h2>Evolução de Peso - Animal Específico</h2>
          </header>

          <div class="filter-group">
            <label>Selecione o Animal:</label>
            <select v-model="selectedAnimalId" @change="loadAnimalWeightData" class="select-input">
              <option value="">-- Escolha um animal --</option>
              <option v-for="animal in animals" :key="animal.id" :value="animal.id">
                {{ animal.name }} ({{ animal.register_number }})
              </option>
            </select>
          </div>

          <div v-if="selectedAnimalId && !loadingWeight" class="report-content">
            <div v-if="selectedAnimalWeight" class="weight-stats">
              <div class="stat-box">
                <span class="stat-label">Peso Atual</span>
                <span class="stat-value">{{ selectedAnimalWeight.ultima_pesagem?.weight }} kg</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">Peso Médio</span>
                <span class="stat-value">{{ (selectedAnimalWeight.peso_medio).toFixed(1) }} kg</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">Maior Peso</span>
                <span class="stat-value">{{ (selectedAnimalWeight.peso_maximo).toFixed(1) }} kg</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">Menor Peso</span>
                <span class="stat-value">{{ (selectedAnimalWeight.peso_minimo).toFixed(1) }} kg</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">Total de Pesagens</span>
                <span class="stat-value">{{ selectedAnimalWeight.total_pesagens }}</span>
              </div>
              <div class="stat-box" v-if="selectedAnimalWeight.ganho_peso_recente !== 0">
                <span class="stat-label">Ganho Recente</span>
                <span class="stat-value" :class="{ 'positive': selectedAnimalWeight.ganho_peso_recente > 0, 'negative': selectedAnimalWeight.ganho_peso_recente < 0 }">
                  {{ (selectedAnimalWeight.ganho_peso_recente > 0 ? '+' : '') }}{{ (selectedAnimalWeight.ganho_peso_recente).toFixed(1) }} kg
                </span>
              </div>
            </div>

            <WeightEvolutionChart 
              v-if="selectedAnimalWeight && selectedAnimalWeight.historico.length > 1"
              :data="selectedAnimalWeight.historico"
              title="Curva de Crescimento"
            />
          </div>

          <div v-else-if="loadingWeight" class="loading-state">
            <div class="spinner-mini"></div>
            <p>Carregando dados de peso...</p>
          </div>

          <div v-else class="empty-state">
            <p>Selecione um animal para visualizar os dados</p>
          </div>
        </div>
      </section>

      <!-- RELATÓRIO 2: EVOLUÇÃO DE PESO - REBANHO INTEIRO -->
      <section v-if="activeTab === 'weight_herd'" class="reports-section">
        <div class="glass-card report-card">
          <header class="card-header">
            <span class="icon">📊</span>
            <h2>Evolução de Peso - Rebanho Completo</h2>
          </header>

          <div v-if="!loadingHerdData" class="report-content">
            <div class="herd-stats">
              <div class="stat-box">
                <span class="stat-label">Total de Animais</span>
                <span class="stat-value">{{ animals.length }}</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">Animais com Pesagem</span>
                <span class="stat-value">{{ animalsWithWeight.length }}</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">Peso Médio do Rebanho</span>
                <span class="stat-value">{{ herdAverageWeight }} kg</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">Maior Peso Registrado</span>
                <span class="stat-value">{{ herdMaxWeight }} kg</span>
              </div>
              <div class="stat-box">
                <span class="stat-label">Menor Peso Registrado</span>
                <span class="stat-value">{{ herdMinWeight }} kg</span>
              </div>
            </div>

            <div class="animals-list">
              <h3>Animais Rastreados</h3>
              <div class="table">
                <div class="table-header">
                  <div class="col-name">Animal</div>
                  <div class="col-weight">Peso Atual</div>
                  <div class="col-avg">Peso Médio</div>
                  <div class="col-gain">Ganho Recente</div>
                </div>
                <div v-for="animal in animalsWithWeight" :key="animal.id" class="table-row">
                  <div class="col-name">{{ animal.name }} ({{ animal.register_number }})</div>
                  <div class="col-weight">{{ animal.lastWeight }} kg</div>
                  <div class="col-avg">{{ animal.avgWeight }} kg</div>
                  <div class="col-gain" :class="{ 'positive': animal.gainWeight > 0, 'negative': animal.gainWeight < 0 }">
                    {{ (animal.gainWeight > 0 ? '+' : '') }}{{ animal.gainWeight }} kg
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="loading-state">
            <div class="spinner-mini"></div>
            <p>Carregando dados do rebanho...</p>
          </div>
        </div>
      </section>

      <!-- RELATÓRIO 3: GANHO DE PESO -->
      <section v-if="activeTab === 'weight_gain'" class="reports-section">
        <div class="glass-card report-card">
          <header class="card-header">
            <span class="icon">📈</span>
            <h2>Análise de Ganho de Peso</h2>
          </header>

          <div v-if="!loadingHerdData" class="report-content">
            <div class="gain-stats">
              <div class="stat-box highlight">
                <span class="stat-label">Ganho Médio do Rebanho</span>
                <span class="stat-value">{{ averageGain }} kg</span>
              </div>
              <div class="stat-box highlight">
                <span class="stat-label">Animal com Maior Ganho</span>
                <span class="stat-value">{{ topGainer?.name }} ({{ topGainer?.gainWeight }} kg)</span>
              </div>
              <div class="stat-box highlight">
                <span class="stat-label">Animal com Menor Ganho</span>
                <span class="stat-value">{{ lowestGainer?.name }} ({{ lowestGainer?.gainWeight }} kg)</span>
              </div>
            </div>

            <div class="gains-list">
              <h3>Ranking de Ganho de Peso</h3>
              <div class="ranking-table">
                <div class="ranking-header">
                  <div class="rank-col">Posição</div>
                  <div class="name-col">Animal</div>
                  <div class="gain-col">Ganho (kg)</div>
                  <div class="status-col">Status</div>
                </div>
                <div v-for="(animal, index) in gainRanking" :key="animal.id" class="ranking-row">
                  <div class="rank-col">{{ index + 1 }}º</div>
                  <div class="name-col">{{ animal.name }}</div>
                  <div class="gain-col" :class="{ 'positive': animal.gainWeight > 0, 'negative': animal.gainWeight < 0 }">
                    {{ (animal.gainWeight > 0 ? '+' : '') }}{{ animal.gainWeight }} kg
                  </div>
                  <div class="status-col" :class="{ 'excellent': animal.gainWeight > 2, 'good': animal.gainWeight > 0, 'poor': animal.gainWeight <= 0 }">
                    {{ animal.gainWeight > 2 ? '✓ Excelente' : animal.gainWeight > 0 ? '→ Bom' : '✗ Crítico' }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="loading-state">
            <div class="spinner-mini"></div>
            <p>Carregando dados de ganho de peso...</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';
import WeightEvolutionChart from '@/components/WeightEvolutionChart.vue';

const activeTab = ref('weight_individual');
const animals = ref([]);
const selectedAnimalId = ref('');
const selectedAnimalWeight = ref(null);
const loadingWeight = ref(false);
const loadingHerdData = ref(true);

const tabs = [
  { id: 'weight_individual', label: 'Por Animal', icon: '🐄' },
  { id: 'weight_herd', label: 'Rebanho Inteiro', icon: '📊' },
  { id: 'weight_gain', label: 'Ganho de Peso', icon: '📈' }
];

const animalsWithWeight = computed(() => {
  return animals.value.map(animal => ({
    ...animal,
    lastWeight: animal.weightData?.ultima_pesagem?.weight || 'N/A',
    avgWeight: animal.weightData?.peso_medio?.toFixed(1) || 'N/A',
    gainWeight: animal.weightData?.ganho_peso_recente?.toFixed(1) || 0
  })).filter(a => a.weightData);
});

const herdAverageWeight = computed(() => {
  if (animalsWithWeight.value.length === 0) return 0;
  const sum = animalsWithWeight.value.reduce((acc, a) => acc + (parseFloat(a.avgWeight) || 0), 0);
  return (sum / animalsWithWeight.value.length).toFixed(1);
});

const herdMaxWeight = computed(() => {
  if (animalsWithWeight.value.length === 0) return 0;
  return Math.max(...animalsWithWeight.value.map(a => parseFloat(a.lastWeight) || 0)).toFixed(1);
});

const herdMinWeight = computed(() => {
  if (animalsWithWeight.value.length === 0) return 0;
  const weights = animalsWithWeight.value.map(a => parseFloat(a.lastWeight) || 0).filter(w => w > 0);
  return (weights.length > 0 ? Math.min(...weights) : 0).toFixed(1);
});

const gainRanking = computed(() => {
  return animalsWithWeight.value
    .sort((a, b) => parseFloat(b.gainWeight) - parseFloat(a.gainWeight));
});

const topGainer = computed(() => {
  return gainRanking.value[0] || null;
});

const lowestGainer = computed(() => {
  return gainRanking.value[gainRanking.value.length - 1] || null;
});

const averageGain = computed(() => {
  if (animalsWithWeight.value.length === 0) return 0;
  const sum = animalsWithWeight.value.reduce((acc, a) => acc + parseFloat(a.gainWeight), 0);
  return (sum / animalsWithWeight.value.length).toFixed(2);
});

const fetchAllAnimals = async () => {
  try {
    const response = await api.getAnimals();
    animals.value = response.data.map(animal => ({ ...animal, weightData: null }));
    await loadHerdWeightData();
  } catch (error) {
    console.error('Erro ao buscar animais:', error);
  } finally {
    loadingHerdData.value = false;
  }
};

const loadHerdWeightData = async () => {
  for (let animal of animals.value) {
    try {
      const response = await api.getWeightHistoryByAnimal(animal.id);
      animal.weightData = response.data.resumo;
    } catch (error) {
      console.error(`Erro ao buscar peso do animal ${animal.id}:`, error);
    }
  }
};

const loadAnimalWeightData = async () => {
  if (!selectedAnimalId.value) return;
  
  loadingWeight.value = true;
  try {
    const response = await api.getWeightHistoryByAnimal(selectedAnimalId.value);
    selectedAnimalWeight.value = response.data.resumo;
    selectedAnimalWeight.value.historico = response.data.historico;
  } catch (error) {
    console.error('Erro ao buscar dados de peso:', error);
    selectedAnimalWeight.value = null;
  } finally {
    loadingWeight.value = false;
  }
};

onMounted(() => {
  fetchAllAnimals();
});
</script>

<style scoped>
.reports-wrapper {
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

.reports-container {
  max-width: 1400px;
  margin: 0 auto;
}

.tabs-section {
  margin-bottom: 30px;
}

.tabs {
  display: flex;
  gap: 15px;
  border-bottom: 1px solid #30363d;
  overflow-x: auto;
}

.tab-button {
  padding: 12px 20px;
  background: transparent;
  border: none;
  color: #8b949e;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  white-space: nowrap;
}

.tab-button:hover {
  color: #e6edf3;
}

.tab-button.active {
  color: #3fb950;
  border-bottom-color: #3fb950;
}

.reports-section {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.glass-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 30px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #30363d;
}

.card-header .icon {
  font-size: 1.5rem;
}

.card-header h2 {
  margin: 0;
  font-size: 1.3rem;
  color: #e6edf3;
}

.filter-group {
  margin-bottom: 30px;
}

.filter-group label {
  display: block;
  color: #8b949e;
  font-size: 0.9rem;
  margin-bottom: 10px;
  font-weight: 600;
  text-transform: uppercase;
}

.select-input {
  width: 100%;
  max-width: 400px;
  padding: 10px 12px;
  background-color: #0d1117;
  border: 1px solid #30363d;
  border-radius: 6px;
  color: #e6edf3;
  font-size: 0.95rem;
  cursor: pointer;
}

.select-input:focus {
  outline: none;
  border-color: #3fb950;
}

.report-content {
  margin-top: 20px;
}

.weight-stats,
.herd-stats,
.gain-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-box {
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-box.highlight {
  border-color: #3fb950;
  background: rgba(63, 185, 80, 0.05);
}

.stat-label {
  font-size: 0.8rem;
  color: #8b949e;
  text-transform: uppercase;
  font-weight: 600;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #3fb950;
}

.stat-value.positive {
  color: #3fb950;
}

.stat-value.negative {
  color: #f85149;
}

.animals-list,
.gains-list {
  margin-top: 30px;
}

.animals-list h3,
.gains-list h3 {
  margin-top: 0;
  color: #e6edf3;
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.table,
.ranking-table {
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 8px;
  overflow: hidden;
}

.table-header,
.ranking-header {
  display: grid;
  gap: 0;
  background: #161b22;
  border-bottom: 2px solid #30363d;
  padding: 12px;
  font-weight: bold;
  color: #3fb950;
  text-transform: uppercase;
  font-size: 0.8rem;
}

.table-header {
  grid-template-columns: 2fr 1fr 1fr 1fr;
}

.ranking-header {
  grid-template-columns: 0.5fr 2fr 1fr 1fr;
}

.table-row,
.ranking-row {
  display: grid;
  gap: 0;
  padding: 12px;
  border-bottom: 1px solid #30363d;
  align-items: center;
  color: #e6edf3;
}

.table-row:hover,
.ranking-row:hover {
  background: rgba(63, 185, 80, 0.05);
}

.table-row:last-child,
.ranking-row:last-child {
  border-bottom: none;
}

.table-row {
  grid-template-columns: 2fr 1fr 1fr 1fr;
}

.ranking-row {
  grid-template-columns: 0.5fr 2fr 1fr 1fr;
}

.col-name,
.name-col {
  font-weight: 500;
}

.col-weight,
.col-avg,
.col-gain,
.rank-col,
.gain-col,
.status-col {
  text-align: right;
}

.col-gain.positive,
.gain-col.positive {
  color: #3fb950;
  font-weight: bold;
}

.col-gain.negative,
.gain-col.negative {
  color: #f85149;
  font-weight: bold;
}

.status-col.excellent {
  color: #3fb950;
  font-weight: bold;
}

.status-col.good {
  color: #58a6ff;
  font-weight: bold;
}

.status-col.poor {
  color: #f85149;
  font-weight: bold;
}

.empty-state,
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 15px;
  color: #8b949e;
}

.spinner-mini {
  width: 30px;
  height: 30px;
  border: 3px solid #30363d;
  border-top-color: #3fb950;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .reports-wrapper {
    padding: 20px;
  }

  .weight-stats,
  .herd-stats,
  .gain-stats {
    grid-template-columns: 1fr;
  }

  .table-header,
  .ranking-header {
    grid-template-columns: 1fr;
    gap: 0;
    padding: 8px;
  }

  .table-row,
  .ranking-row {
    grid-template-columns: 1fr;
    padding: 8px;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .tabs {
    flex-wrap: wrap;
  }
}
</style>
