<template>
  <AppShell>
    <div class="page page--wide animal-list-page">
      <PageHeader
        titulo="Animais"
        :descricao="headerDescription"
        voltar-rotulo="Painel"
        voltar-para="/dashboard-adm"
      >
        <template #acoes>
          <RouterLink to="/animais/novo" class="btn btn--primary">
            <AppIcon name="plus" :size="16" />
            Cadastrar animal
          </RouterLink>
        </template>
      </PageHeader>

      <AppTabs
        v-model="abaAtiva"
        :tabs="abas"
        label="Seções de animais"
        id-base="animais"
      />

      <p v-if="erroAcao" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ erroAcao }}</span>
      </p>

      <!-- ABA REBANHO (VACAS / BOVINOS) -->
      <div
        v-if="abaAtiva === 'rebanho'"
        id="animais-panel-rebanho"
        role="tabpanel"
        aria-labelledby="animais-tab-rebanho"
      >
        <p v-if="alertaProducao" class="alert alert--warn" role="status">
          <AppIcon name="alert" :size="16" />
          <span>A média considera as ordenhas do mês atual. Selecione o alerta ao lado da situação para abrir o gráfico e o histórico.</span>
        </p>
        <p v-if="erroProducaoLeite" class="alert alert--danger" role="alert">
          <AppIcon name="alert" :size="16" />
          <span>{{ erroProducaoLeite }}</span>
          <button type="button" class="btn btn--sm" @click="loadMilkHistory">Tentar novamente</button>
        </p>

        <section class="animal-filters card" aria-label="Filtros do rebanho">
          <div class="animal-filters__heading">
            <div>
              <h2 class="card__title">Rebanho</h2>
              <p class="card__desc">Escolha uma situação para filtrar os animais.</p>
            </div>
            <span class="badge">{{ animals.length }} bovinos</span>
          </div>

          <nav class="animal-filter-tabs" aria-label="Filtrar animais por situação">
            <RouterLink
              v-for="opcao in filtros"
              :key="opcao.valor"
              :to="linkFiltro(opcao.valor)"
              class="animal-filter-tab"
              :class="{ 'is-active': filtro === opcao.valor }"
              :aria-current="filtro === opcao.valor ? 'page' : undefined"
            >
              <span>{{ opcao.rotulo }}</span>
              <span class="count">{{ contar(opcao.valor) }}</span>
            </RouterLink>
          </nav>
        </section>

        <section class="registry-toolbar" aria-label="Busca e filtros adicionais">
          <label class="search">
            <AppIcon name="search" :size="16" />
            <input
              v-model="busca"
              class="input"
              type="search"
              placeholder="Buscar por brinco ou nome"
              aria-label="Buscar animal"
            >
          </label>

          <div class="field animal-list__quadrant">
            <label class="field__label" for="filtro-quadrante">Estábulo</label>
            <select id="filtro-quadrante" v-model="quadrante" class="select">
              <option value="todos">Todos os estábulos</option>
              <option v-for="item in quadrantes" :key="item.id" :value="String(item.id)">
                {{ item.name || item.tipo || `Estábulo ${item.id}` }}
              </option>
            </select>
          </div>

          <span class="registry-toolbar__count">{{ visiveis.length }} resultado(s)</span>
        </section>

        <RegistryCard
          :carregando="loading || (alertaProducao && carregandoProducaoLeite)"
          texto-carregando="Buscando registros..."
          :vazio="animals.length === 0"
          :vazio-filtrado="animals.length > 0 && visiveis.length === 0"
          icone-vazio="animal"
          titulo-vazio="Nenhum bovino cadastrado"
          descricao-vazia="Cadastre um bovino para começar a organizar o rebanho."
          :descricao-vazio-filtrado="alertaProducao ? 'Nenhum animal abaixo da média corresponde aos filtros atuais.' : 'Nenhum animal corresponde a esta busca ou filtro.'"
          @limpar-filtros="limparFiltros"
        >
          <template #acao-vazio>
            <RouterLink to="/animais/novo" class="btn btn--primary">
              <AppIcon name="plus" :size="15" />
              Cadastrar bovino
            </RouterLink>
          </template>

          <div class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>Brinco</th>
                  <th>Nome</th>
                  <th>Estábulo atual</th>
                  <th>Situação</th>
                  <th class="cell-actions">Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="animal in visiveis" :key="animal.id">
                  <td class="mono">#{{ animal.register_number }}</td>
                  <td class="cell-strong truncate" :title="animal.name || '—'">
                    <RouterLink :to="{ name: 'animal-detail', params: { id: animal.id } }" class="cell-link">{{ animal.name || '—' }}</RouterLink>
                  </td>
                  <td class="truncate" :title="estabuloAtual(animal.id)">{{ estabuloAtual(animal.id) }}</td>
                  <td>
                    <div class="animal-list__status">
                      <span class="badge" :class="badgeSituacao(animal.status)">
                        <span class="badge__dot"></span>
                        {{ rotuloSituacao(animal.status) }}
                      </span>
                      <button
                        v-if="abaixoDaMedia(animal)"
                        type="button"
                        class="badge badge--warn animal-list__production-alert"
                        :aria-label="`Produção abaixo da média para ${animal.name || 'animal'} #${animal.register_number}. Abrir histórico de ordenha.`"
                        title="Ver gráfico e histórico de ordenha"
                        @click="viewMilkDetails(animal.id)"
                      >
                        <AppIcon name="alert" :size="13" />
                        Abaixo da média
                      </button>
                    </div>
                  </td>
                  <td class="cell-actions">
                    <div class="registry-actions">
                      <button type="button" class="btn btn--sm" @click="viewDetails(animal.id)">Ver ficha</button>
                      <button
                        type="button"
                        class="btn btn--icon"
                        aria-label="Editar bovino"
                        title="Editar bovino"
                        @click="router.push(`/animais/editar/${animal.id}`)"
                      >
                        <AppIcon name="edit" :size="15" />
                      </button>
                      <button
                        type="button"
                        class="btn btn--icon is-danger"
                        aria-label="Excluir bovino"
                        title="Excluir bovino"
                        @click="excluirAnimal(animal)"
                      >
                        <AppIcon name="trash" :size="15" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </RegistryCard>

        <p v-if="visiveis.length" class="rodape-tabela">
          {{ visiveis.length }} de {{ animals.length }} animais
        </p>
      </div>

      <!-- ABA TOUROS -->
      <div
        v-else
        id="animais-panel-touros"
        role="tabpanel"
        aria-labelledby="animais-tab-touros"
      >
        <section class="registry-toolbar" aria-label="Busca e filtro de touros">
          <label class="search">
            <AppIcon name="search" :size="16" />
            <input
              v-model="buscaTouro"
              class="input"
              type="search"
              placeholder="Buscar touro por brinco, nome ou raça"
              aria-label="Buscar touro"
            >
          </label>

          <div class="field animal-list__quadrant">
            <label class="field__label" for="filtro-touro-ativo">Situação</label>
            <select id="filtro-touro-ativo" v-model="filtroTouroAtivo" class="select">
              <option value="todos">Todos os touros</option>
              <option value="ativos">Ativos</option>
              <option value="inativos">Inativos</option>
            </select>
          </div>

          <span class="registry-toolbar__count">{{ tourosVisiveis.length }} resultado(s)</span>
        </section>

        <RegistryCard
          titulo="Touros cadastrados"
          descricao="Reprodutores disponíveis para inseminações e acompanhamento genealógico."
          :total="bulls.length"
          :carregando="loadingBulls"
          texto-carregando="Carregando touros..."
          :vazio="bulls.length === 0"
          :vazio-filtrado="bulls.length > 0 && tourosVisiveis.length === 0"
          icone-vazio="dna"
          titulo-vazio="Nenhum touro cadastrado"
          descricao-vazia="Cadastre os touros reprodutores da fazenda."
          rotulo-acao-vazio="Cadastrar touro"
          descricao-vazio-filtrado="Nenhum touro corresponde à busca ou ao filtro selecionado."
          @cadastrar="router.push({ path: '/animais/novo', query: { tipo: 'touro' } })"
          @limpar-filtros="limparFiltrosTouro"
        >
          <div class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>Brinco</th>
                  <th>Nome</th>
                  <th>Raça</th>
                  <th>Situação</th>
                  <th class="cell-actions">Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="bull in tourosVisiveis" :key="bull.id">
                  <td class="mono">#{{ bull.register_number }}</td>
                  <td class="cell-strong truncate" :title="bull.name || '—'">{{ bull.name || '—' }}</td>
                  <td class="truncate" :title="nomeRaca(bull.breed)">{{ nomeRaca(bull.breed) }}</td>
                  <td>
                    <span class="badge" :class="bull.active ? 'badge--ok' : ''">
                      <span class="badge__dot"></span>
                      {{ bull.active ? 'Ativo' : 'Inativo' }}
                    </span>
                  </td>
                  <td class="cell-actions">
                    <div class="registry-actions">
                      <button
                        type="button"
                        class="btn btn--icon"
                        aria-label="Editar touro"
                        title="Editar touro"
                        @click="router.push({ path: '/animais/novo', query: { tipo: 'touro', bullId: String(bull.id) } })"
                      >
                        <AppIcon name="edit" :size="15" />
                      </button>
                      <button
                        type="button"
                        class="btn btn--icon is-danger"
                        aria-label="Excluir touro"
                        title="Excluir touro"
                        @click="excluirTouro(bull)"
                      >
                        <AppIcon name="trash" :size="15" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </RegistryCard>

        <p v-if="tourosVisiveis.length" class="rodape-tabela">
          {{ tourosVisiveis.length }} de {{ bulls.length }} touros
        </p>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import { confirmar } from '@/services/confirmService';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppTabs from '@/components/ui/AppTabs.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import RegistryCard from '@/components/layout/RegistryCard.vue';
