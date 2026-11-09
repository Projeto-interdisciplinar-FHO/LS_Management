<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Vacinação"
        descricao="Registre a aplicação em um animal ou no lote inteiro de um estábulo."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <p v-if="optionsError" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ optionsError }}</span>
        <button type="button" class="btn btn--sm" @click="fetchDropdownData">Tentar novamente</button>
      </p>

      <div class="grid grid--wide">
        <section class="card">
          <header class="card__head">
            <div class="list__main">
              <span class="icon-tile icon-tile--accent"><AppIcon name="syringe" :size="17" /></span>
              <div>
                <h2 class="card__title">Individual</h2>
                <p class="card__desc">Uma aplicação, um animal.</p>
              </div>
            </div>
          </header>

          <form @submit.prevent="submitIndividual">
            <div class="card__body stack">
              <div class="field">
                <label class="field__label" for="ind-animal">Animal</label>
                <select id="ind-animal" v-model="individualForm.animal" class="select" required :disabled="loadingOptions || !animalsList.length">
                  <option value="" disabled>{{ loadingOptions ? 'Carregando animais...' : 'Escolha um animal...' }}</option>
                  <option v-for="animal in animalsList" :key="animal.id" :value="animal.id">
                    {{ animal.name || 'Sem nome' }} — brinco #{{ animal.register_number }}
                  </option>
                </select>
                <span v-if="!loadingOptions && !animalsList.length && !optionsError" class="field__hint">
                  Nenhum animal disponível para vacinação.
                </span>
              </div>

              <div class="field">
                <label class="field__label" for="ind-vacina">Vacina aplicada</label>
                <select id="ind-vacina" v-model="individualForm.vaccine" class="select" required :disabled="loadingOptions || !vaccinesList.length">
                  <option value="" disabled>{{ loadingOptions ? 'Carregando vacinas...' : 'Selecione uma vacina...' }}</option>
                  <option v-for="vaccine in vaccinesList" :key="vaccine.id" :value="vaccine.id">
                    {{ vaccine.name }}
                  </option>
                </select>
                <span v-if="!loadingOptions && !vaccinesList.length && !optionsError" class="field__hint">
                  Cadastre uma vacina antes de registrar uma aplicação.
                  <RouterLink to="/vacinas">Cadastrar vacina</RouterLink>
                </span>
              </div>

              <div class="grid grid--2">
                <div class="field">
                  <label class="field__label" for="ind-dose">Dosagem</label>
                  <input id="ind-dose" v-model.number="individualForm.dosage" class="input" type="number" min="0.01" step="0.01" placeholder="5" required>
                </div>
                <div class="field">
                  <label class="field__label" for="ind-data">Data de aplicação</label>
                  <input id="ind-data" v-model="individualForm.date" class="input" type="date" required>
                </div>
              </div>

              <p v-if="msgInd" class="alert" :class="okInd ? 'alert--ok' : 'alert--danger'" :role="okInd ? 'status' : 'alert'">
                <AppIcon :name="okInd ? 'check-circle' : 'alert'" :size="16" />
                <span>{{ msgInd }}</span>
              </p>
            </div>

            <footer class="card__foot">
              <button type="submit" class="btn btn--primary" :disabled="loadingInd || loadingOptions || !animalsList.length || !vaccinesList.length">
                {{ loadingInd ? 'Salvando...' : loadingOptions ? 'Carregando opções...' : 'Registrar vacina' }}
              </button>
            </footer>
          </form>
        </section>

        <section class="card">
          <header class="card__head">
            <div class="list__main">
              <span class="icon-tile icon-tile--warn"><AppIcon name="herd" :size="17" /></span>
              <div>
                <h2 class="card__title">Por estábulo</h2>
                <p class="card__desc">Aplica em todos os animais alojados na instalação.</p>
              </div>
            </div>
          </header>

          <form @submit.prevent="submitBatch">
            <div class="card__body stack">
              <div class="field">
                <label class="field__label" for="lote-estabulo">Estábulo</label>
                <select id="lote-estabulo" v-model="batchForm.quadrant" class="select" required :disabled="loadingOptions || !stablesList.length">
                  <option value="" disabled>{{ loadingOptions ? 'Carregando estábulos...' : 'Escolha um estábulo...' }}</option>
                  <option v-for="stable in stablesList" :key="stable.id" :value="stable.id">
                    {{ stable.name || stable.nome_quadrante || `Estábulo ${stable.id}` }}
                  </option>
                </select>
              </div>

              <div class="field">
                <label class="field__label" for="lote-vacina">Vacina aplicada</label>
                <select id="lote-vacina" v-model="batchForm.vaccine" class="select" required :disabled="loadingOptions || !vaccinesList.length">
                  <option value="" disabled>{{ loadingOptions ? 'Carregando vacinas...' : 'Selecione uma vacina...' }}</option>
                  <option v-for="vaccine in vaccinesList" :key="vaccine.id" :value="vaccine.id">
                    {{ vaccine.name }}
                  </option>
                </select>
              </div>

              <div class="grid grid--2">
                <div class="field">
                  <label class="field__label" for="lote-dose">Dosagem</label>
                  <input id="lote-dose" v-model.number="batchForm.dosage" class="input" type="number" min="0.01" step="0.01" placeholder="5" required>
                </div>
                <div class="field">
                  <label class="field__label" for="lote-data">Data de aplicação</label>
                  <input id="lote-data" v-model="batchForm.date" class="input" type="date" required>
                </div>
              </div>

              <p class="alert alert--info">
                <AppIcon name="info" :size="16" />
                <span>O lançamento vale para todos os animais do estábulo escolhido.</span>
              </p>

              <p v-if="msgLote" class="alert" :class="okLote ? 'alert--ok' : 'alert--danger'" :role="okLote ? 'status' : 'alert'">
                <AppIcon :name="okLote ? 'check-circle' : 'alert'" :size="16" />
                <span>{{ msgLote }}</span>
              </p>
            </div>

            <footer class="card__foot">
              <button type="submit" class="btn btn--primary" :disabled="loadingBatch || loadingOptions || !stablesList.length || !vaccinesList.length">
                {{ loadingBatch ? 'Processando lote...' : loadingOptions ? 'Carregando opções...' : 'Vacinar lote inteiro' }}
              </button>
            </footer>
          </form>
        </section>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';
