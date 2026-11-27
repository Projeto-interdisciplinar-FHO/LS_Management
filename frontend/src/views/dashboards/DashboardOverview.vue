<template>
  <AppShell>
    <div class="page page--wide dashboard">
      <header class="hero dashboard__hero">
        <div class="hero__bg" aria-hidden="true">
          <img :src="heroImage" alt="" class="hero__img">
          <div class="hero__shade"></div>
        </div>
        <div class="hero__content">
          <div>
            <p class="hero__eyebrow">{{ dataHoje }}</p>
            <h1 class="hero__title">{{ saudacao }}!</h1>
          </div>
          <div class="hero__actions">
            <details class="dashboard__filter-menu">
              <summary class="btn">
                <AppIcon name="filter" :size="15" />
                Filtros
              </summary>
              <div class="dashboard__filter-panel">
                <div class="field">
                  <label class="field__label" for="filtro-estabulo">Estábulo</label>
                  <select id="filtro-estabulo" v-model="quadranteSelecionado" class="select">
                    <option value="todos">Todos os estábulos</option>
                    <option v-for="quadrante in quadrantes" :key="quadrante.id" :value="String(quadrante.id)">
                      {{ quadrante.name || quadrante.tipo || `Estábulo ${quadrante.id}` }}
                    </option>
                  </select>
                </div>
                <div class="field">
                  <label class="field__label" for="filtro-periodo">Período dos gráficos</label>
                  <select id="filtro-periodo" v-model="periodoSelecionado" class="select">
                    <option value="30">Últimos 30 dias</option>
                    <option value="90">Últimos 90 dias</option>
                    <option value="365">Últimos 12 meses</option>
                    <option value="todos">Todo o histórico</option>
                  </select>
                </div>
              </div>
            </details>
          </div>
        </div>
      </header>

      <p v-if="erro" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ erro }}</span>
      </p>

      <div class="dashboard__content">
      <div class="dashboard__panel">
      <section class="card dashboard-today" aria-labelledby="dashboard-today-title">
        <header class="dashboard-today__head">
          <div>
            <h2 id="dashboard-today-title" class="dashboard-today__title">Hoje na fazenda</h2>
            <p class="dashboard-today__desc">O que precisa de atenção agora.</p>
          </div>
        </header>
        <div v-if="carregando" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando tarefas...</div>
        <ul v-else class="dashboard-today__list">
          <li v-for="tarefa in tarefasHoje" :key="tarefa.id">
            <RouterLink
              :to="tarefa.para"
              class="dashboard-today__item"
              :class="[`is-${tarefa.tom}`, { 'dashboard-today__item--active': tarefa.total > 0, 'dashboard-today__item--critical': tarefa.total > 0 && tarefa.critico }]"
            >
              <span class="dashboard-today__icon"><AppIcon :name="tarefa.icone" :size="20" /></span>
              <span class="dashboard-today__text">
                <strong>{{ tarefa.titulo }}</strong>
                <small>{{ tarefa.total > 0 ? tarefa.detalhe : tarefa.vazio }}</small>
              </span>
              <span class="dashboard-today__count">{{ tarefa.total }}</span>
            </RouterLink>
          </li>
        </ul>
      </section>

      </div>

      <div
        class="dashboard__panel"
      >
      <section class="dashboard__top-grid" aria-label="Indicadores gerais da fazenda">
        <RouterLink to="/veterinario" class="hero dashboard-vet-card">
          <div class="hero__bg" aria-hidden="true">
            <img :src="vetImage" alt="" class="hero__img">
            <div class="hero__shade"></div>
          </div>
          <div class="dashboard-vet-card__content">
            <div>
              <p class="hero__eyebrow">Saúde do rebanho</p>
              <h2 class="dashboard-vet-card__title">Veterinário</h2>
              <p class="dashboard-vet-card__desc">Registre atendimentos, consulte históricos e pesquise por animal ou veterinário.</p>
            </div>
            <span class="btn dashboard-vet-card__cta">
              <AppIcon name="stethoscope" :size="15" />
              Acessar veterinário
              <AppIcon name="arrow-right" :size="14" />
            </span>
          </div>
        </RouterLink>

        <article class="card dashboard-panel dashboard-panel--reproduction">
          <header class="dashboard-panel__head">
            <span class="dashboard-panel__icon dashboard-panel__icon--reproduction"><AppIcon name="barn" :size="18" /></span>
            <div>
              <h2>Estrutura da fazenda</h2>
              <p>Rebanho e instalações</p>
            </div>
          </header>
          <div v-if="carregando" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando estrutura da fazenda...</div>
          <div v-else class="farm-summary">
            <RouterLink :to="linkAnimais" class="farm-summary__item">
              <span>Animais no recorte</span>
              <strong>{{ animaisFiltrados.length }}</strong>
            </RouterLink>
            <RouterLink to="/estabulos" class="farm-summary__item">
              <span>Estábulos cadastrados</span>
              <strong>{{ quadrantes.length }}</strong>
            </RouterLink>
          </div>
        </article>

        <article class="card dashboard-panel dashboard-panel--milk">
          <header class="dashboard-panel__head">
            <span class="dashboard-panel__icon dashboard-panel__icon--milk"><AppIcon name="milk" :size="18" /></span>
            <div>
              <h2>Produção geral de leite</h2>
              <p>Últimos 30 dias</p>
            </div>
          </header>
          <div v-if="carregando" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando ordenhas...</div>
          <div v-else-if="erro" class="empty dashboard-panel__empty">
            <p class="empty__desc">Não foi possível carregar as ordenhas.</p>
          </div>
          <div v-else class="milk-summary">
            <div class="milk-summary__overview">
              <span class="milk-summary__label">Média geral por ordenha · 30 dias</span>
              <strong class="milk-summary__average">{{ formatarNumero(mediaPorOrdenha30d) }} <small>L</small></strong>
                            <div class="milk-summary__details">
                <span><strong>{{ formatarNumero(totalLeite30d) }} L</strong> nos últimos 30 dias</span>
                <span><strong>{{ ordenhasValidas30d.length }}</strong> ordenhas válidas</span>
              </div>
            </div>
            <section class="milk-month-alert" aria-labelledby="milk-month-alert-title">
              <div class="milk-month-alert__head">
                <span class="milk-month-alert__icon" :class="{ 'is-alert': animaisAbaixoDaMediaMesAtual.length }">
                  <AppIcon :name="animaisAbaixoDaMediaMesAtual.length ? 'alert' : 'check-circle'" :size="18" />
                </span>
                <div>
                  <h3 id="milk-month-alert-title">Alerta de produção · mês atual</h3>
                  <p>Média do rebanho neste mês: {{ formatarNumero(mediaPorOrdenhaMesAtual) }} L por ordenha</p>
                </div>
                <strong class="milk-month-alert__count" :class="{ 'is-alert': animaisAbaixoDaMediaMesAtual.length }">
                  {{ animaisAbaixoDaMediaMesAtual.length }}
                </strong>
                <RouterLink
                  v-if="animaisAbaixoDaMediaMesAtual.length > 3"
                  :to="linkAbaixoDaMedia"
                  class="btn btn--sm"
                >
                  Ver mais
                </RouterLink>
              </div>
              <p v-if="!animaisAbaixoDaMediaMesAtual.length" class="milk-month-alert__empty">
                {{ ordenhasValidasMesAtual.length ? 'Nenhum animal está abaixo da média neste mês.' : 'Sem registros de ordenha neste mês para comparar.' }}
              </p>
              <ul v-else class="milk-month-alert__list">
                <li v-for="item in animaisAbaixoDaMediaVisiveisMesAtual" :key="item.animal.id">
                  <RouterLink
                    :to="{ name: 'animal-detail', params: { id: item.animal.id } }"
                    class="milk-month-alert__animal"
                  >
                    <span class="milk-month-alert__animal-head">
                      <strong>{{ item.animal.name || 'Sem nome' }} · #{{ item.animal.register_number }}</strong>
                      <strong>{{ formatarNumero(item.media) }} L</strong>
                    </span>
                    <span
                      class="milk-month-alert__meter"
                      role="progressbar"
                      :aria-label="`Média de ${item.animal.name || 'animal'} neste mês em relação à média do rebanho`"
                      aria-valuemin="0"
                      aria-valuemax="100"
                      :aria-valuenow="percentualDaMediaMesAtual(item)"
                    >
                      <span :style="{ width: `${percentualDaMediaMesAtual(item)}%` }"></span>
                    </span>
                    <small>{{ formatarNumero(mediaPorOrdenhaMesAtual - item.media) }} L abaixo da média</small>
                  </RouterLink>
                </li>
              </ul>
            </section>
          </div>
        </article>
      </section>
      </div>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import api from '@/services/api';
