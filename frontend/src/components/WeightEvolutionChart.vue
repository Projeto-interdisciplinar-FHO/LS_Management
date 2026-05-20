<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>{{ title }}</h3>
    </div>
    
    <svg v-if="data.length > 0" :viewBox="`0 0 ${svgWidth} ${svgHeight}`" class="chart-svg">
      <!-- Grid lines -->
      <defs>
        <linearGradient id="lineGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color: #3fb950; stop-opacity: 0.3" />
          <stop offset="100%" style="stop-color: #3fb950; stop-opacity: 0.05" />
        </linearGradient>
      </defs>

      <!-- Y-axis grid lines -->
      <g class="grid-lines">
        <line 
          v-for="i in 5" 
          :key="`grid-${i}`"
          :x1="padding"
          :y1="padding + (svgHeight - 2*padding) * (i - 1) / 4"
          :x2="svgWidth - padding"
          :y2="padding + (svgHeight - 2*padding) * (i - 1) / 4"
          stroke="#30363d"
          stroke-dasharray="2,2"
          opacity="0.5"
        />
      </g>

      <!-- Axes -->
      <line :x1="padding" :y1="padding" :x2="padding" :y2="svgHeight - padding" stroke="#8b949e" stroke-width="2" />
      <line :x1="padding" :y1="svgHeight - padding" :x2="svgWidth - padding" :y2="svgHeight - padding" stroke="#8b949e" stroke-width="2" />

      <!-- Y-axis labels -->
      <g class="axis-labels">
        <text 
          v-for="i in 5" 
          :key="`label-y-${i}`"
          :x="padding - 10"
          :y="padding + (svgHeight - 2*padding) * (i - 1) / 4 + 5"
          text-anchor="end"
          fill="#8b949e"
          font-size="12"
        >
          {{ minWeight + (maxWeight - minWeight) * (4 - i + 1) / 4 }}
        </text>
      </g>

      <!-- Area fill under line -->
      <path :d="areaPath" fill="url(#lineGradient)" />

      <!-- Line plot -->
      <polyline :points="points" class="data-line" />

      <!-- Data points (circles) -->
      <g class="data-points">
        <circle 
          v-for="(point, index) in pointsArray" 
          :key="`point-${index}`"
          :cx="point.x"
          :cy="point.y"
          r="5"
          class="point"
          @mouseover="hoveredPoint = index"
          @mouseleave="hoveredPoint = null"
        />
      </g>

      <!-- Tooltip -->
      <g v-if="hoveredPoint !== null" class="tooltip-group">
        <rect 
          :x="pointsArray[hoveredPoint].x - 50" 
          :y="pointsArray[hoveredPoint].y - 40"
          width="100"
          height="35"
          rx="4"
          class="tooltip-bg"
        />
        <text 
          :x="pointsArray[hoveredPoint].x" 
          :y="pointsArray[hoveredPoint].y - 25"
          text-anchor="middle"
          class="tooltip-text"
        >
          {{ data[hoveredPoint].weight }} kg
        </text>
        <text 
          :x="pointsArray[hoveredPoint].x" 
          :y="pointsArray[hoveredPoint].y - 10"
          text-anchor="middle"
          class="tooltip-date"
        >
          {{ new Date(data[hoveredPoint].weighing_date).toLocaleDateString('pt-BR') }}
        </text>
      </g>
    </svg>

    <div v-else class="empty-chart">
      <p>Sem dados de peso para exibir o gráfico</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  title: {
    type: String,
    default: 'Evolução de Peso'
  }
});

const hoveredPoint = ref(null);
const padding = 60;
const svgWidth = 800;
const svgHeight = 300;

const sortedData = computed(() => {
  return [...props.data].sort((a, b) => 
    new Date(a.weighing_date) - new Date(b.weighing_date)
  );
});

const minWeight = computed(() => {
  if (props.data.length === 0) return 0;
  return Math.min(...props.data.map(d => parseFloat(d.weight))) - 5;
});

const maxWeight = computed(() => {
  if (props.data.length === 0) return 100;
  return Math.max(...props.data.map(d => parseFloat(d.weight))) + 5;
});

const pointsArray = computed(() => {
  if (sortedData.value.length === 0) return [];
  
  const yRange = maxWeight.value - minWeight.value;
  const xStep = (svgWidth - 2 * padding) / (sortedData.value.length - 1 || 1);
  
  return sortedData.value.map((point, index) => ({
    x: padding + index * xStep,
    y: svgHeight - padding - ((parseFloat(point.weight) - minWeight.value) / yRange) * (svgHeight - 2 * padding)
  }));
});

const points = computed(() => {
  return pointsArray.value.map(p => `${p.x},${p.y}`).join(' ');
});

const areaPath = computed(() => {
  if (pointsArray.value.length === 0) return '';
  
  const points = pointsArray.value;
  const path = [
    `M ${points[0].x} ${svgHeight - padding}`,
    ...points.map(p => `L ${p.x} ${p.y}`),
    `L ${points[points.length - 1].x} ${svgHeight - padding}`,
    'Z'
  ];
  
  return path.join(' ');
});
</script>

<style scoped>
.chart-container {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.chart-header {
  margin-bottom: 15px;
}

.chart-header h3 {
  color: #e6edf3;
  font-size: 1rem;
  margin: 0;
}

.chart-svg {
  width: 100%;
  height: auto;
  max-width: 100%;
}

.grid-lines line {
  opacity: 0.3;
}

.data-line {
  fill: none;
  stroke: #3fb950;
  stroke-width: 3;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.data-points {
  cursor: pointer;
}

.point {
  fill: #3fb950;
  stroke: #161b22;
  stroke-width: 2;
  transition: all 0.2s;
}

.point:hover {
  r: 7;
  fill: #58a6ff;
}

.tooltip-bg {
  fill: #0d1117;
  stroke: #3fb950;
  stroke-width: 1;
}

.tooltip-text {
  fill: #3fb950;
  font-weight: bold;
  font-size: 13px;
}

.tooltip-date {
  fill: #8b949e;
  font-size: 11px;
}

.axis-labels {
  font-size: 12px;
  color: #8b949e;
}

.empty-chart {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #8b949e;
}

.empty-chart p {
  margin: 0;
}

@media (max-width: 768px) {
  .chart-container {
    padding: 15px;
  }
}
</style>