import { badgeSituacao, rotuloSituacao, situacao } from '@/utils/statusUtils';
import { idRelacao, ultimaMovimentacaoPorAnimal, nomeEstabulo } from '@/utils/animalMovementUtils';
import { apiErrorMessage } from '@/utils/apiError';
import { metricasProducaoPorAnimal, ordenhasDoMesAtual } from '@/utils/milkProductionMetrics';

const router = useRouter();
const route = useRoute();
const animals = ref([]);
const bulls = ref([]);
const breeds = ref([]);
const quadrantes = ref([]);
const movimentacoes = ref([]);
const ordenhas = ref([]);
const erroProducaoLeite = ref('');
const erroAcao = ref('');
const carregandoProducaoLeite = ref(true);
const loading = ref(true);
const loadingBulls = ref(true);

const abaAtiva = ref(route.query.aba === 'touros' ? 'touros' : 'rebanho');
const abas = computed(() => [
  { id: 'rebanho', label: 'Rebanho', icon: 'animal', count: animals.value.length },
  { id: 'touros', label: 'Touros', icon: 'dna', count: bulls.value.length },
]);

const headerDescription = computed(() => {
  if (abaAtiva.value === 'touros') return 'Consulte, filtre e gerencie os touros reprodutores.';
  return alertaProducao.value
    ? 'Animais com produção abaixo da média no mês atual.'
    : 'Consulte e filtre os bovinos do rebanho.';
});