import { ehAdministrador } from '@/services/auth';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import heroImage from '@/assets/images/background_fazenda.jpeg';
import vetImage from '@/assets/images/veterinario.jpg';
import { idRelacao, ultimaMovimentacaoPorAnimal } from '@/utils/animalMovementUtils';
import { metricasProducaoPorAnimal, ordenhasDoMesAtual, ordenhasNosUltimosDias } from '@/utils/milkProductionMetrics';
import {
  situacaoDaInseminacao,
  ultimaInseminacaoPorMatriz,
} from '@/utils/reproducaoUtils';

const carregando = ref(true);
const erro = ref('');
const animais = ref([]);
const quadrantes = ref([]);
const movimentacoes = ref([]);
const ordenhas = ref([]);
const inseminacoes = ref([]);
const vacinacoes = ref([]);
const quadranteSelecionado = ref('todos');
const periodoSelecionado = ref('todos');

const ehAdmin = computed(() => ehAdministrador());
const linkAnimais = computed(() => (ehAdmin.value ? '/animais' : '/rebanho'));
const linkAbaixoDaMedia = computed(() => ({
  name: 'animal-list',
  query: {
    alert: 'below-average',
    ...(quadranteSelecionado.value !== 'todos' ? { quadrant: quadranteSelecionado.value } : {}),
  },
}));
const ultimaMovimentacao = computed(() => ultimaMovimentacaoPorAnimal(movimentacoes.value));

