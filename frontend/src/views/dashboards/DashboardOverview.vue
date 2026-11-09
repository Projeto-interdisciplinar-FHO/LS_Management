<template>
  <AppShell>
    <div class="page page--wide dashboard">
      <header class="dashboard__head">
        <div>
          <p class="dashboard__eyebrow">Visão da fazenda</p>
          <h1 class="page__title">Painel Principal</h1>
          <p class="page__desc">Acompanhe primeiro a fazenda, depois os estábulos e, por fim, cada animal.</p>
        </div>
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
      </header>

      <nav class="dashboard__shortcuts" aria-label="Atalhos principais">
        <RouterLink :to="linkAnimais" class="dashboard__shortcut">
          <AppIcon name="herd" :size="16" /> Animais
        </RouterLink>
        <RouterLink to="/saude" class="dashboard__shortcut">
          <AppIcon name="syringe" :size="16" /> Saúde & Vacinas
        </RouterLink>
        <RouterLink to="/inseminacoes" class="dashboard__shortcut">
          <AppIcon name="dna" :size="16" /> Inseminações
        </RouterLink>
        <RouterLink to="/lancamento-leite" class="dashboard__shortcut">
          <AppIcon name="milk" :size="16" /> Registrar ordenha
        </RouterLink>
        <span v-if="carregando" class="text-muted dashboard__loading" role="status">
          Atualizando dados...
        </span>
      </nav>

      <p v-if="erro" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ erro }}</span>
      </p>

      <section class="dashboard__top-grid" aria-label="Indicadores gerais da fazenda">
        <article class="card dashboard-panel dashboard-panel--health">
          <header class="dashboard-panel__head">
            <span class="dashboard-panel__icon dashboard-panel__icon--health"><AppIcon name="syringe" :size="18" /></span>
            <div>
              <h2>Sanidade & vacinação</h2>
              <p>Prioridade de saúde do rebanho</p>
            </div>
          </header>
          <div v-if="carregando" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando dados sanitários...</div>
          <div v-else class="dashboard-health">
            <RouterLink to="/saude?filter=overdue" class="dashboard-health__metric">
              <span>Vacinas atrasadas</span>
              <strong :class="{ 'text-danger': vacinasAtrasadas.length }">{{ vacinasAtrasadas.length }}</strong>
            </RouterLink>
            <div class="dashboard-health__bar" aria-hidden="true">
              <span :style="{ width: `${percentualVacinasAtrasadas}%` }"></span>
            </div>
            <p class="dashboard-health__note">{{ animaisFiltrados.length }} animais no recorte atual</p>
            <RouterLink to="/veterinario" class="dashboard-health__metric dashboard-health__metric--secondary">
              <span>Ocorrências clínicas recentes</span>
              <strong>{{ atendimentosRecentes.length }}</strong>
            </RouterLink>
          </div>
        </article>

        <article class="card dashboard-panel dashboard-panel--reproduction">
          <header class="dashboard-panel__head">
            <span class="dashboard-panel__icon dashboard-panel__icon--reproduction"><AppIcon name="barn" :size="18" /></span>
            <div>
              <h2>Estrutura da fazenda</h2>
              <p>Visão geral antes do detalhe por animal</p>
            </div>
          </header>
          <div v-if="carregando" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando estrutura da fazenda...</div>
          <div v-else class="farm-summary">
            <RouterLink :to="linkAnimais" class="farm-summary__item">
              <span>Animais no recorte</span>
              <strong>{{ animaisFiltrados.length }}</strong>
            </RouterLink>
            <div class="farm-summary__item">
              <span>Estábulos cadastrados</span>
              <strong>{{ quadrantes.length }}</strong>
            </div>
          </div>
        </article>

        <article class="card dashboard-panel dashboard-panel--milk">
          <header class="dashboard-panel__head">
            <span class="dashboard-panel__icon dashboard-panel__icon--milk"><AppIcon name="milk" :size="18" /></span>
            <div>
              <h2>Produção geral de leite</h2>
              <p>Fazenda ou estábulo selecionado no período</p>
            </div>
          </header>
          <div v-if="carregando" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando ordenhas...</div>
          <div v-else-if="erro" class="empty dashboard-panel__empty">
            <p class="empty__desc">Não foi possível carregar as ordenhas.</p>
          </div>
          <div v-else class="milk-summary">
            <div class="milk-summary__overview">
              <span class="milk-summary__label">Média geral por ordenha</span>
              <strong class="milk-summary__average">{{ formatarNumero(mediaPorOrdenha) }} <small>L</small></strong>
              <p class="milk-summary__caption">Média calculada com os registros válidos do período.</p>
              <div class="milk-summary__details">
                <span><strong>{{ formatarNumero(totalLeite) }} L</strong> no total</span>
                <span><strong>{{ ordenhasValidas.length }}</strong> registros válidos</span>
              </div>
            </div>
            <div class="below-average">
              <div class="below-average__head">
                <div>
                  <h3>Animais abaixo da média</h3>
                  <p>{{ animaisAbaixoDaMedia.length }} animal(is) com produção média inferior</p>
                </div>
                <button
                  v-if="animaisAbaixoDaMedia.length > 4"
                  type="button"
                  class="btn btn--sm"
                  :aria-expanded="exibirTodosAbaixoDaMedia"
                  @click="exibirTodosAbaixoDaMedia = !exibirTodosAbaixoDaMedia"
                >
                  {{ exibirTodosAbaixoDaMedia ? 'Ver menos' : `Ver mais (${animaisAbaixoDaMedia.length - 4})` }}
                </button>
              </div>
              <p v-if="!animaisAbaixoDaMedia.length" class="below-average__empty">
                {{ ordenhasValidas.length ? 'Nenhum animal está abaixo da média no período.' : 'Sem registros de ordenha para comparar.' }}
              </p>
              <ul v-else class="below-average__list">
                <li v-for="item in animaisAbaixoDaMediaVisiveis" :key="item.animal.id">
                  <RouterLink :to="{ name: 'animal-detail', params: { id: item.animal.id } }">
                    <span>{{ item.animal.name || 'Sem nome' }} · #{{ item.animal.register_number }}</span>
                    <strong>{{ formatarNumero(item.media) }} L</strong>
                  </RouterLink>
                </li>
              </ul>
              <p v-if="!exibirTodosAbaixoDaMedia && animaisAbaixoDaMedia.length > 4" class="below-average__hint">
                Exibindo 4 de {{ animaisAbaixoDaMedia.length }} animais. Clique em &quot;Ver mais&quot; para conferir os demais.
              </p>
            </div>
          </div>
        </article>
      </section>

      <section class="dashboard__chart-grid" aria-label="Indicadores gerais de produção e reprodução">
        <article class="card dashboard-chart-card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Ordenha geral</h2>
              <p class="card__desc">Total de litros registrados por dia para o rebanho selecionado.</p>
            </div>
            <span class="dashboard-chart-card__badge">{{ formatarNumero(totalLeite) }} L</span>
          </header>
          <div v-if="carregando" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando ordenhas...</div>
          <div v-else-if="erro" class="empty"><p class="empty__desc">Os dados de ordenha não puderam ser carregados.</p></div>
          <div v-else-if="!milkChartData.labels.length" class="empty">
            <AppIcon name="milk" :size="28" />
            <p class="empty__desc">Sem ordenhas no período selecionado.</p>
          </div>
          <div v-else class="dashboard-chart">
            <Line :data="milkChartData" :options="milkChartOptions" aria-label="Gráfico do total de litros de leite por dia" />
          </div>
        </article>

        <article class="card dashboard-chart-card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Inseminações no período</h2>
              <p class="card__desc">Registros agrupados conforme o intervalo selecionado.</p>
            </div>
            <span class="dashboard-chart-card__badge dashboard-chart-card__badge--blue">{{ inseminacoesFiltradas.length }} registros</span>
          </header>
          <div v-if="carregando" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando inseminações...</div>
          <div v-else-if="erro" class="empty"><p class="empty__desc">Os dados de reprodução não puderam ser carregados.</p></div>
          <div v-else-if="!inseminacoesFiltradas.length" class="empty">
            <AppIcon name="dna" :size="28" />
            <p class="empty__desc">Nenhuma inseminação registrada no período.</p>
          </div>
          <div v-else class="dashboard-chart">
            <Bar :data="inseminationChartData" :options="inseminationChartOptions" aria-label="Gráfico de inseminações ao longo do período" />
          </div>
        </article>
      </section>

      <section class="card dashboard-alerts" aria-labelledby="dashboard-alerts-title">
        <header class="dashboard-alerts__head">
          <span class="dashboard-alerts__icon"><AppIcon name="alert" :size="18" /></span>
          <div>
            <h2 id="dashboard-alerts-title">Avisos e ações pendentes</h2>
            <p>Alertas sanitários e registros clínicos recentes.</p>
          </div>
          <RouterLink to="/saude" class="btn btn--sm dashboard-alerts__action">Abrir saúde</RouterLink>
        </header>
        <div v-if="carregando" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando avisos...</div>
        <div v-else-if="!avisosPainel.length" class="empty dashboard-alerts__empty">
          <AppIcon name="check-circle" :size="26" />
          <p class="empty__desc">Nenhuma pendência encontrada para o filtro atual.</p>
        </div>
        <div v-else class="table-wrap">
          <table class="table dashboard-alerts__table">
            <thead>
              <tr><th>Identificação</th><th>Módulo</th><th>Descrição do alerta</th><th>Ação rápida</th></tr>
            </thead>
            <tbody>
              <tr v-for="aviso in avisosPainel" :key="aviso.id">
                <td class="dashboard-alerts__animal">
                  <span class="dashboard-alerts__animal-mark">#{{ aviso.animal.register_number }}</span>
                  <strong>{{ aviso.animal.name || 'Sem nome' }}</strong>
                </td>
                <td><span class="dashboard-alerts__module" :class="`dashboard-alerts__module--${aviso.tipo}`">{{ aviso.modulo }}</span></td>
                <td>
                  <span class="dashboard-alerts__description" :class="{ 'dashboard-alerts__description--alert': aviso.critico }">
                    <AppIcon :name="aviso.critico ? 'alert' : 'stethoscope'" :size="15" />
                    {{ aviso.descricao }}
                  </span>
                </td>
                <td class="dashboard-alerts__action-cell">
                  <RouterLink :to="aviso.para" class="btn btn--sm">{{ aviso.acao }}</RouterLink>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </AppShell>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  LinearScale,
  LineController,
  LineElement,
  PointElement,
  Tooltip,
} from 'chart.js';
import { Bar, Line } from 'vue-chartjs';
import api from '@/services/api';
import { ehAdministrador } from '@/services/auth';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import { idRelacao, ultimaMovimentacaoPorAnimal } from '@/utils/animalMovementUtils';

