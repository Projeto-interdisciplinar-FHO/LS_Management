<template>
  <div class="dashboard-wrapper op-theme">
    <transition name="slide">
      <aside v-if="isMenuOpen" class="sidebar-drawer">
        <div class="sidebar-content">
          <div class="drawer-header">
            <img src="@/assets/logo-vaca-ls.png" alt="Logo" class="drawer-logo">
            <span class="brand-name">L.S Operacional</span>
          </div>
          <nav class="drawer-menu">
            <router-link to="/dashboard-op" class="nav-link active">
              <span class="nav-icon">⊞</span> Tarefas do Dia
            </router-link>
            <router-link to="/animais" class="nav-link">
              <span class="nav-icon">◈</span> Lista de Animais
            </router-link>
            <router-link to="/lancamento-leite" class="nav-link">
              <span class="nav-icon">🥛</span> Registrar Leite
            </router-link>
            <router-link to="/pesagem" class="nav-link">
              <span class="nav-icon">⚖️</span> Registrar Peso
            </router-link>
            <router-link to="/vacinacao" class="nav-link">
              <span class="nav-icon">✛</span> Registrar Vacina
            </router-link>
          </nav>
          <button @click="logout" class="btn-logout">⏻ Sair do Sistema</button>
        </div>
      </aside>
    </transition>

    <main class="main-layout" :class="{ 'blur-bg': isMenuOpen }">
      <header class="top-bar">
        <button @click="toggleMenu" class="btn-menu">☰</button>
        <div class="user-info">
          <span class="user-role">Operador de Campo</span>
          <div class="avatar">OP</div>
        </div>
      </header>

      <div class="dashboard-content">
        <div class="welcome-section">
          <h1>Rotina Operacional</h1>
          <p>Gerencie suas tarefas diárias de manejo no campo.</p>
        </div>

        <div class="tasks-container">
          <section class="tasks-card">
            <header class="card-header">
              <h2>Lista de Tarefas</h2>
              <span class="date-today">{{ currentData }}</span>
            </header>
            
            <form @submit.prevent="addTask" class="add-task-form">
              <input 
                v-model="newTaskDesc" 
                type="text" 
                placeholder="Adicionar nova tarefa (Ex: Limpar bebedouro do Estábulo 2)..." 
                required
              >
              <button type="submit" class="btn-add-task">Adicionar</button>
            </form>

            <div class="task-list">
              <div 
                v-for="task in tasks" 
                :key="task.id" 
                class="task-item" 
                :class="{ 'completed': task.done }"
              >
                <label class="checkbox-container">
                  <input type="checkbox" v-model="task.done">
                  <span class="checkmark"></span>
                </label>
                <span class="task-text">{{ task.description }}</span>
                <button @click="removeTask(task.id)" class="btn-delete-task">Excluir</button>
              </div>
              <div v-if="tasks.length === 0" class="empty-state">
                <p>Nenhuma tarefa pendente. Excelente trabalho!</p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isMenuOpen = ref(true);

const toggleMenu = () => { isMenuOpen.value = !isMenuOpen.value; };
const logout = () => {
  localStorage.clear();
  router.push('/login');
};

const currentData = computed(() => {
  return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'full' }).format(new Date());
});

// LÓGICA DE TAREFAS
const newTaskDesc = ref('');
const tasks = ref([
  { id: 1, description: 'Verificar cerca do Estábulo 3', done: false },
  { id: 2, description: 'Separar lote para ordenha da tarde', done: true }
]);

const addTask = () => {
  if (!newTaskDesc.value.trim()) return;
  tasks.value.push({
    id: Date.now(),
    description: newTaskDesc.value,
    done: false
  });
  newTaskDesc.value = '';
};

const removeTask = (id) => {
  tasks.value = tasks.value.filter(t => t.id !== id);
};
</script>

