<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>{{ title }}</h3>
    </div>

    <svg
      v-if="data.length > 0"
      :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
      class="chart-svg"
      role="img"
      :aria-label="`${title}: ${data.length} pesagem(ns), de ${fmtPeso(pesoMinimoReal)} a ${fmtPeso(pesoMaximoReal)} kg`"
      @mouseleave="hoveredPoint = null"
    >
      <defs>
        <linearGradient id="lineGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color: var(--accent); stop-opacity: 0.3" />
          <stop offset="100%" style="stop-color: var(--accent); stop-opacity: 0.05" />
        </linearGradient>
      </defs>

      <!-- Linhas de grade -->
      <g class="grid-lines">
        <line
          v-for="i in 5"
          :key="`grid-${i}`"
          :x1="padding"
          :y1="linhaY(i)"
          :x2="svgWidth - padding"
          :y2="linhaY(i)"
          stroke="var(--line)"
          stroke-dasharray="2,2"
        />
      </g>

      <!-- Eixos -->
      <line :x1="padding" :y1="padding" :x2="padding" :y2="svgHeight - padding" stroke="var(--text-3)" stroke-width="1.5" />
      <line :x1="padding" :y1="svgHeight - padding" :x2="svgWidth - padding" :y2="svgHeight - padding" stroke="var(--text-3)" stroke-width="1.5" />

      <!-- Números do eixo Y: ficam bem à esquerda, longe dos pontos -->
      <g class="axis-labels">
        <text
          v-for="i in 5"
          :key="`label-y-${i}`"
          :x="padding - 14"
          :y="linhaY(i) + 4"
          text-anchor="end"
          fill="var(--text-2)"
          font-size="12"
        >
          {{ fmtPeso(minWeight + (maxWeight - minWeight) * (5 - i) / 4) }}
        </text>
      </g>

      <!-- Datas do eixo X -->
      <g class="axis-labels">
        <text
          v-for="(ponto, indice) in pointsArray"
          v-show="mostrarRotuloX(indice)"
          :key="`label-x-${indice}`"
          :x="ponto.x"
          :y="svgHeight - padding + 24"
          text-anchor="middle"
          fill="var(--text-2)"
          font-size="12"
        >
          {{ dataCurta(sortedData[indice].weighing_date) }}
        </text>
      </g>

      <path :d="areaPath" fill="url(#lineGradient)" />
      <polyline :points="points" class="data-line" />

      <!-- Pontos: ficam dentro da área do gráfico, nunca em cima do eixo -->
      <g class="data-points">
        <circle
          v-for="(point, index) in pointsArray"
          :key="`point-${index}`"
          :cx="point.x"
          :cy="point.y"
          r="5"
          class="point"
          tabindex="0"
          role="button"
          :aria-label="`${dataCompleta(sortedData[index].weighing_date)}: ${fmtPeso(sortedData[index].weight)} kg`"
          @mouseover="hoveredPoint = index"
          @focus="hoveredPoint = index"
          @blur="hoveredPoint = null"
          @click="hoveredPoint = hoveredPoint === index ? null : index"
        />
      </g>

      <!-- Dica de valor: sempre dentro do gráfico (vira para o lado ou para baixo se faltar espaço) -->
      <g v-if="dica" class="tooltip-group" pointer-events="none">
        <rect :x="dica.x" :y="dica.y" :width="dica.largura" :height="dica.altura" rx="6" class="tooltip-bg" />
        <text :x="dica.x + dica.largura / 2" :y="dica.y + 20" text-anchor="middle" class="tooltip-text">
          {{ fmtPeso(sortedData[hoveredPoint].weight) }} kg
        </text>
        <text :x="dica.x + dica.largura / 2" :y="dica.y + 37" text-anchor="middle" class="tooltip-date">
          {{ dataCompleta(sortedData[hoveredPoint].weighing_date) }}
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
const padding = 64;
const insetX = 28; // afasta o primeiro e o último ponto dos eixos
const svgWidth = 800;
const svgHeight = 300;

const sortedData = computed(() => {
  return [...props.data].sort((a, b) => chaveData(a.weighing_date).localeCompare(chaveData(b.weighing_date)));
});

// Datas "2026-10-22" viram dia/mês/ano sem passar por fuso horário: antes,
// new Date('2026-10-22') virava 21/10 no horário de Brasília (UTC-3).
function chaveData(valor) {
  return String(valor ?? '').slice(0, 10);
}