ChartJS.register(BarElement, CategoryScale, LinearScale, LineController, LineElement, PointElement, Tooltip);

const carregando = ref(true);
const erro = ref('');
const animais = ref([]);
const quadrantes = ref([]);
const movimentacoes = ref([]);
const ordenhas = ref([]);
const inseminacoes = ref([]);
const atendimentos = ref([]);
const vacinacoes = ref([]);
const quadranteSelecionado = ref('todos');
const periodoSelecionado = ref('30');
const exibirTodosAbaixoDaMedia = ref(false);

const ehAdmin = computed(() => ehAdministrador());
const linkAnimais = computed(() => (ehAdmin.value ? '/animais' : '/rebanho'));
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

const atendimentosRecentes = computed(() =>
  atendimentos.value
    .filter((registro) => {
      const animalId = idRelacao(registro.animal ?? registro.animal_id);
      return animaisPorId.value.has(String(animalId))
        && dentroDoPeriodo(dataDoRegistro(registro, ['consultation_date']));
    })
    .sort((a, b) => String(b.consultation_date || '').localeCompare(String(a.consultation_date || '')))
);

const percentualVacinasAtrasadas = computed(() => {
  if (!animaisFiltrados.value.length) return 0;
  return Math.min(100, (vacinasAtrasadas.value.length / animaisFiltrados.value.length) * 100);
});

