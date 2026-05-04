<template>
  <div class="dashboard-wrapper op-theme">
    <!-- SIDEBAR DRAWER -->
    <transition name="slide">
      <aside v-if="isMenuOpen" class="sidebar-drawer" v-click-outside="closeMenu">
        <div class="sidebar-content">
          <div class="drawer-header">
            <img src="@/assets/logo-vaca-ls.png" alt="Logo" class="drawer-logo">
            <span class="brand-name">L.S Operacional</span>
          </div>
          <nav class="drawer-menu">
            <router-link to="/dashboard-op" class="nav-link active">
              <span class="nav-icon">⊞</span> Minhas Tarefas
            </router-link>
            <router-link to="/rebanho" class="nav-link">
              <span class="nav-icon">◈</span> Consultar Animal
            </router-link>
            <router-link to="/pesagem" class="nav-link">
              <span class="nav-icon">⊡</span> Registrar Peso
            </router-link>
            <router-link to="/vacinacao" class="nav-link">
              <span class="nav-icon">✛</span> Aplicar Vacinas
            </router-link>
          </nav>
          <button @click="logout" class="btn-logout">⏻ Sair</button>
        </div>
      </aside>
    </transition>

    <!-- MAIN CONTENT -->
    <main class="main-layout" :class="{ 'blur-bg': isMenuOpen }">
      <!-- TOP BAR -->
      <header class="top-bar">
        <div class="logo-trigger" @click.stop="toggleMenu">
          <img src="@/assets/logo-vaca-ls.png" alt="Logo" class="mini-logo">
          <span class="logo-text">L.S Management</span>
          <span class="menu-hint">≡</span>
        </div>
        <div class="top-center">
          <div class="search-bar">
            <span class="search-icon">⌕</span>
            <input type="text" placeholder="Buscar animal por brinco, lote..." />
          </div>
        </div>
        <div class="user-profile">
          <div class="notification-bell">
            <span>🔔</span>
            <span class="notif-badge">5</span>
          </div>
          <span class="user-role">Operador de Campo</span>
          <div class="user-avatar op-avatar">
            <span>O</span>
          </div>
        </div>
      </header>

      <!-- DASHBOARD GRID -->
      <div class="dashboard-grid">

        <!-- HERO CARD: TAREFAS DO DIA -->
        <section class="card-hero" @click="goToTasks">
          <div class="hero-scanline"></div>
          <div class="hero-overlay">
            <div class="hero-badge">⊡ OPERACIONAL</div>
            <div class="hero-text">
              <h2>Tarefas do Dia</h2>
              <div class="tags">
                <span class="tag tag-yellow">⚠ 3 Vacinas Pendentes</span>
                <span class="tag">⊡ 5 Pesagens Hoje</span>
              </div>
            </div>
            <div class="hero-corner-stat">
              <span class="corner-label">CONCLUÍDO</span>
              <span class="corner-value op-color">4/9</span>
            </div>
          </div>
        </section>

        <!-- STAT: ALERTAS DE SAÚDE -->
        <div class="stat-card alert-critical">
          <div class="stat-header">
            <span class="stat-icon danger-icon">⚠</span>
            <span class="stat-label">Alertas de Saúde</span>
          </div>
          <div class="stat-main">
            <span class="stat-number danger-text">05</span>
            <span class="stat-unit">animais</span>
          </div>
          <p class="stat-desc">Aguardando inspeção no Quadrante 3</p>
          <div class="pulse-bar"></div>
        </div>

        <!-- STAT: LOCALIZAÇÃO -->
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-icon">⊙</span>
            <span class="stat-label">Quadrantes Ativos</span>
          </div>
          <div class="sector-list">
            <div class="sector-row">
              <span class="sector-dot green"></span>
              <span class="sector-name">Setor Norte</span>
              <span class="sector-count">45</span>
            </div>
            <div class="sector-row">
              <span class="sector-dot blue"></span>
              <span class="sector-name">Setor Sul</span>
              <span class="sector-count">75</span>
            </div>
            <div class="sector-row">
              <span class="sector-dot yellow"></span>
              <span class="sector-name">Setor Leste</span>
              <span class="sector-count">28</span>
            </div>
          </div>
          <span class="sub-link">Ver mapa de pastos →</span>
        </div>

        <!-- ÚLTIMOS REGISTROS -->
        <section class="data-card activity-card">
          <div class="data-header">
            <span class="data-icon">◎</span>
            <span class="data-title">Últimos Registros</span>
            <span class="live-badge">● AO VIVO</span>
          </div>
          <div class="activity-list">
            <div class="activity-item">
              <span class="act-dot green"></span>
              <div class="act-body">
                <p>Animal <strong>#042</strong> pesado</p>
                <span class="act-detail">450 kg registrado com sucesso</span>
              </div>
              <span class="act-time">10 min</span>
            </div>
            <div class="activity-item">
              <span class="act-dot blue"></span>
              <div class="act-body">
                <p>Vacina Febre Aftosa</p>
                <span class="act-detail">Lote B — 12 animais vacinados</span>
              </div>
              <span class="act-time">1 h</span>
            </div>
            <div class="activity-item">
              <span class="act-dot yellow"></span>
              <div class="act-body">
                <p>Animal <strong>#089</strong> — Febre</p>
                <span class="act-detail">Encaminhado para inspeção</span>
              </div>
              <span class="act-time">2 h</span>
            </div>
          </div>
          <button class="btn-primary-op">
            <span>+</span> Novo Registro de Campo
          </button>
        </section>

        <!-- CLIMA -->
        <section class="data-card weather-card">
          <div class="data-header">
            <span class="data-icon">◌</span>
            <span class="data-title">Clima na Fazenda</span>
          </div>
          <div class="weather-main">
            <span class="weather-temp">28°</span>
            <span class="weather-unit">C</span>
          </div>
          <p class="weather-desc">☀ Céu Limpo — Ideal para manejo externo</p>
          <div class="weather-stats">
            <div class="w-stat">
              <span class="w-label">Umidade</span>
              <span class="w-val">62%</span>
            </div>
            <div class="w-stat">
              <span class="w-label">Vento</span>
              <span class="w-val">12 km/h</span>
            </div>
            <div class="w-stat">
              <span class="w-label">UV</span>
              <span class="w-val">Alto</span>
            </div>
          </div>
        </section>

        <!-- PROGRESSO DE TAREFAS -->
        <section class="data-card tasks-progress-card">
          <div class="data-header">
            <span class="data-icon">☑</span>
            <span class="data-title">Progresso do Dia</span>
          </div>
          <div class="task-items">
            <div class="task-row done">
              <span class="task-check">✓</span>
              <span>Pesagem Lote A</span>
            </div>
            <div class="task-row done">
              <span class="task-check">✓</span>
              <span>Vacina Lote B</span>
            </div>
            <div class="task-row pending">
              <span class="task-check pend">○</span>
              <span>Vacinas Pendentes (3)</span>
            </div>
            <div class="task-row pending">
              <span class="task-check pend">○</span>
              <span>Inspeção Quadrante 3</span>
            </div>
          </div>
          <div class="overall-progress">
            <div class="op-bar">
              <div class="op-fill" style="width: 44%"></div>
            </div>
            <span class="op-label">44% concluído</span>
          </div>
        </section>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isMenuOpen = ref(false);