// Filtros Rebanho
const busca = ref('');
const filtrosValidos = ['todos', 'active', 'inactive', 'sold', 'deceased', 'fora', 'rebanho'];
const filtro = computed(() => {
  const status = typeof route.query.status === 'string' ? route.query.status : '';
  return filtrosValidos.includes(status) ? status : 'todos';
});
const quadrante = ref(typeof route.query.quadrant === 'string' ? route.query.quadrant : 'todos');
const filtroReprodutivo = computed(() => (
  route.query.reproductive_status === 'true' || route.query.reproductive_status === 'false'
    ? route.query.reproductive_status
    : ''
));
const filtroNascimento = computed(() => route.query.with_birth === 'true');
const alertaProducao = computed(() => route.query.alert === 'below-average');

// Filtros Touros
const buscaTouro = ref('');
const filtroTouroAtivo = ref('todos');

const filtros = [
  { valor: 'todos', rotulo: 'Todos' },
  { valor: 'active', rotulo: 'Ativos' },
  { valor: 'inactive', rotulo: 'Inativos' },
  { valor: 'sold', rotulo: 'Vendidos' },
  { valor: 'deceased', rotulo: 'Óbito' },
  { valor: 'fora', rotulo: 'Fora do rebanho' },
  { valor: 'rebanho', rotulo: 'No rebanho' },
];