function formatarData(data) {
  if (!data) return '—';
  return new Date(`${String(data).slice(0, 10)}T00:00:00`).toLocaleDateString('pt-BR');
}

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

const ordenhasFiltradas = computed(() => ordenhas.value.filter((registro) => {
  const animalId = idRelacao(registro.animal ?? registro.animal_id);
  return animaisPorId.value.has(String(animalId))
    && dentroDoPeriodo(dataDoRegistro(registro, ['production_date', 'date_collected', 'date']));
}));

const inseminacoesFiltradas = computed(() => inseminacoes.value.filter((registro) => {
  const animalId = idRelacao(registro.mother ?? registro.mother_id);
  return animaisPorId.value.has(String(animalId))
    && dentroDoPeriodo(dataDoRegistro(registro, ['date']));
}));

function quantidadeDeLeite(registro) {
  const quantidade = Number(registro.milk_production ?? registro.milk_quantity ?? registro.quantity);
  return Number.isFinite(quantidade) && quantidade > 0 ? quantidade : 0;
}

const ordenhasValidas = computed(() =>
  ordenhasFiltradas.value.filter((registro) => quantidadeDeLeite(registro) > 0)
);

const totalLeite = computed(() =>
  ordenhasValidas.value.reduce((total, registro) => total + quantidadeDeLeite(registro), 0)
);

