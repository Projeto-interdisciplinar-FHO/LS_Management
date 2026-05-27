<template>
  <div class="dashboard-wrapper">
    <transition name="slide">
      <aside v-if="isMenuOpen" class="sidebar-drawer">
        <div class="sidebar-content">
          <div class="drawer-header">
            <img src="@/assets/logo-vaca-ls.png" alt="Logo" class="drawer-logo">
            <span class="brand-name">L.S Management</span>
          </div>
          
          <nav class="drawer-menu">
            <router-link to="/dashboard-adm" class="nav-link active">
              <span class="nav-icon">⊞</span> Início
            </router-link>

            <div class="menu-category">Cadastros Base</div>
            <router-link to="/estabulos" class="nav-link">
              <span class="nav-icon">☖</span> Estábulos
            </router-link>
            <a href="#" @click.prevent="openSpecieModal" class="nav-link">
              <span class="nav-icon">🧬</span> Espécies
            </a>
            <a href="#" @click.prevent="openBreedModal" class="nav-link">
              <span class="nav-icon">🏷️</span> Raças
            </a>

            <div class="menu-category">Operacional</div>
            <router-link to="/animais" class="nav-link">
              <span class="nav-icon">◈</span> Animais
            </router-link>
            <router-link to="/lancamento-leite" class="nav-link">
              <span class="nav-icon">🥛</span> Produção de Leite
            </router-link>
            <router-link to="/vacinacao" class="nav-link">
              <span class="nav-icon">✛</span> Vacinação
            </router-link>
            
            <div class="menu-divider"></div>
            
            <router-link to="/relatorios" class="nav-link">
              <span class="nav-icon">≡</span> Relatórios
            </router-link>
            <router-link to="/assistente-ia" class="nav-link gemini-link">
              <span class="nav-icon">✨</span> Assistente IA
            </router-link>
          </nav>
          
          <button @click="logout" class="btn-logout">⏻ Sair do Sistema</button>
        </div>
      </aside>
    </transition>

    <main class="main-layout" :class="{ 'blur-bg': isMenuOpen }">
      <header class="top-bar">
        <button @click="toggleMenu" class="btn-menu">☰</button>
        <div class="user-info">
          <span class="user-role">Administrador Geral</span>
          <div class="avatar">AD</div>
        </div>
      </header>

      <div class="dashboard-content">
        <div class="welcome-section">
          <h1>Visão Geral da Fazenda</h1>
          <p>Acompanhe e gerencie as principais métricas do rebanho.</p>
        </div>

        <section class="main-highlight-card">
          <div class="highlight-info">
            <h2>Gestão de Estábulos</h2>
            <p>Acesse a lista completa de estábulos para visualizar ocupação, movimentar lotes, editar ou remover animais específicos de cada setor.</p>
            <button @click="$router.push('/estabulos')" class="btn-primary">
              Acessar Estábulos →
            </button>
          </div>
          <div class="highlight-icon">☖</div>
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

    <div v-if="showSpecieModal" class="modal-overlay" @click.self="showSpecieModal = false">
      <div class="modal-content">
        <header class="modal-header">
          <h2>Cadastrar Nova Espécie</h2>
          <button @click="showSpecieModal = false" class="btn-close">✕</button>
        </header>
        <form @submit.prevent="submitSpecie" class="modal-form">
          <div class="input-group">
            <label>Nome da Espécie</label>
            <input v-model="specieForm.name" type="text" placeholder="Ex: Bovino" required>
          </div>
          <button type="submit" class="btn-primary mt-4" :disabled="loading">
            {{ loading ? 'Salvando...' : 'Salvar Espécie' }}
          </button>
        </form>
      </div>
    </div>

    <div v-if="showBreedModal" class="modal-overlay" @click.self="showBreedModal = false">
      <div class="modal-content">
        <header class="modal-header">
          <h2>Cadastrar Nova Raça</h2>
          <button @click="showBreedModal = false" class="btn-close">✕</button>
        </header>
        <form @submit.prevent="submitBreed" class="modal-form">
          <div class="input-group">
            <label>Nome da Raça</label>
            <input v-model="breedForm.name" type="text" placeholder="Ex: Nelore" required>
          </div>
          <div class="input-group mt-3">
            <label>Pertence a qual Espécie?</label>
            <select v-model="breedForm.specie" required>
              <option value="" disabled>Selecione uma espécie...</option>
              <option v-for="specie in speciesList" :key="specie.id" :value="specie.id">
                {{ specie.name }}
              </option>
            </select>
          </div>
          <button type="submit" class="btn-primary mt-4" :disabled="loading">
            {{ loading ? 'Salvando...' : 'Salvar Raça' }}
          </button>
        </form>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const router = useRouter();
