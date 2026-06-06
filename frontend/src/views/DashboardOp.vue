<template>
  <!-- Adicionamos o mapeamento dinâmico da nossa classe de blindagem escura -->
  <div :class="['ls-op-page-container', { 'ls-op-dark-active': isDark }]">
    <main class="ls-op-main-layout">
      
      <!-- BARRA SUPERIOR OPERACIONAL -->
      <header class="ls-op-top-bar">
        <div class="ls-op-brand-section">
          <div class="ls-op-brand-badge">LO</div>
          <div>
            <p class="ls-op-brand-name">L.S Operacional</p>
            <p class="ls-op-brand-subtitle">Rotina de Campo</p>
          </div>
        </div>

        <nav class="ls-op-dashboard-nav" aria-label="Navegação principal do operador">
          <div class="ls-op-nav-dropdown" @click.stop="toggleDropdown('cadastro')">
            <button class="ls-op-nav-trigger" :class="{active: openDropdown === 'cadastro'}">Cadastro ▾</button>
            <div v-if="openDropdown === 'cadastro'" class="ls-op-dropdown-menu">
              <router-link to="/estabulos" class="ls-op-dropdown-item" @click="closeDropdown">Estábulo</router-link>
              <router-link to="/especies" class="ls-op-dropdown-item" @click="closeDropdown">Espécie</router-link>
              <router-link to="/racas" class="ls-op-dropdown-item" @click="closeDropdown">Raça</router-link>
              <router-link to="/vacinas" class="ls-op-dropdown-item" @click="closeDropdown">Vacina</router-link>
              <router-link to="/dashboard-alimentacao" class="ls-op-dropdown-item" @click="closeDropdown">Alimentação</router-link>
              <router-link to="/animais" class="ls-op-dropdown-item" @click="closeDropdown">Animal</router-link>
            </div>
          </div>
          <div class="ls-op-nav-dropdown" @click.stop="toggleDropdown('operacional')">
            <button class="ls-op-nav-trigger" :class="{active: openDropdown === 'operacional'}">Operacional ▾</button>
            <div v-if="openDropdown === 'operacional'" class="ls-op-dropdown-menu">
              <router-link to="/pesagem" class="ls-op-dropdown-item" @click="closeDropdown">Peso</router-link>
              <router-link to="/lancamento-leite" class="ls-op-dropdown-item" @click="closeDropdown">Registro de leite</router-link>
              <router-link to="/vacinacao" class="ls-op-dropdown-item" @click="closeDropdown">Aplicar vacinação</router-link>
              <router-link to="/lancamento-alimentacao" class="ls-op-dropdown-item" @click="closeDropdown">Registro de alimentação</router-link>
              <router-link to="/veterinario" class="ls-op-dropdown-item" @click="closeDropdown">Veterinário</router-link>
              <router-link to="/rebanho" class="ls-op-dropdown-item" @click="closeDropdown">Ficha do Animal</router-link>
            </div>
          </div>
          <div class="ls-op-nav-dropdown" @click.stop="toggleDropdown('relatorios')">
            <button class="ls-op-nav-trigger" :class="{active: openDropdown === 'relatorios'}">Relatórios ▾</button>
            <div v-if="openDropdown === 'relatorios'" class="ls-op-dropdown-menu">
              <router-link to="/relatorios" class="ls-op-dropdown-item" @click="closeDropdown">Relatórios</router-link>
              <router-link :to="{ path: '/relatorios', query: { tab: 'herd_report' } }" class="ls-op-dropdown-item" @click="closeDropdown">Relatório do Rebanho</router-link>
            </div>
          </div>
        </nav>

        <div class="ls-op-right-controls">
          <div class="ls-op-user-info">
            <span class="ls-op-user-role">Operador de Campo</span>
            <div class="ls-op-avatar">OP</div>
          </div>
          <button @click="logout" class="ls-op-btn-logout">⏻ Sair</button>
        </div>
      </header>

      <!-- CONTEÚDO PRINCIPAL (GRID REESTRUTURADO E SIMÉTRICO) -->
      <div class="ls-op-dashboard-content">
        <div class="ls-op-welcome-section">
          <h1 class="ls-op-page-title">Rotina Operacional</h1>
          <p class="ls-op-page-subtitle">Gerencie suas tarefas diárias de manejo no campo com foco e agilidade.</p>
        </div>

        <div class="ls-op-tasks-grid-layout">
          
          <!-- CARD DE CRIAÇÃO (ESQUERDA) -->
          <section class="ls-op-task-card-block ls-op-creation-side">
            <div class="ls-op-card-badge-header">
              <span class="ls-op-badge-dot"></span>
              <span class="ls-op-badge-text-tag">Manejo Diário</span>
            </div>
            <h2 class="ls-op-card-title">Adicionar Tarefa</h2>
            <p class="ls-op-card-description">Crie um novo apontamento ou lembrete de manejo rápido para organizar a sua rotina de campo.</p>
            
            <form @submit.prevent="addTask" class="ls-op-add-task-form">
              <input 
                v-model="newTaskDesc" 
                type="text" 
                placeholder="Ex: Conferir bebedouro do Estábulo 2" 
                class="ls-op-task-input-field"
                required
              >
              <button type="submit" class="ls-op-btn-submit-task">Adicionar na Lista</button>
            </form>
          </section>

          <!-- CARD DE LISTAGEM (DIREITA) -->
          <section class="ls-op-task-card-block ls-op-list-side">
            <header class="ls-op-list-card-header">
              <h3 class="ls-op-card-title">Minhas Tarefas</h3>
              <span class="ls-op-date-today-tag">{{ currentData }}</span>
            </header>

            <div class="ls-op-task-list-wrapper">
              <div 
                v-for="task in tasks" 
                :key="task.id" 
                :class="['ls-op-task-item-row', { 'ls-op-task-completed': task.done }]"
              >
                <label class="ls-op-checkbox-container">
                  <input type="checkbox" v-model="task.done" class="ls-op-native-checkbox">
                  <span class="ls-op-custom-checkmark"></span>
                </label>
                <span class="ls-op-task-text-content">{{ task.description }}</span>
                <button @click="removeTask(task.id)" class="ls-op-btn-delete-task">Excluir</button>
              </div>

              <div v-if="tasks.length === 0" class="ls-op-empty-tasks-state">
                <p>Nenhuma tarefa pendente para hoje. Excelente trabalho!</p>
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
const newTaskDesc = ref('');
const isDark = ref(false);
let themeObserver = null;

