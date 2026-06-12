<template>
  <div :class="['ls-op-page-container', { 'ls-op-dark-active': isDark }]">
    <main class="ls-op-main-layout">
      
      <!-- BARRA SUPERIOR OPERACIONAL RESTRITA -->
      <header class="ls-op-top-bar">
        <div class="ls-op-brand-section">
          <div class="ls-op-brand-badge">LO</div>
          <div>
            <p class="ls-op-brand-name">L.S Operacional</p>
            <p class="ls-op-brand-subtitle">Rotina de Campo</p>
          </div>
        </div>

        <!-- NAVEGAÇÃO RESTRITA: APENAS OPÇÕES DE MANEJO -->
        <nav class="ls-op-dashboard-nav" aria-label="Navegação principal do operador">
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
        </nav>

        <div class="ls-op-right-controls">
          <div class="ls-op-user-info">
            <span class="ls-op-user-role">Operador de Campo</span>
            <div class="ls-op-avatar">OP</div>
          </div>
          <button @click="logout" class="ls-op-btn-logout">⏻ Sair</button>
        </div>
      </header>

      <!-- CONTEÚDO PRINCIPAL (MÉTRICAS COM IMAGENS ESTILO ADM) -->
      <div class="ls-op-dashboard-content">
        <div class="ls-op-welcome-section">
          <h1 class="ls-op-page-title">Rotina de Manejos</h1>
          <p class="ls-op-page-subtitle">Acompanhe a consolidação técnica das coletas diárias e lançamentos rápidos efetuados hoje.</p>
        </div>

        <!-- GRID DE CARDS COM DOS TRÊS ELEMENTOS DE IMAGEM DO ADM -->
        <section class="ls-op-stats-grid">
          <article class="ls-op-info-card ls-op-border--purple" v-for="card in statCards" :key="card.title">
            <div class="ls-op-card-media">
              <img :src="card.image" :alt="card.title" />
            </div>
            <div class="ls-op-card-content">
              <span class="ls-op-card-meta ls-op-meta--purple">{{ card.category }}</span>
              <h2 class="ls-op-card-title">{{ card.title }}</h2>
              <p class="ls-op-card-description">{{ card.description }}</p>
              <div class="ls-op-card-footer">
                <strong class="ls-op-card-value">{{ card.count }}</strong>
                <span class="ls-op-card-unit">{{ card.unit }}</span>
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

// Importação das imagens idênticas às usadas no painel administrativo
import animaisImage from '../assets/animais.jpeg';
import leiteImage from '../assets/leite.jpeg';

const router = useRouter();
const openDropdown = ref(null);
const isDark = ref(false);
let themeObserver = null;

// Estados numéricos reativos alimentados pela API e incrementos locais
const totalVaccinations = ref(0);
const totalFeedings = ref(0);
const totalMilkRecords = ref(0);
const totalWeighings = ref(0);

// Contador local reativo para capturar ações realizadas em tempo real nesta sessão
const localActionsIncrement = ref(0);

// Configuração dos Cards de Manejo baseados na lógica do Administrador com imagens acopladas
const statCards = computed(() => [
  {
    category: 'MANEJO SANITÁRIO E NUTRICIONAL',
    title: 'Ações de Campo Concluídas',
    count: totalFeedings.value + totalVaccinations.value + localActionsIncrement.value,
    unit: 'lançamentos hoje',
    description: 'Consolidação de atividades executadas diretamente no curral, acumulando o histórico de suplementações e imunizações periódicas do rebanho.',
    image: animaisImage
  },
  {
    category: 'ATIVIDADES COLETADAS',
    title: 'Monitoramento Produtivo',
    count: totalMilkRecords.value + totalWeighings.value,
    unit: 'pesagens e coletas',
    description: 'Acompanhamento do rendimento zootécnico diário na fazenda, consolidando todas as pesagens corporais e ordenhas leiteiras.',
    image: leiteImage
  }
]);

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

