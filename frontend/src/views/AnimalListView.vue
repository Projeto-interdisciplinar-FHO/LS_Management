<template>
  <div class="animal-list-wrapper">
    <header class="page-header">
      <div class="header-info">
        <button @click="$router.push('/dashboard-adm')" class="btn-back">← Voltar ao Dashboard</button>
        <h1>Gestão de Animais</h1>
        <p>Listagem sincronizada com os registros do banco de dados.</p>
      </div>
    </header>

    <!-- FILTROS/ABAS DE STATUS -->
    <section class="filter-tabs">
      <button 
        v-for="status in statusFilters" 
        :key="status.value"
        class="filter-tab"
        :class="{ active: activeStatusFilter === status.value }"
        @click="activeStatusFilter = status.value"
      >
        <span class="filter-icon">{{ status.icon }}</span>
        <span class="filter-label">{{ status.label }}</span>
        <span class="filter-count">{{ getCountByStatus(status.value) }}</span>
      </button>
    </section>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Buscando dados no servidor Django...</p>
    </div>

    <div v-else-if="filteredAnimals.length === 0" class="empty-state">
      <span class="empty-icon">📂</span>
      <h3>Nenhum animal encontrado</h3>
      <p v-if="activeStatusFilter === 'todos'">Não há registros no banco de dados ou a API retornou uma lista vazia.</p>
      <p v-else>Nenhum animal com status "{{ getStatusLabel(activeStatusFilter) }}" encontrado.</p>
    </div>

    <div v-else class="animals-grid">
      <div v-for="animal in filteredAnimals" :key="animal.id" class="animal-card">
        
        <div class="card-header">
          <span class="tag-id">REG: {{ animal.register_number }}</span>
          <div class="header-icons">
            <AnimalAlertBadge :animal-id="animal.id" :show-count="true" />
            <span class="status-dot" :style="{ backgroundColor: getStatusColor(animal.status || 'inativo') }" :title="animal.status || 'inativo'">
              {{ getStatusIcon(animal.status || 'inativo') }}
            </span>
          </div>
        </div>
        
        <div class="animal-image-container">
          <img v-if="animal.image" :src="animal.image" :alt="animal.name" class="animal-image">
          <div v-else class="image-placeholder">
            <span class="image-icon">🐄</span>
          </div>
        </div>
        
        <div class="animal-info">
          <h3>{{ animal.name || 'Sem Nome' }}</h3>
          <p class="birth">Nascimento: {{ animal.birth_date }}</p>
        </div>

        <div class="animal-details">
          <div class="detail-item">
            <span class="label">Sexo</span>
            <span class="value">{{ animal.sex === 'm' || animal.sex === 'M' ? 'Macho' : 'Fêmea' }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Peso</span>
            <span class="value">{{ animal.weight }} kg</span>
          </div>
          <div class="detail-item">
            <span class="label">Status</span>
            <span class="value" :style="{ color: getStatusColor(animal.status || 'inativo') }">
              {{ getStatusIcon(animal.status || 'inativo') }} {{ animal.status || 'Inativo' }}
            </span>
          </div>
        </div>

        <div class="card-actions">
          <button class="btn-detail" @click="viewDetails(animal.id)">Ver Ficha</button>
          <button class="btn-edit" @click="openEditModal(animal)">✏️ Editar</button>
          <button class="btn-delete" @click="deleteAnimal(animal.id)">🗑️ Deletar</button>
        </div>
      </div>
    </div>

    <!-- Botão Flutuante de Adicionar -->
    <button class="btn-add-animal" @click="openAddModal" title="Adicionar novo animal">
      <span class="icon">➕</span>
    </button>

    <!-- Modal de Adicionar Animal -->
    <div v-if="showAddModal" class="modal-overlay" @click="closeAddModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Adicionar Novo Animal</h2>
          <button class="btn-close" @click="closeAddModal">✕</button>
        </div>

        <form @submit.prevent="submitAddAnimal" class="form-animal">
          <div class="form-row">
            <div class="form-group">
              <label>Nome *</label>
              <input v-model="newAnimal.name" type="text" required placeholder="Ex: Bezerro">
            </div>
            <div class="form-group">
              <label>Registro *</label>
              <input v-model.number="newAnimal.register_number" type="number" required placeholder="Ex: 50">
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Data de Nascimento *</label>
              <input v-model="newAnimal.birth_date" type="date" required>
            </div>
            <div class="form-group">
              <label>Peso (kg) *</label>
              <input v-model.number="newAnimal.weight" type="number" step="0.01" required placeholder="Ex: 15.00">
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Sexo *</label>
              <select v-model="newAnimal.sex" required>
                <option value="">Selecione...</option>
                <option value="m">Macho</option>
                <option value="f">Fêmea</option>
              </select>
            </div>
            <div class="form-group">
              <label>Status *</label>
              <select v-model="newAnimal.status" required>
                <option value="">Selecione...</option>
                <option value="ativo">✓ Ativo</option>
                <option value="doente">⚠ Doente</option>
                <option value="vendido">✓ Vendido</option>
                <option value="obito">✗ Óbito</option>
                <option value="inativo">○ Inativo</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Espécie (ID) *</label>
              <input v-model.number="newAnimal.specie" type="number" required placeholder="Ex: 1">
            </div>
            <div class="form-group">
              <label>Raça (ID)</label>
              <input v-model.number="newAnimal.breed" type="number" placeholder="Ex: 1">
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Quadrante (ID) *</label>
              <input v-model.number="newAnimal.quadrant" type="number" required placeholder="Ex: 2">
            </div>
            <div class="form-group">
              <label>Tipo de Propósito (ID) *</label>
              <input v-model.number="newAnimal.purpose" type="number" required placeholder="Ex: 1">
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn-cancel" @click="closeAddModal">Cancelar</button>
            <button type="submit" class="btn-submit" :disabled="loading">
              {{ loading ? 'Salvando...' : 'Adicionar Animal' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de Editar Animal -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Editar Animal</h2>
          <button class="btn-close" @click="closeEditModal">✕</button>
        </div>

        <form @submit.prevent="submitEditAnimal" class="form-animal">
          <div class="form-row">
            <div class="form-group">
              <label>Nome *</label>
              <input v-model="editingAnimal.name" type="text" required placeholder="Ex: Bezerro">
            </div>
            <div class="form-group">
              <label>Registro *</label>
              <input v-model.number="editingAnimal.register_number" type="number" required placeholder="Ex: 50">
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Data de Nascimento *</label>
              <input v-model="editingAnimal.birth_date" type="date" required>
            </div>
            <div class="form-group">
              <label>Peso (kg) *</label>
              <input v-model.number="editingAnimal.weight" type="number" step="0.01" required placeholder="Ex: 15.00">
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Sexo *</label>
              <select v-model="editingAnimal.sex" required>
                <option value="">Selecione...</option>
                <option value="m">Macho</option>
                <option value="f">Fêmea</option>
              </select>
            </div>
            <div class="form-group">
              <label>Status *</label>
              <select v-model="editingAnimal.status" required>
                <option value="">Selecione...</option>
                <option value="ativo">✓ Ativo</option>
                <option value="doente">⚠ Doente</option>
                <option value="vendido">✓ Vendido</option>
                <option value="obito">✗ Óbito</option>
                <option value="inativo">○ Inativo</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Espécie (ID) *</label>
              <input v-model.number="editingAnimal.specie" type="number" required placeholder="Ex: 1">
            </div>
            <div class="form-group">
              <label>Raça (ID)</label>
              <input v-model.number="editingAnimal.breed" type="number" placeholder="Ex: 1">
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Quadrante (ID) *</label>
              <input v-model.number="editingAnimal.quadrant" type="number" required placeholder="Ex: 2">
            </div>
            <div class="form-group">
              <label>Tipo de Propósito (ID) *</label>
              <input v-model.number="editingAnimal.purpose" type="number" required placeholder="Ex: 1">
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="btn-cancel" @click="closeEditModal">Cancelar</button>
            <button type="submit" class="btn-submit" :disabled="loading">
              {{ loading ? 'Salvando...' : 'Atualizar Animal' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import { getStatusColor, getStatusIcon } from '@/utils/statusUtils';
import AnimalAlertBadge from '@/components/AnimalAlertBadge.vue';

const router = useRouter();
const animals = ref([]);
const loading = ref(true);
const showAddModal = ref(false);
const showEditModal = ref(false);
const editingAnimalId = ref(null);
const activeStatusFilter = ref('todos');

const statusFilters = [
  { value: 'todos', label: 'Todos', icon: '◈' },
  { value: 'ativo', label: 'Ativos', icon: '✓' },
  { value: 'doente', label: 'Doentes', icon: '⚠' },
  { value: 'vendido', label: 'Vendidos', icon: '↗' },
  { value: 'obito', label: 'Óbito', icon: '✗' },
  { value: 'inativo', label: 'Inativos', icon: '○' }
];

// Computed property para filtrar animais baseado no status selecionado
const filteredAnimals = computed(() => {
  if (activeStatusFilter.value === 'todos') {
    return animals.value;
  }
  return animals.value.filter(animal => animal.status === activeStatusFilter.value);
});

// Contar animais por status
const getCountByStatus = (status) => {
  if (status === 'todos') {
    return animals.value.length;
  }
  return animals.value.filter(animal => animal.status === status).length;
};

// Obter label do status
const getStatusLabel = (status) => {
  const filter = statusFilters.find(f => f.value === status);
  return filter ? filter.label : status;
};

const newAnimal = ref({
  name: '',
  birth_date: '',
  register_number: '',
  weight: '',
  status: 'ativo',
  sex: '',
  specie: '',
  breed: null,
  quadrant: '',
  purpose: ''
});

const editingAnimal = ref({
  name: '',
  birth_date: '',
  register_number: '',
  weight: '',
  status: 'ativo',
  sex: '',
  specie: '',
  breed: null,
  quadrant: '',
  purpose: ''
});

const loadAnimals = async () => {
  try {
    // Chamada correta utilizando o api.getAnimals() configurado no api.js
    const response = await api.getAnimals();
    
    // Tratamento para garantir que lemos a lista independente do formato do Django (com ou sem paginação)
    if (Array.isArray(response.data)) {
      animals.value = response.data;
    } else if (response.data && response.data.results) {
      animals.value = response.data.results;
    } else {
      animals.value = [];
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

const openAddModal = () => {
  showAddModal.value = true;
};

const closeAddModal = () => {
  showAddModal.value = false;
  resetForm();
};

const resetForm = () => {
  newAnimal.value = {
    name: '',
    birth_date: '',
    register_number: '',
    weight: '',
    status: 'ativo',
    sex: '',
    specie: '',
    breed: null,
    quadrant: '',
    purpose: ''
  };
};

const submitAddAnimal = async () => {
  // Validar campos obrigatórios
  if (!newAnimal.value.name?.trim()) {
    alert("Nome do animal é obrigatório.");
    return;
  }
  if (!newAnimal.value.birth_date) {
    alert("Data de nascimento é obrigatória.");
    return;
  }
  if (!newAnimal.value.register_number) {
    alert("Número de registro é obrigatório.");
    return;
  }
  if (!newAnimal.value.weight) {
    alert("Peso é obrigatório.");
    return;
  }
  if (!newAnimal.value.sex) {
    alert("Sexo é obrigatório.");
    return;
  }
  if (!newAnimal.value.status) {
    alert("Status é obrigatório.");
    return;
  }
  if (!newAnimal.value.specie) {
    alert("Espécie (ID) é obrigatória.");
    return;
  }
  if (!newAnimal.value.quadrant) {
    alert("Quadrante (ID) é obrigatório.");
    return;
  }
  if (!newAnimal.value.purpose) {
    alert("Tipo de Propósito (ID) é obrigatório.");
    return;
  }

  loading.value = true;
  try {
    // Preparar dados para envio - garantir tipos corretos
    const animalData = {
      name: newAnimal.value.name.trim(),
      birth_date: newAnimal.value.birth_date,
      register_number: parseInt(newAnimal.value.register_number),
      weight: parseFloat(newAnimal.value.weight),
      status: newAnimal.value.status,
      active: newAnimal.value.status === 'ativo',
      sex: String(newAnimal.value.sex).toLowerCase(),
      specie: parseInt(newAnimal.value.specie),
      breed: newAnimal.value.breed ? parseInt(newAnimal.value.breed) : null,
      quadrant: parseInt(newAnimal.value.quadrant),
      purpose: parseInt(newAnimal.value.purpose)
    };

    console.log("Enviando dados:", animalData);
    const response = await api.createAnimal(animalData);
    console.log("Animal criado com sucesso:", response.data);

    // Adicionar o novo animal à lista
    animals.value.push(response.data);

    // Fechar modal e resetar formulário
    closeAddModal();
    
    // Recarregar lista para garantir sincronização
    await loadAnimals();
    
    alert("Animal adicionado com sucesso!");
  } catch (error) {
    console.error("Erro ao criar animal:", error);
    console.error("Resposta do servidor:", error.response?.data);
    
    // Extrair mensagem de erro do servidor
    let errorMessage = "Erro ao adicionar animal";
    if (error.response?.data) {
      if (typeof error.response.data === 'object') {
        // Se for um objeto com múltiplos campos de erro
        const errors = Object.entries(error.response.data)
          .map(([field, msgs]) => {
            const msgArray = Array.isArray(msgs) ? msgs : [msgs];
            return `${field}: ${msgArray.join(', ')}`;
          })
          .join('\n');
        errorMessage = errors || error.response.data.detail || errorMessage;
      } else if (error.response.data.detail) {
        errorMessage = error.response.data.detail;
      }
    }
    
    alert(errorMessage);
  } finally {
    loading.value = false;
  }
};

const openEditModal = (animal) => {
  editingAnimalId.value = animal.id;
  editingAnimal.value = { ...animal };
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
  editingAnimalId.value = null;
  editingAnimal.value = {
    name: '',
    birth_date: '',
    register_number: '',
    weight: '',
    status: 'ativo',
    sex: '',
    specie: '',
    breed: null,
    quadrant: '',
    purpose: ''
  };
};

const submitEditAnimal = async () => {
  // Validações similares ao de adição
  if (!editingAnimal.value.name?.trim()) {
    alert("Nome do animal é obrigatório.");
    return;
  }
  if (!editingAnimal.value.birth_date) {
    alert("Data de nascimento é obrigatória.");
    return;
  }
  if (!editingAnimal.value.register_number) {
    alert("Número de registro é obrigatório.");
    return;
  }
  if (!editingAnimal.value.weight) {
    alert("Peso é obrigatório.");
    return;
  }
  if (!editingAnimal.value.sex) {
    alert("Sexo é obrigatório.");
    return;
  }
  if (!editingAnimal.value.status) {
    alert("Status é obrigatório.");
    return;
  }
  if (!editingAnimal.value.specie) {
    alert("Espécie (ID) é obrigatória.");
    return;
  }
  if (!editingAnimal.value.quadrant) {
    alert("Quadrante (ID) é obrigatório.");
    return;
  }
  if (!editingAnimal.value.purpose) {
    alert("Tipo de Propósito (ID) é obrigatório.");
    return;
  }

  loading.value = true;
  try {
    const animalData = {
      name: editingAnimal.value.name.trim(),
      birth_date: editingAnimal.value.birth_date,
      register_number: parseInt(editingAnimal.value.register_number),
      weight: parseFloat(editingAnimal.value.weight),
      status: editingAnimal.value.status,
      active: editingAnimal.value.status === 'ativo',
      sex: String(editingAnimal.value.sex).toLowerCase(),
      specie: parseInt(editingAnimal.value.specie),
      breed: editingAnimal.value.breed ? parseInt(editingAnimal.value.breed) : null,
      quadrant: parseInt(editingAnimal.value.quadrant),
      purpose: parseInt(editingAnimal.value.purpose)
    };

    console.log("Atualizando animal com ID:", editingAnimalId.value, "Dados:", animalData);
    const response = await api.updateAnimal(editingAnimalId.value, animalData);
    console.log("Animal atualizado com sucesso:", response.data);

    // Atualizar o animal na lista
    const index = animals.value.findIndex(a => a.id === editingAnimalId.value);
    if (index !== -1) {
      animals.value[index] = response.data;
    }

    closeEditModal();
    alert("Animal atualizado com sucesso!");
  } catch (error) {
    console.error("Erro ao atualizar animal:", error);
    console.error("Resposta do servidor:", error.response?.data);
    
    let errorMessage = "Erro ao atualizar animal";
    if (error.response?.data) {
      if (typeof error.response.data === 'object') {
        const errors = Object.entries(error.response.data)
          .map(([field, msgs]) => {
            const msgArray = Array.isArray(msgs) ? msgs : [msgs];
            return `${field}: ${msgArray.join(', ')}`;
          })
          .join('\n');
        errorMessage = errors || error.response.data.detail || errorMessage;
      } else if (error.response.data.detail) {
        errorMessage = error.response.data.detail;
      }
    }
    
    alert(errorMessage);
  } finally {
    loading.value = false;
  }
};

const deleteAnimal = async (id) => {
  const confirm = window.confirm("Tem certeza que deseja deletar este animal? Esta ação não pode ser desfeita.");
  if (!confirm) return;

  loading.value = true;
  try {
    console.log("Deletando animal com ID:", id);
    await api.deleteAnimal(id);
    console.log("Animal deletado com sucesso");

    // Remover o animal da lista
    animals.value = animals.value.filter(a => a.id !== id);
    
    alert("Animal deletado com sucesso!");
  } catch (error) {
    console.error("Erro ao deletar animal:", error);
    console.error("Resposta do servidor:", error.response?.data);
    
    let errorMessage = "Erro ao deletar animal";
    if (error.response?.data) {
      if (typeof error.response.data === 'object') {
        const errors = Object.entries(error.response.data)
          .map(([field, msgs]) => {
            const msgArray = Array.isArray(msgs) ? msgs : [msgs];
            return `${field}: ${msgArray.join(', ')}`;
          })
          .join('\n');
        errorMessage = errors || error.response.data.detail || errorMessage;
      } else if (error.response.data.detail) {
        errorMessage = error.response.data.detail;
      }
    }
    
    alert(errorMessage);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.animal-list-wrapper {
  padding: 40px;
  background-color: #0d1117;
  min-height: 100vh;
  color: #e6edf3;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.page-header {
  margin-bottom: 30px;
  border-bottom: 1px solid #30363d;
  padding-bottom: 20px;
}

/* FILTROS/ABAS */
.filter-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #30363d;
  flex-wrap: wrap;
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 8px;
  color: #8b949e;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  font-weight: 500;
}

.filter-tab:hover {
  border-color: #58a6ff;
  color: #58a6ff;
  background: rgba(88, 166, 255, 0.05);
}

.filter-tab.active {
  background: linear-gradient(135deg, #3fb950 0%, #2d8737 100%);
  border-color: #3fb950;
  color: white;
}

.filter-icon {
  font-size: 1.1rem;
}

.filter-label {
  font-weight: 600;
}

.filter-count {
  display: inline-block;
  min-width: 24px;
  height: 24px;
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  text-align: center;
  line-height: 20px;
}

.filter-tab.active .filter-count {
  background: rgba(255, 255, 255, 0.2);
}

.btn-back {
  background: transparent;
  border: 1px solid #30363d;
  color: #8b949e;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 15px;
  transition: 0.2s;
}

.btn-back:hover {
  background: #21262d;
  color: #e6edf3;
}

.page-header h1 {
  font-size: 2.2rem;
  color: #3fb950;
  margin-bottom: 5px;
}

.page-header p {
  color: #8b949e;
  font-size: 0.95rem;
}

/* Telas de Aviso */
.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  background: #161b22;
  border: 1px dashed #30363d;
  border-radius: 12px;
  color: #8b949e;
}

.spinner {
  width: 40px; height: 40px;
  border: 4px solid #30363d;
  border-top-color: #3fb950;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 15px;
}

@keyframes spin { 100% { transform: rotate(360deg); } }

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 15px;
}

.empty-state h3 {
  color: #e6edf3;
  margin-bottom: 5px;
}

/* Grid de Cards */
.animals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 25px;
  margin-top: 30px;
}

.animal-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 24px;
  transition: transform 0.2s, border-color 0.2s;
}

.animal-card:hover {
  transform: translateY(-4px);
  border-color: #58a6ff;
  box-shadow: 0 4px 12px rgba(88, 166, 255, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.tag-id {
  background: rgba(88, 166, 255, 0.1);
  color: #58a6ff;
  padding: 4px 10px;
  border-radius: 6px;
  font-family: monospace;
  font-size: 0.9rem;
  font-weight: bold;
}

.header-icons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #f85149;
  box-shadow: 0 0 5px #f85149;
}

.status-dot.active {
  background: #3fb950;
  box-shadow: 0 0 5px #3fb950;
}

.animal-image-container {
  width: 100%;
  height: 220px;
  background: #0d1117;
  border: 2px dashed #30363d;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  overflow: hidden;
  transition: border-color 0.2s;
}

.animal-image-container:hover {
  border-color: #58a6ff;
}

.animal-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #21262d 0%, #161b22 100%);
}

.image-icon {
  font-size: 4rem;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.animal-image-container:hover .image-icon {
  opacity: 0.8;
}

.animal-info h3 {
  font-size: 1.4rem;
  color: #f0f6fc;
  margin-bottom: 4px;
}

.birth {
  color: #8b949e;
  font-size: 0.85rem;
  margin-bottom: 20px;
}

.animal-details {
  display: flex;
  justify-content: space-between;
  border-top: 1px solid #30363d;
  padding-top: 15px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item .label {
  font-size: 0.75rem;
  color: #8b949e;
  text-transform: uppercase;
}

.detail-item .value {
  font-weight: bold;
  font-size: 0.95rem;
  color: #e6edf3;
}

/* Botão Flutuante */
.btn-add-animal {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #3fb950 0%, #2d8737 100%);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(63, 185, 80, 0.4);
  transition: all 0.3s;
  z-index: 100;
}

.btn-add-animal:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(63, 185, 80, 0.6);
}

.btn-add-animal .icon {
  font-size: 1.8rem;
  color: white;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #30363d;
}

.modal-header h2 {
  color: #3fb950;
  margin: 0;
  font-size: 1.5rem;
}

.btn-close {
  background: transparent;
  border: none;
  color: #8b949e;
  font-size: 1.5rem;
  cursor: pointer;
  transition: color 0.2s;
}

.btn-close:hover {
  color: #e6edf3;
}

/* Formulário */
.form-animal {
  padding: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  color: #8b949e;
  font-size: 0.9rem;
  margin-bottom: 6px;
  font-weight: 500;
}

.form-group input,
.form-group select {
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 6px;
  color: #e6edf3;
  padding: 10px 12px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #58a6ff;
  box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1);
}

.form-group input::placeholder {
  color: #484f58;
}

.form-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #30363d;
}

.btn-cancel,
.btn-submit {
  padding: 12px 16px;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: transparent;
  border: 1px solid #30363d;
  color: #8b949e;
}

.btn-cancel:hover {
  background: #21262d;
  border-color: #484f58;
  color: #e6edf3;
}

.btn-submit {
  background: linear-gradient(135deg, #3fb950 0%, #2d8737 100%);
  color: white;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(63, 185, 80, 0.3);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.text-green { color: #3fb950 !important; }
.text-red { color: #f85149 !important; }

.btn-detail {
  width: 100%;
  background: transparent;
  border: 1px solid #58a6ff;
  color: #58a6ff;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
  font-weight: bold;
}

.btn-detail:hover {
  background: rgba(88, 166, 255, 0.1);
}

.card-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  width: 100%;
}

.btn-detail,
.btn-edit,
.btn-delete {
  flex: 1;
  padding: 10px;
  border-radius: 6px;
  cursor: pointer;
  border: 1px solid;
  font-weight: bold;
  transition: 0.2s;
  font-size: 0.85rem;
}

.btn-detail {
  background: transparent;
  border-color: #58a6ff;
  color: #58a6ff;
}

.btn-detail:hover {
  background: rgba(88, 166, 255, 0.1);
}

.btn-edit {
  background: transparent;
  border-color: #3fb950;
  color: #3fb950;
}

.btn-edit:hover {
  background: rgba(63, 185, 80, 0.1);
}

.btn-delete {
  background: transparent;
  border-color: #f85149;
  color: #f85149;
}

.btn-delete:hover {
  background: rgba(248, 81, 73, 0.1);
}
</style>