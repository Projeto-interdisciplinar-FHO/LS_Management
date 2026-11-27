<template>
  <AppShell>
    <div class="page">
      <header class="hero registry-hero">
        <div class="hero__bg" aria-hidden="true">
          <img :src="racasHero" alt="" class="hero__img">
          <div class="hero__shade"></div>
        </div>
        <div class="hero__content">
          <div>
            <div class="registry-hero__meta">
              <span class="hero__eyebrow">Cadastros</span>
              <span class="registry-hero__pill">{{ breeds.length }} cadastrada(s)</span>
            </div>
            <h1 class="hero__title">Raças</h1>
            <p class="hero__desc">Raças disponíveis para classificação genética de vacas e touros do rebanho.</p>
          </div>
        </div>
      </header>

      <p v-if="erro" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ erro }}</span>
      </p>

      <section class="registry-toolbar" aria-label="Buscar e cadastrar raças">
        <label v-if="breeds.length > 0" class="search">
          <AppIcon name="search" :size="16" />
          <input
            v-model="busca"
            class="input"
            type="search"
            placeholder="Buscar raça por nome"
            aria-label="Buscar raça"
          >
        </label>
        <span v-if="breeds.length > 0" class="registry-toolbar__count">{{ filtradas.length }} resultado(s)</span>
        <button type="button" class="btn btn--primary" @click="openModal()">
          <AppIcon name="plus" :size="16" />
          Cadastrar raça
        </button>
      </section>

      <RegistryCard
        titulo="Raças cadastradas"
        :total="breeds.length"
        :carregando="loading"
        texto-carregando="Carregando raças..."
        :vazio="breeds.length === 0"
        :vazio-filtrado="breeds.length > 0 && filtradas.length === 0"
        icone-vazio="tag"
        titulo-vazio="Nenhuma raça cadastrada"
        descricao-vazia="A raça é obrigatória na ficha do animal. Cadastre as usadas na fazenda."
        rotulo-acao-vazio="Cadastrar raça"
        descricao-vazio-filtrado="Nenhuma raça corresponde à busca informada."
        @cadastrar="openModal()"
        @limpar-filtros="busca = ''"
      >
        <div class="table-wrap">
          <table class="table">
            <thead>
              <tr>
                <th>Raça</th>
                <th class="cell-actions">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filtradas" :key="item.id">
                <td class="truncate" :title="item.name">
                  <div class="registry-item">
                    <span class="icon-tile icon-tile--warn"><AppIcon name="tag" :size="16" /></span>
                    <span class="registry-item__name">{{ item.name }}</span>
                  </div>
                </td>
                <td class="cell-actions">
                  <div class="registry-actions">
                    <button
                      type="button"
                      class="btn btn--icon"
                      aria-label="Editar raça"
                      title="Editar raça"
                      @click="openModal(item)"
                    >
                      <AppIcon name="edit" :size="15" />
                    </button>
                    <button
                      type="button"
                      class="btn btn--icon is-danger"
                      aria-label="Excluir raça"
                      title="Excluir raça"
                      @click="deleteBreed(item)"
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
        :titulo="editingId ? 'Editar raça' : 'Cadastrar raça'"
        @fechar="closeModal"
      >
        <form id="form-raca" class="stack" @submit.prevent="submitBreed">
          <div class="field">
            <label class="field__label" for="nome-raca">Nome da raça</label>
            <input
              id="nome-raca"
              v-model.trim="form.name"
              class="input"
              type="text"
              placeholder="Ex: Holandesa"
              required
            >
          </div>

          <p v-if="erroModal" class="alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ erroModal }}</span>
          </p>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="closeModal">Cancelar</button>
          <button type="submit" form="form-raca" class="btn btn--primary" :disabled="saving">
            {{ saving ? 'Salvando...' : editingId ? 'Salvar alterações' : 'Cadastrar raça' }}
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
import racasHero from '@/assets/images/racas-hero.jpg';
import { apiErrorMessage } from '@/utils/apiError';

const breeds = ref([]);
const busca = ref('');
const loading = ref(true);
const showModal = ref(false);
const editingId = ref(null);
const saving = ref(false);
const erro = ref('');
const erroModal = ref('');
const form = ref({ name: '' });

const filtradas = computed(() => {
  const termo = busca.value.trim().toLowerCase();
  if (!termo) return breeds.value;
  return breeds.value.filter((item) => String(item.name || '').toLowerCase().includes(termo));
});

const normalizeList = (response) => {
  if (Array.isArray(response.data)) return response.data;
  return response.data?.results || [];
};

const loadBreeds = async () => {
  loading.value = true;
  erro.value = '';
  try {
    const response = await api.get('breeds/');
    breeds.value = normalizeList(response);
  } catch (error) {
    console.error('Erro ao carregar raças:', error);
    breeds.value = [];
    erro.value = apiErrorMessage(error, 'Não foi possível carregar as raças.');
  } finally {
    loading.value = false;
  }
};

const openModal = (breed = null) => {
  editingId.value = breed ? breed.id : null;
  form.value = { name: breed ? breed.name || '' : '' };
  erroModal.value = '';
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingId.value = null;
  erroModal.value = '';
};

const submitBreed = async () => {
  saving.value = true;
  erroModal.value = '';
  try {
    if (editingId.value) {
      await api.put(`breeds/${editingId.value}/`, form.value);
    } else {
      await api.post('breeds/', form.value);
    }
    closeModal();
    await loadBreeds();
  } catch (error) {
    console.error('Erro ao salvar raça:', error);
    erroModal.value = apiErrorMessage(error, 'Não foi possível salvar a raça. Confira os dados e tente novamente.');
  } finally {
    saving.value = false;
  }
};

const deleteBreed = async (breed) => {
  const ok = await confirmar({
    titulo: `Excluir a raça "${breed.name}"?`,
    texto: 'Se houver animais vinculados a esta raça, a exclusão será bloqueada pelo servidor.',
    acao: 'Excluir raça',
  });
  if (!ok) return;
  erro.value = '';
  try {
    await api.delete(`breeds/${breed.id}/`);
    await loadBreeds();
  } catch (error) {
    console.error('Erro ao excluir raça:', error);
    erro.value = apiErrorMessage(error, 'Não foi possível excluir a raça. Verifique se há animais vinculados.');
  }
};

onMounted(() => {
  loadBreeds();
});
</script>
