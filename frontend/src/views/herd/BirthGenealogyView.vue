<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Nascimento e genealogia"
        descricao="Registre nascimentos e consulte a ascendência direta disponível na API."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <p class="alert alert--info" role="status">
        <AppIcon name="info" :size="16" />
        <span>A API registra data, peso e ocorrência do nascimento; quando há inseminação vinculada, também é possível consultar mãe e pai. O esquema não contém relações de avós.</span>
      </p>
      <p v-if="error" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ error }}</span>
      </p>
      <p v-if="notice" class="alert alert--warn" role="status">
        <AppIcon name="alert" :size="16" />
        <span>{{ notice }}</span>
      </p>

      <section class="card">
        <header class="card__head">
          <div>
            <h2 class="card__title">Registrar nascimento</h2>
            <p class="card__desc">O registro será associado ao bovino escolhido após ser criado.</p>
          </div>
        </header>

        <form class="card__body stack" @submit.prevent="saveBirth">
          <div class="grid grid--2">
            <div class="field">
              <label class="field__label" for="calf">Bovino</label>
              <select id="calf" v-model.number="form.animalId" class="select" required :disabled="loading || saving || Boolean(pendingLink)">
                <option value="" disabled>Selecione um bovino sem nascimento vinculado...</option>
                <option v-for="animal in animalsWithoutBirth" :key="animal.id" :value="animal.id">
                  {{ animal.name }} · #{{ animal.register_number }}
                </option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="birth-occurrence">Ocorrência</label>
              <select id="birth-occurrence" v-model.number="form.occurrence" class="select" required :disabled="loading || saving">
                <option value="" disabled>Selecione...</option>
                <option v-for="occurrence in occurrences" :key="occurrence.id" :value="occurrence.id">{{ occurrence.description }}</option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="birth-date">Data do nascimento</label>
              <input id="birth-date" v-model="form.date" class="input" type="date" required :disabled="saving">
            </div>
            <div class="field">
              <label class="field__label" for="birth-weight">Peso ao nascer (kg)</label>
              <input id="birth-weight" v-model.number="form.weight" class="input" type="number" min="0" step="0.01" required :disabled="saving">
            </div>
            <div class="field span-full">
              <label class="field__label" for="birth-insemination">Inseminação relacionada (opcional)</label>
              <select id="birth-insemination" v-model.number="form.insemination" class="select" :disabled="loading || saving">
                <option value="">Não informada</option>
                <option v-for="item in inseminations" :key="item.id" :value="item.id">
                  {{ inseminationLabel(item) }}
                </option>
              </select>
            </div>
          </div>

          <div v-if="pendingLink" class="alert alert--warn" role="status">
            Nascimento {{ pendingLink.birthId }} criado, mas ainda não foi vinculado ao bovino.
            <button type="button" class="btn btn--sm" :disabled="saving" @click="retryLink">Tentar vincular</button>
          </div>

          <footer class="row row--between">
            <span class="text-muted">{{ animalsWithoutBirth.length }} bovino(s) sem nascimento vinculado</span>
            <button type="submit" class="btn btn--primary" :disabled="loading || saving || !ready">
              {{ saving ? 'Salvando...' : pendingLink ? 'Vínculo pendente' : 'Registrar nascimento' }}
            </button>
          </footer>
        </form>
      </section>

      <section class="card birth-list">
        <header class="card__head">
          <div>
            <h2 class="card__title">Nascimentos vinculados</h2>
            <p class="card__desc">Ascendência limitada aos dados de inseminação disponíveis.</p>
          </div>
          <span class="badge">{{ linkedBirths.length }}</span>
        </header>
        <div v-if="loading" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando nascimentos...</div>
        <div v-else-if="!linkedBirths.length" class="empty">
          <AppIcon name="dna" :size="28" />
          <p class="empty__desc">Nenhum nascimento está vinculado a um bovino.</p>
        </div>
        <div v-else class="table-wrap">
          <table class="table">
            <thead>
              <tr><th>Bovino</th><th>Data</th><th>Peso</th><th>Ocorrência</th><th>Mãe</th><th>Pai</th></tr>
            </thead>
            <tbody>
              <tr v-for="item in linkedBirths" :key="item.animal.id">
                <td class="cell-strong">{{ item.animal.name }} <span class="mono">#{{ item.animal.register_number }}</span></td>
                <td class="mono nowrap">{{ formatDate(item.birth.date) }}</td>
                <td class="mono">{{ item.birth.weight }} kg</td>
                <td>{{ occurrenceName(item.birth.occurrence) }}</td>
                <td>{{ parentName(item.insemination?.mother, animals) }}</td>
                <td>{{ parentName(item.insemination?.father, bulls) }}</td>
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
const births = ref([]);
const occurrences = ref([]);
const inseminations = ref([]);
const bulls = ref([]);
const loading = ref(true);
const saving = ref(false);
const error = ref('');
const notice = ref('');
const pendingLink = ref(null);

