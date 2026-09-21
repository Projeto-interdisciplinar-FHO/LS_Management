<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Animais"
        descricao="Rebanho cadastrado, com brinco, lotação e situação de cada cabeça."
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

      <div class="toolbar">
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

        <div class="segmented" role="group" aria-label="Filtrar por situação">
          <button
            v-for="opcao in filtros"
            :key="opcao.valor"
            class="segmented__item"
            :class="{ 'is-active': filtro === opcao.valor }"
            @click="filtro = opcao.valor"
          >
            {{ opcao.rotulo }}
            <span class="count">{{ contar(opcao.valor) }}</span>
          </button>
        </div>
      </div>

      <div class="card">
        <div v-if="loading" class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Buscando registros...
        </div>

        <div v-else-if="animals.length === 0" class="empty">
          <AppIcon name="animal" :size="30" />
          <p class="empty__title">Nenhum animal cadastrado</p>
          <p class="empty__desc">Cadastre a primeira cabeça para começar o controle do rebanho.</p>
          <RouterLink to="/animais/novo" class="btn btn--primary">Cadastrar animal</RouterLink>
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
                <th>Sexo</th>
                <th>Situação</th>
                <th class="cell-actions">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="animal in visiveis" :key="animal.id">
                <td class="mono">#{{ animal.register_number }}</td>
                <td class="cell-strong">{{ animal.name || '—' }}</td>
                <td>{{ sexo(animal) }}</td>
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
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { badgeSituacao, rotuloSituacao, situacao } from '@/utils/statusUtils';

const router = useRouter();
const animals = ref([]);
const loading = ref(true);

// A lista vinha inteira, sem busca. Com o rebanho crescendo, achar um brinco
// virava rolagem. O filtro é local: não muda nenhuma chamada de API.
const busca = ref('');
const filtro = ref('todos');

// Os filtros seguem o `status` do backend, que tem cinco opções, e não o
// booleano `active` — assim "doente" deixa de ser invisível na listagem.
const filtros = [
  { valor: 'todos', rotulo: 'Todos' },
  { valor: 'ativo', rotulo: 'Ativos' },
  { valor: 'doente', rotulo: 'Doentes' },
  { valor: 'fora', rotulo: 'Fora do rebanho' },
];

const sexo = (animal) => (animal.sex === 'm' || animal.sex === 'M' ? 'Macho' : 'Fêmea');

const porSituacao = (lista, valor) => {
  if (valor === 'todos') return lista;
  if (valor === 'fora') return lista.filter((a) => !situacao(a.status).noRebanho);
  return lista.filter((a) => situacao(a.status).valor === valor);
};

const contar = (valor) => porSituacao(animals.value, valor).length;

const visiveis = computed(() => {
  const termo = busca.value.trim().toLowerCase();
  return porSituacao(animals.value, filtro.value).filter((animal) => {
    if (!termo) return true;
    return (
      String(animal.register_number ?? '').includes(termo) ||
      String(animal.name ?? '').toLowerCase().includes(termo)
    );
  });
});

const limparFiltros = () => {
  busca.value = '';
  filtro.value = 'todos';
};

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

onMounted(() => {
  loadAnimals();
});

const viewDetails = (id) => {
  router.push({ name: 'animal-detail', params: { id } });
};
</script>

<style scoped>
.rodape-tabela {
  margin-top: 12px;
  color: var(--text-3);
  font-size: var(--fs-sm);
}
</style>
