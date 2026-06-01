<template>
  <div class="dashboard-wrapper op-theme">
    <main class="main-layout">
      <header class="top-bar">
        <div class="brand-section">
          <div class="brand-badge">LO</div>
          <div>
            <p class="brand-name">L.S Operacional</p>
            <p class="brand-subtitle">Rotina de Campo</p>
          </div>
        </div>

        <nav class="dashboard-nav" aria-label="Navegação principal do operador">
          <div class="nav-dropdown" @click.stop="toggleDropdown('cadastro')">
            <button class="nav-trigger" :class="{active: openDropdown === 'cadastro'}">Cadastro ▾</button>
            <div v-if="openDropdown === 'cadastro'" class="dropdown-menu">
              <router-link to="/estabulos" class="dropdown-item" @click="closeDropdown">Estábulo</router-link>
              <router-link to="/especies" class="dropdown-item" @click="closeDropdown">Espécie</router-link>
              <router-link to="/racas" class="dropdown-item" @click="closeDropdown">Raça</router-link>
              <router-link to="/vacinas" class="dropdown-item" @click="closeDropdown">Vacina</router-link>
              <router-link to="/animais/novo" class="dropdown-item" @click="closeDropdown">+ Adicionar Animal</router-link>
            </div>
          </div>
          <div class="nav-dropdown" @click.stop="toggleDropdown('operacional')">
            <button class="nav-trigger" :class="{active: openDropdown === 'operacional'}">Operacional ▾</button>
            <div v-if="openDropdown === 'operacional'" class="dropdown-menu">
              <router-link to="/animais" class="dropdown-item" @click="closeDropdown">Animal</router-link>
              <router-link to="/pesagem" class="dropdown-item" @click="closeDropdown">Peso</router-link>
              <router-link to="/lancamento-leite" class="dropdown-item" @click="closeDropdown">Registro de leite</router-link>
              <router-link to="/vacinacao" class="dropdown-item" @click="closeDropdown">Aplicar vacinação</router-link>
              <router-link to="/dashboard-alimentacao" class="dropdown-item" @click="closeDropdown">Alimentação</router-link>
              <router-link to="/lancamento-alimentacao" class="dropdown-item" @click="closeDropdown">Registro de alimentação</router-link>
              <router-link to="/veterinario" class="dropdown-item" @click="closeDropdown">Veterinário</router-link>
              <router-link to="/rebanho" class="dropdown-item" @click="closeDropdown">Ficha do Animal</router-link>
            </div>
          </div>
          <div class="nav-dropdown" @click.stop="toggleDropdown('relatorios')">
            <button class="nav-trigger" :class="{active: openDropdown === 'relatorios'}">Relatórios ▾</button>
            <div v-if="openDropdown === 'relatorios'" class="dropdown-menu">
              <router-link to="/relatorios" class="dropdown-item" @click="closeDropdown">Relatórios</router-link>
              <router-link :to="{ path: '/relatorios', query: { tab: 'herd_report' } }" class="dropdown-item" @click="closeDropdown">Relatório do Rebanho</router-link>
            </div>
          </div>
        </nav>

        <div class="right-controls">
          <div class="user-info">
            <span class="user-role">Operador de Campo</span>
            <div class="avatar">OP</div>
          </div>
          <button @click="logout" class="btn-logout">⏻ Sair</button>
        </div>
      </header>

      <div class="dashboard-content">
        <div class="welcome-section">
          <h1>Rotina Operacional</h1>
          <p>Gerencie suas tarefas diárias de manejo no campo.</p>
        </div>

        <div class="tasks-container">
          <section class="main-highlight-card op-highlight">
            <div class="highlight-copy-side">
              <div class="highlight-copy-badge">
                <span class="highlight-copy-dot"></span>
                <span class="highlight-copy-text">Rotina de Campo</span>
              </div>
              <h2>Organizar Tarefas</h2>
              <p>Crie, acompanhe e conclua as tarefas mais importantes para o manejo diário.</p>
              <form @submit.prevent="addTask" class="add-task-form op-add-form">
                <input v-model="newTaskDesc" type="text" placeholder="Ex: Conferir bebedouro do Estábulo 2" required>
                <button type="submit" class="btn-primary small">Adicionar</button>
              </form>
            </div>

            <div class="highlight-visual-side tasks-list-side">
              <header class="card-header">
                <h3>Minhas Tarefas</h3>
                <span class="date-today">{{ currentData }}</span>
              </header>
              <div class="task-list">
                <div v-for="task in tasks" :key="task.id" class="task-item" :class="{ 'completed': task.done }">
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
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const openDropdown = ref(null);

