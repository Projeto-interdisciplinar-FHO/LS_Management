<template>
  <section class="vaccine-card">
    <div class="card-header">
      <h3 class="card-title">💉 Manejo Sanitário - Histórico de Vacinação</h3>
      <span v-if="!loading" class="status-badge" :class="{ 'status-danger': hasOverdue, 'status-success': !hasOverdue }">
        {{ hasOverdue ? '⚠ Com Atraso' : '✓ Em Dia' }}
      </span>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner-mini"></div>
      <p>Carregando histórico de vacinação...</p>
    </div>

    <div v-else-if="vaccinations.length === 0" class="empty-state">
      <p>Nenhuma vacinação registrada para este animal.</p>
    </div>

    <div v-else class="vaccine-timeline">
      <div v-for="vacc in vaccinations" :key="vacc.id" class="vaccine-entry" :class="{ 'overdue': isOverdue(vacc) }">
        <div class="vaccine-info">
          <div class="vaccine-header">
            <span class="vaccine-name">{{ vacc.vaccine_name }}</span>
            <span class="vaccine-status" :class="{ 'status-ok': !isOverdue(vacc), 'status-alert': isOverdue(vacc) }">
              {{ isOverdue(vacc) ? '⚠ Atrasada' : '✓ Em Dia' }}
            </span>
          </div>
          <div class="vaccine-dates">
            <div class="date-item">
              <span class="date-label">Aplicada:</span>
              <span class="date-value">{{ formatDate(vacc.vaccination_date) }}</span>
            </div>
            <div class="date-item">
              <span class="date-label">Próxima Dose:</span>
              <span class="date-value" :style="{ color: isOverdue(vacc) ? '#f85149' : '#3fb950' }">
                {{ formatDate(vacc.next_vaccination_date) }}
                <span v-if="getDaysRemaining(vacc)" class="days-remaining">
                  ({{ getDaysRemaining(vacc) }} dias)
                </span>
              </span>
            </div>
          </div>
          <div class="vaccine-details">
            <span class="detail-item">Dosagem: {{ vacc.dosage }} mL</span>
            <span v-if="vacc.doses_taken" class="detail-item">Doses: {{ vacc.doses_taken }}/{{ vacc.total_doses }}</span>
          </div>
        </div>
        <div class="vaccine-indicator" :class="{ 'ok': !isOverdue(vacc), 'alert': isOverdue(vacc) }">
          {{ isOverdue(vacc) ? '⚠' : '✓' }}
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/services/api';

const props = defineProps({
  animalId: {
    type: Number,
    required: true
  }
});

const loading = ref(true);
const vaccinations = ref([]);

const hasOverdue = computed(() => {
  return vaccinations.value.some(vacc => isOverdue(vacc));
});

const formatDate = (dateStr) => {
  if (!dateStr) return '—';
  const date = new Date(dateStr);
  return date.toLocaleDateString('pt-BR', { year: 'numeric', month: 'long', day: 'numeric' });
};

const isOverdue = (vacc) => {
  if (!vacc.next_vaccination_date) return false;
  const nextDate = new Date(vacc.next_vaccination_date);
  return nextDate < new Date();
};

const getDaysRemaining = (vacc) => {
  if (!vacc.next_vaccination_date) return null;
  const nextDate = new Date(vacc.next_vaccination_date);
  const today = new Date();
  const diff = Math.ceil((nextDate - today) / (1000 * 60 * 60 * 24));
  
  if (diff < 0) return `${Math.abs(diff)} dias atrás`;
  if (diff === 0) return 'hoje';
  return `em ${diff}`;
};

onMounted(async () => {
  try {
    const response = await api.getVaccinationsByAnimal(props.animalId);
    vaccinations.value = Array.isArray(response.data) ? response.data : response.data.results || [];
    // Ordenar por data de vacinação (mais recentes primeiro)
    vaccinations.value.sort((a, b) => new Date(b.vaccination_date) - new Date(a.vaccination_date));
  } catch (error) {
    console.error("Erro ao buscar histórico de vacinação:", error);
    vaccinations.value = [];
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.vaccine-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #30363d;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #e6edf3;
  margin: 0;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-badge.status-success {
  background: rgba(63, 185, 80, 0.1);
  color: #3fb950;
  border: 1px solid #3fb950;
}

.status-badge.status-danger {
  background: rgba(248, 81, 73, 0.1);
  color: #f85149;
  border: 1px solid #f85149;
}

.loading-state {
  text-align: center;
  padding: 20px;
  color: #8b949e;
}

.spinner-mini {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid #30363d;
  border-top-color: #58a6ff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #8b949e;
}

.vaccine-timeline {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.vaccine-entry {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 8px;
  border-left: 4px solid #3fb950;
  transition: all 0.3s;
}

.vaccine-entry.overdue {
  border-left-color: #f85149;
  background: rgba(248, 81, 73, 0.05);
}

.vaccine-entry:hover {
  border-color: #58a6ff;
}

.vaccine-info {
  flex: 1;
}

.vaccine-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.vaccine-name {
  font-weight: 600;
  font-size: 1rem;
  color: #e6edf3;
}

.vaccine-status {
  font-size: 0.85rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
}

.vaccine-status.status-ok {
  background: rgba(63, 185, 80, 0.1);
  color: #3fb950;
}

.vaccine-status.status-alert {
  background: rgba(248, 81, 73, 0.1);
  color: #f85149;
}

.vaccine-dates {
  display: flex;
  gap: 20px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.date-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.date-label {
  font-size: 0.75rem;
  color: #8b949e;
  text-transform: uppercase;
}

.date-value {
  font-size: 0.9rem;
  color: #e6edf3;
  font-weight: 500;
}

.days-remaining {
  display: inline-block;
  font-size: 0.8rem;
  color: #8b949e;
  margin-left: 4px;
}

.vaccine-details {
  display: flex;
  gap: 15px;
  font-size: 0.85rem;
  color: #8b949e;
}

.detail-item {
  display: flex;
  align-items: center;
}

.vaccine-indicator {
  font-size: 1.5rem;
  margin-left: 15px;
  min-width: 30px;
  text-align: center;
}

.vaccine-indicator.ok {
  color: #3fb950;
}

.vaccine-indicator.alert {
  color: #f85149;
  animation: pulse-alert 1.5s ease-in-out infinite;
}

@keyframes pulse-alert {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@media (max-width: 768px) {
  .vaccine-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .vaccine-dates {
    flex-direction: column;
    gap: 8px;
  }

  .vaccine-entry {
    flex-direction: column;
    align-items: flex-start;
  }

  .vaccine-indicator {
    margin-left: 0;
    margin-top: 10px;
  }
}
</style>
