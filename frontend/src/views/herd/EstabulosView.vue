<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Estábulos"
        descricao="Ocupação de cada instalação e transferência de animais entre elas."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      >
        <template #acoes>
          <button class="btn btn--primary" @click="openCreateModal">
            <AppIcon name="plus" :size="16" />
            Novo estábulo
          </button>
        </template>
      </PageHeader>

      <div v-if="loading" class="card">
        <div class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Sincronizando instalações e lotação...
        </div>
      </div>

      <div v-else-if="stables.length === 0" class="card">
        <div class="empty">
          <AppIcon :name="erro ? 'alert' : 'barn'" :size="30" />
          <p class="empty__title">{{ erro ? 'Não foi possível carregar' : 'Nenhum estábulo cadastrado' }}</p>
          <p class="empty__desc">
            {{ erro
              ? 'A lista de instalações não chegou do servidor. Verifique a conexão e tente de novo.'
              : 'Cadastre as instalações da fazenda para alocar o rebanho.' }}
          </p>
          <button v-if="erro" class="btn" @click="loadData">Tentar de novo</button>
          <button v-else class="btn btn--primary" @click="openCreateModal">Novo estábulo</button>
        </div>
      </div>

      <div v-else class="stack">
        <article
          v-for="stable in stables"
          :key="stable.id"
          class="card estabulo"
          :class="{ 'estabulo--lotado': getStableAnimalCount(stable.id) > stable.max_animals }"
        >
          <header class="card__head">
            <div class="list__main">
              <span class="icon-tile icon-tile--accent"><AppIcon name="barn" :size="18" /></span>
              <div>
                <h2 class="card__title">{{ stable.name || `Estábulo ${stable.id}` }}</h2>
                <p class="card__desc">{{ stable.description || 'Manejo geral' }}</p>
              </div>
            </div>
            <div class="row">
              <button class="btn btn--icon" title="Editar instalação" @click="editStable(stable)">
                <AppIcon name="edit" :size="15" />
              </button>
              <button class="btn btn--icon is-danger" title="Excluir instalação" @click="deleteStable(stable.id)">
                <AppIcon name="trash" :size="15" />
              </button>
            </div>
          </header>

          <div class="card__body">
            <div class="ocupacao">
              <span class="ocupacao__rotulo">Taxa de ocupação</span>
              <span class="ocupacao__valor mono">
                {{ getStableAnimalCount(stable.id) }} / {{ stable.max_animals }} cabeças
              </span>
            </div>
            <div class="meter">
              <div
                class="meter__fill"
                :class="getProgressBarClass(stable.id, stable.max_animals)"
                :style="{ width: getCapacityPercentage(stable.id, stable.max_animals) + '%' }"
              ></div>
            </div>

            <button class="btn btn--block expandir" @click="toggleStableExpansion(stable.id)">
              <AppIcon :name="expandedStables.includes(stable.id) ? 'chevron-down' : 'chevron-right'" :size="15" />
              {{ expandedStables.includes(stable.id) ? 'Ocultar animais' : `Listar animais (${getStableAnimalCount(stable.id)})` }}
            </button>

            <div v-if="expandedStables.includes(stable.id)" class="sub-tabela">
              <div v-if="getAnimalsInStable(stable.id).length === 0" class="empty">
                <AppIcon name="animal" :size="26" />
                <p class="empty__desc">Nenhum animal alojado neste estábulo.</p>
              </div>

              <div v-else class="table-wrap">
                <table class="table">
                  <thead>
                    <tr>
                      <th>Brinco</th>
                      <th>Nome</th>
                      <th>Peso</th>
                      <th class="cell-actions">Manejo</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="animal in getAnimalsInStable(stable.id)" :key="animal.id">
                      <td class="mono">#{{ animal.register_number }}</td>
                      <td class="cell-strong">{{ animal.name || 'Sem nome' }}</td>
                      <td class="mono">{{ animal.weight }} kg</td>
                      <td class="cell-actions">
                        <div class="acoes-linha">
                          <select
                            class="select select--inline"
                            title="Transferir animal para outra instalação"
                            @change="moveAnimal(animal, $event)"
                          >
                            <option value="" disabled selected>Transferir para...</option>
                            <option
                              v-for="target in stables"
                              :key="target.id"
                              :value="target.id"
                              :disabled="target.id === stable.id"
                            >
                              {{ target.name }}
                            </option>
                          </select>
                          <button
                            class="btn-link"
                            @click="$router.push(`/animais/editar/${animal.id}`)"
                          >
                            Editar
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </article>
      </div>

      <AppModal
        v-if="showModal"
        :titulo="isEditingStable ? 'Editar instalação' : 'Novo estábulo'"
        @fechar="showModal = false"
      >
        <form id="form-estabulo" class="stack" @submit.prevent="saveStable">
          <div class="field">
            <label class="field__label" for="nome-estabulo">Nome do estábulo</label>
            <input id="nome-estabulo" v-model="stableForm.name" class="input" type="text" placeholder="Ex: Estábulo de ordenha B" required>
          </div>

          <div class="grid grid--2">
            <div class="field">
              <label class="field__label" for="capacidade">Capacidade (cabeças)</label>
              <input id="capacidade" v-model.number="stableForm.max_animals" class="input" type="number" min="1" placeholder="50" required>
            </div>

            <div class="field">
              <label class="field__label" for="area">Área (hectares)</label>
              <input id="area" v-model="stableForm.area" class="input" type="number" step="0.01" min="0" placeholder="12.50" required>
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
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="showModal = false">Cancelar</button>
          <button type="submit" form="form-estabulo" class="btn btn--primary" :disabled="savingStable">
            {{ savingStable ? 'Processando...' : 'Confirmar instalação' }}
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
import { confirmar } from '@/services/confirmService';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppModal from '@/components/ui/AppModal.vue';
import PageHeader from '@/components/layout/PageHeader.vue';

