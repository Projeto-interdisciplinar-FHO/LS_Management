<template>
  <!-- Adicionamos uma verificação reativa de classe para garantir a ativação do tema -->
  <div :class="['ls-reports-page-container', { 'ls-dark-active': isDark }]">
    
    <!-- BARRA SUPERIOR E CABEÇALHO -->
    <header class="ls-reports-header-section">
      <div class="ls-reports-header-content">
        <button @click="goHome" class="ls-reports-btn-back">← Voltar ao Dashboard</button>
        <h1 class="ls-reports-main-title">Relatórios de Gestão Individual</h1>
        <p class="ls-reports-main-subtitle">Acompanhe a distribuição consolidada e as flutuações evolutivas de maneira puramente visual e estatística.</p>
      </div>
    </header>

    <!-- SELETOR PREMIUM COM OPÇÃO DE COMPARATIVO GERAL -->
    <section class="ls-reports-selector-wrapper">
      <div class="ls-reports-input-container">
        <label for="ls-animal-dropdown" class="ls-reports-dropdown-label">
          <span class="ls-reports-search-emoji">🔍</span>
          Filtrar Histórico por Animal (Número do Brinco)
        </label>
        <select 
          id="ls-animal-dropdown" 
          v-model="selectedAnimalId" 
          @change="handleSelectionChange" 
          class="ls-reports-select-field"
        >
          <option value="" disabled>Selecione um brinco cadastrado...</option>
          <option value="all">📊 Comparativo geral — Todos os animais simultaneamente</option>
          <option v-for="animal in animalsList" :key="animal.id" :value="animal.id">
            Brinco: #{{ animal.register_number }} — {{ animal.name || 'Sem Nome' }} ({{ animal.weight }} kg)
          </option>
        </select>
      </div>
    </section>

    <!-- LAYOUT PRINCIPAL DE RELATÓRIOS -->
    <div v-if="selectedAnimalId" class="ls-reports-dashboard-layout">
      
      <!-- FILEIRA OPERACIONAL: CARDS 100% COLORIDOS -->
      <section class="ls-reports-kpi-row">
        
        <!-- CARD DE PESO SÓLIDO -->
        <article class="ls-reports-kpi-card ls-reports-kpi-peso">
          <div class="ls-reports-kpi-internal-box">
            <span class="ls-reports-kpi-emoji">⚖️</span>
            <div class="ls-reports-kpi-text-block">
              <span class="ls-reports-kpi-meta">Evolução Biométrica</span>
              <h3 class="ls-reports-kpi-title">Último Peso</h3>
              <div class="ls-reports-kpi-number-zone">
                <strong class="ls-reports-kpi-value">{{ weightLabel }}</strong>
                <span class="ls-reports-kpi-unit">kg</span>
              </div>
            </div>
          </div>
        </article>

        <!-- CARD DE SANITÁRIO SÓLIDO -->
        <article class="ls-reports-kpi-card ls-reports-kpi-vacina">
          <div class="ls-reports-kpi-internal-box">
            <span class="ls-reports-kpi-emoji">💉</span>
            <div class="ls-reports-kpi-text-block">
              <span class="ls-reports-kpi-meta">Historico de Vacinaçao</span>
              <h3 class="ls-reports-kpi-title">Imunizações</h3>
              <div class="ls-reports-kpi-number-zone">
                <strong class="ls-reports-kpi-value">{{ vaccineCount }}</strong>
                <span class="ls-reports-kpi-unit">aplicadas</span>
              </div>
            </div>
          </div>
        </article>

        <!-- CARD LEITEIRO SÓLIDO -->
        <article class="ls-reports-kpi-card ls-reports-kpi-leite">
          <div class="ls-reports-kpi-internal-box">
            <span class="ls-reports-kpi-emoji">🥛</span>
            <div class="ls-reports-kpi-text-block">
              <span class="ls-reports-kpi-meta">Histórico Produtivo</span>
              <h3 class="ls-reports-kpi-title">Manejo Leiteiro</h3>
              <div class="ls-reports-kpi-number-zone">
                <strong class="ls-reports-kpi-value">{{ milkCount }}</strong>
                <span class="ls-reports-kpi-unit">ordenhas</span>
              </div>
            </div>
          </div>
        </article>

      </section>

      <!-- FILEIRA ESTATÍSTICA: TRÊS GRÁFICOS DE PIZZA -->
      <section class="ls-reports-charts-row">
        
        <!-- BLOCO DO GRÁFICO 1 -->
        <div class="ls-reports-chart-block">
          <header class="ls-reports-chart-header">
            <h4 class="ls-reports-chart-title">Distribuição de Ganhos Ponderais</h4>
            <span class="ls-reports-chart-legend">Métrica Flutuante</span>
          </header>
          <div class="ls-reports-chart-container-pizza" :title="weightTooltipTitle">
            <svg class="ls-reports-pizza-svg" viewBox="0 0 200 200">
              <circle r="50" cx="100" cy="100" fill="transparent" stroke="#22c55e" stroke-width="100" :stroke-dasharray="weightSlicePrimary" />
              <circle r="50" cx="100" cy="100" fill="transparent" stroke="#16a34a" stroke-width="100" :stroke-dasharray="weightSliceSecondary" :stroke-dashoffset="weightSliceOffset" />
            </svg>
          </div>
          <footer class="ls-reports-chart-footer-labels">
            <div class="ls-reports-label-item"><span class="ls-reports-dot-peso-1"></span> Ganho Acima da Média</div>
            <div class="ls-reports-label-item"><span class="ls-reports-dot-peso-2"></span> Estabilidade Crítica</div>
          </footer>
        </div>

        <!-- BLOCO DO GRÁFICO 2 -->
        <div class="ls-reports-chart-block">
          <header class="ls-reports-chart-header">
            <h4 class="ls-reports-chart-title">Proporção de Cobertura Sanitária</h4>
            <span class="ls-reports-chart-legend">Status Vacinas</span>
          </header>
          <div class="ls-reports-chart-container-pizza" :title="vaccineTooltipTitle">
            <svg class="ls-reports-pizza-svg" viewBox="0 0 200 200">
              <circle r="50" cx="100" cy="100" fill="transparent" stroke="#a855f7" stroke-width="100" :stroke-dasharray="vaccineSlicePrimary" />
              <circle r="50" cx="100" cy="100" fill="transparent" stroke="#7c3aed" stroke-width="100" :stroke-dasharray="vaccineSliceSecondary" :stroke-dashoffset="vaccineSliceOffset" />
            </svg>
          </div>
          <footer class="ls-reports-chart-footer-labels">
            <div class="ls-reports-label-item"><span class="ls-reports-dot-vac-1"></span> Ciclo Obrigatório Ok</div>
            <div class="ls-reports-label-item"><span class="ls-reports-dot-vac-2"></span> Doses de Reforço</div>
          </footer>
        </div>

        <!-- BLOCO DO GRÁFICO 3 -->
        <div class="ls-reports-chart-block">
          <header class="ls-reports-chart-header">
            <h4 class="ls-reports-chart-title">Rendimento de Ordenhas por Período</h4>
            <span class="ls-reports-chart-legend">Eficiência Láctea</span>
          </header>
          <div class="ls-reports-chart-container-pizza" :title="milkTooltipTitle">
            <svg class="ls-reports-pizza-svg" viewBox="0 0 200 200">
              <circle r="50" cx="100" cy="100" fill="transparent" stroke="#3b82f6" stroke-width="100" :stroke-dasharray="milkSlicePrimary" />
              <circle r="50" cx="100" cy="100" fill="transparent" stroke="#1d4ed8" stroke-width="100" :stroke-dasharray="milkSliceSecondary" :stroke-dashoffset="milkSliceOffset" />
            </svg>
          </div>
          <footer class="ls-reports-chart-footer-labels">
            <div class="ls-reports-label-item"><span class="ls-reports-dot-leite-1"></span> Período Manhã</div>
            <div class="ls-reports-label-item"><span class="ls-reports-dot-leite-2"></span> Período Tarde</div>
          </footer>
        </div>

      </section>

    </div>

    <!-- ESTADO DE TELA VAZIA (PLACEHOLDER) -->
    <div v-else class="ls-reports-empty-state">
      <div class="ls-reports-empty-box-icon">📊</div>
      <h3 class="ls-reports-empty-title">Nenhum Escopo Selecionado</h3>
      <p class="ls-reports-empty-paragraph">Escolha a opção de comparativo geral ou o número de um brinco específico no seletor para renderizar a distribuição dos gráficos.</p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

