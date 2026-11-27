<template>
  <AppShell>
    <div class="page page--wide repro-ai">
      <PageHeader
        titulo="Análise reprodutiva & IA"
        descricao="Valide a compatibilidade genética entre matrizes e touros com prevenção de consanguinidade até a 3ª geração."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <!-- Faixa de métricas rápidas -->
      <section class="repro-ai__kpis" aria-label="Resumo reprodutivo">
        <article class="repro-kpi">
          <span class="repro-kpi__icon repro-kpi__icon--accent"><AppIcon name="animal" :size="18" /></span>
          <div>
            <span class="repro-kpi__label">Matrizes disponíveis</span>
            <strong class="repro-kpi__value">{{ animals.length }}</strong>
          </div>
        </article>
        <article class="repro-kpi">
          <span class="repro-kpi__icon repro-kpi__icon--info"><AppIcon name="dna" :size="18" /></span>
          <div>
            <span class="repro-kpi__label">Touros reprodutores</span>
            <strong class="repro-kpi__value">{{ bulls.length }}</strong>
          </div>
        </article>
        <article class="repro-kpi">
          <span class="repro-kpi__icon repro-kpi__icon--warn"><AppIcon name="sparkle" :size="18" /></span>
          <div>
            <span class="repro-kpi__label">Análises nesta sessão</span>
            <strong class="repro-kpi__value">{{ analises.length }}</strong>
          </div>
        </article>
      </section>

      <p v-if="error" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ error }}</span>
      </p>

      <AppTabs v-model="aba" id-base="ia" label="Análise reprodutiva" :tabs="abas" />

      <!-- ABA NOVA ANÁLISE -->
      <div
        v-if="aba === 'nova'"
        id="ia-panel-nova"
        class="repro-ai__panel"
        role="tabpanel"
        aria-labelledby="ia-tab-nova"
      >
        <section class="card repro-pairing-card">
          <header class="card__head">
            <div class="repro-head__title">
              <span class="icon-tile icon-tile--accent"><AppIcon name="sparkle" :size="18" /></span>
              <div>
                <h2 class="card__title">Simulador de cruzamento com IA</h2>
                <p class="card__desc">Escolha a matriz e o touro para avaliar parentesco, risco de consanguinidade e recomendação técnica.</p>
              </div>
            </div>
          </header>

          <form class="card__body stack" @submit.prevent="solicitarAnalise">
            <div class="repro-pairing">
              <div class="repro-pairing__box">
                <div class="repro-pairing__badge">
                  <AppIcon name="animal" :size="15" />
                  <span>Matriz (Fêmea)</span>
                </div>
                <div class="field">
                  <label class="field__label" for="analysis-cow">Selecione a vaca</label>
                  <select id="analysis-cow" v-model="cowId" class="select" required :disabled="loading || analysisLoading || !animals.length">
                    <option value="">Selecione uma matriz...</option>
                    <option v-for="animal in animals" :key="animal.id" :value="String(animal.id)">
                      {{ animal.name || 'Sem nome' }} · #{{ animal.register_number }}
                    </option>
                  </select>
                </div>
              </div>

              <div class="repro-pairing__connector" aria-hidden="true">
                <span>×</span>
              </div>

              <div class="repro-pairing__box">
                <div class="repro-pairing__badge repro-pairing__badge--bull">
                  <AppIcon name="dna" :size="15" />
                  <span>Reprodutor (Touro)</span>
                </div>
                <div class="field">
                  <label class="field__label" for="analysis-bull">Selecione o touro</label>
                  <select id="analysis-bull" v-model="bullId" class="select" required :disabled="loading || analysisLoading || !bulls.length">
                    <option value="">Selecione um touro...</option>
                    <option v-for="bull in bulls" :key="bull.id" :value="String(bull.id)">
                      {{ bull.name || 'Sem nome' }} · #{{ bull.register_number }}
                    </option>
                  </select>
                </div>
              </div>
            </div>

            <div class="field">
              <label class="field__label" for="analysis-notes">Observações adicionais (opcional)</label>
              <textarea
                id="analysis-notes"
                v-model.trim="observacoes"
                class="textarea"
                rows="3"
                maxlength="500"
                placeholder="Ex.: objetivo produtivo, histórico de parto ou restrições de manejo"
                :disabled="analysisLoading"
              ></textarea>
            </div>

            <footer class="repro-pairing__foot">
              <span class="repro-pairing__hint">
                <AppIcon name="info" :size="15" />
                <span>A análise cruza a árvore genealógica registrada no sistema com parecer técnico via Gemini IA.</span>
              </span>
              <button
                type="submit"
                class="btn btn--primary btn--lg"
                :disabled="loading || analysisLoading || !animals.length || !bulls.length || !cowId || !bullId"
              >
                <AppIcon name="sparkle" :size="16" />
                {{ analysisLoading ? 'Analisando cruzamento...' : 'Analisar compatibilidade' }}
              </button>
            </footer>
          </form>
        </section>
      </div>

      <!-- ABA RESULTADOS -->
      <div
        v-else
        id="ia-panel-resultados"
        class="repro-ai__panel"
        role="tabpanel"
        aria-labelledby="ia-tab-resultados"
      >
        <section class="repro-results__grid">
          <article
            class="card repro-verdict-card"
            :class="analiseAtual ? (analiseFalhou ? 'is-danger' : analiseAtual.resultado.apto ? 'is-ok' : 'is-warn') : ''"
          >
            <header class="card__head">
              <div class="repro-head__title">
                <span class="icon-tile icon-tile--accent"><AppIcon name="chart" :size="17" /></span>
                <div>
                  <h2 class="card__title">Resultado da validação</h2>
                  <p class="card__desc">Resumo executivo do último cruzamento analisado.</p>
                </div>
              </div>
              <span
                v-if="analiseAtual"
                class="badge"
                :class="analiseFalhou ? 'badge--danger' : analiseAtual.resultado.apto ? 'badge--ok' : 'badge--warn'"
              >
                <span class="badge__dot"></span>
                {{ analiseFalhou ? 'Não concluída' : analiseAtual.resultado.apto ? 'Aprovado' : 'Não aprovado' }}
              </span>
            </header>

            <div v-if="!analiseAtual" class="empty">
              <AppIcon name="sparkle" :size="28" />
              <p class="empty__title">Nenhuma análise disponível</p>
              <p class="empty__desc">Volte para "Nova análise" e selecione uma matriz e um touro.</p>
              <button type="button" class="btn btn--primary" @click="aba = 'nova'">Iniciar análise</button>
            </div>

            <div v-else class="card__body stack">
              <div class="repro-facts">
                <div class="repro-fact">
                  <span>Matriz</span>
                  <strong>{{ analiseAtual.matriz }}</strong>
                </div>
                <div class="repro-fact">
                  <span>Touro</span>
                  <strong>{{ analiseAtual.touro }}</strong>
                </div>
                <div class="repro-fact">
                  <span>Risco de consanguinidade</span>
                  <strong>{{ analiseAtual.resultado.nivel_risco_consanguinidade || 'Não informado' }}</strong>
                </div>
                <div class="repro-fact">
                  <span>Grau detectado</span>
                  <strong>{{ analiseAtual.resultado.geracao_parentesco_detectada ?? 'Nenhum' }}</strong>
                </div>
              </div>

              <div v-if="resumoParecer" class="repro-summary-box">
                <h3 class="repro-section-title">Resumo do parecer</h3>
                <p>{{ resumoParecer }}</p>
              </div>

              <div class="repro-download-bar">
                <div>
                  <strong>Documento técnico completo</strong>
                  <p>Inclui análise genealógica detalhada, parecer zootécnico e tabela de ancestrais.</p>
                </div>
                <button
                  type="button"
                  class="btn btn--primary"
                  @click="baixarRelatorio(analiseAtual)"
                >
                  <AppIcon name="download" :size="15" />
                  Baixar relatório
                </button>
              </div>
            </div>
          </article>

          <article class="card">
            <header class="card__head">
              <div class="repro-head__title">
                <span class="icon-tile icon-tile--warn"><AppIcon name="dna" :size="17" /></span>
                <div>
                  <h2 class="card__title">Alertas de parentesco</h2>
                  <p class="card__desc">Ancestrais compartilhados na consulta mais recente.</p>
                </div>
              </div>
              <span v-if="analiseAtual" class="badge">{{ ancestraisComuns.length }}</span>
            </header>

            <div v-if="!analiseAtual" class="empty">
              <AppIcon name="dna" :size="28" />
              <p class="empty__desc">Os alertas aparecerão aqui após a análise de um cruzamento.</p>
            </div>
            <div v-else-if="analiseFalhou" class="empty">
              <AppIcon name="alert" :size="28" />
              <p class="empty__desc">Não foi possível gerar alertas porque a análise não foi concluída.</p>
            </div>
            <div v-else-if="ancestraisComuns.length" class="card__body">
              <ul class="repro-ancestors">
                <li v-for="(ancestor, index) in ancestraisComuns" :key="ancestor.id || index" class="repro-ancestor">
                  <strong>{{ ancestor.nome || `Ancestral #${ancestor.id}` }}</strong>
                  <div class="repro-ancestor__tags">
                    <span class="badge">Matriz: {{ ancestor.parentesco_na_femea || 'Não informado' }}</span>
                    <span class="badge badge--info">Touro: {{ ancestor.parentesco_no_macho || 'Não informado' }}</span>
                  </div>
                </li>
              </ul>
            </div>
            <div v-else class="empty">
              <AppIcon name="check-circle" :size="28" />
              <p class="empty__title">Sem ancestrais comuns</p>
              <p class="empty__desc">Nenhum parentesco compartilhado foi detectado até a 3ª geração.</p>
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
                <tr>
                  <th>Data</th>
                  <th>Matriz</th>
                  <th>Touro</th>
                  <th>Status</th>
                  <th>Risco</th>
                  <th class="cell-actions">Relatório</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="analise in analises" :key="analise.id">
                  <td class="mono nowrap">{{ formatDate(analise.data) }}</td>
                  <td class="cell-strong">{{ analise.matriz }}</td>
                  <td>{{ analise.touro }}</td>
                  <td>
                    <span class="badge" :class="analise.resultado.apto ? 'badge--ok' : 'badge--warn'">
                      <span class="badge__dot"></span>
                      {{ analise.resultado.apto ? 'Aprovado' : 'Não aprovado' }}
                    </span>
                  </td>
                  <td>{{ analise.resultado.nivel_risco_consanguinidade || '—' }}</td>
                  <td class="cell-actions">
                    <button type="button" class="btn btn--sm" @click="baixarRelatorio(analise)">
                      <AppIcon name="download" :size="14" />
                      Baixar
                    </button>
                  </td>
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
const abas = computed(() => [
  { id: 'nova', label: 'Nova análise', icon: 'sparkle' },
  { id: 'resultados', label: 'Resultados e histórico', icon: 'chart', count: analises.value.length },
]);
const analiseAtual = computed(() => analises.value[0] || null);
const ancestraisComuns = computed(() => analiseAtual.value?.resultado?.ancestrais_comuns || []);
const analiseFalhou = computed(() => [
  'ERRO_CONFIGURACAO',
  'ERRO_PROCESSAMENTO_IA',
  'ERRO_PARAMETROS',
  'RESPOSTA_NAO_ESTRUTURADA',
].includes(analiseAtual.value?.resultado?.status));

