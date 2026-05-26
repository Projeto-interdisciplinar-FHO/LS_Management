<template>
  <div class="animals-consultation-container">
    <div class="header">
      <h1>🔍 Consultar Animais</h1>
      <p class="subtitle">Busque e visualize detalhes dos animais</p>
    </div>

    <!-- Filtros -->
    <div class="filters-section">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Buscar por nome, ID ou número de registro..."
          class="search-input"
        >
      </div>

      <div class="filters-grid">
        <div class="filter-group">
          <label>Status</label>
          <select v-model="filterStatus" class="filter-select">
            <option value="">Todos os Status</option>
            <option value="ativo">Ativo</option>
            <option value="doente">Doente</option>
            <option value="vendido">Vendido</option>
            <option value="obito">Óbito</option>
            <option value="inativo">Inativo</option>
          </select>
        </div>

        <div class="filter-group">
          <label>Quadrante</label>
          <select v-model="filterQuadrant" class="filter-select">
            <option value="">Todos os Quadrantes</option>
            <option v-for="quad in quadrants" :key="quad.id" :value="quad.id">
              {{ quad.name }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label>Espécie</label>
          <select v-model="filterSpecie" class="filter-select">
            <option value="">Todas as Espécies</option>
            <option v-for="sp in species" :key="sp.id" :value="sp.id">
              {{ sp.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Lista de Animais -->
    <div class="animals-list-container">
      <div v-if="filteredAnimals.length > 0" class="animals-list">
        <div 
          v-for="animal in filteredAnimals" 
          :key="animal.id"
          @click="selectAnimal(animal)"
          class="animal-card"
          :class="{ 'selected': selectedAnimalId === animal.id }"
        >
          <div class="card-header">
            <h3>{{ animal.name }}</h3>
            <span :class="['status-badge', `status-${animal.status}`]">
              {{ animal.status }}
            </span>
          </div>
          
          <div class="card-info">
            <div class="info-item">
              <span class="label">ID:</span>
              <span class="value">#{{ animal.register_number }}</span>
            </div>
            <div class="info-item">
              <span class="label">Peso:</span>
              <span class="value">{{ animal.weight }}kg</span>
            </div>
            <div class="info-item">
              <span class="label">Quadrante:</span>
              <span class="value">{{ animal.quadrant_name }}</span>
            </div>
            <div class="info-item">
              <span class="label">Espécie:</span>
              <span class="value">{{ animal.specie_name }}</span>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="empty-state">
        <p>Nenhum animal encontrado com os critérios de busca</p>
      </div>
    </div>

    <!-- Painel de Detalhes -->
    <div v-if="selectedAnimal" class="details-panel">
      <button @click="selectedAnimalId = null" class="close-btn">✕</button>
      
      <div class="details-header">
        <h2>{{ selectedAnimal.name }}</h2>
        <span :class="['status-badge', `status-${selectedAnimal.status}`]">
          {{ selectedAnimal.status }}
        </span>
      </div>

      <div class="details-grid">
        <!-- Informações Básicas -->
        <div class="details-section">
          <h3>📋 Informações Básicas</h3>
          <div class="info-row">
            <span class="label">Número de Registro:</span>
            <span class="value">#{{ selectedAnimal.register_number }}</span>
          </div>
          <div class="info-row">
            <span class="label">Sexo:</span>
            <span class="value">{{ selectedAnimal.sex === 'M' ? 'Macho' : 'Fêmea' }}</span>
          </div>
          <div class="info-row">
            <span class="label">Data de Nascimento:</span>
            <span class="value">{{ formatDate(selectedAnimal.birth_date) }}</span>
          </div>
          <div class="info-row">
            <span class="label">Espécie:</span>
            <span class="value">{{ selectedAnimal.specie_name }}</span>
          </div>
          <div class="info-row">
            <span class="label">Raça:</span>
            <span class="value">{{ selectedAnimal.breed_name || 'Não informado' }}</span>
          </div>
          <div class="info-row">
            <span class="label">Quadrante:</span>
            <span class="value">{{ selectedAnimal.quadrant_name }}</span>
          </div>
          <div class="info-row">
            <span class="label">Propósito:</span>
            <span class="value">{{ selectedAnimal.purpose_name }}</span>
          </div>
        </div>

        <!-- Informações de Saúde -->
        <div class="details-section">
          <h3>🏥 Saúde</h3>
          <div class="info-row">
            <span class="label">Peso Atual:</span>
            <span class="value">{{ selectedAnimal.weight }}kg</span>
          </div>
          <div class="info-row">
            <span class="label">Última Pesagem:</span>
            <span class="value">{{ selectedAnimal.last_weighing_date ? formatDate(selectedAnimal.last_weighing_date) : 'Sem registros' }}</span>
          </div>
          <div class="info-row">
            <span class="label">Próxima Vacinação:</span>
            <span class="value">{{ selectedAnimal.next_vaccination_date ? formatDate(selectedAnimal.next_vaccination_date) : 'Sem agendamento' }}</span>
          </div>
          <div class="info-row">
            <span class="label">Última Vacinação:</span>
            <span class="value">{{ selectedAnimal.last_vaccination_date ? formatDate(selectedAnimal.last_vaccination_date) : 'Sem registros' }}</span>
          </div>
        </div>

        <!-- Produção -->
        <div class="details-section">
          <h3>📊 Produção</h3>
          <div class="info-row">
            <span class="label">Última Produção de Leite:</span>
            <span class="value">{{ selectedAnimal.last_milk_production ? `${selectedAnimal.last_milk_production}L` : 'Sem registros' }}</span>
          </div>
          <div class="info-row">
            <span class="label">Data da Produção:</span>
            <span class="value">{{ selectedAnimal.last_milk_date ? formatDate(selectedAnimal.last_milk_date) : 'Sem registros' }}</span>
          </div>
        </div>
      </div>

      <!-- Ações Rápidas -->
      <div class="quick-actions">
        <button @click="goToAnimalProfile" class="action-btn profile-btn">
          👁️ Ver Perfil Completo
        </button>
        <button @click="goToWeightHistory" class="action-btn weight-btn">
          ⚖️ Histórico de Pesos
        </button>
        <button @click="goToVaccinationHistory" class="action-btn vaccine-btn">
          💉 Histórico de Vacinações
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const router = useRouter();

// Dados
const animals = ref([]);
const quadrants = ref([]);
const species = ref([]);

// Filtros
const searchQuery = ref('');
const filterStatus = ref('');
const filterQuadrant = ref('');
const filterSpecie = ref('');
const selectedAnimalId = ref(null);

// Computed
const filteredAnimals = computed(() => {
  return animals.value.filter(animal => {
    const matchSearch = !searchQuery.value || 
      animal.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      animal.register_number.toString().includes(searchQuery.value) ||
      animal.id.toString().includes(searchQuery.value);
    
    const matchStatus = !filterStatus.value || animal.status === filterStatus.value;
    const matchQuadrant = !filterQuadrant.value || animal.quadrant_id.toString() === filterQuadrant.value.toString();
    const matchSpecie = !filterSpecie.value || animal.specie_id.toString() === filterSpecie.value.toString();
    
    return matchSearch && matchStatus && matchQuadrant && matchSpecie;
  });
});

const selectedAnimal = computed(() => {
  return animals.value.find(a => a.id === selectedAnimalId.value) || null;
});

// Métodos
const loadInitialData = async () => {
  try {
    const [animalsRes, quadrantsRes, speciesRes] = await Promise.all([
      api.get('animals/?limit=500'),
      api.get('quadrants/?limit=500'),
      api.get('species/?limit=500')
    ]);

    animals.value = (animalsRes.data.results || animalsRes.data).map(a => ({
      ...a,
      quadrant_id: a.quadrant,
      specie_id: a.specie
    }));
    
    quadrants.value = quadrantsRes.data.results || quadrantsRes.data;
    species.value = speciesRes.data.results || speciesRes.data;

    // Enriquece dados com nomes
    enrichAnimalsWithNames();
  } catch (err) {
    console.error('Erro ao carregar dados:', err);
  }
};

const enrichAnimalsWithNames = () => {
  animals.value = animals.value.map(animal => {
    const quadrant = quadrants.value.find(q => q.id === animal.quadrant_id);
    const specie = species.value.find(s => s.id === animal.specie_id);

    return {
      ...animal,
      quadrant_name: quadrant?.name || 'N/A',
      specie_name: specie?.name || 'N/A',
      breed_name: animal.breed_name || 'N/A'
    };
  });
};

const selectAnimal = (animal) => {
  selectedAnimalId.value = animal.id;
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('pt-BR');
};

const goToAnimalProfile = () => {
  if (selectedAnimal.value) {
    router.push(`/animal/${selectedAnimal.value.id}`);
  }
};

const goToWeightHistory = () => {
  if (selectedAnimal.value) {
    router.push(`/weight-history/${selectedAnimal.value.id}`);
  }
};

const goToVaccinationHistory = () => {
  if (selectedAnimal.value) {
    router.push(`/vaccination-history/${selectedAnimal.value.id}`);
  }
};

onMounted(() => {
  loadInitialData();
});
</script>

<style scoped>
.animals-consultation-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 20px;
  background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
  border-radius: 12px;
}

@media (max-width: 1024px) {
  .animals-consultation-container {
    grid-template-columns: 1fr;
  }
}

.header {
  grid-column: 1 / -1;
  margin-bottom: 10px;
}

.header h1 {
  color: #00d4ff;
  font-size: 28px;
  margin: 0 0 8px 0;
}

.subtitle {
  color: #888;
  font-size: 14px;
  margin: 0;
}

.filters-section {
  grid-column: 1 / -1;
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
}

.search-box {
  margin-bottom: 15px;
}

.search-input {
  width: 100%;
  padding: 12px;
  background: #0a0a0a;
  border: 1px solid #333;
  border-radius: 6px;
  color: #fff;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.2);
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group label {
  color: #aaa;
  font-size: 12px;
  margin-bottom: 5px;
  font-weight: 500;
}

.filter-select {
  padding: 8px;
  background: #0a0a0a;
  border: 1px solid #333;
  border-radius: 4px;
  color: #fff;
  font-size: 13px;
}

.filter-select:focus {
  outline: none;
  border-color: #00d4ff;
}

.animals-list-container {
  grid-column: 1;
}

.animals-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.animal-card {
  background: #1a1a1a;
  border: 2px solid #333;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.animal-card:hover {
  border-color: #00d4ff;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
}

.animal-card.selected {
  border-color: #00ff88;
  background: rgba(0, 255, 136, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.card-header h3 {
  color: #fff;
  font-size: 16px;
  margin: 0;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: bold;
  text-transform: uppercase;
}

.status-ativo {
  background: #00ff88;
  color: #000;
}

.status-doente {
  background: #ffcc00;
  color: #000;
}

.status-vendido,
.status-obito,
.status-inativo {
  background: #ff4444;
  color: #fff;
}

.card-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.info-item .label {
  color: #888;
}

.info-item .value {
  color: #aaa;
  font-weight: 500;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px;
  color: #666;
}

.details-panel {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 20px;
  position: sticky;
  top: 20px;
  max-height: 90vh;
  overflow-y: auto;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  color: #888;
  font-size: 20px;
  cursor: pointer;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #ff4444;
}

.details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #333;
  padding-bottom: 15px;
}

.details-header h2 {
  color: #00d4ff;
  font-size: 18px;
  margin: 0;
}

.details-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.details-section h3 {
  color: #00d4ff;
  font-size: 14px;
  margin: 0 0 10px 0;
  text-transform: uppercase;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: 8px 0;
  border-bottom: 1px solid #2a2a2a;
}

.info-row .label {
  color: #888;
}

.info-row .value {
  color: #aaa;
  text-align: right;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-top: 1px solid #333;
  padding-top: 15px;
}

.action-btn {
  padding: 10px;
  border: 1px solid #333;
  border-radius: 6px;
  background: #0a0a0a;
  color: #fff;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.profile-btn:hover {
  border-color: #00d4ff;
  color: #00d4ff;
}

.weight-btn:hover {
  border-color: #00ff88;
  color: #00ff88;
}

.vaccine-btn:hover {
  border-color: #ffcc00;
  color: #ffcc00;
}
</style>
