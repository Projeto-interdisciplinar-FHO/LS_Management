<template>
  <div class="reports-wrapper">
    <header class="page-header">
      <div class="header-content">
        <button @click="goHome" class="btn-back">← Voltar ao Dashboard</button>
        <h1>Relatórios de Gestão Individual</h1>
        <p>Selecione um animal pelo brinco para auditar o histórico de evolução, vacinas e pesagens.</p>
      </div>
    </header>

    <section class="animal-selector-card">
      <div class="input-group">
        <label for="animal-select">🔍 Escolha o Animal (Número do Brinco)</label>
        <select id="animal-select" v-model="selectedAnimalId" @change="handleAnimalChange" class="select-animal">
          <option value="" disabled>Selecione um brinco cadastrado...</option>
          <option v-for="animal in animalsList" :key="animal.id" :value="animal.id">
            Brinco: #{{ animal.register_number }} — {{ animal.name || 'Sem Nome' }} ({{ animal.weight }} kg)
          </option>
        </select>
      </div>
    </section>

    <div class="reports-container">
      <div v-if="selectedAnimalId" class="summary-cards-grid">
        <section class="glass-card ficha-card">
          <header class="card-header-inline">
            <h2>Ficha do Animal</h2>
            <span class="badge">Brinco #{{ selectedAnimal.register_number || 'N/A' }}</span>
          </header>
          <div class="ficha-grid">
            <div class="ficha-item"><span>Nome</span><strong>{{ selectedAnimal.name || 'Sem nome' }}</strong></div>
            <div class="ficha-item"><span>Espécie</span><strong>{{ selectedAnimal.specie_name || selectedAnimal.specie || 'N/A' }}</strong></div>
            <div class="ficha-item"><span>Raça</span><strong>{{ selectedAnimal.breed_name || 'Não informado' }}</strong></div>
            <div class="ficha-item"><span>Quadrante</span><strong>{{ selectedAnimal.quadrant_name || selectedAnimal.quadrant || 'N/A' }}</strong></div>
            <div class="ficha-item"><span>Propósito</span><strong>{{ selectedAnimal.purpose_name || selectedAnimal.purpose || 'N/A' }}</strong></div>
            <div class="ficha-item"><span>Status</span><strong class="text-capitalize">{{ selectedAnimal.status || (selectedAnimal.active ? 'ativo' : 'inativo') }}</strong></div>
            <div class="ficha-item"><span>Sexo</span><strong>{{ selectedAnimal.sex === 'f' ? 'Fêmea' : 'Macho' }}</strong></div>
            <div class="ficha-item"><span>Data de Nascimento</span><strong>{{ formatDate(selectedAnimal.birth_date) }}</strong></div>
            <div class="ficha-item"><span>Peso Atual</span><strong>{{ selectedAnimal.weight || 0 }} kg</strong></div>
          </div>
        </section>

        <section class="glass-card comparison-card">
          <header class="card-header-inline">
            <h2>Comparativo Individual x Grupo</h2>
            <span class="badge">{{ groupStats.groupName }}</span>
          </header>
          <div class="comparison-grid">
            <div class="comparison-item">
              <span>Animais no grupo</span>
              <strong>{{ groupStats.groupSize }}</strong>
            </div>
            <div class="comparison-item">
              <span>Peso médio do grupo</span>
              <strong>{{ groupStats.groupAvgWeight.toFixed(1) }} kg</strong>
            </div>
            <div class="comparison-item">
              <span>Vacinas médias do grupo</span>
              <strong>{{ groupStats.groupAverageVaccines.toFixed(1) }}</strong>
            </div>
            <div class="comparison-item">
              <span>Média de leite /30d</span>
              <strong>{{ groupStats.groupAverageMilk30.toFixed(1) }} L</strong>
            </div>
            <div class="comparison-item highlight-item">
              <span>Peso do animal</span>
              <strong>{{ selectedAnimal.weight || 0 }} kg</strong>
            </div>
            <div class="comparison-item highlight-item">
              <span>Vacinas do animal</span>
              <strong>{{ groupStats.selectedVaccinesCount }}</strong>
            </div>
            <div class="comparison-item highlight-item">
              <span>Leite do animal /30d</span>
              <strong>{{ groupStats.selectedMilkLastMonth }} L</strong>
            </div>
            <div class="comparison-item highlight-item">
              <span>Diferença de peso</span>
              <strong>{{ groupStats.weightDeltaPercent }}%</strong>
            </div>
          </div>
        </section>
      </div>

      <nav class="tabs-nav">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="{ 'active': activeTab === tab.id }"
          class="tab-button"
        >
          {{ tab.icon }} {{ tab.label }}
        </button>
      </nav>

      <div v-if="loadingHistory && selectedAnimalId" class="loading-history">
        <div class="spinner"></div>
        <p>Buscando históricos do brinco selecionado...</p>
      </div>

      <main v-else class="tab-content-area">
        
        <div v-if="activeTab === 'weight_individual'" class="glass-card">
          <header class="card-header-inline">
            <h2>Histórico de Linha de Peso</h2>
            <span class="badge">{{ weightHistory.length }} Registros</span>
          </header>
          
          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Data da Pesagem</th>
                  <th class="text-right">Peso Medido (kg)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="weight in weightHistory" :key="weight.id">
                  <td>{{ formatDate(weight.date || weight.created_at) }}</td>
                  <td class="text-right font-bold text-green">{{ weight.weight }} kg</td>
                </tr>
                <tr v-if="weightHistory.length === 0">
                  <td colspan="2" class="text-center text-muted">Nenhuma pesagem lançada para este animal.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-if="activeTab === 'vaccination_individual'" class="glass-card">
          <header class="card-header-inline">
            <h2>Vacinas Aplicadas e Imunização</h2>
            <span class="badge">{{ vaccineHistory.length }} Vacinas</span>
          </header>
          
          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Data de Aplicação</th>
                  <th>Vacina / Medicamento</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="vac in vaccineHistory" :key="vac.id">
                  <td>{{ formatDate(vac.date || vac.created_at) }}</td>
                  <td class="font-bold text-purple">{{ vac.vaccine_name || `Vacina ID: ${vac.vaccine_id || vac.vaccine}` }}</td>
                  <td><span class="badge-status-clean">Aplicada</span></td>
                </tr>
                <tr v-if="vaccineHistory.length === 0">
                  <td colspan="3" class="text-center text-muted">Nenhuma vacina registrada no histórico deste animal.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-if="activeTab === 'milk_production'" class="glass-card">
          <header class="card-header-inline">
            <h2>Histórico de Ordenhas (Litros)</h2>
            <span class="badge">{{ milkHistory.length }} Coletas</span>
          </header>
          
          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Data da Coleta</th>
                  <th class="text-right">Volume Extraído</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="milk in milkHistory" :key="milk.id">
                  <td>{{ formatDate(milk.date || milk.created_at) }}</td>
                  <td class="text-right font-bold text-blue">{{ milk.milk_quantity || milk.quantity }} Litros</td>
                </tr>
                <tr v-if="milkHistory.length === 0">
                  <td colspan="2" class="text-center text-muted">Nenhum registro de ordenha encontrado para este animal.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-if="activeTab === 'feeding_history'" class="glass-card">
          <header class="card-header-inline">
            <h2>Histórico de Alimentação</h2>
            <span class="badge">{{ feedingHistory.length }} Registros</span>
          </header>
          
          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Data do Trato</th>
                  <th>Alimento / Ração</th>
                  <th class="text-right">Quantidade (kg)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="feeding in feedingHistory" :key="feeding.id">
                  <td>{{ formatDate(feeding.date_fed || feeding.created_at) }}</td>
                  <td class="font-bold">{{ feeding.feed_name || feeding.food_name || 'Ração Padrão' }}</td>
                  <td class="text-right font-bold text-orange">{{ feeding.quantity }} kg</td>
                </tr>
                <tr v-if="feedingHistory.length === 0">
                  <td colspan="3" class="text-center text-muted">Nenhum registro de alimentação encontrado para este animal.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-if="activeTab === 'herd_report'" class="glass-card">
          <header class="card-header-inline">
            <h2>Relatório do Rebanho</h2>
            <span class="badge">{{ herdReport.totalAnimals }} Animais</span>
          </header>
          <div class="report-grid">
            <div class="report-metric">
              <span>Total de animais cadastrados</span>
              <strong>{{ herdReport.totalAnimals }}</strong>
            </div>
            <div class="report-metric">
              <span>Peso médio geral</span>
              <strong>{{ herdReport.averageWeight.toFixed(1) }} kg</strong>
            </div>
            <div class="report-metric">
              <span>Média de vacinas por animal</span>
              <strong>{{ herdReport.averageVaccinations.toFixed(1) }}</strong>
            </div>
            <div class="report-metric">
              <span>Total leite /30d</span>
              <strong>{{ herdReport.milkLast30Days.toFixed(1) }} L</strong>
            </div>
            <div class="report-metric">
              <span>Média leite /30d</span>
              <strong>{{ herdReport.averageMilkLast30Days.toFixed(1) }} L</strong>
            </div>
            <div class="report-metric">
              <span>Total alimentação /30d</span>
              <strong>{{ herdReport.feedingsLast30Days.toFixed(1) }} kg</strong>
            </div>
            <div class="report-metric">
              <span>Média alimentação /30d</span>
              <strong>{{ herdReport.averageFeedingsLast30Days.toFixed(1) }} kg</strong>
            </div>
          </div>
        </div>

      </main>
    </div>

    <div v-if="!selectedAnimalId && activeTab !== 'herd_report'" class="empty-selection-placeholder">
      <span class="placeholder-icon">📊</span>
      <h3>Nenhum animal selecionado</h3>
      <p>Escolha um brinco no seletor acima para cruzar os dados de peso, vacinas e leite.</p>
    </div>
    <div v-else-if="!selectedAnimalId && activeTab === 'herd_report'" class="empty-selection-placeholder">
      <span class="placeholder-icon">🐄</span>
      <h3>Relatório do Rebanho</h3>
      <p>Aqui está o resumo geral do rebanho inteiro. Selecione um brinco para ver o histórico individual também.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