const selectedAnimalId = ref('')
const animalsList = ref([])
const weightLabel = ref('0.00')
const vaccineCount = ref('0')
const milkCount = ref('0')

const chartCircleLength = 314
const weightSlicePrimary = ref('250 314')
const weightSliceSecondary = ref('64 314')
const weightSliceOffset = ref('-250')
const vaccineSlicePrimary = ref('180 314')
const vaccineSliceSecondary = ref('134 314')
const vaccineSliceOffset = ref('-180')
const milkSlicePrimary = ref('210 314')
const milkSliceSecondary = ref('104 314')
const milkSliceOffset = ref('-210')

const weightPercent = ref(50)
const vaccinePercent = ref(50)
const milkMorningPercent = ref(50)

const weightHistory = ref([])
const vaccineHistory = ref([])
const milkHistory = ref([])

// Estado reativo para monitorar o tema em tempo real
const isDark = ref(false)
let themeObserver = null

const goHome = () => {
  const role = localStorage.getItem('user_role')
  if (role === 'op') router.push('/dashboard-op')
  else router.push('/dashboard-adm')
}

// Função para checar as classes no elemento HTML ou Body do seu app
const checkGlobalTheme = () => {
  const root = document.documentElement
  const body = document.body
  const hasDarkClass = root.classList.contains('dark') || 
                        root.classList.contains('theme-dark') || 
                        body.classList.contains('dark') || 
                        body.classList.contains('theme-dark')
  
  isDark.value = hasDarkClass
}

