<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Manejo"
        descricao="Lançamentos rápidos feitos direto no curral."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <p v-if="mensagem" class="alert alert--ok" role="status">
        <AppIcon name="check-circle" :size="16" />
        <span>{{ mensagem }}</span>
      </p>
      <p v-if="erro" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ erro }}</span>
      </p>
      <p v-if="optionsError" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ optionsError }}</span>
      </p>

      <div class="grid grid--wide">
        <section class="card">
          <header class="card__head">
            <div class="list__main">
              <span class="icon-tile icon-tile--accent"><AppIcon name="scale" :size="17" /></span>
              <div>
                <h2 class="card__title">Pesagem</h2>
                <p class="card__desc">Brinco do animal e peso lido na balança.</p>
              </div>
            </div>
          </header>

          <form @submit.prevent="handleWeight">
            <div class="card__body stack">
              <div class="field">
                <label class="field__label" for="peso-animal">ID do animal (brinco)</label>
                <input id="peso-animal" v-model="weightData.animal" class="input" type="number" placeholder="142" required>
              </div>
              <div class="field">
                <label class="field__label" for="peso-valor">Peso (kg)</label>
                <input id="peso-valor" v-model="weightData.weight" class="input" type="number" step="0.01" placeholder="450.00" required>
              </div>
            </div>
            <footer class="card__foot">
              <button type="submit" class="btn btn--primary" :disabled="loading">
                {{ loading ? 'Salvando...' : 'Confirmar peso' }}
              </button>
            </footer>
          </form>
        </section>

        <section class="card">
          <header class="card__head">
            <div class="list__main">
              <span class="icon-tile icon-tile--info"><AppIcon name="syringe" :size="17" /></span>
              <div>
                <h2 class="card__title">Vacinação</h2>
                <p class="card__desc">Vacina aplicada e brinco do animal imunizado.</p>
              </div>
            </div>
          </header>

          <form @submit.prevent="handleVaccine">
            <div class="card__body stack">
              <div class="field">
                <label class="field__label" for="vac-animal">ID do animal (brinco)</label>
                <input id="vac-animal" v-model="vaccineData.animal" class="input" type="number" placeholder="142" required>
              </div>
              <div class="field">
                <label class="field__label" for="vac-vacina">Vacina aplicada</label>
                <select id="vac-vacina" v-model="vaccineData.vaccine_id" class="select" required :disabled="loadingOptions || !vaccinesList.length">
                  <option value="" disabled>{{ loadingOptions ? 'Carregando vacinas...' : 'Selecione uma vacina...' }}</option>
                  <option v-for="vaccine in vaccinesList" :key="vaccine.id" :value="vaccine.id">
                    {{ vaccine.name }}
                  </option>
                </select>
              </div>
            </div>
            <footer class="card__foot">
              <button type="submit" class="btn btn--primary" :disabled="loading || loadingOptions || !vaccinesList.length">
                {{ loading ? 'Salvando...' : loadingOptions ? 'Carregando opções...' : 'Confirmar vacina' }}
              </button>
            </footer>
          </form>
        </section>

        <section class="card">
          <header class="card__head">
            <div class="list__main">
              <span class="icon-tile icon-tile--warn"><AppIcon name="move" :size="17" /></span>
              <div>
                <h2 class="card__title">Movimentação de lote</h2>
                <p class="card__desc">Move todos os animais de um quadrante para outro.</p>
              </div>
            </div>
          </header>

          <form @submit.prevent="handleBatchMove">
            <div class="card__body stack">
              <div class="field">
                <label class="field__label" for="lote-origem">Quadrante de origem</label>
                <select id="lote-origem" v-model="batchData.origin_quadrant" class="select" required :disabled="loadingOptions || !quadrants.length">
                  <option value="" disabled>{{ loadingOptions ? 'Carregando quadrantes...' : 'Selecione a origem...' }}</option>
                  <option v-for="quad in quadrants" :key="quad.id" :value="quad.id">
                    {{ quad.name }}
                  </option>
                </select>
              </div>
              <div class="field">
                <label class="field__label" for="lote-destino">Quadrante de destino</label>
                <select id="lote-destino" v-model="batchData.target_quadrant" class="select" required :disabled="loadingOptions || !quadrants.length">
                  <option value="" disabled>{{ loadingOptions ? 'Carregando quadrantes...' : 'Selecione o destino...' }}</option>
                  <option v-for="quad in quadrants" :key="quad.id" :value="quad.id">
                    {{ quad.name }}
                  </option>
                </select>
              </div>
            </div>
            <footer class="card__foot">
              <button type="submit" class="btn btn--primary" :disabled="loading || loadingOptions || !quadrants.length || !movementTypes.length">
                {{ loading ? 'Salvando...' : loadingOptions ? 'Carregando opções...' : 'Mover lote' }}
              </button>
            </footer>
          </form>
        </section>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