const goHome = () => {
  const role = localStorage.getItem('user_role');
  if (role === 'op') router.push('/dashboard-op');
  else router.push('/dashboard-adm');
};
import api from '@/services/api'

const animalsList = ref([])
const selectedAnimalId = ref('')
const selectedAnimal = ref(null)
const activeTab = ref('weight_individual')
const loadingHistory = ref(false)

// Históricos individuais do animal selecionado
const weightHistory = ref([])
const vaccineHistory = ref([])
const milkHistory = ref([])
const feedingHistory = ref([])
const weightSummary = ref({})
const milkSummary = ref({})
const herdReport = ref({
  totalAnimals: 0,
  averageWeight: 0,
  averageVaccinations: 0,
  milkLast30Days: 0,
  averageMilkLast30Days: 0,
  feedingsLast30Days: 0,
  averageFeedingsLast30Days: 0
})
const groupStats = ref({
  groupName: 'Grupo',
  groupSize: 0,
  groupAvgWeight: 0,
  groupAverageVaccines: 0,
  groupAverageMilk30: 0,
  weightDeltaPercent: 0,
  milkDeltaPercent: 0,
  vaccineDelta: 0,
  selectedVaccinesCount: 0,
  selectedMilkLastMonth: 0,
  selectedWeightAvg: 0
})