function toggleDropdown(menu) {
  openDropdown.value = openDropdown.value === menu ? null : menu;
}

function closeDropdown() {
  openDropdown.value = null;
}

function handleClickOutside(e) {
  if (!e.target.closest('.dashboard-nav')) {
    closeDropdown();
  }
}

onMounted(() => {
  window.addEventListener('click', handleClickOutside);
});
onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside);
});

const logout = () => {
  localStorage.clear();
  router.push('/');
};

const currentData = computed(() => {
  return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'full' }).format(new Date());
});

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
.dashboard-wrapper {
  min-height: 100vh;
  background-color: #f8fafc;
  color: #0f172a;
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 18px 28px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 50;
}

.brand-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-badge {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #c026d3;
  color: #fff;
  font-weight: 800;
}

.brand-name {
  margin: 0;
  font-size: 0.98rem;
  font-weight: 800;
  color: #0f172a;
}

.brand-subtitle {
  margin: 2px 0 0;
  font-size: 0.68rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.16em;
}

.dashboard-nav {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  justify-content: center;
}

.nav-dropdown {
  position: relative;
}

.nav-trigger {
  list-style: none;
  cursor: pointer;
  background: #faf5ff;
  border: 1px solid #f3e8ff;
  border-radius: 999px;
  padding: 10px 14px;
  color: #0f172a;
  font-size: 0.9rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.nav-trigger::-webkit-details-marker {
  display: none;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  min-width: 220px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 12px 24px -12px rgba(15, 23, 42, 0.3);
  padding: 8px;
  z-index: 10;
}

.dropdown-item {
  text-decoration: none;
  color: #334155;
  font-weight: 600;
  padding: 10px 12px;
  border-radius: 8px;
  transition: 0.2s ease;
}

.dropdown-item:hover,
.dropdown-item.router-link-active {
  background: #faf5ff;
  color: #a21caf;
}

.right-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-role {
  color: #64748b;
  font-size: 0.88rem;
  font-weight: 600;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #c026d3;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
}

.btn-logout {
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #ef4444;
  border-radius: 999px;
  padding: 9px 12px;
  font-weight: 700;
  cursor: pointer;
}

.dashboard-content {
  padding: 40px;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.welcome-section {
  margin-bottom: 32px;
}

.welcome-section h1 {
  font-size: 2rem;
  color: #0f172a;
  margin-bottom: 8px;
  font-weight: 700;
}

.welcome-section p {
  color: #64748b;
  font-size: 1.05rem;
}

.tasks-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.tasks-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.card-header h2 {
  font-size: 1.25rem;
  color: #0f172a;
}

.date-today {
  color: #64748b;
  font-size: 0.9rem;
  text-transform: capitalize;
}

.add-task-form {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
}

.add-task-form input {
  flex: 1;
  padding: 14px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  color: #0f172a;
  outline: none;
  transition: border-color 0.2s;
}

.add-task-form input:focus {
  border-color: #c026d3;
}

.btn-add-task {
  background: #c026d3;
  color: #ffffff;
  border: none;
  padding: 0 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-add-task:hover {
  background: #a21caf;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.2s ease;
  background: #ffffff;
}

.task-item:hover {
  border-color: #cbd5e1;
}

.task-item.completed {
  background: #f8fafc;
  border-color: #e2e8f0;
  opacity: 0.7;
}

.task-item.completed .task-text {
  text-decoration: line-through;
  color: #94a3b8;
}

.task-text {
  flex: 1;
  font-size: 1rem;
  color: #0f172a;
}

.btn-delete-task {
  background: transparent;
  border: none;
  color: #ef4444;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s;
}

.task-item:hover .btn-delete-task {
  opacity: 1;
}

.btn-delete-task:hover {
  text-decoration: underline;
}

.checkbox-container {
  display: block;
  position: relative;
  cursor: pointer;
  width: 24px;
  height: 24px;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 24px;
  width: 24px;
  background-color: #fff;
  border: 2px solid #cbd5e1;
  border-radius: 6px;
  transition: 0.2s;
}

.checkbox-container:hover input ~ .checkmark {
  border-color: #c026d3;
}

.checkbox-container input:checked ~ .checkmark {
  background-color: #c026d3;
  border-color: #c026d3;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-container .checkmark:after {
  left: 7px;
  top: 3px;
  width: 6px;
  height: 12px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.empty-state {
  text-align: center;
  padding: 32px;
  color: #64748b;
  font-style: italic;
}

@media (max-width: 900px) {
  .top-bar {
    flex-wrap: wrap;
  }

  .dashboard-nav {
    order: 3;
    width: 100%;
    justify-content: flex-start;
    overflow-x: auto;
  }
}

.main-highlight-card.op-highlight {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 12px 24px -12px rgba(15,23,42,0.18);
  align-items: center;
}

.op-highlight .highlight-copy-side {
  padding: 20px;
}

.op-highlight .highlight-copy-badge { background: #faf5ff; border: 1px solid #f3e8ff; }
.op-highlight .highlight-copy-dot { background: #7c3aed; }
.op-highlight .btn-primary.small { padding: 8px 14px; border-radius: 10px; background: #7c3aed; }

.tasks-list-side { padding: 12px 18px; }
.tasks-list-side .card-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }

.op-add-form { display:flex; gap:10px; margin-top:12px; }
.op-add-form input { flex:1; padding:10px 12px; border-radius:8px; border:1px solid #e2e8f0; }

.btn-theme-toggle {
  border: 1px solid #cbd5e1;
  background: #eef2ff;
  color: #1f2937;
  border-radius: 999px;
  width: 38px;
  height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
}

.btn-theme-toggle:hover {
  background: #e0e7ff;
  transform: translateY(-1px);
}

.dashboard-wrapper.dark {
  background-color: #0f172a;
  color: #e2e8f0;
}

.dashboard-wrapper.dark .top-bar {
  background: #111827;
  border-color: #1f2937;
}

.dashboard-wrapper.dark .brand-name,
.dashboard-wrapper.dark .brand-subtitle,
.dashboard-wrapper.dark .user-role,
.dashboard-wrapper.dark .task-text,
.dashboard-wrapper.dark .date-today,
.dashboard-wrapper.dark .welcome-section p,
.dashboard-wrapper.dark .highlight-copy-text,
.dashboard-wrapper.dark .highlight-copy-badge,
.dashboard-wrapper.dark .card-header h2,
.dashboard-wrapper.dark .welcome-section h1,
.dashboard-wrapper.dark .action-card h4,
.dashboard-wrapper.dark .action-card p {
  color: #e5e7eb;
}

.dashboard-wrapper.dark .brand-badge {
  background: #8b5cf6;
}

.dashboard-wrapper.dark .nav-trigger {
  background: #1f2937;
  border-color: #374151;
  color: #e5e7eb;
}

.dashboard-wrapper.dark .dropdown-menu {
  background: #111827;
  border-color: #374151;
  box-shadow: 0 12px 24px -12px rgba(0, 0, 0, 0.6);
}

.dashboard-wrapper.dark .dropdown-item {
  color: #e2e8f0;
}

.dashboard-wrapper.dark .dropdown-item:hover,
.dashboard-wrapper.dark .dropdown-item.router-link-active {
  background: #374151;
  color: #fff;
}

.dashboard-wrapper.dark .btn-logout,
.dashboard-wrapper.dark .btn-theme-toggle {
  background: #1f2937;
  border-color: #374151;
  color: #e5e7eb;
}

.dashboard-wrapper.dark .dashboard-content,
.dashboard-wrapper.dark .tasks-container,
.dashboard-wrapper.dark .main-highlight-card,
.dashboard-wrapper.dark .task-item,
.dashboard-wrapper.dark .add-task-form input,
.dashboard-wrapper.dark .task-list,
.dashboard-wrapper.dark .empty-state {
  background: transparent;
}

.dashboard-wrapper.dark .main-highlight-card {
  background: #111827;
  border-color: #1f2937;
}

.dashboard-wrapper.dark .task-item {
  background: #111827;
  border-color: #374151;
}

.dashboard-wrapper.dark .task-item.completed {
  background: #1f2937;
  border-color: #374151;
  opacity: 0.85;
}

.dashboard-wrapper.dark .add-task-form input {
  background: #111827;
  border-color: #374151;
  color: #e5e7eb;
}

.dashboard-wrapper.dark .btn-add-task,
.dashboard-wrapper.dark .btn-primary.small,
.dashboard-wrapper.dark .btn-primary.btn-secondary-restored {
  background: #7c3aed;
  color: #fff;
}

.dashboard-wrapper.dark .welcome-section p,
.dashboard-wrapper.dark .action-card p {
  color: #cbd5e1;
}

.dashboard-wrapper.dark .action-card {
  background: #111827;
  border-color: #1f2937;
}

.dashboard-wrapper.dark .highlight-copy-badge {
  background: #1f2937;
  border-color: #374151;
}

</style>