<template>
  <AppShell>
    <div class="page page--wide">
      <PageHeader
        titulo="Atendimento veterinário"
        descricao="Registre consultas, motivos e tratativas aplicadas ao rebanho e acompanhe o histórico clínico de cada animal."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      >
        <template #acoes>
          <button type="button" class="btn btn--primary" @click="abrirModalCadastro">
            <AppIcon name="plus" :size="16" />
            Cadastrar novo atendimento
          </button>
        </template>
      </PageHeader>

      <p v-if="statusMessage" class="alert alert--ok" role="status">
        <AppIcon name="check-circle" :size="16" />
        <span>{{ statusMessage }}</span>
      </p>
      <p v-if="recordsLoadError" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ recordsLoadError }}</span>
      </p>

      <AppTabs
        v-model="abaAtiva"
        :tabs="abas"
        label="Seções de atendimento veterinário"
        id-base="veterinario"
      />

      <!-- ABA ATENDIMENTOS -->
      <div
        v-if="abaAtiva === 'atendimentos'"
        id="veterinario-panel-atendimentos"
        role="tabpanel"
        aria-labelledby="veterinario-tab-atendimentos"
      >
        <RegistryCard
          titulo="Consultas registradas"
          descricao="Os atendimentos lançados aqui ficam visíveis também na ficha de cada animal."
          :total="enrichedRecords.length"
          :carregando="loading"
          texto-carregando="Carregando histórico veterinário..."
          :vazio="enrichedRecords.length === 0"
          icone-vazio="stethoscope"
          titulo-vazio="Nenhuma consulta registrada"
          descricao-vazia="Os atendimentos lançados aqui aparecem também na ficha do animal."
          rotulo-acao-vazio="Cadastrar novo atendimento"
          @cadastrar="abrirModalCadastro"
        >
          <div class="table-wrap">
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
                <tr v-for="record in enrichedRecords" :key="record.id">
                  <td class="mono nowrap">{{ formatDate(record.consultation_date) }}</td>
                  <td class="cell-strong truncate" :title="record.animalName">
                    {{ record.animalName }}
                  </td>
                  <td class="mono nowrap">{{ record.animalRegister ? `#${record.animalRegister}` : '—' }}</td>
                  <td class="truncate" :title="record.veterinarian || 'Não informado'">
                    {{ record.veterinarian || '—' }}
                  </td>
                  <td class="truncate" :title="record.consultation_reason || '—'">
                    {{ record.consultation_reason || '—' }}
                  </td>
                  <td class="truncate" :title="record.consultation_solution || '—'">
                    {{ record.consultation_solution || '—' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </RegistryCard>
      </div>

      <!-- ABA PESQUISAR -->
      <div
        v-else
        id="veterinario-panel-pesquisar"
        role="tabpanel"
        aria-labelledby="veterinario-tab-pesquisar"
        class="stack"
      >
        <section class="card vet-search-card" aria-label="Filtros de pesquisa de atendimentos">
          <div class="card__body grid grid--2 vet-search-grid">
            <div class="field">
              <label class="field__label" for="vet-filtro-animal">Animal</label>
              <select id="vet-filtro-animal" v-model="filtroAnimal" class="select" :disabled="loadingAnimals">
                <option value="">{{ loadingAnimals ? 'Carregando animais...' : 'Selecione um animal...' }}</option>
                <option v-for="animal in animalsList" :key="animal.id" :value="String(animal.id)">
                  {{ animal.name || 'Sem nome' }} — #{{ animal.register_number }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="vet-filtro-motivo">Motivo</label>
              <select id="vet-filtro-motivo" v-model="filtroMotivo" class="select">
                <option value="">Selecione um motivo...</option>
                <option v-for="motivo in motivosDisponiveis" :key="motivo" :value="motivo">
                  {{ motivo }}
                </option>
              </select>
            </div>

            <div class="field">
              <label class="field__label" for="vet-busca-veterinario">Veterinário</label>
              <label class="search">
                <AppIcon name="search" :size="16" />
                <input
                  id="vet-busca-veterinario"
                  v-model="filtroVeterinario"
                  class="input"
                  type="search"
                  placeholder="Digite o nome do veterinário"
                  aria-label="Buscar por nome do veterinário"
                >
              </label>
            </div>

            <div class="grid grid--2">
              <div class="field">
                <label class="field__label" for="vet-data-inicio">Período — De</label>
                <input id="vet-data-inicio" v-model="filtroDataInicio" class="input" type="date">
              </div>

              <div class="field">
                <label class="field__label" for="vet-data-fim">Período — Até</label>
                <input id="vet-data-fim" v-model="filtroDataFim" class="input" type="date">
              </div>
            </div>
          </div>

          <footer class="card__foot vet-search-foot">
            <span class="vet-search-count">
              <template v-if="temFiltrosAtivos">
                {{ resultadosPesquisa.length }} {{ resultadosPesquisa.length === 1 ? 'resultado encontrado' : 'resultados encontrados' }}
              </template>
              <template v-else>
                Escolha um animal, motivo, período ou digite o nome do veterinário para pesquisar.
              </template>
            </span>
            <button
              type="button"
              class="btn"
              :disabled="!temFiltrosAtivos"
              @click="limparFiltros"
            >
              Limpar filtros
            </button>
          </footer>
        </section>

        <RegistryCard
          v-if="temFiltrosAtivos"
          titulo="Resultados da pesquisa"
          :total="resultadosPesquisa.length"
          :carregando="loading"
          texto-carregando="Carregando histórico veterinário..."
          :vazio="resultadosPesquisa.length === 0"
          icone-vazio="search"
          titulo-vazio="Nenhum atendimento encontrado"
          descricao-vazia="Nenhum atendimento corresponde aos filtros informados."
        >
          <template #acao-vazio>
            <button type="button" class="btn" @click="limparFiltros">
              Limpar filtros
            </button>
          </template>

          <div class="table-wrap">
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
                <tr v-for="record in resultadosPesquisa" :key="record.id">
                  <td class="mono nowrap">{{ formatDate(record.consultation_date) }}</td>
                  <td class="cell-strong truncate" :title="record.animalName">
                    {{ record.animalName }}
                  </td>
                  <td class="mono nowrap">{{ record.animalRegister ? `#${record.animalRegister}` : '—' }}</td>
                  <td class="truncate" :title="record.veterinarian || 'Não informado'">
                    {{ record.veterinarian || '—' }}
                  </td>
                  <td class="truncate" :title="record.consultation_reason || '—'">
                    {{ record.consultation_reason || '—' }}
                  </td>
                  <td class="truncate" :title="record.consultation_solution || '—'">
                    {{ record.consultation_solution || '—' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </RegistryCard>
      </div>

      <!-- Modal de Cadastro de Atendimento -->
      <AppModal
        v-if="showModal"
        titulo="Cadastrar novo atendimento"
        largo
        @fechar="fecharModalCadastro"
      >
        <form id="form-atendimento-vet" class="grid grid--2" @submit.prevent="submitRecord">
          <div class="field span-full">
            <label class="field__label" for="vet-animal">Animal *</label>
            <select
              id="vet-animal"
              v-model="formData.animal"
              class="select"
              required
              :disabled="loadingAnimals || !animalsList.length"
            >
              <option value="" disabled>{{ loadingAnimals ? 'Carregando animais...' : 'Selecione um animal...' }}</option>
              <option v-for="animal in animalsList" :key="animal.id" :value="animal.id">
                {{ animal.name || 'Sem nome' }} — #{{ animal.register_number }}
              </option>
            </select>
            <span v-if="animalsLoadError" class="field__error" role="alert">{{ animalsLoadError }}</span>
          </div>

          <div class="field">
            <label class="field__label" for="vet-nome">Veterinário *</label>
            <input
              id="vet-nome"
              v-model.trim="formData.veterinarian"
              class="input"
              type="text"
              maxlength="150"
              placeholder="Nome do responsável"
              required
            >
          </div>

          <div class="field">
            <label class="field__label" for="vet-data">Data da consulta *</label>
            <input
              id="vet-data"
              v-model="formData.consultation_date"
              class="input"
              type="date"
              required
            >
          </div>

          <div v-if="occurrences.length > 0" class="field span-full">
            <label class="field__label" for="vet-motivo">Motivo da consulta *</label>
            <select
              id="vet-motivo"
              v-model="formData.occurrence"
              class="select"
              required
              :disabled="loadingOccurrences"
            >
              <option value="" disabled>
                {{ loadingOccurrences ? 'Carregando motivos...' : 'Selecione um motivo...' }}
              </option>
              <option v-for="item in occurrences" :key="item.id" :value="item.id">
                {{ item.description }}
              </option>
            </select>
            <span v-if="occurrencesError" class="field__error" role="alert">{{ occurrencesError }}</span>
          </div>

          <div v-else class="field span-full">
            <label class="field__label" for="vet-motivo-texto">Motivo da consulta *</label>
            <input
              id="vet-motivo-texto"
              v-model.trim="formData.consultation_reason"
              class="input"
              type="text"
              placeholder="Descreva o motivo do atendimento"
              required
            >
            <span v-if="occurrencesError" class="field__hint">{{ occurrencesError }}</span>
          </div>

          <div class="field span-full">
            <label class="field__label" for="vet-solucao">Tratativa e acompanhamento *</label>
            <textarea
              id="vet-solucao"
              v-model.trim="formData.consultation_solution"
              class="textarea"
              rows="4"
              placeholder="Tratamento aplicado, medicação e acompanhamento previsto"
              required
            ></textarea>
          </div>

          <p v-if="modalError" class="span-full alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ modalError }}</span>
          </p>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="fecharModalCadastro">Cancelar</button>
          <button
            type="submit"
            form="form-atendimento-vet"
            class="btn btn--primary"
            :disabled="saving || loadingAnimals || loadingOccurrences || !animalsList.length"
          >
            {{ saving ? 'Salvando...' : loadingAnimals || loadingOccurrences ? 'Carregando opções...' : 'Registrar consulta' }}
          </button>
        </template>
      </AppModal>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';
import { painelDoPapel } from '@/services/auth';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppModal from '@/components/ui/AppModal.vue';
import AppTabs from '@/components/ui/AppTabs.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import RegistryCard from '@/components/layout/RegistryCard.vue';
import { idRelacao } from '@/utils/animalMovementUtils';
import { apiErrorMessage } from '@/utils/apiError';

const painel = computed(() => painelDoPapel());

const abaAtiva = ref('atendimentos');
const showModal = ref(false);
const loading = ref(true);
const saving = ref(false);
const loadingAnimals = ref(true);
const loadingOccurrences = ref(true);
const animalsList = ref([]);
const records = ref([]);
const occurrences = ref([]);
const statusMessage = ref('');
const modalError = ref('');
const animalsLoadError = ref('');
const recordsLoadError = ref('');
const occurrencesError = ref('');

// Filtros da aba Pesquisar
const filtroAnimal = ref('');
const filtroVeterinario = ref('');
const filtroDataInicio = ref('');
const filtroDataFim = ref('');
const filtroMotivo = ref('');

function todayIso() {
  const date = new Date();
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

const emptyForm = () => ({
  animal: '',
  veterinarian: '',
  consultation_date: todayIso(),
  occurrence: '',
  consultation_reason: '',
  consultation_solution: '',
});

const formData = ref(emptyForm());

const animalsById = computed(() => new Map(
  animalsList.value.map((animal) => [String(animal.id), animal])
));

const enrichedRecords = computed(() =>
  records.value.map((record) => {
    const animalId = idRelacao(record.animal);
    const animal = animalsById.value.get(String(animalId));
    return {
      ...record,
      animalName: record.animal_name || animal?.name || 'Sem nome',
      animalRegister: record.animal_register ?? animal?.register_number ?? '',
    };
  })
);

const abas = computed(() => [
  { id: 'atendimentos', label: 'Atendimentos', icon: 'stethoscope', count: enrichedRecords.value.length },
  { id: 'pesquisar', label: 'Pesquisar', icon: 'search' },
]);

const motivosDisponiveis = computed(() => {
  const set = new Set();
  for (const occ of occurrences.value) {
    if (occ?.description) set.add(occ.description);
  }
  for (const rec of enrichedRecords.value) {
    if (rec?.consultation_reason) set.add(rec.consultation_reason);
  }
  return [...set].sort((a, b) => a.localeCompare(b, 'pt-BR'));
});

const temFiltrosAtivos = computed(() => Boolean(
  filtroAnimal.value
  || filtroVeterinario.value.trim()
  || filtroDataInicio.value
  || filtroDataFim.value
  || filtroMotivo.value
));

const resultadosPesquisa = computed(() => {
  if (!temFiltrosAtivos.value) return [];
  const termoVet = filtroVeterinario.value.trim().toLowerCase();

  return enrichedRecords.value.filter((record) => {
    const animalId = String(idRelacao(record.animal) ?? '');
    if (filtroAnimal.value && animalId !== filtroAnimal.value) return false;
    const dataIso = String(record.consultation_date || '').slice(0, 10);
    if (filtroDataInicio.value && (!dataIso || dataIso < filtroDataInicio.value)) return false;
    if (filtroDataFim.value && (!dataIso || dataIso > filtroDataFim.value)) return false;
    if (filtroMotivo.value && String(record.consultation_reason || '') !== filtroMotivo.value) return false;
    if (termoVet && !String(record.veterinarian || '').toLowerCase().includes(termoVet)) return false;
    return true;
  });
});

const limparFiltros = () => {
  filtroAnimal.value = '';
  filtroVeterinario.value = '';
  filtroDataInicio.value = '';
  filtroDataFim.value = '';
  filtroMotivo.value = '';
};

const abrirModalCadastro = () => {
  formData.value = emptyForm();
  modalError.value = '';
  showModal.value = true;
};

const fecharModalCadastro = () => {
  showModal.value = false;
  modalError.value = '';
};

const loadAnimals = async () => {
  loadingAnimals.value = true;
  animalsLoadError.value = '';
  try {
    const response = await api.getAnimals();
    animalsList.value = response.data.results || response.data;
  } catch (error) {
    console.error('Erro ao carregar animais:', error);
    animalsList.value = [];
    animalsLoadError.value = apiErrorMessage(error, 'Não foi possível carregar os animais.');
  } finally {
    loadingAnimals.value = false;
  }
};

const loadRecords = async () => {
  loading.value = true;
  recordsLoadError.value = '';
  try {
    const response = await api.getVeterinaryRecords();
    records.value = response.data.results || response.data;
  } catch (error) {
    console.error('Erro ao carregar registros veterinários:', error);
    records.value = [];
    recordsLoadError.value = apiErrorMessage(error, 'Não foi possível carregar o histórico veterinário.');
  } finally {
    loading.value = false;
  }
};

const loadOccurrences = async () => {
  loadingOccurrences.value = true;
  occurrencesError.value = '';
  try {
    const response = await api.get('veterinary_occurrences/');
    occurrences.value = response.data.results || response.data;
  } catch (error) {
    console.error('Erro ao carregar motivos veterinários:', error);
    occurrences.value = [];
    occurrencesError.value = apiErrorMessage(error, 'Não foi possível carregar os motivos veterinários.');
  } finally {
    loadingOccurrences.value = false;
  }
};

const submitRecord = async () => {
  const occurrence = occurrences.value.find((item) => String(item.id) === String(formData.value.occurrence));
  const reason = occurrence ? occurrence.description : formData.value.consultation_reason.trim();
  if (!reason) {
    modalError.value = 'Informe o motivo da consulta.';
    return;
  }

  saving.value = true;
  modalError.value = '';
  try {
    const payload = {
      animal: Number(formData.value.animal),
      veterinarian: formData.value.veterinarian.trim(),
      consultation_date: formData.value.consultation_date,
      consultation_reason: reason,
      consultation_solution: formData.value.consultation_solution.trim(),
      ...(occurrence ? { occurrence: occurrence.id } : {}),
    };
    await api.createVeterinaryRecord(payload);
    fecharModalCadastro();
    statusMessage.value = 'Atendimento veterinário registrado com sucesso.';
    setTimeout(() => { statusMessage.value = ''; }, 5000);
    await loadRecords();
  } catch (error) {
    console.error('Erro ao salvar registro:', error);
    modalError.value = apiErrorMessage(error, 'Não foi possível registrar o atendimento veterinário.');
  } finally {
    saving.value = false;
  }
};

const formatDate = (value) => {
  if (!value) return '—';
  const iso = String(value).slice(0, 10);
  const parsed = new Date(`${iso}T00:00:00`);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleDateString('pt-BR');
};

onMounted(async () => {
  await Promise.all([loadAnimals(), loadRecords(), loadOccurrences()]);
});
</script>

<style scoped>
.vet-search-foot {
  justify-content: space-between;
}

.vet-search-count {
  color: var(--text-2);
  font-size: var(--fs-sm);
  font-weight: 500;
}
</style>
