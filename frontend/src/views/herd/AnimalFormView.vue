<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        :titulo="pageTitle"
        :descricao="pageDescription"
        voltar-rotulo="Animais"
        voltar-para="/animais"
      />

      <AppTabs
        v-if="!isEdit && !isEditBull"
        v-model="animalType"
        :tabs="typeTabs"
        label="Tipo de cadastro"
        id-base="animal-form-type"
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

      <!-- Formulário de Vaca / Bovino -->
      <form v-if="animalType === 'cow'" class="stack-24" novalidate @submit.prevent="saveAnimal">
        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Identificação e classificação</h2>
              <p class="card__desc">Campos obrigatórios do cadastro bovino: nome, brinco, raça, situação e escore.</p>
            </div>
          </header>

          <div class="card__body grid grid--2">
            <div class="field">
              <label class="field__label" for="nome">Nome *</label>
              <input
                id="nome"
                v-model.trim="formData.name"
                class="input"
                :class="{ 'input--error': fieldErrors.name }"
                type="text"
                maxlength="100"
                :aria-invalid="Boolean(fieldErrors.name)"
                placeholder="Ex: Mimosa"
                required
              >
              <span v-if="fieldErrors.name" class="field__error" role="alert">{{ fieldErrors.name }}</span>
            </div>

            <div class="field">
              <label class="field__label" for="registro">Número de registro (brinco) *</label>
              <input
                id="registro"
                v-model="formData.register_number"
                class="input"
                :class="{ 'input--error': fieldErrors.register_number }"
                type="number"
                min="1"
                step="1"
                :aria-invalid="Boolean(fieldErrors.register_number)"
                placeholder="Ex: 1042"
                required
              >
              <span v-if="fieldErrors.register_number" class="field__error" role="alert">{{ fieldErrors.register_number }}</span>
            </div>

            <div class="field">
              <label class="field__label" for="raca">Raça *</label>
              <select
                id="raca"
                v-model="formData.breed"
                class="select"
                :class="{ 'select--error': fieldErrors.breed }"
                :aria-invalid="Boolean(fieldErrors.breed)"
                :disabled="loadingOptions"
                required
              >
                <option value="" disabled>{{ loadingOptions ? 'Carregando raças...' : 'Selecione uma raça...' }}</option>
                <option v-for="breed in breeds" :key="breed.id" :value="String(breed.id)">{{ breed.name }}</option>
              </select>
              <span v-if="fieldErrors.breed" class="field__error" role="alert">{{ fieldErrors.breed }}</span>
              <span v-else-if="!loadingOptions && !breeds.length" class="field__hint">
                Nenhuma raça cadastrada. Cadastre uma raça em Cadastros &rarr; Raças.
              </span>
            </div>

            <div class="field">
              <label class="field__label" for="situacao">Situação</label>
              <select
                id="situacao"
                v-model="formData.status"
                class="select"
                :class="{ 'select--error': fieldErrors.status }"
                :aria-invalid="Boolean(fieldErrors.status)"
              >
                <option v-for="status in SITUACOES" :key="status.valor" :value="status.valor">
                  {{ status.rotulo }}
                </option>
              </select>
              <span v-if="fieldErrors.status" class="field__error" role="alert">{{ fieldErrors.status }}</span>
            </div>

            <div class="field">
              <label class="field__label" for="escore">Escore</label>
              <input
                id="escore"
                v-model="formData.score"
                class="input"
                :class="{ 'input--error': fieldErrors.score }"
                type="number"
                min="0"
                max="999999.99"
                step="0.01"
                :aria-invalid="Boolean(fieldErrors.score)"
                placeholder="0.00"
              >
              <span v-if="fieldErrors.score" class="field__error" role="alert">{{ fieldErrors.score }}</span>
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
              <p class="card__desc">Opcional: defina o estábulo inicial ou registre uma transferência.</p>
            </div>
          </header>

          <div class="card__body grid grid--2">
            <div class="field">
              <label class="field__label" for="estabulo">Estábulo</label>
              <select
                id="estabulo"
                v-model="formData.quadrant"
                class="select"
                :class="{ 'select--error': fieldErrors.quadrant }"
                :aria-invalid="Boolean(fieldErrors.quadrant)"
                :disabled="loadingOptions"
              >
                <option value="">{{ loadingOptions ? 'Carregando estábulos...' : 'Sem estábulo definido' }}</option>
                <option v-for="quadrant in quadrants" :key="quadrant.id" :value="String(quadrant.id)">{{ quadrant.name }}</option>
              </select>
              <span v-if="fieldErrors.quadrant" class="field__error" role="alert">{{ fieldErrors.quadrant }}</span>
            </div>

            <div class="field">
              <label class="field__label" for="tipo-movimentacao">Tipo de movimentação</label>
              <select
                id="tipo-movimentacao"
                v-model="formData.movement_type"
                class="select"
                :class="{ 'select--error': fieldErrors.movement_type }"
                :aria-invalid="Boolean(fieldErrors.movement_type)"
                :disabled="loadingOptions || !formData.quadrant"
              >
                <option value="" disabled>{{ loadingOptions ? 'Carregando tipos...' : 'Selecione um tipo...' }}</option>
                <option v-for="type in movementTypes" :key="type.id" :value="String(type.id)">{{ type.name }}</option>
              </select>
              <span v-if="fieldErrors.movement_type" class="field__error" role="alert">{{ fieldErrors.movement_type }}</span>
            </div>

            <div class="field">
              <label class="field__label" for="data-movimentacao">Data da movimentação</label>
              <input
                id="data-movimentacao"
                v-model="formData.movement_date"
                class="input"
                :class="{ 'input--error': fieldErrors.movement_date }"
                type="date"
                :disabled="!formData.quadrant"
              >
              <span v-if="fieldErrors.movement_date" class="field__error" role="alert">{{ fieldErrors.movement_date }}</span>
            </div>

            <div class="field">
              <label class="field__label" for="motivo-movimentacao">Motivo</label>
              <input
                id="motivo-movimentacao"
                v-model.trim="formData.movement_reason"
                class="input"
                :class="{ 'input--error': fieldErrors.movement_reason }"
                type="text"
                :disabled="!formData.quadrant"
              >
              <span v-if="fieldErrors.movement_reason" class="field__error" role="alert">{{ fieldErrors.movement_reason }}</span>
            </div>
          </div>

          <footer class="card__foot">
            <button type="button" class="btn" @click="$router.push('/animais')">Cancelar</button>
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

      <!-- Formulário de Touro -->
      <form v-else class="stack-24" novalidate @submit.prevent="saveBull">
        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Dados do touro</h2>
              <p class="card__desc">Cadastre o reprodutor para vinculá-lo às inseminações e genealogia.</p>
            </div>
          </header>

          <div class="card__body grid grid--2">
            <div class="field">
              <label class="field__label" for="touro-nome">Nome do touro *</label>
              <input
                id="touro-nome"
                v-model.trim="bullForm.name"
                class="input"
                :class="{ 'input--error': fieldErrors.name }"
                type="text"
                maxlength="100"
                :aria-invalid="Boolean(fieldErrors.name)"
                placeholder="Ex: Imperador"
                required
              >
              <span v-if="fieldErrors.name" class="field__error" role="alert">{{ fieldErrors.name }}</span>
            </div>

            <div class="field">
              <label class="field__label" for="touro-registro">Número de registro (brinco) *</label>
              <input
                id="touro-registro"
                v-model="bullForm.register_number"
                class="input"
                :class="{ 'input--error': fieldErrors.register_number }"
                type="number"
                min="1"
                step="1"
                :aria-invalid="Boolean(fieldErrors.register_number)"
                placeholder="Ex: 2001"
                required
              >
              <span v-if="fieldErrors.register_number" class="field__error" role="alert">{{ fieldErrors.register_number }}</span>
            </div>

            <div class="field">
              <label class="field__label" for="touro-raca">Raça *</label>
              <select
                id="touro-raca"
                v-model="bullForm.breed"
                class="select"
                :class="{ 'select--error': fieldErrors.breed }"
                :aria-invalid="Boolean(fieldErrors.breed)"
                :disabled="loadingOptions"
                required
              >
                <option value="" disabled>{{ loadingOptions ? 'Carregando raças...' : 'Selecione uma raça...' }}</option>
                <option v-for="breed in breeds" :key="breed.id" :value="String(breed.id)">{{ breed.name }}</option>
              </select>
              <span v-if="fieldErrors.breed" class="field__error" role="alert">{{ fieldErrors.breed }}</span>
            </div>

            <label class="field field--check">
              <input v-model="bullForm.active" type="checkbox">
              <span class="field__label">Touro ativo para reprodução</span>
            </label>
          </div>

          <footer class="card__foot">
            <button type="button" class="btn" @click="$router.push({ path: '/animais', query: { aba: 'touros' } })">Cancelar</button>
            <button
              type="submit"
              class="btn btn--primary"
              :disabled="loading || loadingOptions || loadingRecord"
            >
              {{ loading ? 'Salvando...' : loadingRecord ? 'Carregando touro...' : isEditBull ? 'Salvar alterações' : 'Cadastrar touro' }}
            </button>
          </footer>
        </section>
      </form>
    </div>
  </AppShell>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppTabs from '@/components/ui/AppTabs.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { SITUACOES } from '@/utils/statusUtils';
