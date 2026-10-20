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
              </div>

              <div class="field">
                <label class="field__label" for="ind-vacina">Vacina aplicada</label>
                <select id="ind-vacina" v-model="individualForm.vaccine" class="select" required :disabled="loadingOptions || !vaccinesList.length">
                  <option value="" disabled>{{ loadingOptions ? 'Carregando vacinas...' : 'Selecione uma vacina...' }}</option>
                  <option v-for="vaccine in vaccinesList" :key="vaccine.id" :value="vaccine.id">
                    {{ vaccine.name }}
                  </option>
                </select>
              </div>

              <div class="grid grid--2">
                <div class="field">
                  <label class="field__label" for="ind-dose">Dosagem</label>
                  <input id="ind-dose" v-model="individualForm.dosage" class="input" type="text" placeholder="Ex: 5 ml" required>
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
                  <input id="lote-dose" v-model="batchForm.dosage" class="input" type="text" placeholder="Ex: 5 ml" required>
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
const animalsList = ref([]); // Nova lista para o dropdown de animais

const individualForm = ref({
  animal: '',
  vaccine: '',
  dosage: '',
  date: new Date().toISOString().split('T')[0]
});

const batchForm = ref({
  quadrant: '',
  vaccine: '',
  dosage: '',
  date: new Date().toISOString().split('T')[0]
});

onMounted(() => {
  fetchDropdownData();
});

const fetchDropdownData = async () => {
  loadingOptions.value = true;
  optionsError.value = '';
  const setters = [animalsList, vaccinesList, stablesList];
  const labels = ['animais', 'vacinas', 'estábulos'];

  try {
    const responses = await Promise.allSettled([
      api.get('animals/'),
      api.get('vaccines/'),
      api.get('quadrants/'),
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
      dosage: individualForm.value.dosage
    };

    await api.post('vaccinations/', payload);

    okInd.value = true;
    msgInd.value = 'Vacina registrada com sucesso.';
    individualForm.value.animal = '';
    individualForm.value.vaccine = '';
    individualForm.value.dosage = '';
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
    const payload = {
      quadrant_id: batchForm.value.quadrant,
      vaccine_id: batchForm.value.vaccine,
      vaccination_date: batchForm.value.date,
      dosage: batchForm.value.dosage
    };

    await api.post('vaccinations/batch/', payload);

    okLote.value = true;
    msgLote.value = 'Lote vacinado com sucesso.';
    batchForm.value.quadrant = '';
    batchForm.value.vaccine = '';
    batchForm.value.dosage = '';
  } catch (error) {
    console.error(error);
    okLote.value = false;
    msgLote.value = apiErrorMessage(error, 'Não foi possível vacinar o lote selecionado.');
  } finally {
    loadingBatch.value = false;
    setTimeout(() => { msgLote.value = ''; }, 5000);
  }
};
</script>
