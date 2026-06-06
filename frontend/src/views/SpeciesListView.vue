<template>
  <div class="taxonomy-page">
    <header class="page-header">
      <div class="header-copy">
        <button @click="goHome" class="btn-back">← Voltar ao Dashboard</button>
        <h1>Espécies cadastradas</h1>
        <p>Lista das espécies registradas no sistema e suas contagens vinculadas.</p>
      </div>
      <button @click="openModal" class="btn-primary">+ Adicionar espécie</button>
    </header>

    <section class="content-card">
      <div class="section-header">
        <div>
          <h2>Espécies</h2>
          <p>Consulte e mantenha o cadastro técnico das espécies do rebanho.</p>
        </div>
        <span class="count-badge">{{ species.length }} cadastradas</span>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Carregando espécies...</p>
      </div>

      <div v-else-if="species.length === 0" class="empty-state">
        <p>Nenhuma espécie cadastrada no momento.</p>
      </div>

      <div v-else class="taxonomy-list">
        <article v-for="item in species" :key="item.id" class="taxonomy-item">
          <div class="taxonomy-main">
            <span class="taxonomy-icon">🧬</span>
            <div>
              <h3>{{ item.name }}</h3>
              <p>{{ item.breeds_count ?? 0 }} raças vinculadas</p>
            </div>
          </div>
        </article>
      </div>
    </section>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content">
        <header class="modal-header">
          <h2>Cadastrar Nova Espécie</h2>
          <button @click="showModal = false" class="btn-close">✕</button>
        </header>

        <form @submit.prevent="submitSpecie" class="modal-form">
          <div class="input-group">
            <label>Nome da Espécie</label>
            <input v-model="form.name" type="text" placeholder="Ex: Bovino" required>
          </div>

          <button type="submit" class="btn-primary mt-4" :disabled="saving">
            {{ saving ? 'Salvando...' : 'Salvar Espécie' }}
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

const species = ref([]);
const loading = ref(false);
const showModal = ref(false);
const saving = ref(false);
const form = ref({ name: '' });

const normalizeList = (response) => {
  if (Array.isArray(response.data)) return response.data;
  return response.data?.results || [];
};

const loadSpecies = async () => {
  loading.value = true;
  try {
    const response = await api.get('species/');
    species.value = normalizeList(response);
  } catch (error) {
    console.error('Erro ao carregar espécies:', error);
    species.value = [];
    alert('Erro ao carregar as espécies.');
  } finally {
    loading.value = false;
  }
};

const openModal = () => {
  form.value = { name: '' };
  showModal.value = true;
};

const submitSpecie = async () => {
  saving.value = true;
  try {
    await api.post('species/', form.value);
    alert('Espécie cadastrada com sucesso!');
    showModal.value = false;
    await loadSpecies();
  } catch (error) {
    console.error('Erro ao cadastrar espécie:', error);
    alert('Erro ao cadastrar espécie.');
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadSpecies();
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
  font-weight: 700;
  cursor: pointer;
}

.content-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.06);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  font-size: 1.2rem;
}

.section-header p {
  margin: 6px 0 0;
  color: #64748b;
}

.count-badge {
  background: #f0fdf4;
  color: #15803d;
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 0.72rem;
  font-weight: 700;
}

.loading-state, .empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  min-height: 180px;
  color: #64748b;
  border: 1px dashed #cbd5e1;
  border-radius: 10px;
  background: #fcfcfd;
}

.spinner {
  width: 18px;
  height: 18px;
  border-radius: 999px;
  border: 2px solid #bbf7d0;
  border-top-color: #16a34a;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.taxonomy-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.taxonomy-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 16px 18px;
  background: #fff;
}

.taxonomy-main {
  display: flex;
  align-items: center;
  gap: 12px;
}

.taxonomy-icon {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0fdf4;
  color: #16a34a;
}

.taxonomy-item h3 {
  margin: 0;
  font-size: 1rem;
}

.taxonomy-item p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 0.88rem;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  border-radius: 12px;
  width: min(420px, calc(100vw - 24px));
  padding: 24px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.1rem;
}

.btn-close {
  background: transparent;
  border: none;
  color: #64748b;
  font-size: 1rem;
  cursor: pointer;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-size: 0.88rem;
  font-weight: 700;
  color: #475569;
}

.input-group input {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 12px 14px;
  font-size: 0.95rem;
}

.mt-4 {
  margin-top: 8px;
}

@media (max-width: 700px) {
  .taxonomy-page {
    padding: 20px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
