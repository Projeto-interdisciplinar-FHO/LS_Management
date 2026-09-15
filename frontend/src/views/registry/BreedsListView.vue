<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        titulo="Raças"
        descricao="Raças registradas e a espécie a que cada uma pertence."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      >
        <template #acoes>
          <button class="btn btn--primary" @click="openModal">
            <AppIcon name="plus" :size="16" />
            Adicionar raça
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
          <span class="badge">{{ breeds.length }}</span>
        </header>

        <div v-if="loading" class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Carregando raças...
        </div>

        <div v-else-if="breeds.length === 0" class="empty">
          <AppIcon name="tag" :size="30" />
          <p class="empty__title">Nenhuma raça cadastrada</p>
          <p class="empty__desc">A raça é obrigatória na ficha do animal. Cadastre as usadas na fazenda.</p>
          <button class="btn btn--primary" @click="openModal">Adicionar raça</button>
        </div>

        <div v-else class="list">
          <article v-for="item in breeds" :key="item.id" class="list__item">
            <div class="list__main">
              <span class="icon-tile icon-tile--warn"><AppIcon name="tag" :size="16" /></span>
              <div>
                <span class="list__title">{{ item.name }}</span>
                <span class="list__sub">{{ item.specie_name || 'Espécie não informada' }}</span>
              </div>
            </div>
          </article>
        </div>
      </section>

      <AppModal v-if="showModal" titulo="Nova raça" @fechar="showModal = false">
        <form id="form-raca" class="stack" @submit.prevent="submitBreed">
          <div class="field">
            <label class="field__label" for="nome-raca">Nome da raça</label>
            <input id="nome-raca" v-model="form.name" class="input" type="text" placeholder="Ex: Nelore" required>
          </div>

          <div class="field">
            <label class="field__label" for="especie-raca">Espécie</label>
            <select id="especie-raca" v-model="form.specie" class="select" required>
              <option value="" disabled>Selecione uma espécie...</option>
              <option v-for="specie in species" :key="specie.id" :value="specie.id">
                {{ specie.name }}
              </option>
            </select>
            <span v-if="!species.length" class="field__hint">
              Nenhuma espécie cadastrada ainda — cadastre uma antes de criar a raça.
            </span>
          </div>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="showModal = false">Cancelar</button>
          <button type="submit" form="form-raca" class="btn btn--primary" :disabled="saving">
            {{ saving ? 'Salvando...' : 'Salvar raça' }}
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

const breeds = ref([]);
const species = ref([]);
const loading = ref(false);
const showModal = ref(false);
const saving = ref(false);
const erro = ref('');
const form = ref({ name: '', specie: '' });

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
    erro.value = 'Não foi possível carregar as raças.';
  } finally {
    loading.value = false;
  }
};

const loadSpecies = async () => {
  try {
    const response = await api.get('species/');
    species.value = normalizeList(response);
  } catch (error) {
    console.error('Erro ao carregar espécies:', error);
    species.value = [];
  }
};

const openModal = async () => {
  form.value = { name: '', specie: '' };
  await loadSpecies();
  showModal.value = true;
};

const submitBreed = async () => {
  saving.value = true;
  try {
    await api.post('breeds/', form.value);
    notify('Raça cadastrada com sucesso.', 'success');
    showModal.value = false;
    await loadBreeds();
  } catch (error) {
    console.error('Erro ao cadastrar raça:', error);
    notify('Erro ao cadastrar raça.', 'error');
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadBreeds();
  loadSpecies();
});
</script>
