<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Saúde e vacinação"
        descricao="Controle de reforços: o que venceu, o que vence na semana e o que está em dia."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <div v-if="loading" class="card">
        <div class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Carregando dados de vacinação...
        </div>
      </div>

      <template v-else>
        <!-- Atrasado primeiro: é o único número desta tela que exige ação hoje. -->
        <section class="grid grid--3" aria-label="Resumo sanitário">
          <article class="stat" :class="{ 'stat--alerta': overdueCount > 0 }">
            <span class="stat__label"><AppIcon name="alert" :size="15" /> Atrasadas</span>
            <strong class="stat__value">{{ overdueCount }}</strong>
            <span class="stat__foot">Reforço já vencido</span>
          </article>
          <article class="stat">
            <span class="stat__label"><AppIcon name="calendar" :size="15" /> Próximos 7 dias</span>
            <strong class="stat__value">{{ upcomingCount }}</strong>
            <span class="stat__foot">Programar aplicação</span>
          </article>
          <article class="stat">
            <span class="stat__label"><AppIcon name="check-circle" :size="15" /> Em dia</span>
            <strong class="stat__value">{{ upToDateCount }}</strong>
            <span class="stat__foot">Sem pendência de reforço</span>
          </article>
        </section>

        <div class="toolbar toolbar--filtros">
          <div class="segmented" role="group" aria-label="Filtrar vacinações">
            <button
              v-for="filter in vaccineFilters"
              :key="filter.value"
              class="segmented__item"
              :class="{ 'is-active': activeFilter === filter.value }"
              @click="activeFilter = filter.value"
            >
              {{ filter.label }}
              <span class="count">{{ getCountByFilter(filter.value) }}</span>
            </button>
          </div>
        </div>

        <section class="card">
          <header class="card__head">
            <h2 class="card__title">{{ getFilterLabel(activeFilter) }}</h2>
            <span class="badge">{{ filteredVaccinations.length }}</span>
          </header>

          <div v-if="filteredVaccinations.length === 0" class="empty">
            <AppIcon name="inbox" :size="30" />
            <p class="empty__title">Nada neste filtro</p>
            <p class="empty__desc">Nenhuma vacinação corresponde ao filtro selecionado.</p>
          </div>

          <div v-else class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>Animal</th>
                  <th>Brinco</th>
                  <th>Vacina</th>
                  <th>Aplicada</th>
                  <th>Próxima dose</th>
                  <th>Dosagem</th>
                  <th>Situação</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="vac in filteredVaccinations" :key="vac.id">
                  <td class="cell-strong">{{ vac.animal_name || '—' }}</td>
                  <td class="mono">{{ brinco(vac) }}</td>
                  <td>{{ vac.vaccine_name }}</td>
                  <td class="mono nowrap">{{ formatDate(vac.vaccination_date) }}</td>
                  <td class="nowrap">
                    <span class="mono">{{ formatDate(vac.next_vaccination_date) }}</span>
                    <span v-if="getDaysInfo(vac)" class="prazo" :class="{ 'prazo--vencido': isOverdue(vac) }">
                      {{ getDaysInfo(vac) }}
                    </span>
                  </td>
                  <td class="mono">{{ vac.dosage }} mL</td>
                  <td>
                    <span class="badge" :class="badgeSituacao(vac)">
                      <span class="badge__dot"></span>
                      {{ getStatusLabel(vac) }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </template>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/services/api';
import { painelDoPapel } from '@/services/auth';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';

const painel = computed(() => painelDoPapel());

const loading = ref(true);
const vaccinations = ref([]);
const activeFilter = ref('all');

/*
 * O VaccinationSerializer devolve `animal` (o id da chave estrangeira), nao
 * `animal_id` — este ultimo so existe no endpoint por animal, que monta o JSON
 * a mao. A tela lia `animal_id` da listagem e imprimia "#undefined".
 *
 * E o id interno nao e o brinco: `register_number` nao e exposto pelo
 * serializer. Entao buscamos os animais junto e resolvemos o numero aqui,
 * como a tela de Consulta ja fazia.
 */
const brincoPorAnimal = ref({});

const brinco = (vac) => {
  const registro = brincoPorAnimal.value[vac.animal];
  return registro ? `#${registro}` : '—';
};

const vaccineFilters = [
  { value: 'all', label: 'Todas' },
  { value: 'overdue', label: 'Atrasadas' },
  { value: 'upcoming', label: 'Próximos 7 dias' },
  { value: 'uptodate', label: 'Em dia' }
];

const filteredVaccinations = computed(() => {
  if (activeFilter.value === 'all') {
    return [...vaccinations.value].sort((a, b) => new Date(b.vaccination_date) - new Date(a.vaccination_date));
  }
  if (activeFilter.value === 'overdue') {
    return vaccinations.value.filter(v => isOverdue(v)).sort((a, b) => new Date(a.next_vaccination_date) - new Date(b.next_vaccination_date));
  }
  if (activeFilter.value === 'upcoming') {
    return vaccinations.value.filter(v => isUpcoming(v)).sort((a, b) => new Date(a.next_vaccination_date) - new Date(b.next_vaccination_date));
  }
  if (activeFilter.value === 'uptodate') {
    return vaccinations.value.filter(v => !isOverdue(v) && !isUpcoming(v)).sort((a, b) => new Date(b.vaccination_date) - new Date(a.vaccination_date));
  }
  return vaccinations.value;
});

const overdueCount = computed(() => vaccinations.value.filter(v => isOverdue(v)).length);
const upcomingCount = computed(() => vaccinations.value.filter(v => isUpcoming(v)).length);
const upToDateCount = computed(() => vaccinations.value.filter(v => !isOverdue(v) && !isUpcoming(v)).length);

const formatDate = (dateStr) => {
  if (!dateStr) return '—';
  const date = new Date(dateStr);
  return date.toLocaleDateString('pt-BR');
};

// O serializer ja devolve `is_overdue` e `days_until_next` calculados no
// servidor, com o fuso dele. Usamos o que vem e so calculamos aqui quando a
// resposta nao traz o campo — o endpoint por animal, por exemplo, nao traz.
const isOverdue = (vac) => {
  if (typeof vac.is_overdue === 'boolean') return vac.is_overdue;
  if (!vac.next_vaccination_date) return false;
  return new Date(vac.next_vaccination_date) < new Date();
};

const isUpcoming = (vac) => {
  const dias = diasAteProxima(vac);
  if (dias === null) return false;
  return dias >= 0 && dias <= 7;
};

const diasAteProxima = (vac) => {
  if (typeof vac.days_until_next === 'number') return vac.days_until_next;
  if (!vac.next_vaccination_date) return null;
  const hoje = new Date();
  hoje.setHours(0, 0, 0, 0);
  return Math.ceil((new Date(vac.next_vaccination_date) - hoje) / 86400000);
};

const getDaysInfo = (vac) => {
  const diff = diasAteProxima(vac);
  if (diff === null) return null;
  if (diff < 0) return `${Math.abs(diff)} dias atrás`;
  if (diff === 0) return 'hoje';
  return `em ${diff} dias`;
};

const getStatusLabel = (vac) => {
  if (isOverdue(vac)) return 'Atrasada';
  if (isUpcoming(vac)) return 'Próxima semana';
  return 'Em dia';
};

const badgeSituacao = (vac) => {
  if (isOverdue(vac)) return 'badge--danger';
  if (isUpcoming(vac)) return 'badge--warn';
  return 'badge--ok';
};

const getCountByFilter = (filter) => {
  if (filter === 'all') return vaccinations.value.length;
  if (filter === 'overdue') return overdueCount.value;
  if (filter === 'upcoming') return upcomingCount.value;
  if (filter === 'uptodate') return upToDateCount.value;
  return 0;
};

const getFilterLabel = (filter) => {
  const f = vaccineFilters.find(f => f.value === filter);
  return f ? f.label : 'Todas';
};

onMounted(async () => {
  try {
    const [vacRes, animaisRes] = await Promise.all([
      api.getVaccinationsByAnimal(0), // 0 significa todas
      api.getAnimals().catch(() => ({ data: [] })),
    ]);

    vaccinations.value = Array.isArray(vacRes.data) ? vacRes.data : vacRes.data.results || [];

    const animais = animaisRes.data.results || animaisRes.data || [];
    brincoPorAnimal.value = Object.fromEntries(
      animais.map((a) => [a.id, a.register_number])
    );
  } catch (error) {
    console.error("Erro ao buscar vacinações:", error);
    vaccinations.value = [];
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.stat--alerta {
  border-color: var(--danger-line);
  background: var(--danger-soft);
}

.stat--alerta .stat__value,
.stat--alerta .stat__label,
.stat--alerta .stat__foot { color: var(--danger); }

.toolbar--filtros { margin-top: 24px; }

.prazo {
  display: block;
  margin-top: 2px;
  color: var(--text-3);
  font-size: var(--fs-xs);
}

.prazo--vencido { color: var(--danger); }
</style>
