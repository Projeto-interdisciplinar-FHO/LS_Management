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
              <router-link to="/dashboard-alimentacao" class="dropdown-item" @click="closeDropdown">Alimentação</router-link>
              <router-link to="/animais" class="dropdown-item" @click="closeDropdown">Animal</router-link>
            </div>
          </div>
          <div class="nav-dropdown" @click.stop="toggleDropdown('operacional')">
            <button class="nav-trigger" :class="{active: openDropdown === 'operacional'}">Operacional ▾</button>
            <div v-if="openDropdown === 'operacional'" class="dropdown-menu">
              <router-link to="/pesagem" class="dropdown-item" @click="closeDropdown">Peso</router-link>
              <router-link to="/lancamento-leite" class="dropdown-item" @click="closeDropdown">Registro de leite</router-link>
              <router-link to="/vacinacao" class="dropdown-item" @click="closeDropdown">Aplicar vacinação</router-link>
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
        <section class="page-hero">
          <div class="hero-copy">
            <span class="eyebrow">Painel Administrativo</span>
          </div>
        </section>

        <section class="stats-grid">
          <article class="info-card" v-for="card in statCards" :key="card.title" :class="card.borderClass">
            <div class="card-media">
              <img :src="card.image" :alt="card.title" />
            </div>
            <div class="card-content">
              <span class="card-meta" :class="card.accentClass">{{ card.category }}</span>
              <h2 class="card-title">{{ card.title }}</h2>
              <p class="card-description">{{ card.description }}</p>
              <div class="card-footer">
                <strong class="card-value">{{ card.count }}</strong>
                <span class="card-unit">{{ card.unit }}</span>
              </div>
            </div>
          </article>
        </section>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import animaisImage from '../assets/animais.jpeg';
import estabuloImage from '../assets/Estabulo.jpeg';
import leiteImage from '../assets/leite.jpeg';

const router = useRouter();
const openDropdown = ref(null);
const totalAnimals = ref(0);
const totalQuadrants = ref(0);
const totalVaccinations = ref(0);
const totalFeedings = ref(0);

const statCards = computed(() => [
  {
    category: 'CONTROLE POPULACIONAL',
    title: 'Gestão de Animais',
    count: totalAnimals.value,
    unit: 'cabeças',
    description: 'Visão geral de cabeças registradas na fazenda, mapeando a distribuição biológica de matrizes, e gado de engorda.',
    image: animaisImage,
    accentClass: 'card-meta--green',
    borderClass: 'card-border--green',
  },
  {
    category: 'CAPACIDADE DE ALOCAÇÃO',
    title: 'Lotação de Estábulos',
    count: totalQuadrants.value,
    unit: 'quadrantes',
    description: 'Espaços de confinamento e módulos de pasto rotacionado ativos, monitorando os limites críticos de capacidade.',
    image: estabuloImage,
    accentClass: 'card-meta--blue',
    borderClass: 'card-border--blue',
  },
  {
    category: 'ATIVIDADES COLETADAS',
    title: 'Manejos Realizados',
    count: totalFeedings.value + totalVaccinations.value,
    unit: 'ações hoje',
    description: 'Consolidação técnica das coletas diárias de campo, acumulando todas as pesagens corporais e registros de ordenhas leiteiras.',
    image: leiteImage,
    accentClass: 'card-meta--purple',
    borderClass: 'card-border--purple',
  },
]);

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

async function fetchMetrics() {
  try {
    const [animalsRes, quadrantsRes, vaccinationsRes, feedingsRes] = await Promise.all([
      api.getAnimals(),
      api.getQuadrants(),
      api.getVaccinationsByAnimal(0),
      api.getFeedings()
    ]);

    totalAnimals.value = Array.isArray(animalsRes.data) ? animalsRes.data.length : 0;
    totalQuadrants.value = Array.isArray(quadrantsRes.data) ? quadrantsRes.data.length : 0;
    totalVaccinations.value = Array.isArray(vaccinationsRes.data) ? vaccinationsRes.data.length : 0;
    totalFeedings.value = Array.isArray(feedingsRes.data) ? feedingsRes.data.length : 0;
  } catch (error) {
    console.error('Erro ao carregar métricas do painel administrativo', error);
  }
}