import { painelDoPapel } from '@/services/auth';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { apiErrorMessage } from '@/utils/apiError';
import { situacao } from '@/utils/statusUtils';
import { idRelacao, ultimaMovimentacaoPorAnimal } from '@/utils/animalMovementUtils';

const painel = computed(() => painelDoPapel());

const loadingInd = ref(false);
const loadingBatch = ref(false);
const loadingOptions = ref(true);
const optionsError = ref('');

// Cada formulário tem a sua própria resposta, do lado do botão que a produziu.
// Antes os dois usavam alert(), sem dizer qual dos dois tinha respondido.
const msgInd = ref('');
const okInd = ref(false);
const msgLote = ref('');
const okLote = ref(false);

const vaccinesList = ref([]);
const stablesList = ref([]);
const animalsList = ref([]);
const movementsList = ref([]);
const completedBatchAnimalIds = ref(new Set());
const lastBatchKey = ref('');

const individualForm = ref({
  animal: '',
  vaccine: '',
  dosage: 1,
  date: new Date().toISOString().split('T')[0]
});

const batchForm = ref({
  quadrant: '',
  vaccine: '',
  dosage: 1,
  date: new Date().toISOString().split('T')[0]
});

onMounted(() => {
  fetchDropdownData();
});

const fetchDropdownData = async () => {
  loadingOptions.value = true;
  optionsError.value = '';
  const setters = [animalsList, vaccinesList, stablesList, movementsList];
  const labels = ['animais', 'vacinas', 'estábulos', 'movimentações'];

  try {
    const responses = await Promise.allSettled([
      api.getAnimals(),
      api.get('vaccines/'),
      api.getQuadrants(),
      api.get('animal_movements/'),
    ]);
    const failedLabels = [];

    responses.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        const data = result.value.data;
        setters[index].value = data?.results || data || [];
      } else {
        setters[index].value = [];
        failedLabels.push(labels[index]);
      }
    });

    if (failedLabels.length) {
      optionsError.value = `Não foi possível carregar ${failedLabels.join(', ')}. Verifique a conexão e tente novamente.`;
    }
  } catch (error) {
    console.error(error);
    optionsError.value = apiErrorMessage(error, 'Não foi possível carregar as opções de vacinação.');
  } finally {
    loadingOptions.value = false;
  }
};

