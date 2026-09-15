<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        titulo="Registro de ordenha"
        descricao="Lance a produção diária de leite por fêmea do rebanho."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <section class="card">
        <header class="card__head">
          <div>
            <h2 class="card__title">Nova entrada de leite</h2>
            <p class="card__desc">Só fêmeas aparecem na lista — o macho não entra na ordenha.</p>
          </div>
          <span class="badge"><AppIcon name="milk" :size="13" /> Ordenha</span>
        </header>

        <form @submit.prevent="handleSubmit">
          <div class="card__body grid grid--2">
            <div class="field span-2">
              <label class="field__label" for="animal">Animal</label>
              <select
                id="animal"
                v-model.number="formData.animal"
                class="select"
                required
                :disabled="femaleAnimals.length === 0"
              >
                <option value="" disabled>
                  {{ femaleAnimals.length > 0 ? 'Selecione um animal...' : 'Nenhuma fêmea cadastrada disponível' }}
                </option>
                <option v-for="animal in femaleAnimals" :key="animal.id" :value="animal.id">
                  {{ animal.name || 'Sem nome' }} — brinco #{{ animal.register_number }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="litros">Quantidade (litros)</label>
              <input id="litros" v-model="formData.milk_production" class="input" type="number" step="0.1" placeholder="15.5" required>
            </div>

            <div class="field">
              <label class="field__label" for="data">Data da coleta</label>
              <input id="data" v-model="formData.production_date" class="input" type="date" required>
            </div>

            <p v-if="message" class="span-2 alert" :class="isSuccess ? 'alert--ok' : 'alert--danger'" role="status">
              <AppIcon :name="isSuccess ? 'check-circle' : 'alert'" :size="16" />
              <span>{{ message }}</span>
            </p>
          </div>

          <footer class="card__foot">
            <button type="submit" class="btn btn--primary" :disabled="loading || femaleAnimals.length === 0">
              {{ loading ? 'Salvando...' : 'Registrar ordenha' }}
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
const message = ref('');
const isSuccess = ref(false);
const animals = ref([]);

const isFemaleAnimal = (animalData) => String(animalData?.sex || '').toLowerCase() === 'f';
const femaleAnimals = computed(() => animals.value.filter(isFemaleAnimal));

const formData = ref({
  animal: '',
  milk_production: '',
  production_date: new Date().toISOString().split('T')[0]
});

onMounted(async () => {
  try {
    const res = await api.get('animals/');
    animals.value = (res.data.results || res.data).filter(isFemaleAnimal);
  } catch (error) {
    console.error('Erro ao carregar animais para ordenha:', error);
    animals.value = [];
  }
});

const handleSubmit = async () => {
  loading.value = true;
  message.value = '';
  try {
    const payload = {
      animal: parseInt(formData.value.animal),
      milk_production: parseFloat(formData.value.milk_production),
      production_date: formData.value.production_date
    };
    await api.post('milk_production_history/', payload);
    isSuccess.value = true;
    message.value = 'Ordenha registrada com sucesso!';
    formData.value.animal = '';
    formData.value.milk_production = '';
    formData.value.production_date = new Date().toISOString().split('T')[0];
  } catch (error) {
    console.error('Erro ao salvar ordenha:', error);
    console.error('Resposta do servidor:', error.response?.data);
    isSuccess.value = false;
    message.value = 'Erro ao registrar ordenha. Verifique os dados.';
  } finally {
    loading.value = false;
    setTimeout(() => { message.value = ''; }, 4000);
  }
};
</script>
