<template>
  <div class="dashboard-wrapper">
    <main class="main-layout">
      <header class="top-bar">
        <div class="brand-section">
          <div class="brand-badge">LS</div>
          <div>
            <p class="brand-name">L.S Management</p>
            <p class="brand-subtitle">Gestão Técnica</p>
          </div>
        </div>

        <nav class="dashboard-nav" aria-label="Navegação principal">
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
            </div>
          </div>
          <div class="nav-dropdown" @click.stop="toggleDropdown('relatorios')">
            <button class="nav-trigger" :class="{active: openDropdown === 'relatorios'}">Relatórios ▾</button>
            <div v-if="openDropdown === 'relatorios'" class="dropdown-menu">
              <router-link to="/relatorios" class="dropdown-item" @click="closeDropdown">Relatórios</router-link>
            </div>
          </div>
        </nav>

        <div class="right-controls">
          <div class="user-info">
            <span class="user-role">Administrador Geral</span>
            <div class="avatar">AD</div>
          </div>
          <button @click="logout" class="btn-logout">⏻ Sair</button>
        </div>
      </header>

      <div class="dashboard-content">
        <div class="welcome-section">
          <h1>Visão Geral da Fazenda</h1>
          <p>Acompanhe e gerencie as principais métricas do rebanho.</p>
        </div>

        <section class="main-highlight-card">
          <div class="highlight-copy-side">
            <div class="highlight-copy-badge">
              <span class="highlight-copy-dot"></span>
              <span class="highlight-copy-text">Gestão Técnica</span>
            </div>
            <h2>Gestão de Estábulos</h2>
            <p>Acesse a lista completa de estábulos para visualizar ocupação, movimentar lotes, editar ou remover animais específicos de cada setor.</p>
            <button @click="$router.push('/estabulos')" class="btn-primary btn-secondary-restored">
              Acessar Estábulos →
            </button>
          </div>

          <div class="highlight-visual-side">
            <img src="@/assets/Estabulo.jpeg" alt="Estábulo" class="highlight-cover-image">
          </div>
        </section>

        <h3 class="section-title">Controles Operacionais</h3>
        <div class="secondary-cards-grid">
          <div class="action-card" @click="$router.push('/animais')">
            <div class="card-icon">◈</div>
            <div class="card-text">
              <h4>Animais</h4>
              <p>Listagem e cadastro do rebanho</p>
            </div>
          </div>
          <div class="action-card" @click="$router.push('/lancamento-leite')">
            <div class="card-icon">🥛</div>
            <div class="card-text">
              <h4>Produção de Leite</h4>
              <p>Registros e histórico de ordenha</p>
            </div>
          </div>
          <div class="action-card" @click="$router.push('/pesagem')">
            <div class="card-icon">⚖️</div>
            <div class="card-text">
              <h4>Registro de Peso</h4>
              <p>Registre o peso do rebanho rapidamente.</p>
            </div>
          </div>
          <div class="action-card" @click="$router.push('/vacinacao')">
            <div class="card-icon">✛</div>
            <div class="card-text">
              <h4>Vacinação</h4>
              <p>Manejo sanitário e histórico</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
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
  // Fecha dropdown se clicar fora do nav
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
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.dashboard-wrapper {
  min-height: 100vh;
  background-color: #f8fafc;
  color: #0f172a;
  font-family: 'Inter', sans-serif;
}

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
  background: #16a34a;
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
  background: #f8fafc;
  border: 1px solid #e2e8f0;
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
  background: #f0fdf4;
  color: #15803d;
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
  background: #16a34a;
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
  max-width: 1200px;
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

.main-highlight-card {
  background: linear-gradient(180deg, #ffffff 0%, #fcfdfd 100%);
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 0;
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 20px;
  align-items: stretch;
  margin-bottom: 40px;
  box-shadow: 0 12px 30px -18px rgba(15, 23, 42, 0.35);
  overflow: hidden;
}

.highlight-copy-side {
  padding: 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 16px;
}

.highlight-copy-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #f0fdf4;
  border: 1px solid #dcfce7;
  border-radius: 999px;
  padding: 6px 12px;
  width: fit-content;
}

.highlight-copy-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #16a34a;
}

.highlight-copy-text {
  color: #166534;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.highlight-copy-side h2 {
  font-size: 1.8rem;
  color: #0f172a;
  margin: 0;
}

.highlight-copy-side p {
  color: #64748b;
  line-height: 1.6;
  margin: 0;
  max-width: 620px;
}

.highlight-copy-side .btn-primary {
  width: fit-content;
  margin-top: 8px;
}

.btn-secondary-restored {
  background: #16a34a;
  color: #ffffff;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: 0.2s;
}

.btn-secondary-restored:hover {
  background: #15803d;
}

.highlight-visual-side {
  position: relative;
  min-height: 280px;
  display: flex;
  align-items: stretch;
  justify-content: stretch;
}

.highlight-cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  position: relative;
  z-index: 1;
  border-radius: 0;
  filter: saturate(1.05);
}

.highlight-visual-side::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  z-index: 2;
  pointer-events: none;
  background: linear-gradient(180deg, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0.18) 30%, rgba(255,255,255,0.05) 100%);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.55);
}

.highlight-visual-side::after {
  content: '';
  position: absolute;
  inset: 0;
  z-index: 3;
  pointer-events: none;
  background: linear-gradient(90deg, rgba(255,255,255,0.72) 0%, rgba(255,255,255,0.18) 35%, rgba(255,255,255,0) 65%, rgba(255,255,255,0.3) 100%);
  mix-blend-mode: soft-light;
}

.section-title {
  font-size: 1.1rem;
  color: #0f172a;
  margin-bottom: 16px;
  font-weight: 600;
}

.secondary-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.action-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border-color: #16a34a;
}

.action-card .card-icon {
  font-size: 2rem;
  color: #16a34a;
  background: #f0fdf4;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.card-text h4 {
  font-size: 1.1rem;
  color: #0f172a;
  margin-bottom: 4px;
}

.card-text p {
  font-size: 0.9rem;
  color: #64748b;
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

.dashboard-wrapper.dark {
  background-color: #0f172a;
  color: #e5e7eb;
}

.dashboard-wrapper.dark .top-bar {
  background: #111827;
  border-color: #1f2937;
}

.dashboard-wrapper.dark .brand-name,
.dashboard-wrapper.dark .brand-subtitle,
.dashboard-wrapper.dark .user-role,
.dashboard-wrapper.dark .welcome-section p,
.dashboard-wrapper.dark .highlight-copy-text,
.dashboard-wrapper.dark .card-text p,
.dashboard-wrapper.dark .action-card h4,
.dashboard-wrapper.dark .action-card p,
.dashboard-wrapper.dark .section-title {
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

.dashboard-wrapper.dark .main-highlight-card,
.dashboard-wrapper.dark .action-card,
.dashboard-wrapper.dark .highlight-copy-badge,
.dashboard-wrapper.dark .dashboard-content {
  background: #111827;
}

.dashboard-wrapper.dark .main-highlight-card {
  border-color: #1f2937;
}

.dashboard-wrapper.dark .action-card {
  border: 1px solid #1f2937;
}

.dashboard-wrapper.dark .highlight-copy-badge {
  border: 1px solid #374151;
}

.dashboard-wrapper.dark .btn-secondary-restored,
.dashboard-wrapper.dark .btn-primary {
  background: #7c3aed;
  color: #fff;
}

.dashboard-wrapper.dark .highlight-cover-image {
  filter: brightness(0.95) contrast(1.05);
}
</style>