const getStrokeArray = (percent) => `${Math.max(0, Math.min(100, percent)) * chartCircleLength / 100} ${chartCircleLength}`
const getOffsetValue = (percent) => `-${Math.round(Math.max(0, Math.min(100, percent)) * chartCircleLength / 100)}`

const normalizeDate = (record) => {
  const raw = record.vaccination_date || record.date || record.date_applied || record.created_at || record.updated_at || record.production_date || record.timestamp
  return raw ? new Date(raw) : null
}

const numericWeight = (record) => parseFloat(record.weight || record.value || record.animal_weight || 0) || 0

const updateChartSlices = ({ weightPercent: wp = 50, vaccinePercent: vp = 50, milkMorning: mm = 50 }) => {
  weightPercent.value = wp
  vaccinePercent.value = vp
  milkMorningPercent.value = mm

  weightSlicePrimary.value = getStrokeArray(wp)
  weightSliceSecondary.value = getStrokeArray(100 - wp)
  weightSliceOffset.value = getOffsetValue(wp)

  vaccineSlicePrimary.value = getStrokeArray(vp)
  vaccineSliceSecondary.value = getStrokeArray(100 - vp)
  vaccineSliceOffset.value = getOffsetValue(vp)

  milkSlicePrimary.value = getStrokeArray(mm)
  milkSliceSecondary.value = getStrokeArray(100 - mm)
  milkSliceOffset.value = getOffsetValue(mm)
}

const weightTooltipTitle = computed(() => {
  const rise = weightPercent.value
  const stable = 100 - rise
  return `Acima da média: ${rise}%\nEstabilidade: ${stable}%`
})

const vaccineTooltipTitle = computed(() => {
  const cycleOk = vaccinePercent.value
  const reinforcement = 100 - cycleOk
  return `Ciclo ok: ${cycleOk}%\nReforço: ${reinforcement}%`
})

const milkTooltipTitle = computed(() => {
  const morning = milkMorningPercent.value
  const afternoon = 100 - morning
  return `Período manhã: ${morning}%\nPeríodo tarde: ${afternoon}%`
})

onMounted(() => {
  loadDropdownData()
  checkGlobalTheme()

  // Criamos um observador para capturar mudanças de classe no HTML global instantaneamente
  themeObserver = new MutationObserver(() => {
    checkGlobalTheme()
  })

  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
  themeObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] })
})

onBeforeUnmount(() => {
  if (themeObserver) themeObserver.disconnect()
})

