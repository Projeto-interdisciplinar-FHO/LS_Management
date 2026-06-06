<template>
  <div class="taxonomy-page">
    <header class="page-header">
      <div class="header-copy">
        <button @click="goHome" class="btn-back">← Voltar ao Dashboard</button>
        <h1>Vacinas cadastradas</h1>
        <p>Lista das vacinas registradas no sistema.</p>
      </div>
      <button @click="openModal" class="btn-primary">+ Adicionar vacina</button>
    </header>

    <section class="content-card">
      <div class="section-header">
        <div>
          <h2>Vacinas</h2>
          <p>Consulte e mantenha o cadastro técnico das vacinas disponíveis.</p>
        </div>
        <span class="count-badge">{{ vaccines.length }} cadastradas</span>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Carregando vacinas...</p>
      </div>

      <div v-else-if="vaccines.length === 0" class="empty-state">
        <p>Nenhuma vacina cadastrada no momento.</p>
      </div>

      <div v-else class="taxonomy-list">
        <article v-for="item in vaccines" :key="item.id" class="taxonomy-item">
          <div class="taxonomy-main">
            <span class="taxonomy-icon">💉</span>
            <div>
              <h3>{{ item.name }}</h3>
              <p>{{ item.description || 'Sem descrição' }}</p>
            </div>
          </div>
        </article>
      </div>
    </section>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content">
        <header class="modal-header">
          <h2>Cadastrar Nova Vacina</h2>
          <button @click="showModal = false" class="btn-close">✕</button>
        </header>

        <form @submit.prevent="submitVaccine" class="modal-form">
          <div class="input-group">
            <label>Nome da Vacina</label>
            <input v-model="form.name" type="text" placeholder="Ex: Brucelose" required>
          </div>
          <div class="input-group">
            <label>Descrição</label>
            <input v-model="form.description" type="text" placeholder="Descrição opcional">
          </div>
          <button type="submit" class="btn-primary mt-4" :disabled="saving">
            {{ saving ? 'Salvando...' : 'Salvar Vacina' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

const goHome = () => {
  const role = localStorage.getItem('user_role');
  if (role === 'op') router.push('/dashboard-op');
  else router.push('/dashboard-adm');
};
import api from '@/services/api';

const vaccines = ref([]);
const loading = ref(false);
const showModal = ref(false);
const saving = ref(false);
const form = ref({ name: '', description: '' });

const normalizeList = (response) => {
  if (Array.isArray(response.data)) return response.data;
  return response.data?.results || [];
};

const loadVaccines = async () => {
  loading.value = true;
  try {
    const response = await api.get('vaccines/');
    vaccines.value = normalizeList(response);
  } catch (error) {
    console.error('Erro ao carregar vacinas:', error);
    vaccines.value = [];
    alert('Erro ao carregar as vacinas.');
  } finally {
    loading.value = false;
  }
};

const openModal = () => {
  form.value = { name: '', description: '' };
  showModal.value = true;
};

const submitVaccine = async () => {
  saving.value = true;
  try {
    await api.post('vaccines/', form.value);
    alert('Vacina cadastrada com sucesso!');
    showModal.value = false;
    await loadVaccines();
  } catch (error) {
    console.error('Erro ao cadastrar vacina:', error);
    alert('Erro ao cadastrar vacina.');
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadVaccines();
});
</script>

<style scoped>
.taxonomy-page {
  min-height: 100vh;
  background: #f8fafc;
  color: #0f172a;
  font-family: 'Lexend', sans-serif;
  padding: 32px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}

.header-copy h1 {
  margin: 12px 0 8px;
  font-size: 2rem;
}

.header-copy p {
  margin: 0;
  color: #64748b;
}

.btn-back {
  background: transparent;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  color: #64748b;
  padding: 8px 12px;
  cursor: pointer;
}

.btn-primary {
  background: #16a34a;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 12px 18px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-primary:hover {
  background: #15803d;
}

.content-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.count-badge {
  background: #f0fdf4;
  color: #16a34a;
  border-radius: 999px;
  padding: 6px 16px;
  font-weight: 700;
  font-size: 0.95rem;
}

.taxonomy-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
}

.taxonomy-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.taxonomy-main {
  display: flex;
  align-items: center;
  gap: 14px;
}

.taxonomy-icon {
  font-size: 2rem;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  border-radius: 12px;
  padding: 32px 28px;
  min-width: 340px;
  max-width: 95vw;
  box-shadow: 0 8px 32px -8px rgba(0,0,0,0.18);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 1.3rem;
  color: #64748b;
  cursor: pointer;
}

.modal-form .input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

input[type="text"] {
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.95rem;
  outline: none;
  transition: 0.2s;
}
input[type="text"]:focus {
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}
.mt-4 { margin-top: 18px; }
</style>