const mediaPorOrdenha = computed(() =>
  ordenhasValidas.value.length ? totalLeite.value / ordenhasValidas.value.length : 0
);

const mediasPorAnimal = computed(() => {
  const totais = new Map();
  for (const registro of ordenhasValidas.value) {
    const animalId = idRelacao(registro.animal ?? registro.animal_id);
    const animal = animaisPorId.value.get(String(animalId));
    const litros = quantidadeDeLeite(registro);
    if (!animal || !litros) continue;
    const item = totais.get(String(animal.id)) || { animal, litros: 0, registros: 0 };
    item.litros += litros;
    item.registros += 1;
    totais.set(String(animal.id), item);
  }
  return [...totais.values()].map((item) => ({
    ...item,
    media: item.litros / item.registros,
  }));
});

const animaisAbaixoDaMedia = computed(() =>
  mediasPorAnimal.value
    .filter((item) => item.media < mediaPorOrdenha.value)
    .sort((a, b) => a.media - b.media)
);
const animaisAbaixoDaMediaVisiveis = computed(() =>
  exibirTodosAbaixoDaMedia.value
    ? animaisAbaixoDaMedia.value
    : animaisAbaixoDaMedia.value.slice(0, 4)
);

const producaoLeitePorDia = computed(() => {
  const totaisPorDia = new Map();

  for (const registro of ordenhasValidas.value) {
    const data = dataDoRegistro(registro, ['production_date', 'date_collected', 'date']);
    if (!data) continue;

    const dia = [
      data.getFullYear(),
      String(data.getMonth() + 1).padStart(2, '0'),
      String(data.getDate()).padStart(2, '0'),
    ].join('-');
    totaisPorDia.set(dia, (totaisPorDia.get(dia) || 0) + quantidadeDeLeite(registro));
  }

  return [...totaisPorDia.entries()]
    .sort(([diaA], [diaB]) => diaA.localeCompare(diaB))
    .map(([dia, litros]) => ({
      rotulo: formatarData(dia),
      litros,
    }));
});

const milkChartData = computed(() => ({
  labels: producaoLeitePorDia.value.map((item) => item.rotulo),
  datasets: [{
    label: 'Produção geral (L)',
    data: producaoLeitePorDia.value.map((item) => item.litros),
    borderColor: chartColor('--accent'),
    backgroundColor: chartColor('--accent'),
    pointBackgroundColor: chartColor('--accent'),
    pointRadius: producaoLeitePorDia.value.length > 60 ? 1 : 3,
    pointHoverRadius: 5,
    borderWidth: 2,
    tension: 0.25,
    spanGaps: false,
  }],
}));

const inseminacoesPorIntervalo = computed(() => {
  const agrupadas = new Map();
  const agruparPorSemana = periodoSelecionado.value === '30' || periodoSelecionado.value === '90';

  for (const registro of inseminacoesFiltradas.value) {
    const data = dataDoRegistro(registro, ['date']);
    if (!data) continue;

    const inicio = new Date(data);
    if (agruparPorSemana) {
      const diasDesdeSegunda = (inicio.getDay() + 6) % 7;
      inicio.setDate(inicio.getDate() - diasDesdeSegunda);
    } else {
      inicio.setDate(1);
    }

    const chave = `${inicio.getFullYear()}-${String(inicio.getMonth() + 1).padStart(2, '0')}-${String(inicio.getDate()).padStart(2, '0')}`;
    agrupadas.set(chave, (agrupadas.get(chave) || 0) + 1);
  }

  return [...agrupadas.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .slice(-12)
    .map(([chave, quantidade]) => {
      const [ano, mes, dia] = chave.split('-').map(Number);
      const data = new Date(ano, mes - 1, dia);
      return {
        rotulo: agruparPorSemana
          ? data.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })
          : data.toLocaleDateString('pt-BR', { month: 'short', year: '2-digit' }),
        quantidade,
      };
    });
});

function formatarNumero(valor) {
  return valor.toLocaleString('pt-BR', { maximumFractionDigits: 1 });
}

function chartColor(token) {
  return getComputedStyle(document.documentElement).getPropertyValue(token).trim();
}

