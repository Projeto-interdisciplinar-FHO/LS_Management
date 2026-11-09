<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        :titulo="isEdit ? 'Editar bovino' : 'Cadastrar bovino'"
        :descricao="isEdit ? 'Atualize os dados e registre uma movimentação se mudar o estábulo.' : 'Cadastre o bovino e registre sua lotação inicial.'"
        voltar-rotulo="Animais"
        voltar-para="/animais"
      />

      <p v-if="optionsError" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ optionsError }}</span>
      </p>
      <p v-if="formMessage" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ formMessage }}</span>
      </p>
      <p v-if="partialSuccess" class="alert alert--warn" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ partialSuccess }}</span>
      </p>

      <form class="stack-24" @submit.prevent="saveAnimal">
        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Identificação e classificação</h2>
              <p class="card__desc">Campos do cadastro bovino: identificação, raça, situação e escore.</p>
            </div>
          </header>

          <div class="card__body grid grid--2">
            <div class="field">
              <label class="field__label" for="nome">Nome</label>
              <input id="nome" v-model.trim="formData.name" class="input" type="text" maxlength="100" required>
            </div>

            <div class="field">
              <label class="field__label" for="registro">Número de registro</label>
              <input id="registro" v-model.number="formData.register_number" class="input" type="number" min="1" required>
            </div>

            <div class="field">
              <label class="field__label" for="raca">Raça</label>
              <select id="raca" v-model.number="formData.breed" class="select" required :disabled="loadingOptions">
                <option value="" disabled>{{ loadingOptions ? 'Carregando raças...' : 'Selecione uma raça...' }}</option>
                <option v-for="breed in breeds" :key="breed.id" :value="breed.id">{{ breed.name }}</option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="situacao">Situação</label>
              <select id="situacao" v-model="formData.status" class="select">
                <option v-for="status in SITUACOES" :key="status.valor" :value="status.valor">
                  {{ status.rotulo }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="escore">Escore</label>
              <input id="escore" v-model.number="formData.score" class="input" type="number" min="0" step="0.01" required>
            </div>

            <label class="field field--check">
              <input v-model="formData.reproductive_status" type="checkbox">
              <span class="field__label">Status reprodutivo ativo</span>
            </label>
          </div>
        </section>

        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Lotação inicial / movimentação</h2>
              <p class="card__desc">O estábulo atual é determinado pela movimentação mais recente do bovino.</p>
            </div>
          </header>

          <div class="card__body grid grid--2">
            <div class="field">
              <label class="field__label" for="estabulo">Estábulo</label>
              <select id="estabulo" v-model.number="formData.quadrant" class="select" required :disabled="loadingOptions">
                <option value="" disabled>{{ loadingOptions ? 'Carregando estábulos...' : 'Selecione um estábulo...' }}</option>
                <option v-for="quadrant in quadrants" :key="quadrant.id" :value="quadrant.id">{{ quadrant.name }}</option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="tipo-movimentacao">Tipo de movimentação</label>
              <select id="tipo-movimentacao" v-model.number="formData.movement_type" class="select" required :disabled="loadingOptions">
                <option value="" disabled>{{ loadingOptions ? 'Carregando tipos...' : 'Selecione um tipo...' }}</option>
                <option v-for="type in movementTypes" :key="type.id" :value="type.id">{{ type.name }}</option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="data-movimentacao">Data</label>
              <input id="data-movimentacao" v-model="formData.movement_date" class="input" type="date" required>
            </div>

            <div class="field">
              <label class="field__label" for="motivo-movimentacao">Motivo</label>
              <input id="motivo-movimentacao" v-model.trim="formData.movement_reason" class="input" type="text" required>
            </div>
          </div>

          <footer class="card__foot">
            <button type="button" class="btn" @click="$router.back()">Cancelar</button>
            <button
              v-if="movementPending"
              type="button"
              class="btn btn--primary"
              :disabled="loading"
              @click="retryMovement"
            >
              {{ loading ? 'Tentando novamente...' : 'Tentar salvar movimentação' }}
            </button>
            <button
              v-else
              type="submit"
              class="btn btn--primary"
              :disabled="loading || loadingOptions || loadingRecord || Boolean(partialSuccess)"
            >
              {{ loading ? 'Salvando...' : loadingRecord ? 'Carregando bovino...' : isEdit ? 'Salvar alterações' : 'Cadastrar bovino' }}
            </button>
          </footer>
        </section>
      </form>
    </div>
  </AppShell>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { SITUACOES } from '@/utils/statusUtils';
import { idRelacao, ultimaMovimentacaoPorAnimal } from '@/utils/animalMovementUtils';
import { apiErrorMessage } from '@/utils/apiError';

const route = useRoute();
const router = useRouter();

const isEdit = Boolean(route.params.id);
const loading = ref(false);
const loadingOptions = ref(true);
const loadingRecord = ref(false);
const optionsError = ref('');
const formMessage = ref('');
const partialSuccess = ref('');
const breeds = ref([]);
const quadrants = ref([]);
const movementTypes = ref([]);
const movementPending = ref(null);
const currentQuadrantId = ref(null);

function todayIso() {
  const date = new Date();
  const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
  return localDate.toISOString().slice(0, 10);
}

const formData = ref({
  name: '',
  register_number: '',
  breed: '',
  status: 'active',
  score: 0,
  reproductive_status: true,
  quadrant: '',
  movement_type: '',
  movement_date: todayIso(),
  movement_reason: 'Lotação inicial',
});

function listFromResponse(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  throw new Error('A API retornou um formato de lista inesperado.');
}

async function loadOptions() {
  optionsError.value = '';
  try {
    const [breedsResponse, quadrantsResponse, typesResponse] = await Promise.all([
      api.get('breeds/'),
      api.get('quadrants/'),
      api.get('movement_types/'),
    ]);
    breeds.value = listFromResponse(breedsResponse.data);
    quadrants.value = listFromResponse(quadrantsResponse.data);
    movementTypes.value = listFromResponse(typesResponse.data);
  } catch (error) {
    console.error('Erro ao carregar opções do cadastro bovino:', error);
    optionsError.value = apiErrorMessage(error, 'Não foi possível carregar raças, estábulos ou tipos de movimentação.');
  } finally {
    loadingOptions.value = false;
  }
}

async function loadAnimal() {
  loadingRecord.value = true;
  try {
    const [animalResponse, movementResponse] = await Promise.all([
      api.get(`animals/${route.params.id}/`),
      api.get(`animal_movements/?animal_id=${route.params.id}`),
    ]);
    const animal = animalResponse.data;
    const movements = listFromResponse(movementResponse.data);
    const latest = ultimaMovimentacaoPorAnimal(movements).get(String(animal.id));
    currentQuadrantId.value = latest ? idRelacao(latest.quadrant) : null;
    formData.value = {
      ...formData.value,
      name: animal.name || '',
      register_number: animal.register_number,
      breed: Number(idRelacao(animal.breed)),
      status: animal.status || 'active',
      score: Number(animal.score || 0),
      reproductive_status: Boolean(animal.reproductive_status),
      quadrant: latest ? Number(idRelacao(latest.quadrant)) : '',
      movement_type: latest ? Number(idRelacao(latest.movement_type)) : '',
      movement_date: latest?.movement_date || todayIso(),
      movement_reason: latest?.movement_reason || 'Transferência de estábulo',
    };
  } catch (error) {
    console.error('Erro ao carregar bovino para edição:', error);
    formMessage.value = apiErrorMessage(error, 'Não foi possível carregar os dados deste bovino.');
  } finally {
    loadingRecord.value = false;
  }
}

function animalPayload() {
  return {
    name: formData.value.name,
    register_number: Number(formData.value.register_number),
    breed: Number(formData.value.breed),
    status: formData.value.status,
    score: Number(formData.value.score),
    reproductive_status: Boolean(formData.value.reproductive_status),
  };
}

function movementPayload(animalId) {
  return {
    animal: animalId,
    quadrant: Number(formData.value.quadrant),
    movement_type: Number(formData.value.movement_type),
    movement_date: formData.value.movement_date,
    movement_reason: formData.value.movement_reason,
  };
}

async function saveAnimal() {
  if (loading.value || movementPending.value) return;
  loading.value = true;
  formMessage.value = '';
  partialSuccess.value = '';
  try {
    let animalId;
    if (isEdit) {
      animalId = Number(route.params.id);
      await api.patch(`animals/${animalId}/`, animalPayload());
    } else {
      const response = await api.post('animals/', animalPayload());
      animalId = response.data?.id;
      if (!animalId) throw new Error('O cadastro foi aceito, mas a API não retornou o ID do bovino.');
    }

    const newQuadrantId = Number(formData.value.quadrant);
    if (!isEdit || String(newQuadrantId) !== String(currentQuadrantId.value)) {
      const payload = movementPayload(animalId);
      try {
        await api.post('animal_movements/', payload);
      } catch (errorMovement) {
        console.error('Bovino salvo, mas a movimentação falhou:', errorMovement);
        movementPending.value = { animalId, payload };
        partialSuccess.value = isEdit
          ? 'Os dados do bovino foram salvos, mas a nova lotação não. Tente registrar a movimentação novamente.'
          : `O bovino #${animalId} foi criado, mas a lotação não foi registrada. Tente salvar a movimentação novamente.`;
        formMessage.value = apiErrorMessage(errorMovement, 'A API não aceitou a movimentação.');
        return;
      }
    }
    router.push('/animais');
  } catch (error) {
    console.error('Erro ao salvar bovino:', error);
    formMessage.value = apiErrorMessage(error, 'Não foi possível salvar o bovino. Confira os campos e tente novamente.');
  } finally {
    loading.value = false;
  }
}

async function retryMovement() {
  if (!movementPending.value || loading.value) return;
  loading.value = true;
  formMessage.value = '';
  try {
    await api.post('animal_movements/', movementPending.value.payload);
    movementPending.value = null;
    partialSuccess.value = '';
    router.push('/animais');
  } catch (error) {
    console.error('Erro ao repetir movimentação do bovino:', error);
    formMessage.value = apiErrorMessage(error, 'Não foi possível registrar a movimentação.');
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  await loadOptions();
  if (isEdit) await loadAnimal();
});
</script>
