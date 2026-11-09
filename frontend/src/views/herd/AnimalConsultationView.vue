<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Consultar animais"
        descricao="Busque por nome, número de registro, situação e estábulo atual."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <p v-if="error" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ error }}</span>
      </p>

      <div class="toolbar">
        <label class="search">
          <AppIcon name="search" :size="16" />
          <input
            v-model="searchQuery"
            class="input"
            type="search"
            placeholder="Buscar por nome, ID ou número de registro"
            aria-label="Buscar animal"
          >
        </label>

        <select v-model="filterStatus" class="select select--filtro" aria-label="Filtrar por situação">
          <option value="">Todos os status</option>
          <option value="active">Ativo</option>
          <option value="inactive">Inativo</option>
          <option value="sold">Vendido</option>
          <option value="deceased">Óbito</option>
        </select>

        <select v-model="filterQuadrant" class="select select--filtro" aria-label="Filtrar por estábulo">
          <option value="">Todos os estábulos</option>
          <option v-for="quad in quadrants" :key="quad.id" :value="quad.id">{{ quad.name }}</option>
        </select>

      </div>

      <!-- Lista à esquerda, ficha à direita: escolher um animal não faz mais
           o painel de detalhes brotar embaixo da lista, fora da vista. -->
      <div class="consulta">
        <section class="card consulta__lista">
          <header class="card__head">
            <h2 class="card__title">Resultados</h2>
            <span class="badge">{{ filteredAnimals.length }}</span>
          </header>

          <div v-if="filteredAnimals.length === 0" class="empty">
            <AppIcon name="search" :size="28" />
            <p class="empty__desc">Nenhum animal encontrado com esses critérios.</p>
          </div>

          <div v-else class="list">
            <button
              v-for="animal in filteredAnimals"
              :key="animal.id"
              class="list__item item-animal"
              :class="{ 'is-selected': selectedAnimalId === animal.id }"
              @click="selectAnimal(animal)"
            >
              <span class="list__main">
                <span class="icon-tile"><AppIcon name="animal" :size="16" /></span>
                <span>
                  <span class="list__title">{{ animal.name }}</span>
                  <span class="list__sub mono">#{{ animal.register_number }} · {{ animal.quadrant_name }}</span>
                </span>
              </span>
              <span class="badge" :class="badgeStatus(animal.status)">{{ labelStatus(animal.status) }}</span>
            </button>
          </div>
        </section>

        <section class="card consulta__ficha">
          <template v-if="selectedAnimal">
            <header class="card__head">
              <div>
                <h2 class="card__title">{{ selectedAnimal.name }}</h2>
                <p class="card__desc mono">Brinco #{{ selectedAnimal.register_number }}</p>
              </div>
              <button class="btn btn--icon" aria-label="Fechar ficha" @click="selectedAnimalId = null">
                <AppIcon name="close" :size="16" />
              </button>
            </header>

            <div class="card__body stack-24">
              <div>
                <h3 class="bloco__titulo">Dados básicos</h3>
                <div class="kv">
                  <div class="kv__row"><span class="kv__key">Raça</span><span class="kv__val">{{ selectedAnimal.breed_name || 'Não informado' }}</span></div>
                  <div class="kv__row"><span class="kv__key">Estábulo atual</span><span class="kv__val">{{ selectedAnimal.quadrant_name }}</span></div>
                  <div class="kv__row"><span class="kv__key">Escore</span><span class="kv__val mono">{{ selectedAnimal.score }}</span></div>
                  <div class="kv__row"><span class="kv__key">Status reprodutivo</span><span class="kv__val">{{ selectedAnimal.reproductive_status ? 'Ativo' : 'Inativo' }}</span></div>
                </div>
              </div>

              <div>
                <h3 class="bloco__titulo">Saúde</h3>
                <div class="kv">
                  <div class="kv__row"><span class="kv__key">Última pesagem</span><span class="kv__val mono">{{ selectedAnimal.last_weighing_date ? formatDate(selectedAnimal.last_weighing_date) : 'Sem registros' }}</span></div>
                  <div class="kv__row"><span class="kv__key">Última vacinação</span><span class="kv__val mono">{{ selectedAnimal.last_vaccination_date ? formatDate(selectedAnimal.last_vaccination_date) : 'Sem registros' }}</span></div>
                  <div class="kv__row"><span class="kv__key">Próxima vacinação</span><span class="kv__val mono">{{ selectedAnimal.next_vaccination_date ? formatDate(selectedAnimal.next_vaccination_date) : 'Sem agendamento' }}</span></div>
                </div>
              </div>

              <div>
                <h3 class="bloco__titulo">Produção</h3>
                <div class="kv">
                  <div class="kv__row"><span class="kv__key">Última ordenha</span><span class="kv__val mono">{{ selectedAnimal.last_milk_production ? `${selectedAnimal.last_milk_production} L` : 'Sem registros' }}</span></div>
                  <div class="kv__row"><span class="kv__key">Data da coleta</span><span class="kv__val mono">{{ selectedAnimal.last_milk_date ? formatDate(selectedAnimal.last_milk_date) : 'Sem registros' }}</span></div>
                </div>
              </div>
            </div>

            <footer class="card__foot">
              <button class="btn btn--primary" @click="goToAnimalProfile">
                Ver ficha completa
                <AppIcon name="arrow-right" :size="15" />
              </button>
            </footer>
          </template>

          <div v-else class="empty">
            <AppIcon name="clipboard" :size="30" />
            <p class="empty__title">Nenhum animal selecionado</p>
            <p class="empty__desc">Escolha um animal na lista para ver a ficha resumida.</p>
          </div>
        </section>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { painelDoPapel } from '@/services/auth';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { badgeSituacao, rotuloSituacao } from '@/utils/statusUtils';