function resumirTexto(texto, limite = 220) {
  const limpo = String(texto || '').replace(/\s+/g, ' ').trim();
  if (!limpo) return '';
  if (limpo.length <= limite) return limpo;
  const corte = limpo.slice(0, limite);
  const ultimoPonto = corte.lastIndexOf('.');
  if (ultimoPonto > 90) return corte.slice(0, ultimoPonto + 1);
  const ultimoEspaco = corte.lastIndexOf(' ');
  return `${corte.slice(0, ultimoEspaco > 0 ? ultimoEspaco : limite)}…`;
}

const resumoParecer = computed(() => {
  const res = analiseAtual.value?.resultado;
  if (!res) return '';
  if (analiseFalhou.value && res.analise_genealogica) {
    return res.analise_genealogica;
  }
  return resumirTexto(res.veredito_final || res.analise_genealogica || res.analise_zootecnica_complementar);
});

function escaparHtml(valor) {
  return String(valor ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function baixarRelatorio(analise) {
  if (!analise) return;
  const res = analise.resultado || {};
  const ancestrais = Array.isArray(res.ancestrais_comuns) ? res.ancestrais_comuns : [];
  const statusLabel = res.apto ? 'APROVADO' : 'NÃO APROVADO';
  const badgeColor = res.apto ? '#1e6b43' : '#b42318';
  const badgeBg = res.apto ? '#e8f5ee' : '#fef3f2';

  const ancestraisHtml = ancestrais.length
    ? `<table>
        <thead><tr><th>Ancestral</th><th>Parentesco na Matriz</th><th>Parentesco no Touro</th></tr></thead>
        <tbody>
          ${ancestrais.map((a) => `<tr>
            <td>${escaparHtml(a.nome || `Ancestral #${a.id || '—'}`)}</td>
            <td>${escaparHtml(a.parentesco_na_femea || 'Não informado')}</td>
            <td>${escaparHtml(a.parentesco_no_macho || 'Não informado')}</td>
          </tr>`).join('')}
        </tbody>
      </table>`
    : '<p class="muted">Nenhum ancestral comum identificado até a 3ª geração.</p>';

  const html = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Relatório de Análise Reprodutiva — ${escaparHtml(analise.matriz)} x ${escaparHtml(analise.touro)}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #1d241e; background: #f6f7f5; margin: 0; padding: 32px; line-height: 1.6; }
    .doc { max-width: 820px; margin: 0 auto; background: #fff; border: 1px solid #dfe3dd; border-radius: 12px; padding: 36px 40px; }
    .head { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; border-bottom: 2px solid #2f6b46; padding-bottom: 18px; margin-bottom: 24px; }
    .brand { font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #2f6b46; }
    h1 { margin: 4px 0 0; font-size: 22px; }
    .badge { display: inline-block; padding: 6px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; color: ${badgeColor}; background: ${badgeBg}; border: 1px solid ${badgeColor}33; }
    .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 24px; }
    .box { padding: 12px 14px; border: 1px solid #e5e8e3; border-radius: 8px; background: #fafbf9; }
    .box small { display: block; font-size: 11px; text-transform: uppercase; color: #5f6860; font-weight: 600; }
    .box strong { font-size: 15px; }
    h2 { font-size: 15px; color: #2f6b46; border-bottom: 1px solid #e5e8e3; padding-bottom: 6px; margin: 24px 0 10px; }
    p { margin: 0 0 12px; }
    .verdict { padding: 14px 16px; border-left: 4px solid ${badgeColor}; background: ${badgeBg}; border-radius: 6px; font-weight: 500; }
    table { width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 14px; }
    th, td { text-align: left; padding: 9px 12px; border-bottom: 1px solid #e5e8e3; }
    th { background: #f3f5f2; font-size: 12px; text-transform: uppercase; color: #525b53; }
    .muted { color: #667067; font-size: 14px; }
    .foot { margin-top: 32px; padding-top: 14px; border-top: 1px solid #e5e8e3; font-size: 12px; color: #667067; display: flex; justify-content: space-between; }
    @media print { body { background: #fff; padding: 0; } .doc { border: 0; padding: 0; } }
  </style>
</head>
<body>
  <article class="doc">
    <header class="head">
      <div>
        <div class="brand">L.S Management · Análise Reprodutiva &amp; IA</div>
        <h1>Parecer Técnico de Cruzamento</h1>
        <p class="muted">Emitido em ${escaparHtml(formatDate(analise.data))}</p>
      </div>
      <span class="badge">${escaparHtml(statusLabel)}</span>
    </header>

    <section class="grid">
      <div class="box"><small>Matriz (Vaca)</small><strong>${escaparHtml(analise.matriz)}</strong></div>
      <div class="box"><small>Reprodutor (Touro)</small><strong>${escaparHtml(analise.touro)}</strong></div>
      <div class="box"><small>Nível de risco de consanguinidade</small><strong>${escaparHtml(res.nivel_risco_consanguinidade || 'Não informado')}</strong></div>
      <div class="box"><small>Geração de parentesco detectada</small><strong>${escaparHtml(res.geracao_parentesco_detectada ?? 'Nenhum parentesco detectado')}</strong></div>
    </section>

    <h2>Veredito Final</h2>
    <p class="verdict">${escaparHtml(res.veredito_final || 'Não informado.')}</p>

    <h2>Análise Genealógica Detalhada</h2>
    <p>${escaparHtml(res.analise_genealogica || 'Sem detalhamento adicional.')}</p>

    <h2>Análise Zootécnica Complementar</h2>
    <p>${escaparHtml(res.analise_zootecnica_complementar || 'Sem observações zootécnicas adicionais.')}</p>

    <h2>Ancestrais Comuns Identificados</h2>
    ${ancestraisHtml}

    ${analise.observacoes ? `<h2>Observações Informadas na Solicitação</h2><p>${escaparHtml(analise.observacoes)}</p>` : ''}

    <footer class="foot">
      <span>Status do sistema: ${escaparHtml(res.status || statusLabel)}</span>
      <span>Gerado pelo módulo Reprodução &amp; IA · L.S Management</span>
    </footer>
  </article>
</body>
</html>`;

  const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  const slug = `${analise.matriz}-${analise.touro}`.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 50);
  link.href = url;
  link.download = `relatorio-reprodutivo-${slug}.html`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

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
      observacoes: observacoes.value,
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
.repro-ai__kpis {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 20px;
}

.repro-kpi {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 18px;
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  background: var(--surface);
  box-shadow: var(--shadow-card);
}

.repro-kpi__icon {
  display: grid;
  width: 42px;
  height: 42px;
  flex: none;
  place-items: center;
  border-radius: 12px;
}

.repro-kpi__icon--accent { background: var(--accent-soft); color: var(--accent); }
.repro-kpi__icon--info { background: var(--info-soft); color: var(--info); }
.repro-kpi__icon--warn { background: var(--warn-soft); color: var(--warn); }

.repro-kpi__label {
  display: block;
  color: var(--text-3);
  font-size: var(--fs-xs);
  font-weight: 500;
}

.repro-kpi__value {
  display: block;
  margin-top: 2px;
  font-family: var(--font-mono);
  font-size: var(--fs-2xl);
  font-weight: 600;
  line-height: 1.1;
}

.repro-ai__panel { display: grid; gap: 18px; }
.repro-head__title { display: flex; align-items: center; gap: 12px; }

.repro-pairing {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  align-items: stretch;
  gap: 16px;
}

.repro-pairing__box {
  display: grid;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface-2);
}

.repro-pairing__badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  width: fit-content;
  padding: 4px 10px;
  border-radius: var(--r-full);
  background: var(--accent-soft);
  color: var(--accent);
  font-size: var(--fs-xs);
  font-weight: 600;
}

.repro-pairing__badge--bull {
  background: var(--info-soft);
  color: var(--info);
}

.repro-pairing__connector {
  display: grid;
  place-items: center;
}

.repro-pairing__connector span {
  display: grid;
  width: 36px;
  height: 36px;
  place-items: center;
  border: 1px solid var(--line-strong);
  border-radius: 50%;
  background: var(--surface);
  color: var(--text-2);
  font-size: 18px;
  font-weight: 600;
}

.repro-pairing__foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  padding-top: 14px;
  border-top: 1px solid var(--line);
}

.repro-pairing__hint {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--text-3);
  font-size: var(--fs-xs);
}

.repro-results__grid {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(0, 0.9fr);
  gap: 16px;
  align-items: start;
}

.repro-verdict-card.is-ok { border-top: 3px solid var(--ok); }
.repro-verdict-card.is-warn { border-top: 3px solid var(--warn); }
.repro-verdict-card.is-danger { border-top: 3px solid var(--danger); }

.repro-facts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.repro-fact {
  padding: 12px 14px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface-2);
}

.repro-fact span {
  display: block;
  color: var(--text-3);
  font-size: var(--fs-xs);
}

.repro-fact strong {
  display: block;
  margin-top: 3px;
  font-size: var(--fs-md);
}

.repro-section-title {
  margin: 0 0 6px;
  font-size: var(--fs-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-3);
}

.repro-summary-box {
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface-2);
}

.repro-summary-box p {
  margin: 0;
  color: var(--text);
  line-height: 1.6;
}

.repro-download-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
  padding: 14px 16px;
  border: 1px solid var(--accent-line);
  border-radius: var(--r-md);
  background: var(--accent-soft);
}

.repro-download-bar strong { display: block; font-size: var(--fs-sm); color: var(--text); }
.repro-download-bar p { margin: 2px 0 0; font-size: var(--fs-xs); color: var(--text-2); }

.repro-ancestors {
  display: grid;
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.repro-ancestor {
  display: grid;
  gap: 8px;
  padding: 12px 14px;
  border: 1px solid var(--warn-line);
  border-radius: var(--r-md);
  background: var(--warn-soft);
}

.repro-ancestor__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

@media (max-width: 900px) {
  .repro-ai__kpis,
  .repro-results__grid,
  .repro-pairing { grid-template-columns: 1fr; }
  .repro-pairing__connector { display: none; }
}

@media (max-width: 600px) {
  .repro-facts { grid-template-columns: 1fr; }
}
</style>