const avisosPainel = computed(() => {
  const alertasVacina = vacinasAtrasadas.value.map((vacina) => {
    const animalId = idRelacao(vacina.animal ?? vacina.animal_id);
    const animal = animaisPorId.value.get(String(animalId));
    if (!animal) return null;
    const nomeVacina = vacina.vaccine_name || vacina.vaccine?.name || 'Vacina';
    return {
      id: `vacina-${vacina.id}`,
      animal,
      tipo: 'health',
      modulo: 'SANIDADE',
      critico: true,
      descricao: `${nomeVacina} · reforço vencido em ${formatarData(vacina.next_vaccination_date)}`,
      para: { name: 'animal-detail', params: { id: animal.id }, query: { tab: 'vacinas' } },
      acao: 'Ver ficha',
    };
  });
  const alertasClinicos = atendimentosRecentes.value.map((registro) => {
    const animalId = idRelacao(registro.animal ?? registro.animal_id);
    const animal = animaisPorId.value.get(String(animalId));
    if (!animal) return null;
    return {
      id: `clinico-${registro.id}`,
      animal,
      tipo: 'clinical',
      modulo: 'VETERINÁRIO',
      critico: false,
      descricao: `${registro.consultation_reason || 'Atendimento registrado'} · ${formatarData(registro.consultation_date)}`,
      para: { name: 'animal-detail', params: { id: animal.id }, query: { tab: 'veterinario' } },
      acao: 'Ver ficha',
    };
  });
  return [...alertasVacina, ...alertasClinicos].filter(Boolean).slice(0, 8);
});

function chartOptions(unit) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom',
        labels: { color: chartColor('--text-2'), boxWidth: 10, usePointStyle: true },
      },
      tooltip: {
        callbacks: {
          label: (context) => ` ${context.raw.toLocaleString('pt-BR', { maximumFractionDigits: 1 })} ${unit}`,
        },
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { color: chartColor('--text-2'), maxRotation: 0 },
      },
      y: {
        beginAtZero: unit === 'L',
        grid: { color: chartColor('--line') },
        ticks: { color: chartColor('--text-3') },
      },
    },
  };
}

const milkChartOptions = computed(() => chartOptions('L'));

const inseminationChartData = computed(() => ({
  labels: inseminacoesPorIntervalo.value.map((item) => item.rotulo),
  datasets: [{
    label: 'Inseminações',
    data: inseminacoesPorIntervalo.value.map((item) => item.quantidade),
    backgroundColor: chartColor('--info'),
    borderRadius: 7,
    maxBarThickness: 32,
  }],
}));

const inseminationChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context) => ` ${context.raw} inseminação(ões)`,
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: chartColor('--text-2') },
    },
    y: {
      beginAtZero: true,
      ticks: { precision: 0, color: chartColor('--text-3') },
      grid: { color: chartColor('--line') },
    },
  },
}));

