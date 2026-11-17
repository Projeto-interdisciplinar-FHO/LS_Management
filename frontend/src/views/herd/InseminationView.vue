<template>
  <AppShell>
    <div class="page page--wide insemination-page">
      <PageHeader
        titulo="Inseminações"
        descricao="Registre o acasalamento e acompanhe o histórico reprodutivo do rebanho."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <p v-if="error" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ error }}</span>
      </p>
      <p v-if="notice" class="alert alert--ok" role="status">
        <AppIcon name="check-circle" :size="16" />
        <span>{{ notice }}</span>
      </p>

      <AppTabs v-model="aba" id-base="insem" label="Reprodução" :tabs="abas" />

      <div
        v-if="aba === 'registro'"
        id="insem-panel-registro"
        class="insemination__panel"
        role="tabpanel"
        aria-labelledby="insem-tab-registro"
      >
      <section class="card">
        <header class="card__head">
          <div class="insemination__heading">
            <span class="icon-tile icon-tile--info"><AppIcon name="dna" :size="18" /></span>
            <div>
              <h2 class="card__title">Registrar inseminação</h2>
              <p class="card__desc">Informe a matriz, o touro e a data do procedimento.</p>
            </div>
          </div>
          <span class="badge">{{ inseminations.length }} registros</span>
        </header>

        <form class="card__body stack" @submit.prevent="saveInsemination">
          <div v-if="!loading && (!animals.length || !bulls.length)" class="alert alert--warn" role="status">
            <AppIcon name="info" :size="16" />
            <span>
              {{ !animals.length ? 'Cadastre animais antes de lançar uma inseminação.' : 'Cadastre touros antes de lançar uma inseminação.' }}
            </span>
          </div>

          <div class="field">
            <label class="field__label" for="procedure-type">Tipo de procedimento</label>
            <select id="procedure-type" v-model="procedureType" class="select" :disabled="loading || saving">
              <option value="insemination">Inseminação artificial</option>
              <option value="embryo-transfer">Transplante de embrião</option>
            </select>
          </div>

          <div v-if="procedureType === 'embryo-transfer'" class="alert alert--info" role="status">
            <AppIcon name="info" :size="16" />
            <span>O formulário de transplante está preparado, mas a API atual só aceita inseminação artificial. Nenhum procedimento será enviado por esta opção.</span>
          </div>

          <div class="grid grid--3">
            <div class="field">
              <label class="field__label" for="insemination-mother">Matriz</label>
              <select id="insemination-mother" v-model.number="form.mother" class="select" required :disabled="loading || saving || !animals.length">
                <option value="" disabled>Selecione a matriz...</option>
                <option v-for="animal in animals" :key="animal.id" :value="animal.id">
                  {{ animal.name || 'Sem nome' }} · #{{ animal.register_number }}
                </option>
              </select>
            </div>
            <div v-if="procedureType === 'embryo-transfer'" class="field">
              <label class="field__label" for="insemination-donor">Doadora do embrião</label>
              <select id="insemination-donor" v-model="donorId" class="select" :disabled="loading || saving || !animals.length">
                <option value="" disabled>Selecione a doadora...</option>
                <option v-for="animal in animals" :key="animal.id" :value="String(animal.id)">
                  {{ animal.name || 'Sem nome' }} · #{{ animal.register_number }}
                </option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="insemination-father">
                {{ procedureType === 'embryo-transfer' ? 'Pai genético do embrião' : 'Touro' }}
              </label>
              <select id="insemination-father" v-model.number="form.father" class="select" required :disabled="loading || saving || !bulls.length">
                <option value="" disabled>Selecione o touro...</option>
                <option v-for="bull in bulls" :key="bull.id" :value="bull.id">
                  {{ bull.name }} · #{{ bull.register_number }}
                </option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="insemination-date">{{ procedureType === 'embryo-transfer' ? 'Data do transplante' : 'Data da inseminação' }}</label>
              <input id="insemination-date" v-model="form.date" class="input" type="date" required :disabled="saving">
            </div>
            <div v-if="procedureType === 'embryo-transfer'" class="field span-full">
              <label class="field__label" for="embryo-reference">Identificação do embrião</label>
              <input id="embryo-reference" v-model="embryoReference" class="input" type="text" maxlength="100" placeholder="Opcional">
            </div>
          </div>

          <p class="alert alert--info" role="status">
            <AppIcon name="info" :size="16" />
            <span>A idade mínima de 13 meses e o parentesco são validados pelo servidor. Rejeições da API serão exibidas nesta tela; não há aprovação local.</span>
          </p>

          <footer class="row row--between">
            <span v-if="loading" class="text-muted" role="status">Carregando dados reprodutivos...</span>
            <span v-else class="text-muted">{{ animals.length }} matrizes · {{ bulls.length }} touros disponíveis</span>
            <button type="submit" class="btn btn--primary" :disabled="loading || saving || procedureType !== 'insemination' || !animals.length || !bulls.length">
              {{ saving ? 'Salvando...' : 'Registrar inseminação' }}
            </button>
          </footer>
        </form>
      </section>

      <section class="card insemination__diagnosis">
        <header class="card__head">
          <div>
            <h2 class="card__title">Diagnóstico de prenhez</h2>
            <p class="card__desc">Prepare o lançamento do resultado clínico.</p>
          </div>
          <span class="badge badge--info">Em breve</span>
        </header>
        <form class="card__body stack" @submit.prevent>
          <div class="field">
            <label class="field__label" for="diagnosis-insemination">Inseminação relacionada</label>
            <select id="diagnosis-insemination" ref="diagnosisSelect" v-model="diagnosis.insemination" class="select" :disabled="loading || !inseminations.length">
              <option value="">Selecione uma inseminação...</option>
              <option v-for="item in orderedInseminations" :key="item.id" :value="item.id">
                {{ animalName(item.mother) }} · {{ formatDate(item.date) }}
              </option>
            </select>
          </div>
          <div class="grid grid--2">
            <div class="field">
              <label class="field__label" for="diagnosis-result">Resultado</label>
              <select id="diagnosis-result" v-model="diagnosis.result" class="select">
                <option value="">Selecione...</option>
                <option value="positive">Prenhez confirmada</option>
                <option value="negative">Vazia</option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="diagnosis-date">Data do diagnóstico</label>
              <input id="diagnosis-date" v-model="diagnosis.date" class="input" type="date">
            </div>
          </div>
          <p class="alert alert--info" role="status">
            <AppIcon name="info" :size="16" />
            <span>Disponível em breve. Por enquanto este formulário não altera o status reprodutivo da vaca.</span>
          </p>
          <button type="button" class="btn" disabled>Salvar diagnóstico</button>
          <button type="button" class="btn" disabled>Iniciar nascimento pela prenhez</button>
        </form>
      </section>

      </div>

      <div
        v-else-if="aba === 'ultrassons'"
        id="insem-panel-ultrassons"
        class="insemination__panel"
        role="tabpanel"
        aria-labelledby="insem-tab-ultrassons"
      >
      <section v-if="!loading && inseminations.length" class="grid grid--auto insemination__summary" aria-label="Acompanhamento de ultrassons">
        <article class="stat">
          <span class="stat__label"><AppIcon name="stethoscope" :size="15" />Ultrassons pendentes</span>
          <strong class="stat__value" :class="{ 'insemination__value--warn': resumo.ultrassom }">{{ resumo.ultrassom }}</strong>
          <span class="stat__foot">Inseminadas entre 30 e 90 dias atrás</span>
        </article>
        <article class="stat">
          <span class="stat__label"><AppIcon name="clock" :size="15" />Aguardando prazo</span>
          <strong class="stat__value">{{ resumo.aguardando }}</strong>
          <span class="stat__foot">Inseminadas há menos de 30 dias</span>
        </article>
        <article class="stat">
          <span class="stat__label"><AppIcon name="clipboard" :size="15" />Diagnósticos em atraso</span>
          <strong class="stat__value">{{ resumo.diagnosticoAtrasado }}</strong>
          <span class="stat__foot">Inseminadas há mais de 90 dias, sem confirmação</span>
        </article>
      </section>


      <section class="card insemination__history">
        <header class="card__head">
          <div>
            <h2 class="card__title">Histórico reprodutivo</h2>
            <p class="card__desc">Inseminações cadastradas, da mais recente para a mais antiga.</p>
          </div>
          <span class="badge">{{ inseminations.length }}</span>
        </header>
        <div v-if="loading" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando inseminações...</div>
        <div v-else-if="!inseminations.length" class="empty">
          <AppIcon name="dna" :size="28" />
          <p class="empty__title">Sem inseminações registradas</p>
          <p class="empty__desc">Os lançamentos confirmados aparecerão aqui.</p>
        </div>
        <div v-else class="table-wrap">
          <table class="table">
            <thead>
              <tr><th>Data</th><th>Matriz</th><th>Touro</th><th>Acompanhamento</th><th>Diagnóstico</th><th>Ações</th></tr>
            </thead>
            <tbody>
              <tr v-for="item in orderedInseminations" :key="item.id">
                <td class="mono nowrap">{{ formatDate(item.date) }}</td>
                <td>
                  <RouterLink :to="{ name: 'animal-detail', params: { id: idRelacao(item.mother) } }" class="insemination__animal">
                    {{ animalName(item.mother) }}
                  </RouterLink>
                </td>
                <td>{{ bullName(item.father) }}</td>
                <td>
                  <span v-if="situacao(item)" class="badge" :class="situacao(item).classe">
                    <span class="badge__dot"></span>{{ situacao(item).rotulo }}
                  </span>
                  <span v-else class="text-muted">Anterior</span>
                </td>
                <td class="text-muted">Sem confirmação clínica</td>
                <td>
                  <button type="button" class="btn btn--sm" @click="prepararDiagnostico(item)">
                    Selecionar para diagnóstico
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      </div>

      <div
        v-else
        id="insem-panel-secagem"
        class="insemination__panel"
        role="tabpanel"
        aria-labelledby="insem-tab-secagem"
      >
      <section class="card insemination__drying">
          <header class="card__head">
            <div>
              <h2 class="card__title">Controle de secagem</h2>
              <p class="card__desc">A secagem deve ser vinculada a uma prenhez confirmada.</p>
            </div>
            <span class="badge badge--info">Em breve</span>
          </header>
          <form class="card__body stack" @submit.prevent>
            <div class="field">
              <label class="field__label" for="drying-animal">Matriz</label>
              <select id="drying-animal" v-model="drying.animal" class="select" :disabled="loading || !animals.length">
                <option value="">Selecione uma matriz...</option>
                <option v-for="animal in animals" :key="animal.id" :value="animal.id">
                  {{ animal.name || 'Sem nome' }} · #{{ animal.register_number }}
                </option>
              </select>
            </div>
            <div class="grid grid--2">
              <div class="field">
                <label class="field__label" for="drying-date">Data da secagem</label>
                <input id="drying-date" v-model="drying.date" class="input" type="date">
              </div>
              <div class="field">
                <label class="field__label" for="drying-notes">Observação</label>
                <input id="drying-notes" v-model="drying.notes" class="input" type="text" placeholder="Opcional">
              </div>
            </div>
            <p class="alert alert--info" role="status">
              <AppIcon name="info" :size="16" />
              <span>Disponível em breve. O registro será vinculado à gestação confirmada.</span>
            </p>
            <button type="button" class="btn" disabled>Registrar secagem</button>
          </form>
      </section>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from 'vue';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppTabs from '@/components/ui/AppTabs.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { painelDoPapel } from '@/services/auth';