function registrosDaResposta(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  if (Array.isArray(data?.historico)) return data.historico;
  throw new Error('A consulta retornou um formato de lista inesperado.');
}

async function consultarTodos(endpoint) {
  let url = endpoint;
  const registros = [];
  const paginasVisitadas = new Set();

  while (url) {
    if (paginasVisitadas.has(url)) {
      throw new Error(`A paginação de ${endpoint} retornou uma página repetida.`);
    }
    paginasVisitadas.add(url);

    const resposta = await api.get(url);
    const data = resposta.data;
    registros.push(...registrosDaResposta(data));
    url = Array.isArray(data) ? null : (data.next || null);
  }

  return registros;
}

const animaisFiltrados = computed(() => animais.value.filter((animal) => {
  if (quadranteSelecionado.value === 'todos') return true;
  const movement = ultimaMovimentacao.value.get(String(animal.id));
  return String(idRelacao(movement?.quadrant)) === quadranteSelecionado.value;
}));

const animaisPorId = computed(() => new Map(
animaisFiltrados.value.map((animal) => [String(animal.id), animal])
));

function dataAtualIso() {
  const hoje = new Date();
  const deslocamento = hoje.getTimezoneOffset() * 60000;
  return new Date(hoje.getTime() - deslocamento).toISOString().slice(0, 10);
}

const vacinasAtrasadas = computed(() => {
  const hoje = dataAtualIso();
  return vacinacoes.value
    .filter((vacina) => {
      const animalId = idRelacao(vacina.animal ?? vacina.animal_id);
      const dataProxima = String(vacina.next_vaccination_date || '').slice(0, 10);
      return animaisPorId.value.has(String(animalId))
        && (vacina.is_overdue === true || (vacina.is_overdue !== false && dataProxima && dataProxima < hoje));
    })
    .sort((a, b) => String(a.next_vaccination_date).localeCompare(String(b.next_vaccination_date)));
});

function dataDoRegistro(registro, campos) {
  for (const campo of campos) {
    if (!registro?.[campo]) continue;
    const valor = String(registro[campo]).slice(0, 10);
    const data = new Date(`${valor}T00:00:00`);
    if (!Number.isNaN(data.getTime())) return data;
  }
  return null;
}