const toggleMenu = () => { isMenuOpen.value = !isMenuOpen.value; };
const closeMenu = () => { isMenuOpen.value = false; };
const goToTasks = () => { router.push('/tarefas'); };
const logout = () => { localStorage.clear(); router.push('/'); };

const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event);
      }
    };
    document.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent);
  },
};
</script>

<style scoped>
/* =====================================================
   DESIGN SYSTEM — DARK TECH OPERACIONAL
   Mesmo sistema visual do ADM, identidade de operador
   ===================================================== */

:root {
  --bg-base:       #0d1117;
  --bg-card:       #161b22;
  --bg-card-hover: #1c2128;
  --bg-sidebar:    #0a0f14;
  --border:        #21262d;
  --border-accent: #30363d;
  --green-neon:    #3fb950;
  --green-dim:     #238636;
  --green-glow:    rgba(63, 185, 80, 0.25);
  --yellow:        #d29922;
  --yellow-glow:   rgba(210, 153, 34, 0.2);
  --red:           #f85149;
  --blue:          #58a6ff;
  --blue-glow:     rgba(88, 166, 255, 0.2);
  --text-primary:  #e6edf3;
  --text-secondary:#8b949e;
  --text-muted:    #484f58;
  --font-mono:     'Courier New', Courier, monospace;
  /* Operador usa azul/amarelo como accent secundário */
  --op-accent:     #58a6ff;
  --op-glow:       rgba(88, 166, 255, 0.25);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard-wrapper {
  width: 100%;
  min-height: 100vh;
  background-color: var(--bg-base);
  background-image:
    radial-gradient(ellipse at 80% 0%, rgba(88,166,255,0.05) 0%, transparent 60%),
    radial-gradient(ellipse at 20% 100%, rgba(63,185,80,0.04) 0%, transparent 60%);
  font-family: 'Segoe UI', system-ui, sans-serif;
  color: var(--text-primary);
  display: flex;
  flex-direction: column;
}

/* ============ SIDEBAR ============ */
.sidebar-drawer {
  position: fixed;
  left: 0; top: 0;
  width: 260px; height: 100%;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-accent);
  z-index: 9999;
  box-shadow: 4px 0 24px rgba(0,0,0,0.6);
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 24px 16px;
}

