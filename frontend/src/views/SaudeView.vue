<template>
  <div class="saude-wrapper">
    <header class="page-header">
      <div class="header-info">
        <button @click="goHome" class="btn-back">← Voltar ao Dashboard</button>
        <h1>💪 Saúde & Vacinação</h1>
        <p>Controle centralizado de vacinações da fazenda</p>
      </div>
    </header>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando dados de vacinação...</p>
    </div>

    <div v-else class="saude-content">
      <!-- FILTROS DE STATUS -->
      <section class="filter-tabs">
        <button 
          v-for="filter in vaccineFilters" 
          :key="filter.value"
          class="filter-tab"
          :class="{ active: activeFilter === filter.value }"
          @click="activeFilter = filter.value"
        >
          <span class="filter-icon">{{ filter.icon }}</span>
          <span class="filter-label">{{ filter.label }}</span>
          <span class="filter-count">{{ getCountByFilter(filter.value) }}</span>
        </button>
      </section>

      <!-- CARD DE RESUMO -->
      <section class="summary-cards">
        <div class="summary-card alert-overdue">
          <div class="summary-icon">⚠</div>
          <div class="summary-info">
            <span class="summary-label">Vacinações Atrasadas</span>
            <span class="summary-value">{{ overdueCount }}</span>
          </div>
        </div>
        <div class="summary-card alert-upcoming">
          <div class="summary-icon">📅</div>
          <div class="summary-info">
            <span class="summary-label">Próximos 7 Dias</span>
            <span class="summary-value">{{ upcomingCount }}</span>
          </div>
        </div>
        <div class="summary-card alert-ok">
          <div class="summary-icon">✓</div>
          <div class="summary-info">
            <span class="summary-label">Em Dia</span>
            <span class="summary-value">{{ upToDateCount }}</span>
          </div>
        </div>
      </section>

      <!-- LISTA DE VACINAÇÕES FILTRADAS -->
      <section class="vaccinations-list">
        <h2>{{ getFilterLabel(activeFilter) }}</h2>
        
        <div v-if="filteredVaccinations.length === 0" class="empty-state">
          <span class="empty-icon">📭</span>
          <p>Nenhuma vacinação encontrada para este filtro.</p>
        </div>

        <div v-else class="vaccines-grid">
          <div v-for="vac in filteredVaccinations" :key="vac.id" class="vaccine-card" :class="{ 'overdue': isOverdue(vac) }">
            <div class="vaccine-card-header">
              <h3 class="vaccine-card-title">{{ vac.animal_name }}</h3>
              <span class="vaccine-card-id">Brinco: {{ vac.animal_id }}</span>
            </div>

            <div class="vaccine-card-body">
              <div class="vaccine-detail">
                <span class="label">Vacina:</span>
                <span class="value">{{ vac.vaccine_name }}</span>
              </div>
              <div class="vaccine-detail">
                <span class="label">Aplicada:</span>
                <span class="value">{{ formatDate(vac.vaccination_date) }}</span>
              </div>
              <div class="vaccine-detail">
                <span class="label">Próxima Dose:</span>
                <span class="value" :style="{ color: isOverdue(vac) ? '#f85149' : '#3fb950' }">
                  {{ formatDate(vac.next_vaccination_date) }}
                  <span v-if="getDaysInfo(vac)" class="days-info">
                    ({{ getDaysInfo(vac) }})
                  </span>
                </span>
              </div>
              <div class="vaccine-detail">
                <span class="label">Dosagem:</span>
                <span class="value">{{ vac.dosage }} mL</span>
              </div>
            </div>

            <div class="vaccine-card-status" :class="{ 'overdue': isOverdue(vac), 'upcoming': isUpcoming(vac) }">
              {{ getStatusLabel(vac) }}
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const router = useRouter();

const goHome = () => {
  const role = localStorage.getItem('user_role');
  if (role === 'op') router.push('/dashboard-op');
  else router.push('/dashboard-adm');
};
const loading = ref(true);
const vaccinations = ref([]);
const activeFilter = ref('all');