const fetchOperationalMetrics = async () => {
  try {
    const [vaccinationsRes, feedingsRes, milkRes] = await Promise.all([
      api.getVaccinationsByAnimal(0),
      api.getFeedings(),
      api.getMilkProductions ? api.getMilkProductions() : { data: [] }
    ]);

    totalVaccinations.value = Array.isArray(vaccinationsRes.data) ? vaccinationsRes.data.length : 0;
    totalFeedings.value = Array.isArray(feedingsRes.data) ? feedingsRes.data.length : 0;
    totalMilkRecords.value = Array.isArray(milkRes.data) ? milkRes.data.length : 0;
    
    // Fallback de pesagens corporais coletadas se o método existir na sua api.js
    if (api.getWeightHistoryByAnimal) {
      const weightsRes = await api.getWeightHistoryByAnimal(0);
      totalWeighings.value = Array.isArray(weightsRes.data) ? weightsRes.data.length : 0;
    }
  } catch (error) {
    console.error('Erro ao buscar métricas de manejo do operador:', error);
  }
};

// Função ouvinte para interceptar quando o operador realiza um lançamento nas subpáginas
const checkLocalManejoUpdates = () => {
  const localSavedManejos = localStorage.getItem('ls_manejo_action_performed');
  if (localSavedManejos) {
    localActionsIncrement.value = parseInt(localSavedManejos, 10);
  }
};