const tasks = ref([
  { id: 1, description: 'Verificar cerca do Estábulo 3', done: false },
  { id: 2, description: 'Separar lote para ordenha da tarde', done: true }
]);

const currentData = computed(() => {
  return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'full' }).format(new Date());
});

const toggleDropdown = (menu) => {
  openDropdown.value = openDropdown.value === menu ? null : menu;
};

const closeDropdown = () => { openDropdown.value = null; };

const handleClickOutside = (e) => {
  if (!e.target.closest('.ls-op-dashboard-nav')) closeDropdown();
};

const checkGlobalTheme = () => {
  const root = document.documentElement;
  const body = document.body;
  isDark.value = root.classList.contains('dark') || 
                 root.classList.contains('theme-dark') || 
                 body.classList.contains('dark') || 
                 body.classList.contains('theme-dark');
};

onMounted(() => {
  window.addEventListener('click', handleClickOutside);
  checkGlobalTheme();

  themeObserver = new MutationObserver(() => {
    checkGlobalTheme();
  });
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  themeObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });
});

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside);
  if (themeObserver) themeObserver.disconnect();
});

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

const logout = () => {
  localStorage.clear();
  router.push('/');
};
</script>

<style scoped>
/* ==========================================================================
   ESTRUTURA BASE E TEMA CLARO OPERACIONAL (ROXO)
   ========================================================================== */
