<template>
  <div class="dashboard-wrapper">
    <!-- SIDEBAR DRAWER -->
    <transition name="slide">
      <aside v-if="isMenuOpen" class="sidebar-drawer" v-click-outside="closeMenu">
        <div class="sidebar-content">
          <div class="drawer-header">
            <img src="@/assets/logo-vaca-ls.png" alt="Logo" class="drawer-logo">
            <span class="brand-name">L.S Management</span>
          </div>
          <nav class="drawer-menu">
            <router-link to="/dashboard-adm" class="nav-link active">
              <span class="nav-icon">⊞</span> Dashboard
            </router-link>
            <router-link to="/rebanho" class="nav-link">
              <span class="nav-icon">◈</span> Rebanho
            </router-link>
            <router-link to="/saude" class="nav-link">
              <span class="nav-icon">♥</span> Saúde Animal
            </router-link>
            <router-link to="/relatorios" class="nav-link">
              <span class="nav-icon">≡</span> Relatórios
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
            <input type="text" placeholder="Buscar animais, lotes, alertas..." />
          </div>
        </div>
        <div class="user-profile">
          <div class="notification-bell">
            <span>🔔</span>
            <span class="notif-badge">3</span>
          </div>
          <span class="user-role">Administrador</span>
          <div class="user-avatar">
            <span>A</span>
          </div>
        </div>
      </header>

      <!-- DASHBOARD GRID -->
      <div class="dashboard-grid">

        <!-- HERO CARD -->
        <section class="card-hero" @click="goToMap">
          <div class="hero-scanline"></div>
          <div class="hero-overlay">
            <div class="hero-badge">● LIVE</div>
            <div class="hero-text">
              <h2>Fazenda Santa Clara</h2>
              <div class="tags">
                <span class="tag tag-green">✓ Solo Saudável</span>
                <span class="tag">◈ 120 Animais Ativos</span>
              </div>
            </div>
            <div class="hero-corner-stat">
              <span class="corner-label">UPTIME</span>
              <span class="corner-value">99.8%</span>
            </div>
          </div>
        </section>

        <!-- STAT: ANIMAIS -->
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-icon">◈</span>
            <span class="stat-label">Animais</span>
          </div>
          <div class="stat-main">
            <span class="stat-number">120</span>
            <span class="stat-unit">total</span>
          </div>
          <div class="stat-alert">
            <span class="alert-dot red"></span>
            <span>5 doentes</span>
            <span class="arrow">→</span>
          </div>
        </div>

        <!-- STAT: PASTAGEM -->
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-icon">◉</span>
            <span class="stat-label">Pastagem</span>
          </div>
          <div class="stat-row">
            <span class="row-label">Capacidade:</span>
            <span class="row-value">100</span>
          </div>
          <div class="stat-row warning">
            <span class="row-label">Uso atual:</span>
            <span class="row-value danger">120</span>
            <span class="warn-icon">⚠</span>
          </div>
          <div class="capacity-bar">
            <div class="capacity-fill over"></div>
          </div>
        </div>

        <!-- SAUDE CARD -->
        <section class="data-card health-card">
          <div class="data-header">
            <span class="data-icon">♥</span>
            <span class="data-title">Saúde</span>
            <span class="data-badge ok">NORMAL</span>
          </div>
          <div class="health-percent">
            <span class="big-number">90</span><span class="big-unit">%</span>
          </div>
          <div class="progress-track">
            <div class="progress-fill health" style="width: 90%">
              <div class="progress-glow"></div>
            </div>
          </div>
          <div class="data-footer">
            <span class="alert-dot red"></span>
            <span>5 Alertas</span>
            <span class="arrow">→</span>
          </div>
        </section>

        <!-- ALERTAS CARD -->
        <section class="data-card alerts-card">
          <div class="data-header">
            <span class="data-icon warn-icon-y">⚠</span>
            <span class="data-title">Alertas</span>
          </div>
          <div class="alerts-count">
            <span class="big-number">03</span>
            <span class="big-unit">ativos</span>
          </div>
          <ul class="alert-list">
            <li><span class="alert-dot red"></span> Animal com febre</li>
            <li><span class="alert-dot yellow"></span> Excesso de lotação na pastagem</li>
            <li><span class="alert-dot yellow"></span> Vacina pendente - Lote C</li>
          </ul>
        </section>

        <!-- PRODUCAO CARD -->
        <section class="data-card production-card">
          <div class="data-header">
            <span class="data-icon">▦</span>
            <span class="data-title">Produção</span>
          </div>
          <div class="prod-row">
            <span class="prod-label">Leite:</span>
            <span class="prod-value">320 <small>L/dia</small></span>
          </div>
          <div class="prod-row">
            <span class="prod-label">Peso médio:</span>
            <span class="prod-value">450 <small>kg</small></span>
          </div>
          <div class="mini-chart">
            <div class="bar" style="--h: 35%"></div>
            <div class="bar" style="--h: 50%"></div>
            <div class="bar" style="--h: 45%"></div>
            <div class="bar" style="--h: 70%"></div>
            <div class="bar" style="--h: 60%"></div>
            <div class="bar" style="--h: 80%"></div>
            <div class="bar" style="--h: 75%"></div>
            <div class="bar active" style="--h: 90%"></div>
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
const goToMap = () => { router.push('/mapa-completo'); };
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
   DESIGN SYSTEM — DARK TECH / AGRO MONITOR
   Inspired by industrial monitoring dashboards
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
  --red:           #f85149;
  --blue:          #58a6ff;
  --text-primary:  #e6edf3;
  --text-secondary:#8b949e;
  --text-muted:    #484f58;
  --font-mono:     'Courier New', Courier, monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard-wrapper {
  width: 100%;
  min-height: 100vh;
  background-color: var(--bg-base);
  background-image:
    radial-gradient(ellipse at 20% 0%, rgba(63,185,80,0.05) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 100%, rgba(88,166,255,0.04) 0%, transparent 60%);
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
  padding: 0;
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
  filter: drop-shadow(0 0 6px var(--green-neon));
}