const ultimaMovimentacao = computed(() => ultimaMovimentacaoPorAnimal(movimentacoes.value));
const estabuloAtual = (animalId) => nomeEstabulo(
  quadrantes.value,
  ultimaMovimentacao.value.get(String(animalId))?.quadrant
);

const nomeRaca = (breedId) => {
  const id = idRelacao(breedId);
  return breeds.value.find((item) => String(item.id) === String(id))?.name || '—';
};

const porSituacao = (lista, valor) => {
  if (valor === 'todos') return lista;
  if (valor === 'fora') return lista.filter((a) => !situacao(a.status).noRebanho);
  if (valor === 'rebanho') return lista.filter((a) => situacao(a.status).noRebanho);
  return lista.filter((a) => situacao(a.status).valor === valor);
};

const porQuadrante = (lista) => quadrante.value === 'todos'
  ? lista
  : lista.filter((animal) => String(idRelacao(
    ultimaMovimentacao.value.get(String(animal.id))?.quadrant
  )) === quadrante.value);

const animaisNoEstabulo = computed(() => porQuadrante(animals.value));
const ordenhasDoMes = computed(() => ordenhasDoMesAtual(ordenhas.value));
const metricasDeProducao = computed(() =>
  metricasProducaoPorAnimal(animaisNoEstabulo.value, ordenhasDoMes.value)
);
const animaisAbaixoDaMedia = computed(() => new Set(
  metricasDeProducao.value.abaixoDaMedia.map((item) => String(item.animal.id))
));
const abaixoDaMedia = (animal) => animaisAbaixoDaMedia.value.has(String(animal.id));

const porIndicadores = (lista) => lista.filter((animal) => {
  if (filtroReprodutivo.value && String(Boolean(animal.reproductive_status)) !== filtroReprodutivo.value) return false;
  return !filtroNascimento.value || Boolean(idRelacao(animal.birth));
});

const contar = (valor) => {
  const lista = porSituacao(porIndicadores(porQuadrante(animals.value)), valor);
  return alertaProducao.value ? lista.filter(abaixoDaMedia).length : lista.length;
};

const linkFiltro = (valor) => ({
  name: 'animal-list',
  query: {
    ...(valor !== 'todos' ? { status: valor } : {}),
    ...(quadrante.value !== 'todos' ? { quadrant: quadrante.value } : {}),
    ...(filtroReprodutivo.value ? { reproductive_status: filtroReprodutivo.value } : {}),
    ...(filtroNascimento.value ? { with_birth: 'true' } : {}),
    ...(alertaProducao.value ? { alert: 'below-average' } : {}),
  },
});