import { idRelacao } from '@/utils/animalMovementUtils';
import { apiErrorMessage } from '@/utils/apiError';
import {
  situacaoDaInseminacao,
  ultimaInseminacaoPorMatriz,
} from '@/utils/reproducaoUtils';

const painel = computed(() => painelDoPapel());
const animals = ref([]);
const bulls = ref([]);
const inseminations = ref([]);
const aba = ref('registro');
const loading = ref(true);
const saving = ref(false);
const error = ref('');
const notice = ref('');
const form = ref({ mother: '', father: '', date: todayIso() });
const procedureType = ref('insemination');
const donorId = ref('');
const embryoReference = ref('');
const diagnosis = ref({ insemination: '', result: '', date: todayIso() });
const diagnosisSelect = ref(null);
const drying = ref({ animal: '', date: todayIso(), notes: '' });

const orderedInseminations = computed(() =>
  [...inseminations.value].sort((a, b) => String(b.date).localeCompare(String(a.date)))
);

const ultimaPorMatriz = computed(() => ultimaInseminacaoPorMatriz(inseminations.value, idRelacao));

const ROTULOS_SITUACAO = {
  aguardando: { rotulo: 'Aguardando prazo do ultrassom', classe: '' },
  ultrassom: { rotulo: 'Ultrassom pendente', classe: 'badge--warn' },
  'diagnostico-atrasado': { rotulo: 'Diagnóstico pendente', classe: 'badge--warn' },
};

