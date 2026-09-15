<template>
  <AppShell>
    <div class="page">
      <header class="page__head">
        <div>
          <h1 class="page__title">Painel administrativo</h1>
          <p class="page__desc">{{ dataPorExtenso }}</p>
        </div>
        <div class="page__actions">
          <RouterLink to="/relatorios" class="btn">
            <AppIcon name="chart" :size="16" />
            Relatórios
          </RouterLink>
          <RouterLink to="/animais/novo" class="btn btn--primary">
            <AppIcon name="plus" :size="16" />
            Novo animal
          </RouterLink>
        </div>
      </header>

      <p v-if="erro" class="alert alert--warn" role="status">
        <AppIcon name="alert" :size="16" />
        <span>{{ erro }}</span>
      </p>

      <!-- Números do dia. Uma linha, sem foto de banco de imagens em cima. -->
      <section class="grid grid--auto" aria-label="Indicadores">
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
      </section>

      <!-- Atalhos para o que se faz todo dia, em vez de forçar a caça pelo menu. -->
      <section class="secao">
        <h2 class="secao__titulo">Ações frequentes</h2>
        <div class="grid grid--auto">
          <RouterLink v-for="atalho in atalhos" :key="atalho.to" :to="atalho.to" class="atalho">
            <span class="icon-tile icon-tile--accent"><AppIcon :name="atalho.icone" :size="17" /></span>
            <span class="atalho__texto">
              <strong>{{ atalho.titulo }}</strong>
              <span>{{ atalho.descricao }}</span>
            </span>
            <AppIcon name="chevron-right" :size="16" class="atalho__seta" />
          </RouterLink>
        </div>
      </section>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';

const carregando = ref(true);
const erro = ref('');
const totalAnimals = ref(0);
const totalQuadrants = ref(0);
const totalVaccinations = ref(0);
const totalFeedings = ref(0);

const dataPorExtenso = computed(() => {
  const texto = new Date().toLocaleDateString('pt-BR', {
    weekday: 'long',
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  });
  return texto.charAt(0).toUpperCase() + texto.slice(1);
});

const indicadores = computed(() => [
  {
    icone: 'animal',
    rotulo: 'Rebanho',
    valor: totalAnimals.value,
    unidade: 'cabeças',
    nota: 'Animais registrados no sistema',
  },
  {
    icone: 'barn',
    rotulo: 'Estábulos',
    valor: totalQuadrants.value,
    unidade: 'quadrantes',
    nota: 'Instalações ativas para alocação',
  },
  {
    icone: 'syringe',
    rotulo: 'Vacinações',
    valor: totalVaccinations.value,
    unidade: 'registros',
    nota: 'Aplicações lançadas até agora',
  },
  {
    icone: 'feed',
    rotulo: 'Alimentação',
    valor: totalFeedings.value,
    unidade: 'registros',
    nota: 'Tratos lançados pelo campo',
  },
]);

const atalhos = [
  { to: '/pesagem', icone: 'scale', titulo: 'Registrar pesagem', descricao: 'Peso individual com data da balança' },
  { to: '/lancamento-leite', icone: 'milk', titulo: 'Lançar ordenha', descricao: 'Produção diária por fêmea' },
  { to: '/vacinacao', icone: 'syringe', titulo: 'Aplicar vacina', descricao: 'Individual ou lote inteiro do estábulo' },
  { to: '/lancamento-alimentacao', icone: 'feed', titulo: 'Lançar alimentação', descricao: 'Consumo de ração e suplemento' },
  { to: '/veterinario', icone: 'stethoscope', titulo: 'Atendimento veterinário', descricao: 'Motivo, tratativa e responsável' },
  { to: '/saude', icone: 'alert', titulo: 'Vacinas em atraso', descricao: 'Reforços vencidos e da próxima semana' },
];

async function fetchMetrics() {
  try {
    const [animalsRes, quadrantsRes, vaccinationsRes, feedingsRes] = await Promise.all([
      api.getAnimals(),
      api.getQuadrants(),
      api.getVaccinationsByAnimal(0),
      api.getFeedings()
    ]);

    totalAnimals.value = Array.isArray(animalsRes.data) ? animalsRes.data.length : 0;
    totalQuadrants.value = Array.isArray(quadrantsRes.data) ? quadrantsRes.data.length : 0;
    totalVaccinations.value = Array.isArray(vaccinationsRes.data) ? vaccinationsRes.data.length : 0;
    totalFeedings.value = Array.isArray(feedingsRes.data) ? feedingsRes.data.length : 0;
  } catch (error) {
    // O painel ficava com quatro zeros e o motivo morria no console.
    console.error('Erro ao carregar métricas do painel administrativo', error);
    erro.value = 'Não foi possível carregar os números do painel. Os demais atalhos continuam funcionando.';
  } finally {
    carregando.value = false;
  }
}

onMounted(fetchMetrics);
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

.atalho {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 14px 16px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  color: var(--text);
  text-decoration: none;
  transition: border-color var(--dur) var(--ease), background var(--dur) var(--ease);
}

.atalho:hover {
  border-color: var(--accent-line);
  background: var(--surface-2);
  text-decoration: none;
}

.atalho__texto {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
  flex: 1;
}

.atalho__texto strong { font-size: var(--fs-md); font-weight: 500; }
.atalho__texto span { color: var(--text-2); font-size: var(--fs-sm); }

.atalho__seta { color: var(--text-3); flex: none; }
</style>