.brand-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--green-neon);
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
  background: rgba(63, 185, 80, 0.1);
  color: var(--green-neon);
  border-color: rgba(63, 185, 80, 0.3);
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

.btn-logout:hover {
  border-color: var(--red);
  color: var(--red);
}

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
  filter: drop-shadow(0 0 4px var(--green-neon));
}

.logo-text {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
}

.menu-hint {
  font-size: 1.2rem;
  color: var(--text-muted);
  margin-left: 4px;
}

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
  border-color: var(--green-neon);
  box-shadow: 0 0 0 3px var(--green-glow);
}

.search-icon { color: var(--text-muted); font-size: 1rem; }

.search-bar input {
  background: none;
  border: none;
  outline: none;
  color: var(--text-primary);
  font-size: 0.88rem;
  width: 100%;
}

.search-bar input::placeholder { color: var(--text-muted); }

.user-profile {
  display: flex;
  align-items: center;
  gap: 14px;
}

.notification-bell {
  position: relative;
  cursor: pointer;
  font-size: 1.1rem;
}

.notif-badge {
  position: absolute;
  top: -4px; right: -6px;
  background: var(--red);
  color: white;
  font-size: 0.6rem;
  font-weight: bold;
  width: 16px; height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-role {
  font-size: 0.82rem;
  color: var(--text-secondary);
}

.user-avatar {
  width: 34px; height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--green-dim), var(--green-neon));
  display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem; font-weight: bold;
  color: #0d1117;
  border: 2px solid var(--green-neon);
  box-shadow: 0 0 8px var(--green-glow);
}

/* ============ GRID ============ */
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

/* ============ HERO CARD ============ */
.card-hero {
  grid-column: 1 / 2;
  grid-row: 1 / 2;
  height: 260px;
  border-radius: 12px;
  background-image: url('@/assets/adm_background.jpg');
  background-size: cover;
  background-position: center;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid var(--border-accent);
  transition: border-color 0.3s;
}

.card-hero:hover { border-color: var(--green-neon); }

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
  background: linear-gradient(
    135deg,
    rgba(13,17,23,0.3) 0%,
    rgba(13,17,23,0.75) 100%
  );
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px 24px;
  z-index: 2;
}