function situacao(item) {
  const matriz = String(idRelacao(item.mother));
  if (ultimaPorMatriz.value.get(matriz)?.id !== item.id) return null;
  const info = situacaoDaInseminacao(item.date);
  if (!info) return null;
  const base = ROTULOS_SITUACAO[info.fase];
  return { info, rotulo: base.rotulo, classe: base.classe };
}

const resumo = computed(() => {
  const totais = { ultrassom: 0, aguardando: 0, diagnosticoAtrasado: 0 };
  for (const item of ultimaPorMatriz.value.values()) {
    const info = situacaoDaInseminacao(item.date);
    if (!info) continue;
    if (info.fase === 'ultrassom') totais.ultrassom += 1;
    if (info.fase === 'aguardando') totais.aguardando += 1;
    if (info.fase === 'diagnostico-atrasado') totais.diagnosticoAtrasado += 1;
  }
  return totais;
});

const abas = computed(() => [
  { id: 'registro', label: 'Registrar e diagnóstico', icon: 'dna' },
  { id: 'ultrassons', label: 'Ultrassons', icon: 'stethoscope', count: resumo.value.ultrassom, warn: true },
  { id: 'secagem', label: 'Secagem', icon: 'calendar' },
]);

async function prepararDiagnostico(item) {
  diagnosis.value.insemination = item.id;
  aba.value = 'registro';
  await nextTick();
  diagnosisSelect.value?.focus();
}

