<template>
  <div class="map-wrapper">
    <header class="page-header">
      <div class="header-info">
        <h1>Mapa de Ocupação</h1>
        <p>Distribuição do rebanho por quadrantes (pastos)</p>
      </div>
    </header>

    <section class="simulation-header">
      <div>
        <h2>Modo de Simulação</h2>
        <p>Ative a simulação para testar realocações sem alterar o banco de dados.</p>
      </div>
      <div class="sim-actions">
        <button class="sim-toggle" @click="toggleSimulation()">
          {{ simulationMode ? 'Desativar Simulação' : 'Ativar Simulação' }}
        </button>
        <button v-if="simulationMode && hasChanges" class="sim-save" @click="saveSimulation()">Salvar Simulação</button>
        <button v-if="simulationMode && hasChanges" class="sim-reset" @click="resetSimulation()">Resetar</button>
      </div>
    </section>

    <div v-if="loading" class="loading-state">Carregando mapa...</div>

    <div v-else class="map-grid">
      <div v-for="q in quadrants" :key="q.id" class="quadrant-card">
        <div class="card-glow"></div>
        <header class="q-header">
          <span class="q-tag">ID #{{ q.id }}</span>
          <span class="q-area">{{ q.area }} ha</span>
        </header>

        <div class="q-body">
          <h3>{{ q.name || q.nome_quadrante }}</h3>
          <p class="description">{{ q.description || q.descricao }}</p>

          <div class="lotacao-info">
            <span class="value">{{ getMaxAnimals(q) }}</span>
            <span class="label">Capacidade Máxima</span>
          </div>

          <div class="occupancy">
            <strong>Ocupação atual</strong>
            <span>{{ totalAnimals(q) }} / {{ getMaxAnimals(q) }} animais</span>
          </div>

          <div class="status-pill" :class="occupancyState(q)">
            {{ stateLabel(q) }}
          </div>

          <div class="simulation-note" v-if="simulationMode">
            <p>Adições de simulação: <strong>{{ getSimulationCount(q) }}</strong></p>
            <div class="sim-controls">
              <button @click="changeSimulation(q, -1)" :disabled="getSimulationCount(q) <= 0">-</button>
              <button @click="changeSimulation(q, 1)">+</button>
            </div>
          </div>
        </div>

        <div class="q-footer">
          <div class="progress-container">
            <div
              class="progress-bar"
              :class="occupancyState(q)"
              :style="{ width: progressWidth(q) }"
            ></div>
          </div>
          <span class="sync-status">Sincronizado com DB</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/services/api';

const quadrants = ref([]);
const loading = ref(true);
const simulationMode = ref(false);
const simulatedAnimals = ref({});
const animalCounts = ref({});

const normalizeQuadrantId = quadrant => {
  if (quadrant === null || quadrant === undefined) return null;
  return typeof quadrant === 'object' ? quadrant.id : quadrant;
};

const loadMapData = async () => {
  loading.value = true;
  try {
    const [quadrantsResponse, animalsResponse] = await Promise.all([
      api.getQuadrants(),
      api.getAnimals(),
    ]);

    quadrants.value = quadrantsResponse.data.results || quadrantsResponse.data;

    const animals = animalsResponse.data.results || animalsResponse.data;
    animalCounts.value = animals.reduce((counts, animal) => {
      const quadrantId = normalizeQuadrantId(animal.quadrant);
      if (!quadrantId) return counts;
      counts[quadrantId] = (counts[quadrantId] || 0) + 1;
      return counts;
    }, {});
  } catch (error) {
    console.error('Erro ao carregar quadrantes ou animais:', error);
  } finally {
    loading.value = false;
  }
};

const toggleSimulation = () => {
  simulationMode.value = !simulationMode.value;
  if (!simulationMode.value) {
    simulatedAnimals.value = {};
  }
};

const getMaxAnimals = quadrant => quadrant.max_animals || quadrant.qtd_max_animal || 0;
const getActualCount = quadrant => animalCounts.value[quadrant.id] || 0;
const getSimulationCount = quadrant => simulatedAnimals.value[quadrant.id] || 0;
const totalAnimals = quadrant => getActualCount(quadrant) + getSimulationCount(quadrant);

const progressWidth = quadrant => {
  const max = getMaxAnimals(quadrant) || 1;
  const ratio = totalAnimals(quadrant) / max;
  return `${Math.min(100, Math.round(ratio * 100))}%`;
};

const occupancyState = quadrant => {
  const max = getMaxAnimals(quadrant) || 1;
  const ratio = totalAnimals(quadrant) / max;
  if (ratio >= 1) return 'danger';
  if (ratio >= 0.75) return 'warning';
  return 'safe';
};

const stateLabel = quadrant => {
  const max = getMaxAnimals(quadrant) || 1;
  const ratio = totalAnimals(quadrant) / max;
  if (ratio >= 1) return 'Lotado';
  if (ratio >= 0.75) return 'Atenção';
  return 'Espaço disponível';
};

const changeSimulation = (quadrant, delta) => {
  if (!simulationMode.value) return;

  const id = quadrant.id;
  const current = simulatedAnimals.value[id] || 0;
  const next = Math.max(0, current + delta);
  simulatedAnimals.value = { ...simulatedAnimals.value, [id]: next };
};

const hasChanges = computed(() => Object.keys(simulatedAnimals.value).some(k => simulatedAnimals.value[k] > 0));

