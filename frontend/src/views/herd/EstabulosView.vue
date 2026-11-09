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

      <p v-if="erro && stables.length" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ erro }}</span>
      </p>

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
              ? erro
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
                      <th class="cell-actions">Manejo</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="animal in getAnimalsInStable(stable.id)" :key="animal.id">
                      <td class="mono">#{{ animal.register_number }}</td>
                      <td class="cell-strong">{{ animal.name || 'Sem nome' }}</td>
                      <td class="cell-actions">
                        <div class="acoes-linha">
                          <select
                            class="select select--inline"
                            title="Transferir animal para outra instalação"
                            @change="openMoveModal(animal, $event)"
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
          <p v-if="formError" class="alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ formError }}</span>
          </p>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="showModal = false">Cancelar</button>
          <button type="submit" form="form-estabulo" class="btn btn--primary" :disabled="savingStable">
            {{ savingStable ? 'Salvando...' : 'Confirmar instalação' }}
          </button>
        </template>
      </AppModal>

      <AppModal v-if="showMoveModal" titulo="Registrar movimentação" @fechar="showMoveModal = false">
        <form id="form-movimentacao" class="stack" @submit.prevent="moveAnimal">
          <p>
            {{ selectedAnimal?.name }} · #{{ selectedAnimal?.register_number }}
            para {{ stables.find((stable) => String(stable.id) === String(movementForm.quadrant))?.name }}
          </p>
          <div class="field">
            <label class="field__label" for="tipo-movimentacao">Tipo</label>
            <select id="tipo-movimentacao" v-model.number="movementForm.movement_type" class="select" required>
              <option value="" disabled>Selecione um tipo...</option>
              <option v-for="type in movementTypes" :key="type.id" :value="type.id">{{ type.name }}</option>
            </select>
          </div>
          <div class="field">
            <label class="field__label" for="data-movimentacao">Data</label>
            <input id="data-movimentacao" v-model="movementForm.movement_date" class="input" type="date" required>
          </div>
          <div class="field">
            <label class="field__label" for="motivo-movimentacao">Motivo</label>
            <textarea id="motivo-movimentacao" v-model.trim="movementForm.movement_reason" class="input" rows="3" required></textarea>
          </div>
          <p v-if="movementError" class="alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ movementError }}</span>
          </p>
        </form>
        <template #rodape>
          <button type="button" class="btn" @click="showMoveModal = false">Cancelar</button>
          <button type="submit" form="form-movimentacao" class="btn btn--primary" :disabled="savingMovement">
            {{ savingMovement ? 'Registrando...' : 'Confirmar transferência' }}
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
import { apiErrorMessage } from '@/utils/apiError';
import { situacao } from '@/utils/statusUtils';
import { idRelacao, ultimaMovimentacaoPorAnimal } from '@/utils/animalMovementUtils';

const painel = computed(() => painelDoPapel());

const stables = ref([]);
const animals = ref([]);
const movements = ref([]);
const movementTypes = ref([]);
const loading = ref(true);
// Sem isto a tela ficava totalmente em branco quando a API não respondia:
// o `catch` só escrevia no console e a lista vazia não desenhava nada.
const erro = ref('');
const showModal = ref(false);
const isEditingStable = ref(false);
const savingStable = ref(false);
const formError = ref('');
const expandedStables = ref([]);
const showMoveModal = ref(false);
const savingMovement = ref(false);
const movementError = ref('');
const selectedAnimal = ref(null);
const movementForm = ref({ quadrant: '', movement_type: '', movement_date: '', movement_reason: '' });

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
  erro.value = '';
  try {
    const [stablesRes, animalsRes, movementsRes, typesRes] = await Promise.all([
      api.getQuadrants(),
      api.getAnimals(),
      api.get('animal_movements/'),
      api.get('movement_types/'),
    ]);
    const rows = (response) => response.data?.results || response.data || [];
    stables.value = rows(stablesRes);
    animals.value = rows(animalsRes);
    movements.value = rows(movementsRes);
    movementTypes.value = rows(typesRes);

  } catch (error) {
    console.error("Erro ao sincronizar dados de instalações:", error);
    erro.value = apiErrorMessage(error, 'Não foi possível carregar os estábulos e animais.');
  } finally {
    loading.value = false;
  }
};

const latestMovements = computed(() => ultimaMovimentacaoPorAnimal(movements.value));

const getAnimalsInStable = (stableId) => {
  return animals.value.filter((animal) =>
    situacao(animal.status).noRebanho
    && String(idRelacao(latestMovements.value.get(String(animal.id))?.quadrant)) === String(stableId)
  );
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

const openMoveModal = (animal, event) => {
  const targetStableId = Number(event.target.value);
  event.target.value = '';
  if (!targetStableId) return;
  selectedAnimal.value = animal;
  movementError.value = '';
  movementForm.value = {
    quadrant: targetStableId,
    movement_type: '',
    movement_date: todayIso(),
    movement_reason: `Transferência para ${stables.value.find((item) => item.id === targetStableId)?.name || 'outro estábulo'}`,
  };
  showMoveModal.value = true;
};

const moveAnimal = async () => {
  if (!selectedAnimal.value) return;
  savingMovement.value = true;
  movementError.value = '';
  try {
    await api.post('animal_movements/', {
      animal: selectedAnimal.value.id,
      quadrant: Number(movementForm.value.quadrant),
      movement_type: Number(movementForm.value.movement_type),
      movement_date: movementForm.value.movement_date,
      movement_reason: movementForm.value.movement_reason,
    });
    showMoveModal.value = false;
    await loadData();
  } catch (error) {
    console.error(error);
    movementError.value = apiErrorMessage(error, 'Não foi possível registrar a movimentação.');
  } finally {
    savingMovement.value = false;
  }
};

function todayIso() {
  const date = new Date();
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

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
    loadData();
  } catch (error) {
    console.error(error);
    formError.value = apiErrorMessage(error, 'Não foi possível salvar o estábulo. Confira os dados e tente novamente.');
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
      loadData();
    } catch (error) {
      console.error(error);
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
