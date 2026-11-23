<template>
  <AppShell>
    <div class="page page--wide analysis">
      <PageHeader
        titulo="Análise reprodutiva e IA"
        descricao="Valide o cruzamento e consulte os resultados e alertas de parentesco."
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
              <h2 class="card__title">Solicitar análise do cruzamento</h2>
              <p class="card__desc">Selecione a matriz e o touro para validar a genealogia registrada.</p>
            </div>
          </header>
          <form class="card__body stack" @submit.prevent="solicitarAnalise">
            <div class="grid grid--2">
              <div class="field">
                <label class="field__label" for="analysis-cow">Matriz (vaca)</label>
                <select id="analysis-cow" v-model="cowId" class="select" required :disabled="loading || analysisLoading || !animals.length">
                  <option value="">Selecione uma matriz...</option>
                  <option v-for="animal in animals" :key="animal.id" :value="String(animal.id)">
                    {{ animal.name || 'Sem nome' }} · #{{ animal.register_number }}
                  </option>
                </select>
              </div>
              <div class="field">
                <label class="field__label" for="analysis-bull">Touro</label>
                <select id="analysis-bull" v-model="bullId" class="select" required :disabled="loading || analysisLoading || !bulls.length">
                  <option value="">Selecione um touro...</option>
                  <option v-for="bull in bulls" :key="bull.id" :value="String(bull.id)">
                    {{ bull.name || 'Sem nome' }} · #{{ bull.register_number }}
                  </option>
                </select>
              </div>
              <div class="field span-full">
                <label class="field__label" for="analysis-notes">Observações (opcional)</label>
                <textarea
                  id="analysis-notes"
                  v-model.trim="observacoes"
                  class="textarea"
                  rows="3"
                  maxlength="500"
                  placeholder="Inclua informações adicionais para a análise"
                  :disabled="analysisLoading"
                ></textarea>
              </div>
            </div>
            <p class="alert alert--info" role="status">
              <AppIcon name="info" :size="16" />
              <span>A rota consulta os IDs da matriz e do touro, recupera a genealogia e envia os dados ao serviço de IA configurado para produzir o parecer.</span>
            </p>
            <div class="row row--between analysis__actions">
              <span v-if="loading" class="text-muted" role="status">Carregando matrizes e touros...</span>
              <span v-else class="text-muted">{{ animals.length }} matrizes · {{ bulls.length }} touros disponíveis</span>
              <button
                type="submit"
                class="btn btn--primary"
                :disabled="loading || analysisLoading || !animals.length || !bulls.length || !cowId || !bullId"
              >
                {{ analysisLoading ? 'Analisando cruzamento...' : 'Solicitar análise' }}
              </button>
            </div>
          </form>
        </section>
      </div>

      <div
        v-else
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
                  <h2 class="card__title">Resultado da validação</h2>
                  <p class="card__desc">Parecer genealógico e zootécnico do último cruzamento analisado.</p>
                </div>
              </div>
            </header>
            <div v-if="!analiseAtual" class="empty">
              <AppIcon name="chart" :size="28" />
              <p class="empty__title">Nenhuma análise disponível</p>
              <p class="empty__desc">Solicite uma análise para consultar o resultado.</p>
            </div>
            <div v-else class="card__body stack">
              <p
                class="alert"
                :class="analiseFalhou ? 'alert--danger' : analiseAtual.resultado.apto ? 'alert--ok' : 'alert--warn'"
                role="status"
              >
                <AppIcon :name="analiseFalhou ? 'alert' : analiseAtual.resultado.apto ? 'check-circle' : 'alert'" :size="16" />
                <span>
                  <strong>{{ analiseFalhou ? 'Análise não concluída' : analiseAtual.resultado.apto ? 'Cruzamento aprovado' : 'Cruzamento não aprovado' }}</strong>
                  · {{ analiseAtual.resultado.status || 'Status não informado' }}
                </span>
              </p>
              <div class="analysis__facts">
                <p><strong>Matriz:</strong> {{ analiseAtual.matriz }}</p>
                <p><strong>Touro:</strong> {{ analiseAtual.touro }}</p>
                <p><strong>Risco:</strong> {{ analiseAtual.resultado.nivel_risco_consanguinidade || 'Não informado' }}</p>
                <p><strong>Grau detectado:</strong> {{ analiseAtual.resultado.geracao_parentesco_detectada ?? 'Nenhum' }}</p>
              </div>
              <div v-if="analiseAtual.resultado.analise_genealogica">
                <h3 class="analysis__section-title">Análise genealógica</h3>
                <p>{{ analiseAtual.resultado.analise_genealogica }}</p>
              </div>
              <div v-if="analiseAtual.resultado.analise_zootecnica_complementar">
                <h3 class="analysis__section-title">Análise zootécnica</h3>
                <p>{{ analiseAtual.resultado.analise_zootecnica_complementar }}</p>
              </div>
              <p v-if="analiseAtual.resultado.veredito_final" class="analysis__verdict">
                {{ analiseAtual.resultado.veredito_final }}
              </p>
            </div>
          </article>

          <article class="card">
            <header class="card__head">
              <div class="analysis__title">
                <span class="icon-tile icon-tile--warn"><AppIcon name="dna" :size="17" /></span>
                <div>
                  <h2 class="card__title">Alertas de parentesco</h2>
                  <p class="card__desc">Ancestrais compartilhados encontrados na consulta mais recente.</p>
                </div>
              </div>
            </header>
            <div v-if="!analiseAtual" class="empty">
              <AppIcon name="dna" :size="28" />
              <p class="empty__desc">Os alertas serão exibidos após a análise de um cruzamento.</p>
            </div>
            <div v-else-if="analiseFalhou" class="empty">
              <AppIcon name="alert" :size="28" />
              <p class="empty__desc">Não foi possível gerar alertas porque a análise não foi concluída.</p>
            </div>
            <div v-else-if="ancestraisComuns.length" class="card__body stack">
              <ul class="analysis__ancestors">
                <li v-for="(ancestor, index) in ancestraisComuns" :key="ancestor.id || index">
                  <strong>{{ ancestor.nome || `Ancestral #${ancestor.id}` }}</strong>
                  <span>{{ ancestor.parentesco_na_femea || 'Parentesco da matriz não informado' }}</span>
                  <span>{{ ancestor.parentesco_no_macho || 'Parentesco do touro não informado' }}</span>
                </li>
              </ul>
            </div>
            <div v-else class="empty">
              <AppIcon name="check-circle" :size="28" />
              <p class="empty__desc">A análise não identificou ancestrais comuns.</p>
            </div>
          </article>
        </section>

        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Histórico de análises</h2>
              <p class="card__desc">Consultas realizadas nesta sessão.</p>
            </div>
            <span class="badge">{{ analises.length }}</span>
          </header>
          <div v-if="!analises.length" class="empty">
            <AppIcon name="clipboard" :size="28" />
            <p class="empty__desc">As análises solicitadas aparecerão aqui.</p>
          </div>
          <div v-else class="table-wrap">
            <table class="table">
              <thead>
                <tr><th>Data</th><th>Matriz</th><th>Touro</th><th>Status</th><th>Risco</th></tr>
              </thead>
              <tbody>
                <tr v-for="analise in analises" :key="analise.id">
                  <td class="mono nowrap">{{ formatDate(analise.data) }}</td>
                  <td>{{ analise.matriz }}</td>
                  <td>{{ analise.touro }}</td>
                  <td>{{ analise.resultado.status || (analise.resultado.apto ? 'APROVADO' : 'NÃO APROVADO') }}</td>
                  <td>{{ analise.resultado.nivel_risco_consanguinidade || '—' }}</td>
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
const bulls = ref([]);
const cowId = ref('');
const bullId = ref('');
const observacoes = ref('');
const aba = ref('nova');
const loading = ref(true);
const analysisLoading = ref(false);
const error = ref('');
const analises = ref([]);
const abas = [
  { id: 'nova', label: 'Nova análise', icon: 'sparkle' },
  { id: 'resultados', label: 'Resultados, alertas e histórico', icon: 'chart' },
];
const analiseAtual = computed(() => analises.value[0] || null);
const ancestraisComuns = computed(() => analiseAtual.value?.resultado?.ancestrais_comuns || []);
const analiseFalhou = computed(() => [
  'ERRO_CONFIGURACAO',
  'ERRO_PROCESSAMENTO_IA',
  'ERRO_PARAMETROS',
  'RESPOSTA_NAO_ESTRUTURADA',
].includes(analiseAtual.value?.resultado?.status));