const dataLimite = computed(() => {
  if (periodoSelecionado.value === 'todos') return null;
  const dias = Number(periodoSelecionado.value);
  const limite = new Date();
  limite.setHours(0, 0, 0, 0);
  limite.setDate(limite.getDate() - dias);
  return limite;
});

function dentroDoPeriodo(data) {
  return data && (!dataLimite.value || data >= dataLimite.value);
}

const inseminacoesFiltradas = computed(() => inseminacoes.value.filter((registro) => {
  const animalId = idRelacao(registro.mother ?? registro.mother_id);
  return animaisPorId.value.has(String(animalId))
    && dentroDoPeriodo(dataDoRegistro(registro, ['date']));
}));

function quantidadeDeLeite(registro) {
  const quantidade = Number(registro.milk_production ?? registro.milk_quantity ?? registro.quantity);
  return Number.isFinite(quantidade) && quantidade > 0 ? quantidade : 0;
}

const ordenhasUltimos30Dias = computed(() => ordenhasNosUltimosDias(ordenhas.value, 30).filter((registro) => {
  const animalId = idRelacao(registro.animal ?? registro.animal_id);
  return animaisPorId.value.has(String(animalId));
}));

const ordenhasValidas30d = computed(() =>
  ordenhasUltimos30Dias.value.filter((registro) => quantidadeDeLeite(registro) > 0)
);

const ordenhasMesAtual = computed(() => ordenhasDoMesAtual(ordenhas.value).filter((registro) => {
  const animalId = idRelacao(registro.animal ?? registro.animal_id);
  return animaisPorId.value.has(String(animalId));
}));
const ordenhasValidasMesAtual = computed(() =>
  ordenhasMesAtual.value.filter((registro) => quantidadeDeLeite(registro) > 0)
);

const metricasProducao30d = computed(() =>
  metricasProducaoPorAnimal([...animaisPorId.value.values()], ordenhasValidas30d.value)
);
const totalLeite30d = computed(() => metricasProducao30d.value.totalLitros);
const mediaPorOrdenha30d = computed(() => metricasProducao30d.value.mediaRebanho);
const metricasProducaoMesAtual = computed(() =>
  metricasProducaoPorAnimal([...animaisPorId.value.values()], ordenhasValidasMesAtual.value)
);
const mediaPorOrdenhaMesAtual = computed(() => metricasProducaoMesAtual.value.mediaRebanho);
const animaisAbaixoDaMediaMesAtual = computed(() => metricasProducaoMesAtual.value.abaixoDaMedia);
const animaisAbaixoDaMediaVisiveisMesAtual = computed(() => animaisAbaixoDaMediaMesAtual.value.slice(0, 3));

function percentualDaMediaMesAtual(item) {
  if (!mediaPorOrdenhaMesAtual.value) return 0;
  return Math.max(0, Math.min(100, Math.round((item.media / mediaPorOrdenhaMesAtual.value) * 100)));
}

function formatarNumero(valor) {
  return valor.toLocaleString('pt-BR', { maximumFractionDigits: 1 });
}

const reproducaoPorMatriz = computed(() => {
  const ultimas = ultimaInseminacaoPorMatriz(inseminacoes.value, idRelacao);
  const itens = [];
  for (const registro of ultimas.values()) {
    const animalId = idRelacao(registro.mother ?? registro.mother_id);
    const animal = animaisPorId.value.get(String(animalId));
    const info = situacaoDaInseminacao(registro.date);
    if (animal && info) itens.push({ registro, animal, info });
  }
  return itens;
});

const ultrassonsPendentes = computed(() =>
  reproducaoPorMatriz.value
    .filter((item) => item.info.fase === 'ultrassom')
    .sort((a, b) => b.info.dias - a.info.dias)
);

const diagnosticosAtrasados = computed(() =>
  reproducaoPorMatriz.value
    .filter((item) => item.info.fase === 'diagnostico-atrasado')
    .sort((a, b) => b.info.dias - a.info.dias)
);

const matrizesAptas = computed(() =>
  animaisFiltrados.value.filter((animal) => Boolean(animal.reproductive_status))
);

