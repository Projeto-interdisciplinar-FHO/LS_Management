<template>
  <div class="tasks-management-container">
    <div class="header">
      <h1>📋 Gerenciar Tarefas</h1>
      <p class="subtitle">Acompanhe e edite suas tarefas diárias</p>
    </div>

    <!-- Abas de Filtro -->
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['tab', { active: activeTab === tab.id }]"
      >
        {{ tab.label }}
        <span class="count">{{ getTabCount(tab.id) }}</span>
      </button>
    </div>

    <!-- Lista de Tarefas -->
    <div class="tasks-list">
      <transition-group name="list" tag="div">
        <div 
          v-for="task in filteredTasks" 
          :key="task.id"
          @click="selectTask(task)"
          class="task-card"
          :class="{ 
            'selected': selectedTaskId === task.id,
            'completed': task.completed,
            'urgent': isUrgent(task)
          }"
        >
          <div class="task-checkbox">
            <input 
              type="checkbox" 
              :checked="task.completed"
              @click.stop="toggleTaskComplete(task)"
              class="checkbox"
            >
          </div>

          <div class="task-content">
            <h3>{{ task.title }}</h3>
            <p class="description">{{ task.description }}</p>
            
            <div class="task-meta">
              <span v-if="task.priority" :class="['priority', `priority-${task.priority}`]">
                {{ getPriorityLabel(task.priority) }}
              </span>
              <span class="due-date">
                📅 {{ formatDate(task.due_date) }}
              </span>
              <span v-if="task.animal" class="animal-ref">
                🐄 {{ task.animal_name }}
              </span>
            </div>
          </div>

          <div class="task-actions">
            <button @click.stop="editTask(task)" class="action-btn edit-btn">✏️</button>
            <button @click.stop="deleteTask(task)" class="action-btn delete-btn">🗑️</button>
          </div>
        </div>
      </transition-group>

      <div v-if="filteredTasks.length === 0" class="empty-state">
        <p>Nenhuma tarefa neste filtro</p>
      </div>
    </div>

    <!-- Modal de Edição -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <button @click="closeModal" class="modal-close">✕</button>
        
        <h2>{{ isNewTask ? 'Nova Tarefa' : 'Editar Tarefa' }}</h2>

        <div class="form-group">
          <label>Título</label>
          <input v-model="editingTask.title" type="text" class="input-field">
        </div>

        <div class="form-group">
          <label>Descrição</label>
          <textarea v-model="editingTask.description" rows="3" class="input-field"></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Prioridade</label>
            <select v-model="editingTask.priority" class="input-field">
              <option value="">Selecione...</option>
              <option value="baixa">🟢 Baixa</option>
              <option value="media">🟡 Média</option>
              <option value="alta">🔴 Alta</option>
            </select>
          </div>

          <div class="form-group">
            <label>Data de Vencimento</label>
            <input v-model="editingTask.due_date" type="date" class="input-field">
          </div>
        </div>

        <div class="form-group">
          <label>Animal (Opcional)</label>
          <select v-model="editingTask.animal" class="input-field">
            <option :value="null">Nenhum animal</option>
            <option v-for="animal in activeAnimals" :key="animal.id" :value="animal.id">
              {{ animal.name }} (#{{ animal.register_number }})
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>
            <input type="checkbox" v-model="editingTask.completed">
            Marcar como concluída
          </label>
        </div>

        <div class="modal-actions">
          <button @click="closeModal" class="btn btn-secondary">Cancelar</button>
          <button @click="saveTask" class="btn btn-primary">Salvar</button>
        </div>
      </div>
    </div>

    <!-- Modal de Novo Botão Flutuante -->
    <button class="fab" @click="createNewTask">
      ➕
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';

// Dados
const tasks = ref([]);
const activeAnimals = ref([]);

// Estado da UI
const activeTab = ref('all');
const selectedTaskId = ref(null);
const showEditModal = ref(false);
const isNewTask = ref(false);

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

const selectedTask = computed(() => {
  return tasks.value.find(t => t.id === selectedTaskId.value) || null;
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

    tasks.value = tasksRes.data.results || tasksRes.data || [];
    activeAnimals.value = animalsRes.data.results || animalsRes.data;

    // Enriquece com nomes de animais
    tasks.value = tasks.value.map(task => {
      if (task.animal) {
        const animal = activeAnimals.value.find(a => a.id === task.animal);
        return { ...task, animal_name: animal?.name || 'Animal não encontrado' };
      }
      return task;
    });
  } catch (err) {
    console.error('Erro ao carregar tarefas:', err);
    tasks.value = [];
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  const today = new Date().toDateString();
  if (date.toDateString() === today) return 'Hoje';
  const tomorrow = new Date(Date.now() + 86400000).toDateString();
  if (date.toDateString() === tomorrow) return 'Amanhã';
  return date.toLocaleDateString('pt-BR');
};

const getPriorityLabel = (priority) => {
  const labels = { alta: '🔴 Alta', media: '🟡 Média', baixa: '🟢 Baixa' };
  return labels[priority] || '';
};

const isUrgent = (task) => {
  return !task.completed && task.priority === 'alta';
};

const selectTask = (task) => {
  selectedTaskId.value = task.id;
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

const deleteTask = async (task) => {
  if (confirm('Tem certeza que deseja deletar esta tarefa?')) {
    try {
      await api.delete(`tasks/${task.id}/`, { headers: { 'X-Source': 'operator' } });
      tasks.value = tasks.value.filter(t => t.id !== task.id);
      
      // Cria notificação para admin
      await api.post('notifications/', {
        message: `Operador deletou tarefa: "${task.title}"`,
        notification_type: 'task_deleted'
      }).catch(() => {});
    } catch (err) {
      console.error('Erro ao deletar tarefa:', err);
      alert('Erro ao deletar tarefa');
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

    // Cria notificação para admin
    const message = updated.completed 
      ? `Operador concluiu tarefa: "${task.title}"`
      : `Operador reabertu tarefa: "${task.title}"`;
    
    await api.post('notifications/', {
      message,
      notification_type: 'task_updated'
    }).catch(() => {});
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
      
      // Notifica admin sobre nova tarefa
      await api.post('notifications/', {
        message: `Operador criou nova tarefa: "${editingTask.value.title}"`,
        notification_type: 'task_created'
      }).catch(() => {});
    } else {
      await api.put(`tasks/${editingTask.value.id}/`, editingTask.value, { headers: { 'X-Source': 'operator' } });
      const index = tasks.value.findIndex(t => t.id === editingTask.value.id);
      if (index !== -1) {
        tasks.value[index] = editingTask.value;
      }
      
      // Notifica admin sobre edição
      await api.post('notifications/', {
        message: `Operador atualizou tarefa: "${editingTask.value.title}"`,
        notification_type: 'task_updated'
      }).catch(() => {});
    }

    closeModal();
    loadInitialData(); // Recarrega para garantir sincronização
  } catch (err) {
    console.error('Erro ao salvar tarefa:', err);
    alert('Erro ao salvar tarefa');
  }
};

const closeModal = () => {
  showEditModal.value = false;
};

onMounted(() => {
  loadInitialData();
  // Recarrega tarefas a cada 30 segundos
  setInterval(() => {
    loadInitialData();
  }, 30000);
});
</script>

<style scoped>
.tasks-management-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
  background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
  border-radius: 12px;
  min-height: 100vh;
}

.header {
  margin-bottom: 20px;
}

.header h1 {
  color: #00d4ff;
  font-size: 28px;
  margin: 0 0 8px 0;
}

.subtitle {
  color: #888;
  font-size: 14px;
  margin: 0;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.tab {
  padding: 10px 16px;
  background: #0a0a0a;
  border: 1px solid #333;
  border-radius: 6px;
  color: #888;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab:hover {
  border-color: #00d4ff;
  color: #00d4ff;
}

.tab.active {
  background: #00d4ff;
  border-color: #00d4ff;
  color: #000;
}

.count {
  background: rgba(0, 212, 255, 0.2);
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: bold;
}

.tab.active .count {
  background: rgba(0, 0, 0, 0.3);
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 80px;
}

.task-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 15px;
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.task-card:hover {
  border-color: #00d4ff;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.1);
}

.task-card.selected {
  border-color: #00ff88;
  background: rgba(0, 255, 136, 0.05);
}

.task-card.completed {
  opacity: 0.6;
}

.task-card.urgent {
  border-left: 4px solid #ff4444;
}

.task-checkbox {
  flex-shrink: 0;
  margin-top: 2px;
}

.checkbox {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #00d4ff;
}

.task-content {
  flex: 1;
  min-width: 0;
}

.task-content h3 {
  color: #fff;
  font-size: 15px;
  margin: 0 0 4px 0;
  text-decoration: var(--text-decoration, none);
}

.task-card.completed .task-content h3 {
  --text-decoration: line-through;
  color: #666;
}

.description {
  color: #888;
  font-size: 13px;
  margin: 0 0 8px 0;
}

.task-meta {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  font-size: 12px;
}

.priority {
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.priority-alta {
  background: rgba(255, 68, 68, 0.2);
  color: #ff4444;
}

.priority-media {
  background: rgba(255, 204, 0, 0.2);
  color: #ffcc00;
}

.priority-baixa {
  background: rgba(0, 255, 136, 0.2);
  color: #00ff88;
}

.due-date,
.animal-ref {
  color: #888;
}

.task-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}

.action-btn {
  background: none;
  border: 1px solid #333;
  border-radius: 4px;
  padding: 6px 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.edit-btn:hover {
  border-color: #00d4ff;
  color: #00d4ff;
}

.delete-btn:hover {
  border-color: #ff4444;
  color: #ff4444;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 25px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  color: #888;
  font-size: 24px;
  cursor: pointer;
}

.modal h2 {
  color: #00d4ff;
  font-size: 20px;
  margin: 0 0 20px 0;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  color: #aaa;
  font-size: 13px;
  margin-bottom: 6px;
  font-weight: 500;
}

.input-field {
  width: 100%;
  padding: 10px;
  background: #0a0a0a;
  border: 1px solid #333;
  border-radius: 6px;
  color: #fff;
  font-size: 14px;
}

.input-field:focus {
  outline: none;
  border-color: #00d4ff;
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.2);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.form-group input[type="checkbox"] {
  margin-right: 8px;
  accent-color: #00d4ff;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: #00d4ff;
  color: #000;
}

.btn-primary:hover {
  background: #00a8cc;
}

.btn-secondary {
  background: #333;
  color: #fff;
}

.btn-secondary:hover {
  background: #444;
}

/* FAB - Floating Action Button */
.fab {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00d4ff, #00ff88);
  border: none;
  font-size: 28px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fab:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 212, 255, 0.6);
}

.fab:active {
  transform: scale(0.95);
}

/* Animações */
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style>
