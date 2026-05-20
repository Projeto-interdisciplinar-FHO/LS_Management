<template>
  <div v-if="hasAlerts" class="alert-banner-wrapper">
    <!-- Loading -->
    <div v-if="loading" class="banner-content">
      <div class="spinner-mini"></div>
      <p>Carregando alertas...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="banner-content error">
      <p>❌ Erro ao carregar alertas: {{ error }}</p>
    </div>

    <!-- Critical Alerts -->
    <div v-else class="banner-content">
      <div class="alert-icon-large">🚨</div>
      <div class="alert-text-wrapper">
        <div class="banner-title">URGENTE: Animal com Alerta Crítico</div>
        <div
          v-for="alert in criticalAlerts"
          :key="alert.id"
          class="alert-message"
        >
          <span class="animal-badge">{{ alert.animal_name }}</span>
          <span class="alert-description">
            {{ alert.title }} no Quadrante {{ alert.animal_quadrant }}.
            {{ alert.description }}
          </span>
        </div>
      </div>
      <div class="banner-actions">
        <button @click="acknowledgeAlert" class="btn-acknowledge">
          ✓ Reconhecer
        </button>
      </div>
    </div>

    <!-- Dismiss button -->
    <button @click="dismissBanner" class="btn-dismiss">×</button>
  </div>
</template>

<script>
export default {
  name: 'AlertBanner',
  props: {
    refreshInterval: {
      type: Number,
      default: 30 * 1000, // 30 segundos
    },
  },
  data() {
    return {
      criticalAlerts: [],
      loading: false,
      error: null,
      dismissed: true,
      refreshTimer: null,
    };
  },
  computed: {
    apiBaseUrl() {
      return import.meta.env.VITE_API_URL || 'http://localhost:8000';
    },
    hasAlerts() {
      return !this.dismissed && this.criticalAlerts.length > 0 && !this.loading;
    },
  },
  mounted() {
    this.fetchCriticalAlerts();
    // Atualizar a cada 30 segundos
    this.refreshTimer = setInterval(
      () => this.fetchCriticalAlerts(),
      this.refreshInterval
    );
  },
  beforeUnmount() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
  },
  methods: {
    async fetchCriticalAlerts() {
      try {
        this.loading = true;
        const response = await fetch(
          `${this.apiBaseUrl}/biometrics/animal-alerts/critical/`
        );

        if (!response.ok) {
          throw new Error('Falha ao carregar alertas críticos');
        }

        const data = await response.json();
        this.criticalAlerts = data.alerts || [];
        this.loading = false;
      } catch (err) {
        this.error = err.message;
        this.loading = false;
      }
    },

    async acknowledgeAlert() {
      if (this.criticalAlerts.length === 0) return;

      try {
        const alert = this.criticalAlerts[0];
        const response = await fetch(
          `${this.apiBaseUrl}/biometrics/animal-alerts/${alert.id}/acknowledge/`,
          { method: 'POST' }
        );

        if (response.ok) {
          // Remove o alerta da lista
          this.criticalAlerts.shift();
          if (this.criticalAlerts.length === 0) {
            this.dismissed = true;
          }
        }
      } catch (err) {
        console.error('Erro ao reconhecer alerta:', err);
      }
    },

    dismissBanner() {
      this.dismissed = true;
    },
  },
};
</script>

<style scoped>
.alert-banner-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
  border: 2px solid #ef4444;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 8px 16px rgba(239, 68, 68, 0.2);
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.alert-banner-wrapper.error {
  border-color: #f97316;
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.2) 0%, rgba(249, 115, 22, 0.1) 100%);
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-grow: 1;
  min-height: 60px;
}

.banner-content.error {
  color: #f97316;
}

/* Spinner Mini */
.spinner-mini {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(239, 68, 68, 0.2);
  border-top-color: #ef4444;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  flex-shrink: 0;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Alert Icon */
.alert-icon-large {
  font-size: 32px;
  line-height: 1;
  flex-shrink: 0;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

/* Text Wrapper */
.alert-text-wrapper {
  flex-grow: 1;
  min-width: 0;
}

.banner-title {
  font-size: 14px;
  font-weight: 700;
  color: #ef4444;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.alert-message {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #fecaca;
  line-height: 1.4;
}

.animal-badge {
  display: inline-block;
  padding: 2px 8px;
  background-color: rgba(239, 68, 68, 0.3);
  border-radius: 4px;
  font-weight: 700;
  color: #fca5a5;
  white-space: nowrap;
  flex-shrink: 0;
}

.alert-description {
  flex-grow: 1;
  word-break: break-word;
}

/* Actions */
.banner-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.btn-acknowledge {
  padding: 8px 16px;
  background-color: #ef4444;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-acknowledge:hover {
  background-color: #dc2626;
  transform: scale(1.05);
}

.btn-acknowledge:active {
  transform: scale(0.95);
}

/* Dismiss Button */
.btn-dismiss {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  padding: 0;
  background: transparent;
  color: #ef4444;
  border: none;
  font-size: 24px;
  font-weight: 700;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.3s ease;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-dismiss:hover {
  opacity: 1;
}

/* Responsive */
@media (max-width: 768px) {
  .alert-banner-wrapper {
    flex-direction: column;
    align-items: flex-start;
    padding: 12px 16px;
  }

  .banner-content {
    width: 100%;
  }

  .banner-actions {
    width: 100%;
    margin-top: 12px;
  }

  .btn-acknowledge {
    flex-grow: 1;
    text-align: center;
  }

  .alert-message {
    flex-direction: column;
    gap: 4px;
  }
}

@media (max-width: 480px) {
  .alert-banner-wrapper {
    padding: 12px;
  }

  .alert-icon-large {
    font-size: 24px;
  }

  .banner-title {
    font-size: 12px;
  }

  .alert-message {
    font-size: 12px;
  }
}
</style>