import { idRelacao, nomeEstabulo, ultimaMovimentacaoPorAnimal } from '@/utils/animalMovementUtils';
import { apiErrorMessage } from '@/utils/apiError';

const router = useRouter();
const painel = computed(() => painelDoPapel());

// Dados
const animals = ref([]);
const quadrants = ref([]);
const error = ref('');

// Filtros
const searchQuery = ref('');
const filterStatus = ref('');
const filterQuadrant = ref('');
const selectedAnimalId = ref(null);

// Computed
const filteredAnimals = computed(() => {
  return animals.value.filter(animal => {
    const termo = searchQuery.value.trim().toLowerCase();
    const matchSearch = !termo ||
      String(animal.name ?? '').toLowerCase().includes(termo) ||
      String(animal.register_number ?? '').includes(searchQuery.value) ||
      String(animal.id ?? '').includes(searchQuery.value);

    const matchStatus = !filterStatus.value || animal.status === filterStatus.value;
    const matchQuadrant = !filterQuadrant.value || String(animal.quadrant_id) === String(filterQuadrant.value);
    return matchSearch && matchStatus && matchQuadrant;
  });
});

const selectedAnimal = computed(() => {
  return animals.value.find(a => a.id === selectedAnimalId.value) || null;
});

const badgeStatus = badgeSituacao;
const labelStatus = rotuloSituacao;

// Métodos
const loadInitialData = async () => {
  error.value = '';
  try {
    const [animalsRes, quadrantsRes, breedsRes, movementsRes, weightsRes, milkRes, vaccinesRes] = await Promise.all([
      api.getAnimals(),
      api.getQuadrants(),
      api.get('breeds/'),
      api.get('animal_movements/'),
      api.get('weight_history/'),
      api.get('milk_production_history/'),
      api.get('vaccinations/'),
    ]);
    const rows = (response) => {
      const data = response.data;
      if (Array.isArray(data)) return data;
      if (Array.isArray(data?.results)) return data.results;
      throw new Error('A API retornou um formato de lista inesperado.');
    };
    const quadrantList = rows(quadrantsRes);
    const breedList = rows(breedsRes);
    quadrants.value = quadrantList;
    const latestMovements = ultimaMovimentacaoPorAnimal(rows(movementsRes));
    const latestByAnimal = (records, dateField) => {
      const latest = new Map();
      for (const record of records) {
        const animalId = idRelacao(record.animal);
        const current = latest.get(String(animalId));
        if (!current || String(record[dateField]) > String(current[dateField])) {
          latest.set(String(animalId), record);
        }
      }
      return latest;
    };
    const latestWeights = latestByAnimal(rows(weightsRes), 'weighing_date');
    const latestMilk = latestByAnimal(rows(milkRes), 'production_date');
    const latestVaccines = latestByAnimal(rows(vaccinesRes), 'vaccination_date');
    animals.value = rows(animalsRes).map((animal) => {
      const movement = latestMovements.get(String(animal.id));
      const weight = latestWeights.get(String(animal.id));
      const milk = latestMilk.get(String(animal.id));
      const vaccine = latestVaccines.get(String(animal.id));
      const breedId = idRelacao(animal.breed);
      return {
        ...animal,
        quadrant_id: movement ? idRelacao(movement.quadrant) : null,
        quadrant_name: nomeEstabulo(quadrantList, movement?.quadrant),
        breed_name: breedList.find((breed) => String(breed.id) === String(breedId))?.name || '—',
        last_weighing_date: weight?.weighing_date || null,
        last_vaccination_date: vaccine?.vaccination_date || null,
        next_vaccination_date: vaccine?.next_vaccination_date || null,
        last_milk_production: milk?.milk_production || null,
        last_milk_date: milk?.production_date || null,
      };
    });
  } catch (err) {
    console.error('Erro ao carregar dados:', err);
    error.value = apiErrorMessage(err, 'Não foi possível carregar os dados de consulta do rebanho.');
  }
};

const selectAnimal = (animal) => {
  selectedAnimalId.value = animal.id;
};

const formatDate = (dateString) => {
  if (!dateString) return 'Sem registros';
  return new Date(`${dateString}T00:00:00`).toLocaleDateString('pt-BR');
};

const goToAnimalProfile = () => {
  if (selectedAnimal.value) {
    router.push(`/animal/${selectedAnimal.value.id}`);
  }
};

onMounted(() => {
  loadInitialData();
});
</script>

<style scoped>
.select--filtro { width: auto; min-width: 170px; flex: none; }

.consulta {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 0.9fr);
  gap: 16px;
  align-items: start;
}

.consulta__lista { max-height: 70vh; overflow-y: auto; }
.consulta__lista .card__head { position: sticky; top: 0; z-index: 1; background: var(--surface); }

.item-animal {
  width: 100%;
  border-left: 2px solid transparent;
  background: none;
  font: inherit;
  color: inherit;
  text-align: left;
}

.item-animal.is-selected {
  border-left-color: var(--accent);
  background: var(--accent-soft);
}

.bloco__titulo {
  margin-bottom: 4px;
  color: var(--text-2);
  font-size: var(--fs-xs);
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

@media (max-width: 1000px) {
  .consulta { grid-template-columns: 1fr; }
  .consulta__lista { max-height: none; }
}
</style>