const loadDropdownData = async () => {
  try {
    const response = await api.get('animals/')
    animalsList.value = response.data.results || response.data
  } catch (error) {
    console.error("Erro ao alimentar dropdown de relatórios:", error)
  }
}

const handleSelectionChange = async () => {
  if (!selectedAnimalId.value) return

  if (selectedAnimalId.value === 'all') {
    try {
      const [vaccinesRes, milkRes] = await Promise.all([
        api.getVaccinationsByAnimal(0),
        api.get('milk_production_history/')
      ])

      vaccineHistory.value = Array.isArray(vaccinesRes.data.results || vaccinesRes.data) ? (vaccinesRes.data.results || vaccinesRes.data) : []
      milkHistory.value = Array.isArray(milkRes.data.results || milkRes.data) ? (milkRes.data.results || milkRes.data) : []

      const totalWeight = animalsList.value.reduce((sum, animal) => sum + (parseFloat(animal.weight) || 0), 0)
      const avgWeight = animalsList.value.length ? totalWeight / animalsList.value.length : 0

      weightLabel.value = animalsList.value.length ? avgWeight.toFixed(2) : '0.00'
      vaccineCount.value = String(vaccineHistory.value.length)
      milkCount.value = String(milkHistory.value.length)

      const aboveAverageCount = animalsList.value.filter(animal => (parseFloat(animal.weight) || 0) >= avgWeight).length
      const weightPercent = animalsList.value.length ? Math.round((aboveAverageCount / animalsList.value.length) * 100) : 50
      const vaccinePercent = vaccineHistory.value.length ? Math.round(((vaccineHistory.value.filter(v => {
        const next = normalizeDate(v)
        return next ? next > new Date() : false
      }).length) / vaccineHistory.value.length) * 100) : 50
      const milkMorning = milkHistory.value.length ? Math.round((milkHistory.value.filter(m => {
        const dt = normalizeDate(m)
        return dt ? dt.getHours() < 12 : false
      }).length / milkHistory.value.length) * 100) : 50

      updateChartSlices({ weightPercent, vaccinePercent, milkMorning })
      return
    } catch (error) {
      console.error('Erro ao carregar resumo geral de relatórios:', error)
      weightLabel.value = '0.00'
      vaccineCount.value = '0'
      milkCount.value = '0'
      updateChartSlices({ weightPercent: 50, vaccinePercent: 50, milkMorning: 50 })
      return
    }
  }

  const target = animalsList.value.find(a => String(a.id) === String(selectedAnimalId.value))
  weightLabel.value = target ? String(target.weight || '0.00') : '0.00'

  try {
    const id = Number(selectedAnimalId.value)
    const [vaccinesRes, milkRes, weightRes] = await Promise.all([
      api.getVaccinationsByAnimal(id),
      api.getMilkProductionByAnimal(id),
      api.getWeightHistoryByAnimal(id)
    ])

    const rawVaccines = vaccinesRes.data.results || vaccinesRes.data
    const rawMilk = milkRes.data.historico || milkRes.data.results || milkRes.data
    const rawWeight = weightRes.data.historico || weightRes.data.results || weightRes.data

    vaccineHistory.value = Array.isArray(rawVaccines) ? rawVaccines : []
    milkHistory.value = Array.isArray(rawMilk) ? rawMilk : []
    weightHistory.value = Array.isArray(rawWeight) ? rawWeight : []

    const latestWeightRecord = [...weightHistory.value].sort((a, b) => {
      const dateA = normalizeDate(a)
      const dateB = normalizeDate(b)
      return (dateB ? dateB.getTime() : 0) - (dateA ? dateA.getTime() : 0)
    })[0]

    const latestWeight = latestWeightRecord ? numericWeight(latestWeightRecord) : parseFloat(target?.weight || 0)
    weightLabel.value = latestWeight ? latestWeight.toFixed(2) : '0.00'

    const weightAverage = weightHistory.value.length ? weightHistory.value.reduce((sum, record) => sum + numericWeight(record), 0) / weightHistory.value.length : latestWeight
    const aboveAverageCount = weightHistory.value.filter(record => numericWeight(record) >= weightAverage).length
    const weightPercent = weightHistory.value.length ? Math.round((aboveAverageCount / weightHistory.value.length) * 100) : 50

    vaccineCount.value = String(vaccineHistory.value.length)
    milkCount.value = String(milkHistory.value.length)

    const vaccinePercent = vaccineHistory.value.length ? Math.round(((vaccineHistory.value.filter(v => {
      const next = normalizeDate(v)
      return next ? next > new Date() : false
    }).length) / vaccineHistory.value.length) * 100) : 50

    const milkMorning = milkHistory.value.length ? Math.round((milkHistory.value.filter(m => {
      const dt = normalizeDate(m)
      return dt ? dt.getHours() < 12 : false
    }).length / milkHistory.value.length) * 100) : 50

    updateChartSlices({ weightPercent, vaccinePercent, milkMorning })
  } catch (error) {
    console.error("Erro ao carregar histórico real de relatórios:", error)
    vaccineCount.value = '0'
    milkCount.value = '0'
    updateChartSlices({ weightPercent: 50, vaccinePercent: 50, milkMorning: 50 })
  }
}
</script>

