<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Estábulos"
        descricao="Instalações cadastradas na fazenda com capacidade, área e finalidade."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      >
        <template #acoes>
          <button type="button" class="btn btn--primary" @click="openCreateModal">
            <AppIcon name="plus" :size="16" />
            Cadastrar estábulo
          </button>
        </template>
      </PageHeader>

      <p v-if="erro && stables.length" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ erro }}</span>
      </p>

      <section v-if="stables.length > 0" class="registry-toolbar" aria-label="Buscar estábulos">
        <label class="search">
          <AppIcon name="search" :size="16" />
          <input
            v-model="busca"
            class="input"
            type="search"
            placeholder="Buscar estábulo por nome ou propósito"
            aria-label="Buscar estábulo"
          >
        </label>
        <span class="registry-toolbar__count">{{ filteredStables.length }} resultado(s)</span>
      </section>

      <RegistryCard
        titulo="Estábulos cadastrados"
        :total="stables.length"
        :carregando="loading"
        texto-carregando="Carregando estábulos..."
        :vazio="!loading && stables.length === 0"
        :vazio-filtrado="!loading && stables.length > 0 && filteredStables.length === 0"
        :icone-vazio="erro ? 'alert' : 'barn'"
        :titulo-vazio="erro ? 'Não foi possível carregar' : 'Nenhum estábulo cadastrado'"
        :descricao-vazia="erro || 'Cadastre as instalações da fazenda para organizar o rebanho.'"
        :rotulo-acao-vazio="erro ? '' : 'Cadastrar estábulo'"
        descricao-vazio-filtrado="Nenhum estábulo corresponde à busca informada."
        @cadastrar="openCreateModal"
        @limpar-filtros="busca = ''"
      >
        <template v-if="erro" #acao-vazio>
          <button type="button" class="btn" @click="loadData">Tentar de novo</button>
        </template>

        <div class="table-wrap">
          <table class="table">
            <thead>
              <tr>
                <th>Estábulo</th>
                <th>Propósito</th>
                <th>Capacidade</th>
                <th>Área</th>
                <th class="cell-actions">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="stable in filteredStables" :key="stable.id">
                <td class="truncate" :title="stable.name || `Estábulo ${stable.id}`">
                  <div class="registry-item">
                    <span class="icon-tile icon-tile--accent"><AppIcon name="barn" :size="16" /></span>
                    <span class="registry-item__name">{{ stable.name || `Estábulo ${stable.id}` }}</span>
                  </div>
                </td>
                <td class="text-muted truncate" :title="stable.description || 'Manejo geral'">
                  {{ stable.description || 'Manejo geral' }}
                </td>
                <td class="mono nowrap">{{ stable.max_animals }} cabeças</td>
                <td class="mono nowrap">{{ formatArea(stable.area) }}</td>
                <td class="cell-actions">
                  <div class="registry-actions">
                    <button
                      type="button"
                      class="btn btn--icon"
                      aria-label="Editar instalação"
                      title="Editar instalação"
                      @click="editStable(stable)"
                    >
                      <AppIcon name="edit" :size="15" />
                    </button>
                    <button
                      type="button"
                      class="btn btn--icon is-danger"
                      aria-label="Excluir instalação"
                      title="Excluir instalação"
                      @click="deleteStable(stable)"
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
        :titulo="isEditingStable ? 'Editar estábulo' : 'Cadastrar estábulo'"
        @fechar="showModal = false"
      >
        <form id="form-estabulo" class="stack" @submit.prevent="saveStable">
          <div class="field">
            <label class="field__label" for="nome-estabulo">Nome do estábulo</label>
            <input
              id="nome-estabulo"
              v-model.trim="stableForm.name"
              class="input"
              type="text"
              placeholder="Ex: Estábulo de ordenha B"
              required
            >
          </div>

          <div class="grid grid--2">
            <div class="field">
              <label class="field__label" for="capacidade">Capacidade (cabeças)</label>
              <input
                id="capacidade"
                v-model.number="stableForm.max_animals"
                class="input"
                type="number"
                min="1"
                placeholder="50"
                required
              >
            </div>

            <div class="field">
              <label class="field__label" for="area">Área (hectares)</label>
              <input
                id="area"
                v-model="stableForm.area"
                class="input"
                type="number"
                step="0.01"
                min="0"
                placeholder="12.50"
                required
              >
            </div>
          </div>

          <div class="field">
            <label class="field__label" for="proposito">Propósito</label>
            <select id="proposito" v-model="stableForm.description" class="select" required>
              <option value="" disabled>Selecione uma finalidade...</option>
              <option value="Ordenha Higiênica">Ordenha higiênica</option>
              <option value="Maternidade / Crias">Maternidade / crias</option>
              <option value="Engorda / Confinamento">Engorda / confinamento</option>
              <option value="Tratamento Veterinário">Tratamento veterinário</option>
              <option value="Manejo Geral">Manejo geral</option>
            </select>
          </div>

          <p v-if="formError" class="alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ formError }}</span>
          </p>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="showModal = false">Cancelar</button>
          <button type="submit" form="form-estabulo" class="btn btn--primary" :disabled="savingStable">
            {{ savingStable ? 'Salvando...' : isEditingStable ? 'Salvar alterações' : 'Cadastrar estábulo' }}
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
import { confirmar } from '@/services/confirmService';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppModal from '@/components/ui/AppModal.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import RegistryCard from '@/components/layout/RegistryCard.vue';
import { apiErrorMessage } from '@/utils/apiError';

