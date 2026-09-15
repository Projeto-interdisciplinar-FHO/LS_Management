<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Registro veterinário"
        descricao="Consultas, motivos e tratativas aplicadas a cada animal."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <div class="stack-24">
        <section class="card">
          <header class="card__head">
            <div class="list__main">
              <span class="icon-tile icon-tile--accent"><AppIcon name="stethoscope" :size="17" /></span>
              <div>
                <h2 class="card__title">Nova consulta</h2>
                <p class="card__desc">O descritivo fica visível na ficha do animal.</p>
              </div>
            </div>
          </header>

          <form @submit.prevent="submitRecord">
            <div class="card__body grid grid--3">
              <div class="field">
                <label class="field__label" for="vet-animal">Animal</label>
                <select id="vet-animal" v-model="formData.animal" class="select" required>
                  <option value="" disabled>Selecione um animal...</option>
                  <option v-for="animal in animalsList" :key="animal.id" :value="animal.id">
                    {{ animal.name || 'Sem nome' }} — #{{ animal.register_number }}
                  </option>
                </select>
              </div>

              <div class="field">
                <label class="field__label" for="vet-nome">Veterinário</label>
                <input id="vet-nome" v-model="formData.veterinarian" class="input" type="text" placeholder="Nome do responsável" required>
              </div>

              <div class="field">
                <label class="field__label" for="vet-data">Data da consulta</label>
                <input id="vet-data" v-model="formData.consultation_date" class="input" type="date" required>
              </div>

              <div class="field span-full">
                <label class="field__label" for="vet-motivo">Motivo da consulta</label>
                <textarea id="vet-motivo" v-model="formData.consultation_reason" class="textarea" rows="3" placeholder="O que foi observado no animal" required></textarea>
              </div>

              <div class="field span-full">
                <label class="field__label" for="vet-solucao">Tratativa e acompanhamento</label>
                <textarea id="vet-solucao" v-model="formData.consultation_solution" class="textarea" rows="4" placeholder="Tratamento aplicado, medicação e acompanhamento previsto" required></textarea>
              </div>

              <p v-if="message" class="span-full alert" :class="isSuccess ? 'alert--ok' : 'alert--danger'" role="status">
                <AppIcon :name="isSuccess ? 'check-circle' : 'alert'" :size="16" />
                <span>{{ message }}</span>
              </p>
            </div>

            <footer class="card__foot">
              <button type="submit" class="btn btn--primary" :disabled="saving">
                {{ saving ? 'Salvando...' : 'Registrar consulta' }}
              </button>
            </footer>
          </form>
        </section>

        <section class="card">
          <header class="card__head">
            <h2 class="card__title">Consultas registradas</h2>
            <span class="badge">{{ records.length }}</span>
          </header>

          <div v-if="loading" class="loading">
            <span class="spinner" aria-hidden="true"></span>
            Carregando histórico veterinário...
          </div>

          <div v-else-if="records.length === 0" class="empty">
            <AppIcon name="stethoscope" :size="30" />
            <p class="empty__title">Nenhuma consulta registrada</p>
            <p class="empty__desc">Os atendimentos lançados aqui aparecem também na ficha do animal.</p>
          </div>

          <div v-else class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Animal</th>
                  <th>Brinco</th>
                  <th>Veterinário</th>
                  <th>Motivo</th>
                  <th>Tratativa</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="record in records" :key="record.id">
                  <td class="mono nowrap">{{ formatDate(record.consultation_date) }}</td>
                  <!-- `animal_register` e o brinco, ja pronto no AnimalHealthSerializer.
                       A coluna mostrava `record.animal`, que e o id interno. -->
                  <td class="cell-strong nowrap">{{ record.animal_name || 'Sem nome' }}</td>
                  <td class="mono nowrap">{{ record.animal_register ? `#${record.animal_register}` : '—' }}</td>
                  <td>{{ record.veterinarian }}</td>
                  <td class="truncate" :title="record.consultation_reason">{{ record.consultation_reason }}</td>
                  <td class="truncate" :title="record.consultation_solution">{{ record.consultation_solution }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';
import { painelDoPapel } from '@/services/auth';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';

const painel = computed(() => painelDoPapel());

const loading = ref(true);
const saving = ref(false);
const animalsList = ref([]);
const records = ref([]);
const message = ref('');
const isSuccess = ref(false);

const formData = ref({
  animal: '',
  veterinarian: '',
  consultation_date: new Date().toISOString().split('T')[0],
  consultation_reason: '',
  consultation_solution: ''
});

const loadAnimals = async () => {
  try {
    const response = await api.getAnimals();
    animalsList.value = response.data.results || response.data;
  } catch (error) {
    console.error('Erro ao carregar animais:', error);
    animalsList.value = [];
  }
};

const loadRecords = async () => {
  loading.value = true;
  try {
    const response = await api.getVeterinaryRecords();
    records.value = response.data.results || response.data;
  } catch (error) {
    console.error('Erro ao carregar registros veterinários:', error);
    records.value = [];
  } finally {
    loading.value = false;
  }
};

const submitRecord = async () => {
  saving.value = true;
  message.value = '';
  try {
    await api.createVeterinaryRecord(formData.value);
    isSuccess.value = true;
    message.value = 'Consulta veterinária registrada com sucesso.';
    formData.value = {
      animal: '',
      veterinarian: '',
      consultation_date: new Date().toISOString().split('T')[0],
      consultation_reason: '',
      consultation_solution: ''
    };
    await loadRecords();
  } catch (error) {
    console.error('Erro ao salvar registro:', error);
    isSuccess.value = false;
    message.value = 'Erro ao salvar consulta veterinária.';
  } finally {
    saving.value = false;
    setTimeout(() => { message.value = ''; }, 5000);
  }
};

const formatDate = (value) => {
  if (!value) return 'N/A';
  return new Date(value).toLocaleDateString('pt-BR');
};

onMounted(async () => {
  await Promise.all([loadAnimals(), loadRecords()]);
});
</script>