.drawer-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 8px 24px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 20px;
}

.drawer-logo {
  width: 36px; height: 36px;
  object-fit: contain;
  filter: drop-shadow(0 0 6px var(--op-accent));
}

.brand-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--op-accent);
  letter-spacing: 0.02em;
}

.drawer-menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 11px 14px;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.nav-link:hover {
  background: var(--bg-card);
  color: var(--text-primary);
  border-color: var(--border);
}

.nav-link.active {
  background: rgba(88, 166, 255, 0.1);
  color: var(--op-accent);
  border-color: rgba(88, 166, 255, 0.3);
}

.nav-icon { font-size: 0.85rem; width: 18px; text-align: center; }

.btn-logout {
  margin-top: auto;
  padding: 11px 14px;
  background: transparent;
  border: 1px solid var(--border-accent);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  text-align: left;
}

.btn-logout:hover { border-color: var(--red); color: var(--red); }

/* ============ TOP BAR ============ */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  height: 60px;
  background: var(--bg-sidebar);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.logo-trigger {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  min-width: 180px;
}

.mini-logo {
  width: 32px; height: 32px;
  object-fit: contain;
  filter: drop-shadow(0 0 4px var(--op-accent));
}

.logo-text { font-size: 0.9rem; font-weight: 600; color: var(--text-primary); }
.menu-hint { font-size: 1.2rem; color: var(--text-muted); margin-left: 4px; }

.top-center { flex: 1; max-width: 480px; margin: 0 24px; }

.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--bg-card);
  border: 1px solid var(--border-accent);
  border-radius: 8px;
  padding: 8px 14px;
  transition: border-color 0.2s;
}

.search-bar:focus-within {
  border-color: var(--op-accent);
  box-shadow: 0 0 0 3px var(--op-glow);
}

.search-icon { color: var(--text-muted); }

.search-bar input {
  background: none;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 0.88rem;
  width: 100%;
}

.search-bar input::placeholder { color: var(--text-muted); }

.user-profile { display: flex; align-items: center; gap: 14px; }

.notification-bell { position: relative; cursor: pointer; font-size: 1.1rem; }

.notif-badge {
  position: absolute;
  top: -4px; right: -6px;
  background: var(--yellow);
  color: #0d1117;
  font-size: 0.6rem;
  font-weight: bold;
  width: 16px; height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-role { font-size: 0.82rem; color: var(--text-secondary); }

.user-avatar {
  width: 34px; height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1c4a7a, var(--op-accent));
  display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem; font-weight: bold;
  color: #0d1117;
  border: 2px solid var(--op-accent);
  box-shadow: 0 0 8px var(--op-glow);
}