const painel = computed(() => painelDoPapel());

const stables = ref([]);
const animals = ref([]);
const loading = ref(true);
// Sem isto a tela ficava totalmente em branco quando a API não respondia:
// o `catch` só escrevia no console e a lista vazia não desenhava nada.
const erro = ref(false);
const showModal = ref(false);
const isEditingStable = ref(false);
const savingStable = ref(false);
const expandedStables = ref([]);

/*
 * Os nomes aqui seguem o modelo Quadrant do backend: `max_animals`, `area` e
 * `description`. A tela usava `capacity` e `purpose`, que nao existem la — o
 * serializer ignorava os dois e recusava o POST por falta de `description`,
 * `area` e `max_animals`, todos obrigatorios. Nenhum estabulo salvava, e na
 * leitura a barra de ocupacao dividia por `undefined`.
 *
 * `purpose` (a finalidade) virou `description`: e o campo de texto livre que
 * o modelo oferece, e e exatamente o que a tela ja mostrava como subtitulo.
 */
const stableForm = ref({
  id: null,
  name: '',
  max_animals: '',
  area: '',
  description: ''
});

onMounted(() => {
  loadData();
});

const loadData = async () => {
  loading.value = true;
  erro.value = false;
  try {
    const stablesRes = await api.get('quadrants/');
    stables.value = stablesRes.data.results || stablesRes.data;

    if (stables.value.length === 0) {
      stables.value = [
        { id: 1, name: 'Estábulo Principal A', max_animals: 40, area: '12.50', description: 'Ordenha Higiênica' },
        { id: 2, name: 'Piquete Sul Maternidade', max_animals: 15, area: '6.00', description: 'Maternidade / Crias' }
      ];
    }

    const animalsRes = await api.get('animals/');
    animals.value = animalsRes.data.results || animalsRes.data;

  } catch (error) {
    console.error("Erro ao sincronizar dados de instalações:", error);
    erro.value = true;
  } finally {
    loading.value = false;
  }
};