const tarefasHoje = computed(() => [
  {
    id: 'reproducao-ia',
    icone: 'sparkle',
    tom: 'info',
    titulo: 'Reprodução e IA',
    total: matrizesAptas.value.length,
    critico: false,
    detalhe: 'Matrizes aptas para validação genética de cruzamento com IA.',
    vazio: 'Nenhuma matriz apta para análise reprodutiva.',
    para: '/analise-reprodutiva',
  },
  {
    id: 'diagnosticos',
    icone: 'clipboard',
    tom: 'warn',
    titulo: 'Diagnósticos de prenhez pendentes',
    total: diagnosticosAtrasados.value.length,
    critico: false,
    detalhe: 'Inseminações há mais de 90 dias sem confirmação clínica.',
    vazio: 'Nenhum diagnóstico atrasado.',
    para: { path: '/inseminacoes', query: { aba: 'diagnostico' } },
  },
  {
    id: 'vacinas',
    icone: 'syringe',
    tom: 'danger',
    titulo: 'Reforços de vacina vencidos',
    total: vacinasAtrasadas.value.length,
    critico: true,
    detalhe: 'Animais com a próxima dose já vencida.',
    vazio: 'Vacinação em dia.',
    para: '/saude',
  },
  {
    id: 'producao',
    icone: 'milk',
    tom: 'warn',
    titulo: 'Produção abaixo da média neste mês',
    total: animaisAbaixoDaMediaMesAtual.value.length,
    critico: false,
    detalhe: 'Animais com média abaixo da média do rebanho neste mês.',
    vazio: 'Nenhum animal abaixo da média neste mês.',
    para: '/lancamento-leite',
  },
]);

const saudacao = computed(() => {
  const hora = new Date().getHours();
  if (hora < 12) return 'Bom dia';
  if (hora < 18) return 'Boa tarde';
  return 'Boa noite';
});

const dataHoje = computed(() => new Date().toLocaleDateString('pt-BR', {
  weekday: 'long', day: 'numeric', month: 'long',
}));

onMounted(async () => {
  quadranteSelecionado.value = 'todos';
  try {
    const [animaisRes, quadrantesRes, movimentacoesRes, ordenhasRes, inseminacoesRes, vacinacoesRes] = await Promise.all([
      consultarTodos('animals/'),
      consultarTodos('quadrants/'),
      consultarTodos('animal_movements/'),
      consultarTodos('milk_production_history/'),
      consultarTodos('inseminations/'),
      consultarTodos('vaccinations/'),
    ]);

    animais.value = animaisRes;
    quadrantes.value = quadrantesRes;
    movimentacoes.value = movimentacoesRes;
    ordenhas.value = ordenhasRes;
    inseminacoes.value = inseminacoesRes;
    vacinacoes.value = vacinacoesRes;
  } catch (error) {
    console.error('Erro ao carregar dados do painel:', error);
    erro.value = 'Não foi possível carregar todos os dados do painel. Tente novamente mais tarde.';
  } finally {
    carregando.value = false;
  }
});
</script>

<style scoped>
.dashboard__hero { margin-bottom: 20px; }

.hero__actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
}

.dashboard__filter-menu { position: relative; flex: none; }
.dashboard__filter-menu > summary { list-style: none; }
.dashboard__filter-menu > summary::-webkit-details-marker { display: none; }

.dashboard__filter-panel {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  z-index: 20;
  display: grid;
  width: min(320px, calc(100vw - 32px));
  gap: 14px;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface);
  box-shadow: var(--shadow-md);
}

.dashboard__filter-panel .field { margin: 0; }
.dashboard__filter-panel .select { width: 100%; }

.dashboard__content { display: grid; gap: 20px; }
.dashboard__panel { display: flex; flex-direction: column; gap: 20px; }
.dashboard__panel > * { margin-bottom: 0; }

.dashboard__top-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.dashboard-panel {
  min-width: 0;
  min-height: 258px;
  padding: 18px;
}

.dashboard-panel--reproduction { border-top: 2px solid var(--accent); }
.dashboard-panel--milk {
  grid-column: 1 / -1;
  border-top: 2px solid var(--info);
}

.dashboard-panel__head {
  display: flex;
  align-items: center;
  gap: 11px;
  margin-bottom: 18px;
}