/* ============ LAYOUT ============ */
.main-layout {
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease; /* Transição suave quando o menu abre */
  padding-left: 0; /* Padrão quando menu está fechado */
}

.main-layout.blur-bg {
  filter: blur(3px);
  padding-left: 280px; /* Mesma largura da sidebar + respiro */
  pointer-events: none;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 20px;
  padding: 30px;
  max-width: 1200px; 
  margin: 0 auto;
  width: 100%;
}

@media (max-width: 1100px) {
  .dashboard-grid {
    grid-template-columns: 1fr 1fr;
    max-width: 900px;
  }
  .card-hero { grid-column: 1 / -1; } /* Hero ocupa a largura toda */
}
/* ============ HERO ============ */
.card-hero {
  grid-column: 1 / -1;
  grid-row: 1 / 2;
  height: 260px;
  border-radius: 12px;
  background-image: url('@/assets/op_background.jpg');
  background-size: cover;
  background-position: center;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid var(--border-accent);
  transition: border-color 0.3s;
}

.card-hero:hover { border-color: var(--op-accent); }

.hero-scanline {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.04) 2px,
    rgba(0,0,0,0.04) 4px
  );
  pointer-events: none;
  z-index: 1;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(13,17,23,0.3) 0%, rgba(13,17,23,0.75) 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px 24px;
  z-index: 2;
}

.hero-badge {
  align-self: flex-start;
  background: rgba(88, 166, 255, 0.2);
  border: 1px solid var(--op-accent);
  color: var(--op-accent);
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 4px;
  letter-spacing: 0.08em;
  font-family: var(--font-mono);
}

.hero-text h2 {
  font-size: 1.9rem;
  font-weight: 700;
  color: var(--text-primary);
  text-shadow: 0 2px 8px rgba(0,0,0,0.6);
  margin-bottom: 10px;
}

.tags { display: flex; gap: 8px; flex-wrap: wrap; }

.tag {
  background: rgba(255,255,255,0.12);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255,255,255,0.2);
  color: white;
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 500;
}

.tag-yellow {
  background: rgba(210, 153, 34, 0.2);
  border-color: var(--yellow);
  color: var(--yellow);
}

.hero-corner-stat {
  position: absolute;
  top: 20px; right: 20px;
  text-align: right;
}

.corner-label {
  display: block;
  font-size: 0.65rem;
  color: var(--text-secondary);
  font-family: var(--font-mono);
  letter-spacing: 0.1em;
}

.corner-value {
  display: block;
  font-size: 1.3rem;
  font-weight: 700;
  font-family: var(--font-mono);
}

.op-color { color: var(--op-accent); }

/* ============ STAT CARDS ============ */
.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s;
}

.stat-card:hover {
  border-color: var(--border-accent);
  background: var(--bg-card-hover);
}

.alert-critical { border-color: rgba(248, 81, 73, 0.3); }

.stat-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
}

.stat-icon { color: var(--op-accent); font-size: 1.1rem; }
.danger-icon { color: var(--red) !important; }

.stat-label {
  font-size: 0.82rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
}

.stat-main {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 8px;
}

.stat-number {
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  font-family: var(--font-mono);
}

.danger-text { color: var(--red) !important; }

.stat-unit { font-size: 0.85rem; color: var(--text-muted); }
.stat-desc { font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 12px; }

.pulse-bar {
  height: 3px;
  background: linear-gradient(90deg, var(--red) 0%, transparent 100%);
  border-radius: 2px;
  animation: pulse-anim 2s ease-in-out infinite;
}

@keyframes pulse-anim {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* Sectors */
.sector-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 14px; }

.sector-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
}

.sector-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.sector-dot.green { background: var(--green-neon); box-shadow: 0 0 5px var(--green-neon); }
.sector-dot.blue { background: var(--op-accent); box-shadow: 0 0 5px var(--op-accent); }
.sector-dot.yellow { background: var(--yellow); box-shadow: 0 0 5px var(--yellow); }

.sector-name { flex: 1; color: var(--text-secondary); }

.sector-count {
  font-weight: 700;
  color: var(--text-primary);
  font-family: var(--font-mono);
}