/*
 * Esta tela chamava /api/weights/, /api/vaccinations/ e /api/quadrants/ com
 * `axios` cru. Nenhuma dessas rotas existe no backend (sao weight_history/,
 * vaccinations/ e quadrants/), e o axios cru nao passa pelo interceptor que
 * anexa o token — entao, mesmo com a rota certa, viria 401.
 *
 * Resultado: os tres botoes desta tela nunca funcionaram. O `catch` mostrava
 * "Erro ao salvar" e o motivo real morria no console.
 */
import { onMounted, computed, ref } from 'vue'
import api from '@/services/api'
import { painelDoPapel } from '@/services/auth'
import AppShell from '@/components/layout/AppShell.vue'
import AppIcon from '@/components/ui/AppIcon.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { apiErrorMessage } from '@/utils/apiError'

const painel = computed(() => painelDoPapel())

const loading = ref(false)
const loadingOptions = ref(true)
const vaccinesList = ref([])
const quadrants = ref([])
const movementTypes = ref([])
const mensagem = ref('')
const erro = ref('')
const optionsError = ref('')

const hoje = () => new Date().toISOString().slice(0, 10)

const weightData = ref({ animal: '', weight: '' })
const vaccineData = ref({ animal: '', vaccine_id: '', dosage: 1 })
const batchData = ref({ origin_quadrant: '', target_quadrant: '' })

function avisar(texto, ehErro = false) {
  mensagem.value = ehErro ? '' : texto
  erro.value = ehErro ? texto : ''
  setTimeout(() => { mensagem.value = ''; erro.value = '' }, 5000)
}

const handleWeight = async () => {
  loading.value = true
  try {
    await api.post('weight_history/', {
      animal: Number(weightData.value.animal),
      weight: weightData.value.weight,
      weighing_date: hoje(),
    })
    avisar('Peso registrado.')
    weightData.value = { animal: '', weight: '' }
  } catch (err) {
    avisar(apiErrorMessage(err, 'Não foi possível salvar a pesagem.'), true)
  } finally {
    loading.value = false
  }
}

const handleVaccine = async () => {
  loading.value = true
  try {
    await api.post('vaccinations/', {
      animal: Number(vaccineData.value.animal),
      vaccine: Number(vaccineData.value.vaccine_id),
      dosage: vaccineData.value.dosage || 1,
      vaccination_date: hoje(),
    })
    avisar('Vacinacao registrada.')
    vaccineData.value = { animal: '', vaccine_id: '', dosage: 1 }
  } catch (err) {
    avisar(apiErrorMessage(err, 'Não foi possível salvar a vacinação.'), true)
  } finally {
    loading.value = false
  }
}

// Nao existe endpoint de "mover lote" no backend. O que existe e
// animal_movements/, um registro por animal. Entao a tela busca os animais do
// quadrante de origem e grava uma movimentacao para cada um.
const handleBatchMove = async () => {
  const { origin_quadrant: origem, target_quadrant: destino } = batchData.value
  if (!origem || !destino) return avisar('Escolha origem e destino.', true)
  if (origem === destino) return avisar('Origem e destino sao o mesmo quadrante.', true)

  loading.value = true
  try {
    const { data: animais } = await api.get('animals/')
    const doQuadrante = animais.filter(
      (a) => String(a.quadrant?.id ?? a.quadrant) === String(origem)
    )
    if (!doQuadrante.length) {
      return avisar('Nenhum animal neste quadrante de origem.', true)
    }

    const tipo = movementTypes.value[0]?.id
    await Promise.all(doQuadrante.map((a) =>
      api.post('animal_movements/', {
        animal: a.id,
        quadrant: Number(destino),
        movement_date: hoje(),
        movement_reason: 'Movimentacao de lote pela tela de manejo',
        movement_type: tipo,
      })
    ))
    avisar(`${doQuadrante.length} animal(is) movimentado(s).`)
    batchData.value = { origin_quadrant: '', target_quadrant: '' }
  } catch (err) {
    avisar(apiErrorMessage(err, 'Não foi possível mover o lote.'), true)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  loadingOptions.value = true
  optionsError.value = ''
  try {
    const [v, q, t] = await Promise.all([
      api.get('vaccines/'),
      api.get('quadrants/'),
      api.get('movement_types/'),
    ])
    vaccinesList.value = v.data
    quadrants.value = q.data
    movementTypes.value = t.data
  } catch (err) {
    vaccinesList.value = []
    quadrants.value = []
    movementTypes.value = []
    optionsError.value = apiErrorMessage(err, 'Não foi possível carregar vacinas, quadrantes e tipos de movimentação.')
  } finally {
    loadingOptions.value = false
  }
})
</script>