const painel = computed(() => painelDoPapel());

const stables = ref([]);
const busca = ref('');
const loading = ref(true);
const erro = ref('');
const showModal = ref(false);
const isEditingStable = ref(false);
const savingStable = ref(false);
const formError = ref('');

const stableForm = ref({
  id: null,
  name: '',
  max_animals: '',
  area: '',
  description: '',
});

const filteredStables = computed(() => {
  const termo = busca.value.trim().toLowerCase();
  if (!termo) return stables.value;
  return stables.value.filter((stable) =>
    String(stable.name || '').toLowerCase().includes(termo)
    || String(stable.description || '').toLowerCase().includes(termo)
  );
});

const formatArea = (area) => {
  const num = Number(area);
  if (!Number.isFinite(num)) return '—';
  return `${num.toLocaleString('pt-BR', { maximumFractionDigits: 2 })} ha`;
};

const loadData = async () => {
  loading.value = true;
  erro.value = '';
  try {
    const response = await api.getQuadrants();
    stables.value = response.data?.results || response.data || [];
  } catch (error) {
    console.error('Erro ao carregar estábulos:', error);
    erro.value = apiErrorMessage(error, 'Não foi possível carregar os estábulos.');
  } finally {
    loading.value = false;
  }
};

const openCreateModal = () => {
  isEditingStable.value = false;
  formError.value = '';
  stableForm.value = { id: null, name: '', max_animals: '', area: '', description: '' };
  showModal.value = true;
};

const editStable = (stable) => {
  isEditingStable.value = true;
  formError.value = '';
  stableForm.value = { ...stable };
  showModal.value = true;
};

const saveStable = async () => {
  savingStable.value = true;
  formError.value = '';
  try {
    if (isEditingStable.value) {
      await api.put(`quadrants/${stableForm.value.id}/`, stableForm.value);
    } else {
      await api.post('quadrants/', stableForm.value);
    }
    showModal.value = false;
    await loadData();
  } catch (error) {
    console.error('Erro ao salvar estábulo:', error);
    formError.value = apiErrorMessage(error, 'Não foi possível salvar o estábulo. Confira os dados e tente novamente.');
  } finally {
    savingStable.value = false;
  }
};

const deleteStable = async (stable) => {
  const ok = await confirmar({
    titulo: `Excluir o estábulo "${stable.name || `Estábulo ${stable.id}`}"?`,
    texto: 'Esta ação remove o cadastro da instalação.',
    acao: 'Excluir estábulo',
  });
  if (!ok) return;
  erro.value = '';
  try {
    await api.delete(`quadrants/${stable.id}/`);
    await loadData();
  } catch (error) {
    console.error('Erro ao excluir estábulo:', error);
    erro.value = apiErrorMessage(error, 'Não foi possível excluir o estábulo.');
  }
};

onMounted(loadData);
</script>
