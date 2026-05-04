<template>
  <div class="dashboard-wrapper op-theme">
    <!-- MENU LATERAL RETRÁTIL -->
    <transition name="slide">
      <aside v-if="isMenuOpen" class="sidebar-drawer" v-click-outside="closeMenu">
        <div class="sidebar-content">
          <div class="drawer-header">
             <img src="@/assets/logo-vaca-ls.png" alt="Logo" class="drawer-logo">
             <span>L.S Operacional</span>
          </div>
          <nav class="drawer-menu">
            <router-link to="/dashboard-op" class="nav-link active">Minhas Tarefas</router-link>
            <router-link to="/rebanho" class="nav-link">Consultar Animal</router-link>
            <router-link to="/pesagem" class="nav-link">Registrar Peso</router-link>
            <router-link to="/vacinacao" class="nav-link">Aplicar Vacinas</router-link>
          </nav>
          <button @click="logout" class="btn-logout">Sair</button>
        </div>
      </aside>
    </transition>

    <!-- ÁREA PRINCIPAL -->
    <main class="main-layout" :class="{ 'blur-bg': isMenuOpen }">
      <header class="top-bar">
        <div class="logo-trigger" @click.stop="toggleMenu">
          <img src="@/assets/logo-vaca-ls.png" alt="Logo" class="mini-logo">
          <span class="logo-text">L.S Management</span>
        </div>
        <div class="user-profile">
          <span class="user-role">Operador de Campo</span>
          <div class="user-avatar op-avatar"></div>
        </div>
      </header>

      <div class="dashboard-grid">
        
        <!-- LADO ESQUERDO: FOCO EM AÇÃO -->
        <div class="grid-left">
          <!-- CARD OPERACIONAL HERO -->
          <section class="card-hero op-hero" @click="goToTasks">
            <div class="hero-overlay">
              <div class="hero-text">
                <h2>Tarefas do Dia</h2>
                <div class="tags">
                  <span class="tag warning">3 Vacinas Pendentes</span>
                  <span class="tag">5 Pesagens Hoje</span>
                </div>
              </div>
            </div>
          </section>

          <!-- CARD DE MANEJO RÁPIDO -->
          <section class="glass-card action-card">
            <header>
              <span class="card-title">Últimos Registros</span>
            </header>
            <div class="activity-list">
              <div class="activity-item">
                <span class="dot green"></span>
                <p>Animal <strong>#042</strong> pesado com 450kg</p>
                <span class="time">10min atrás</span>
              </div>
              <div class="activity-item">
                <span class="dot blue"></span>
                <p>Vacina Febre Aftosa aplicada no Lote B</p>
                <span class="time">1h atrás</span>
              </div>
            </div>
            <button class="btn-primary-op">Novo Registro de Campo</button>
          </section>
        </div>

        <!-- LADO DIREITO: ALERTAS E QUADRANTES -->
        <div class="grid-right">
          <div class="glass-card stat-item alert-card">
            <label>Alertas de Saúde</label>
            <h3 class="danger-text">05 <small>animais</small></h3>
            <p class="desc">Aguardando inspeção no Quadrante 3</p>
          </div>

          <div class="glass-card stat-item">
            <label>Localização (Quadrantes)</label>
            <div class="quadrant-info">
              <p>📍 Setor Norte: <strong>45 animais</strong></p>
              <p>📍 Setor Sul: <strong>75 animais</strong></p>
            </div>
            <span class="sub-link">Ver mapa de pastos →</span>
          </div>

          <div class="glass-card stat-item weather-widget">
            <label>Clima na Fazenda</label>
            <div class="weather-content">
              <span class="temp">28°C</span>
              <p>Céu Limpo - Ideal para manejo externo</p>
            </div>
          </div>
        </div>

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
    document.addEventListener("click", el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener("click", el.clickOutsideEvent);
  },
};
</script>

<style scoped>
/* REUTILIZANDO A BASE DO ADM COM AJUSTES OPERACIONAIS */
.dashboard-wrapper {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background-color: #f4f7f2 !important; /* Tom levemente mais verde/terra */
  overflow-y: auto;
}

.op-hero {
  background-image: url('@/assets/op_background.jpg') !important;
  height: 380px; border-radius: 30px; position: relative; overflow: hidden; cursor: pointer;
}

.btn-primary-op {
  width: 100%; margin-top: 20px; padding: 15px;
  background-color: #46a350; color: white; border: none;
  border-radius: 12px; font-weight: bold; cursor: pointer; transition: 0.3s;
}

.btn-primary-op:hover { background-color: #357a3d; transform: scale(1.02); }

.activity-list { margin-top: 15px; }
.activity-item { display: flex; align-items: center; gap: 10px; padding: 12px 0; border-bottom: 1px solid #eee; font-size: 0.9rem; }
.dot { width: 8px; height: 8px; border-radius: 50%; }
.green { background: #46a350; }
.blue { background: #3182ce; }
.time { margin-left: auto; color: #a0aec0; font-size: 0.8rem; }

.op-avatar { background: #2d3748; } /* Diferenciação de cor no perfil */
.danger-text { color: #e53e3e; }
.tag.warning { background: #ecc94b; color: #744210; }

/* Estilos de Grid e Drawer seguem o padrão do ADM para consistência */
.dashboard-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 25px; max-width: 1400px; margin: 0 auto; }
.glass-card { background: white; border-radius: 24px; padding: 25px; border: 1px solid #eef0eb; }
.sidebar-drawer { position: fixed; left: 0; top: 0; width: 280px; height: 100%; background: #051a05; z-index: 1000; padding: 40px 20px; }
.nav-link { display: block; color: #a0aec0; text-decoration: none; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
.nav-link.active { background: #46a350; color: white; }
.top-bar { padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; }
.logo-trigger { display: flex; align-items: center; gap: 12px; cursor: pointer; }
.mini-logo { width: 40px; }
.hero-overlay { position: absolute; inset: 0; background: linear-gradient(transparent, rgba(0,0,0,0.7)); display: flex; align-items: flex-end; padding: 40px; }
.hero-text h2 { color: white; font-size: 2.2rem; }
.tag { background: rgba(255,255,255,0.2); backdrop-filter: blur(5px); color: white; padding: 6px 15px; border-radius: 20px; font-size: 0.8rem; margin-right: 10px; }
.slide-enter-active, .slide-leave-active { transition: 0.4s ease; }
.slide-enter-from, .slide-leave-to { transform: translateX(-100%); }
</style>