const visiveis = computed(() => {
  const termo = busca.value.trim().toLowerCase();
  const lista = porSituacao(porIndicadores(porQuadrante(animals.value)), filtro.value).filter((animal) => {
    if (!termo) return true;
    return (
      String(animal.register_number ?? '').includes(termo) ||
      String(animal.name ?? '').toLowerCase().includes(termo)
    );
  });
  return alertaProducao.value ? lista.filter(abaixoDaMedia) : lista;
});

const tourosVisiveis = computed(() => {
  const termo = buscaTouro.value.trim().toLowerCase();
  return bulls.value.filter((bull) => {
    if (filtroTouroAtivo.value === 'ativos' && !bull.active) return false;
    if (filtroTouroAtivo.value === 'inativos' && bull.active) return false;
    if (!termo) return true;
    return (
      String(bull.register_number ?? '').includes(termo) ||
      String(bull.name ?? '').toLowerCase().includes(termo) ||
      nomeRaca(bull.breed).toLowerCase().includes(termo)
    );
  });
});

const limparFiltros = () => {
  busca.value = '';
  quadrante.value = 'todos';
  router.replace({ name: 'animal-list', query: {} });
};

const limparFiltrosTouro = () => {
  buscaTouro.value = '';
  filtroTouroAtivo.value = 'todos';
};

watch(() => route.query.aba, (value) => {
  if (value === 'touros' || value === 'rebanho') abaAtiva.value = value;
});

watch(abaAtiva, (value) => {
  const nextAba = value === 'touros' ? 'touros' : undefined;
  if (route.query.aba === nextAba) return;
  router.replace({ query: { ...route.query, aba: nextAba } });
});

watch(() => route.query.quadrant, (value) => {
  quadrante.value = typeof value === 'string' ? value : 'todos';
});

watch(quadrante, (value) => {
  const nextQuadrant = value === 'todos' ? undefined : value;
  if (route.query.quadrant === nextQuadrant) return;
  router.replace({
    query: {
      ...route.query,
      quadrant: nextQuadrant,
    },
  });
});

const normalizeList = (data) => (Array.isArray(data) ? data : data?.results || []);

const loadAnimals = async () => {
  try {
    const response = await api.get('animals/');
    animals.value = normalizeList(response.data);
  } catch (error) {
    console.error('Erro ao carregar animais:', error);
  } finally {
    loading.value = false;
  }
};

const loadBulls = async () => {
  loadingBulls.value = true;
  try {
    const response = await api.getBulls();
    bulls.value = normalizeList(response.data);
  } catch (error) {
    console.error('Erro ao carregar touros:', error);
  } finally {
    loadingBulls.value = false;
  }
};

const loadBreeds = async () => {
  try {
    const response = await api.get('breeds/');
    breeds.value = normalizeList(response.data);
  } catch (error) {
    console.error('Erro ao carregar raças:', error);
  }
};

const loadQuadrants = async () => {
  try {
    const response = await api.getQuadrants();
    quadrantes.value = normalizeList(response.data);
  } catch (error) {
    console.error('Erro ao carregar estábulos para filtrar o rebanho:', error);
  }
};

const loadMovements = async () => {
  try {
    const response = await api.get('animal_movements/');
    movimentacoes.value = normalizeList(response.data);
  } catch (error) {
    console.error('Erro ao carregar movimentações do rebanho:', error);
  }
};

const loadMilkHistory = async () => {
  carregandoProducaoLeite.value = true;
  erroProducaoLeite.value = '';
  try {
    const records = [];
    const visited = new Set();
    let url = 'milk_production_history/';
    while (url) {
      if (visited.has(url)) throw new Error('A paginação das ordenhas retornou uma página repetida.');
      visited.add(url);
      const response = await api.get(url);
      const data = response.data;
      const rows = Array.isArray(data) ? data : data?.results;
      if (!Array.isArray(rows)) throw new Error('A API retornou um formato inesperado para o histórico de ordenha.');
      records.push(...rows);
      url = Array.isArray(data) ? null : data.next || null;
    }
    ordenhas.value = records;
  } catch (error) {
    console.error('Erro ao carregar ordenhas para os alertas de produção:', error);
    erroProducaoLeite.value = apiErrorMessage(error, 'Não foi possível carregar as médias de produção dos animais.');
  } finally {
    carregandoProducaoLeite.value = false;
  }
};