<style scoped>


.ls-reports-page-container {
  padding: 40px;
  background-color: #f0f5fb;
  min-height: 100vh;
  font-family: 'Lexend', sans-serif;
  color: #102a43;
  transition: background-color 0.2s ease, color 0.2s ease;
  box-sizing: border-box;
}

.ls-reports-header-section {
  margin-bottom: 32px;
  border-bottom: 1px solid #d8e3ef;
  padding-bottom: 24px;
}
.ls-reports-btn-back {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  color: #102a43;
  padding: 10px 20px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  margin-bottom: 16px;
  font-family: inherit;
  transition: background 0.2s ease;
}
.ls-reports-btn-back:hover {
  background: #f1f5f9;
}
.ls-reports-main-title {
  margin: 0 0 6px 0;
  font-size: 2.2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #102a43;
}
.ls-reports-main-subtitle {
  margin: 0;
  color: #486581;
  font-size: 1.05rem;
  line-height: 1.5;
}

.ls-reports-selector-wrapper {
  background: #ffffff;
  border: 1px solid #d8e3ef;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 10px 25px rgba(15, 42, 67, 0.04);
  margin-bottom: 32px;
}
.ls-reports-input-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.ls-reports-dropdown-label {
  font-size: 0.95rem;
  font-weight: 700;
  color: #102a43;
  display: flex;
  align-items: center;
  gap: 6px;
}
.ls-reports-select-field {
  padding: 14px 18px;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  font-size: 1rem;
  outline: none;
  background: #ffffff;
  color: #102a43;
  font-family: inherit;
  font-weight: 600;
  cursor: pointer;
}

.ls-reports-kpi-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}
.ls-reports-kpi-card {
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 15px 35px rgba(15, 42, 67, 0.06);
  color: #ffffff !important;
}
.ls-reports-kpi-internal-box {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}
.ls-reports-kpi-emoji {
  font-size: 2.2rem;
  background: rgba(255, 255, 255, 0.18);
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
}
.ls-reports-kpi-text-block {
  display: flex;
  flex-direction: column;
}
.ls-reports-kpi-meta {
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  opacity: 0.85;
  margin-bottom: 2px;
}
.ls-reports-kpi-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0 0 12px 0;
}
.ls-reports-kpi-number-zone {
  display: flex;
  align-items: baseline;
  gap: 6px;
}
.ls-reports-kpi-value {
  font-size: 2.4rem;
  font-weight: 800;
  line-height: 1;
}
.ls-reports-kpi-unit {
  font-size: 0.95rem;
  font-weight: 600;
  opacity: 0.9;
}

