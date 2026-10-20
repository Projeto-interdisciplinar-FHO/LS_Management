<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        titulo="Registro de peso"
        descricao="Lance o peso medido na balança para acompanhar a evolução do animal."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <section class="card">
        <header class="card__head">
          <div>
            <h2 class="card__title">Nova pesagem</h2>
            <p class="card__desc">Escolha o animal, informe o peso e a data da medição.</p>
          </div>
          <span class="badge"><AppIcon name="scale" :size="13" /> Pesagem</span>
        </header>

        <form @submit.prevent="handleSubmit">
          <div class="card__body grid grid--2">
            <div class="field span-2">
              <label class="field__label" for="animal">Animal</label>
              <select id="animal" v-model.number="formData.animal" class="select" required :disabled="loadingAnimals || !animals.length">
                <option value="" disabled>{{ loadingAnimals ? 'Carregando animais...' : 'Selecione um animal...' }}</option>
                <option v-for="animal in animals" :key="animal.id" :value="animal.id">
                  {{ animal.name || 'Sem nome' }} — brinco #{{ animal.register_number }}
                </option>
              </select>
              <span v-if="animalLoadError" class="field__hint" role="alert">{{ animalLoadError }}</span>
              <span v-else-if="!loadingAnimals && !animals.length" class="field__hint">
                Nenhum animal disponível. Cadastre o rebanho antes de lançar pesagens.
              </span>
            </div>

            <div class="field">
              <label class="field__label" for="peso">Peso (kg)</label>
              <input id="peso" v-model="formData.weight" class="input" type="number" step="0.1" placeholder="450.5" required>
            </div>

            <div class="field">
              <label class="field__label" for="data">Data da pesagem</label>
              <input id="data" v-model="formData.weighing_date" class="input" type="date" required>
            </div>

            <p v-if="message" class="span-2 alert" :class="isSuccess ? 'alert--ok' : 'alert--danger'" :role="isSuccess ? 'status' : 'alert'">
              <AppIcon :name="isSuccess ? 'check-circle' : 'alert'" :size="16" />
              <span>{{ message }}</span>
            </p>
          </div>

          <footer class="card__foot">
            <button type="submit" class="btn btn--primary" :disabled="loading || loadingAnimals || !animals.length">
              {{ loading ? 'Salvando...' : 'Confirmar peso' }}
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
import { apiErrorMessage } from '@/utils/apiError';

const painel = computed(() => painelDoPapel());

const loading = ref(false);
const loadingAnimals = ref(true);
const message = ref('');
const isSuccess = ref(false);
const animalLoadError = ref('');
const animals = ref([]);

const formData = ref({
  animal: '',
  weight: '',
  weighing_date: new Date().toISOString().split('T')[0]
});

const loadAnimals = async () => {
  loadingAnimals.value = true;
  animalLoadError.value = '';
  try {
    const response = await api.getAnimals();
    animals.value = response.data.results || response.data;
  } catch (error) {
    console.error('Erro ao carregar animais:', error);
    animals.value = [];
    animalLoadError.value = apiErrorMessage(error, 'Não foi possível carregar os animais.');
  } finally {
    loadingAnimals.value = false;
  }
};

const handleSubmit = async () => {
  loading.value = true;
  message.value = '';
  try {
    const payload = {
      animal: parseInt(formData.value.animal, 10),
      weight: parseFloat(formData.value.weight),
      weighing_date: formData.value.weighing_date
    };
    await api.registrarPeso(payload);
    isSuccess.value = true;
    message.value = 'Pesagem registrada com sucesso!';
    formData.value.animal = '';
    formData.value.weight = '';
    formData.value.weighing_date = new Date().toISOString().split('T')[0];
  } catch (error) {
    console.error('Erro ao salvar pesagem:', error.response?.data || error);
    isSuccess.value = false;
    message.value = apiErrorMessage(error, 'Não foi possível registrar a pesagem. Confira os dados informados.');
  } finally {
    loading.value = false;
    setTimeout(() => {
      message.value = '';
    }, 4000);
  }
};

onMounted(loadAnimals);
</script>