const vaccineFilters = [
  { value: 'all', label: 'Todas', icon: '📋' },
  { value: 'overdue', label: 'Atrasadas', icon: '⚠' },
  { value: 'upcoming', label: 'Próximos 7 dias', icon: '📅' },
  { value: 'uptodate', label: 'Em Dia', icon: '✓' }
];

const filteredVaccinations = computed(() => {
  if (activeFilter.value === 'all') {
    return vaccinations.value.sort((a, b) => new Date(b.vaccination_date) - new Date(a.vaccination_date));
  }
  if (activeFilter.value === 'overdue') {
    return vaccinations.value.filter(v => isOverdue(v)).sort((a, b) => new Date(a.next_vaccination_date) - new Date(b.next_vaccination_date));
  }
  if (activeFilter.value === 'upcoming') {
    return vaccinations.value.filter(v => isUpcoming(v)).sort((a, b) => new Date(a.next_vaccination_date) - new Date(b.next_vaccination_date));
  }
  if (activeFilter.value === 'uptodate') {
    return vaccinations.value.filter(v => !isOverdue(v) && !isUpcoming(v)).sort((a, b) => new Date(b.vaccination_date) - new Date(a.vaccination_date));
  }
  return vaccinations.value;
});

const overdueCount = computed(() => vaccinations.value.filter(v => isOverdue(v)).length);
const upcomingCount = computed(() => vaccinations.value.filter(v => isUpcoming(v)).length);
const upToDateCount = computed(() => vaccinations.value.filter(v => !isOverdue(v) && !isUpcoming(v)).length);

const formatDate = (dateStr) => {
  if (!dateStr) return '—';
  const date = new Date(dateStr);
  return date.toLocaleDateString('pt-BR');
};

const isOverdue = (vac) => {
  if (!vac.next_vaccination_date) return false;
  const nextDate = new Date(vac.next_vaccination_date);
  return nextDate < new Date();
};

const isUpcoming = (vac) => {
  if (!vac.next_vaccination_date) return false;
  const nextDate = new Date(vac.next_vaccination_date);
  const today = new Date();
  const sevenDaysFromNow = new Date(today.getTime() + 7 * 24 * 60 * 60 * 1000);
  return nextDate >= today && nextDate <= sevenDaysFromNow;
};

const getDaysInfo = (vac) => {
  if (!vac.next_vaccination_date) return null;
  const nextDate = new Date(vac.next_vaccination_date);
  const today = new Date();
  const diff = Math.ceil((nextDate - today) / (1000 * 60 * 60 * 24));
  
  if (diff < 0) return `${Math.abs(diff)} dias atrás`;
  if (diff === 0) return 'hoje';
  return `em ${diff} dias`;
};

const getStatusLabel = (vac) => {
  if (isOverdue(vac)) return '⚠ ATRASADA';
  if (isUpcoming(vac)) return '📅 PRÓXIMA SEMANA';
  return '✓ EM DIA';
};

const getCountByFilter = (filter) => {
  if (filter === 'all') return vaccinations.value.length;
  if (filter === 'overdue') return overdueCount.value;
  if (filter === 'upcoming') return upcomingCount.value;
  if (filter === 'uptodate') return upToDateCount.value;
  return 0;
};

const getFilterLabel = (filter) => {
  const f = vaccineFilters.find(f => f.value === filter);
  return f ? f.label : 'Todas';
};

