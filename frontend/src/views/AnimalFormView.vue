<template>
  <div class="form-wrapper">
    <header class="page-header">
      <button @click="$router.back()" class="btn-back">← Cancelar</button>
      <h1>{{ isEdit ? 'Editar Animal' : 'Cadastrar Novo Animal' }}</h1>
      <p>Preencha as informações técnicas do rebanho.</p>
    </header>

    <div class="form-container">
      <form @submit.prevent="saveAnimal" class="animal-form glass-card">
        
        <div class="form-grid">
          <div class="input-group">
            <label>Nome ou Apelido</label>
            <input v-model="formData.name" type="text" placeholder="Ex: Mimosa" required>
          </div>

          <div class="input-group">
            <label>Nº de Registro (Brinco)</label>
            <input v-model="formData.register_number" type="number" placeholder="Ex: 142" required>
          </div>

          <div class="input-group">
            <label>Data de Nascimento</label>
            <input v-model="formData.birth_date" type="date" required>
          </div>

          <div class="input-group">
            <label>Peso (kg)</label>
            <input v-model="formData.weight" type="number" step="0.01" placeholder="Ex: 450.50" required>
          </div>

          <div class="input-group">
            <label>Sexo</label>
            <select v-model="formData.sex">
              <option value="m">Macho</option>
              <option value="f">Fêmea</option>
            </select>
          </div>

          <div class="input-group">
            <label>Status</label>
            <select v-model="formData.status">
              <option value="ativo">✓ Ativo</option>
              <option value="doente">⚠ Doente</option>
              <option value="vendido">✓ Vendido</option>
              <option value="obito">✗ Óbito</option>
              <option value="inativo">○ Inativo</option>
            </select>
          </div>
          
          <div class="input-group">
            <label>ID da Espécie</label>
            <input v-model="formData.specie" type="number" required>
          </div>
          <div class="input-group">
            <label>ID da Raça</label>
            <input v-model="formData.breed" type="number" required>
          </div>
          <div class="input-group">
            <label>ID do Quadrante (Pasto)</label>
            <input v-model="formData.quadrant" type="number" required>
          </div>
          <div class="input-group">
            <label>ID do Propósito</label>
            <input v-model="formData.purpose" type="number" required>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-save" :disabled="loading">
            {{ loading ? 'Salvando...' : (isEdit ? 'Salvar Alterações' : 'Cadastrar Animal') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();

const isEdit = ref(false);
const loading = ref(false);

const formData = ref({
  name: '',
  register_number: '',
  birth_date: '',
  weight: '',
  sex: 'm',
  status: 'ativo',
  specie: 1,
  breed: 1,
  quadrant: 1,
  purpose: 1
});

onMounted(async () => {
  // Se existir um ID na URL, estamos no modo de Edição (Req 2.3)
  if (route.params.id) {
    isEdit.value = true;
    try {
      const response = await api.getAnimalById(route.params.id);
      formData.value = response.data;
    } catch (error) {
      console.error("Erro ao carregar animal para edição:", error);
      alert("Erro ao buscar dados do animal.");
    }
  }
});

const saveAnimal = async () => {
  loading.value = true;
  try {
    if (isEdit.value) {
      // Requisito 2.3 - Atualizar
      await api.updateAnimal(route.params.id, formData.value);
    } else {
      // Requisito 2.1 - Criar
      await api.createAnimal(formData.value);
    }
    // Sucesso! Volta para a lista
    router.push('/animais');
  } catch (error) {
    console.error("Erro ao salvar:", error);
    console.error("Detalhes do erro:", error.response?.data);
    alert("Falha ao salvar o registro. Verifique os dados.");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.form-wrapper { padding: 40px; background-color: #0d1117; min-height: 100vh; color: #e6edf3; }
.btn-back { background: transparent; border: 1px solid #30363d; color: #8b949e; padding: 8px 16px; border-radius: 6px; cursor: pointer; margin-bottom: 20px; }
.page-header h1 { color: #3fb950; margin-bottom: 5px; }
.page-header p { color: #8b949e; }
.form-container { max-width: 800px; margin-top: 30px; }
.glass-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 30px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.85rem; color: #8b949e; font-weight: bold; }
input, select { background: #0d1117; border: 1px solid #30363d; color: white; padding: 12px; border-radius: 8px; outline: none; }
input:focus, select:focus { border-color: #58a6ff; }
.form-actions { display: flex; justify-content: flex-end; border-top: 1px solid #30363d; padding-top: 20px; }
.btn-save { background: #3fb950; color: #0d1117; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; }
.btn-save:hover { background: #2ea043; }
.btn-save:disabled { background: #30363d; color: #8b949e; cursor: not-allowed; }
</style>