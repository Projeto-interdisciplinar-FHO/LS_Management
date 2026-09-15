<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        titulo="Registro de alimentação"
        descricao="Lance o consumo de ração ou suplemento, por animal ou para todo o rebanho."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

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
              <select id="animal" v-model="formData.animal" class="select" required>
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
              <select id="alimento" v-model="formData.feed_type_id" class="select" required>
                <option value="" disabled>Selecione o alimento...</option>
                <option v-for="feed in feedTypesList" :key="feed.id" :value="feed.id">
                  {{ feed.name }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="quantidade">Quantidade fornecida (kg)</label>
              <input id="quantidade" v-model="formData.quantity" class="input" type="number" step="0.01" placeholder="4.50" required>
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
            <button type="submit" class="btn btn--primary" :disabled="loading">
              {{ loading ? 'Salvando...' : 'Confirmar alimentação' }}
            </button>
          </footer>
        </form>
      </section>
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

const painel = computed(() => painelDoPapel());

const loading = ref(false);
const animalsList = ref([]);
const feedTypesList = ref([]);
const message = ref('');
const isSuccess = ref(false);

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
  try {
    // Busca animais cadastrados
    const animRes = await api.get('animals/');
    animalsList.value = animRes.data.results || animRes.data;

    // Busca os tipos de alimentos cadastrados no backend
    const feedRes = await api.get('foods/');
    feedTypesList.value = feedRes.data.results || feedRes.data;
  } catch (error) {
    console.error("Erro ao carregar dados do formulário nutricional:", error);
    // Fallback de segurança para testes
    feedTypesList.value = [
      { id: 1, name: 'Ração Concentrada 22%' },
      { id: 2, name: 'Silagem de Milho' },
      { id: 3, name: 'Suplemento Mineral' }
    ];
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
    avisar('Erro ao registrar alimentação no servidor.', false);
  } finally {
    loading.value = false;
  }
};
</script>
