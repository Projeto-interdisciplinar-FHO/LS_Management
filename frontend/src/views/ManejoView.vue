<template>
  <div class="manejo-wrapper">
    <header class="page-header">
      <button @click="$router.push('/dashboardop')" class="btn-back">← Voltar</button>
      <h1>Registro de Manejo</h1>
      <p>Lance os dados coletados diretamente no campo</p>
    </header>

    <div class="manejo-grid">
      <section class="action-card">
        <div class="card-icon weight-icon">⊡</div>
        <h2>Registrar Pesagem</h2>
        <p class="description">Informe o brinco do animal e o peso atual medido na balança.</p>
        
        <form @submit.prevent="handleWeight" class="manejo-form">
          <div class="form-group">
            <label>ID do Animal (Brinco)</label>
            <input v-model="weightData.animal" type="number" placeholder="Ex: 142" required>
          </div>
          <div class="form-group">
            <label>Peso (kg)</label>
            <input v-model="weightData.weight" type="number" step="0.01" placeholder="000.00" required>
          </div>
          <button type="submit" class="btn-submit weight-btn" :disabled="loading">
            {{ loading ? 'Salvando...' : 'Confirmar Peso' }}
          </button>
        </form>
      </section>

      <section class="action-card">
        <div class="card-icon vaccine-icon">✛</div>
        <h2>Registrar Vacinação</h2>
        <p class="description">Informe a vacina aplicada e o brinco do animal imunizado.</p>
        
        <form @submit.prevent="handleVaccine" class="manejo-form">
          <div class="form-group">
            <label>ID do Animal (Brinco)</label>
            <input v-model="vaccineData.animal" type="number" placeholder="Ex: 142" required>
          </div>
          <div class="form-group">
            <label>Vacina Aplicada</label>
            <select v-model="vaccineData.vaccine_id" required>
              <option value="" disabled>Selecione uma vacina...</option>
              <option v-for="vaccine in vaccinesList" :key="vaccine.id" :value="vaccine.id">
                {{ vaccine.name }}
              </option>
            </select>
          </div>
          <button type="submit" class="btn-submit vaccine-btn" :disabled="loading">
            {{ loading ? 'Salvando...' : 'Confirmar Vacina' }}
          </button>
        </form>
      </section>

      <section class="action-card batch-card">
        <div class="card-icon batch-icon">🌾</div>
        <h2>Movimentação de Lote</h2>
        <p class="description">Mova todos os animais de um quadrante para outro de forma coletiva.</p>
        
        <form @submit.prevent="handleBatchMove" class="manejo-form">
          <div class="form-group">
            <label>Quadrante Origem</label>
            <select v-model="batchData.origin_quadrant" required>
              <option value="" disabled>Selecione a origem...</option>
              <option v-for="quad in quadrants" :key="quad.id" :value="quad.id">
                {{ quad.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Quadrante Destino</label>
            <select v-model="batchData.target_quadrant" required>
              <option value="" disabled>Selecione o destino...</option>
              <option v-for="quad in quadrants" :key="quad.id" :value="quad.id">
                {{ quad.name }}
              </option>
            </select>
          </div>
          <button type="submit" class="btn-submit batch-btn" :disabled="loading">
            {{ loading ? 'Salvando...' : 'Mover Lote' }}
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(false)
const vaccinesList = ref([])
const quadrants = ref([])

const weightData = ref({ animal: '', weight: '' })
const vaccineData = ref({ animal: '', vaccine_id: '' })
const batchData = ref({ origin_quadrant: '', target_quadrant: '' })

const handleWeight = async () => {
  loading.value = true
  try {
    await axios.post('/api/weights/', weightData.value)
    alert('Peso registrado com sucesso!')
    weightData.value = { animal: '', weight: '' }
  } catch (err) {
    alert('Erro ao salvar pesagem.')
  } finally { 
    loading.value = false 
  }
}

const handleVaccine = async () => {
  loading.value = true
  try {
    await axios.post('/api/vaccinations/', vaccineData.value)
    alert('Vacinação registrada com sucesso!')
    vaccineData.value = { animal: '', vaccine_id: '' }
  } catch (err) {
    alert('Erro ao salvar vacinação.')
  } finally { 
    loading.value = false 
  }
}

const handleBatchMove = async () => {
  loading.value = true
  try {
    await axios.post('/api/quadrants/move-batch/', batchData.value)
    alert('Lote movimentado com sucesso!')
    batchData.value = { origin_quadrant: '', target_quadrant: '' }
  } catch (err) {
    alert('Erro ao mover lote.')
  } finally { 
    loading.value = false 
  }
}

onMounted(async () => {
  try {
    const [vRes, qRes] = await Promise.all([
      axios.get('/api/vaccines/'),
      axios.get('/api/quadrants/')
    ])
    vaccinesList.value = vRes.data
    quadrants.value = qRes.data
  } catch (err) {
    console.error('Erro ao carregar dados iniciais.')
  }
})
</script>

<style scoped>
.manejo-wrapper { padding: 40px; background: #0d1117; min-height: 100vh; color: white; }
.page-header { display: flex; align-items: center; gap: 20px; margin-bottom: 40px; }
.btn-back { background: transparent; border: 1px solid #30363d; color: #8b949e; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: 600; }
.btn-back:hover { border-color: #8b949e; color: white; }
.page-header h1 { margin: 0; font-size: 2.2rem; }
.manejo-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
.action-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 30px; display: flex; flex-direction: column; }
.card-icon { font-size: 2rem; margin-bottom: 15px; }
.weight-icon { color: #58a6ff; }
.vaccine-icon { color: #f85149; }
.batch-icon { color: #58a6ff; }
.action-card h2 { margin: 0 0 10px 0; font-size: 1.4rem; }
.description { color: #8b949e; font-size: 0.95rem; line-height: 1.5; margin: 0 0 25px 0; flex-grow: 1; }
.manejo-form { display: flex; flex-direction: column; gap: 20px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { font-size: 0.85rem; color: #8b949e; font-weight: 600; }
input, select { background: #0d1117; border: 1px solid #30363d; color: white; padding: 12px; border-radius: 8px; outline: none; }
input:focus, select:focus { border-color: #58a6ff; }
.btn-submit { color: white; border: none; padding: 14px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; }
.weight-btn { background: #238636; }
.weight-btn:hover { background: #2ea043; }
.vaccine-btn { background: #f85149; }
.vaccine-btn:hover { background: #da3633; }
.batch-btn { background: #238636; }
.batch-btn:hover { background: #2ea043; }
</style>