<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        titulo="Alimentos e insumos"
        descricao="Rações e suplementos disponíveis para lançamento no trato diário."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      >
        <template #acoes>
          <button class="btn btn--primary" @click="showAddFeedModal = true">
            <AppIcon name="plus" :size="16" />
            Novo alimento
          </button>
        </template>
      </PageHeader>

      <section class="card">
        <header class="card__head">
          <h2 class="card__title">Cadastrados</h2>
          <span class="badge">{{ foodsList.length }}</span>
        </header>

        <div v-if="loading" class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Carregando insumos...
        </div>

        <div v-else-if="foodsList.length === 0" class="empty">
          <AppIcon name="feed" :size="30" />
          <p class="empty__title">Nenhum alimento cadastrado</p>
          <p class="empty__desc">Cadastre as rações e suplementos usados para poder lançar o trato no campo.</p>
          <button class="btn btn--primary" @click="showAddFeedModal = true">Novo alimento</button>
        </div>

        <div v-else class="table-wrap">
          <table class="table">
            <thead>
              <tr>
                <th>Nome</th>
                <th>Fabricante ou composição</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="food in foodsList" :key="food.id">
                <td class="cell-strong">{{ food.name }}</td>
                <td class="text-muted">{{ food.description || '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <AppModal v-if="showAddFeedModal" titulo="Novo alimento" @fechar="showAddFeedModal = false">
        <form id="form-alimento" class="stack" @submit.prevent="submitNewFeed">
          <div class="field">
            <label class="field__label" for="nome-alimento">Nome comercial</label>
            <input id="nome-alimento" v-model="newFeedForm.name" class="input" type="text" placeholder="Ex: Ração Lactação Premium" required>
          </div>

          <div class="field">
            <label class="field__label" for="desc-alimento">Fabricante ou composição</label>
            <input id="desc-alimento" v-model="newFeedForm.description" class="input" type="text" placeholder="Ex: Milho e soja com minerais">
          </div>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="showAddFeedModal = false">Cancelar</button>
          <button type="submit" form="form-alimento" class="btn btn--primary" :disabled="savingFeed">
            {{ savingFeed ? 'Salvando...' : 'Cadastrar alimento' }}
          </button>
        </template>
      </AppModal>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';
import { painelDoPapel } from '@/services/auth';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppModal from '@/components/ui/AppModal.vue';
import PageHeader from '@/components/layout/PageHeader.vue';

const painel = computed(() => painelDoPapel());

const loading = ref(true);
const savingFeed = ref(false);
const showAddFeedModal = ref(false);

const foodsList = ref([]);
const newFeedForm = ref({ name: '', description: '' });

onMounted(() => {
  loadFoodsList();
});

const loadFoodsList = async () => {
  loading.value = true;
  try {
    const historyRes = await api.get('foods/');
    foodsList.value = historyRes.data.results || historyRes.data;
  } catch (error) {
    console.error("Erro ao puxar dados alimentares:", error);
  } finally {
    loading.value = false;
  }
};

const submitNewFeed = async () => {
  savingFeed.value = true;
  try {
    await api.post('foods/', newFeedForm.value);
    showAddFeedModal.value = false;
    newFeedForm.value = { name: '', description: '' };
    loadFoodsList();
  } catch (error) {
    console.error(error);
  } finally {
    savingFeed.value = false;
  }
};
</script>