import { idRelacao, ultimaMovimentacaoPorAnimal } from '@/utils/animalMovementUtils';
import { apiErrorMessage, apiFieldErrors } from '@/utils/apiError';

const route = useRoute();
const router = useRouter();

const isEdit = Boolean(route.params.id);
const editBullId = route.query.bullId ? Number(route.query.bullId) : null;
const isEditBull = Boolean(editBullId);
const animalType = ref(!isEdit && (route.query.tipo === 'touro' || isEditBull) ? 'bull' : 'cow');
const typeTabs = [
  { id: 'cow', label: 'Vaca / Bovino', icon: 'animal' },
  { id: 'bull', label: 'Touro', icon: 'dna' },
];

const pageTitle = computed(() => {
  if (isEdit) return 'Editar bovino';
  if (isEditBull) return 'Editar touro';
  return animalType.value === 'bull' ? 'Cadastrar touro' : 'Cadastrar bovino';
});

const pageDescription = computed(() => {
  if (isEdit) return 'Atualize os dados e registre uma movimentação se mudar o estábulo.';
  if (isEditBull) return 'Atualize os dados do touro reprodutor.';
  return animalType.value === 'bull'
    ? 'Cadastre um touro reprodutor para o rebanho.'
    : 'Cadastre a vaca/bovino e, se desejar, registre sua lotação inicial.';
});

