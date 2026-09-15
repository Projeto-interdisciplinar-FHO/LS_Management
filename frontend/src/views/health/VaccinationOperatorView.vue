<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Vacinação"
        descricao="Registre a aplicação em um animal ou no lote inteiro de um estábulo."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

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
                <select id="ind-animal" v-model="individualForm.animal" class="select" required>
                  <option value="" disabled>Escolha um animal...</option>
                  <option v-for="animal in animalsList" :key="animal.id" :value="animal.id">
                    {{ animal.name || 'Sem nome' }} — brinco #{{ animal.register_number }}
                  </option>
                </select>
              </div>

              <div class="field">
                <label class="field__label" for="ind-vacina">Vacina aplicada</label>
                <select id="ind-vacina" v-model="individualForm.vaccine" class="select" required>
                  <option value="" disabled>Selecione uma vacina...</option>
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

              <p v-if="msgInd" class="alert" :class="okInd ? 'alert--ok' : 'alert--danger'" role="status">
                <AppIcon :name="okInd ? 'check-circle' : 'alert'" :size="16" />
                <span>{{ msgInd }}</span>
              </p>
            </div>

            <footer class="card__foot">
              <button type="submit" class="btn btn--primary" :disabled="loadingInd">
                {{ loadingInd ? 'Salvando...' : 'Registrar vacina' }}
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
                <select id="lote-estabulo" v-model="batchForm.quadrant" class="select" required>
                  <option value="" disabled>Escolha um estábulo...</option>
                  <option v-for="stable in stablesList" :key="stable.id" :value="stable.id">
                    {{ stable.name || stable.nome_quadrante || `Estábulo ${stable.id}` }}
                  </option>
                </select>
              </div>

              <div class="field">
                <label class="field__label" for="lote-vacina">Vacina aplicada</label>
                <select id="lote-vacina" v-model="batchForm.vaccine" class="select" required>
                  <option value="" disabled>Selecione uma vacina...</option>
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

              <p v-if="msgLote" class="alert" :class="okLote ? 'alert--ok' : 'alert--danger'" role="status">
                <AppIcon :name="okLote ? 'check-circle' : 'alert'" :size="16" />
                <span>{{ msgLote }}</span>
              </p>
            </div>

            <footer class="card__foot">
              <button type="submit" class="btn btn--primary" :disabled="loadingBatch">
                {{ loadingBatch ? 'Processando lote...' : 'Vacinar lote inteiro' }}
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

const painel = computed(() => painelDoPapel());

const loadingInd = ref(false);
const loadingBatch = ref(false);

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
  try {
    // 1. Busca os animais para o novo dropdown
    api.get('animals/').then(res => {
      // Trata tanto a resposta paginada do Django quanto a direta
      animalsList.value = res.data.results || res.data;
    }).catch(e => console.error("Erro ao carregar animais", e));

    // 2. Busca as vacinas
    api.get('vaccines/').then(res => {
      vaccinesList.value = res.data.results || res.data;
    }).catch(() => {
      // Mock de segurança caso a rota não exista no backend ainda
      vaccinesList.value = [
        { id: 1, name: 'Febre Aftosa' },
        { id: 2, name: 'Brucelose' },
        { id: 3, name: 'Raiva' }
      ];
    });

    // 3. Busca os estábulos
    api.get('quadrants/').then(res => {
      stablesList.value = res.data.results || res.data;
    }).catch(() => {
      stablesList.value = [
        { id: 1, name: 'Estábulo Principal' },
        { id: 2, name: 'Estábulo Sul' }
      ];
    });
  } catch (e) {
    console.error(e);
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
    msgInd.value = 'Erro ao registrar a vacina. Verifique a conexão com o servidor.';
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
    msgLote.value = 'Erro ao vacinar o lote no servidor.';
  } finally {
    loadingBatch.value = false;
    setTimeout(() => { msgLote.value = ''; }, 5000);
  }
};
</script>
