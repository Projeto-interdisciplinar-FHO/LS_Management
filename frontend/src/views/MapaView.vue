<template>
  <div class="map-wrapper">
    <header class="page-header">
      <div class="header-info">
        <h1>Mapa de Ocupação</h1>
        <p>Distribuição do rebanho por quadrantes (pastos)</p>
      </div>
    </header>

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
          
          <div class="lotação-info">
            <span class="value">{{ q.max_animals || q.qtd_max_animal }}</span>
            <span class="label">Capacidade Máxima</span>
          </div>
        </div>

        <div class="q-footer">
          <div class="progress-container">
            <div class="progress-bar" style="width: 65%"></div>
          </div>
          <span class="sync-status">Sincronizado com DB</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const quadrants = ref([]);
const loading = ref(true);

const loadMapData = async () => {
  try {
    const response = await api.getQuadrants();
    // O Django pode retornar os dados direto ou dentro de .results
    quadrants.value = response.data.results || response.data;
  } catch (error) {
    console.error("Erro ao carregar quadrantes:", error);
  } finally {
    loading.value = false;
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

.page-header h1 { color: #3fb950; font-size: 2rem; margin-bottom: 5px; }
.page-header p { color: #8b949e; margin-bottom: 40px; }

.map-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

.quadrant-card {
  background: #161b22;
  border: 1.5px solid #3fb950; /* Bordas verdes conforme solicitado */
  border-radius: 12px;
  padding: 24px;
  position: relative;
  overflow: hidden;
  transition: 0.3s;
}

.quadrant-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 20px rgba(63, 185, 80, 0.15);
}

.q-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  font-size: 0.8rem;
  color: #8b949e;
}

.q-tag { background: rgba(63, 185, 80, 0.1); color: #3fb950; padding: 2px 8px; border-radius: 4px; }

.q-body h3 { font-size: 1.4rem; margin-bottom: 8px; color: #f0f6fc; }
.description { color: #8b949e; font-size: 0.9rem; margin-bottom: 20px; min-height: 40px; }

.lotação-info { text-align: center; margin-bottom: 20px; }
.lotação-info .value { font-size: 2.2rem; font-weight: bold; color: #3fb950; display: block; }
.lotação-info .label { font-size: 0.75rem; text-transform: uppercase; color: #8b949e; letter-spacing: 1px; }

.progress-container { height: 6px; background: #30363d; border-radius: 3px; overflow: hidden; margin-bottom: 8px; }
.progress-bar { height: 100%; background: #3fb950; box-shadow: 0 0 10px #3fb950; }
.sync-status { font-size: 0.65rem; color: #484f58; font-family: monospace; }
</style>