.dashboard-panel__head > div { min-width: 0; }
.dashboard-panel__head h2 { font-size: var(--fs-md); }
.dashboard-panel__head p { margin-top: 3px; color: var(--text-3); font-size: var(--fs-xs); }

.dashboard-panel__icon {
  display: grid;
  width: 34px;
  height: 34px;
  place-items: center;
  flex: none;
  border-radius: 10px;
}

.dashboard-panel__icon--reproduction { background: var(--accent-soft); color: var(--accent); }
.dashboard-panel__icon--milk { background: var(--info-soft); color: var(--info); }
.dashboard-panel__empty { min-height: 150px; }

.dashboard-vet-card {
  min-width: 0;
  min-height: 258px;
  margin-bottom: 0;
  border-radius: var(--r-lg);
  text-decoration: none;
  transition: transform var(--dur-slow) var(--ease-out), box-shadow var(--dur-slow) var(--ease-out);
}

.dashboard-vet-card .hero__img {
  object-position: center 18%;
}

.dashboard-vet-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-hover);
  text-decoration: none;
}

.dashboard-vet-card__content {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 22px 24px;
}

.dashboard-vet-card__title {
  margin-top: 4px;
  color: #fff;
  font-size: 1.55rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  text-shadow: 0 1px 14px rgba(0, 0, 0, 0.38);
}

.dashboard-vet-card__desc {
  max-width: 36ch;
  margin-top: 6px;
  color: rgba(255, 255, 255, 0.92);
  font-size: var(--fs-sm);
  line-height: 1.5;
  text-shadow: 0 1px 10px rgba(0, 0, 0, 0.38);
}

.dashboard-vet-card__cta {
  align-self: flex-start;
}

.farm-summary {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.farm-summary__item {
  display: grid;
  gap: 8px;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface-2);
  color: var(--text-2);
  font-size: var(--fs-xs);
  text-decoration: none;
}

.farm-summary__item:hover {
  border-color: var(--accent-line);
  color: var(--accent);
  text-decoration: none;
}

.farm-summary__item strong {
  color: var(--text);
  font-family: var(--font-mono);
  font-size: var(--fs-2xl);
}

.farm-summary__item:hover strong { color: var(--accent); }

.milk-summary {
  display: grid;
  grid-template-columns: minmax(210px, 0.8fr) minmax(0, 1.2fr);
  align-items: start;
  gap: 24px;
}

.milk-summary__overview { display: grid; align-content: start; gap: 10px; }
.milk-summary__label { color: var(--text-3); font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; }
.milk-summary__average {
  color: var(--text);
  font-family: var(--font-mono);
  font-size: clamp(2rem, 3vw, 2.5rem);
  font-weight: 600;
  line-height: 1;
}

.milk-summary__average small { color: var(--text-2); font-family: var(--font-sans); font-size: var(--fs-sm); }
.milk-summary__details { display: flex; justify-content: space-between; gap: 10px; color: var(--text-3); font-size: var(--fs-xs); }
.milk-summary__details strong { color: var(--text); font-size: var(--fs-sm); }

.milk-month-alert {
  min-width: 0;
  padding: 14px;
  border: 1px solid var(--warn-line);
  border-radius: var(--r-md);
  background: var(--surface-2);
}

.milk-month-alert__head {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 12px;
}

.milk-month-alert__icon,
.milk-month-alert__count {
  display: grid;
  width: 34px;
  height: 34px;
  place-items: center;
  flex: none;
  border-radius: 50%;
  background: var(--ok-soft);
  color: var(--ok);
}

.milk-month-alert__icon.is-alert,
.milk-month-alert__count.is-alert {
  background: var(--warn-soft);
  color: var(--warn);
}

.milk-month-alert__head > div { min-width: 0; flex: 1; }
.milk-month-alert__head h3 { font-size: var(--fs-sm); }
.milk-month-alert__head p,
.milk-month-alert__empty { margin-top: 3px; color: var(--text-3); font-size: var(--fs-xs); }
.milk-month-alert__count { font-family: var(--font-mono); font-weight: 700; }
.milk-month-alert__list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  max-height: 340px;
  overflow-y: auto;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 10px;
}

