<template>
  <AppShell>
    <div class="page page--wide dev-page">
      <header class="hero registry-hero">
        <div class="hero__bg" aria-hidden="true">
          <img :src="pesagemHero" alt="" class="hero__img">
          <div class="hero__shade"></div>
        </div>
        <div class="hero__content">
          <div>
            <div class="registry-hero__meta">
              <span class="hero__eyebrow">Desenvolvimento · Curva de crescimento</span>
              <span class="registry-hero__pill">{{ weights.length }} pesagem(ns)</span>
            </div>
            <h1 class="hero__title">Desenvolvimento</h1>
            <p class="hero__desc">Acompanhe pesagens nos marcos de 30 dias, 60 dias e desmame, visualize a curva de crescimento e identifique animais fora do padrão.</p>
          </div>
        </div>
      </header>

      <div class="dev-actions">
        <button type="button" class="btn btn--primary" @click="abrirModalPesagem()">
          <AppIcon name="plus" :size="16" />
          Registrar pesagem
        </button>
      </div>

      <p v-if="loadError" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ loadError }}</span>
        <button type="button" class="btn btn--sm" @click="carregarDados">Tentar novamente</button>
      </p>

      <p v-if="statusNotice" class="alert alert--ok" role="status">
        <AppIcon name="check-circle" :size="16" />
        <span>{{ statusNotice }}</span>
      </p>

      <!-- KPIs -->
      <section class="dev-kpis" aria-label="Resumo do desenvolvimento do rebanho">
        <button type="button" class="dev-kpi" @click="abaAtiva = 'rebanho'">
          <span class="dev-kpi__icon dev-kpi__icon--accent"><AppIcon name="animal" :size="18" /></span>
          <span>
            <small>Animais monitorados</small>
            <strong>{{ animaisComPeso.length }} <span class="dev-kpi__sub">/ {{ animals.length }}</span></strong>
          </span>
        </button>
        <button type="button" class="dev-kpi" @click="abaAtiva = 'curva'">
          <span class="dev-kpi__icon dev-kpi__icon--info"><AppIcon name="scale" :size="18" /></span>
          <span>
            <small>Peso médio atual</small>
            <strong>{{ pesoMedioAtual ? `${fmt(pesoMedioAtual)} kg` : '—' }}</strong>
          </span>
        </button>
        <button type="button" class="dev-kpi" @click="abaAtiva = 'curva'">
          <span class="dev-kpi__icon dev-kpi__icon--accent"><AppIcon name="chart" :size="18" /></span>
          <span>
            <small>Pesagens registradas</small>
            <strong>{{ weights.length }}</strong>
          </span>
        </button>
        <button
          type="button"
          class="dev-kpi"
          :class="{ 'is-warn': animaisForaDoEsperado.length > 0 }"
          @click="abaAtiva = 'alertas'"
        >
          <span class="dev-kpi__icon" :class="animaisForaDoEsperado.length > 0 ? 'dev-kpi__icon--danger' : 'dev-kpi__icon--accent'">
            <AppIcon :name="animaisForaDoEsperado.length > 0 ? 'alert' : 'check-circle'" :size="18" />
          </span>
          <span>
            <small>Crescimento fora do esperado</small>
            <strong>{{ animaisForaDoEsperado.length }}</strong>
          </span>
        </button>
      </section>

      <AppTabs
        v-model="abaAtiva"
        :tabs="abas"
        label="Seções de desenvolvimento"
        id-base="desenvolvimento"
      />

      <!-- ABA 1: CURVA DE CRESCIMENTO -->
      <div
        v-if="abaAtiva === 'curva'"
        id="desenvolvimento-panel-curva"
        role="tabpanel"
        aria-labelledby="desenvolvimento-tab-curva"
        class="stack"
      >
        <section class="card">
          <header class="card__head dev-curve__head">
            <div>
              <h2 class="card__title">Curva de crescimento individual</h2>
              <p class="card__desc">Selecione um animal para analisar a evolução de peso e os marcos de desenvolvimento.</p>
            </div>
            <div class="dev-curve__selector">
              <label class="sr-only" for="dev-animal-select">Selecionar animal</label>
              <select
                id="dev-animal-select"
                v-model="selectedAnimalId"
                class="select"
                :disabled="loading || !animals.length"
              >
                <option value="" disabled>{{ loading ? 'Carregando animais...' : 'Selecione um animal...' }}</option>
                <option v-for="item in animaisResumo" :key="item.animal.id" :value="String(item.animal.id)">
                  {{ item.animal.name || 'Sem nome' }} · #{{ item.animal.register_number }}
                  {{ item.pesoAtual !== null ? `(${fmt(item.pesoAtual)} kg)` : '(sem pesagem)' }}
                </option>
              </select>
            </div>
          </header>

          <div v-if="loading" class="loading">
            <span class="spinner" aria-hidden="true"></span>
            Carregando histórico de pesagens...
          </div>

          <div v-else-if="!animalSelecionadoResumo" class="empty">
            <AppIcon name="scale" :size="30" />
            <p class="empty__title">Nenhum animal selecionado</p>
            <p class="empty__desc">Escolha um bovino acima para visualizar a curva de crescimento e os marcos de pesagem.</p>
          </div>

          <div v-else class="card__body stack">
            <!-- Status / alerta do animal selecionado -->
            <div
              v-if="animalSelecionadoResumo.alerta"
              class="alert alert--warn"
              role="status"
            >
              <AppIcon name="alert" :size="16" />
              <span>
                <strong>Padrão de crescimento fora do esperado:</strong>
                {{ animalSelecionadoResumo.alerta.mensagem }}
              </span>
            </div>

            <!-- Marcos de Desenvolvimento (RN-07) -->
            <div class="dev-milestones" aria-label="Marcos de pesagem do animal">
              <article class="dev-milestone">
                <span class="dev-milestone__label">Nascimento</span>
                <strong>{{ animalSelecionadoResumo.marcos.nascimento ? `${fmt(animalSelecionadoResumo.marcos.nascimento.weight)} kg` : '—' }}</strong>
                <small>{{ animalSelecionadoResumo.marcos.nascimento ? formatarData(animalSelecionadoResumo.marcos.nascimento.date) : 'Não vinculado' }}</small>
              </article>
              <article class="dev-milestone" :class="{ 'is-filled': animalSelecionadoResumo.marcos.d30 }">
                <span class="dev-milestone__label">Marco 30 dias</span>
                <strong>{{ animalSelecionadoResumo.marcos.d30 ? `${fmt(animalSelecionadoResumo.marcos.d30.weight)} kg` : 'Pendente' }}</strong>
                <small>{{ animalSelecionadoResumo.marcos.d30 ? formatarData(animalSelecionadoResumo.marcos.d30.weighing_date) : '15 a 45 dias' }}</small>
              </article>
              <article class="dev-milestone" :class="{ 'is-filled': animalSelecionadoResumo.marcos.d60 }">
                <span class="dev-milestone__label">Marco 60 dias</span>
                <strong>{{ animalSelecionadoResumo.marcos.d60 ? `${fmt(animalSelecionadoResumo.marcos.d60.weight)} kg` : 'Pendente' }}</strong>
                <small>{{ animalSelecionadoResumo.marcos.d60 ? formatarData(animalSelecionadoResumo.marcos.d60.weighing_date) : '46 a 75 dias' }}</small>
              </article>
              <article class="dev-milestone" :class="{ 'is-filled': animalSelecionadoResumo.marcos.desmame }">
                <span class="dev-milestone__label">Desmame</span>
                <strong>{{ animalSelecionadoResumo.marcos.desmame ? `${fmt(animalSelecionadoResumo.marcos.desmame.weight)} kg` : 'Pendente' }}</strong>
                <small>{{ animalSelecionadoResumo.marcos.desmame ? formatarData(animalSelecionadoResumo.marcos.desmame.weighing_date) : 'A partir de 76 dias' }}</small>
              </article>
            </div>

            <!-- Gráfico Chart.js -->
            <div v-if="pontosCurvaSelecionado.length === 0" class="empty">
              <AppIcon name="chart" :size="28" />
              <p class="empty__title">Sem pesagens para este animal</p>
              <p class="empty__desc">Registre a primeira pesagem para gerar a curva de crescimento.</p>
              <button type="button" class="btn btn--primary" @click="abrirModalPesagem(animalSelecionadoResumo.animal.id)">
                <AppIcon name="plus" :size="15" />
                Registrar pesagem
              </button>
            </div>
            <div v-else class="dev-chart-wrap">
              <Line
                :key="`dev-chart-${selectedAnimalId}-${pontosCurvaSelecionado.length}`"
                :data="chartData"
                :options="chartOptions"
                aria-label="Curva de crescimento do animal selecionado"
              />
            </div>

            <!-- Tabela de pesagens do animal -->
            <div v-if="animalSelecionadoResumo.pesagens.length" class="table-wrap">
              <table class="table">
                <thead>
                  <tr>
                    <th>Data</th>
                    <th>Marco</th>
                    <th>Peso</th>
                    <th>Variação</th>
                    <th>Ganho diário (GMD)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="linha in historicoDetalhadoSelecionado" :key="linha.id">
                    <td class="mono nowrap">{{ formatarData(linha.weighing_date) }}</td>
                    <td>
                      <span class="badge" :class="linha.marcoBadge">{{ linha.marcoRotulo }}</span>
                    </td>
                    <td class="mono cell-strong">{{ fmt(linha.weight) }} kg</td>
                    <td class="mono" :class="linha.variacao < 0 ? 'text-danger' : linha.variacao > 0 ? 'text-ok' : 'text-muted'">
                      {{ linha.variacao === null ? '—' : `${linha.variacao >= 0 ? '+' : ''}${fmt(linha.variacao)} kg` }}
                    </td>
                    <td class="mono" :class="linha.gmd !== null && linha.gmd < GMD_MINIMO ? 'text-danger' : 'text-muted'">
                      {{ linha.gmd === null ? '—' : `${fmt(linha.gmd)} kg/dia` }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </div>

      <!-- ABA 2: ALERTAS DE CRESCIMENTO (RF-06) -->
      <div
        v-else-if="abaAtiva === 'alertas'"
        id="desenvolvimento-panel-alertas"
        role="tabpanel"
        aria-labelledby="desenvolvimento-tab-alertas"
      >
        <RegistryCard
          titulo="Animais com crescimento fora do esperado"
          descricao="Sinalização automática para perda de peso, estagnação ou ganho médio diário abaixo da referência (0,45 kg/dia)."
          :total="animaisForaDoEsperado.length"
          :carregando="loading"
          texto-carregando="Analisando curvas de crescimento..."
          :vazio="animaisForaDoEsperado.length === 0"
          icone-vazio="check-circle"
          titulo-vazio="Nenhum alerta de crescimento"
          descricao-vazia="Todos os animais monitorados estão evoluindo dentro do padrão esperado."
        >
          <div class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>Brinco</th>
                  <th>Animal</th>
                  <th>Peso anterior</th>
                  <th>Peso atual</th>
                  <th>GMD</th>
                  <th>Motivo do alerta</th>
                  <th class="cell-actions">Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in animaisForaDoEsperado" :key="item.animal.id">
                  <td class="mono">#{{ item.animal.register_number }}</td>
                  <td class="cell-strong truncate" :title="item.animal.name || 'Sem nome'">
                    <RouterLink :to="{ name: 'animal-detail', params: { id: item.animal.id } }" class="cell-link">
                      {{ item.animal.name || 'Sem nome' }}
                    </RouterLink>
                  </td>
                  <td class="mono">{{ item.pesoAnterior !== null ? `${fmt(item.pesoAnterior)} kg` : '—' }}</td>
                  <td class="mono cell-strong">{{ item.pesoAtual !== null ? `${fmt(item.pesoAtual)} kg` : '—' }}</td>
                  <td class="mono text-danger">{{ item.gmd !== null ? `${fmt(item.gmd)} kg/dia` : '—' }}</td>
                  <td>
                    <span class="badge" :class="item.alerta.critico ? 'badge--danger' : 'badge--warn'">
                      <span class="badge__dot"></span>
                      {{ item.alerta.rotulo }}
                    </span>
                  </td>
                  <td class="cell-actions">
                    <button type="button" class="btn btn--sm" @click="abrirCurvaAnimal(item.animal.id)">
                      Ver curva
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </RegistryCard>
      </div>

      <!-- ABA 3: PANORAMA DO REBANHO -->
      <div
        v-else
        id="desenvolvimento-panel-rebanho"
        role="tabpanel"
        aria-labelledby="desenvolvimento-tab-rebanho"
      >
        <section class="registry-toolbar" aria-label="Filtrar desenvolvimento do rebanho">
          <label class="search">
            <AppIcon name="search" :size="16" />
            <input
              v-model="buscaRebanho"
              class="input"
              type="search"
              placeholder="Buscar por nome ou brinco"
              aria-label="Buscar animal"
            >
          </label>
          <select v-model="filtroStatus" class="select dev-filter-select" aria-label="Filtrar por padrão de crescimento">
            <option value="todos">Todos os padrões</option>
            <option value="alerta">Fora do esperado</option>
            <option value="ok">Dentro do esperado</option>
            <option value="sem-peso">Sem pesagem</option>
          </select>
          <span class="registry-toolbar__count">{{ rebanhoFiltrado.length }} resultado(s)</span>
        </section>

        <RegistryCard
          titulo="Desenvolvimento por animal"
          descricao="O peso atual é obtido automaticamente da última pesagem registrada no histórico."
          :total="rebanhoFiltrado.length"
          :carregando="loading"
          texto-carregando="Carregando desenvolvimento do rebanho..."
          :vazio="animals.length === 0"
          :vazio-filtrado="animals.length > 0 && rebanhoFiltrado.length === 0"
          icone-vazio="animal"
          titulo-vazio="Nenhum animal cadastrado"
          descricao-vazia="Cadastre animais no rebanho para acompanhar seu desenvolvimento."
          descricao-vazio-filtrado="Nenhum animal corresponde aos filtros selecionados."
          @limpar-filtros="limparFiltrosRebanho"
        >
          <div class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>Brinco</th>
                  <th>Animal</th>
                  <th>Peso atual</th>
                  <th>Última pesagem</th>
                  <th>Pesagens</th>
                  <th>Padrão de crescimento</th>
                  <th class="cell-actions">Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in rebanhoFiltrado" :key="item.animal.id">
                  <td class="mono">#{{ item.animal.register_number }}</td>
                  <td class="cell-strong truncate" :title="item.animal.name || 'Sem nome'">
                    <RouterLink :to="{ name: 'animal-detail', params: { id: item.animal.id } }" class="cell-link">
                      {{ item.animal.name || 'Sem nome' }}
                    </RouterLink>
                  </td>
                  <td class="mono cell-strong">{{ item.pesoAtual !== null ? `${fmt(item.pesoAtual)} kg` : '—' }}</td>
                  <td class="mono nowrap">{{ item.ultimaData ? formatarData(item.ultimaData) : '—' }}</td>
                  <td class="mono">{{ item.pesagens.length }}</td>
                  <td>
                    <span v-if="item.alerta" class="badge" :class="item.alerta.critico ? 'badge--danger' : 'badge--warn'">
                      <span class="badge__dot"></span>
                      {{ item.alerta.rotulo }}
                    </span>
                    <span v-else-if="item.pesagens.length" class="badge badge--ok">
                      <span class="badge__dot"></span>
                      Dentro do esperado
                    </span>
                    <span v-else class="badge">Sem pesagem</span>
                  </td>
                  <td class="cell-actions">
                    <div class="registry-actions">
                      <button type="button" class="btn btn--sm" @click="abrirCurvaAnimal(item.animal.id)">
                        Curva
                      </button>
                      <button
                        type="button"
                        class="btn btn--icon"
                        aria-label="Registrar pesagem"
                        title="Registrar pesagem"
                        @click="abrirModalPesagem(item.animal.id)"
                      >
                        <AppIcon name="plus" :size="15" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </RegistryCard>
      </div>

      <!-- MODAL: REGISTRAR PESAGEM POR MARCO (RF-04 / RN-07) -->
      <AppModal
        v-if="showModal"
        titulo="Registrar pesagem de desenvolvimento"
        @fechar="fecharModalPesagem"
      >
        <form id="form-dev-pesagem" class="stack" @submit.prevent="salvarPesagem">
          <div class="field">
            <label class="field__label" for="dev-modal-animal">Animal *</label>
            <select id="dev-modal-animal" v-model="form.animal" class="select" required>
              <option value="" disabled>Selecione um animal...</option>
              <option v-for="animal in animals" :key="animal.id" :value="String(animal.id)">
                {{ animal.name || 'Sem nome' }} · #{{ animal.register_number }}
              </option>
            </select>
          </div>

          <div class="field">
            <label class="field__label" for="dev-modal-marco">Marco da pesagem (RN-07)</label>
            <select id="dev-modal-marco" v-model="form.marco" class="select" @change="sugerirDataMarco">
              <option value="d30">30 dias</option>
              <option value="d60">60 dias</option>
              <option value="desmame">Desmame</option>
              <option value="acompanhamento">Acompanhamento geral</option>
            </select>
            <span class="field__hint">Classifica a pesagem nos marcos de desenvolvimento da fazenda.</span>
          </div>

          <div class="grid grid--2">
            <div class="field">
              <label class="field__label" for="dev-modal-peso">Peso (kg) *</label>
              <input
                id="dev-modal-peso"
                v-model="form.weight"
                class="input"
                type="number"
                min="0.1"
                step="0.1"
                placeholder="Ex.: 85.5"
                required
              >
            </div>
            <div class="field">
              <label class="field__label" for="dev-modal-data">Data da pesagem *</label>
              <input
                id="dev-modal-data"
                v-model="form.weighing_date"
                class="input"
                type="date"
                required
              >
            </div>
          </div>

          <p v-if="modalError" class="alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ modalError }}</span>
          </p>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="fecharModalPesagem">Cancelar</button>
          <button type="submit" form="form-dev-pesagem" class="btn btn--primary" :disabled="saving">
            {{ saving ? 'Salvando...' : 'Salvar pesagem' }}
          </button>
        </template>
      </AppModal>
    </div>
  </AppShell>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import {
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LineController,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip,
} from 'chart.js';
import { Line } from 'vue-chartjs';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppModal from '@/components/ui/AppModal.vue';
import AppTabs from '@/components/ui/AppTabs.vue';
import RegistryCard from '@/components/layout/RegistryCard.vue';
import pesagemHero from '@/assets/images/pesagem-hero.jpg';
import { idRelacao } from '@/utils/animalMovementUtils';
import { apiErrorMessage } from '@/utils/apiError';

ChartJS.register(CategoryScale, LinearScale, LineController, LineElement, PointElement, Filler, Legend, Tooltip);

const GMD_MINIMO = 0.45;
const GMD_REFERENCIA = 0.70;
const MARCOS_STORAGE_KEY = 'ls-management-weight-milestones';

const MARCO_ROTULOS = {
  d30: { rotulo: '30 dias', badge: 'badge--info' },
  d60: { rotulo: '60 dias', badge: 'badge--info' },
  desmame: { rotulo: 'Desmame', badge: 'badge--ok' },
  acompanhamento: { rotulo: 'Acompanhamento', badge: '' },
};

const loading = ref(true);
const loadError = ref('');
const statusNotice = ref('');
const animals = ref([]);
const weights = ref([]);
const births = ref([]);
const abaAtiva = ref('curva');
const selectedAnimalId = ref('');
const buscaRebanho = ref('');
const filtroStatus = ref('todos');

const showModal = ref(false);
const saving = ref(false);
const modalError = ref('');
const marcosSalvos = ref(carregarMarcosLocais());

function dataLocalHoje() {
  const hoje = new Date();
  return new Date(hoje.getTime() - hoje.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

const form = ref({
  animal: '',
  marco: 'd30',
  weight: '',
  weighing_date: dataLocalHoje(),
});

function carregarMarcosLocais() {
  try {
    const raw = localStorage.getItem(MARCOS_STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function salvarMarcoLocal(weightId, marco) {
  if (!weightId || !marco) return;
  const atualizado = { ...marcosSalvos.value, [String(weightId)]: marco };
  marcosSalvos.value = atualizado;
  try {
    localStorage.setItem(MARCOS_STORAGE_KEY, JSON.stringify(atualizado));
  } catch {
    // ignora erro de quota do navegador
  }
}

function listaDaResposta(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  return [];
}

function fmt(valor) {
  const num = Number(valor);
  if (!Number.isFinite(num)) return '—';
  return num.toLocaleString('pt-BR', { maximumFractionDigits: 2 });
}

function formatarData(valor) {
  if (!valor) return '—';
  const iso = String(valor).slice(0, 10);
  const d = new Date(`${iso}T00:00:00`);
  return Number.isNaN(d.getTime()) ? '—' : d.toLocaleDateString('pt-BR');
}

function diasEntre(dataA, dataB) {
  if (!dataA || !dataB) return null;
  const a = new Date(`${String(dataA).slice(0, 10)}T00:00:00`);
  const b = new Date(`${String(dataB).slice(0, 10)}T00:00:00`);
  if (Number.isNaN(a.getTime()) || Number.isNaN(b.getTime())) return null;
  return Math.round((b - a) / 86400000);
}

function classificarMarco(registro, birthDate) {
  const salvo = marcosSalvos.value[String(registro.id)];
  if (salvo && MARCO_ROTULOS[salvo]) return salvo;
  if (birthDate) {
    const idade = diasEntre(birthDate, registro.weighing_date);
    if (idade !== null) {
      if (idade >= 15 && idade <= 45) return 'd30';
      if (idade >= 46 && idade <= 75) return 'd60';
      if (idade >= 76 && idade <= 150) return 'desmame';
    }
  }
  return 'acompanhamento';
}

const birthsPorId = computed(() => new Map(births.value.map((b) => [String(b.id), b])));

const pesagensPorAnimal = computed(() => {
  const map = new Map();
  for (const w of weights.value) {
    const id = String(idRelacao(w.animal));
    if (!map.has(id)) map.set(id, []);
    map.get(id).push(w);
  }
  for (const lista of map.values()) {
    lista.sort((a, b) => String(a.weighing_date).localeCompare(String(b.weighing_date)) || (a.id - b.id));
  }
  return map;
});

const animaisResumo = computed(() => animals.value.map((animal) => {
  const pesagens = pesagensPorAnimal.value.get(String(animal.id)) || [];
  const birth = animal.birth ? birthsPorId.value.get(String(idRelacao(animal.birth))) || null : null;
  const ultima = pesagens.length ? pesagens[pesagens.length - 1] : null;
  const penultima = pesagens.length >= 2 ? pesagens[pesagens.length - 2] : null;
  const pesoAtual = ultima ? Number(ultima.weight) : null;
  const pesoAnterior = penultima ? Number(penultima.weight) : (birth && birth.weight ? Number(birth.weight) : null);
  const dataAnterior = penultima ? penultima.weighing_date : (birth?.date || null);

  let gmd = null;
  let variacao = null;
  if (ultima && pesoAnterior !== null) {
    variacao = pesoAtual - pesoAnterior;
    const dias = diasEntre(dataAnterior, ultima.weighing_date);
    if (dias && dias > 0) gmd = variacao / dias;
  }

  let alerta = null;
  if (variacao !== null && variacao < 0) {
    alerta = {
      critico: true,
      rotulo: 'Perda de peso',
      mensagem: `Redução de ${fmt(Math.abs(variacao))} kg em relação à medição anterior (${fmt(pesoAnterior)} kg → ${fmt(pesoAtual)} kg).`,
    };
  } else if (variacao !== null && variacao === 0 && pesagens.length >= 2) {
    alerta = {
      critico: false,
      rotulo: 'Peso estagnado',
      mensagem: `Sem ganho de peso entre as últimas medições (${fmt(pesoAtual)} kg).`,
    };
  } else if (gmd !== null && gmd < GMD_MINIMO) {
    alerta = {
      critico: false,
      rotulo: 'GMD abaixo do esperado',
      mensagem: `Ganho médio diário de ${fmt(gmd)} kg/dia, abaixo da referência mínima de ${fmt(GMD_MINIMO)} kg/dia.`,
    };
  }

  const marcos = { nascimento: birth, d30: null, d60: null, desmame: null };
  for (const p of pesagens) {
    const tipo = classificarMarco(p, birth?.date);
    if (tipo === 'd30') marcos.d30 = p;
    else if (tipo === 'd60') marcos.d60 = p;
    else if (tipo === 'desmame') marcos.desmame = p;
  }

  return {
    animal,
    birth,
    pesagens,
    pesoAtual,
    pesoAnterior,
    ultimaData: ultima?.weighing_date || null,
    variacao,
    gmd,
    alerta,
    marcos,
  };
}));

const animaisComPeso = computed(() => animaisResumo.value.filter((i) => i.pesoAtual !== null));
const pesoMedioAtual = computed(() => {
  if (!animaisComPeso.value.length) return 0;
  return animaisComPeso.value.reduce((acc, i) => acc + i.pesoAtual, 0) / animaisComPeso.value.length;
});
const animaisForaDoEsperado = computed(() => animaisResumo.value.filter((i) => Boolean(i.alerta)));

const abas = computed(() => [
  { id: 'curva', label: 'Curva de crescimento', icon: 'chart' },
  { id: 'alertas', label: 'Fora do esperado', icon: 'alert', count: animaisForaDoEsperado.value.length, warn: animaisForaDoEsperado.value.length > 0 },
  { id: 'rebanho', label: 'Panorama do rebanho', icon: 'animal', count: animals.value.length },
]);

const animalSelecionadoResumo = computed(() =>
  animaisResumo.value.find((i) => String(i.animal.id) === selectedAnimalId.value) || null
);

const pontosCurvaSelecionado = computed(() => {
  const item = animalSelecionadoResumo.value;
  if (!item) return [];
  const pontos = [];
  if (item.birth?.date && item.birth?.weight) {
    pontos.push({ data: item.birth.date, peso: Number(item.birth.weight), rotulo: 'Nascimento' });
  }
  for (const p of item.pesagens) {
    const marco = classificarMarco(p, item.birth?.date);
    pontos.push({
      data: p.weighing_date,
      peso: Number(p.weight),
      rotulo: MARCO_ROTULOS[marco]?.rotulo || 'Pesagem',
    });
  }
  return pontos.sort((a, b) => String(a.data).localeCompare(String(b.data)));
});

const historicoDetalhadoSelecionado = computed(() => {
  const item = animalSelecionadoResumo.value;
  if (!item) return [];
  return item.pesagens.map((p, idx) => {
    const anterior = idx > 0 ? item.pesagens[idx - 1] : null;
    const pesoAnt = anterior ? Number(anterior.weight) : (item.birth?.weight ? Number(item.birth.weight) : null);
    const dataAnt = anterior ? anterior.weighing_date : (item.birth?.date || null);
    const variacao = pesoAnt !== null ? Number(p.weight) - pesoAnt : null;
    const dias = dataAnt ? diasEntre(dataAnt, p.weighing_date) : null;
    const gmd = variacao !== null && dias && dias > 0 ? variacao / dias : null;
    const marco = classificarMarco(p, item.birth?.date);
    return {
      ...p,
      variacao,
      gmd,
      marcoRotulo: MARCO_ROTULOS[marco]?.rotulo || 'Acompanhamento',
      marcoBadge: MARCO_ROTULOS[marco]?.badge || '',
    };
  }).reverse();
});

const rebanhoFiltrado = computed(() => {
  const termo = buscaRebanho.value.trim().toLowerCase();
  return animaisResumo.value.filter((item) => {
    if (filtroStatus.value === 'alerta' && !item.alerta) return false;
    if (filtroStatus.value === 'ok' && (item.alerta || !item.pesagens.length)) return false;
    if (filtroStatus.value === 'sem-peso' && item.pesagens.length > 0) return false;
    if (!termo) return true;
    return (
      String(item.animal.name || '').toLowerCase().includes(termo)
      || String(item.animal.register_number || '').includes(termo)
    );
  });
});

function chartColor(token) {
  return getComputedStyle(document.documentElement).getPropertyValue(token).trim();
}

function gradientArea(context) {
  const { ctx, chartArea } = context.chart;
  const accent = chartColor('--accent') || '#2f6b46';
  if (!chartArea) return accent;
  const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
  gradient.addColorStop(0, `${accent}42`);
  gradient.addColorStop(0.65, `${accent}14`);
  gradient.addColorStop(1, `${accent}00`);
  return gradient;
}

const chartData = computed(() => {
  const accent = chartColor('--accent') || '#2f6b46';
  const surface = chartColor('--surface') || '#ffffff';
  const info = chartColor('--info') || '#1d5b8a';
  const pontos = pontosCurvaSelecionado.value;
  const labels = pontos.map((p) => `${formatarData(p.data)} (${p.rotulo})`);
  const valores = pontos.map((p) => p.peso);

  const primeiro = pontos[0];
  const curvaEsperada = primeiro && pontos.length > 1
    ? pontos.map((p) => {
        const dias = Math.max(0, diasEntre(primeiro.data, p.data) || 0);
        return Number((primeiro.peso + dias * GMD_REFERENCIA).toFixed(2));
      })
    : [];

  return {
    labels,
    datasets: [
      {
        label: 'Peso real (kg)',
        data: valores,
        borderColor: accent,
        backgroundColor: gradientArea,
        pointBackgroundColor: accent,
        pointBorderColor: surface,
        pointBorderWidth: 2.5,
        pointRadius: 5,
        pointHoverRadius: 7,
        borderWidth: 3,
        tension: 0.34,
        fill: true,
      },
      ...(curvaEsperada.length
        ? [{
            label: `Referência esperada (+${fmt(GMD_REFERENCIA)} kg/dia)`,
            data: curvaEsperada,
            borderColor: info,
            borderWidth: 1.8,
            borderDash: [6, 5],
            pointRadius: 0,
            pointHoverRadius: 4,
            fill: false,
            tension: 0.2,
          }]
        : []),
    ],
  };
});

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: { left: 2, right: 12 } },
  interaction: { intersect: false, mode: 'index' },
  plugins: {
    legend: {
      display: true,
      position: 'top',
      align: 'end',
      labels: {
        usePointStyle: true,
        pointStyle: 'circle',
        boxWidth: 8,
        boxHeight: 8,
        padding: 16,
        color: chartColor('--text-2') || '#525b53',
        font: { size: 12, weight: '500' },
      },
    },
    tooltip: {
      backgroundColor: 'rgba(20, 26, 22, 0.92)',
      titleColor: '#ffffff',
      bodyColor: '#e9eee9',
      cornerRadius: 10,
      padding: 12,
      callbacks: {
        label: (ctx) => ` ${ctx.dataset.label.split(' (')[0]}: ${fmt(ctx.raw)} kg`,
      },
    },
  },
  scales: {
    x: {
      offset: false,
      border: { display: false },
      grid: { display: false },
      ticks: {
        padding: 8,
        color: chartColor('--text-3'),
        font: { size: 11 },
        maxRotation: 0,
        autoSkip: true,
        maxTicksLimit: 8,
      },
    },
    y: {
      beginAtZero: false,
      grace: '12%',
      border: { display: false, dash: [4, 4] },
      grid: { color: chartColor('--line'), tickLength: 0 },
      ticks: {
        padding: 10,
        color: chartColor('--text-3'),
        font: { size: 11 },
        callback: (value) => `${fmt(value)} kg`,
      },
    },
  },
}));

function abrirCurvaAnimal(animalId) {
  selectedAnimalId.value = String(animalId);
  abaAtiva.value = 'curva';
}

function limparFiltrosRebanho() {
  buscaRebanho.value = '';
  filtroStatus.value = 'todos';
}

function abrirModalPesagem(animalId = null) {
  modalError.value = '';
  form.value = {
    animal: animalId ? String(animalId) : selectedAnimalId.value || '',
    marco: 'd30',
    weight: '',
    weighing_date: dataLocalHoje(),
  };
  showModal.value = true;
}

function fecharModalPesagem() {
  showModal.value = false;
  modalError.value = '';
}

function sugerirDataMarco() {
  const item = animaisResumo.value.find((i) => String(i.animal.id) === form.value.animal);
  if (!item?.birth?.date) return;
  const dias = { d30: 30, d60: 60, desmame: 90 }[form.value.marco];
  if (!dias) return;
  const base = new Date(`${String(item.birth.date).slice(0, 10)}T00:00:00`);
  if (Number.isNaN(base.getTime())) return;
  base.setDate(base.getDate() + dias);
  form.value.weighing_date = new Date(base.getTime() - base.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

async function salvarPesagem() {
  if (saving.value) return;
  saving.value = true;
  modalError.value = '';
  try {
    const response = await api.registrarPeso({
      animal: Number(form.value.animal),
      weight: Number(form.value.weight),
      weighing_date: form.value.weighing_date,
    });
    if (response.data?.id) {
      salvarMarcoLocal(response.data.id, form.value.marco);
    }
    selectedAnimalId.value = String(form.value.animal);
    fecharModalPesagem();
    statusNotice.value = 'Pesagem registrada com sucesso na curva de desenvolvimento.';
    setTimeout(() => { statusNotice.value = ''; }, 5000);
    await carregarDados();
  } catch (err) {
    console.error('Erro ao registrar pesagem:', err);
    modalError.value = apiErrorMessage(err, 'Não foi possível registrar a pesagem. Confira os dados e tente novamente.');
  } finally {
    saving.value = false;
  }
}

async function carregarDados() {
  loading.value = true;
  loadError.value = '';
  try {
    const [animalsRes, weightsRes, birthsRes] = await Promise.all([
      api.getAnimals(),
      api.get('weight_history/'),
      api.get('births/'),
    ]);
    animals.value = listaDaResposta(animalsRes.data);
    weights.value = listaDaResposta(weightsRes.data);
    births.value = listaDaResposta(birthsRes.data);

    if (!selectedAnimalId.value && animals.value.length) {
      const primeiroComPeso = animaisResumo.value.find((i) => i.pesagens.length > 0);
      selectedAnimalId.value = String((primeiroComPeso || animaisResumo.value[0]).animal.id);
    }
  } catch (err) {
    console.error('Erro ao carregar dados de desenvolvimento:', err);
    loadError.value = apiErrorMessage(err, 'Não foi possível carregar os dados de desenvolvimento.');
  } finally {
    loading.value = false;
  }
}

onMounted(carregarDados);
</script>

<style scoped>
.dev-actions {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 16px;
}

.dev-kpis {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.dev-kpi {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  background: var(--surface);
  color: var(--text);
  font: inherit;
  text-align: left;
  cursor: pointer;
  box-shadow: var(--shadow-card);
  transition: transform var(--dur) var(--ease), border-color var(--dur) var(--ease), box-shadow var(--dur) var(--ease);
}

.dev-kpi:hover {
  transform: translateY(-2px);
  border-color: var(--accent-line);
  box-shadow: var(--shadow-hover);
}

.dev-kpi.is-warn {
  border-color: var(--warn-line);
  background: var(--warn-soft);
}

.dev-kpi__icon {
  display: grid;
  width: 40px;
  height: 40px;
  flex: none;
  place-items: center;
  border-radius: 11px;
}

.dev-kpi__icon--accent { background: var(--accent-soft); color: var(--accent); }
.dev-kpi__icon--info { background: var(--info-soft); color: var(--info); }
.dev-kpi__icon--danger { background: var(--danger-soft); color: var(--danger); }

.dev-kpi small { display: block; color: var(--text-3); font-size: var(--fs-xs); }
.dev-kpi strong { display: block; margin-top: 2px; font-family: var(--font-mono); font-size: var(--fs-xl); font-weight: 600; }
.dev-kpi__sub { color: var(--text-3); font-size: var(--fs-sm); font-weight: 400; }

.dev-curve__head { flex-wrap: wrap; }
.dev-curve__selector { width: min(320px, 100%); }

.dev-milestones {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.dev-milestone {
  padding: 13px 15px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface-2);
}

.dev-milestone.is-filled {
  border-color: var(--accent-line);
  background: var(--accent-soft);
}

.dev-milestone__label {
  display: block;
  color: var(--text-3);
  font-size: var(--fs-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.dev-milestone strong {
  display: block;
  margin-top: 4px;
  font-family: var(--font-mono);
  font-size: var(--fs-lg);
  color: var(--text);
}

.dev-milestone small {
  display: block;
  margin-top: 2px;
  color: var(--text-3);
  font-size: var(--fs-xs);
}

.dev-chart-wrap {
  position: relative;
  height: 300px;
  padding: 6px 0;
}

.dev-filter-select {
  width: auto;
  min-width: 190px;
  flex: none;
}

.text-ok { color: var(--ok); }
.text-danger { color: var(--danger); }

@media (max-width: 960px) {
  .dev-kpis,
  .dev-milestones { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 560px) {
  .dev-kpis,
  .dev-milestones { grid-template-columns: 1fr; }
  .dev-filter-select { width: 100%; }
}
</style>
