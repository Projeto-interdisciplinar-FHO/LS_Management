<template>
  <AppShell>
    <div class="page page--wide insemination-page">
      <PageHeader
        titulo="Inseminações"
        descricao="Registre o acasalamento e acompanhe o histórico reprodutivo do rebanho."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <p v-if="error" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ error }}</span>
      </p>
      <p v-if="notice" class="alert alert--ok" role="status">
        <AppIcon name="check-circle" :size="16" />
        <span>{{ notice }}</span>
      </p>

      <section class="card">
        <header class="card__head">
          <div class="insemination__heading">
            <span class="icon-tile icon-tile--info"><AppIcon name="dna" :size="18" /></span>
            <div>
              <h2 class="card__title">Registrar inseminação</h2>
              <p class="card__desc">Informe a matriz, o touro e a data do procedimento.</p>
            </div>
          </div>
          <span class="badge">{{ inseminations.length }} registros</span>
        </header>

        <form class="card__body stack" @submit.prevent="saveInsemination">
          <div v-if="!loading && (!animals.length || !bulls.length)" class="alert alert--warn" role="status">
            <AppIcon name="info" :size="16" />
            <span>
              {{ !animals.length ? 'Cadastre animais antes de lançar uma inseminação.' : 'Cadastre touros antes de lançar uma inseminação.' }}
            </span>
          </div>

          <div class="grid grid--3">
            <div class="field">
              <label class="field__label" for="insemination-mother">Matriz</label>
              <select id="insemination-mother" v-model.number="form.mother" class="select" required :disabled="loading || saving || !animals.length">
                <option value="" disabled>Selecione a matriz...</option>
                <option v-for="animal in animals" :key="animal.id" :value="animal.id">
                  {{ animal.name || 'Sem nome' }} · #{{ animal.register_number }}
                </option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="insemination-father">Touro</label>
              <select id="insemination-father" v-model.number="form.father" class="select" required :disabled="loading || saving || !bulls.length">
                <option value="" disabled>Selecione o touro...</option>
                <option v-for="bull in bulls" :key="bull.id" :value="bull.id">
                  {{ bull.name }} · #{{ bull.register_number }}
                </option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="insemination-date">Data da inseminação</label>
              <input id="insemination-date" v-model="form.date" class="input" type="date" required :disabled="saving">
            </div>
          </div>

          <footer class="row row--between">
            <span v-if="loading" class="text-muted" role="status">Carregando dados reprodutivos...</span>
            <span v-else class="text-muted">{{ animals.length }} matrizes · {{ bulls.length }} touros disponíveis</span>
            <button type="submit" class="btn btn--primary" :disabled="loading || saving || !animals.length || !bulls.length">
              {{ saving ? 'Salvando...' : 'Registrar inseminação' }}
            </button>
          </footer>
        </form>
      </section>

      <section class="card insemination__history">
        <header class="card__head">
          <div>
            <h2 class="card__title">Histórico reprodutivo</h2>
            <p class="card__desc">Inseminações cadastradas, da mais recente para a mais antiga.</p>
          </div>
          <span class="badge">{{ inseminations.length }}</span>
        </header>
        <div v-if="loading" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando inseminações...</div>
        <div v-else-if="!inseminations.length" class="empty">
          <AppIcon name="dna" :size="28" />
          <p class="empty__title">Sem inseminações registradas</p>
          <p class="empty__desc">Os lançamentos confirmados aparecerão aqui.</p>
        </div>
        <div v-else class="table-wrap">
          <table class="table">
            <thead>
              <tr><th>Data</th><th>Matriz</th><th>Touro</th></tr>
            </thead>
            <tbody>
              <tr v-for="item in orderedInseminations" :key="item.id">
                <td class="mono nowrap">{{ formatDate(item.date) }}</td>
                <td>
                  <RouterLink :to="{ name: 'animal-detail', params: { id: idRelacao(item.mother) } }" class="insemination__animal">
                    {{ animalName(item.mother) }}
                  </RouterLink>
                </td>
                <td>{{ bullName(item.father) }}</td>
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
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { painelDoPapel } from '@/services/auth';
import { idRelacao } from '@/utils/animalMovementUtils';
import { apiErrorMessage } from '@/utils/apiError';

const painel = computed(() => painelDoPapel());
const animals = ref([]);
const bulls = ref([]);
const inseminations = ref([]);
const loading = ref(true);
const saving = ref(false);
const error = ref('');
const notice = ref('');
const form = ref({ mother: '', father: '', date: todayIso() });

const orderedInseminations = computed(() =>
  [...inseminations.value].sort((a, b) => String(b.date).localeCompare(String(a.date)))
);

function todayIso() {
  const date = new Date();
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

function listFromResponse(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  throw new Error('A API retornou um formato de lista inesperado.');
}

function formatDate(value) {
  if (!value) return '—';
  return new Date(`${value}T00:00:00`).toLocaleDateString('pt-BR');
}

function animalName(animalRef) {
  const id = idRelacao(animalRef);
  const animal = animals.value.find((item) => String(item.id) === String(id));
  return animal ? `${animal.name || 'Sem nome'} · #${animal.register_number}` : 'Animal';
}

function bullName(bullRef) {
  const id = idRelacao(bullRef);
  const bull = bulls.value.find((item) => String(item.id) === String(id));
  return bull ? `${bull.name} · #${bull.register_number}` : 'Touro';
}

async function loadData() {
  loading.value = true;
  error.value = '';
  try {
    const [animalsResponse, bullsResponse, inseminationsResponse] = await Promise.all([
      api.getAnimals(),
      api.get('bulls/'),
      api.get('inseminations/'),
    ]);
    animals.value = listFromResponse(animalsResponse.data);
    bulls.value = listFromResponse(bullsResponse.data);
    inseminations.value = listFromResponse(inseminationsResponse.data);
  } catch (loadError) {
    console.error('Erro ao carregar dados de inseminação:', loadError);
    error.value = apiErrorMessage(loadError, 'Não foi possível carregar os dados de reprodução.');
  } finally {
    loading.value = false;
  }
}

async function saveInsemination() {
  if (saving.value) return;
  saving.value = true;
  error.value = '';
  notice.value = '';
  try {
    const response = await api.post('inseminations/', {
      mother: form.value.mother,
      father: form.value.father,
      date: form.value.date,
    });
    inseminations.value = [response.data, ...inseminations.value];
    notice.value = 'Inseminação registrada com sucesso.';
    form.value = { mother: '', father: '', date: todayIso() };
  } catch (saveError) {
    console.error('Erro ao registrar inseminação:', saveError);
    error.value = apiErrorMessage(saveError, 'Não foi possível registrar a inseminação.');
  } finally {
    saving.value = false;
  }
}

onMounted(loadData);
</script>

<style scoped>
.insemination__heading { display: flex; align-items: center; gap: 12px; }
.insemination__history { margin-top: 20px; }
.insemination__animal { color: var(--text); font-weight: 600; }
.insemination__animal:hover { color: var(--accent); }
</style>