const getAnimalQuadrantId = (animal) => {
  if (animal && animal.quadrant && typeof animal.quadrant === 'object') {
    return animal.quadrant.id || animal.quadrant;
  }
  return animal.quadrant;
};

const getAnimalsInStable = (stableId) => {
  return animals.value.filter(animal => String(getAnimalQuadrantId(animal)) === String(stableId));
};

const getStableAnimalCount = (stableId) => {
  return getAnimalsInStable(stableId).length;
};

const getCapacityPercentage = (stableId, maxCapacity) => {
  const current = getStableAnimalCount(stableId);
  const percent = (current / maxCapacity) * 100;
  return percent > 100 ? 100 : percent;
};

const getProgressBarClass = (stableId, maxCapacity) => {
  const current = getStableAnimalCount(stableId);
  if (current >= maxCapacity) return 'is-danger';
  if (current >= maxCapacity * 0.8) return 'is-warn';
  return '';
};

const toggleStableExpansion = (stableId) => {
  if (expandedStables.value.includes(stableId)) {
    expandedStables.value = expandedStables.value.filter(id => id !== stableId);
  } else {
    expandedStables.value.push(stableId);
  }
};

const moveAnimal = async (animal, event) => {
  const targetStableId = Number(event.target.value);
  if (!targetStableId) return;

  try {
    await api.patch(`animals/${animal.id}/`, { quadrant: targetStableId });
    notify(`Animal ${animal.name || ''} transferido com sucesso!`, 'success');
    loadData();
  } catch (error) {
    console.error(error);
    notify('Falha ao processar movimentação do animal.', 'error');
  } finally {
    event.target.value = '';
  }
};

const openCreateModal = () => {
  isEditingStable.value = false;
  stableForm.value = { id: null, name: '', max_animals: '', area: '', description: '' };
  showModal.value = true;
};

const editStable = (stable) => {
  isEditingStable.value = true;
  stableForm.value = { ...stable };
  showModal.value = true;
};

const saveStable = async () => {
  savingStable.value = true;
  try {
    if (isEditingStable.value) {
      await api.put(`quadrants/${stableForm.value.id}/`, stableForm.value);
      notify('Instalação atualizada com sucesso!', 'success');
    } else {
      await api.post('quadrants/', stableForm.value);
      notify('Novo estábulo cadastrado no sistema!', 'success');
    }
    showModal.value = false;
    loadData();
  } catch (error) {
    console.error(error);
    notify('Erro ao salvar instalação técnica.', 'error');
  } finally {
    savingStable.value = false;
  }
};

const deleteStable = async (stableId) => {
  const ok = await confirmar({
    titulo: 'Excluir este estábulo?',
    texto: 'Os animais alojados nele ficam sem lotação até serem transferidos.',
    acao: 'Excluir estábulo',
  });
  if (ok) {
    try {
      await api.delete(`quadrants/${stableId}/`);
      notify('Estábulo excluído com sucesso.', 'success');
      loadData();
    } catch (error) {
      console.error(error);
      notify('Falha ao excluir estábulo.', 'error');
    }
  }
};
</script>

<style scoped>
/* Um estábulo acima da capacidade é a informação mais urgente desta tela:
   ele se marca na borda, sem precisar de leitura. */
.estabulo--lotado { border-color: var(--danger-line); }

.ocupacao {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 7px;
}

.ocupacao__rotulo { color: var(--text-2); font-size: var(--fs-sm); }
.ocupacao__valor { font-size: var(--fs-sm); font-weight: 500; }

.expandir {
  margin-top: 16px;
  justify-content: flex-start;
  color: var(--text-2);
}

.expandir svg { color: var(--text-3); }

.sub-tabela {
  margin-top: 12px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  overflow: hidden;
}

.acoes-linha {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  justify-content: flex-end;
}

.select--inline {
  width: auto;
  height: 28px;
  padding: 0 28px 0 9px;
  font-size: var(--fs-sm);
}
</style>
