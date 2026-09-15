<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        :titulo="isEdit ? 'Editar animal' : 'Cadastrar animal'"
        :descricao="isEdit ? 'Altere os dados da ficha e salve.' : 'Preencha a ficha do animal para incluí-lo no rebanho.'"
        voltar-rotulo="Animais"
        voltar-para="/animais"
      />

      <form class="stack-24" @submit.prevent="saveAnimal">
        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Identificação</h2>
              <p class="card__desc">Como o animal é reconhecido no curral e no sistema.</p>
            </div>
          </header>

          <div class="card__body grid grid--2">
            <div class="field">
              <label class="field__label" for="nome">Nome ou apelido</label>
              <input id="nome" v-model="formData.name" class="input" type="text" placeholder="Ex: Mimosa" required>
            </div>

            <div class="field">
              <label class="field__label" for="brinco">Nº de registro (brinco)</label>
              <input id="brinco" v-model="formData.register_number" class="input" type="number" placeholder="Ex: 142" required>
            </div>

            <div class="field">
              <label class="field__label" for="nascimento">Data de nascimento</label>
              <input id="nascimento" v-model="formData.birth_date" class="input" type="date" required>
            </div>

            <div class="field">
              <label class="field__label" for="peso">Peso (kg)</label>
              <input id="peso" v-model="formData.weight" class="input" type="number" step="0.01" placeholder="450.00" required>
            </div>

            <div class="field">
              <label class="field__label" for="sexo">Sexo</label>
              <select id="sexo" v-model="formData.sex" class="select">
                <option value="m">Macho</option>
                <option value="f">Fêmea</option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="situacao">Situação</label>
              <select id="situacao" v-model="formData.status" class="select">
                <option v-for="s in SITUACOES" :key="s.valor" :value="s.valor">{{ s.rotulo }}</option>
              </select>
              <span class="field__hint">
                Vendido, óbito e inativo tiram o animal das rotinas de manejo, mas preservam o histórico.
              </span>
            </div>
          </div>
        </section>

        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Classificação e localização</h2>
              <p class="card__desc">Origem biológica do animal e onde ele fica alojado.</p>
            </div>
          </header>

          <div class="card__body grid grid--2">
            <div class="field">
              <label class="field__label" for="especie">Espécie</label>
              <select id="especie" v-model="formData.specie" class="select" required>
                <option value="" disabled>Selecione uma espécie...</option>
                <option v-for="specie in speciesList" :key="specie.id" :value="specie.id">
                  {{ specie.name }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="raca">Raça</label>
              <select id="raca" v-model="formData.breed" class="select" required>
                <option value="" disabled>Selecione uma raça...</option>
                <option v-for="breed in breedsList" :key="breed.id" :value="breed.id">
                  {{ breed.name }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="estabulo">Estábulo</label>
              <select id="estabulo" v-model="formData.quadrant" class="select" required>
                <option value="" disabled>Selecione um estábulo...</option>
                <option v-for="stable in stablesList" :key="stable.id" :value="stable.id">
                  {{ stable.name || stable.nome_quadrante || `Estábulo ${stable.id}` }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="finalidade">Finalidade</label>
              <select id="finalidade" v-model="formData.purpose" class="select" required>
                <option value="" disabled>Selecione a finalidade...</option>
                <option v-for="purpose in purposeList" :key="purpose.id" :value="purpose.id">
                  {{ purpose.name || purpose.tipo || `Finalidade ${purpose.id}` }}
                </option>
              </select>
            </div>
          </div>

          <footer class="card__foot">
            <button type="button" class="btn" @click="$router.back()">Cancelar</button>
            <button type="submit" class="btn btn--primary" :disabled="loading">
              {{ loading ? 'Salvando...' : (isEdit ? 'Salvar alterações' : 'Cadastrar animal') }}
            </button>
          </footer>
        </section>
      </form>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import { notify } from '@/services/notificationService';
import AppShell from '@/components/layout/AppShell.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { SITUACOES, ativoPara } from '@/utils/statusUtils';

const route = useRoute();
const router = useRouter();

const isEdit = ref(false);
const loading = ref(false);

const speciesList = ref([]);
const breedsList = ref([]);
const stablesList = ref([]);
const purposeList = ref([]);

const formData = ref({
  name: '', register_number: '', birth_date: '', weight: '', sex: 'm',
  status: 'ativo', active: true,
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
    // O booleano legado `active` sai do `status` — a tela não tem dois
    // controles para a mesma coisa, mas o backend continua recebendo os dois.
    const dados = { ...formData.value, active: ativoPara(formData.value.status) };

    if (isEdit.value) {
      await api.put(`animals/${route.params.id}/`, dados);
    } else {
      await api.post('animals/', dados);
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
