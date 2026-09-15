<template>
  <div class="biometric-cards-container">
    <!-- Loading state -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando dados de biometria...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-state">
      <p>❌ Erro ao carregar biometria: {{ error }}</p>
    </div>

    <!-- Sem dados -->
    <div v-else-if="!latestReading" class="no-data-state">
      <p>📡 Nenhuma leitura de biometria disponível para este animal.</p>
    </div>

    <!-- Biometric Cards -->
    <div v-else class="cards-grid">
      <!-- Frequência Cardíaca -->
      <div class="biometric-card heart-rate-card" :class="alertLevelClass('heart_rate')">
        <div class="card-header">
          <span class="card-icon">🫀</span>
          <span class="card-title">Frequência Cardíaca</span>
        </div>
        <div class="card-value">
          {{ latestReading.heart_rate }} <span class="unit">BPM</span>
        </div>
        <div class="card-status">
          <span v-if="latestReading.heart_rate < 60" class="status-badge low">Baixa</span>
          <span v-else-if="latestReading.heart_rate < 80" class="status-badge normal">Normal</span>
          <span v-else-if="latestReading.heart_rate < 100" class="status-badge elevated">Elevada</span>
          <span v-else class="status-badge high">Muito Alta</span>
        </div>
        <div class="card-meta">
          Leitura: {{ formatTime(latestReading.reading_timestamp) }}
        </div>
      </div>

      <!-- Sono -->
      <div class="biometric-card sleep-card" :class="alertLevelClass('sleep_duration')">
        <div class="card-header">
          <span class="card-icon">💤</span>
          <span class="card-title">Sono (24h)</span>
        </div>
        <div class="card-value">
          {{ latestReading.sleep_duration }} <span class="unit">horas</span>
        </div>
        <div class="card-status">
          <span v-if="latestReading.sleep_duration < 2" class="status-badge high">Crítico</span>
          <span v-else-if="latestReading.sleep_duration < 4" class="status-badge elevated">Reduzido</span>
          <span v-else class="status-badge normal">Normal</span>
        </div>
        <div class="card-meta">
          Ideal: 6-8 horas
        </div>
      </div>

      <!-- Temperatura -->
      <div class="biometric-card temperature-card" :class="alertLevelClass('body_temperature')">
        <div class="card-header">
          <span class="card-icon">🌡️</span>
          <span class="card-title">Temperatura</span>
        </div>
        <div class="card-value">
          {{ latestReading.body_temperature || 'N/A' }} <span class="unit">°C</span>
        </div>
        <div class="card-status">
          <span v-if="!latestReading.body_temperature" class="status-badge neutral">Sem dados</span>
          <span v-else-if="latestReading.body_temperature > 39.5" class="status-badge critical">Crítica</span>
          <span v-else-if="latestReading.body_temperature > 38.5" class="status-badge high">Elevada</span>
          <span v-else class="status-badge normal">Normal</span>
        </div>
        <div class="card-meta">
          Normal: 37.5-38.5°C
        </div>
      </div>

      <!-- Sintomas -->
      <div class="biometric-card symptoms-card" :class="{ 'has-symptoms': latestReading.symptoms }">
        <div class="card-header">
          <span class="card-icon">🩺</span>
          <span class="card-title">Sintomas Detectados</span>
        </div>
        <div v-if="latestReading.symptoms" class="symptoms-content">
          <p class="symptoms-text">{{ latestReading.symptoms }}</p>
        </div>
        <div v-else class="symptoms-content">
          <p class="symptoms-text">✅ Nenhum sintoma detectado</p>
        </div>
        <div class="card-meta">
          Última leitura: {{ formatTime(latestReading.reading_timestamp) }}
        </div>
      </div>
    </div>

    <!-- Alerts Section -->
    <div v-if="activeAlerts.length > 0" class="alerts-section">
      <div class="section-title">🚨 Alertas Ativos</div>
      <div class="alerts-list">
        <div
          v-for="alert in activeAlerts"
          :key="alert.id"
          class="alert-item"
          :class="`severity-${alert.severity}`"
        >
          <div class="alert-icon">{{ getAlertEmoji(alert.severity) }}</div>
          <div class="alert-content">
            <div class="alert-title">{{ alert.title }}</div>
            <div class="alert-description">{{ alert.description }}</div>
            <div class="alert-reason">Motivo: {{ alert.reason }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sensor Info -->
    <div v-if="latestReading" class="sensor-info">
      <div class="info-row">
        <span class="info-label">Bateria do Sensor:</span>
        <span class="info-value">{{ latestReading.sensor_battery || 'N/A' }}%</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BiometricCard',
  props: {
    animalId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      latestReading: null,
      activeAlerts: [],
      loading: true,
      error: null,
    };
  },
  computed: {
    apiBaseUrl() {
      return import.meta.env.VITE_API_URL || 'http://localhost:8000';
    },
  },
  mounted() {
    this.fetchBiometricData();
    // Atualizar a cada 5 minutos
    setInterval(() => this.fetchBiometricData(), 5 * 60 * 1000);
  },
  methods: {
    async fetchBiometricData() {
      try {
        this.loading = true;
        this.error = null;

        const response = await fetch(
          `${this.apiBaseUrl}/biometrics/biometric-readings/by_animal/?animal_id=${this.animalId}`
        );

        if (!response.ok) {
          throw new Error('Falha ao carregar dados de biometria');
        }

        const data = await response.json();

        this.latestReading = data.latest_reading;
        this.activeAlerts = data.active_alerts || [];

        this.loading = false;
      } catch (err) {
        this.error = err.message;
        this.loading = false;
      }
    },

    formatTime(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    },

    alertLevelClass(metric) {
      if (!this.latestReading) return '';

      const alertLevel = this.latestReading.alert_level || 'normal';
      return `alert-${alertLevel}`;
    },

    getAlertEmoji(severity) {
      const emojis = {
        critical: '🚨',
        high: '🔴',
        medium: '⚠️',
        low: '💭',
      };
      return emojis[severity] || '❓';
    },
  },
};
</script>

