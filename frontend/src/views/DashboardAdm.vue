<template>
  <!-- Adicionamos uma classe extra para garantir o preenchimento total -->
  <div class="dashboard-wrapper vh-100">
    <!-- O resto do template permanece igual ao que você enviou -->
    <transition name="slide">
      <aside v-if="isMenuOpen" class="sidebar-drawer" v-click-outside="closeMenu">
        <div class="sidebar-content">
          <div class="drawer-header">
             <img src="@/assets/logo-vaca-ls.png" alt="Logo" class="drawer-logo">
             <span>L.S Management</span>
          </div>
          <nav class="drawer-menu">
            <router-link to="/dashboard-adm" class="nav-link active">Dashboard</router-link>
            <router-link to="/rebanho" class="nav-link">Rebanho</router-link>
            <router-link to="/saude" class="nav-link">Saúde Animal</router-link>
            <router-link to="/relatorios" class="nav-link">Relatórios</router-link>
          </nav>
          <button @click="logout" class="btn-logout">Sair</button>
        </div>
      </aside>
    </transition>

    <main class="main-layout" :class="{ 'blur-bg': isMenuOpen }">
      <header class="top-bar">
        <div class="logo-trigger" @click.stop="toggleMenu">
          <img src="@/assets/logo-vaca-ls.png" alt="Logo" class="mini-logo">
          <span class="logo-text">L.S Management</span>
        </div>
        <div class="user-profile">
          <span class="user-role">Administrador</span>
          <div class="user-avatar"></div>
        </div>
      </header>

      <div class="dashboard-grid">
        <div class="grid-left">
          <section class="card-hero" @click="goToMap">
            <div class="hero-overlay">
              <div class="hero-text">
                <h2>Fazenda Santa Clara</h2>
                <div class="tags">
                  <span class="tag">Solo Saudável</span>
                  <span class="tag">120 Animais Ativos</span>
                </div>
              </div>
            </div>
          </section>

          <section class="glass-card health-card">
            <header>
              <span class="card-title">Saúde</span>
              <span class="card-status">90%</span>
            </header>
            <div class="progress-wrapper">
              <div class="progress-bar"><div class="fill" style="width: 90%"></div></div>
            </div>
            <p class="card-footer">Normal | <strong>5 Alertas →</strong></p>
          </section>
        </div>

        <div class="grid-right">
          <div class="glass-card stat-item">
            <label>Animais</label>
            <h3>120 <small>total</small></h3>
            <span class="sub-link">3 doentes →</span>
          </div>

          <div class="glass-card stat-item">
            <label>Pastagem</label>
            <p>Capacidade: <strong>100</strong></p>
            <p>Uso atual: <strong class="danger">120</strong></p>
          </div>

          <div class="glass-card stat-item production">
            <label>Produção de Leite</label>
            <h3>320 <small>L/dia</small></h3>
            <div class="fake-chart">
               <div class="bar" style="height: 30%"></div>
               <div class="bar" style="height: 50%"></div>
               <div class="bar" style="height: 80%"></div>
               <div class="bar" style="height: 60%"></div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// O Script permanece exatamente o mesmo
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
    document.addEventListener("click", el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener("click", el.clickOutsideEvent);
  },
};
</script>

<style scoped>
/* 1. RESET RADICAL PARA FORÇAR O FUNDO */
.dashboard-wrapper {
  position: fixed; /* Força o componente a ocupar a tela toda independente do body */
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: #f8f9f5 !important; /* Cor de fundo da AgroSmart */
  color: #051a05;
  overflow-y: auto; /* Permite scroll se o conteúdo crescer */
}

.dashboard-wrapper * { 
  box-sizing: border-box; 
  font-family: 'Inter', sans-serif; 
}

/* 2. SIDEBAR DRAWER - Cor Verde Escuro */
.sidebar-drawer {
  position: fixed; 
  left: 0; 
  top: 0; 
  width: 280px; 
  height: 100%;
  background: #051a05; 
  z-index: 1000; 
  padding: 40px 20px;
  box-shadow: 10px 0 30px rgba(0,0,0,0.3);
}

.drawer-header { 
  display: flex; 
  align-items: center; 
  gap: 10px; 
  color: white; 
  margin-bottom: 40px; 
  font-weight: bold; 
}

.drawer-logo { width: 35px; }

.nav-link { 
  display: block; 
  color: #a0aec0; /* Cinza claro para os links inativos */
  text-decoration: none; 
  padding: 15px;
  border-radius: 12px; 
  margin-bottom: 10px; 
  transition: 0.3s;
}

.nav-link.active, .nav-link:hover { 
  background: #46a350; /* Verde principal[cite: 2] */
  color: white; 
}

/* 3. CARDS E TEXTOS */
.logo-text { 
  font-size: 1.2rem; 
  font-weight: 800; 
  color: #051a05; /* Garante que o texto do logo não seja branco no fundo claro */
}

.glass-card {
  background: #ffffff; 
  border-radius: 24px; 
  padding: 25px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.03);
  border: 1px solid #eef0eb; /* Borda sutil para definir o card[cite: 2] */
}

.user-role {
  font-weight: 600;
  color: #051a05;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: #46a350;
  border-radius: 50%;
  margin-left: 10px;
}

/* REAPLICANDO O GRID */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 25px;
  max-width: 1400px;
  margin: 0 auto;
}

/* Estilos de Animação e Layout permanecem iguais[cite: 2] */
.main-layout { padding: 20px 40px; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.logo-trigger { display: flex; align-items: center; gap: 12px; cursor: pointer; }
.mini-logo { width: 40px; }
.card-hero {
  height: 380px;
  background-image: url('@/assets/adm_background.jpg');
  background-size: cover;
  background-position: center;
  border-radius: 30px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
}
.hero-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.7));
  display: flex; align-items: flex-end; padding: 40px;
}
.hero-text h2 { color: white; font-size: 2.2rem; }
.tag { background: rgba(255,255,255,0.2); backdrop-filter: blur(5px); color: white; padding: 6px 15px; border-radius: 20px; font-size: 0.8rem; margin-right: 10px; }
.progress-bar { width: 100%; height: 10px; background: #edf2f7; border-radius: 5px; overflow: hidden; margin-top: 10px; }
.fill { height: 100%; background: #46a350; }
.danger { color: #e53e3e; }
.fake-chart { display: flex; align-items: flex-end; gap: 8px; height: 60px; margin-top: 15px; }
.bar { flex: 1; background: #46a350; border-radius: 4px; opacity: 0.7; }
.slide-enter-active, .slide-leave-active { transition: 0.4s ease; }
.slide-enter-from, .slide-leave-to { transform: translateX(-100%); }
</style>