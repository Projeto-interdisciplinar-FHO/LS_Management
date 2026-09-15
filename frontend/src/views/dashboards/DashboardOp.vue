<template>
  <AppShell>
    <div class="page">
      <header class="page__head">
        <div>
          <h1 class="page__title">Rotina de campo</h1>
          <p class="page__desc">{{ dataPorExtenso }}</p>
        </div>
      </header>

      <p v-if="erro" class="alert alert--warn" role="status">
        <AppIcon name="alert" :size="16" />
        <span>{{ erro }}</span>
      </p>

      <!-- O operador chega aqui para lançar, não para ler. Os lançamentos
           vêm primeiro; os números são só a conferência do que foi feito. -->
      <section class="secao">
        <h2 class="secao__titulo">Lançar</h2>
        <div class="grid grid--auto">
          <RouterLink v-for="acao in lancamentos" :key="acao.to" :to="acao.to" class="acao">
            <span class="icon-tile icon-tile--accent"><AppIcon :name="acao.icone" :size="19" /></span>
            <span class="acao__texto">
              <strong>{{ acao.titulo }}</strong>
              <span>{{ acao.descricao }}</span>
            </span>
          </RouterLink>
        </div>
      </section>

      <section class="secao">
        <h2 class="secao__titulo">Registrado até agora</h2>
        <div class="grid grid--auto">
          <article v-for="cartao in indicadores" :key="cartao.rotulo" class="stat">
            <span class="stat__label">
              <AppIcon :name="cartao.icone" :size="15" />
              {{ cartao.rotulo }}
            </span>
            <strong class="stat__value">
              <span v-if="carregando" class="skeleton skeleton--num"></span>
              <template v-else>
                {{ cartao.valor }}<span class="stat__unit">{{ cartao.unidade }}</span>
              </template>
            </strong>
            <span class="stat__foot">{{ cartao.nota }}</span>
          </article>
        </div>
      </section>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';

const carregando = ref(true);
const erro = ref('');

const totalVaccinations = ref(0);
const totalFeedings = ref(0);
const totalMilkRecords = ref(0);
const totalWeighings = ref(0);

// Contador local reativo para capturar ações realizadas em tempo real nesta sessão
const localActionsIncrement = ref(0);

const dataPorExtenso = computed(() => {
  const texto = new Date().toLocaleDateString('pt-BR', {
    weekday: 'long',
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  });
  return texto.charAt(0).toUpperCase() + texto.slice(1);
});

const lancamentos = [
  { to: '/pesagem', icone: 'scale', titulo: 'Pesagem', descricao: 'Peso do animal na balança' },
  { to: '/lancamento-leite', icone: 'milk', titulo: 'Ordenha', descricao: 'Litros coletados por fêmea' },
  { to: '/vacinacao', icone: 'syringe', titulo: 'Vacinação', descricao: 'Individual ou lote do estábulo' },
  { to: '/lancamento-alimentacao', icone: 'feed', titulo: 'Alimentação', descricao: 'Ração e suplemento fornecidos' },
  { to: '/veterinario', icone: 'stethoscope', titulo: 'Veterinário', descricao: 'Consulta, motivo e tratativa' },
];

const indicadores = computed(() => [
  {
    icone: 'clipboard',
    rotulo: 'Ações de manejo',
    valor: totalFeedings.value + totalVaccinations.value + localActionsIncrement.value,
    unidade: 'lançamentos',
    nota: 'Alimentação e vacinação somadas',
  },
  {
    icone: 'chart',
    rotulo: 'Produção',
    valor: totalMilkRecords.value + totalWeighings.value,
    unidade: 'registros',
    nota: 'Ordenhas e pesagens coletadas',
  },
]);

const fetchOperationalMetrics = async () => {
  try {
    const [vaccinationsRes, feedingsRes, milkRes] = await Promise.all([
      api.getVaccinationsByAnimal(0),
      api.getFeedings(),
      api.getMilkProductions ? api.getMilkProductions() : { data: [] }
    ]);

    totalVaccinations.value = Array.isArray(vaccinationsRes.data) ? vaccinationsRes.data.length : 0;
    totalFeedings.value = Array.isArray(feedingsRes.data) ? feedingsRes.data.length : 0;
    totalMilkRecords.value = Array.isArray(milkRes.data) ? milkRes.data.length : 0;

    // Fallback de pesagens corporais coletadas se o método existir na sua api.js
    if (api.getWeightHistoryByAnimal) {
      const weightsRes = await api.getWeightHistoryByAnimal(0);
      totalWeighings.value = Array.isArray(weightsRes.data) ? weightsRes.data.length : 0;
    }
  } catch (error) {
    console.error('Erro ao buscar métricas de manejo do operador:', error);
    erro.value = 'Não foi possível carregar os totais. Os lançamentos continuam funcionando normalmente.';
  } finally {
    carregando.value = false;
  }
};

// Função ouvinte para interceptar quando o operador realiza um lançamento nas subpáginas
const checkLocalManejoUpdates = () => {
  const localSavedManejos = localStorage.getItem('ls_manejo_action_performed');
  if (localSavedManejos) {
    localActionsIncrement.value = parseInt(localSavedManejos, 10);
  }
};

onMounted(() => {
  window.addEventListener('storage', checkLocalManejoUpdates);
  fetchOperationalMetrics();
  checkLocalManejoUpdates();
});

onBeforeUnmount(() => {
  window.removeEventListener('storage', checkLocalManejoUpdates);
});
</script>

<style scoped>
.page > section { margin-top: 28px; }

.secao__titulo {
  margin-bottom: 12px;
  color: var(--text-2);
  font-size: var(--fs-sm);
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.skeleton--num {
  display: block;
  width: 56px;
  height: 28px;
}

/* Alvos grandes: quem usa esta tela costuma estar de luva, no curral. */
.acao {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  color: var(--text);
  text-decoration: none;
  transition: border-color var(--dur) var(--ease), background var(--dur) var(--ease);
}

.acao:hover {
  border-color: var(--accent-line);
  background: var(--surface-2);
  text-decoration: none;
}

.acao .icon-tile { width: 40px; height: 40px; }

.acao__texto { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.acao__texto strong { font-size: var(--fs-lg); font-weight: 600; }
.acao__texto span { color: var(--text-2); font-size: var(--fs-sm); }
</style>