const tabs = ref([
  { id: 'weight_individual', label: 'Evolução de Peso', icon: '⚖️' },
  { id: 'vaccination_individual', label: 'Histórico Sanitário', icon: '💉' },
  { id: 'milk_production', label: 'Produção de Leite', icon: '🥛' },
  { id: 'feeding_history', label: 'Alimentação', icon: '🍽️' },
  { id: 'herd_report', label: 'Relatório do Rebanho', icon: '🐄' }
])

onMounted(() => {
  loadAnimals()
})

const loadAnimals = async () => {
  try {
    const response = await api.get('animals/')
    animalsList.value = response.data.results || response.data
    await loadHerdReport()
  } catch (error) {
    console.error("Erro ao puxar lista de brincos:", error)
  }
}

const loadHerdReport = async () => {
  if (!animalsList.value.length) {
    herdReport.value = {
      totalAnimals: 0,
      averageWeight: 0,
      averageVaccinations: 0,
      milkLast30Days: 0,
      averageMilkLast30Days: 0,
      feedingsLast30Days: 0,
      averageFeedingsLast30Days: 0
    }
    return
  }

  try {
    const [weightsRes, vaccinesRes, milkRes, feedingsRes] = await Promise.all([
      api.get('weight_history/'),
      api.get('vaccinations/'),
      api.get('milk_production_history/'),
      api.get('feedings/')
    ])

    const animalsIds = animalsList.value.map(animal => getAnimalId(animal)).filter(id => id)
    const allWeights = weightsRes.data.results || weightsRes.data || []
    const allVaccines = vaccinesRes.data.results || vaccinesRes.data || []
    const allMilk = milkRes.data.results || milkRes.data || []
    const allFeedings = feedingsRes.data.results || feedingsRes.data || []

    const totalWeight = animalsList.value.reduce((sum, animal) => sum + normalizeNumber(animal.weight), 0)
    const totalAnimals = animalsList.value.length
    const averageWeight = totalAnimals ? totalWeight / totalAnimals : 0

    const validVaccines = allVaccines.filter(item => animalsIds.includes(getAnimalId(item)))
    const averageVaccinations = totalAnimals ? validVaccines.length / totalAnimals : 0

    const milkLast30 = allMilk.reduce((sum, item) => {
      const animalId = getAnimalId(item)
      if (!animalsIds.includes(animalId)) return sum
      const amount = normalizeNumber(item.milk_production || item.milk_quantity || item.quantity)
      return isWithinDays(item.production_date || item.date || item.created_at, 30) ? sum + amount : sum
    }, 0)

    const feedingsLast30 = allFeedings.reduce((sum, item) => {
      const animalId = getAnimalId(item)
      if (!animalsIds.includes(animalId)) return sum
      const amount = normalizeNumber(item.quantity)
      return isWithinDays(item.date_fed || item.created_at, 30) ? sum + amount : sum
    }, 0)

    herdReport.value = {
      totalAnimals,
      averageWeight,
      averageVaccinations,
      milkLast30Days: milkLast30,
      averageMilkLast30Days: totalAnimals ? milkLast30 / totalAnimals : 0,
      feedingsLast30Days: feedingsLast30,
      averageFeedingsLast30Days: totalAnimals ? feedingsLast30 / totalAnimals : 0
    }
  } catch (error) {
    console.error('Erro ao carregar relatório do rebanho:', error)
  }
}

