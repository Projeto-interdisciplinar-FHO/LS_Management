<template>
  <AppShell>
    <div class="page">
      <header class="hero registry-hero">
        <div class="hero__bg" aria-hidden="true">
          <img :src="alimentosHero" alt="" class="hero__img">
          <div class="hero__shade"></div>
        </div>
        <div class="hero__content">
          <div>
            <div class="registry-hero__meta">
              <span class="hero__eyebrow">Cadastros · Nutrição</span>
              <span class="registry-hero__pill">{{ foodsList.length }} cadastrado(s)</span>
            </div>
            <h1 class="hero__title">Alimentos e insumos</h1>
            <p class="hero__desc">Rações, silagens e suplementos disponíveis para lançamento no trato diário.</p>
          </div>
        </div>
      </header>

      <p v-if="errorMessage" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ errorMessage }}</span>
      </p>

      <section class="registry-toolbar" aria-label="Buscar e cadastrar alimentos">
        <label v-if="foodsList.length > 0" class="search">
          <AppIcon name="search" :size="16" />
          <input
            v-model="busca"
            class="input"
            type="search"
            placeholder="Buscar alimento por nome ou composição"
            aria-label="Buscar alimento"
          >
        </label>
        <span v-if="foodsList.length > 0" class="registry-toolbar__count">{{ filtrados.length }} resultado(s)</span>
        <button type="button" class="btn btn--primary" @click="openModal()">
          <AppIcon name="plus" :size="16" />
          Cadastrar alimento
        </button>
      </section>

      <RegistryCard
        titulo="Alimentos cadastrados"
        :total="foodsList.length"
        :carregando="loading"
        texto-carregando="Carregando insumos..."
        :vazio="foodsList.length === 0"
        :vazio-filtrado="foodsList.length > 0 && filtrados.length === 0"
        icone-vazio="feed"
        titulo-vazio="Nenhum alimento cadastrado"
        descricao-vazia="Cadastre as rações e suplementos usados para poder lançar o trato no campo."
        rotulo-acao-vazio="Cadastrar alimento"
        descricao-vazio-filtrado="Nenhum alimento corresponde à busca informada."
        @cadastrar="openModal()"
        @limpar-filtros="busca = ''"
      >
        <div class="table-wrap">
          <table class="table">
            <thead>
              <tr>
                <th>Alimento</th>
                <th>Fabricante ou composição</th>
                <th class="cell-actions">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="food in filtrados" :key="food.id">
                <td class="truncate" :title="food.name">
                  <div class="registry-item">
                    <span class="icon-tile icon-tile--accent"><AppIcon name="feed" :size="16" /></span>
                    <span class="registry-item__name">{{ food.name }}</span>
                  </div>
                </td>
                <td class="text-muted truncate" :title="food.description || '—'">{{ food.description || '—' }}</td>
                <td class="cell-actions">
                  <div class="registry-actions">
                    <button
                      type="button"
                      class="btn btn--icon"
                      aria-label="Editar alimento"
                      title="Editar alimento"
                      @click="openModal(food)"
                    >
                      <AppIcon name="edit" :size="15" />
                    </button>
                    <button
                      type="button"
                      class="btn btn--icon is-danger"
                      aria-label="Excluir alimento"
                      title="Excluir alimento"
                      @click="deleteFood(food)"
                    >
                      <AppIcon name="trash" :size="15" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </RegistryCard>

      <AppModal
        v-if="showModal"
        :titulo="editingId ? 'Editar alimento' : 'Cadastrar alimento'"
        @fechar="closeModal"
      >
        <form id="form-alimento" class="stack" @submit.prevent="submitFood">
          <div class="field">
            <label class="field__label" for="nome-alimento">Nome comercial</label>
            <input
              id="nome-alimento"
              v-model.trim="foodForm.name"
              class="input"
              type="text"
              placeholder="Ex: Ração Lactação Premium"
              required
            >
          </div>

          <div class="field">
            <label class="field__label" for="desc-alimento">Fabricante ou composição</label>
            <input
              id="desc-alimento"
              v-model.trim="foodForm.description"
              class="input"
              type="text"
              placeholder="Ex: Milho e soja com minerais"
            >
          </div>

          <p v-if="formError" class="alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ formError }}</span>
          </p>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="closeModal">Cancelar</button>
          <button type="submit" form="form-alimento" class="btn btn--primary" :disabled="savingFeed">
            {{ savingFeed ? 'Salvando...' : editingId ? 'Salvar alterações' : 'Cadastrar alimento' }}
          </button>
        </template>
      </AppModal>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';
import { confirmar } from '@/services/confirmService';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppModal from '@/components/ui/AppModal.vue';
import RegistryCard from '@/components/layout/RegistryCard.vue';
import alimentosHero from '@/assets/images/alimentos-hero.jpg';
import { apiErrorMessage } from '@/utils/apiError';

const loading = ref(true);
const savingFeed = ref(false);
const showModal = ref(false);
const editingId = ref(null);
const errorMessage = ref('');
const formError = ref('');
const busca = ref('');

const foodsList = ref([]);
const foodForm = ref({ name: '', description: '' });

const filtrados = computed(() => {
  const termo = busca.value.trim().toLowerCase();
  if (!termo) return foodsList.value;
  return foodsList.value.filter((item) =>
    String(item.name || '').toLowerCase().includes(termo)
    || String(item.description || '').toLowerCase().includes(termo)
  );
});

onMounted(() => {
  loadFoodsList();
});

const loadFoodsList = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    const historyRes = await api.get('foods/');
    foodsList.value = historyRes.data.results || historyRes.data;
  } catch (error) {
    console.error('Erro ao puxar dados alimentares:', error);
    foodsList.value = [];
    errorMessage.value = apiErrorMessage(error, 'Não foi possível carregar os alimentos.');
  } finally {
    loading.value = false;
  }
};

const openModal = (food = null) => {
  editingId.value = food ? food.id : null;
  foodForm.value = {
    name: food ? food.name || '' : '',
    description: food ? food.description || '' : '',
  };
  formError.value = '';
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingId.value = null;
  formError.value = '';
};

const submitFood = async () => {
  savingFeed.value = true;
  formError.value = '';
  try {
    if (editingId.value) {
      await api.put(`foods/${editingId.value}/`, foodForm.value);
    } else {
      await api.post('foods/', foodForm.value);
    }
    closeModal();
    await loadFoodsList();
  } catch (error) {
    console.error(error);
    formError.value = apiErrorMessage(error, 'Não foi possível salvar o alimento. Confira os dados e tente novamente.');
  } finally {
    savingFeed.value = false;
  }
};

const deleteFood = async (food) => {
  const ok = await confirmar({
    titulo: `Excluir o alimento "${food.name}"?`,
    texto: 'Esta ação remove o insumo do catálogo de alimentação.',
    acao: 'Excluir alimento',
  });
  if (!ok) return;
  errorMessage.value = '';
  try {
    await api.delete(`foods/${food.id}/`);
    await loadFoodsList();
  } catch (error) {
    console.error('Erro ao excluir alimento:', error);
    errorMessage.value = apiErrorMessage(error, 'Não foi possível excluir o alimento.');
  }
};
</script>