const isMenuOpen = ref(true);

const toggleMenu = () => { isMenuOpen.value = !isMenuOpen.value; };
const logout = () => {
  localStorage.clear();
  router.push('/login');
};

// ==========================================
// LÓGICA DOS MODAIS DE CADASTRO BASE
// ==========================================
const showSpecieModal = ref(false);
const showBreedModal = ref(false);
const loading = ref(false);

const specieForm = ref({ name: '' });
const breedForm = ref({ name: '', specie: '' });
const speciesList = ref([]);

// Abre modal de espécie
const openSpecieModal = () => {
  specieForm.value.name = '';
  showSpecieModal.value = true;
};

// Abre modal de raça e busca espécies no backend
const openBreedModal = async () => {
  breedForm.value = { name: '', specie: '' };
  try {
    const res = await api.get('species/');
    speciesList.value = res.data.results || res.data;
  } catch (error) {
    console.error("Erro ao buscar espécies", error);
    // Fallback caso a API ainda não esteja rodando perfeitamente
    speciesList.value = [{ id: 1, name: 'Bovino' }];
  }
  showBreedModal.value = true;
};

// Envia cadastro de espécie
const submitSpecie = async () => {
  loading.value = true;
  try {
    await api.post('species/', specieForm.value);
    alert("Espécie cadastrada com sucesso!");
    showSpecieModal.value = false;
  } catch (error) {
    console.error(error);
    alert("Erro ao cadastrar espécie.");
  } finally {
    loading.value = false;
  }
};