onMounted(() => {
  window.addEventListener('click', handleClickOutside);
  fetchMetrics();
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
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700;800&display=swap');

.dashboard-wrapper {
  min-height: 100vh;
  background: #f0f5fb;
  color: #102a43;
  font-family: 'Lexend', sans-serif;
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
  padding: 20px 32px;
  background: #ffffff;
  border-bottom: 1px solid #d8e3ef;
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
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #16a34a;
  color: #fff;
  font-weight: 800;
}

.brand-name,
.brand-subtitle,
.user-role {
  margin: 0;
}

.brand-name {
  font-size: 1rem;
  font-weight: 800;
  color: #102a43;
}

.brand-subtitle {
  margin-top: 2px;
  font-size: 0.72rem;
  color: #627d98;
  text-transform: uppercase;
  letter-spacing: 0.18em;
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
  cursor: pointer;
  background: #f8fbff;
  border: 1px solid #dfe7ef;
  border-radius: 999px;
  padding: 10px 15px;
  color: #102a43;
  font-size: 0.9rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s ease, border-color 0.2s ease;
}

.nav-trigger.active,
.nav-trigger:hover {
  background: #e8f1fb;
  border-color: #b7d1ec;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  min-width: 170px;
  background: #ffffff;
  border: 1px solid #d8e3ef;
  border-radius: 16px;
  box-shadow: 0 18px 36px rgba(16, 42, 67, 0.08);
  padding: 10px 0;
  z-index: 100;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 10px 18px;
  color: #102a43;
  font-size: 0.92rem;
  text-decoration: none;
}

.dropdown-item:hover {
  background: #eff6ff;
}

.right-controls {
  display: flex;
  align-items: center;
  gap: 14px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0f5b8a;
  color: #fff;
  font-weight: 800;
}

.btn-logout {
  border: 1px solid #d8e3ef;
  background: #ffffff;
  color: #102a43;
  font-weight: 700;
  padding: 10px 16px;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-logout:hover {
  background: #f1f5f9;
}

.dashboard-content {
  width: min(1180px, calc(100% - 48px));
  margin: 32px auto 48px;
  display: grid;
  gap: 32px;
}

.page-hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  width: 100%;
}

.hero-copy {
  display: flex;
  flex-direction: column;
  gap: 18px;
  justify-content: center;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: min(720px, 100%);
  padding: 12px 18px;
  border-radius: 999px;
  background: #16a34a;
  color: #ebf8f1;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  text-align: center;
  margin: 0 auto;
}

.page-hero h1 {
  margin: 0;
  font-size: clamp(2rem, 2.3vw, 3rem);
  line-height: 1.05;
  color: #102a43;
}

.page-hero p {
  margin: 0;
  max-width: 620px;
  line-height: 1.75;
  color: #334e68;
}

.hero-image-card {
  position: relative;
  overflow: hidden;
  border-radius: 32px;
  min-height: 280px;
  background: linear-gradient(180deg, rgba(15,91,138,0.12) 0%, rgba(248,249,255,0.72) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-image-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 24px;
  padding-top: 26px;
  border-top: 1px solid rgba(15, 23, 42, 0.08);
}

.info-card {
  border-radius: 28px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 20px 50px rgba(15, 42, 67, 0.08);
  display: flex;
  flex-direction: column;
  min-height: 420px;
}

.card-media {
  min-height: 180px;
  overflow: hidden;
  background: #f4f7ff;
}

.card-media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.card-meta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #2563eb;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  background: rgba(37, 99, 235, 0.08);
  padding: 8px 12px;
  border-radius: 999px;
}

.card-meta::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

.card-meta--green {
  color: #047857;
  background: rgba(16, 185, 129, 0.08);
}

.card-meta--blue {
  color: #1d4ed8;
  background: rgba(37, 99, 235, 0.08);
}

.card-meta--purple {
  color: #7c3aed;
  background: rgba(168, 85, 247, 0.08);
}

.card-border--green {
  border: 1px solid rgba(16, 185, 129, 0.28);
}

.card-border--blue {
  border: 1px solid rgba(37, 99, 235, 0.28);
}

.card-border--purple {
  border: 1px solid rgba(168, 85, 247, 0.28);
}

.card-value {
  font-size: 3rem;
  color: #102a43;
  line-height: 1;
}

.card-unit {
  display: block;
  color: #64748b;
  font-size: 0.95rem;
  margin-top: 6px;
  text-transform: lowercase;
}

.card-title {
  margin: 0;
  font-size: 1.2rem;
  line-height: 1.3;
  color: #102a43;
}

.card-description {
  margin: 0;
  color: #486581;
  line-height: 1.75;
  min-height: 80px;
}

.card-footer {
  margin-top: auto;
}
.theme-dark .info-card {
  background: #111827;
  border-color: #1f2937;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.18);
}
.theme-dark .card-media {
  background: #0f172a;
}
.theme-dark .card-content {
  background: transparent;
}
.theme-dark .card-title,
.theme-dark .card-description,
.theme-dark .card-unit,
.theme-dark .card-value,
.theme-dark .card-meta,
.theme-dark .eyebrow,
.theme-dark .brand-name,
.theme-dark .brand-subtitle,
.theme-dark .user-role {
  color: #e5e7eb;
}
.theme-dark .card-meta {
  background: rgba(255,255,255,0.06);
}
.theme-dark .card-meta--green {
  background: rgba(16, 185, 129, 0.15);
}
.theme-dark .card-meta--blue {
  background: rgba(37, 99, 235, 0.15);
}
.theme-dark .card-meta--purple {
  background: rgba(168, 85, 247, 0.15);
}
.theme-dark .brand-badge {
  background: #16a34a;
}
.theme-dark .top-bar {
  background: #0f172a;
}
.theme-dark .dashboard-content {
  background: #0b1120;
}
.theme-dark .stats-grid {
  border-top-color: rgba(255, 255, 255, 0.08);
}
.theme-dark .card-description {
  color: #cbd5e1;
}
.theme-dark .card-unit {
  color: #94a3b8;
}
.theme-dark .card-title {
  color: #f8fafc;
}
.theme-dark .btn-logout {
  background: #1f2937;
  color: #e5e7eb;
}
.theme-dark .nav-trigger {
  background: #111827;
  border-color: #1f2937;
  color: #e5e7eb;
}
.theme-dark .dropdown-menu {
  background: #111827;
  border-color: #1f2937;
}
.theme-dark .dropdown-item {
  color: #e5e7eb;
}
.theme-dark .dropdown-item:hover,
.theme-dark .dropdown-item.router-link-active {
  background: #1f2937;
  color: #ffffff;
}
.theme-dark .btn-theme-toggle {
  background: #1f2937;
  color: #e5e7eb;
}
.details-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  padding: 28px 30px;
  background: #ffffff;
  border: 1px solid #d8e3ef;
  border-radius: 28px;
}

.details-row h2 {
  margin: 0 0 10px;
  font-size: 1.2rem;
  color: #102a43;
}

.details-row p {
  margin: 0;
  color: #486581;
  line-height: 1.75;
}

.small-stat {
  min-width: 180px;
  padding: 22px;
  background: #eff6ff;
  border-radius: 22px;
  text-align: center;
}

.small-stat span {
  display: block;
  color: #627d98;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.small-stat strong {
  display: block;
  font-size: 2rem;
  color: #0f172a;
}

@media (max-width: 1100px) {
  .page-hero,
  .stats-grid,
  .details-row {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    gap: 20px;
  }
}

@media (max-width: 720px) {
  .top-bar {
    flex-wrap: wrap;
    justify-content: center;
  }

  .dashboard-nav {
    order: 3;
    width: 100%;
    justify-content: center;
  }

  .hero-image-card {
    min-height: 220px;
  }
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