function todayIso() {
  const date = new Date();
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

const form = ref({ animalId: '', occurrence: '', date: todayIso(), weight: '', insemination: '' });
const ready = computed(() => Boolean(
  form.value.animalId
  && form.value.occurrence
  && form.value.date
  && form.value.weight !== ''
  && Number(form.value.weight) >= 0
));
const animalsWithoutBirth = computed(() => animals.value.filter((animal) => !animal.birth));

const linkedBirths = computed(() => animals.value.flatMap((animal) => {
  const birthId = idRelacao(animal.birth);
  if (!birthId) return [];
  const birth = births.value.find((item) => String(item.id) === String(birthId));
  if (!birth) return [];
  const inseminationId = idRelacao(birth.insemination);
  return [{
    animal,
    birth,
    insemination: inseminations.value.find((item) => String(item.id) === String(inseminationId)) || null,
  }];
}));

function listFromResponse(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  throw new Error('A API retornou um formato de lista inesperado.');
}

function formatDate(value) {
  if (!value) return '—';
  return new Date(`${value}T00:00:00`).toLocaleDateString('pt-BR');
}

function occurrenceName(id) {
  return occurrences.value.find((item) => String(item.id) === String(idRelacao(id)))?.description || '—';
}

function parentName(id, list) {
  const parent = list.find((item) => String(item.id) === String(idRelacao(id)));
  return parent ? `${parent.name} · #${parent.register_number}` : 'Não informado';
}

function inseminationLabel(item) {
  return `Inseminação #${item.id} · ${formatDate(item.date)}`;
}

async function linkBirth(animalId, birthId) {
  await api.patch(`animals/${animalId}/`, { birth: birthId });
}

async function saveBirth() {
  if (!ready.value || saving.value || pendingLink.value) return;
  saving.value = true;
  error.value = '';
  notice.value = '';
  try {
    const response = await api.post('births/', {
      date: form.value.date,
      weight: Number(form.value.weight),
      occurrence: Number(form.value.occurrence),
      insemination: form.value.insemination ? Number(form.value.insemination) : null,
    });
    const birthId = response.data?.id;
    if (!birthId) throw new Error('O nascimento foi criado, mas a API não retornou o identificador.');
    try {
      await linkBirth(Number(form.value.animalId), birthId);
      form.value = { animalId: '', occurrence: '', date: todayIso(), weight: '', insemination: '' };
      await loadData();
    } catch (linkError) {
      pendingLink.value = { animalId: Number(form.value.animalId), birthId };
      notice.value = `O nascimento #${birthId} foi criado, mas o vínculo ao bovino falhou. Use “Tentar vincular”; não envie o formulário novamente.`;
      error.value = apiErrorMessage(linkError, 'Não foi possível vincular o nascimento ao bovino.');
    }
  } catch (saveError) {
    console.error('Erro ao registrar nascimento:', saveError);
    error.value = apiErrorMessage(saveError, 'Não foi possível registrar o nascimento.');
  } finally {
    saving.value = false;
  }
}

async function retryLink() {
  if (!pendingLink.value || saving.value) return;
  saving.value = true;
  error.value = '';
  try {
    await linkBirth(pendingLink.value.animalId, pendingLink.value.birthId);
    pendingLink.value = null;
    notice.value = '';
    form.value = { animalId: '', occurrence: '', date: todayIso(), weight: '', insemination: '' };
    await loadData();
  } catch (linkError) {
    console.error('Erro ao vincular nascimento:', linkError);
    error.value = apiErrorMessage(linkError, 'Não foi possível vincular o nascimento ao bovino.');
  } finally {
    saving.value = false;
  }
}

async function loadData() {
  loading.value = true;
  error.value = '';
  try {
    const [animalsResponse, birthsResponse, occurrencesResponse, inseminationsResponse, bullsResponse] = await Promise.all([
      api.getAnimals(),
      api.get('births/'),
      api.get('birth_occurrences/'),
      api.get('inseminations/'),
      api.get('bulls/'),
    ]);
    animals.value = listFromResponse(animalsResponse.data);
    births.value = listFromResponse(birthsResponse.data);
    occurrences.value = listFromResponse(occurrencesResponse.data);
    inseminations.value = listFromResponse(inseminationsResponse.data);
    bulls.value = listFromResponse(bullsResponse.data);
  } catch (loadError) {
    console.error('Erro ao carregar dados de nascimento e genealogia:', loadError);
    error.value = apiErrorMessage(loadError, 'Não foi possível carregar os dados de nascimento e genealogia.');
  } finally {
    loading.value = false;
  }
}

onMounted(loadData);
</script>

<style scoped>
.birth-list { margin-top: 20px; }
.row--between { justify-content: space-between; flex-wrap: wrap; }
</style>