.milk-month-alert__animal {
  display: grid;
  align-content: start;
  gap: 9px;
  height: 100%;
  padding: 12px;
  border: 1px solid var(--warn-line);
  border-radius: var(--r-md);
  background: var(--surface);
  color: var(--text-2);
  font-size: var(--fs-xs);
  text-decoration: none;
}

.milk-month-alert__animal:hover {
  border-color: var(--warn);
  color: var(--text);
  text-decoration: none;
}

.milk-month-alert__animal-head { display: flex; justify-content: space-between; gap: 8px; }
.milk-month-alert__animal-head strong:first-child { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.milk-month-alert__animal-head strong:last-child { flex: none; color: var(--text); font-family: var(--font-mono); }
.milk-month-alert__meter { display: block; height: 7px; overflow: hidden; border-radius: var(--r-full); background: var(--surface-3); }
.milk-month-alert__meter > span { display: block; height: 100%; border-radius: inherit; background: var(--warn); transition: width 180ms ease; }
.milk-month-alert__animal small { color: var(--warn); font-size: var(--fs-xs); font-weight: 600; }

.dashboard-today { margin-bottom: 20px; overflow: hidden; }
.dashboard-today__head { padding: 16px 18px 4px; }
.dashboard-today__title { margin: 0; font-size: var(--fs-lg); font-weight: 600; color: var(--text); }
.dashboard-today__desc { margin: 2px 0 0; color: var(--text-3); font-size: var(--fs-sm); }
.dashboard-today__list {
  list-style: none;
  margin: 0;
  padding: 12px 18px 18px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}
.dashboard-today__list > li { display: flex; min-width: 0; }
.dashboard-today__item {
  position: relative;
  display: flex;
  width: 100%;
  height: 106px;
  min-height: 106px;
  align-items: center;
  gap: 14px;
  overflow: hidden;
  padding: 12px 14px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface);
  color: var(--text-2);
  text-decoration: none;
  transition: transform var(--dur-slow) var(--ease-out), box-shadow var(--dur-slow) var(--ease-out),
              border-color var(--dur) var(--ease), background var(--dur) var(--ease);
}
.dashboard-today__item:hover {
  border-color: var(--line-strong);
  background: var(--surface-2);
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
}
.dashboard-today__item:active { transform: scale(0.98); }
.dashboard-today__item--active { border-color: var(--warn-line); background: var(--warn-soft); color: var(--text); }
.dashboard-today__item--active.is-info { border-color: var(--info-line); background: var(--info-soft); }
.dashboard-today__item--critical { border-color: var(--danger-line); background: var(--danger-soft); }
.dashboard-today__icon {
  display: flex;
  width: 44px;
  height: 44px;
  flex: none;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  background: var(--ok-soft);
  color: var(--ok);
}
.dashboard-today__item--active .dashboard-today__icon {
  background: var(--surface);
  box-shadow: var(--shadow-sm);
}
.dashboard-today__item--active.is-warn .dashboard-today__icon { color: var(--warn); }
.dashboard-today__item--active.is-info .dashboard-today__icon { color: var(--info); }
.dashboard-today__item--active.is-danger .dashboard-today__icon { color: var(--danger); }
.dashboard-today__count {
  min-width: 32px;
  font-family: var(--font-mono);
  font-size: var(--fs-2xl);
  font-weight: 600;
  line-height: 1;
  text-align: right;
  color: var(--text-3);
}
.dashboard-today__item--active .dashboard-today__count { color: var(--warn); }
.dashboard-today__item--active.is-info .dashboard-today__count { color: var(--info); }
.dashboard-today__item--critical .dashboard-today__count { color: var(--danger); }
.dashboard-today__text { flex: 1; display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.dashboard-today__text strong { font-size: var(--fs-md); font-weight: 600; color: var(--text); }
.dashboard-today__text small { font-size: var(--fs-xs); color: var(--text-3); }
.dashboard-today__text strong,
.dashboard-today__text small {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

@media (max-width: 760px) {
  .dashboard__top-grid { grid-template-columns: 1fr; }
  .dashboard-panel--milk { grid-column: auto; }
  .milk-summary { grid-template-columns: 1fr; }
  .farm-summary { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 520px) {
  .dashboard__filter-menu { align-self: flex-end; }
}
</style>
