<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        :titulo="isEdit ? 'Editar animal' : 'Cadastrar animal'"
        :descricao="isEdit ? 'Altere os dados da ficha e salve.' : 'Preencha a ficha do animal para incluí-lo no rebanho.'"
        voltar-rotulo="Animais"
        voltar-para="/animais"
      />

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
              <label class="field__label" for="raca">Raça</label>
              <select id="raca" v-model="formData.breed" class="select" required>
                <option value="" disabled>Selecione uma raça...</option>
                <option v-for="breed in breedsList" :key="breed.id" :value="breed.id">
                  {{ breed.name }}
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
            <button type="submit" class="btn btn--primary" :disabled="loading">
              {{ loading ? 'Salvando...' : (isEdit ? 'Salvar alterações' : 'Cadastrar animal') }}
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
import PageHeader from '@/components/layout/PageHeader.vue';

const route = useRoute();
const router = useRouter();

const isEdit = ref(false);
const loading = ref(false);

const breedsList = ref([]);

const formData = ref({
  name: '', register_number: '', status: 'active', score: 0,
  reproductive_status: true, breed: '', birth: null
});

onMounted(async () => {
  // Carrega as listas dos menus suspensos
  fetchDropdownData();

  if (route.params.id) {
    isEdit.value = true;
    try {
      const response = await api.get(`animals/${route.params.id}/`);
      formData.value = response.data;
    } catch (error) {
      console.error("Erro ao carregar animal:", error);
    }
  }
});

const fetchDropdownData = async () => {
  try {
    api.get('breeds/').then(res => breedsList.value = res.data).catch(() => {
      breedsList.value = [];
    });
  } catch (e) {
    console.error(e);
  }
};

const saveAnimal = async () => {
  loading.value = true;
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
  } finally {
    loading.value = false;
  }
};
</script>
