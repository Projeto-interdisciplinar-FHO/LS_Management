<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        titulo="Espécies"
        descricao="Base taxonômica do rebanho. Cada raça cadastrada pertence a uma espécie."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      >
        <template #acoes>
          <button class="btn btn--primary" @click="openModal">
            <AppIcon name="plus" :size="16" />
            Adicionar espécie
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
          <span class="badge">{{ species.length }}</span>
        </header>

        <div v-if="loading" class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Carregando espécies...
        </div>

        <div v-else-if="species.length === 0" class="empty">
          <AppIcon name="dna" :size="30" />
          <p class="empty__title">Nenhuma espécie cadastrada</p>
          <p class="empty__desc">Cadastre ao menos uma espécie antes de registrar raças e animais.</p>
          <button class="btn btn--primary" @click="openModal">Adicionar espécie</button>
        </div>

        <div v-else class="list">
          <article v-for="item in species" :key="item.id" class="list__item">
            <div class="list__main">
              <span class="icon-tile icon-tile--accent"><AppIcon name="dna" :size="16" /></span>
              <div>
                <span class="list__title">{{ item.name }}</span>
                <span class="list__sub">{{ item.breeds_count ?? 0 }} raças vinculadas</span>
              </div>
            </div>
          </article>
        </div>
      </section>

      <AppModal v-if="showModal" titulo="Nova espécie" @fechar="showModal = false">
        <form id="form-especie" class="stack" @submit.prevent="submitSpecie">
          <div class="field">
            <label class="field__label" for="nome-especie">Nome da espécie</label>
            <input id="nome-especie" v-model="form.name" class="input" type="text" placeholder="Ex: Bovino" required>
          </div>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="showModal = false">Cancelar</button>
          <button type="submit" form="form-especie" class="btn btn--primary" :disabled="saving">
            {{ saving ? 'Salvando...' : 'Salvar espécie' }}
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

const species = ref([]);
const loading = ref(false);
const showModal = ref(false);
const saving = ref(false);
const erro = ref('');
const form = ref({ name: '' });

const normalizeList = (response) => {
  if (Array.isArray(response.data)) return response.data;
  return response.data?.results || [];
};

const loadSpecies = async () => {
  loading.value = true;
  erro.value = '';
  try {
    const response = await api.get('species/');
    species.value = normalizeList(response);
  } catch (error) {
    console.error('Erro ao carregar espécies:', error);
    species.value = [];
    // Era um alert() do navegador: travava a tela e não deixava rastro.
    erro.value = 'Não foi possível carregar as espécies.';
  } finally {
    loading.value = false;
  }
};

const openModal = () => {
  form.value = { name: '' };
  showModal.value = true;
};

const submitSpecie = async () => {
  saving.value = true;
  try {
    await api.post('species/', form.value);
    notify('Espécie cadastrada com sucesso.', 'success');
    showModal.value = false;
    await loadSpecies();
  } catch (error) {
    console.error('Erro ao cadastrar espécie:', error);
    notify('Erro ao cadastrar espécie.', 'error');
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadSpecies();
});
</script>
