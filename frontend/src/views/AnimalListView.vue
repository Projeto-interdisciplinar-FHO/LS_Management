<template>
  <div class="list-wrapper">
    <header class="page-header">
      <div class="header-info">
        <button @click="goBackToDashboard" class="btn-back">← Voltar</button>
        <h1>Gestão de Animais</h1>
        <p>Listagem completa e controle do rebanho por estábulos.</p>
      </div>
      <button @click="$router.push('/animais/novo')" class="btn-primary">
        + Cadastrar Animal
      </button>
    </header>

    <div class="table-container">
      <div v-if="loading" class="loading-state">
        Buscando registros...
      </div>

      <div v-else-if="animals.length === 0" class="empty-state">
        <p>Nenhum animal cadastrado no sistema ainda.</p>
      </div>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Registro (Brinco)</th>
            <th>Nome/Apelido</th>
            <th>Sexo</th>
            <th>Peso</th>
            <th>Status</th>
            <th class="text-right">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="animal in animals" :key="animal.id">
            <td class="font-mono">#{{ animal.register_number }}</td>
            <td class="font-bold">{{ animal.name || 'N/A' }}</td>
            <td>{{ animal.sex === 'm' || animal.sex === 'M' ? 'Macho' : 'Fêmea' }}</td>
            <td>{{ animal.weight }} kg</td>
            <td>
              <span class="status-badge" :class="animal.active ? 'active' : 'inactive'">
                {{ animal.active ? 'Ativo' : 'Inativo' }}
              </span>
            </td>
            <td class="actions-cell">
              <button @click="viewDetails(animal.id)" class="btn-action">Ver Ficha</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const router = useRouter();
const animals = ref([]);
const loading = ref(true);

const loadAnimals = async () => {
  try {
    const response = await api.get('animals/');
    if (Array.isArray(response.data)) {
      animals.value = response.data;
    } else if (response.data && response.data.results) {
      animals.value = response.data.results;
    }
  } catch (error) {
    console.error("Erro ao carregar animais:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadAnimals();
});

const viewDetails = (id) => {
  router.push({ name: 'animal-detail', params: { id } });
};

const goBackToDashboard = () => {
  router.back();
};
</script>

<style scoped>
.list-wrapper { padding: 40px; background-color: #f8fafc; min-height: 100vh; color: #0f172a; font-family: 'Inter', sans-serif; }
.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 32px; border-bottom: 1px solid #e2e8f0; padding-bottom: 24px; }
.btn-back { background: transparent; border: 1px solid #e2e8f0; color: #64748b; padding: 8px 16px; border-radius: 8px; cursor: pointer; margin-bottom: 16px; font-weight: 500; transition: 0.2s; }
.btn-back:hover { background: #f1f5f9; color: #0f172a; }
.page-header h1 { font-size: 2rem; font-weight: 700; margin-bottom: 8px; }
.page-header p { color: #64748b; font-size: 1rem; }
.btn-primary { background: #16a34a; color: #ffffff; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { background: #15803d; }

.table-container { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th { background: #f8fafc; padding: 16px 24px; font-size: 0.85rem; text-transform: uppercase; color: #64748b; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 16px 24px; border-bottom: 1px solid #e2e8f0; font-size: 0.95rem; color: #0f172a; vertical-align: middle; }
.data-table tr:hover { background: #f8fafc; }
.data-table tr:last-child td { border-bottom: none; }

.font-mono { font-family: monospace; color: #64748b; font-size: 1rem; }
.font-bold { font-weight: 600; }
.status-badge { padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
.status-badge.active { background: #dcfce7; color: #166534; }
.status-badge.inactive { background: #f1f5f9; color: #475569; }

.actions-cell { text-align: right; }
.btn-action { background: transparent; border: 1px solid #e2e8f0; color: #16a34a; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-action:hover { background: #f0fdf4; border-color: #16a34a; }

.loading-state, .empty-state { padding: 60px; text-align: center; color: #64748b; font-size: 1.1rem; }
</style>