const saveSimulation = async () => {
  if (!hasChanges.value) {
    alert('Nenhuma alteração para salvar.');
    return;
  }

  const payload = {
    timestamp: new Date().toISOString(),
    changes: simulatedAnimals.value
  };

  try {
    // Tenta enviar para um endpoint de simulações (se existir)
    await api.post('simulations/', payload);
    alert('Simulação enviada ao servidor com sucesso.');
    // após salvar no servidor, limpa o buffer de simulação
    simulatedAnimals.value = {};
  } catch (err) {
    // fallback para armazenamento local
    try {
      localStorage.setItem('map_simulation', JSON.stringify(payload));
      alert('Servidor indisponível. Simulação salva localmente.');
      simulatedAnimals.value = {};
    } catch (storageErr) {
      console.error('Erro ao salvar simulação localmente:', storageErr);
      alert('Falha ao salvar a simulação. Veja o console para detalhes.');
    }
  }
};

const resetSimulation = () => {
  if (confirm('Deseja descartar as alterações da simulação?')) {
    simulatedAnimals.value = {};
  }
};

onMounted(() => {
  loadMapData();
});
</script>

<style scoped>
.map-wrapper {
  padding: 40px;
  background-color: #0d1117;
  min-height: 100vh;
  color: #e6edf3;
}

.page-header h1 {
  color: #3fb950;
  font-size: 2rem;
  margin-bottom: 5px;
}

.page-header p {
  color: #8b949e;
  margin-bottom: 30px;
}

.simulation-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 30px;
  padding: 24px;
  background: rgba(63, 185, 80, 0.08);
  border: 1px solid rgba(63, 185, 80, 0.2);
  border-radius: 16px;
}

.simulation-header h2 {
  margin: 0;
  font-size: 1.2rem;
  color: #c8ffb3;
}

.simulation-header p {
  margin: 6px 0 0;
  color: #94a3b8;
}

.sim-toggle {
  border: 1px solid #3fb950;
  background: transparent;
  color: #c8ffb3;
  padding: 12px 18px;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
}

.sim-toggle:hover {
  background: rgba(63, 185, 80, 0.18);
  transform: translateY(-1px);
}

.sim-actions { display: flex; gap: 12px; align-items: center; }
.sim-save, .sim-reset { border: 1px solid rgba(63,185,80,0.22); background: transparent; color: #c8ffb3; padding: 10px 14px; border-radius: 10px; cursor: pointer; }
.sim-save:hover { background: rgba(63,185,80,0.14); }
.sim-reset { border-color: rgba(255,255,255,0.08); color: #e6edf3; }
.sim-reset:hover { background: rgba(255,255,255,0.02); }

.loading-state {
  color: #8b949e;
  font-size: 1rem;
}

.map-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

.quadrant-card {
  background: #161b22;
  border: 1.5px solid #3fb950;
  border-radius: 16px;
  padding: 24px;
  position: relative;
  overflow: hidden;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.quadrant-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 22px rgba(63, 185, 80, 0.15);
}

.card-glow {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top left, rgba(63, 185, 80, 0.14), transparent 35%);
  pointer-events: none;
}

.q-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 18px;
  font-size: 0.8rem;
  color: #8b949e;
}

.q-tag {
  background: rgba(63, 185, 80, 0.1);
  color: #3fb950;
  padding: 4px 10px;
  border-radius: 999px;
}

.q-area {
  color: #94a3b8;
}

.q-body h3 {
  font-size: 1.45rem;
  margin-bottom: 10px;
  color: #f8fafc;
}

.description {
  color: #8b949e;
  font-size: 0.92rem;
  margin-bottom: 20px;
  min-height: 42px;
}

.lotacao-info {
  text-align: center;
  margin-bottom: 18px;
}

.lotacao-info .value {
  font-size: 2.1rem;
  font-weight: 700;
  color: #3fb950;
  display: block;
}

.lotacao-info .label {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #8b949e;
  letter-spacing: 1px;
}

.occupancy {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 12px;
  color: #c8d1dc;
}

.occupancy strong {
  font-size: 0.95rem;
}

.status-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 0.78rem;
  letter-spacing: 0.4px;
  text-transform: uppercase;
  font-weight: 700;
}

.status-pill.safe {
  background: rgba(63, 185, 80, 0.12);
  color: #7ef2a8;
}

.status-pill.warning {
  background: rgba(255, 159, 28, 0.14);
  color: #ffd28a;
}

.status-pill.danger {
  background: rgba(239, 68, 68, 0.14);
  color: #ffb3b3;
}

.simulation-note {
  margin-top: 18px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 14px;
}

.sim-controls {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.sim-controls button {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid rgba(63, 185, 80, 0.3);
  background: rgba(31, 41, 55, 0.96);
  color: #c8ffb3;
  cursor: pointer;
  transition: transform 0.2s ease, background 0.2s ease;
}

.sim-controls button:hover:not(:disabled) {
  transform: translateY(-1px);
  background: rgba(63, 185, 80, 0.12);
}

.sim-controls button:disabled {
  opacity: 0.42;
  cursor: not-allowed;
}

.q-footer {
  margin-top: 22px;
}

.progress-container {
  height: 8px;
  background: #20272f;
  border-radius: 999px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-bar {
  height: 100%;
  transition: width 0.35s ease;
}

.progress-bar.safe {
  background: #3fb950;
  box-shadow: 0 0 14px rgba(63, 185, 80, 0.35);
}

.progress-bar.warning {
  background: #ff9f1c;
  box-shadow: 0 0 14px rgba(255, 159, 28, 0.35);
}

.progress-bar.danger {
  background: #ef4444;
  box-shadow: 0 0 14px rgba(239, 68, 68, 0.45);
  animation: pulse-danger 2s ease-in-out infinite;
}

.sync-status {
  font-size: 0.7rem;
  color: #6b7280;
  font-family: monospace;
}

@keyframes pulse-danger {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
</style>