function partesData(valor) {
  const [ano, mes, dia] = chaveData(valor).split('-');
  return { ano, mes, dia };
}

function dataCompleta(valor) {
  const { ano, mes, dia } = partesData(valor);
  return ano && mes && dia ? `${dia}/${mes}/${ano}` : '—';
}

function dataCurta(valor) {
  const { mes, dia } = partesData(valor);
  return mes && dia ? `${dia}/${mes}` : '';
}

// Peso com até 2 casas, vírgula decimal e sem zeros sobrando (18,25 · 20).
function fmtPeso(valor) {
  const numero = Number(valor);
  if (!Number.isFinite(numero)) return '—';
  return numero.toLocaleString('pt-BR', { maximumFractionDigits: 2 });
}

const pesoMinimoReal = computed(() => Math.min(...props.data.map(d => parseFloat(d.weight))));
const pesoMaximoReal = computed(() => Math.max(...props.data.map(d => parseFloat(d.weight))));

// Escala do eixo Y com folga e valores "redondos" (sem 13,75; 18,25...).
const minWeight = computed(() => {
  if (props.data.length === 0) return 0;
  return Math.max(0, Math.floor((pesoMinimoReal.value - 2) / 2) * 2);
});

const maxWeight = computed(() => {
  if (props.data.length === 0) return 100;
  const topo = Math.ceil((pesoMaximoReal.value + 2) / 2) * 2;
  return topo > minWeight.value ? topo : minWeight.value + 2;
});

function linhaY(i) {
  return padding + (svgHeight - 2 * padding) * (i - 1) / 4;
}

const pointsArray = computed(() => {
  const dados = sortedData.value;
  if (dados.length === 0) return [];

  const yRange = maxWeight.value - minWeight.value || 1;
  const largura = svgWidth - 2 * padding - 2 * insetX;
  const xStep = dados.length > 1 ? largura / (dados.length - 1) : 0;

  return dados.map((point, index) => ({
    x: dados.length > 1 ? padding + insetX + index * xStep : svgWidth / 2,
    y: svgHeight - padding - ((parseFloat(point.weight) - minWeight.value) / yRange) * (svgHeight - 2 * padding)
  }));
});

// Com muitas pesagens, mostra só algumas datas para não amontoar.
function mostrarRotuloX(indice) {
  const total = pointsArray.value.length;
  const passo = Math.ceil(total / 8);
  return indice % passo === 0 || indice === total - 1 && (total - 1) % passo >= Math.ceil(passo / 2);
}

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

const dica = computed(() => {
  if (hoveredPoint.value === null) return null;
  const ponto = pointsArray.value[hoveredPoint.value];
  if (!ponto) return null;

  const largura = 112;
  const altura = 46;
  const x = Math.min(Math.max(ponto.x - largura / 2, padding), svgWidth - padding - largura + 8);
  const acima = ponto.y - altura - 14;
  const y = acima >= 4 ? acima : ponto.y + 14; // sem espaço em cima: abre embaixo
  return { x, y, largura, altura };
});
</script>

<style scoped>
.chart-container {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.chart-header {
  margin-bottom: 15px;
}

.chart-header h3 {
  color: var(--text);
  font-size: 1rem;
  margin: 0;
}

.chart-svg {
  width: 100%;
  height: auto;
  max-width: 100%;
  overflow: visible;
}

.grid-lines line {
  opacity: 0.6;
}

.data-line {
  fill: none;
  stroke: var(--ok);
  stroke-width: 3;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.data-points {
  cursor: pointer;
}

.point {
  fill: var(--ok);
  stroke: var(--surface);
  stroke-width: 2;
  transition: r 0.15s, fill 0.15s;
}

.point:hover,
.point:focus-visible {
  r: 7;
  fill: var(--info);
  outline: none;
}

/* Dica invertida: escura no tema claro e clara no escuro, sempre legível. */
.tooltip-bg {
  fill: var(--text);
  filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.25));
}

.tooltip-text {
  fill: var(--surface);
  font-weight: 700;
  font-size: 14px;
}

.tooltip-date {
  fill: var(--surface);
  opacity: 0.8;
  font-size: 12px;
}

.axis-labels {
  font-size: 12px;
}

.empty-chart {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: var(--text-2);
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
