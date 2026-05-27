<template>
  <div class="form-wrapper">
    <header class="page-header">
      <button @click="$router.back()" class="btn-back">← Cancelar</button>
      <h1>{{ isEdit ? 'Editar Animal' : 'Cadastrar Novo Animal' }}</h1>
    </header>

    <div class="form-container">
      <form @submit.prevent="saveAnimal" class="data-form">
        <h3 class="section-title">Dados Básicos</h3>
        <div class="form-grid">
          <div class="input-group">
            <label>Nome ou Apelido</label>
            <input v-model="formData.name" type="text" placeholder="Ex: Mimosa" required>
          </div>
          <div class="input-group">
            <label>Nº de Registro (Brinco)</label>
            <input v-model="formData.register_number" type="number" required>
          </div>
          <div class="input-group">
            <label>Data de Nascimento</label>
            <input v-model="formData.birth_date" type="date" required>
          </div>
          <div class="input-group">
            <label>Peso (kg)</label>
            <input v-model="formData.weight" type="number" step="0.01" required>
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
            <select v-model="formData.active">
              <option :value="true">Ativo</option>
              <option :value="false">Inativo</option>
            </select>
          </div>
        </div>

        <h3 class="section-title mt-4">Classificação e Localização</h3>
        <div class="form-grid">
          <div class="input-group">
            <label>Espécie</label>
            <select v-model="formData.specie" required>
              <option value="" disabled>Selecione uma espécie...</option>
              <option v-for="specie in speciesList" :key="specie.id" :value="specie.id">
                {{ specie.name }}
              </option>
            </select>
          </div>
          <div class="input-group">
            <label>Raça</label>
            <select v-model="formData.breed" required>
              <option value="" disabled>Selecione uma raça...</option>
              <option v-for="breed in breedsList" :key="breed.id" :value="breed.id">
                {{ breed.name }}
              </option>
            </select>
          </div>
          <div class="input-group">
            <label>Estábulo (Localização)</label>
            <select v-model="formData.quadrant" required>
              <option value="" disabled>Selecione um estábulo...</option>
              <option v-for="stable in stablesList" :key="stable.id" :value="stable.id">
                {{ stable.name || stable.nome_quadrante || `Estábulo ${stable.id}` }}
              </option>
            </select>
          </div>
          <div class="input-group">
            <label>Finalidade</label>
            <select v-model="formData.purpose" required>
              <option value="" disabled>Selecione a finalidade...</option>
              <option v-for="purpose in purposeList" :key="purpose.id" :value="purpose.id">
                {{ purpose.name || purpose.tipo || `Finalidade ${purpose.id}` }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="loading">
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
import { notify } from '@/services/notificationService';

const route = useRoute();
const router = useRouter();

const isEdit = ref(false);
const loading = ref(false);

const speciesList = ref([]);
const breedsList = ref([]);
const stablesList = ref([]);
const purposeList = ref([]);

const formData = ref({
  name: '', register_number: '', birth_date: '', weight: '', sex: 'm', active: true,
  specie: '', breed: '', quadrant: '', purpose: '' // purpose é obrigatório no backend
});

onMounted(async () => {
  // Carrega as listas dos menus suspensos
  fetchDropdownData();

  if (route.params.id) {
    isEdit.value = true;
    try {
      const response = await api.get(`animals/${route.params.id}/`);
      formData.value = response.data;
    } catch (error) {
      console.error("Erro ao carregar animal:", error);
    }
  }
});

const fetchDropdownData = async () => {
  try {
    // Estas chamadas assumem que você criará as rotas /species/ e /breeds/ no Django
    // O catch silencioso garante que a tela não quebre caso a API ainda não exista
    api.get('species/').then(res => speciesList.value = res.data).catch(() => {
      // Mock provisório enquanto o backend não tem a rota
      speciesList.value = [{id: 1, name: 'Bovino'}, {id: 2, name: 'Equino'}];
    });
    
    api.get('breeds/').then(res => breedsList.value = res.data).catch(() => {
      breedsList.value = [{id: 1, name: 'Holandês'}, {id: 2, name: 'Nelore'}, {id: 3, name: 'Angus'}];
    });

    api.get('purpose_types/').then(res => purposeList.value = res.data).catch(() => {
      purposeList.value = [
        {id: 1, name: 'Criação'},
        {id: 2, name: 'Leite'},
        {id: 3, name: 'Venda'}
      ];
    });

    api.get('quadrants/').then(res => stablesList.value = res.data).catch(() => {
      stablesList.value = [{id: 1, name: 'Estábulo Principal'}, {id: 2, name: 'Estábulo Sul'}];
    });
  } catch (e) {
    console.error(e);
  }
};

const saveAnimal = async () => {
  loading.value = true;
  try {
    if (isEdit.value) {
      await api.put(`animals/${route.params.id}/`, formData.value);
    } else {
      await api.post('animals/', formData.value);
    }
    router.push('/animais');
  } catch (error) {
    console.error("Erro ao salvar:", error);
    notify("Falha ao salvar os dados.", 'error');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.form-wrapper { padding: 40px; background-color: #f8fafc; min-height: 100vh; color: #0f172a; font-family: 'Inter', sans-serif; }
.page-header { margin-bottom: 32px; }
.btn-back { background: transparent; border: 1px solid #e2e8f0; color: #64748b; padding: 8px 16px; border-radius: 8px; cursor: pointer; margin-bottom: 16px; font-weight: 500; }
.page-header h1 { font-size: 2rem; font-weight: 700; color: #0f172a; }

.form-container { max-width: 900px; }
.data-form { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
.section-title { font-size: 1.1rem; color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 24px; }
.mt-4 { margin-top: 40px; }

.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 24px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #475569; }
input, select { padding: 12px 16px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; color: #0f172a; outline: none; transition: 0.2s; background: #fff; }
input:focus, select:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1); }

.form-actions { display: flex; justify-content: flex-end; margin-top: 40px; border-top: 1px solid #e2e8f0; padding-top: 24px; }
.btn-primary { background: #16a34a; color: #ffffff; border: none; padding: 14px 28px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { background: #15803d; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
</style>