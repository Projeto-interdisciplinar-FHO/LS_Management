<template>
  <AppShell>
    <div class="page page--narrow">
      <header class="hero registry-hero">
        <div class="hero__bg" aria-hidden="true">
          <img :src="alimentosHero" alt="" class="hero__img">
          <div class="hero__shade"></div>
        </div>
        <div class="hero__content">
          <div>
            <div class="registry-hero__meta">
              <span class="hero__eyebrow">Manejo · Nutrição</span>
              <span class="registry-hero__pill">{{ feedTypesList.length }} alimento(s)</span>
            </div>
            <h1 class="hero__title">Registro de alimentação</h1>
            <p class="hero__desc">Lance o consumo de ração ou suplemento, por animal ou para todo o rebanho.</p>
          </div>
        </div>
      </header>

      <p v-if="optionsError" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ optionsError }}</span>
      </p>

      <section class="card">
        <header class="card__head">
          <div>
            <h2 class="card__title">Nova entrada de trato</h2>
            <p class="card__desc">O lançamento é gravado com a data informada, para cada animal selecionado.</p>
          </div>
          <span class="badge"><AppIcon name="feed" :size="13" /> Nutrição</span>
        </header>

        <form @submit.prevent="handleSubmit">
          <div class="card__body grid grid--2">
            <div class="field span-2">
              <label class="field__label" for="animal">Animal ou rebanho</label>
              <select id="animal" v-model="formData.animal" class="select" required :disabled="loadingOptions">
                <option value="" disabled>Escolha um animal ou todo o rebanho...</option>
                <option value="all">Todo o rebanho</option>
                <option v-for="animal in animalsList" :key="animal.id" :value="animal.id">
                  {{ animal.name || 'Sem nome' }} — brinco #{{ animal.register_number }}
                </option>
              </select>
              <!-- Lançar para o rebanho inteiro grava um registro por animal.
                   Dizer quantos são antes evita o susto depois. -->
              <span v-if="formData.animal === 'all'" class="field__hint">
                Serão gravados {{ animalsList.length }} registros — um para cada animal cadastrado.
              </span>
            </div>

            <div class="field">
              <label class="field__label" for="alimento">Tipo de alimento</label>
              <select id="alimento" v-model="formData.feed_type_id" class="select" required :disabled="loadingOptions || !feedTypesList.length">
                <option value="" disabled>{{ loadingOptions ? 'Carregando alimentos...' : 'Selecione o alimento...' }}</option>
                <option v-for="feed in feedTypesList" :key="feed.id" :value="feed.id">
                  {{ feed.name }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="quantidade">Quantidade fornecida (kg)</label>
              <input id="quantidade" v-model="formData.quantity" class="input" type="number" min="0" inputmode="decimal" step="0.01" placeholder="4.50" required>
            </div>

            <div class="field">
              <label class="field__label" for="data">Data do trato</label>
              <input id="data" v-model="formData.date_fed" class="input" type="date" required>
            </div>

            <p v-if="message" class="span-2 alert" :class="isSuccess ? 'alert--ok' : 'alert--danger'" role="status">
              <AppIcon :name="isSuccess ? 'check-circle' : 'alert'" :size="16" />
              <span>{{ message }}</span>
            </p>
          </div>

          <footer class="card__foot">
            <button type="submit" class="btn btn--primary" :disabled="loading || loadingOptions || !animalsList.length || !feedTypesList.length">
              {{ loading ? 'Salvando...' : loadingOptions ? 'Carregando opções...' : 'Confirmar alimentação' }}
            </button>
          </footer>
        </form>
      </section>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import alimentosHero from '@/assets/images/alimentos-hero.jpg';
import { apiErrorMessage } from '@/utils/apiError';

const loading = ref(false);
const loadingOptions = ref(true);
const animalsList = ref([]);
const feedTypesList = ref([]);
const message = ref('');
const isSuccess = ref(false);
const optionsError = ref('');

const formData = ref({
  animal: '',
  feed_type_id: '',
  quantity: '',
  date_fed: new Date().toISOString().split('T')[0]
});

onMounted(() => {
  fetchData();
});

const fetchData = async () => {
  loadingOptions.value = true;
  optionsError.value = '';
  try {
    const [animalsResult, feedsResult] = await Promise.allSettled([
      api.get('animals/'),
      api.get('foods/'),
    ]);
    const failedLists = [];

    if (animalsResult.status === 'fulfilled') {
      animalsList.value = animalsResult.value.data.results || animalsResult.value.data;
    } else {
      animalsList.value = [];
      failedLists.push('animais');
    }

    if (feedsResult.status === 'fulfilled') {
      feedTypesList.value = feedsResult.value.data.results || feedsResult.value.data;
    } else {
      feedTypesList.value = [];
      failedLists.push('alimentos');
    }

    if (failedLists.length) {
      optionsError.value = `Não foi possível carregar ${failedLists.join(' e ')}. Verifique a conexão e tente novamente.`;
    }
  } catch (error) {
    console.error("Erro ao carregar dados do formulário nutricional:", error);
    optionsError.value = apiErrorMessage(error, 'Não foi possível carregar as opções de alimentação.');
  } finally {
    loadingOptions.value = false;
  }
};

// O retorno era um alert() do navegador, que trava a tela e some sem deixar
// rastro. Agora a resposta fica no formulário, ao lado do que foi lançado.
const avisar = (texto, sucesso) => {
  isSuccess.value = sucesso;
  message.value = texto;
  setTimeout(() => { message.value = ''; }, 5000);
};

const handleSubmit = async () => {
  loading.value = true;
  message.value = '';
  try {
    const selectedAnimalIds = formData.value.animal === 'all'
      ? animalsList.value.map(a => a.id)
      : [formData.value.animal];

    if (selectedAnimalIds.length === 0) {
      throw new Error('Nenhum animal selecionado para lançamento.');
    }

    const payloads = selectedAnimalIds.map(animalId => ({
      animal: animalId,
      food: formData.value.feed_type_id,
      feeding_time: `${formData.value.date_fed}T12:00:00Z`,
      meal_weight: formData.value.quantity
    }));

    await Promise.all(payloads.map(payload => api.post('feedings/', payload)));
    avisar(
      formData.value.animal === 'all'
        ? `Alimentação lançada para ${selectedAnimalIds.length} animais.`
        : 'Alimentação lançada com sucesso.',
      true
    );

    // Reseta o formulário mantendo apenas a data
    formData.value.animal = '';
    formData.value.feed_type_id = '';
    formData.value.quantity = '';
  } catch (error) {
    console.error(error);
    avisar(apiErrorMessage(error, 'Não foi possível registrar a alimentação. Confira os dados informados.'), false);
  } finally {
    loading.value = false;
  }
};
</script>
