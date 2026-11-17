<template>
  <AppShell>
    <div class="page page--wide analysis">
      <PageHeader
        titulo="Análise reprodutiva e IA"
        descricao="Previsões de desempenho, alertas de parentesco e histórico das análises."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <p v-if="error" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ error }}</span>
      </p>

      <AppTabs v-model="aba" id-base="ia" label="Análise reprodutiva" :tabs="abas" />

      <div
        v-if="aba === 'nova'"
        id="ia-panel-nova"
        class="analysis__panel"
        role="tabpanel"
        aria-labelledby="ia-tab-nova"
      >
      <section class="card">
        <header class="card__head">
          <div>
            <h2 class="card__title">Solicitar análise</h2>
            <p class="card__desc">Escolha um animal e um período para preparar a consulta.</p>
          </div>
          <span class="badge badge--info">Em breve</span>
        </header>
        <div class="card__body stack">
          <div class="grid grid--3">
            <div class="field">
              <label class="field__label" for="analysis-animal">Animal</label>
              <select id="analysis-animal" v-model="animalId" class="select" :disabled="loading || !animals.length">
                <option value="">Selecione um animal...</option>
                <option v-for="animal in animals" :key="animal.id" :value="String(animal.id)">
                  {{ animal.name || 'Sem nome' }} · #{{ animal.register_number }}
                </option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="analysis-start">Início do período</label>
              <input id="analysis-start" v-model="period.start" class="input" type="date">
            </div>
            <div class="field">
              <label class="field__label" for="analysis-end">Fim do período</label>
              <input id="analysis-end" v-model="period.end" class="input" type="date">
            </div>
          </div>
          <p class="alert alert--info" role="status">
            <AppIcon name="info" :size="16" />
            <span>As análises por IA serão liberadas em breve. Até lá, nenhuma previsão é exibida.</span>
          </p>
          <div class="row row--between analysis__actions">
            <span v-if="loading" class="text-muted" role="status">Carregando animais...</span>
            <span v-else class="text-muted">{{ animals.length }} animais disponíveis</span>
            <button type="button" class="btn btn--primary" disabled>Solicitar análise</button>
          </div>
        </div>
      </section>
      </div>

      <div
        v-else-if="aba === 'resultados'"
        id="ia-panel-resultados"
        class="analysis__panel"
        role="tabpanel"
        aria-labelledby="ia-tab-resultados"
      >
      <section class="analysis__grid">
        <article class="card">
          <header class="card__head">
            <div class="analysis__title">
              <span class="icon-tile icon-tile--accent"><AppIcon name="chart" :size="17" /></span>
              <div>
                <h2 class="card__title">Desempenho e risco reprodutivo</h2>
                <p class="card__desc">Resultado acompanhado de explicação e origem dos dados.</p>
              </div>
            </div>
          </header>
          <div class="empty">
            <AppIcon name="chart" :size="28" />
            <p class="empty__title">Nenhuma análise disponível</p>
            <p class="empty__desc">Os resultados aparecerão aqui, sempre acompanhados da explicação.</p>
          </div>
        </article>

        <article class="card">
          <header class="card__head">
            <div class="analysis__title">
              <span class="icon-tile icon-tile--warn"><AppIcon name="dna" :size="17" /></span>
              <div>
                <h2 class="card__title">Alertas de parentesco</h2>
                <p class="card__desc">A avaliação de cruzamentos precisa considerar a árvore genealógica.</p>
              </div>
            </div>
          </header>
          <div class="empty">
            <AppIcon name="dna" :size="28" />
            <p class="empty__title">Alertas em breve</p>
            <p class="empty__desc">Ascendência não registrada nunca será tratada como cruzamento seguro.</p>
          </div>
        </article>
      </section>
      </div>

      <div
        v-else
        id="ia-panel-historico"
        class="analysis__panel"
        role="tabpanel"
        aria-labelledby="ia-tab-historico"
      >
      <section class="analysis__grid">
        <article class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Histórico de análises</h2>
              <p class="card__desc">Consultas anteriores, data e estado do processamento.</p>
            </div>
          </header>
          <div class="empty">
            <AppIcon name="clipboard" :size="28" />
            <p class="empty__title">Nenhuma consulta ainda</p>
            <p class="empty__desc">As análises solicitadas aparecerão aqui, com data e situação.</p>
          </div>
        </article>

        <article class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Sugestão de layout de exportação</h2>
              <p class="card__desc">Descreva os campos desejados e revise a sugestão antes de aplicar.</p>
            </div>
            <span class="badge badge--info">Em breve</span>
          </header>
          <div class="card__body stack">
            <div class="field">
              <label class="field__label" for="layout-prompt">Como deseja organizar o arquivo?</label>
              <textarea
                id="layout-prompt"
                v-model="layoutPrompt"
                class="textarea"
                rows="3"
                maxlength="500"
                placeholder="Ex.: identificação, peso atual e histórico de vacinação"
              ></textarea>
              <span class="field__hint">{{ layoutPrompt.length }}/500 caracteres</span>
            </div>
            <p class="text-muted">A sugestão não será aplicada nem salva sem revisão e confirmação.</p>
            <button type="button" class="btn" disabled>Gerar sugestão</button>
          </div>
        </article>
      </section>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppTabs from '@/components/ui/AppTabs.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { painelDoPapel } from '@/services/auth';
import { apiErrorMessage } from '@/utils/apiError';

const painel = computed(() => painelDoPapel());
const animals = ref([]);
const animalId = ref('');
const aba = ref('nova');
const abas = [
  { id: 'nova', label: 'Nova análise', icon: 'sparkle' },
  { id: 'resultados', label: 'Resultados e alertas', icon: 'chart' },
  { id: 'historico', label: 'Histórico e exportação', icon: 'clipboard' },
];
const loading = ref(true);
const error = ref('');
const period = ref({ start: '', end: '' });
const layoutPrompt = ref('');

async function loadAnimals() {
  loading.value = true;
  error.value = '';
  try {
    const response = await api.getAnimals();
    animals.value = Array.isArray(response.data) ? response.data : response.data?.results || [];
  } catch (loadError) {
    console.error('Erro ao carregar animais para análise reprodutiva:', loadError);
    error.value = apiErrorMessage(loadError, 'Não foi possível carregar os animais.');
  } finally {
    loading.value = false;
  }
}

onMounted(loadAnimals);
</script>

<style scoped>
.analysis { display: grid; gap: 18px; }
.analysis__panel { display: grid; gap: 16px; }
.analysis__grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
.analysis__title { display: flex; align-items: center; gap: 12px; }
.analysis__actions { flex-wrap: wrap; }

@media (max-width: 760px) {
  .analysis__grid { grid-template-columns: 1fr; }
}
</style>