<style scoped>
.biometric-cards-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Loading & Error States */
.loading-state,
.no-data-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
  text-align: center;
  background: linear-gradient(135deg, rgba(230, 237, 243, 0.1) 0%, rgba(30, 41, 59, 0.05) 100%);
  border-radius: 12px;
  color: #94a3b8;
  font-size: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(148, 163, 184, 0.2);
  border-top-color: #60a5fa;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-state {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

/* Cards Grid */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.biometric-card {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.biometric-card:hover {
  border-color: rgba(148, 163, 184, 0.4);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

/* Alert Level Colors */
.biometric-card.alert-critical {
  border-left: 4px solid #ef4444;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%),
              linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, transparent 100%);
}

.biometric-card.alert-warning {
  border-left: 4px solid #f59e0b;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%),
              linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, transparent 100%);
}

.biometric-card.alert-normal {
  border-left: 4px solid #10b981;
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.card-icon {
  font-size: 24px;
  line-height: 1;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Card Value */
.card-value {
  font-size: 32px;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 12px;
  line-height: 1;
}

.unit {
  font-size: 14px;
  font-weight: 500;
  color: #94a3b8;
  margin-left: 4px;
}

/* Status Badge */
.card-status {
  margin-bottom: 12px;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.status-badge.normal {
  background-color: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.status-badge.elevated {
  background-color: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.status-badge.high {
  background-color: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.status-badge.critical {
  background-color: rgba(239, 68, 68, 0.3);
  color: #ff6b6b;
  animation: pulse 2s ease-in-out infinite;
}

.status-badge.low {
  background-color: rgba(99, 102, 241, 0.2);
  color: #6366f1;
}

.status-badge.neutral {
  background-color: rgba(148, 163, 184, 0.2);
  color: #94a3b8;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.card-meta {
  font-size: 12px;
  color: #64748b;
  font-style: italic;
}

/* Symptoms Card Special */
.symptoms-card {
  grid-column: span 1;
}

.symptoms-content {
  margin: 12px 0;
}

.symptoms-text {
  font-size: 14px;
  color: #cbd5e1;
  margin: 0;
  line-height: 1.5;
}

.symptoms-card.has-symptoms .symptoms-text {
  color: #fbbf24;
  font-weight: 600;
}

/* Alerts Section */
.alerts-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #ef4444;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alert-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.5) 100%);
  border-left: 4px solid;
}

.alert-item.severity-critical {
  border-left-color: #ef4444;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(30, 41, 59, 0.5) 100%);
}

.alert-item.severity-high {
  border-left-color: #f59e0b;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(30, 41, 59, 0.5) 100%);
}

.alert-item.severity-medium {
  border-left-color: #eab308;
  background: linear-gradient(135deg, rgba(234, 179, 8, 0.1) 0%, rgba(30, 41, 59, 0.5) 100%);
}

.alert-icon {
  font-size: 24px;
  line-height: 1.4;
  flex-shrink: 0;
}

.alert-content {
  flex-grow: 1;
}

.alert-title {
  font-size: 14px;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 4px;
}

.alert-description {
  font-size: 13px;
  color: #cbd5e1;
  margin-bottom: 4px;
}

.alert-reason {
  font-size: 12px;
  color: #94a3b8;
  font-style: italic;
}

/* Sensor Info */
.sensor-info {
  padding: 12px;
  background: rgba(148, 163, 184, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.info-label {
  color: #94a3b8;
  font-weight: 600;
}

.info-value {
  color: #cbd5e1;
  font-weight: 700;
}

/* Responsive */
@media (max-width: 768px) {
  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .card-value {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }

  .symptoms-card {
    grid-column: span 1;
  }
}
</style>
