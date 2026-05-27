<template>
  <div class="reports-wrapper">
    <header class="page-header">
      <div class="header-content">
        <button @click="$router.push('/dashboard-adm')" class="btn-back">← Voltar ao Dashboard</button>
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

    <div v-if="selectedAnimalId" class="reports-container">
      
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

      <div v-if="loadingHistory" class="loading-history">
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

      </main>
    </div>

    <div v-else class="empty-selection-placeholder">
      <span class="placeholder-icon">📊</span>
      <h3>Nenhum animal selecionado</h3>
      <p>Escolha um brinco no seletor acima para cruzar os dados de peso, vacinas e leite.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const animalsList = ref([])
const selectedAnimalId = ref('')
const activeTab = ref('weight_individual')
const loadingHistory = ref(false)

// Históricos individuais do animal selecionado
const weightHistory = ref([])
const vaccineHistory = ref([])
const milkHistory = ref([])

const tabs = ref([
  { id: 'weight_individual', label: 'Evolução de Peso', icon: '⚖️' },
  { id: 'vaccination_individual', label: 'Histórico Sanitário', icon: '💉' },
  { id: 'milk_production', label: 'Produção de Leite', icon: '🥛' }
])

onMounted(() => {
  loadAnimals()
})

const loadAnimals = async () => {
  try {
    const response = await api.get('animals/')
    animalsList.value = response.data.results || response.data
  } catch (error) {
    console.error("Erro ao puxar lista de brincos:", error)
  }
}

const handleAnimalChange = async () => {
  if (!selectedAnimalId.value) return
  loadingHistory.value = true

  try {
    // Faz chamadas gerais para buscar as tabelas completas do banco
    const [weightsRes, vaccinesRes, milkRes] = await Promise.all([
      api.get('weights/'),
      api.get('vaccinations/'),
      api.get('milk-productions/')
    ])

    const rawWeights = weightsRes.data.results || weightsRes.data
    const rawVaccines = vaccinesRes.data.results || vaccinesRes.data
    const rawMilk = milkRes.data.results || milkRes.data

    // FUNÇÃO AUXILIAR DE COMPARAÇÃO BLINDADA
    // Testa se o campo animal é o próprio ID numérico OU se é um objeto contendo o ID dentro
    const checkMatch = (itemAnimalField, selectedId) => {
      if (!itemAnimalField) return false
      if (typeof itemAnimalField === 'object') {
        return String(itemAnimalField.id) === String(selectedId)
      }
      return String(itemAnimalField) === String(selectedId)
    }

    // Filtra localmente de forma precisa e flexível conforme o retorno do Django
    weightHistory.value = rawWeights.filter(item => checkMatch(item.animal, selectedAnimalId.value))
    vaccineHistory.value = rawVaccines.filter(item => checkMatch(item.animal, selectedAnimalId.value))
    milkHistory.value = rawMilk.filter(item => checkMatch(item.animal, selectedAnimalId.value))

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
.badge-status-clean { background: #f0fdf4; color: #166534; padding: 4px 8px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; }

/* PLACEHOLDERS */
.empty-selection-placeholder { text-align: center; padding: 80px 40px; color: #64748b; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }
.placeholder-icon { font-size: 3rem; display: block; margin-bottom: 16px; }
.empty-selection-placeholder h3 { color: #0f172a; margin-bottom: 8px; }

.loading-history { text-align: center; padding: 60px; color: #64748b; }
.spinner { width: 36px; height: 36px; border: 4px solid #e2e8f0; border-top-color: #16a34a; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 16px; }
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>