// Envia cadastro de raça
const submitBreed = async () => {
  loading.value = true;
  try {
    await api.post('breeds/', breedForm.value);
    alert("Raça cadastrada com sucesso!");
    showBreedModal.value = false;
  } catch (error) {
    console.error(error);
    alert("Erro ao cadastrar raça.");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.dashboard-wrapper { display: flex; height: 100vh; background-color: #f8fafc; color: #0f172a; font-family: 'Inter', sans-serif; overflow: hidden; }

/* SIDEBAR */
.sidebar-drawer { width: 260px; background: #ffffff; border-right: 1px solid #e2e8f0; display: flex; flex-direction: column; z-index: 100; }
.sidebar-content { display: flex; flex-direction: column; height: 100%; }
.drawer-header { display: flex; align-items: center; gap: 12px; padding: 24px 20px; border-bottom: 1px solid #e2e8f0; }
.drawer-logo { width: 40px; height: auto; }
.brand-name { font-size: 1.1rem; font-weight: 700; color: #0f172a; }

.drawer-menu { display: flex; flex-direction: column; padding: 20px 12px; flex: 1; gap: 4px; overflow-y: auto; }
.menu-category { font-size: 0.75rem; text-transform: uppercase; color: #94a3b8; font-weight: 700; margin: 16px 0 8px 12px; letter-spacing: 0.5px; }

.nav-link { display: flex; align-items: center; gap: 12px; padding: 10px 16px; text-decoration: none; color: #64748b; border-radius: 8px; transition: 0.2s; font-weight: 500; font-size: 0.95rem; cursor: pointer; }
.nav-link:hover, .nav-link.active { background: #f0fdf4; color: #16a34a; }
.nav-icon { font-size: 1.2rem; width: 24px; text-align: center; }
.menu-divider { height: 1px; background: #e2e8f0; margin: 12px 0; }
.gemini-link { color: #8b5cf6; }
.gemini-link:hover { background: #f5f3ff; color: #7c3aed; }
.btn-logout { margin: 20px; padding: 12px; background: transparent; border: 1px solid #e2e8f0; color: #ef4444; border-radius: 8px; cursor: pointer; transition: 0.2s; font-weight: 600; }
.btn-logout:hover { background: #fef2f2; border-color: #fca5a5; }

/* TOP BAR */
.main-layout { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }
.top-bar { display: flex; justify-content: space-between; align-items: center; padding: 16px 32px; background: #ffffff; border-bottom: 1px solid #e2e8f0; }
.btn-menu { background: transparent; border: none; font-size: 1.5rem; cursor: pointer; color: #0f172a; }
.user-info { display: flex; align-items: center; gap: 12px; }
.user-role { color: #64748b; font-size: 0.9rem; font-weight: 500; }
.avatar { width: 36px; height: 36px; border-radius: 50%; background: #16a34a; color: #ffffff; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 0.9rem; }

/* CONTENT */
.dashboard-content { padding: 40px; max-width: 1200px; margin: 0 auto; width: 100%; box-sizing: border-box; }
.welcome-section { margin-bottom: 32px; }
.welcome-section h1 { font-size: 2rem; color: #0f172a; margin-bottom: 8px; font-weight: 700; }
.welcome-section p { color: #64748b; font-size: 1.05rem; }

/* MAIN HIGHLIGHT CARD */
.main-highlight-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
.highlight-info h2 { font-size: 1.5rem; color: #0f172a; margin-bottom: 12px; }
.highlight-info p { color: #64748b; line-height: 1.6; margin-bottom: 24px; max-width: 600px; }
.btn-primary { background: #16a34a; color: #ffffff; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 1rem; cursor: pointer; transition: 0.2s; width: 100%; }
.btn-primary:hover:not(:disabled) { background: #15803d; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.highlight-icon { font-size: 5rem; color: #f0fdf4; text-shadow: 0 0 20px #16a34a; opacity: 0.8; }

/* SECONDARY CARDS */
.section-title { font-size: 1.1rem; color: #0f172a; margin-bottom: 16px; font-weight: 600; }
.secondary-cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }
.action-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; display: flex; align-items: center; gap: 20px; cursor: pointer; transition: all 0.2s ease; }
.action-card:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); border-color: #16a34a; }
.action-card .card-icon { font-size: 2rem; color: #16a34a; background: #f0fdf4; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; border-radius: 12px; }
.card-text h4 { font-size: 1.1rem; color: #0f172a; margin-bottom: 4px; }
.card-text p { font-size: 0.9rem; color: #64748b; }

/* =========================================
   ESTILOS DOS MODAIS (NOVO)
   ========================================= */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15, 23, 42, 0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; backdrop-filter: blur(4px); }
.modal-content { background: #ffffff; border-radius: 12px; width: 100%; max-width: 400px; padding: 24px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04); animation: modalIn 0.3s ease-out; }
@keyframes modalIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; }
.modal-header h2 { font-size: 1.25rem; font-weight: 600; color: #0f172a; margin: 0; }
.btn-close { background: transparent; border: none; font-size: 1.2rem; color: #64748b; cursor: pointer; transition: 0.2s; }
.btn-close:hover { color: #ef4444; }

.modal-form { display: flex; flex-direction: column; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #475569; }
.input-group input, .input-group select { padding: 12px 16px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; color: #0f172a; outline: none; transition: 0.2s; background: #fff; font-family: inherit; }
.input-group input:focus, .input-group select:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1); }
.mt-3 { margin-top: 16px; }
.mt-4 { margin-top: 24px; }
</style>