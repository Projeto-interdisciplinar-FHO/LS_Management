<template>
  <AppShell>
    <div class="page">
      <header class="hero registry-hero">
        <div class="hero__bg" aria-hidden="true">
          <img :src="vacinasHero" alt="" class="hero__img">
          <div class="hero__shade"></div>
        </div>
        <div class="hero__content">
          <div>
            <div class="registry-hero__meta">
              <span class="hero__eyebrow">Cadastros · Saúde</span>
              <span class="registry-hero__pill">{{ vaccines.length }} cadastrada(s)</span>
            </div>
            <h1 class="hero__title">Vacinas</h1>
            <p class="hero__desc">Catálogo de vacinas disponíveis para aplicação e controle no manejo sanitário.</p>
          </div>
        </div>
      </header>

      <p v-if="erro" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ erro }}</span>
      </p>

      <section class="registry-toolbar" aria-label="Buscar e cadastrar vacinas">
        <label v-if="vaccines.length > 0" class="search">
          <AppIcon name="search" :size="16" />
          <input
            v-model="busca"
            class="input"
            type="search"
            placeholder="Buscar vacina por nome ou descrição"
            aria-label="Buscar vacina"
          >
        </label>
        <span v-if="vaccines.length > 0" class="registry-toolbar__count">{{ filtradas.length }} resultado(s)</span>
        <button type="button" class="btn btn--primary" @click="openModal()">
          <AppIcon name="plus" :size="16" />
          Cadastrar vacina
        </button>
      </section>

      <RegistryCard
        titulo="Vacinas cadastradas"
        :total="vaccines.length"
        :carregando="loading"
        texto-carregando="Carregando vacinas..."
        :vazio="vaccines.length === 0"
        :vazio-filtrado="vaccines.length > 0 && filtradas.length === 0"
        icone-vazio="syringe"
        titulo-vazio="Nenhuma vacina cadastrada"
        descricao-vazia="Sem vacina no catálogo, a tela de vacinação fica sem opções para escolher."
        rotulo-acao-vazio="Cadastrar vacina"
        descricao-vazio-filtrado="Nenhuma vacina corresponde à busca informada."
        @cadastrar="openModal()"
        @limpar-filtros="busca = ''"
      >
        <div class="table-wrap">
          <table class="table">
            <thead>
              <tr>
                <th>Vacina</th>
                <th>Descrição</th>
                <th class="cell-actions">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filtradas" :key="item.id">
                <td class="truncate" :title="item.name">
                  <div class="registry-item">
                    <span class="icon-tile icon-tile--info"><AppIcon name="syringe" :size="16" /></span>
                    <span class="registry-item__name">{{ item.name }}</span>
                  </div>
                </td>
                <td class="text-muted truncate" :title="item.description || 'Sem descrição'">
                  {{ item.description || '—' }}
                </td>
                <td class="cell-actions">
                  <div class="registry-actions">
                    <button
                      type="button"
                      class="btn btn--icon"
                      aria-label="Editar vacina"
                      title="Editar vacina"
                      @click="openModal(item)"
                    >
                      <AppIcon name="edit" :size="15" />
                    </button>
                    <button
                      type="button"
                      class="btn btn--icon is-danger"
                      aria-label="Excluir vacina"
                      title="Excluir vacina"
                      @click="deleteVaccine(item)"
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
        :titulo="editingId ? 'Editar vacina' : 'Cadastrar vacina'"
        @fechar="closeModal"
      >
        <form id="form-vacina" class="stack" @submit.prevent="submitVaccine">
          <div class="field">
            <label class="field__label" for="nome-vacina">Nome da vacina</label>
            <input
              id="nome-vacina"
              v-model.trim="form.name"
              class="input"
              type="text"
              placeholder="Ex: Brucelose"
              required
            >
          </div>

          <div class="field">
            <label class="field__label" for="desc-vacina">Descrição</label>
            <input
              id="desc-vacina"
              v-model.trim="form.description"
              class="input"
              type="text"
              placeholder="Opcional — fabricante, dose de referência"
            >
          </div>

          <p v-if="erroModal" class="alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ erroModal }}</span>
          </p>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="closeModal">Cancelar</button>
          <button type="submit" form="form-vacina" class="btn btn--primary" :disabled="saving">
            {{ saving ? 'Salvando...' : editingId ? 'Salvar alterações' : 'Cadastrar vacina' }}
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
import vacinasHero from '@/assets/images/vacinas-hero.jpg';
import { apiErrorMessage } from '@/utils/apiError';

const vaccines = ref([]);
const busca = ref('');
const loading = ref(true);
const showModal = ref(false);
const editingId = ref(null);
const saving = ref(false);
const erro = ref('');
const erroModal = ref('');
const form = ref({ name: '', description: '' });

const filtradas = computed(() => {
  const termo = busca.value.trim().toLowerCase();
  if (!termo) return vaccines.value;
  return vaccines.value.filter((item) =>
    String(item.name || '').toLowerCase().includes(termo)
    || String(item.description || '').toLowerCase().includes(termo)
  );
});

const normalizeList = (response) => {
  if (Array.isArray(response.data)) return response.data;
  return response.data?.results || [];
};

const loadVaccines = async () => {
  loading.value = true;
  erro.value = '';
  try {
    const response = await api.get('vaccines/');
    vaccines.value = normalizeList(response);
  } catch (error) {
    console.error('Erro ao carregar vacinas:', error);
    vaccines.value = [];
    erro.value = apiErrorMessage(error, 'Não foi possível carregar as vacinas.');
  } finally {
    loading.value = false;
  }
};

const openModal = (vaccine = null) => {
  editingId.value = vaccine ? vaccine.id : null;
  form.value = {
    name: vaccine ? vaccine.name || '' : '',
    description: vaccine ? vaccine.description || '' : '',
  };
  erroModal.value = '';
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingId.value = null;
  erroModal.value = '';
};

const submitVaccine = async () => {
  saving.value = true;
  erroModal.value = '';
  try {
    if (editingId.value) {
      await api.put(`vaccines/${editingId.value}/`, form.value);
    } else {
      await api.post('vaccines/', form.value);
    }
    closeModal();
    await loadVaccines();
  } catch (error) {
    console.error('Erro ao salvar vacina:', error);
    erroModal.value = apiErrorMessage(error, 'Não foi possível salvar a vacina. Confira o nome e tente novamente.');
  } finally {
    saving.value = false;
  }
};

const deleteVaccine = async (vaccine) => {
  const ok = await confirmar({
    titulo: `Excluir a vacina "${vaccine.name}"?`,
    texto: 'Esta ação remove a vacina do catálogo de manejo sanitário.',
    acao: 'Excluir vacina',
  });
  if (!ok) return;
  erro.value = '';
  try {
    await api.delete(`vaccines/${vaccine.id}/`);
    await loadVaccines();
  } catch (error) {
    console.error('Erro ao excluir vacina:', error);
    erro.value = apiErrorMessage(error, 'Não foi possível excluir a vacina.');
  }
};

onMounted(() => {
  loadVaccines();
});
</script>
