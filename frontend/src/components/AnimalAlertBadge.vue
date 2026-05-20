<template>
  <div v-if="hasAlerts" class="alert-badge-wrapper" :class="`severity-${highestSeverity}`">
    <div class="alert-pulse"></div>
    <span class="alert-icon">{{ getAlertEmoji(highestSeverity) }}</span>
    <span v-if="showCount" class="alert-count">{{ alertCount }}</span>
  </div>
</template>

<script>
export default {
  name: 'AnimalAlertBadge',
  props: {
    animalId: {
      type: Number,
      required: true,
    },
    showCount: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      alerts: [],
      loading: false,
    };
  },
  computed: {
    apiBaseUrl() {
      return import.meta.env.VITE_API_URL || 'http://localhost:8000';
    },

    hasAlerts() {
      return this.alerts.length > 0;
    },

    alertCount() {
      return this.alerts.length;
    },

    highestSeverity() {
      if (!this.hasAlerts) return 'none';

      const severityOrder = ['critical', 'high', 'medium', 'low'];
      for (const severity of severityOrder) {
        if (this.alerts.some((a) => a.severity === severity && a.status === 'active')) {
          return severity;
        }
      }
      return 'low';
    },
  },
  mounted() {
    this.fetchAlerts();
    // Atualizar a cada minuto
    setInterval(() => this.fetchAlerts(), 60 * 1000);
  },
  methods: {
    async fetchAlerts() {
      try {
        const response = await fetch(
          `${this.apiBaseUrl}/biometrics/animal-alerts/by_animal/?animal_id=${this.animalId}&status=active`
        );

        if (!response.ok) {
          throw new Error('Falha ao carregar alertas');
        }

        const data = await response.json();
        this.alerts = data.results || data.alerts || [];
      } catch (err) {
        console.error('Erro ao carregar alertas do animal:', err);
        this.alerts = [];
      }
    },

    getAlertEmoji(severity) {
      const emojis = {
        critical: '🚨',
        high: '🔴',
        medium: '⚠️',
        low: '💭',
        none: '',
      };
      return emojis[severity] || '';
    },
  },
};
</script>

<style scoped>
.alert-badge-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.alert-badge-wrapper.severity-critical {
  background-color: rgba(239, 68, 68, 0.2);
  border: 2px solid #ef4444;
  animation: pulse-critical 1s ease-in-out infinite;
}

.alert-badge-wrapper.severity-high {
  background-color: rgba(249, 115, 22, 0.2);
  border: 2px solid #f97316;
  animation: pulse 1.5s ease-in-out infinite;
}

.alert-badge-wrapper.severity-medium {
  background-color: rgba(234, 179, 8, 0.2);
  border: 2px solid #eab308;
}

.alert-badge-wrapper.severity-low {
  background-color: rgba(99, 102, 241, 0.2);
  border: 2px solid #6366f1;
}

@keyframes pulse-critical {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(239, 68, 68, 0);
  }
}

@keyframes pulse {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(249, 115, 22, 0.7);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(249, 115, 22, 0);
  }
}

.alert-pulse {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background-color: transparent;
  animation: pulse-ring 2s ease-out infinite;
}

@keyframes pulse-ring {
  0% {
    box-shadow: 0 0 0 0 currentColor;
  }
  70% {
    box-shadow: 0 0 0 8px rgba(239, 68, 68, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0);
  }
}

.alert-icon {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  line-height: 1;
}

.alert-count {
  position: absolute;
  bottom: -2px;
  right: -2px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  background-color: #ef4444;
  color: #fff;
  border-radius: 50%;
  font-size: 10px;
  font-weight: 700;
  border: 2px solid #0f172a;
}

/* Tooltip on hover */
.alert-badge-wrapper:hover::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(30, 41, 59, 0.95);
  color: #fca5a5;
  padding: 6px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
  margin-bottom: 8px;
  border: 1px solid rgba(239, 68, 68, 0.3);
  z-index: 10;
}

/* Responsive */
@media (max-width: 480px) {
  .alert-badge-wrapper {
    width: 24px;
    height: 24px;
    font-size: 12px;
  }

  .alert-count {
    width: 16px;
    height: 16px;
    font-size: 9px;
  }
}
</style>