function listFromResponse(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  throw new Error('A API retornou um formato de lista inesperado.');
}

function animalLabel(animal) {
  return `${animal.name || 'Sem nome'} · #${animal.register_number}`;
}

function formatDate(value) {
  return new Date(value).toLocaleString('pt-BR');
}

async function loadAnimals() {
  loading.value = true;
  error.value = '';
  try {
    const [animalsResponse, bullsResponse] = await Promise.all([
      api.getAnimals(),
      api.get('bulls/'),
    ]);
    animals.value = listFromResponse(animalsResponse.data);
    bulls.value = listFromResponse(bullsResponse.data);
  } catch (loadError) {
    console.error('Erro ao carregar animais e touros para análise reprodutiva:', loadError);
    error.value = apiErrorMessage(loadError, 'Não foi possível carregar matrizes e touros.');
  } finally {
    loading.value = false;
  }
}

async function solicitarAnalise() {
  if (analysisLoading.value || !cowId.value || !bullId.value) return;
  analysisLoading.value = true;
  error.value = '';
  try {
    const response = await api.post('api/reproducao/validar-genealogia/', {
      cow_id: Number(cowId.value),
      bull_id: Number(bullId.value),
      observacoes: observacoes.value,
    });
    if (!response.data || typeof response.data !== 'object') {
      throw new Error('A API retornou um resultado de análise inválido.');
    }
    const matriz = animals.value.find((animal) => String(animal.id) === cowId.value);
    const touro = bulls.value.find((bull) => String(bull.id) === bullId.value);
    analises.value.unshift({
      id: `${Date.now()}-${cowId.value}-${bullId.value}`,
      data: new Date().toISOString(),
      matriz: matriz ? animalLabel(matriz) : `Matriz #${cowId.value}`,
      touro: touro ? animalLabel(touro) : `Touro #${bullId.value}`,
      resultado: response.data,
    });
    aba.value = 'resultados';
  } catch (analysisError) {
    console.error('Erro ao solicitar análise reprodutiva:', analysisError);
    error.value = apiErrorMessage(analysisError, 'Não foi possível concluir a análise do cruzamento.');
  } finally {
    analysisLoading.value = false;
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
.analysis__facts { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px 18px; }
.analysis__facts p { margin: 0; }
.analysis__section-title { margin: 0 0 6px; font-size: var(--fs-sm); }
.analysis__verdict { padding: 12px; border-radius: var(--r); background: var(--surface-2); }
.analysis__ancestors { display: grid; gap: 12px; margin: 0; padding-left: 20px; }
.analysis__ancestors li { display: grid; gap: 4px; }

@media (max-width: 760px) {
  .analysis__grid,
  .analysis__facts { grid-template-columns: 1fr; }
}
</style>