const getAnimalId = (animal) => {
  if (!animal) return null
  if (animal.animal_id) return Number(animal.animal_id)
  if (animal.animal && animal.animal.id) return Number(animal.animal.id)
  return Number(animal.id || animal.pk || animal.register_number)
}

const getQuadrantId = (animal) => {
  if (!animal) return null
  if (animal.quadrant_id) return Number(animal.quadrant_id)
  if (animal.quadrant && typeof animal.quadrant === 'object') return Number(animal.quadrant.id || animal.quadrant)
  if (animal.quadrant) return Number(animal.quadrant)
  return null
}

const normalizeNumber = (value) => {
  const normalized = Number(value)
  return Number.isFinite(normalized) ? normalized : 0
}

const isWithinDays = (dateStr, days) => {
  if (!dateStr) return false
  const date = new Date(dateStr)
  if (Number.isNaN(date.getTime())) return false

  const diff = new Date() - date
  return diff >= 0 && diff <= days * 24 * 60 * 60 * 1000
}

const buildGroupStats = (selected, rawWeights, rawVaccines, rawMilk) => {
  const quadrantId = getQuadrantId(selected)
  const groupAnimals = animalsList.value.filter(animal => getQuadrantId(animal) === quadrantId)
  const groupSize = groupAnimals.length

  const groupTotalWeight = groupAnimals.reduce((sum, animal) => sum + normalizeNumber(animal.weight), 0)
  const groupAvgWeight = groupSize ? groupTotalWeight / groupSize : 0

  const groupAnimalIds = groupAnimals.map(getAnimalId)
  const groupVaccines = rawVaccines.filter(item => groupAnimalIds.includes(getAnimalId(item)))
  const groupAverageVaccines = groupSize ? groupVaccines.length / groupSize : 0

  const groupMilk30 = rawMilk.reduce((sum, item) => {
    if (!groupAnimalIds.includes(getAnimalId(item))) return sum
    const amount = normalizeNumber(item.milk_production || item.milk_quantity || item.quantity)
    if (isWithinDays(item.production_date || item.date || item.created_at, 30)) {
      return sum + amount
    }
    return sum
  }, 0)
  const groupAverageMilk30 = groupSize ? groupMilk30 / groupSize : 0

  const selectedWeight = normalizeNumber(selected.weight)
  const selectedWeightAvg = normalizeNumber(weightSummary.value?.peso_medio)
  const selectedVaccinesCount = vaccineHistory.value.length
  const selectedMilkLastMonth = normalizeNumber(milkSummary.value?.total_mes)

  const weightDeltaPercent = groupAvgWeight ? Number(((selectedWeight - groupAvgWeight) / groupAvgWeight * 100).toFixed(1)) : 0
  const milkDeltaPercent = groupAverageMilk30 ? Number(((selectedMilkLastMonth - groupAverageMilk30) / groupAverageMilk30 * 100).toFixed(1)) : 0
  const vaccineDelta = Number((selectedVaccinesCount - groupAverageVaccines).toFixed(1))

  return {
    groupName: selected.quadrant_name || (quadrantId ? `Quadrante ${quadrantId}` : 'Grupo'),
    groupSize,
    groupAvgWeight,
    groupAverageVaccines,
    groupAverageMilk30,
    weightDeltaPercent,
    milkDeltaPercent,
    vaccineDelta,
    selectedVaccinesCount,
    selectedMilkLastMonth,
    selectedWeightAvg
  }
}

