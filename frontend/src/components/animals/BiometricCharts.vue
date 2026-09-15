<template>
  <div class="biometric-charts-container">
    <!-- Loading state -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando gráficos...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-state">
      <p>❌ Erro ao carregar gráficos: {{ error }}</p>
    </div>

    <!-- No data -->
    <div v-else-if="!hasData" class="no-data-state">
      <p>📊 Dados insuficientes para exibir gráficos.</p>
    </div>

    <!-- Charts -->
    <div v-else class="charts-wrapper">
      <!-- Frequência Cardíaca Chart -->
      <div class="chart-card">
        <div class="chart-title">📈 Frequência Cardíaca (últimos 7 dias)</div>
        <div class="chart-container">
          <Line :data="heartRateChartData" :options="chartOptions" />
        </div>
      </div>

      <!-- Sono Chart -->
      <div class="chart-card">
        <div class="chart-title">💤 Horas de Sono (últimos 7 dias)</div>
        <div class="chart-container">
          <Line :data="sleepChartData" :options="chartOptions" />
        </div>
      </div>

      <!-- Temperatura Chart -->
      <div class="chart-card">
        <div class="chart-title">🌡️ Temperatura Corporal (últimos 7 dias)</div>
        <div class="chart-container">
          <Line :data="temperatureChartData" :options="chartOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export default {
  name: 'BiometricCharts',
  components: {
    Line,
  },
  props: {
    animalId: {
      type: Number,
      required: true,
    },
    days: {
      type: Number,
      default: 7,
    },
  },
  data() {
    return {
      readings: [],
      loading: true,
      error: null,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            display: true,
            labels: {
              color: '#cbd5e1',
              font: {
                size: 12,
                weight: '600',
              },
            },
          },
          tooltip: {
            backgroundColor: 'rgba(30, 41, 59, 0.9)',
            titleColor: '#f1f5f9',
            bodyColor: '#cbd5e1',
            borderColor: 'rgba(148, 163, 184, 0.3)',
            borderWidth: 1,
            padding: 12,
            displayColors: true,
            callbacks: {
              label: (context) => {
                let label = context.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                label += context.parsed.y;
                if (context.dataset.yAxisID === 'y') {
                  label += ' BPM';
                } else if (context.dataset.yAxisID === 'y1') {
                  label += ' h';
                } else if (context.dataset.yAxisID === 'y2') {
                  label += '°C';
                }
                return label;
              },
            },
          },
        },
        scales: {
          x: {
            grid: {
              color: 'rgba(148, 163, 184, 0.1)',
              drawBorder: false,
            },
            ticks: {
              color: '#94a3b8',
              font: {
                size: 11,
              },
            },
          },
          y: {
            grid: {
              color: 'rgba(148, 163, 184, 0.1)',
              drawBorder: false,
            },
            ticks: {
              color: '#94a3b8',
              font: {
                size: 11,
              },
            },
            title: {
              display: true,
              text: 'BPM',
              color: '#94a3b8',
            },
          },
          y1: {
            type: 'linear',
            position: 'right',
            grid: {
              drawOnChartArea: false,
            },
            ticks: {
              color: '#94a3b8',
              font: {
                size: 11,
              },
            },
            title: {
              display: true,
              text: 'Horas',
              color: '#94a3b8',
            },
          },
          y2: {
            type: 'linear',
            position: 'right',
            grid: {
              drawOnChartArea: false,
            },
            ticks: {
              color: '#94a3b8',
              font: {
                size: 11,
              },
            },
            title: {
              display: true,
              text: '°C',
              color: '#94a3b8',
            },
          },
        },
      },
    };
  },
  computed: {
    apiBaseUrl() {
      return import.meta.env.VITE_API_URL || 'http://localhost:8000';
    },

    hasData() {
      return this.readings && this.readings.length > 0;
    },

    chartLabels() {
      return this.readings.map((reading) => {
        const date = new Date(reading.reading_timestamp);
        return date.toLocaleString('pt-BR', {
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
        });
      });
    },

    heartRateChartData() {
      return {
        labels: this.chartLabels,
        datasets: [
          {
            label: 'Frequência Cardíaca (BPM)',
            data: this.readings.map((r) => r.heart_rate),
            borderColor: '#ef4444',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointBackgroundColor: '#ef4444',
            pointBorderColor: '#fff',
            pointRadius: 4,
            pointHoverRadius: 6,
            yAxisID: 'y',
          },
        ],
      };
    },

    sleepChartData() {
      return {
        labels: this.chartLabels,
        datasets: [
          {
            label: 'Horas de Sono',
            data: this.readings.map((r) => r.sleep_duration),
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointBackgroundColor: '#3b82f6',
            pointBorderColor: '#fff',
            pointRadius: 4,
            pointHoverRadius: 6,
            yAxisID: 'y1',
          },
        ],
      };
    },

    temperatureChartData() {
      return {
        labels: this.chartLabels,
        datasets: [
          {
            label: 'Temperatura Corporal (°C)',
            data: this.readings
              .map((r) => r.body_temperature)
              .map((t) => (t !== null ? t : null)),
            borderColor: '#f59e0b',
            backgroundColor: 'rgba(245, 158, 11, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointBackgroundColor: '#f59e0b',
            pointBorderColor: '#fff',
            pointRadius: 4,
            pointHoverRadius: 6,
            yAxisID: 'y2',
            spanGaps: true,
          },
        ],
      };
    },
  },

  mounted() {
    this.fetchHistoryData();
  },

  methods: {
    async fetchHistoryData() {
      try {
        this.loading = true;
        this.error = null;

        const response = await fetch(
          `${this.apiBaseUrl}/biometrics/biometric-readings/history/?animal_id=${this.animalId}&days=${this.days}`
        );

        if (!response.ok) {
          throw new Error('Falha ao carregar histórico de biometria');
        }

        const data = await response.json();
        this.readings = data.readings || data.results || [];
        this.loading = false;
      } catch (err) {
        this.error = err.message;
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.biometric-charts-container {
  width: 100%;
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

/* Charts Wrapper */
.charts-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
}

.chart-card {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.chart-card:hover {
  border-color: rgba(148, 163, 184, 0.4);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.chart-title {
  font-size: 14px;
  font-weight: 700;
  color: #cbd5e1;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}

/* Responsive */
@media (max-width: 1024px) {
  .charts-wrapper {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .chart-container {
    height: 250px;
  }

  .chart-title {
    font-size: 12px;
  }
}
</style>