.hero-badge {
  align-self: flex-start;
  background: rgba(63, 185, 80, 0.2);
  border: 1px solid var(--green-neon);
  color: var(--green-neon);
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

.tag-green {
  background: rgba(63, 185, 80, 0.2);
  border-color: var(--green-neon);
  color: var(--green-neon);
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
  color: var(--green-neon);
  font-family: var(--font-mono);
}

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

.stat-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
}

.stat-icon {
  color: var(--green-neon);
  font-size: 1.1rem;
}

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
  margin-bottom: 12px;
}

.stat-number {
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  font-family: var(--font-mono);
}

.stat-unit {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.stat-alert {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.82rem;
  color: var(--text-secondary);
}

.alert-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}

.alert-dot.red { background: var(--red); box-shadow: 0 0 5px var(--red); }
.alert-dot.yellow { background: var(--yellow); box-shadow: 0 0 5px var(--yellow); }
.alert-dot.green { background: var(--green-neon); box-shadow: 0 0 5px var(--green-neon); }

.arrow { color: var(--green-neon); margin-left: auto; }

.stat-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.88rem;
}

.stat-row:last-of-type { border-bottom: none; }

.row-label { color: var(--text-secondary); flex: 1; }
.row-value { font-weight: 700; color: var(--text-primary); font-family: var(--font-mono); }
.row-value.danger { color: var(--red); }

.warn-icon { color: var(--yellow); font-size: 0.9rem; }

.capacity-bar {
  margin-top: 12px;
  height: 4px;
  background: var(--border-accent);
  border-radius: 2px;
  overflow: hidden;
}

.capacity-fill {
  height: 100%;
  width: 100%;
  background: var(--red);
  box-shadow: 0 0 6px var(--red);
}

/* ============ DATA CARDS (bottom row) ============ */
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

.data-icon {
  font-size: 1rem;
  color: var(--green-neon);
}

.warn-icon-y { color: var(--yellow) !important; }

.data-title {
  font-size: 0.82rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
  flex: 1;
}

.data-badge {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  font-family: var(--font-mono);
  letter-spacing: 0.05em;
}

.data-badge.ok {
  background: rgba(63, 185, 80, 0.1);
  border: 1px solid var(--green-dim);
  color: var(--green-neon);
}

.health-percent {
  display: flex;
  align-items: baseline;
  gap: 2px;
  margin-bottom: 14px;
}

.big-number {
  font-size: 2.8rem;
  font-weight: 700;
  color: var(--text-primary);
  font-family: var(--font-mono);
  line-height: 1;
}

.big-unit {
  font-size: 1.2rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
}

.progress-track {
  height: 5px;
  background: var(--border-accent);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 14px;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  position: relative;
}

.progress-fill.health {
  background: linear-gradient(90deg, var(--green-dim), var(--green-neon));
  box-shadow: 0 0 8px var(--green-glow);
}

.data-footer {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.82rem;
  color: var(--text-secondary);
}

/* Health card spans full width at bottom-left */
.health-card {
  grid-column: 1 / 2;
  grid-row: 2 / 3;
}

.alerts-card { grid-column: 2 / 3; grid-row: 2 / 3; }
.production-card { grid-column: 3 / 4; grid-row: 2 / 3; }

.alerts-count {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 14px;
}

.alert-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.alert-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.84rem;
  color: var(--text-secondary);
}

/* Production */
.prod-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
}

.prod-row:last-of-type { border-bottom: none; }
.prod-label { font-size: 0.82rem; color: var(--text-secondary); }

.prod-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  font-family: var(--font-mono);
}

.prod-value small {
  font-size: 0.75rem;
  color: var(--text-muted);
  font-weight: 400;
  font-family: inherit;
}

.mini-chart {
  display: flex;
  align-items: flex-end;
  gap: 4px;
  height: 50px;
  margin-top: 14px;
  padding-top: 4px;
}

.bar {
  flex: 1;
  height: var(--h);
  background: var(--border-accent);
  border-radius: 3px 3px 0 0;
  transition: background 0.2s;
}

.bar.active {
  background: var(--green-neon);
  box-shadow: 0 0 6px var(--green-glow);
}

/* ============ TRANSITIONS ============ */
.slide-enter-active, .slide-leave-active { transition: transform 0.3s ease; }
.slide-enter-from, .slide-leave-to { transform: translateX(-100%); }
</style>