onMounted(async () => {
  try {
    const [animaisRes, quadrantesRes, movimentacoesRes, ordenhasRes, inseminacoesRes, atendimentosRes, vacinacoesRes] = await Promise.all([
      consultarTodos('animals/'),
      consultarTodos('quadrants/'),
      consultarTodos('animal_movements/'),
      consultarTodos('milk_production_history/'),
      consultarTodos('inseminations/'),
      consultarTodos('animal_health/'),
      consultarTodos('vaccinations/'),
    ]);

    animais.value = animaisRes;
    quadrantes.value = quadrantesRes;
    movimentacoes.value = movimentacoesRes;
    ordenhas.value = ordenhasRes;
    inseminacoes.value = inseminacoesRes;
    atendimentos.value = atendimentosRes;
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
.dashboard__actions { align-items: center; }
.dashboard__action-menu { position: relative; }

.dashboard__action-popover {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  z-index: 20;
  min-width: 180px;
  padding: 5px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface);
  box-shadow: var(--shadow-md);
}

.dashboard__action-popover--right { right: 0; left: auto; }

.dashboard__action-option {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 9px 10px;
  border-radius: var(--r);
  color: var(--text-2);
  font-size: var(--fs-sm);
  text-decoration: none;
}

.dashboard__action-option:hover {
  background: var(--surface-3);
  color: var(--text);
  text-decoration: none;
}

.dashboard__action-option svg { color: var(--accent); }
</style>

<style scoped>
.dashboard__filters {
  align-items: flex-end;
  margin-bottom: 20px;
}

.dashboard__filter { width: min(280px, 100%); }
.dashboard__loading { padding-bottom: 8px; }
.dashboard__charts { align-items: start; }
.dashboard__metrics {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.dashboard-metric {
  position: relative;
  min-width: 0;
  overflow: hidden;
  padding: 15px 17px;
  color: var(--text);
  text-decoration: none;
  border-left: 3px solid var(--metric-color, var(--accent));
  background: linear-gradient(
    125deg,
    color-mix(in srgb, var(--metric-color, var(--accent)) 18%, var(--surface)),
    var(--surface) 78%
  );
  transition: border-color var(--dur) var(--ease), transform var(--dur) var(--ease), box-shadow var(--dur) var(--ease);
}

.dashboard-metric:hover {
  border-color: var(--metric-color, var(--accent));
  color: var(--text);
  text-decoration: none;
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.dashboard-metric--herd { --metric-color: var(--accent); }
.dashboard-metric--milk { --metric-color: var(--accent); }
.dashboard-metric--insemination { --metric-color: var(--info); }
.dashboard-metric--birth { --metric-color: var(--warn); }
.dashboard-metric--health { --metric-color: var(--danger); }

.dashboard-metric__label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--metric-color, var(--text-2));
  font-size: var(--fs-sm);
  font-weight: 600;
}

.dashboard-metric__label svg {
  box-sizing: content-box;
  padding: 6px;
  border-radius: 9px;
  background: color-mix(in srgb, var(--metric-color, var(--accent)) 20%, var(--surface));
  color: var(--metric-color, var(--accent));
}

.dashboard-metric__value {
  display: block;
  margin-top: 12px;
  color: var(--metric-color, var(--text));
  font-family: var(--font-mono);
  font-size: var(--fs-3xl);
  font-weight: 500;
  line-height: 1;
}

.dashboard-metric__detail {
  display: block;
  margin-top: 8px;
  color: var(--text-3);
  font-size: var(--fs-xs);
}

.dashboard-metric--alert {
  border-color: var(--danger-line);
  background: linear-gradient(125deg, var(--danger-soft), var(--surface) 76%);
}

.dashboard-metric--alert .dashboard-metric__label,
.dashboard-metric--alert .dashboard-metric__value { color: var(--danger); }
.dashboard-metric--alert .dashboard-metric__label svg { color: var(--danger); }

.dashboard__overview { align-items: stretch; margin-bottom: 18px; }
.dashboard__charts { align-items: stretch; }
.dashboard__status-card,
.dashboard__health-card { border-top: 2px solid var(--accent); }
.dashboard__health-card { border-top-color: var(--danger); }
.dashboard__health-link {
  border-color: var(--danger-line);
  color: var(--danger);
}
.dashboard__health-link:hover { background: var(--danger-soft); }
.dashboard__total-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 9px;
  border-radius: var(--r-full);
  background: var(--accent-soft);
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: var(--fs-xs);
  font-weight: 600;
}

.dashboard-chart-icon {
  display: grid;
  width: 34px;
  height: 34px;
  place-items: center;
  border-radius: 10px;
}

.dashboard-chart-icon--milk { background: var(--accent-soft); color: var(--accent); }
.dashboard-chart-icon--reproduction { background: var(--info-soft); color: var(--info); }
.dashboard__reproduction-card { border-top: 2px solid var(--info); }
.dashboard__pregnancy-note {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 0 18px 16px;
  padding: 11px 12px;
  border: 1px solid color-mix(in srgb, var(--info) 28%, var(--line));
  border-radius: var(--r);
  background: color-mix(in srgb, var(--info) 9%, var(--surface));
  color: var(--text-2);
  font-size: var(--fs-xs);
  line-height: 1.5;
}

.dashboard__attention-empty { min-height: 240px; }
.dashboard__attention-list { padding: 4px 18px; }

.dashboard__attention-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  border-bottom: 1px solid var(--line);
  color: var(--text);
  text-decoration: none;
}

.dashboard__attention-item:last-child { border-bottom: 0; }
.dashboard__attention-item:hover { color: var(--accent); text-decoration: none; }
.dashboard__attention-item > svg { color: var(--text-3); flex: none; }

.dashboard__attention-icon {
  display: grid;
  width: 34px;
  height: 34px;
  place-items: center;
  flex: none;
  border-radius: 50%;
  background: var(--surface-3);
  color: var(--accent);
}

.dashboard__attention-item--alert .dashboard__attention-icon {
  background: var(--danger-soft);
  color: var(--danger);
}