onMounted(() => {
  window.addEventListener('click', handleClickOutside);
  // Escuta atualizações de armazenamento vindas das telas de formulários de registro
  window.addEventListener('storage', checkLocalManejoUpdates);
  
  checkGlobalTheme();
  fetchOperationalMetrics();
  checkLocalManejoUpdates();

  themeObserver = new MutationObserver(() => {
    checkGlobalTheme();
  });
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  themeObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });
});

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside);
  window.removeEventListener('storage', checkLocalManejoUpdates);
  if (themeObserver) themeObserver.disconnect();
});

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
  background-color: #f0f5fb; /* Sincronizado com a cor base do adm */
  color: #102a43;
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
  padding: 20px 32px;
  background: #ffffff;
  border-bottom: 1px solid #d8e3ef;
  position: sticky;
  top: 0;
  z-index: 50;
}
.ls-op-brand-section { display: flex; align-items: center; gap: 12px; }
.ls-op-brand-badge {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #c026d3;
  color: #fff;
  font-weight: 800;
}
.ls-op-brand-name { margin: 0; font-size: 1rem; font-weight: 800; color: #102a43; }
.ls-op-brand-subtitle { margin: 2px 0 0; font-size: 0.72rem; color: #627d98; text-transform: uppercase; letter-spacing: 0.18em; }

.ls-op-dashboard-nav { display: flex; align-items: center; gap: 10px; flex: 1; justify-content: center; }
.ls-op-nav-dropdown { position: relative; }
.ls-op-nav-trigger {
  cursor: pointer;
  background: #faf5ff;
  border: 1px solid #f3e8ff;
  border-radius: 999px;
  padding: 10px 15px;
  color: #102a43;
  font-size: 0.9rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: inherit;
}
.ls-op-dropdown-menu {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  min-width: 220px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: #ffffff;
  border: 1px solid #d8e3ef;
  border-radius: 16px;
  box-shadow: 0 18px 36px rgba(16, 42, 67, 0.08);
  padding: 10px 0;
  z-index: 100;
}
.ls-op-dropdown-item {
  text-decoration: none;
  color: #102a43;
  font-weight: 600;
  padding: 10px 18px;
  border-radius: 8px;
  transition: 0.2s;
}
.ls-op-dropdown-item:hover, .ls-op-dropdown-item.router-link-active { background: #faf5ff; color: #a21caf; }

.ls-op-right-controls { display: flex; align-items: center; gap: 14px; }
.ls-op-user-info { display: flex; align-items: center; gap: 12px; }
.ls-op-user-role { color: #627d98; font-size: 0.88rem; font-weight: 600; }
.ls-op-avatar { width: 36px; height: 36px; border-radius: 50%; background: #c026d3; color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9rem; }
.ls-op-btn-logout { border: 1px solid #d8e3ef; background: #fff; color: #ef4444; border-radius: 999px; padding: 10px 16px; font-weight: 700; cursor: pointer; font-family: inherit; }

/* LAYOUT DE CARDS COM CAPAS DE MÍDIA - PARIDADE ADM */
.ls-op-dashboard-content { padding: 40px; max-width: 1200px; margin: 0 auto; width: 100%; box-sizing: border-box; }
.ls-op-welcome-section { margin-bottom: 32px; }
.ls-op-page-title { font-size: 2rem; color: #102a43; margin: 0 0 8px 0; font-weight: 800; letter-spacing: -0.5px; }
.ls-op-page-subtitle { color: #334e68; font-size: 1.05rem; margin: 0; }

.ls-op-stats-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}
.ls-op-info-card {
  border-radius: 28px;
  overflow: hidden;
  background: #ffffff;
  box-shadow: 0 20px 50px rgba(15, 42, 67, 0.08);
  display: flex;
  flex-direction: column;
  min-height: 420px;
  border: 1px solid transparent;
}
.ls-op-card-media {
  min-height: 180px;
  overflow: hidden;
  background: #f4f7ff;
}
.ls-op-card-media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.ls-op-card-content {
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.ls-op-card-meta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  padding: 8px 12px;
  border-radius: 999px;
  width: fit-content;
}
.ls-op-card-meta::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}
.ls-op-meta--purple {
  color: #c026d3;
  background: rgba(192, 38, 211, 0.08);
}
.ls-op-border--purple {
  border: 1px solid rgba(192, 38, 211, 0.28);
}
.ls-op-card-title {
  margin: 0;
  font-size: 1.2rem;
  line-height: 1.3;
  color: #102a43;
  font-weight: 700;
}
.ls-op-card-description {
  margin: 0;
  color: #486581;
  line-height: 1.75;
  font-size: 0.95rem;
  min-height: 80px;
}
.ls-op-card-footer {
  margin-top: auto;
}
.ls-op-card-value {
  font-size: 3rem;
  color: #102a43;
  line-height: 1;
  font-weight: 800;
}
.ls-op-card-unit {
  display: block;
  color: #64748b;
  font-size: 0.95rem;
  margin-top: 6px;
}

@media (max-width: 768px) {
  .ls-op-stats-grid { grid-template-columns: 1fr; }
}

/* ==========================================================================
   BLINDAGEM DO TEMA ESCURO AUTOMÁTICO (MAPEANDO .ls-op-dark-active)
   ========================================================================== */
.ls-op-page-container.ls-op-dark-active {
  background-color: #000000 !important; /* Fundo 100% Preto */
}

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

/* Blindagem Sólida dos Cards e Conteúdos do Operador no Modo Escuro */
.ls-op-page-container.ls-op-dark-active .ls-op-info-card,
.ls-op-page-container.ls-op-dark-active .ls-op-card-content {
  background-color: #111827 !important;
  border-color: #1f2937 !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-info-card {
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5) !important;
}
.ls-op-page-container.ls-op-dark-active .ls-op-card-media {
  background: #0f172a !important;
}

.ls-op-page-container.ls-op-dark-active .ls-op-card-meta.ls-op-meta--purple {
  color: #ffffff !important;
  background-color: #4c1d95 !important; /* Roxo Sólido Técnico Fundo */
}

/* CORREÇÃO DO EYEBROW: Fundo Verde Sólido como no Painel Adm */
.ls-op-page-container.ls-op-dark-active .eyebrow {
  background-color: #064e3b !important;
  color: #ffffff !important;
  border: 1px solid #059669 !important;
}

/* Forçamento das Fontes para Branco Puro */
.ls-op-page-container.ls-op-dark-active .ls-op-page-title,
.ls-op-page-container.ls-op-dark-active .ls-op-card-title,
.ls-op-page-container.ls-op-dark-active .ls-op-card-value,
.ls-op-page-container.ls-op-dark-active .ls-op-brand-name,
.ls-op-page-container.ls-op-dark-active .ls-op-user-role {
  color: #ffffff !important;
}

/* Textos Secundários e Legendas em Cinza Claro Legível */
.ls-op-page-container.ls-op-dark-active .ls-op-page-subtitle,
.ls-op-page-container.ls-op-dark-active .ls-op-card-description,
.ls-op-page-container.ls-op-dark-active .ls-op-card-unit,
.ls-op-page-container.ls-op-dark-active .ls-op-brand-subtitle {
  color: #cbd5e1 !important;
}

.ls-op-page-container.ls-op-dark-active .ls-op-btn-logout {
  background-color: #1f2937 !important;
  border-color: #374151 !important;
  color: #fca5a5 !important;
}
</style>