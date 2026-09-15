<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        titulo="Tarefas"
        descricao="O que precisa ser feito, por prioridade e vencimento."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      >
        <template #acoes>
          <button class="btn btn--primary" @click="createNewTask">
            <AppIcon name="plus" :size="16" />
            Nova tarefa
          </button>
        </template>
      </PageHeader>

      <div class="toolbar">
        <div class="segmented" role="group" aria-label="Filtrar tarefas">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            class="segmented__item"
            :class="{ 'is-active': activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            {{ tab.label }}
            <span class="count">{{ getTabCount(tab.id) }}</span>
          </button>
        </div>
      </div>

      <section class="card">
        <div v-if="filteredTasks.length === 0" class="empty">
          <AppIcon name="clipboard" :size="30" />
          <p class="empty__title">Nenhuma tarefa neste filtro</p>
          <p class="empty__desc">
            {{ activeTab === 'completed' ? 'Nada foi concluído ainda.' : 'Crie uma tarefa para organizar a rotina da fazenda.' }}
          </p>
        </div>

        <div v-else class="list">
          <article
            v-for="task in filteredTasks"
            :key="task.id"
            class="list__item tarefa"
            :class="{ 'tarefa--feita': task.completed }"
          >
            <div class="list__main tarefa__conteudo">
              <input
                type="checkbox"
                class="tarefa__marca"
                :checked="task.completed"
                :aria-label="`Concluir ${task.title}`"
                @click.stop="toggleTaskComplete(task)"
              >

              <div class="tarefa__texto">
                <span class="list__title">
                  <span class="tarefa__titulo">{{ task.title }}</span>
                  <span v-if="task.priority" class="badge" :class="badgePrioridade(task.priority)">
                    {{ getPriorityLabel(task.priority) }}
                  </span>
                </span>
                <span v-if="task.description" class="list__sub">{{ task.description }}</span>
                <span class="tarefa__meta">
                  <span class="tarefa__meta-item" :class="{ 'is-atrasada': estaAtrasada(task) }">
                    <AppIcon :name="estaAtrasada(task) ? 'alert' : 'calendar'" :size="13" />
                    {{ formatDate(task.due_date) }}
                    <template v-if="estaAtrasada(task)">· atrasada</template>
                  </span>
                  <span v-if="task.animal" class="tarefa__meta-item">
                    <AppIcon name="animal" :size="13" />
                    {{ task.animal_name }}
                  </span>
                </span>
              </div>
            </div>

            <div class="row">
              <button class="btn btn--icon" title="Editar tarefa" @click.stop="editTask(task)">
                <AppIcon name="edit" :size="15" />
              </button>
              <button class="btn btn--icon is-danger" title="Excluir tarefa" @click.stop="deleteTask(task)">
                <AppIcon name="trash" :size="15" />
              </button>
            </div>
          </article>
        </div>
      </section>

      <AppModal
        v-if="showEditModal"
        :titulo="isNewTask ? 'Nova tarefa' : 'Editar tarefa'"
        @fechar="closeModal"
      >
        <form id="form-tarefa" class="stack" @submit.prevent="saveTask">
          <div class="field">
            <label class="field__label" for="tarefa-titulo">Título</label>
            <input id="tarefa-titulo" v-model="editingTask.title" class="input" type="text" placeholder="Ex: Conferir cocho do piquete sul" required>
          </div>

          <div class="field">
            <label class="field__label" for="tarefa-desc">Descrição</label>
            <textarea id="tarefa-desc" v-model="editingTask.description" class="textarea" rows="3" placeholder="Detalhes úteis para quem for executar"></textarea>
          </div>

          <div class="grid grid--2">
            <div class="field">
              <label class="field__label" for="tarefa-prioridade">Prioridade</label>
              <select id="tarefa-prioridade" v-model="editingTask.priority" class="select">
                <option value="">Selecione...</option>
                <option value="baixa">Baixa</option>
                <option value="media">Média</option>
                <option value="alta">Alta</option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="tarefa-data">Vencimento</label>
              <input id="tarefa-data" v-model="editingTask.due_date" class="input" type="date">
            </div>
          </div>

          <div class="field">
            <label class="field__label" for="tarefa-animal">Animal (opcional)</label>
            <select id="tarefa-animal" v-model="editingTask.animal" class="select">
              <option :value="null">Nenhum animal</option>
              <option v-for="animal in activeAnimals" :key="animal.id" :value="animal.id">
                {{ animal.name }} (#{{ animal.register_number }})
              </option>
            </select>
          </div>

          <label class="checkbox">
            <input type="checkbox" v-model="editingTask.completed">
            Marcar como concluída
          </label>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="closeModal">Cancelar</button>
          <button type="submit" form="form-tarefa" class="btn btn--primary">Salvar</button>
        </template>
      </AppModal>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import api from '@/services/api';
import { painelDoPapel } from '@/services/auth';
import { notify } from '@/services/notificationService';
import { confirmar } from '@/services/confirmService';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppModal from '@/components/ui/AppModal.vue';
import PageHeader from '@/components/layout/PageHeader.vue';

const painel = computed(() => painelDoPapel());

// Dados
const tasks = ref([]);
const activeAnimals = ref([]);

// Estado da UI
const activeTab = ref('all');
const showEditModal = ref(false);
const isNewTask = ref(false);

// O recarregamento periódico ficava sem `clearInterval`: cada visita à tela
// deixava mais um timer vivo batendo na API para sempre.
let recarga = null;

// Edição
const editingTask = ref({
  title: '',
  description: '',
  priority: 'media',
  due_date: new Date().toISOString().split('T')[0],
  completed: false,
  animal: null
});

// Abas
const tabs = [
  { id: 'all', label: 'Todas' },
  { id: 'pending', label: 'Pendentes' },
  { id: 'completed', label: 'Concluídas' },
  { id: 'urgent', label: 'Urgentes' }
];

// Computed
const filteredTasks = computed(() => {
  return tasks.value.filter(task => {
    if (activeTab.value === 'pending') return !task.completed;
    if (activeTab.value === 'completed') return task.completed;
    if (activeTab.value === 'urgent') return !task.completed && task.priority === 'alta';
    return true;
  }).sort((a, b) => {
    // Ordena por prioridade e data
    const priorityOrder = { alta: 0, media: 1, baixa: 2 };
    if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    return new Date(a.due_date) - new Date(b.due_date);
  });
});

// Métodos
const getTabCount = (tabId) => {
  if (tabId === 'all') return tasks.value.length;
  if (tabId === 'pending') return tasks.value.filter(t => !t.completed).length;
  if (tabId === 'completed') return tasks.value.filter(t => t.completed).length;
  if (tabId === 'urgent') return tasks.value.filter(t => !t.completed && t.priority === 'alta').length;
  return 0;
};

const loadInitialData = async () => {
  try {
    const [tasksRes, animalsRes] = await Promise.all([
      api.get('tasks/', { headers: { 'X-Source': 'operator' } }).catch(() => ({ data: [] })),
      api.get('animals/?status=ativo')
    ]);

    // `animal_name` ja vem do TaskSerializer. A tela cruzava a lista de animais
    // para recalcular o mesmo nome que o servidor tinha acabado de mandar.
    tasks.value = tasksRes.data.results || tasksRes.data || [];
    // A lista de animais continua sendo necessaria: alimenta o seletor do modal.
    activeAnimals.value = animalsRes.data.results || animalsRes.data;
  } catch (err) {
    console.error('Erro ao carregar tarefas:', err);
    tasks.value = [];
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'sem prazo';
  const date = new Date(dateString);
  const today = new Date().toDateString();
  if (date.toDateString() === today) return 'Hoje';
  const tomorrow = new Date(Date.now() + 86400000).toDateString();
  if (date.toDateString() === tomorrow) return 'Amanhã';
  return date.toLocaleDateString('pt-BR');
};

const getPriorityLabel = (priority) => {
  const labels = { alta: 'Alta', media: 'Média', baixa: 'Baixa' };
  return labels[priority] || '';
};

// Prazo vencido em tarefa aberta lê igual à vacina em atraso: mesma cor,
// mesmo ícone. Duas telas, uma convenção.
const estaAtrasada = (task) => {
  if (task.completed || !task.due_date) return false;
  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);
  return new Date(task.due_date) < hoje;
};

const badgePrioridade = (priority) => {
  if (priority === 'alta') return 'badge--danger';
  if (priority === 'media') return 'badge--warn';
  return '';
};

const createNewTask = () => {
  isNewTask.value = true;
  editingTask.value = {
    title: '',
    description: '',
    priority: 'media',
    due_date: new Date().toISOString().split('T')[0],
    completed: false,
    animal: null
  };
  showEditModal.value = true;
};

const editTask = (task) => {
  isNewTask.value = false;
  editingTask.value = { ...task };
  showEditModal.value = true;
};

/*
 * Cada uma destas acoes disparava tambem um `POST notifications/` com
 * `notification_type: 'task_created' | 'task_updated' | 'task_deleted'` —
 * valores que nao estao nas choices do modelo Notification. O serializer
 * devolvia 400 e o `.catch(() => {})` engolia o erro: eram quatro requisicoes
 * jogadas fora por acao.
 *
 * E eram redundantes de qualquer forma: TaskViewSet.perform_create,
 * perform_update e perform_destroy ja gravam a notificacao no servidor.
 */
const deleteTask = async (task) => {
  const ok = await confirmar({
    titulo: `Excluir "${task.title}"?`,
    texto: 'A tarefa é removida da lista para todo mundo.',
    acao: 'Excluir tarefa',
  });
  if (ok) {
    try {
      await api.delete(`tasks/${task.id}/`, { headers: { 'X-Source': 'operator' } });
      tasks.value = tasks.value.filter(t => t.id !== task.id);
    } catch (err) {
      console.error('Erro ao deletar tarefa:', err);
      notify('Erro ao deletar tarefa.', 'error');
    }
  }
};

const toggleTaskComplete = async (task) => {
  try {
    const updated = { ...task, completed: !task.completed };
    await api.put(`/tasks/${task.id}/`, updated, { headers: { 'X-Source': 'operator' } });

    const index = tasks.value.findIndex(t => t.id === task.id);
    if (index !== -1) {
      tasks.value[index] = updated;
    }
  } catch (err) {
    console.error('Erro ao atualizar tarefa:', err);
  }
};

const saveTask = async () => {
  try {
    let response;
    if (isNewTask.value) {
      response = await api.post('tasks/', editingTask.value, { headers: { 'X-Source': 'operator' } });
      tasks.value.push(response.data);
    } else {
      await api.put(`tasks/${editingTask.value.id}/`, editingTask.value, { headers: { 'X-Source': 'operator' } });
      const index = tasks.value.findIndex(t => t.id === editingTask.value.id);
      if (index !== -1) {
        tasks.value[index] = editingTask.value;
      }
    }

    closeModal();
    loadInitialData(); // Recarrega para garantir sincronização
  } catch (err) {
    console.error('Erro ao salvar tarefa:', err);
    notify('Erro ao salvar tarefa.', 'error');
  }
};

const closeModal = () => {
  showEditModal.value = false;
};

onMounted(() => {
  loadInitialData();
  // Recarrega tarefas a cada 30 segundos
  recarga = setInterval(loadInitialData, 30000);
});

onBeforeUnmount(() => {
  if (recarga) clearInterval(recarga);
});
</script>

<style scoped>
.tarefa__conteudo { align-items: flex-start; flex: 1; }

.tarefa__marca {
  width: 16px;
  height: 16px;
  margin: 3px 0 0;
  flex: none;
  accent-color: var(--accent);
  cursor: pointer;
}

.tarefa__texto { min-width: 0; }

/* Concluída sai do caminho sem sumir: risco no título e texto apagado. */
.tarefa--feita .tarefa__titulo {
  text-decoration: line-through;
  color: var(--text-3);
}

.tarefa--feita .list__sub { color: var(--text-3); }

.tarefa__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 7px;
}

.tarefa__meta-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--text-3);
  font-size: var(--fs-xs);
}

.tarefa__meta-item.is-atrasada { color: var(--danger); font-weight: 500; }
</style>
