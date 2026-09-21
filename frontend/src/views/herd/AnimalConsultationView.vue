<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Consultar animais"
        descricao="Busque por brinco, nome ou filtre por quadrante e espécie."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

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

        <select v-model="filterStatus" class="select select--filtro" aria-label="Filtrar por status">
          <option value="">Todos os status</option>
          <option value="ativo">Ativo</option>
          <option value="doente">Doente</option>
          <option value="vendido">Vendido</option>
          <option value="obito">Óbito</option>
          <option value="inativo">Inativo</option>
        </select>

        <select v-model="filterQuadrant" class="select select--filtro" aria-label="Filtrar por quadrante">
          <option value="">Todos os quadrantes</option>
          <option v-for="quad in quadrants" :key="quad.id" :value="quad.id">{{ quad.name }}</option>
        </select>

        <select v-model="filterSpecie" class="select select--filtro" aria-label="Filtrar por espécie">
          <option value="">Todas as espécies</option>
          <option v-for="sp in species" :key="sp.id" :value="sp.id">{{ sp.name }}</option>
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
              <span class="badge" :class="badgeStatus(animal.status)">{{ animal.status || '—' }}</span>
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
                  <div class="kv__row"><span class="kv__key">Sexo</span><span class="kv__val">{{ selectedAnimal.sex === 'M' ? 'Macho' : 'Fêmea' }}</span></div>
                  <div class="kv__row"><span class="kv__key">Nascimento</span><span class="kv__val mono">{{ formatDate(selectedAnimal.birth_date) }}</span></div>
                  <div class="kv__row"><span class="kv__key">Espécie</span><span class="kv__val">{{ selectedAnimal.specie_name }}</span></div>
                  <div class="kv__row"><span class="kv__key">Raça</span><span class="kv__val">{{ selectedAnimal.breed_name || 'Não informado' }}</span></div>
                  <div class="kv__row"><span class="kv__key">Quadrante</span><span class="kv__val">{{ selectedAnimal.quadrant_name }}</span></div>
                  <div class="kv__row"><span class="kv__key">Propósito</span><span class="kv__val">{{ selectedAnimal.purpose_name || '—' }}</span></div>
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
                <div v-if="isFemaleAnimal(selectedAnimal)" class="kv">
                  <div class="kv__row"><span class="kv__key">Última ordenha</span><span class="kv__val mono">{{ selectedAnimal.last_milk_production ? `${selectedAnimal.last_milk_production} L` : 'Sem registros' }}</span></div>
                  <div class="kv__row"><span class="kv__key">Data da coleta</span><span class="kv__val mono">{{ selectedAnimal.last_milk_date ? formatDate(selectedAnimal.last_milk_date) : 'Sem registros' }}</span></div>
                </div>
                <p v-else class="text-subtle">Produção de leite disponível apenas para fêmeas.</p>
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

const router = useRouter();
const painel = computed(() => painelDoPapel());

// Dados
const animals = ref([]);
const quadrants = ref([]);
const species = ref([]);

// Filtros
const searchQuery = ref('');
const filterStatus = ref('');
const filterQuadrant = ref('');
const filterSpecie = ref('');
const selectedAnimalId = ref(null);

// Computed
const filteredAnimals = computed(() => {
  return animals.value.filter(animal => {
    const termo = searchQuery.value.toLowerCase();
    const matchSearch = !searchQuery.value ||
      String(animal.name ?? '').toLowerCase().includes(termo) ||
      String(animal.register_number ?? '').includes(searchQuery.value) ||
      String(animal.id ?? '').includes(searchQuery.value);

    const matchStatus = !filterStatus.value || animal.status === filterStatus.value;
    const matchQuadrant = !filterQuadrant.value || String(animal.quadrant_id) === String(filterQuadrant.value);
    const matchSpecie = !filterSpecie.value || String(animal.specie_id) === String(filterSpecie.value);

    return matchSearch && matchStatus && matchQuadrant && matchSpecie;
  });
});

const selectedAnimal = computed(() => {
  return animals.value.find(a => a.id === selectedAnimalId.value) || null;
});

const isFemaleAnimal = (animalData) => String(animalData?.sex || '').toLowerCase() === 'f';

const badgeStatus = (status) => {
  if (status === 'ativo') return 'badge--ok';
  if (status === 'doente') return 'badge--warn';
  if (status === 'obito') return 'badge--danger';
  return '';
};

// Métodos
const loadInitialData = async () => {
  try {
    const [animalsRes, quadrantsRes, speciesRes] = await Promise.all([
      api.get('animals/?limit=500'),
      api.get('quadrants/?limit=500'),
      api.get('species/?limit=500')
    ]);

    animals.value = (animalsRes.data.results || animalsRes.data).map(a => ({
      ...a,
      quadrant_id: a.quadrant,
      specie_id: a.specie
    }));

    quadrants.value = quadrantsRes.data.results || quadrantsRes.data;
    species.value = speciesRes.data.results || speciesRes.data;

    // Enriquece dados com nomes
    enrichAnimalsWithNames();
  } catch (err) {
    console.error('Erro ao carregar dados:', err);
  }
};

const enrichAnimalsWithNames = () => {
  animals.value = animals.value.map(animal => {
    const quadrant = quadrants.value.find(q => q.id === animal.quadrant_id);
    const specie = species.value.find(s => s.id === animal.specie_id);

    return {
      ...animal,
      quadrant_name: quadrant?.name || 'N/A',
      specie_name: specie?.name || 'N/A',
      breed_name: animal.breed_name || 'N/A'
    };
  });
};

const selectAnimal = (animal) => {
  selectedAnimalId.value = animal.id;
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('pt-BR');
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
