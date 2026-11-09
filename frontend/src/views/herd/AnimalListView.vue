<template>
  <AppShell>
    <div class="page page--wide animal-list-page">
      <PageHeader
        titulo="Animais"
        descricao="Consulte e filtre os bovinos do rebanho."
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

      <section class="toolbar animal-list-toolbar" aria-label="Busca e filtros adicionais">
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

        <span class="animal-list-toolbar__count">{{ visiveis.length }} resultado(s)</span>
      </section>

      <div class="card">
        <div v-if="loading" class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Buscando registros...
        </div>

        <div v-else-if="animals.length === 0" class="empty">
          <AppIcon name="animal" :size="30" />
          <p class="empty__title">Nenhum bovino cadastrado</p>
          <p class="empty__desc">Cadastre um bovino para começar a organizar o rebanho.</p>
          <div class="row">
            <RouterLink to="/animais/novo" class="btn btn--primary">Cadastrar bovino</RouterLink>
          </div>
        </div>

        <div v-else-if="visiveis.length === 0" class="empty">
          <AppIcon name="search" :size="30" />
          <p class="empty__title">Nada encontrado</p>
          <p class="empty__desc">Nenhum animal corresponde a esta busca ou filtro.</p>
          <button class="btn" @click="limparFiltros">Limpar filtros</button>
        </div>

        <div v-else class="table-wrap">
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
                <td class="cell-strong">{{ animal.name || '—' }}</td>
                <td>{{ estabuloAtual(animal.id) }}</td>
                <td>
                  <span class="badge" :class="badgeSituacao(animal.status)">
                    <span class="badge__dot"></span>
                    {{ rotuloSituacao(animal.status) }}
                  </span>
                </td>
                <td class="cell-actions">
                  <button class="btn btn--sm" @click="viewDetails(animal.id)">Ver ficha</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <p v-if="visiveis.length" class="rodape-tabela">
        {{ visiveis.length }} de {{ animals.length }} animais
      </p>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { badgeSituacao, rotuloSituacao, situacao } from '@/utils/statusUtils';
import { idRelacao, ultimaMovimentacaoPorAnimal, nomeEstabulo } from '@/utils/animalMovementUtils';

const router = useRouter();
const route = useRoute();
const animals = ref([]);
const quadrantes = ref([]);
const movimentacoes = ref([]);
const loading = ref(true);

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

const porIndicadores = (lista) => lista.filter((animal) => {
  if (filtroReprodutivo.value && String(Boolean(animal.reproductive_status)) !== filtroReprodutivo.value) return false;
  return !filtroNascimento.value || Boolean(idRelacao(animal.birth));
});

const contar = (valor) => porSituacao(porIndicadores(porQuadrante(animals.value)), valor).length;

const linkFiltro = (valor) => ({
  name: 'animal-list',
  query: {
    ...(valor !== 'todos' ? { status: valor } : {}),
    ...(quadrante.value !== 'todos' ? { quadrant: quadrante.value } : {}),
    ...(filtroReprodutivo.value ? { reproductive_status: filtroReprodutivo.value } : {}),
    ...(filtroNascimento.value ? { with_birth: 'true' } : {}),
  },
});

const visiveis = computed(() => {
  const termo = busca.value.trim().toLowerCase();
  return porSituacao(porIndicadores(porQuadrante(animals.value)), filtro.value).filter((animal) => {
    if (!termo) return true;
    return (
      String(animal.register_number ?? '').includes(termo) ||
      String(animal.name ?? '').toLowerCase().includes(termo)
    );
  });
});

const limparFiltros = () => {
  busca.value = '';
  quadrante.value = 'todos';
  router.replace({ name: 'animal-list', query: {} });
};

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

const loadAnimals = async () => {
  try {
    const response = await api.get('animals/');
    if (Array.isArray(response.data)) {
      animals.value = response.data;
    } else if (response.data && response.data.results) {
      animals.value = response.data.results;
    }
  } catch (error) {
    console.error("Erro ao carregar animais:", error);
  } finally {
    loading.value = false;
  }
};

const loadQuadrants = async () => {
  try {
    const response = await api.getQuadrants();
    const data = response.data;
    quadrantes.value = Array.isArray(data) ? data : data?.results || [];
  } catch (error) {
    console.error('Erro ao carregar estábulos para filtrar o rebanho:', error);
  }
};

const loadMovements = async () => {
  try {
    const response = await api.get('animal_movements/');
    const data = response.data;
    movimentacoes.value = Array.isArray(data) ? data : data?.results || [];
  } catch (error) {
    console.error('Erro ao carregar movimentações do rebanho:', error);
  }
};

onMounted(() => {
  loadAnimals();
  loadQuadrants();
  loadMovements();
});

const viewDetails = (id) => {
  router.push({ name: 'animal-detail', params: { id } });
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

.animal-list-toolbar {
  align-items: flex-end;
  margin-bottom: 12px;
}

.animal-list__quadrant { width: min(250px, 100%); }

.animal-list-toolbar__count {
  margin-left: auto;
  padding-bottom: 9px;
  color: var(--text-3);
  font-size: var(--fs-sm);
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
  .animal-list-toolbar > .search,
  .animal-list__quadrant { width: 100%; }
  .animal-list-toolbar__count { margin-left: 0; padding-bottom: 0; }
}
</style>
