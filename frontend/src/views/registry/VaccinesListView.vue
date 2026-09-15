<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        titulo="Vacinas"
        descricao="Catálogo de vacinas disponíveis para aplicação no manejo sanitário."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      >
        <template #acoes>
          <button class="btn btn--primary" @click="openModal">
            <AppIcon name="plus" :size="16" />
            Adicionar vacina
          </button>
        </template>
      </PageHeader>

      <p v-if="erro" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ erro }}</span>
      </p>

      <section class="card">
        <header class="card__head">
          <h2 class="card__title">Cadastradas</h2>
          <span class="badge">{{ vaccines.length }}</span>
        </header>

        <div v-if="loading" class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Carregando vacinas...
        </div>

        <div v-else-if="vaccines.length === 0" class="empty">
          <AppIcon name="syringe" :size="30" />
          <p class="empty__title">Nenhuma vacina cadastrada</p>
          <p class="empty__desc">Sem vacina no catálogo, a tela de vacinação fica sem opções para escolher.</p>
          <button class="btn btn--primary" @click="openModal">Adicionar vacina</button>
        </div>

        <div v-else class="list">
          <article v-for="item in vaccines" :key="item.id" class="list__item">
            <div class="list__main">
              <span class="icon-tile icon-tile--info"><AppIcon name="syringe" :size="16" /></span>
              <div>
                <span class="list__title">{{ item.name }}</span>
                <span class="list__sub">{{ item.description || 'Sem descrição' }}</span>
              </div>
            </div>
          </article>
        </div>
      </section>

      <AppModal v-if="showModal" titulo="Nova vacina" @fechar="showModal = false">
        <form id="form-vacina" class="stack" @submit.prevent="submitVaccine">
          <div class="field">
            <label class="field__label" for="nome-vacina">Nome da vacina</label>
            <input id="nome-vacina" v-model="form.name" class="input" type="text" placeholder="Ex: Brucelose" required>
          </div>

          <div class="field">
            <label class="field__label" for="desc-vacina">Descrição</label>
            <input id="desc-vacina" v-model="form.description" class="input" type="text" placeholder="Opcional — fabricante, dose de referência">
          </div>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="showModal = false">Cancelar</button>
          <button type="submit" form="form-vacina" class="btn btn--primary" :disabled="saving">
            {{ saving ? 'Salvando...' : 'Salvar vacina' }}
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
import { notify } from '@/services/notificationService';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppModal from '@/components/ui/AppModal.vue';
import PageHeader from '@/components/layout/PageHeader.vue';

const painel = computed(() => painelDoPapel());

const vaccines = ref([]);
const loading = ref(false);
const showModal = ref(false);
const saving = ref(false);
const erro = ref('');
const form = ref({ name: '', description: '' });

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
    erro.value = 'Não foi possível carregar as vacinas.';
  } finally {
    loading.value = false;
  }
};

const openModal = () => {
  form.value = { name: '', description: '' };
  showModal.value = true;
};

const submitVaccine = async () => {
  saving.value = true;
  try {
    await api.post('vaccines/', form.value);
    notify('Vacina cadastrada com sucesso.', 'success');
    showModal.value = false;
    await loadVaccines();
  } catch (error) {
    console.error('Erro ao cadastrar vacina:', error);
    notify('Erro ao cadastrar vacina.', 'error');
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadVaccines();
});
</script>
