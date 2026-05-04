<template>
  <div class="dashboard-layout">
    <!-- BARRA LATERAL -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <img src="@/assets/logo-vaca-ls.png" alt="Logo">
        <span>L.S Management</span>
      </div>
      
      <nav class="menu">
        <router-link to="/dashboard" class="menu-item">
          <i class="icon-dash"></i> Home
        </router-link>
        <router-link to="/animais" class="menu-item">
          <i class="icon-cow"></i> Rebanho
        </router-link>
        <router-link to="/manejo" class="menu-item">
          <i class="icon-health"></i> Manejo Sanitário
        </router-link>
        <!-- Item exclusivo do ADM -->
        <router-link v-if="userRole === 'adm'" to="/relatorios" class="menu-item">
          <i class="icon-chart"></i> Relatórios Financeiros
        </router-link>
      </nav>

      <button @click="logout" class="logout-btn">Sair</button>
    </aside>

    <!-- ÁREA PRINCIPAL -->
    <main class="main-container">
      <header class="top-header">
        <h3>Dashboard {{ userRole.toUpperCase() }}</h3>
        <div class="user-info">
          <span>Olá, {{ userRole === 'adm' ? 'Administrador' : 'Operador' }}</span>
        </div>
      </header>

      <section class="dashboard-content">
        <!-- Aqui vamos inserir os cards de resumo -->
        <div class="stats-grid">
          <div class="stat-card">
            <h4>Total de Animais</h4>
            <p class="number">142</p>
          </div>
          <div class="stat-card">
            <h4>Ganho de Peso Médio</h4>
            <p class="number">0.8 kg/dia</p>
          </div>
          <div class="stat-card" :class="{ 'alert': userRole === 'op' }">
            <h4>Pendências de Saúde</h4>
            <p class="number">5</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const userRole = ref('');

onMounted(() => {
  // Recupera o papel que salvamos no Login
  userRole.ref = localStorage.getItem('user_role') || 'visitante';
});

const logout = () => {
  localStorage.clear();
  router.push('/');
};
</script>

<style scoped>
.dashboard-layout { display: flex; height: 100vh; background: #f4f7f6; }

.sidebar {
  width: 260px;
  background: #051a05;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.sidebar-header { display: flex; align-items: center; gap: 10px; margin-bottom: 40px; }
.sidebar-header img { width: 40px; }

.menu { flex: 1; }
.menu-item {
  display: block;
  padding: 15px;
  color: #a0aec0;
  text-decoration: none;
  border-radius: 8px;
  margin-bottom: 5px;
}
.menu-item:hover, .router-link-active {
  background: #46a350;
  color: white;
}

.main-container { flex: 1; display: flex; flex-direction: column; }
.top-header {
  background: white;
  padding: 20px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 40px;
}

.stat-card {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
  border-left: 5px solid #46a350;
}

.number { font-size: 2rem; font-weight: bold; color: #2d3748; margin-top: 10px; }
.alert { border-left-color: #e53e3e; }
.logout-btn { background: none; border: 1px solid #ff4d4d; color: #ff4d4d; padding: 10px; border-radius: 5px; cursor: pointer; }
</style>