const excluirAnimal = async (animal) => {
  const ok = await confirmar({
    titulo: `Excluir ${animal.name || `#${animal.register_number}`}?`,
    texto: 'O cadastro e os históricos vinculados a este bovino serão removidos permanentemente.',
    acao: 'Excluir bovino',
  });
  if (!ok) return;
  erroAcao.value = '';
  try {
    await api.deleteAnimal(animal.id);
    await loadAnimals();
  } catch (error) {
    console.error('Erro ao excluir bovino:', error);
    erroAcao.value = apiErrorMessage(error, 'Não foi possível excluir o bovino.');
  }
};

const excluirTouro = async (bull) => {
  const ok = await confirmar({
    titulo: `Excluir o touro ${bull.name || `#${bull.register_number}`}?`,
    texto: 'Esta ação remove o cadastro do reprodutor.',
    acao: 'Excluir touro',
  });
  if (!ok) return;
  erroAcao.value = '';
  try {
    await api.deleteBull(bull.id);
    await loadBulls();
  } catch (error) {
    console.error('Erro ao excluir touro:', error);
    erroAcao.value = apiErrorMessage(error, 'Não foi possível excluir o touro.');
  }
};

onMounted(() => {
  loadAnimals();
  loadBulls();
  loadBreeds();
  loadQuadrants();
  loadMovements();
  loadMilkHistory();
});

const viewDetails = (id) => {
  router.push({ name: 'animal-detail', params: { id } });
};

const viewMilkDetails = (id) => {
  router.push({ name: 'animal-detail', params: { id }, query: { tab: 'leite' } });
};
</script>

<style scoped>
.animal-filters {
  margin-bottom: 14px;
  overflow: hidden;
}

.animal-filters__heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 20px 12px;
}

.animal-filter-tabs {
  display: flex;
  min-width: 0;
  overflow-x: auto;
  border-top: 1px solid var(--line);
  scrollbar-width: thin;
}

.animal-filter-tab {
  position: relative;
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
  gap: 8px;
  min-height: 48px;
  padding: 0 16px;
  border-right: 1px solid var(--line);
  color: var(--text-2);
  font-size: var(--fs-sm);
  font-weight: 500;
  text-decoration: none;
  white-space: nowrap;
}

.animal-filter-tab:hover,
.animal-filter-tab.is-active {
  background: var(--surface-2);
  color: var(--text);
  text-decoration: none;
}

.animal-filter-tab.is-active::after {
  position: absolute;
  right: 12px;
  bottom: 0;
  left: 12px;
  height: 2px;
  border-radius: 2px 2px 0 0;
  background: var(--accent);
  content: '';
}

.animal-filter-tab .count {
  min-width: 22px;
  padding: 2px 6px;
  border-radius: var(--r-full);
  background: var(--surface-3);
  color: var(--text-3);
  font-family: var(--font-mono);
  font-size: var(--fs-xs);
  text-align: center;
}

.animal-filter-tab.is-active .count {
  background: var(--accent-soft);
  color: var(--accent);
}

.animal-list__quadrant { width: min(250px, 100%); }

.animal-list__status {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
}

.animal-list__production-alert {
  padding: 4px 8px;
  border: 1px solid var(--warn-line);
  font: inherit;
  font-size: var(--fs-xs);
  cursor: pointer;
  white-space: nowrap;
}

.rodape-tabela {
  margin-top: 12px;
  color: var(--text-3);
  font-size: var(--fs-sm);
}

@media (max-width: 600px) {
  .animal-filters__heading { padding-inline: 14px; }
  .animal-filter-tab { padding-inline: 12px; }
  .animal-list__quadrant { width: 100%; }
}
</style>