.ls-op-page-container {
  min-height: 100vh;
  background-color: #f8fafc;
  color: #0f172a;
  font-family: 'Lexend', sans-serif;
  transition: background-color 0.2s, color 0.2s;
  box-sizing: border-box;
}
.ls-op-main-layout { display: flex; flex-direction: column; min-height: 100vh; }

.ls-op-top-bar {
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
.ls-op-brand-section { display: flex; align-items: center; gap: 12px; }
.ls-op-brand-badge {
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
.ls-op-brand-name { margin: 0; font-size: 0.98rem; font-weight: 800; color: #0f172a; }
.ls-op-brand-subtitle { margin: 2px 0 0; font-size: 0.68rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.16em; }

.ls-op-dashboard-nav { display: flex; align-items: center; gap: 10px; flex: 1; justify-content: center; }
.ls-op-nav-dropdown { position: relative; }
.ls-op-nav-trigger {
  cursor: pointer;
  background: #faf5ff;
  border: 1px solid #f3e8ff;
  border-radius: 999px;
  padding: 10px 16px;
  color: #0f172a;
  font-size: 0.9rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: inherit;
}
.ls-op-dropdown-menu {
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
  box-shadow: 0 12px 24px -12px rgba(15, 23, 42, 0.15);
  padding: 8px;
  z-index: 10;
}
.ls-op-dropdown-item {
  text-decoration: none;
  color: #334155;
  font-weight: 600;
  padding: 10px 12px;
  border-radius: 8px;
  transition: 0.2s;
}
.ls-op-dropdown-item:hover, .ls-op-dropdown-item.router-link-active { background: #faf5ff; color: #a21caf; }

.ls-op-right-controls { display: flex; align-items: center; gap: 12px; }
.ls-op-user-info { display: flex; align-items: center; gap: 10px; }
.ls-op-user-role { color: #64748b; font-size: 0.88rem; font-weight: 600; }
.ls-op-avatar { width: 36px; height: 36px; border-radius: 50%; background: #c026d3; color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9rem; }
.ls-op-btn-logout { border: 1px solid #e2e8f0; background: #fff; color: #ef4444; border-radius: 999px; padding: 9px 16px; font-weight: 700; cursor: pointer; font-family: inherit; }

/* LAYOUT DE CARDS SIMÉTRICOS LADO A LADO */
.ls-op-dashboard-content { padding: 40px; max-width: 1200px; margin: 0 auto; width: 100%; box-sizing: border-box; }
.ls-op-welcome-section { margin-bottom: 32px; }
.ls-op-page-title { font-size: 2rem; color: #0f172a; margin: 0 0 8px 0; font-weight: 800; letter-spacing: -0.5px; }
.ls-op-page-subtitle { color: #64748b; font-size: 1.05rem; margin: 0; }

.ls-op-tasks-grid-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: start; }
.ls-op-task-card-block { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 32px; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.03); min-height: 340px; box-sizing: border-box; }

/* CARD ESQUERDA: CRIAÇÃO */
.ls-op-card-badge-header { display: inline-flex; align-items: center; gap: 8px; background: #faf5ff; border: 1px solid #f3e8ff; border-radius: 999px; padding: 6px 12px; margin-bottom: 16px; }
.ls-op-badge-dot { width: 8px; height: 8px; border-radius: 50%; background: #7c3aed; }
.ls-op-badge-text-tag { color: #6d28d9; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; }
.ls-op-card-title { font-size: 1.35rem; color: #0f172a; margin: 0 0 12px 0; font-weight: 700; }
.ls-op-card-description { color: #64748b; font-size: 0.95rem; line-height: 1.6; margin: 0 0 24px 0; }

.ls-op-add-task-form { display: flex; flex-direction: column; gap: 14px; }
.ls-op-task-input-field { padding: 14px 16px; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 1rem; color: #0f172a; outline: none; transition: border-color 0.2s; font-family: inherit; font-weight: 600; }
.ls-op-task-input-field:focus { border-color: #7c3aed; }
.ls-op-btn-submit-task { background: #7c3aed; color: #ffffff; border: none; padding: 14px; border-radius: 10px; font-weight: 700; font-size: 1rem; cursor: pointer; transition: background 0.2s; font-family: inherit; }
.ls-op-btn-submit-task:hover { background: #6d28d9; }

/* CARD DIREITA: LISTAGEM */
.ls-op-list-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0; }
.ls-op-list-card-header .ls-op-card-title { margin-bottom: 0; }
.ls-op-date-today-tag { color: #64748b; font-size: 0.88rem; font-weight: 600; text-transform: capitalize; }
.ls-op-task-list-wrapper { display: flex; flex-direction: column; gap: 12px; }

.ls-op-task-item-row { display: flex; align-items: center; gap: 16px; padding: 14px 16px; border: 1px solid #e2e8f0; border-radius: 10px; background: #ffffff; transition: all 0.2s; }
.ls-op-task-item-row:hover { border-color: #cbd5e1; }
.ls-op-task-text-content { flex: 1; font-size: 0.98rem; color: #0f172a; font-weight: 600; }

.ls-op-btn-delete-task { background: transparent; border: none; color: #ef4444; font-size: 0.88rem; font-weight: 700; cursor: pointer; opacity: 0; transition: opacity 0.2s; font-family: inherit; }
.ls-op-task-item-row:hover .ls-op-btn-delete-task { opacity: 1; }
.ls-op-btn-delete-task:hover { text-decoration: underline; }

/* CHECKBOX INTERATIVO PREMIUM */
.ls-op-checkbox-container { display: block; position: relative; cursor: pointer; width: 22px; height: 22px; }
.ls-op-native-checkbox { position: absolute; opacity: 0; cursor: pointer; height: 0; width: 0; }
.ls-op-custom-checkmark { position: absolute; top: 0; left: 0; height: 22px; width: 22px; background-color: #fff; border: 2px solid #cbd5e1; border-radius: 6px; transition: 0.2s; }
.ls-op-checkbox-container:hover input ~ .ls-op-custom-checkmark { border-color: #7c3aed; }
.ls-op-checkbox-container input:checked ~ .ls-op-custom-checkmark { background-color: #7c3aed; border-color: #7c3aed; }
.ls-op-custom-checkmark:after { content: ""; position: absolute; display: none; }
.ls-op-checkbox-container input:checked ~ .ls-op-custom-checkmark:after { display: block; }
.ls-op-checkbox-container .ls-op-custom-checkmark:after { left: 6px; top: 2px; width: 5px; height: 11px; border: solid white; border-width: 0 2px 2px 0; transform: rotate(45deg); }

/* ESTADO CONCLUÍDO (LIGHT) */
.ls-op-task-item-row.ls-op-task-completed { background: #f8fafc; opacity: 0.75; }
.ls-op-task-item-row.ls-op-task-completed .ls-op-task-text-content { text-decoration: line-through; color: #94a3b8; }

.ls-op-empty-tasks-state { text-align: center; padding: 40px 20px; color: #64748b; font-style: italic; font-weight: 500; }

/* RESPONSIVIDADE */
@media (max-width: 900px) {
  .ls-op-tasks-grid-layout { grid-template-columns: 1fr; }
  .ls-op-top-bar { flex-wrap: wrap; }
  .ls-op-dashboard-nav { order: 3; width: 100%; justify-content: flex-start; overflow-x: auto; }
}

/* ==========================================================================
   BLINDAGEM DO TEMA ESCURO AUTOMÁTICO (MAPEANDO .ls-op-dark-active)
   ========================================================================== */
.ls-op-page-container.ls-op-dark-active {
  background-color: #000000 !important; /* Fundo 100% Preto */
}

/* Topbar e Menus Escuros */
.ls-op-page-container.ls-op-dark-active .ls-op-top-bar {
  background-color: #0f172a !important;
  border-bottom-color: #1f2937 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-nav-trigger {
  background-color: #1f2937 !important;
  border-color: #374151 !important;
  color: #ffffff !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-dropdown-menu {
  background-color: #111827 !important;
  border-color: #374151 !important;
  box-shadow: 0 12px 24px -12px rgba(0, 0, 0, 0.6) !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-dropdown-item {
  color: #e2e8f0 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-dropdown-item:hover,
.ls-op-page-container.ls-op-dark-active .ls-op-dropdown-item.router-link-active {
  background-color: #374151 !important;
  color: #ffffff !important;
}

/* Cards Sólidos Symmetrical Grafite */
.ls-op-page-container.ls-op-dark-active .ls-op-task-card-block {
  background-color: #111827 !important;
  border-color: #1f2937 !important;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5) !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-list-card-header {
  border-bottom-color: #1f2937 !important;
}

/* Linhas das Tarefas e Inputs Modificados para Sólido Grafite */
.ls-op-page-container.ls-op-dark-active .ls-op-task-item-row {
  background-color: #111827 !important;
  border-color: #1f2937 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-task-item-row:hover {
  border-color: #374151 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-task-input-field {
  background-color: #1f2937 !important;
  border-color: #374151 !important;
  color: #ffffff !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-task-input-field:focus {
  border-color: #c026d3 !important;
}

/* Badge de Identificação Operacional */
.ls-op-page-container.ls-op-dark-active .ls-op-card-badge-header {
  background-color: #1f2937 !important;
  border-color: #374151 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-badge-text-tag {
  color: #c026d3 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-badge-dot {
  background-color: #c026d3 !important;
}

/* Checkbox Escuro Customizado */
.ls-op-page-container.ls-op-dark-active .ls-op-custom-checkmark {
  background-color: #1f2937 !important;
  border-color: #4b5563 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-checkbox-container:hover input ~ .ls-op-custom-checkmark {
  border-color: #c026d3 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-checkbox-container input:checked ~ .ls-op-custom-checkmark {
  background-color: #c026d3 !important;
  border-color: #c026d3 !important;
}

/* Estado de Tarefa Concluída no Modo Escuro (Sem sumir o texto) */
.ls-op-page-container.ls-op-dark-active .ls-op-task-item-row.ls-op-task-completed {
  background-color: #1f2937 !important;
  opacity: 0.65 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-task-item-row.ls-op-task-completed .ls-op-task-text-content {
  color: #9ca3af !important;
}

/* Forçamento das Fontes para Branco Puro */
.ls-op-page-container.ls-op-dark-active .ls-op-page-title,
.ls-op-page-container.ls-op-dark-active .ls-op-card-title,
.ls-op-page-container.ls-op-dark-active .ls-op-task-text-content,
.ls-op-page-container.ls-op-dark-active .ls-op-brand-name,
.ls-op-page-container.ls-op-dark-active .ls-op-user-role {
  color: #ffffff !important;
}

/* Textos Secundários em Cinza Claro Legível */
.ls-op-page-container.ls-op-dark-active .ls-op-page-subtitle,
.ls-op-page-container.ls-op-dark-active .ls-op-card-description,
.ls-op-page-container.ls-op-dark-active .ls-op-date-today-tag,
.ls-op-page-container.ls-op-dark-active .ls-op-empty-tasks-state,
.ls-op-page-container.ls-op-dark-active .ls-op-brand-subtitle {
  color: #cbd5e1 !important;
}

.ls-op-page-container.ls-op-dark-active .ls-op-btn-logout {
  background-color: #1f2937 !important;
  border-color: #374151 !important;
  color: #fca5a5 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-btn-submit-task {
  background-color: #c026d3 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-btn-submit-task:hover {
  background-color: #a21caf !important;
}
</style>