function todayIso() {
  const date = new Date();
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

function listFromResponse(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  throw new Error('A API retornou um formato de lista inesperado.');
}

function formatDate(value) {
  if (!value) return '—';
  return new Date(`${value}T00:00:00`).toLocaleDateString('pt-BR');
}

function animalName(animalRef) {
  const id = idRelacao(animalRef);
  const animal = animals.value.find((item) => String(item.id) === String(id));
  return animal ? `${animal.name || 'Sem nome'} · #${animal.register_number}` : 'Animal';
}

function bullName(bullRef) {
  const id = idRelacao(bullRef);
  const bull = bulls.value.find((item) => String(item.id) === String(id));
  return bull ? `${bull.name} · #${bull.register_number}` : 'Touro';
}

async function loadData() {
  loading.value = true;
  error.value = '';
  try {
    const [animalsResponse, bullsResponse, inseminationsResponse] = await Promise.all([
      api.getAnimals(),
      api.get('bulls/'),
      api.get('inseminations/'),
    ]);
    animals.value = listFromResponse(animalsResponse.data);
    bulls.value = listFromResponse(bullsResponse.data);
    inseminations.value = listFromResponse(inseminationsResponse.data);
  } catch (loadError) {
    console.error('Erro ao carregar dados de inseminação:', loadError);
    error.value = apiErrorMessage(loadError, 'Não foi possível carregar os dados de reprodução.');
  } finally {
    loading.value = false;
  }
}

async function saveInsemination() {
  if (saving.value || procedureType.value !== 'insemination') return;
  saving.value = true;
  error.value = '';
  notice.value = '';
  try {
    const response = await api.post('inseminations/', {
      mother: form.value.mother,
      father: form.value.father,
      date: form.value.date,
    });
    inseminations.value = [response.data, ...inseminations.value];
    notice.value = 'Inseminação registrada com sucesso.';
    form.value = { mother: '', father: '', date: todayIso() };
  } catch (saveError) {
    console.error('Erro ao registrar inseminação:', saveError);
    error.value = apiErrorMessage(saveError, 'Não foi possível registrar a inseminação.');
  } finally {
    saving.value = false;
  }
}

onMounted(loadData);
</script>

<style scoped>
.insemination__heading { display: flex; align-items: center; gap: 12px; }
.insemination__history { margin-top: 20px; }
.insemination__summary { margin-top: 20px; }
.insemination__value--warn { color: var(--warn); }
.insemination__hint { display: block; color: var(--text-3); font-size: var(--fs-xs); font-family: var(--font-sans); }
.insemination__animal { color: var(--text); font-weight: 600; }
.insemination__animal:hover { color: var(--accent); }
.insemination__panel > :first-child { margin-top: 0; }
.insemination__summary .stat__label > svg { color: var(--accent); }
.insemination__summary .stat:nth-child(1) .stat__label > svg { color: var(--warn); }
.insemination__summary .stat:nth-child(3) .stat__label > svg { color: var(--info); }
</style>