onMounted(async () => {
  try {
    const response = await api.getVaccinationsByAnimal(0); // 0 significa todas
    vaccinations.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    console.error("Erro ao buscar vacinações:", error);
    vaccinations.value = [];
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.saude-wrapper {
  padding: 40px;
  background-color: #0d1117;
  min-height: 100vh;
  color: #e6edf3;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.page-header {
  margin-bottom: 40px;
  border-bottom: 1px solid #30363d;
  padding-bottom: 20px;
}

.header-info h1 {
  font-size: 2rem;
  color: #58a6ff;
  margin-bottom: 10px;
}

.header-info p {
  color: #8b949e;
  font-size: 1rem;
}

.btn-back {
  background: transparent;
  border: 1px solid #30363d;
  color: #8b949e;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: all 0.3s;
}

.btn-back:hover {
  border-color: #58a6ff;
  color: #58a6ff;
}

/* LOADING STATE */
.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 4px solid #30363d;
  border-top-color: #58a6ff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* FILTER TABS */
.filter-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #30363d;
  flex-wrap: wrap;
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 8px;
  color: #8b949e;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  font-weight: 500;
}

.filter-tab:hover {
  border-color: #58a6ff;
  color: #58a6ff;
  background: rgba(88, 166, 255, 0.05);
}

.filter-tab.active {
  background: linear-gradient(135deg, #3fb950 0%, #2d8737 100%);
  border-color: #3fb950;
  color: white;
}

.filter-count {
  display: inline-block;
  min-width: 24px;
  height: 24px;
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  text-align: center;
  line-height: 20px;
}

.filter-tab.active .filter-count {
  background: rgba(255, 255, 255, 0.2);
}

/* SUMMARY CARDS */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.summary-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  border-left: 4px solid #30363d;
}

.summary-card.alert-overdue {
  border-left-color: #f85149;
  background: rgba(248, 81, 73, 0.05);
}

.summary-card.alert-upcoming {
  border-left-color: #d29922;
  background: rgba(210, 153, 34, 0.05);
}

.summary-card.alert-ok {
  border-left-color: #3fb950;
  background: rgba(63, 185, 80, 0.05);
}

.summary-icon {
  font-size: 2rem;
}

.summary-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.summary-label {
  font-size: 0.85rem;
  color: #8b949e;
  text-transform: uppercase;
  font-weight: 600;
}

.summary-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #e6edf3;
}

/* VACCINES LIST */
.vaccinations-list {
  margin-bottom: 40px;
}

.vaccinations-list h2 {
  font-size: 1.3rem;
  margin-bottom: 20px;
  color: #e6edf3;
  border-bottom: 1px solid #30363d;
  padding-bottom: 10px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  background: #161b22;
  border: 1px dashed #30363d;
  border-radius: 8px;
  color: #8b949e;
}

.empty-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 10px;
}

/* VACCINES GRID */
.vaccines-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.vaccine-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  border-left: 4px solid #3fb950;
}

.vaccine-card.overdue {
  border-left-color: #f85149;
  background: rgba(248, 81, 73, 0.02);
}

.vaccine-card:hover {
  border-color: #58a6ff;
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(88, 166, 255, 0.2);
}

.vaccine-card-header {
  padding: 16px;
  background: #0d1117;
  border-bottom: 1px solid #30363d;
}

.vaccine-card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e6edf3;
  margin: 0 0 5px 0;
}

.vaccine-card-id {
  font-size: 0.85rem;
  color: #8b949e;
}

.vaccine-card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.vaccine-detail {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
}

.vaccine-detail .label {
  color: #8b949e;
  font-weight: 600;
  min-width: 100px;
}

.vaccine-detail .value {
  color: #e6edf3;
  text-align: right;
  flex: 1;
}

.days-info {
  display: block;
  font-size: 0.8rem;
  color: #8b949e;
}

.vaccine-card-status {
  padding: 12px 16px;
  background: rgba(63, 185, 80, 0.1);
  color: #3fb950;
  font-weight: 600;
  font-size: 0.9rem;
  text-align: center;
  border-top: 1px solid #30363d;
}

.vaccine-card-status.overdue {
  background: rgba(248, 81, 73, 0.1);
  color: #f85149;
}

.vaccine-card-status.upcoming {
  background: rgba(210, 153, 34, 0.1);
  color: #d29922;
}

@media (max-width: 768px) {
  .saude-wrapper {
    padding: 20px;
  }

  .vaccines-grid {
    grid-template-columns: 1fr;
  }
}
</style>