const submitIndividual = async () => {
  loadingInd.value = true;
  msgInd.value = '';
  try {
    const payload = {
      animal: individualForm.value.animal,
      vaccine: individualForm.value.vaccine,
      vaccination_date: individualForm.value.date,
      dosage: Number(individualForm.value.dosage)
    };

    await api.post('vaccinations/', payload);

    okInd.value = true;
    msgInd.value = 'Vacina registrada com sucesso.';
    individualForm.value.animal = '';
    individualForm.value.vaccine = '';
    individualForm.value.dosage = 1;
  } catch (error) {
    console.error(error);
    okInd.value = false;
    msgInd.value = apiErrorMessage(error, 'Não foi possível registrar a vacinação individual.');
  } finally {
    loadingInd.value = false;
    setTimeout(() => { msgInd.value = ''; }, 5000);
  }
};

const submitBatch = async () => {
  loadingBatch.value = true;
  msgLote.value = '';
  try {
    const key = [
      batchForm.value.quadrant,
      batchForm.value.vaccine,
      batchForm.value.date,
      batchForm.value.dosage,
    ].join('|');
    if (key !== lastBatchKey.value) {
      completedBatchAnimalIds.value = new Set();
      lastBatchKey.value = key;
    }
    const latest = ultimaMovimentacaoPorAnimal(movementsList.value);
    const stableAnimals = animalsList.value.filter((animal) =>
      String(idRelacao(latest.get(String(animal.id))?.quadrant)) === String(batchForm.value.quadrant)
      && situacao(animal.status).noRebanho
      && !completedBatchAnimalIds.value.has(animal.id)
    );
    if (!stableAnimals.length) {
      throw new Error('Não há animais pendentes nesse estábulo para os dados selecionados.');
    }
    const results = await Promise.allSettled(stableAnimals.map((animal) =>
      api.post('vaccinations/', {
        animal: animal.id,
        vaccine: Number(batchForm.value.vaccine),
        vaccination_date: batchForm.value.date,
        dosage: Number(batchForm.value.dosage),
      })
    ));
    const failed = [];
    results.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        completedBatchAnimalIds.value.add(stableAnimals[index].id);
      } else {
        failed.push(stableAnimals[index].name || `#${stableAnimals[index].register_number}`);
        console.error(`Falha ao vacinar ${stableAnimals[index].name}:`, result.reason);
      }
    });
    const succeeded = results.length - failed.length;
    okLote.value = failed.length === 0;
    msgLote.value = failed.length
      ? `${succeeded} aplicação(ões) registrada(s); falha para: ${failed.join(', ')}. Reenvie para tentar apenas os pendentes.`
      : `${succeeded} aplicação(ões) registradas.`;
    if (!failed.length) {
      batchForm.value.quadrant = '';
      batchForm.value.vaccine = '';
      batchForm.value.dosage = 1;
      completedBatchAnimalIds.value = new Set();
      lastBatchKey.value = '';
    }
  } catch (error) {
    console.error(error);
    okLote.value = false;
    msgLote.value = error?.message || apiErrorMessage(error, 'Não foi possível vacinar o lote selecionado.');
  } finally {
    loadingBatch.value = false;
  }
};
</script>
