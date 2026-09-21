<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Relatórios"
        descricao="Consolidação por animal ou do rebanho inteiro."
        voltar-rotulo="Painel"
        voltar-para="/dashboard-adm"
      />

      <div class="toolbar">
        <div class="field seletor">
          <label class="field__label" for="escopo">Escopo do relatório</label>
          <select id="escopo" v-model="selectedAnimalId" class="select" @change="handleSelectionChange">
            <option value="" disabled>Selecione um escopo...</option>
            <option value="all">Rebanho inteiro — todos os animais</option>
            <option v-for="animal in animalsList" :key="animal.id" :value="animal.id">
              #{{ animal.register_number }} — {{ animal.name || 'Sem nome' }}
            </option>
          </select>
        </div>
      </div>

      <div v-if="!selectedAnimalId" class="card">
        <div class="empty">
          <AppIcon name="chart" :size="30" />
          <p class="empty__title">Nenhum escopo selecionado</p>
          <p class="empty__desc">
            Escolha o rebanho inteiro ou um brinco específico para carregar os números.
          </p>
        </div>
      </div>

      <div v-else class="stack-24">
        <section class="grid grid--3" aria-label="Indicadores do escopo">
          <article class="stat">
            <span class="stat__label"><AppIcon name="scale" :size="15" /> {{ ehRebanho ? 'Peso médio' : 'Último peso' }}</span>
            <strong class="stat__value">{{ weightLabel }}<span class="stat__unit">kg</span></strong>
            <span class="stat__foot">{{ ehRebanho ? `Média de ${animalsList.length} animais` : `${weightHistory.length} pesagens registradas` }}</span>
          </article>

          <article class="stat">
            <span class="stat__label"><AppIcon name="syringe" :size="15" /> Vacinações</span>
            <strong class="stat__value">{{ vaccineCount }}<span class="stat__unit">aplicações</span></strong>
            <span class="stat__foot">Registros sanitários no escopo</span>
          </article>

          <article class="stat">
            <span class="stat__label"><AppIcon name="milk" :size="15" /> Ordenhas</span>
            <strong class="stat__value">{{ milkCount }}<span class="stat__unit">coletas</span></strong>
            <span class="stat__foot">
              <template v-if="totalLitros > 0">{{ totalLitros.toFixed(1) }} litros no total</template>
              <template v-else>Sem volume registrado</template>
            </span>
          </article>
        </section>

        <!--
          Os três gráficos de pizza que existiam aqui eram decoração: as fatias
          vinham de percentuais fabricados ("Ganho acima da média" x
          "Estabilidade crítica") que não correspondiam a nada gravado. Foram
          substituídos pelas séries que o backend realmente devolve.
        -->
        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Evolução de peso</h2>
              <p class="card__desc">{{ ehRebanho ? 'Selecione um animal para ver a curva individual.' : 'Pesagens na ordem em que foram lançadas.' }}</p>
            </div>
            <span v-if="serieDePeso.length" class="badge">{{ serieDePeso.length }} pontos</span>
          </header>

          <div v-if="serieDePeso.length < 2" class="empty">
            <AppIcon name="chart" :size="28" />
            <p class="empty__desc">
              {{ ehRebanho
                ? 'A curva de peso é exibida por animal. Escolha um brinco no seletor acima.'
                : 'São necessárias ao menos duas pesagens para desenhar a evolução.' }}
            </p>
          </div>

          <div v-else class="card__body">
            <svg class="grafico" :viewBox="`0 0 ${LARGURA} ${ALTURA}`" role="img" :aria-label="descricaoGrafico">
              <!-- Grade horizontal, para o olho medir a altura sem contar pixel -->
              <line
                v-for="(linha, i) in linhasDeGrade"
                :key="`g${i}`"
                :x1="MARGEM.esq" :x2="LARGURA - MARGEM.dir"
                :y1="linha.y" :y2="linha.y"
                class="grafico__grade"
              />
              <text
                v-for="(linha, i) in linhasDeGrade"
                :key="`t${i}`"
                :x="MARGEM.esq - 8" :y="linha.y + 4"
                class="grafico__rotulo" text-anchor="end"
              >{{ linha.valor }}</text>

              <polyline class="grafico__linha" :points="pontosDaLinha" />
              <circle
                v-for="(p, i) in pontos"
                :key="`p${i}`"
                :cx="p.x" :cy="p.y" r="3"
                class="grafico__ponto"
              >
                <title>{{ p.rotuloData }}: {{ p.peso }} kg</title>
              </circle>
            </svg>

            <div class="grafico__eixo">
              <span class="mono">{{ pontos[0]?.rotuloData }}</span>
              <span class="mono">{{ pontos[pontos.length - 1]?.rotuloData }}</span>
            </div>
          </div>
        </section>

        <section class="card">
          <header class="card__head">
            <h2 class="card__title">Últimos registros sanitários</h2>
            <span class="badge">{{ vaccineHistory.length }}</span>
          </header>

          <div v-if="vaccineHistory.length === 0" class="empty">
            <AppIcon name="syringe" :size="28" />
            <p class="empty__desc">Nenhuma vacinação registrada neste escopo.</p>
          </div>

          <div v-else class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Vacina</th>
                  <th>Animal</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(registro, i) in vacinasRecentes" :key="registro.id || i">
                  <td class="mono nowrap">{{ formatarData(normalizeDate(registro)) }}</td>
                  <td class="cell-strong">{{ registro.vaccine_name || registro.name || '—' }}</td>
                  <td class="mono">{{ registro.animal_name || (registro.animal_id ? `#${registro.animal_id}` : '—') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import AppShell from '@/components/layout/AppShell.vue'
import AppIcon from '@/components/ui/AppIcon.vue'
import PageHeader from '@/components/layout/PageHeader.vue'

const selectedAnimalId = ref('')
const animalsList = ref([])
const weightLabel = ref('0.00')
const vaccineCount = ref('0')
const milkCount = ref('0')

const weightHistory = ref([])
const vaccineHistory = ref([])
const milkHistory = ref([])

const ehRebanho = computed(() => selectedAnimalId.value === 'all')

const normalizeDate = (record) => {
  const raw = record.vaccination_date || record.date || record.date_applied || record.created_at || record.updated_at || record.production_date || record.timestamp
  return raw ? new Date(raw) : null
}

const numericWeight = (record) => parseFloat(record.weight || record.value || record.animal_weight || 0) || 0

const dataDaPesagem = (registro) => {
  const bruto = registro.weighing_date || registro.date || registro.date_weighed || registro.created_at
  return bruto ? new Date(bruto) : null
}

const formatarData = (data) => (data ? data.toLocaleDateString('pt-BR') : '—')

const totalLitros = computed(() =>
  milkHistory.value.reduce(
    (soma, r) => soma + (parseFloat(r.milk_production || r.milk_quantity || r.quantity || 0) || 0),
    0
  )
)

const vacinasRecentes = computed(() =>
  [...vaccineHistory.value]
    .sort((a, b) => (normalizeDate(b)?.getTime() || 0) - (normalizeDate(a)?.getTime() || 0))
    .slice(0, 10)
)

/* ---------- Gráfico de evolução de peso ----------
   SVG desenhado à mão a partir das pesagens reais: sem biblioteca, sem
   número inventado. Cada ponto é um registro que existe no banco. */
const LARGURA = 720
const ALTURA = 220
const MARGEM = { topo: 16, dir: 12, base: 24, esq: 46 }

const serieDePeso = computed(() =>
  weightHistory.value
    .map((registro) => ({ data: dataDaPesagem(registro), peso: numericWeight(registro) }))
    .filter((p) => p.data && p.peso > 0)
    .sort((a, b) => a.data - b.data)
)

const escala = computed(() => {
  const pesos = serieDePeso.value.map((p) => p.peso)
  const min = Math.min(...pesos)
  const max = Math.max(...pesos)
  // Uma folga evita a linha colar no topo e no fundo da área do gráfico.
  const folga = (max - min) * 0.15 || Math.max(max * 0.05, 1)
  return { min: min - folga, max: max + folga }
})

const pontos = computed(() => {
  const serie = serieDePeso.value
  if (serie.length < 2) return []

  const { min, max } = escala.value
  const largura = LARGURA - MARGEM.esq - MARGEM.dir
  const altura = ALTURA - MARGEM.topo - MARGEM.base
  const amplitude = max - min || 1

  return serie.map((ponto, i) => ({
    x: MARGEM.esq + (i / (serie.length - 1)) * largura,
    y: MARGEM.topo + (1 - (ponto.peso - min) / amplitude) * altura,
    peso: ponto.peso.toFixed(1),
    rotuloData: ponto.data.toLocaleDateString('pt-BR'),
  }))
})

const pontosDaLinha = computed(() => pontos.value.map((p) => `${p.x},${p.y}`).join(' '))

const linhasDeGrade = computed(() => {
  if (pontos.value.length < 2) return []
  const { min, max } = escala.value
  const altura = ALTURA - MARGEM.topo - MARGEM.base
  return [0, 0.25, 0.5, 0.75, 1].map((fracao) => ({
    y: MARGEM.topo + fracao * altura,
    valor: Math.round(max - fracao * (max - min)),
  }))
})

const descricaoGrafico = computed(() => {
  const serie = serieDePeso.value
  if (serie.length < 2) return 'Sem dados suficientes para o gráfico.'
  const primeiro = serie[0]
  const ultimo = serie[serie.length - 1]
  const delta = (ultimo.peso - primeiro.peso).toFixed(1)
  return `Evolução de peso de ${primeiro.peso} kg para ${ultimo.peso} kg (${delta} kg) em ${serie.length} pesagens.`
})

onMounted(() => {
  loadDropdownData()
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
      weightHistory.value = []

      weightLabel.value = '0.00'
      vaccineCount.value = String(vaccineHistory.value.length)
      milkCount.value = String(milkHistory.value.length)
      return
    } catch (error) {
      console.error('Erro ao carregar resumo geral de relatórios:', error)
      weightLabel.value = '0.00'
      vaccineCount.value = '0'
      milkCount.value = '0'
      weightHistory.value = []
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
      const dateA = dataDaPesagem(a)
      const dateB = dataDaPesagem(b)
      return (dateB ? dateB.getTime() : 0) - (dateA ? dateA.getTime() : 0)
    })[0]

    const latestWeight = latestWeightRecord ? numericWeight(latestWeightRecord) : parseFloat(target?.weight || 0)
    weightLabel.value = latestWeight ? latestWeight.toFixed(2) : '0.00'

    vaccineCount.value = String(vaccineHistory.value.length)
    milkCount.value = String(milkHistory.value.length)
  } catch (error) {
    console.error("Erro ao carregar histórico real de relatórios:", error)
    vaccineCount.value = '0'
    milkCount.value = '0'
    weightHistory.value = []
  }
}
</script>

<style scoped>
.seletor { min-width: 340px; max-width: 460px; }

.grafico {
  width: 100%;
  height: auto;
  overflow: visible;
}

.grafico__grade {
  stroke: var(--line);
  stroke-width: 1;
}

.grafico__rotulo {
  fill: var(--text-3);
  font-family: var(--font-mono);
  font-size: 10px;
}

.grafico__linha {
  fill: none;
  stroke: var(--accent);
  stroke-width: 2;
  stroke-linejoin: round;
  stroke-linecap: round;
}

.grafico__ponto {
  fill: var(--surface);
  stroke: var(--accent);
  stroke-width: 2;
}

.grafico__eixo {
  display: flex;
  justify-content: space-between;
  margin-top: 6px;
  padding: 0 12px 0 46px;
  color: var(--text-3);
  font-size: var(--fs-xs);
}
</style>