.dashboard__attention-copy { display: grid; min-width: 0; gap: 4px; }
.dashboard__attention-copy strong,
.dashboard__attention-copy span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dashboard__attention-copy strong { font-size: var(--fs-sm); font-weight: 600; }
.dashboard__attention-copy span { color: var(--text-3); font-size: var(--fs-xs); }
.dashboard-chart { position: relative; height: 270px; padding: 8px 18px 18px; }
.status-chart { display: grid; grid-template-columns: minmax(130px, 0.9fr) minmax(125px, 1fr); align-items: center; gap: 18px; padding: 18px; }
.status-chart__plot { position: relative; width: 100%; max-width: 190px; height: 190px; justify-self: center; }
.status-chart__legend { display: grid; gap: 8px; }
.status-chart__legend-item { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 8px; border-radius: var(--r); color: var(--text); text-decoration: none; }
.status-chart__legend-item:hover { background: var(--surface-2); }
.status-chart__legend-item strong { font-family: var(--font-mono); font-size: var(--fs-sm); }
.status-chart__legend-name { display: flex; align-items: center; gap: 8px; color: var(--text-2); font-size: var(--fs-sm); }
.status-chart__dot { width: 9px; height: 9px; flex: none; border-radius: var(--r-full); background: var(--ok); }
.status-chart__dot--muted { background: var(--text-3); }
.status-chart__dot--warn { background: var(--warn); }
.status-chart__dot--danger { background: var(--danger); }

@media (max-width: 600px) {
  .page__actions { width: 100%; flex-wrap: wrap; }
  .dashboard__filter { width: 100%; }
  .dashboard__metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 9px; }
  .dashboard-metric { padding: 12px; }
  .dashboard-metric__detail { min-height: 30px; }
  .status-chart { grid-template-columns: 1fr; }
  .dashboard__attention-list { padding-inline: 14px; }
  .status-chart__plot { height: 170px; }
  .dashboard-chart { height: 230px; padding-inline: 8px; }
}
</style>

<style scoped>
.dashboard__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 12px;
}

.dashboard__eyebrow {
  margin-bottom: 4px;
  color: var(--accent);
  font-size: var(--fs-xs);
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.dashboard__head .page__title { font-size: var(--fs-2xl); }
.dashboard__head .page__desc { margin-top: 4px; }

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

.dashboard__shortcuts {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.dashboard__shortcut {
  display: inline-flex;
  min-height: 34px;
  align-items: center;
  gap: 7px;
  padding: 0 11px;
  border: 1px solid var(--line);
  border-radius: var(--r);
  background: var(--surface);
  color: var(--text-2);
  font-size: var(--fs-sm);
  font-weight: 500;
  text-decoration: none;
  transition: background var(--dur) var(--ease), color var(--dur) var(--ease), border-color var(--dur) var(--ease);
}

.dashboard__shortcut svg { color: var(--accent); }
.dashboard__shortcut:hover {
  border-color: var(--accent-line);
  background: var(--accent-soft);
  color: var(--accent);
  text-decoration: none;
}

.dashboard__loading { margin-left: auto; font-size: var(--fs-xs); }
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

.dashboard-panel--health { border-top: 2px solid var(--danger); }
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

.dashboard-panel__icon--health { background: var(--danger-soft); color: var(--danger); }
.dashboard-panel__icon--reproduction { background: var(--accent-soft); color: var(--accent); }
.dashboard-panel__icon--milk { background: var(--info-soft); color: var(--info); }

.dashboard-health { display: grid; gap: 10px; }
.dashboard-health__metric,
.dashboard-health__coverage {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  color: var(--text-2);
  font-size: var(--fs-sm);
  text-decoration: none;
}

.dashboard-health__metric:hover { color: var(--text); text-decoration: none; }
.dashboard-health__metric strong { color: var(--text); font-family: var(--font-mono); }
.dashboard-health__metric strong.text-danger { color: var(--danger); }
.dashboard-health__metric--secondary {
  padding-top: 10px;
  border-top: 1px solid var(--line);
}

.dashboard-health__bar {
  height: 7px;
  overflow: hidden;
  border-radius: var(--r-full);
  background: var(--surface-3);
}

.dashboard-health__bar span {
  display: block;
  height: 100%;
  min-width: 0;
  border-radius: inherit;
  background: var(--danger);
  transition: width 180ms ease;
}

.dashboard-health__note { color: var(--text-3); font-size: var(--fs-xs); }
.dashboard-panel__empty { min-height: 150px; }

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
.milk-summary__caption { color: var(--text-3); font-size: var(--fs-xs); }
.milk-summary__details { display: flex; justify-content: space-between; gap: 10px; color: var(--text-3); font-size: var(--fs-xs); }
.milk-summary__details strong { color: var(--text); font-size: var(--fs-sm); }

.below-average {
  min-width: 0;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface-2);
}

.below-average__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.below-average__head h3 { font-size: var(--fs-sm); }
.below-average__head p,
.below-average__empty { margin-top: 3px; color: var(--text-3); font-size: var(--fs-xs); }
.below-average__hint { margin-top: 8px; color: var(--text-3); font-size: var(--fs-xs); }
.below-average__list {
  display: grid;
  max-height: 240px;
  overflow-y: auto;
  list-style: none;
}
.below-average__list li + li { border-top: 1px solid var(--line); }
.below-average__list a {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 0;
  color: var(--text-2);
  font-size: var(--fs-xs);
  text-decoration: none;
}

.below-average__list a:hover { color: var(--accent); text-decoration: none; }
.below-average__list strong { flex: none; color: var(--text); font-family: var(--font-mono); }

.dashboard__chart-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr);
  align-items: stretch;
  gap: 16px;
  margin-bottom: 16px;
}