const handleAnimalChange = async () => {
  if (!selectedAnimalId.value) return
  loadingHistory.value = true
  activeTab.value = 'weight_individual'

  try {
    const [animalRes, weightsRes, vaccinesRes, milkRes, feedingsRes, allWeightsRes, allVaccinesRes, allMilkRes] = await Promise.all([
      api.get(`animals/${selectedAnimalId.value}/`),
      api.get(`weight_history/animal/${selectedAnimalId.value}/`),
      api.getVaccinationsByAnimal(selectedAnimalId.value),
      api.get(`milk_production_history/animal/${selectedAnimalId.value}/`),
      api.get(`feedings/?animal_id=${selectedAnimalId.value}`),
      api.get('weight_history/'),
      api.get('vaccinations/'),
      api.get('milk_production_history/')
    ])

    selectedAnimal.value = animalRes.data

    const weightData = weightsRes.data
    weightHistory.value = weightData.historico || weightData.results || []
    weightSummary.value = weightData.resumo || {}

    vaccineHistory.value = vaccinesRes.data || []

    const feedingData = feedingsRes.data
    feedingHistory.value = feedingData.results || feedingData || []

    const milkData = milkRes.data
    milkHistory.value = milkData.historico || milkData.results || []
    milkSummary.value = milkData.resumo || {}

    const rawWeights = allWeightsRes.data.results || allWeightsRes.data
    const rawVaccines = allVaccinesRes.data.results || allVaccinesRes.data
    const rawMilk = allMilkRes.data.results || allMilkRes.data

    groupStats.value = buildGroupStats(selectedAnimal.value, rawWeights, rawVaccines, rawMilk)
  } catch (error) {
    console.error("Erro ao buscar histórico do animal selecionado:", error)
  } finally {
    loadingHistory.value = false
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleDateString('pt-BR', { timeZone: 'UTC' })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.reports-wrapper { padding: 40px; background-color: #f8fafc; min-height: 100vh; font-family: 'Inter', sans-serif; color: #0f172a; }
.page-header { margin-bottom: 32px; border-bottom: 1px solid #e2e8f0; padding-bottom: 24px; }
.btn-back { background: transparent; border: 1px solid #e2e8f0; color: #64748b; padding: 8px 16px; border-radius: 8px; cursor: pointer; margin-bottom: 16px; font-weight: 500; transition: 0.2s; }
.btn-back:hover { background: #f1f5f9; color: #0f172a; }
.page-header h1 { margin: 0 0 8px 0; font-size: 2rem; font-weight: 700; }
.page-header p { margin: 0; color: #64748b; }

/* CARD SELETOR */
.animal-selector-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 32px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.95rem; font-weight: 600; color: #475569; }
.select-animal { padding: 12px 16px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 1rem; outline: none; background: #ffffff; color: #0f172a; font-family: inherit; }
.select-animal:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22,163,74,0.1); }

/* ABAS DE NAVEGAÇÃO */
.tabs-nav { display: flex; gap: 12px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; margin-bottom: 24px; }
.tab-button { background: #ffffff; border: 1px solid #e2e8f0; color: #64748b; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600; transition: 0.2s; font-family: inherit; }
.tab-button:hover { border-color: #cbd5e1; color: #0f172a; }
.tab-button.active { background: #16a34a; border-color: #15803d; color: white; }

/* CARTÕES DE RELATÓRIO */
.glass-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
.card-header-inline { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #f1f5f9; padding-bottom: 16px; }
.card-header-inline h2 { font-size: 1.25rem; font-weight: 700; margin: 0; }
.badge { background: #f1f5f9; color: #475569; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }

/* TABELAS */
.table-responsive { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th { background: #f8fafc; padding: 16px; font-size: 0.8rem; text-transform: uppercase; color: #64748b; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 16px; border-bottom: 1px solid #e2e8f0; font-size: 0.95rem; color: #334155; }
.data-table tr:last-child td { border-bottom: none; }
.text-right { text-align: right; }
.text-center { text-align: center; }
.text-muted { color: #94a3b8; font-style: italic; padding: 24px !important; }
.font-bold { font-weight: 600; }

/* CORES DE TEXTO */
.text-green { color: #16a34a; }
.text-blue { color: #1d4ed8; }
.text-purple { color: #7c3aed; }
.text-orange { color: #ea580c; }
.badge-status-clean { background: #f0fdf4; color: #166534; padding: 4px 8px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; }

.report-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; margin-top: 12px; }
.report-metric { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 8px; }
.report-metric span { font-size: 0.9rem; color: #475569; }
.report-metric strong { font-size: 1.25rem; color: #0f172a; }

.summary-cards-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; margin-bottom: 32px; }
.ficha-grid, .comparison-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
.ficha-item, .comparison-item { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; display: flex; flex-direction: column; gap: 6px; }
.ficha-item span, .comparison-item span { color: #64748b; font-size: 0.85rem; }
.ficha-item strong, .comparison-item strong { font-size: 1rem; color: #0f172a; }
.highlight-item { background: #eff6ff; border-color: #bfdbfe; }

/* PLACEHOLDERS */
.empty-selection-placeholder { text-align: center; padding: 80px 40px; color: #64748b; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }
.placeholder-icon { font-size: 3rem; display: block; margin-bottom: 16px; }
.empty-selection-placeholder h3 { color: #0f172a; margin-bottom: 8px; }

.loading-history { text-align: center; padding: 60px; color: #64748b; }
.spinner { width: 36px; height: 36px; border: 4px solid #e2e8f0; border-top-color: #16a34a; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 16px; }
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>