.ls-reports-kpi-peso { background: #16a34a !important; }
.ls-reports-kpi-vacina { background: #7c3aed !important; }
.ls-reports-kpi-leite { background: #1d4ed8 !important; }

.ls-reports-charts-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.ls-reports-chart-block {
  background: #ffffff;
  border: 1px solid #d8e3ef;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 15px 35px rgba(15, 42, 67, 0.04);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.ls-reports-chart-header {
  width: 100%;
  text-align: left;
  margin-bottom: 20px;
  border-bottom: 1px solid #f0f5fb;
  padding-bottom: 12px;
}
.ls-reports-chart-title {
  font-size: 1rem;
  font-weight: 700;
  color: #102a43;
  margin: 0 0 2px 0;
}
.ls-reports-chart-legend {
  font-size: 0.75rem;
  font-weight: 600;
  color: #627d98;
}
.ls-reports-chart-container-pizza {
  width: 150px;
  height: 150px;
  margin: 16px 0;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ls-reports-pizza-svg {
  transform: rotate(-90deg);
  border-radius: 50%;
}
.ls-reports-chart-footer-labels {
  width: 100%;
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid #f0f5fb;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  color: #486581;
}
.ls-reports-label-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
.ls-reports-label-item span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.ls-reports-dot-peso-1 { background-color: #22c55e; }
.ls-reports-dot-peso-2 { background-color: #16a34a; }
.ls-reports-dot-vac-1 { background-color: #a855f7; }
.ls-reports-dot-vac-2 { background-color: #7c3aed; }
.ls-reports-dot-leite-1 { background-color: #3b82f6; }
.ls-reports-dot-leite-2 { background-color: #1d4ed8; }

.ls-reports-empty-state {
  text-align: center;
  padding: 80px 40px;
  background: #ffffff;
  border: 1px solid #d8e3ef;
  border-radius: 24px;
  max-width: 620px;
  margin: 40px auto 0;
  box-shadow: 0 15px 35px rgba(15, 42, 67, 0.04);
}
.ls-reports-empty-box-icon { font-size: 3rem; margin-bottom: 16px; }
.ls-reports-empty-title { font-size: 1.4rem; color: #102a43; margin-bottom: 8px; font-weight: 700; }
.ls-reports-empty-paragraph { color: #486581; line-height: 1.6; font-size: 0.95rem; margin: 0; }


.ls-reports-page-container.ls-dark-active {
  background-color: #111827 !important;
}

.ls-reports-page-container.ls-dark-active .ls-reports-selector-wrapper,
.ls-reports-page-container.ls-dark-active .ls-reports-chart-block,
.ls-reports-page-container.ls-dark-active .ls-reports-empty-state {
  background-color: #111827 !important; 
  border-color: #1f2937 !important;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5) !important;
}

.ls-reports-page-container.ls-dark-active .ls-reports-chart-header,
.ls-reports-page-container.ls-dark-active .ls-reports-chart-footer-labels,
.ls-reports-page-container.ls-dark-active .ls-reports-header-section {
  border-color: #1f2937 !important;
}

.ls-reports-page-container.ls-dark-active .ls-reports-select-field,
.ls-reports-page-container.ls-dark-active .ls-reports-btn-back {
  background-color: #1f2937 !important;
  border-color: #374151 !important;
  color: #ffffff !important;
}

.ls-reports-page-container.ls-dark-active .ls-reports-select-field option {
  background-color: #111827 !important;
  color: #ffffff !important;
}

/* Tons escuros para os cards de KPI */
.ls-reports-page-container.ls-dark-active .ls-reports-kpi-peso { background-color: #064e3b !important; }
.ls-reports-page-container.ls-dark-active .ls-reports-kpi-vacina { background-color: #4c1d95 !important; }
.ls-reports-page-container.ls-dark-active .ls-reports-kpi-leite { background-color: #1e3a8a !important; }
.ls-reports-page-container.ls-dark-active .ls-reports-kpi-emoji { background-color: rgba(0, 0, 0, 0.3) !important; }

/* Fontes e Títulos forçados para Branco Puro */
.ls-reports-page-container.ls-dark-active .ls-reports-main-title,
.ls-reports-page-container.ls-dark-active .ls-reports-dropdown-label,
.ls-reports-page-container.ls-dark-active .ls-reports-chart-title,
.ls-reports-page-container.ls-dark-active .ls-reports-empty-title {
  color: #ffffff !important;
}

/* Legendas e Textos de apoio em Cinza Claro Legível */
.ls-reports-page-container.ls-dark-active .ls-reports-main-subtitle,
.ls-reports-page-container.ls-dark-active .ls-reports-chart-legend,
.ls-reports-page-container.ls-dark-active .ls-reports-chart-footer-labels,
.ls-reports-page-container.ls-dark-active .ls-reports-empty-paragraph {
  color: #e5e7eb !important;
}

</style>