const loading = ref(false);
const loadingOptions = ref(true);
const loadingRecord = ref(false);
const optionsError = ref('');
const formMessage = ref('');
const partialSuccess = ref('');
const fieldErrors = ref({});
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

const bullForm = ref({
  name: '',
  register_number: '',
  breed: '',
  active: true,
});

watch(animalType, () => {
  formMessage.value = '';
  partialSuccess.value = '';
  fieldErrors.value = {};
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
    if (!isEdit && movementTypes.value.length && !formData.value.movement_type) {
      formData.value.movement_type = String(movementTypes.value[0].id);
    }
  } catch (error) {
    console.error('Erro ao carregar opções do cadastro animal:', error);
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
      register_number: animal.register_number ?? '',
      breed: idRelacao(animal.breed) ? String(idRelacao(animal.breed)) : '',
      status: animal.status || 'active',
      score: Number(animal.score ?? 0),
      reproductive_status: Boolean(animal.reproductive_status),
      quadrant: latest && idRelacao(latest.quadrant) ? String(idRelacao(latest.quadrant)) : '',
      movement_type: latest && idRelacao(latest.movement_type)
        ? String(idRelacao(latest.movement_type))
        : (movementTypes.value[0] ? String(movementTypes.value[0].id) : ''),
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

function validateAnimalForm() {
  const errors = {};
  if (!formData.value.name.trim()) {
    errors.name = 'Informe o nome do animal.';
  }
  const reg = Number(formData.value.register_number);
  if (formData.value.register_number === '' || !Number.isInteger(reg) || reg < 1) {
    errors.register_number = 'Informe um número de registro inteiro maior que zero.';
  }
  if (!formData.value.breed) {
    errors.breed = 'Selecione uma raça.';
  }
  const score = Number(formData.value.score === '' ? 0 : formData.value.score);
  if (!Number.isFinite(score) || score < 0) {
    errors.score = 'Informe um escore válido maior ou igual a zero.';
  }
  const hasQuadrant = Boolean(formData.value.quadrant);
  const changedQuadrant = !isEdit || String(formData.value.quadrant) !== String(currentQuadrantId.value || '');
  if (hasQuadrant && changedQuadrant) {
    if (!formData.value.movement_type) errors.movement_type = 'Selecione o tipo de movimentação.';
    if (!formData.value.movement_date) errors.movement_date = 'Informe a data da movimentação.';
    if (!formData.value.movement_reason.trim()) errors.movement_reason = 'Informe o motivo da movimentação.';
  }
  fieldErrors.value = errors;
  return Object.keys(errors).length === 0;
}

function validateBullForm() {
  const errors = {};
  if (!bullForm.value.name.trim()) {
    errors.name = 'Informe o nome do touro.';
  }
  const reg = Number(bullForm.value.register_number);
  if (bullForm.value.register_number === '' || !Number.isInteger(reg) || reg < 1) {
    errors.register_number = 'Informe um número de registro inteiro maior que zero.';
  }
  if (!bullForm.value.breed) {
    errors.breed = 'Selecione uma raça.';
  }
  fieldErrors.value = errors;
  return Object.keys(errors).length === 0;
}

function animalPayload() {
  const rawScore = formData.value.score === '' || formData.value.score === null ? 0 : Number(formData.value.score);
  const normalizedScore = Number.isFinite(rawScore) ? Number(rawScore.toFixed(2)) : 0;
  return {
    name: formData.value.name.trim(),
    register_number: Number(formData.value.register_number),
    breed: Number(formData.value.breed),
    status: formData.value.status || 'active',
    score: normalizedScore,
    reproductive_status: Boolean(formData.value.reproductive_status),
  };
}

function movementPayload(animalId) {
  return {
    animal: animalId,
    quadrant: Number(formData.value.quadrant),
    movement_type: Number(formData.value.movement_type),
    movement_date: formData.value.movement_date,
    movement_reason: formData.value.movement_reason.trim(),
  };
}

async function saveAnimal() {
  if (loading.value || movementPending.value) return;
  formMessage.value = '';
  partialSuccess.value = '';
  if (!validateAnimalForm()) {
    formMessage.value = 'Confira os campos destacados antes de salvar.';
    return;
  }

  loading.value = true;
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

    const hasQuadrant = Boolean(formData.value.quadrant);
    const changedQuadrant = !isEdit || String(formData.value.quadrant) !== String(currentQuadrantId.value || '');
    if (hasQuadrant && changedQuadrant) {
      const payload = movementPayload(animalId);
      try {
        await api.post('animal_movements/', payload);
      } catch (errorMovement) {
        console.error('Bovino salvo, mas a movimentação falhou:', errorMovement);
        movementPending.value = { animalId, payload };
        fieldErrors.value = apiFieldErrors(errorMovement);
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
    fieldErrors.value = apiFieldErrors(error);
    formMessage.value = apiErrorMessage(error, 'Não foi possível salvar o bovino. Confira os campos e tente novamente.');
  } finally {
    loading.value = false;
  }
}

async function loadBull() {
  loadingRecord.value = true;
  try {
    const response = await api.getBullById(editBullId);
    const bull = response.data;
    bullForm.value = {
      name: bull.name || '',
      register_number: bull.register_number ?? '',
      breed: idRelacao(bull.breed) ? String(idRelacao(bull.breed)) : '',
      active: Boolean(bull.active),
    };
  } catch (error) {
    console.error('Erro ao carregar touro para edição:', error);
    formMessage.value = apiErrorMessage(error, 'Não foi possível carregar os dados deste touro.');
  } finally {
    loadingRecord.value = false;
  }
}

async function saveBull() {
  if (loading.value) return;
  formMessage.value = '';
  if (!validateBullForm()) {
    formMessage.value = 'Confira os campos destacados antes de salvar.';
    return;
  }

  loading.value = true;
  try {
    const payload = {
      name: bullForm.value.name.trim(),
      register_number: Number(bullForm.value.register_number),
      breed: Number(bullForm.value.breed),
      active: Boolean(bullForm.value.active),
    };
    if (isEditBull) {
      await api.updateBull(editBullId, payload);
    } else {
      await api.createBull(payload);
    }
    router.push({ path: '/animais', query: { aba: 'touros' } });
  } catch (error) {
    console.error('Erro ao salvar touro:', error);
    fieldErrors.value = apiFieldErrors(error);
    formMessage.value = apiErrorMessage(error, 'Não foi possível salvar o touro. Confira os campos e tente novamente.');
  } finally {
    loading.value = false;
  }
}

async function retryMovement() {
  if (!movementPending.value || loading.value) return;
  loading.value = true;
  formMessage.value = '';
  fieldErrors.value = {};
  try {
    await api.post('animal_movements/', movementPending.value.payload);
    movementPending.value = null;
    partialSuccess.value = '';
    router.push('/animais');
  } catch (error) {
    console.error('Erro ao repetir movimentação do bovino:', error);
    fieldErrors.value = apiFieldErrors(error);
    formMessage.value = apiErrorMessage(error, 'Não foi possível registrar a movimentação.');
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  await loadOptions();
  if (isEdit) await loadAnimal();
  else if (isEditBull) await loadBull();
});
</script>