.dashboard-chart-card { min-width: 0; min-height: 310px; }
.dashboard-chart-card .card__head { align-items: flex-start; }
.dashboard-chart-card__badge {
  flex: none;
  padding: 5px 8px;
  border: 1px solid var(--accent-line);
  border-radius: var(--r);
  background: var(--accent-soft);
  color: var(--accent);
  font-size: var(--fs-xs);
  font-weight: 600;
}

.dashboard-chart-card__badge--blue {
  border-color: var(--info-line);
  background: var(--info-soft);
  color: var(--info);
}

.dashboard-chart { position: relative; height: 250px; padding: 8px 18px 18px; }

.dashboard-alerts { overflow: hidden; }
.dashboard-alerts__head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 18px;
  border-bottom: 1px solid var(--line);
}

.dashboard-alerts__head > div { min-width: 0; flex: 1; }
.dashboard-alerts__head h2 { font-size: var(--fs-lg); }
.dashboard-alerts__head p { margin-top: 3px; color: var(--text-3); font-size: var(--fs-xs); }
.dashboard-alerts__icon {
  display: grid;
  width: 36px;
  height: 36px;
  place-items: center;
  flex: none;
  border: 1px solid var(--danger-line);
  border-radius: 50%;
  background: var(--danger-soft);
  color: var(--danger);
}

.dashboard-alerts__action { border-color: var(--accent-line); color: var(--accent); }
.dashboard-alerts__empty { min-height: 130px; }
.dashboard-alerts__table { min-width: 700px; }
.dashboard-alerts__animal { display: flex; align-items: center; gap: 9px; }
.dashboard-alerts__animal-mark {
  display: inline-grid;
  width: 34px;
  height: 34px;
  place-items: center;
  flex: none;
  border-radius: 50%;
  background: var(--surface-3);
  color: var(--text-2);
  font-family: var(--font-mono);
  font-size: 10px;
}

.dashboard-alerts__module {
  display: inline-flex;
  padding: 5px 8px;
  border-radius: var(--r);
  background: var(--info-soft);
  color: var(--info);
  font-size: 10px;
  font-weight: 700;
}

.dashboard-alerts__module--clinical { background: var(--accent-soft); color: var(--accent); }
.dashboard-alerts__description { display: inline-flex; align-items: center; gap: 7px; color: var(--text-2); }
.dashboard-alerts__description--alert { color: var(--danger); }
.dashboard-alerts__description svg { flex: none; }
.dashboard-alerts__action-cell { text-align: right; }

@media (max-width: 1120px) {
  .dashboard__top-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .dashboard-panel--milk { grid-column: 1 / -1; }
}

@media (max-width: 760px) {
  .dashboard__head { align-items: flex-start; }
  .dashboard__top-grid,
  .dashboard__chart-grid { grid-template-columns: 1fr; }
  .dashboard-panel--milk { grid-column: auto; }
  .milk-summary { grid-template-columns: 1fr; }
  .farm-summary { grid-template-columns: 1fr 1fr; }
  .dashboard__loading { width: 100%; margin-left: 0; }
  .dashboard-alerts__head { align-items: flex-start; flex-wrap: wrap; }
  .dashboard-alerts__action { margin-left: 48px; }
}

@media (max-width: 520px) {
  .dashboard__head { flex-direction: column; }
  .dashboard__filter-menu { align-self: flex-end; }
  .dashboard__shortcuts { gap: 6px; }
  .dashboard__shortcut { font-size: var(--fs-xs); }
  .dashboard-chart-card .card__head { flex-wrap: wrap; }
  .dashboard-chart { height: 230px; padding-inline: 10px; }
}
</style>