.sub-link {
  font-size: 0.8rem;
  color: var(--op-accent);
  cursor: pointer;
  display: block;
  margin-top: 4px;
}

/* ============ DATA CARDS ============ */
.data-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s;
}

.data-card:hover {
  border-color: var(--border-accent);
  background: var(--bg-card-hover);
}

.data-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.data-icon { font-size: 1rem; color: var(--op-accent); }

.data-title {
  font-size: 0.82rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
  flex: 1;
}

.live-badge {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(63, 185, 80, 0.1);
  border: 1px solid var(--green-dim);
  color: var(--green-neon);
  font-family: var(--font-mono);
  letter-spacing: 0.05em;
  animation: live-pulse 2s ease-in-out infinite;
}

@keyframes live-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

/* Activity card */
.activity-card { grid-column: 1 / 2; grid-row: 2 / 3; }

.activity-list { display: flex; flex-direction: column; gap: 12px; margin-bottom: 16px; }

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}

.activity-item:last-child { border-bottom: none; padding-bottom: 0; }

.act-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  margin-top: 5px;
  flex-shrink: 0;
}

.act-dot.green { background: var(--green-neon); box-shadow: 0 0 5px var(--green-neon); }
.act-dot.blue { background: var(--op-accent); box-shadow: 0 0 5px var(--op-accent); }
.act-dot.yellow { background: var(--yellow); box-shadow: 0 0 5px var(--yellow); }

.act-body { flex: 1; }
.act-body p { font-size: 0.88rem; color: var(--text-primary); margin-bottom: 2px; }
.act-body strong { color: var(--op-accent); }
.act-detail { font-size: 0.78rem; color: var(--text-secondary); }
.act-time { font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono); white-space: nowrap; }

.btn-primary-op {
  width: 100%;
  padding: 12px;
  background: rgba(88, 166, 255, 0.1);
  border: 1px solid var(--op-accent);
  border-radius: 8px;
  color: var(--op-accent);
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary-op:hover {
  background: rgba(88, 166, 255, 0.2);
  box-shadow: 0 0 12px var(--op-glow);
}

/* Weather card */
.weather-card { grid-column: 2 / 3; grid-row: 2 / 3; }

.weather-main { display: flex; align-items: flex-start; gap: 2px; margin-bottom: 6px; }

.weather-temp {
  font-size: 3.5rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  font-family: var(--font-mono);
}

.weather-unit {
  font-size: 1.5rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
  margin-top: 8px;
}

.weather-desc { font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 16px; }

.weather-stats { display: flex; gap: 12px; }

.w-stat { flex: 1; text-align: center; }
.w-label { display: block; font-size: 0.7rem; color: var(--text-muted); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em; }
.w-val { font-size: 0.9rem; font-weight: 700; color: var(--text-primary); font-family: var(--font-mono); }


.tasks-progress-card { grid-column: 3 / 4; grid-row: 2 / 3; }

.task-items { display: flex; flex-direction: column; gap: 10px; margin-bottom: 16px; }

.task-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.85rem;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid transparent;
}

.task-row.done {
  background: rgba(63, 185, 80, 0.06);
  border-color: rgba(63, 185, 80, 0.15);
  color: var(--text-secondary);
}

.task-row.pending {
  background: rgba(210, 153, 34, 0.06);
  border-color: rgba(210, 153, 34, 0.15);
  color: var(--text-primary);
}

.task-check {
  font-size: 0.9rem;
  color: var(--green-neon);
  font-weight: bold;
}

.task-check.pend { color: var(--yellow); }

.overall-progress { margin-top: 4px; }

.op-bar {
  height: 4px;
  background: var(--border-accent);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 6px;
}

.op-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--green-dim), var(--green-neon));
  border-radius: 2px;
  box-shadow: 0 0 6px var(--green-glow);
}

.op-label { font-size: 0.78rem; color: var(--text-muted); font-family: var(--font-mono); }

/* ============ TRANSITIONS ============ */
.slide-enter-active, .slide-leave-active { transition: transform 0.3s ease; }
.slide-enter-from, .slide-leave-to { transform: translateX(-100%); }
</style>