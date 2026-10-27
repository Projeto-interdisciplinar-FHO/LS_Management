<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        :titulo="isEdit ? 'Editar animal' : 'Cadastrar animal'"
        :descricao="isEdit ? 'Altere os dados da ficha e salve.' : 'Preencha a ficha do animal para incluí-lo no rebanho.'"
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

      <form class="stack-24" @submit.prevent="saveAnimal">
        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Identificação</h2>
              <p class="card__desc">Como o animal é reconhecido no curral e no sistema.</p>
            </div>
          </header>

          <div class="card__body grid grid--2">
            <div class="field">
              <label class="field__label" for="nome">Nome ou apelido</label>
              <input id="nome" v-model="formData.name" class="input" type="text" placeholder="Ex: Mimosa" required>
            </div>

            <div class="field">
              <label class="field__label" for="brinco">Nº de registro (brinco)</label>
              <input id="brinco" v-model="formData.register_number" class="input" type="number" placeholder="Ex: 142" required>
            </div>

            <div class="field">
              <label class="field__label" for="situacao">Situação</label>
              <select id="situacao" v-model="formData.status" class="select">
                <option value="active">Ativa</option>
                <option value="inactive">Inativa</option>
                <option value="sold">Vendida</option>
                <option value="deceased">Óbito</option>
              </select>
            </div>
          </div>
        </section>

        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Classificação e localização</h2>
              <p class="card__desc">Origem biológica do animal e onde ele fica alojado.</p>
            </div>
          </header>

          <div class="card__body grid grid--2">
            <div class="field">
              <label class="field__label" for="especie">Espécie</label>
              <select id="especie" v-model="formData.specie" class="select" required :disabled="loadingOptions">
                <option value="" disabled>{{ loadingOptions ? 'Carregando espécies...' : 'Selecione uma espécie...' }}</option>
                <option v-for="specie in speciesList" :key="specie.id" :value="specie.id">
                  {{ specie.name }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="raca">Raça</label>
              <select id="raca" v-model="formData.breed" class="select" required :disabled="loadingOptions">
                <option value="" disabled>{{ loadingOptions ? 'Carregando raças...' : 'Selecione uma raça...' }}</option>
                <option v-for="breed in breedsList" :key="breed.id" :value="breed.id">
                  {{ breed.name }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="estabulo">Estábulo</label>
              <select id="estabulo" v-model="formData.quadrant" class="select" required :disabled="loadingOptions">
                <option value="" disabled>{{ loadingOptions ? 'Carregando estábulos...' : 'Selecione um estábulo...' }}</option>
                <option v-for="stable in stablesList" :key="stable.id" :value="stable.id">
                  {{ stable.name || stable.nome_quadrante || `Estábulo ${stable.id}` }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="finalidade">Finalidade</label>
              <select id="finalidade" v-model="formData.purpose" class="select" required :disabled="loadingOptions">
                <option value="" disabled>{{ loadingOptions ? 'Carregando finalidades...' : 'Selecione a finalidade...' }}</option>
                <option v-for="purpose in purposeList" :key="purpose.id" :value="purpose.id">
                  {{ purpose.name || purpose.tipo || `Finalidade ${purpose.id}` }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="escore">Escore corporal</label>
              <input id="escore" v-model.number="formData.score" class="input" type="number" min="0" step="0.01">
            </div>

            <div class="field">
              <label class="field__label" for="reproductive-status">Status reprodutivo</label>
              <select id="reproductive-status" v-model="formData.reproductive_status" class="select">
                <option :value="true">Apto</option>
                <option :value="false">Inapto</option>
              </select>
            </div>
          </div>

          <footer class="card__foot">
            <button type="button" class="btn" @click="$router.back()">Cancelar</button>
            <button type="submit" class="btn btn--primary" :disabled="loading || loadingOptions || loadingRecord">
              {{ loading ? 'Salvando...' : loadingRecord ? 'Carregando animal...' : loadingOptions ? 'Carregando cadastros...' : (isEdit ? 'Salvar alterações' : 'Cadastrar animal') }}
            </button>
          </footer>
        </section>
      </form>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { SITUACOES, ativoPara } from '@/utils/statusUtils';
import { apiErrorMessage } from '@/utils/apiError';

const route = useRoute();
const router = useRouter();

const isEdit = ref(false);
const loading = ref(false);
const loadingOptions = ref(true);
const loadingRecord = ref(false);
const optionsError = ref('');
const formMessage = ref('');

const breedsList = ref([]);

const formData = ref({
  name: '', register_number: '', status: 'active', score: 0,
  reproductive_status: true, breed: '', birth: null
});

onMounted(async () => {
  fetchDropdownData();

  if (route.params.id) {
    isEdit.value = true;
    loadingRecord.value = true;
    try {
      const response = await api.get(`animals/${route.params.id}/`);
      formData.value = response.data;
    } catch (error) {
      console.error("Erro ao carregar animal:", error);
      formMessage.value = apiErrorMessage(error, 'Não foi possível carregar os dados deste animal.');
    } finally {
      loadingRecord.value = false;
    }
  }
});

const fetchDropdownData = async () => {
  loadingOptions.value = true;
  optionsError.value = '';
  const destinations = [speciesList, breedsList, purposeList, stablesList];
  const labels = ['espécies', 'raças', 'finalidades', 'estábulos'];

  try {
    const responses = await Promise.allSettled([
      api.get('species/'),
      api.get('breeds/'),
      api.get('purpose_types/'),
      api.get('quadrants/'),
    ]);
    const failedLabels = [];

    responses.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        const data = result.value.data;
        destinations[index].value = data?.results || data || [];
      } else {
        destinations[index].value = [];
        failedLabels.push(labels[index]);
      }
    });

    if (failedLabels.length) {
      optionsError.value = `Não foi possível carregar ${failedLabels.join(', ')}. Verifique a conexão e tente novamente.`;
    }
  } catch (e) {
    console.error(e);
    optionsError.value = apiErrorMessage(e, 'Não foi possível carregar os cadastros do formulário.');
  } finally {
    loadingOptions.value = false;
  }
};

const saveAnimal = async () => {
  loading.value = true;
  formMessage.value = '';
  try {
    // O booleano legado `active` sai do `status` — a tela não tem dois
    // controles para a mesma coisa, mas o backend continua recebendo os dois.
    const dados = { ...formData.value, register_number: Number(formData.value.register_number) };

    if (isEdit.value) {
      await api.put(`animals/${route.params.id}/`, dados);
    } else {
      await api.post('animals/', dados);
    }
    router.push('/animais');
  } catch (error) {
    console.error("Erro ao salvar:", error);
    formMessage.value = apiErrorMessage(error, 'Confira os dados do animal e tente novamente.');
  } finally {
    loading.value = false;
  }
};
</script>