<style scoped>
/* ESTILO LIMPO E FOCADO PARA O OPERADOR */
.dashboard-wrapper { display: flex; height: 100vh; background-color: #f8fafc; color: #0f172a; font-family: 'Inter', 'Segoe UI', sans-serif; overflow: hidden; }

/* SIDEBAR (Mesmo padrão visual do ADM) */
.sidebar-drawer { width: 260px; background: #ffffff; border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; z-index: 100; }
.sidebar-content { display: flex; flex-direction: column; height: 100%; }
.drawer-header { display: flex; align-items: center; gap: 12px; padding: 24px 20px; border-bottom: 1px solid #e2e8f0; }
.drawer-logo { width: 40px; }
.brand-name { font-size: 1.1rem; font-weight: 700; color: #0f172a; }
.drawer-menu { display: flex; flex-direction: column; padding: 20px 12px; flex: 1; gap: 4px; }
.nav-link { display: flex; align-items: center; gap: 12px; padding: 12px 16px; text-decoration: none; color: #64748b; border-radius: 8px; transition: 0.2s; font-weight: 500; font-size: 0.95rem; }
.nav-link:hover, .nav-link.active { background: #fdf4ff; color: #c026d3; } /* Operador ganha um acento visual diferente, ex: roxo/magenta */
.nav-icon { font-size: 1.2rem; width: 24px; text-align: center; }
.btn-logout { margin: 20px; padding: 12px; background: transparent; border: 1px solid #e2e8f0; color: #ef4444; border-radius: 8px; cursor: pointer; transition: 0.2s; font-weight: 600; }
.btn-logout:hover { background: #fef2f2; border-color: #fca5a5; }

/* TOP BAR */
.main-layout { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }
.top-bar { display: flex; justify-content: space-between; align-items: center; padding: 16px 32px; background: #ffffff; border-bottom: 1px solid #e2e8f0; }
.btn-menu { background: transparent; border: none; font-size: 1.5rem; cursor: pointer; color: #0f172a; }
.user-info { display: flex; align-items: center; gap: 12px; }
.user-role { color: #64748b; font-size: 0.9rem; font-weight: 500; }
.avatar { width: 36px; height: 36px; border-radius: 50%; background: #c026d3; color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9rem; }

/* CONTENT */
.dashboard-content { padding: 40px; max-width: 900px; margin: 0 auto; width: 100%; box-sizing: border-box; }
.welcome-section { margin-bottom: 32px; }
.welcome-section h1 { font-size: 2rem; color: #0f172a; margin-bottom: 8px; font-weight: 700; }
.welcome-section p { color: #64748b; font-size: 1.05rem; }

/* TASKS */
.tasks-container { display: flex; flex-direction: column; gap: 24px; }
.tasks-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0; }
.card-header h2 { font-size: 1.25rem; color: #0f172a; }
.date-today { color: #64748b; font-size: 0.9rem; text-transform: capitalize; }

.add-task-form { display: flex; gap: 12px; margin-bottom: 32px; }
.add-task-form input { flex: 1; padding: 14px 16px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 1rem; color: #0f172a; outline: none; transition: border-color 0.2s; }
.add-task-form input:focus { border-color: #c026d3; }
.btn-add-task { background: #c026d3; color: #ffffff; border: none; padding: 0 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-add-task:hover { background: #a21caf; }

.task-list { display: flex; flex-direction: column; gap: 12px; }
.task-item { display: flex; align-items: center; gap: 16px; padding: 16px; border: 1px solid #e2e8f0; border-radius: 8px; transition: all 0.2s ease; background: #ffffff; }
.task-item:hover { border-color: #cbd5e1; }
.task-item.completed { background: #f8fafc; border-color: #e2e8f0; opacity: 0.7; }
.task-item.completed .task-text { text-decoration: line-through; color: #94a3b8; }

.task-text { flex: 1; font-size: 1rem; color: #0f172a; }
.btn-delete-task { background: transparent; border: none; color: #ef4444; font-size: 0.9rem; font-weight: 500; cursor: pointer; opacity: 0; transition: opacity 0.2s; }
.task-item:hover .btn-delete-task { opacity: 1; }
.btn-delete-task:hover { text-decoration: underline; }

/* Custom Checkbox */
.checkbox-container { display: block; position: relative; cursor: pointer; width: 24px; height: 24px; }
.checkbox-container input { position: absolute; opacity: 0; cursor: pointer; height: 0; width: 0; }
.checkmark { position: absolute; top: 0; left: 0; height: 24px; width: 24px; background-color: #fff; border: 2px solid #cbd5e1; border-radius: 6px; transition: 0.2s; }
.checkbox-container:hover input ~ .checkmark { border-color: #c026d3; }
.checkbox-container input:checked ~ .checkmark { background-color: #c026d3; border-color: #c026d3; }
.checkmark:after { content: ""; position: absolute; display: none; }
.checkbox-container input:checked ~ .checkmark:after { display: block; }
.checkbox-container .checkmark:after { left: 7px; top: 3px; width: 6px; height: 12px; border: solid white; border-width: 0 2px 2px 0; transform: rotate(45deg); }

.empty-state { text-align: center; padding: 32px; color: #64748b; font-style: italic; }
</style>