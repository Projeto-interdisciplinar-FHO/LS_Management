<template>
  <AppShell>
    <div v-if="animal && !loading" class="page">
      <PageHeader
        :titulo="animal.name || 'Sem nome'"
        :descricao="`Ficha individual · brinco #${animal.register_number}`"
        voltar-rotulo="Voltar"
      >
        <template #acoes>
          <span class="badge" :class="badgeSituacao(animal.status)">
            <span class="badge__dot"></span>
            {{ rotuloSituacao(animal.status) }}
          </span>
          <button class="btn btn--danger" :disabled="deleting" @click="deleteAnimal">
            <AppIcon name="trash" :size="15" />
            Excluir registro
          </button>
        </template>
      </PageHeader>

      <nav class="tabs" aria-label="Seções da ficha">
        <button
          v-for="aba in abasVisiveis"
          :key="aba.id"
          class="tabs__item"
          :class="{ 'is-active': activeTab === aba.id }"
          @click="activeTab = aba.id"
        >
          {{ aba.rotulo }}
        </button>
      </nav>

      <div class="conteudo">
        <!-- GERAL -->
        <div v-if="activeTab === 'geral'" class="grid grid--2">
          <section class="card">
            <header class="card__head">
              <h2 class="card__title">Informações do animal</h2>
              <button class="btn btn--sm" @click="toggleEdit">
                <AppIcon :name="isEditing ? 'close' : 'edit'" :size="14" />
                {{ isEditing ? 'Cancelar' : 'Editar' }}
              </button>
            </header>

            <div v-if="!isEditing" class="card__body">
              <div class="kv">
                <div class="kv__row"><span class="kv__key">Data de nascimento</span><span class="kv__val mono">{{ formatDate(animal.birth_date) }}</span></div>
                <div class="kv__row"><span class="kv__key">Sexo</span><span class="kv__val">{{ animal.sex === 'm' || animal.sex === 'M' ? 'Macho' : 'Fêmea' }}</span></div>
                <div class="kv__row">
                  <span class="kv__key">Situação</span>
                  <span class="kv__val">
                    <span class="badge" :class="badgeSituacao(animal.status)">{{ rotuloSituacao(animal.status) }}</span>
                  </span>
                </div>
              </div>
            </div>

            <form v-else @submit.prevent="updateAnimalInfo">
              <div class="card__body stack">
                <div class="field">
                  <label class="field__label" for="ed-nome">Nome / apelido</label>
                  <input id="ed-nome" v-model="editData.name" class="input" type="text" required>
                </div>
                <div class="field">
                  <label class="field__label" for="ed-nasc">Data de nascimento</label>
                  <input id="ed-nasc" v-model="editData.birth_date" class="input" type="date" required>
                </div>
                <div class="grid grid--2">
                  <div class="field">
                    <label class="field__label" for="ed-sexo">Sexo</label>
                    <select id="ed-sexo" v-model="editData.sex" class="select">
                      <option value="m">Macho</option>
                      <option value="f">Fêmea</option>
                    </select>
                  </div>
                  <div class="field">
                    <label class="field__label" for="ed-situacao">Situação</label>
                    <select id="ed-situacao" v-model="editData.status" class="select">
                      <option v-for="s in SITUACOES" :key="s.valor" :value="s.valor">{{ s.rotulo }}</option>
                    </select>
                  </div>
                </div>
              </div>
              <footer class="card__foot">
                <button type="submit" class="btn btn--primary" :disabled="saving">
                  {{ saving ? 'Salvando...' : 'Salvar alterações' }}
                </button>
              </footer>
            </form>
          </section>

          <section class="card">
            <header class="card__head">
              <h2 class="card__title">Classificação e localização</h2>
            </header>
            <div class="card__body">
              <div class="kv">
                <div class="kv__row"><span class="kv__key">Espécie</span><span class="kv__val">{{ rotulos.specie }}</span></div>
                <div class="kv__row"><span class="kv__key">Raça</span><span class="kv__val">{{ rotulos.breed }}</span></div>
                <div class="kv__row"><span class="kv__key">Estábulo</span><span class="kv__val">{{ rotulos.quadrant }}</span></div>
                <div class="kv__row"><span class="kv__key">Finalidade</span><span class="kv__val">{{ rotulos.purpose }}</span></div>
              </div>
            </div>
            <footer class="card__foot nota">
              <AppIcon name="lock" :size="15" />
              <span>Dados estruturais são alterados no cadastro base do animal.</span>
            </footer>
          </section>
        </div>

        <!-- HISTÓRICOS EM TABELA -->
        <section v-else-if="abaAtual && abaAtual.tabela" class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">{{ abaAtual.titulo }}</h2>
              <p v-if="abaAtual.descricao" class="card__desc">{{ abaAtual.descricao }}</p>
            </div>
            <span class="badge">{{ abaAtual.registros.length }}</span>
          </header>

          <div v-if="abaAtual.registros.length === 0" class="empty">
            <AppIcon :name="abaAtual.icone" :size="30" />
            <p class="empty__title">Sem registros</p>
            <p class="empty__desc">{{ abaAtual.vazio }}</p>
          </div>

          <div v-else class="table-wrap">
            <!-- LEITE -->
            <table v-if="activeTab === 'leite'" class="table">
              <thead><tr><th>Data da coleta</th><th>Quantidade</th></tr></thead>
              <tbody>
                <tr v-for="record in milkHistory" :key="record.id">
                  <td class="mono nowrap">{{ formatDate(record.production_date || record.date_collected || record.date) }}</td>
                  <td class="mono cell-strong">{{ record.milk_production || record.milk_quantity || record.quantity }} L</td>
                </tr>
              </tbody>
            </table>

            <!-- PESO -->
            <table v-else-if="activeTab === 'peso'" class="table">
              <thead><tr><th>Data da pesagem</th><th>Peso</th><th>Variação</th></tr></thead>
              <tbody>
                <tr v-for="(record, i) in pesagensOrdenadas" :key="record.id">
                  <td class="mono nowrap">{{ formatDate(record.weighing_date || record.date || record.date_weighed) }}</td>
                  <td class="mono cell-strong">{{ record.weight }} kg</td>
                  <!-- A pesagem só significa alguma coisa comparada com a anterior. -->
                  <td class="mono" :class="classeVariacao(i)">{{ variacao(i) }}</td>
                </tr>
              </tbody>
            </table>

            <!-- NUTRIÇÃO -->
            <table v-else-if="activeTab === 'nutricao'" class="table">
              <thead><tr><th>Data</th><th>Alimento</th><th>Quantidade</th></tr></thead>
              <tbody>
                <tr v-for="record in feedings" :key="record.id || record.feeding_time + record.animal">
                  <td class="mono nowrap">{{ formatDate(record.date_fed || record.feeding_time) }}</td>
                  <td>{{ record.feed_name || record.food?.name || '—' }}</td>
                  <td class="mono cell-strong">{{ record.quantity ? `${record.quantity} kg` : record.meal_weight ? `${record.meal_weight} kg` : '—' }}</td>
                </tr>
              </tbody>
            </table>

            <!-- VETERINÁRIO -->
            <table v-else-if="activeTab === 'veterinario'" class="table">
              <thead><tr><th>Data</th><th>Motivo</th><th>Tratativa</th><th>Veterinário</th><th class="cell-actions">Ações</th></tr></thead>
              <tbody>
                <tr v-for="record in healthRecords" :key="record.id || record.consultation_date + record.veterinarian">
                  <td class="mono nowrap">{{ formatDate(record.consultation_date) }}</td>
                  <td class="truncate" :title="record.consultation_reason || '—'">{{ record.consultation_reason || '—' }}</td>
                  <td class="truncate" :title="record.consultation_solution || '—'">{{ record.consultation_solution || '—' }}</td>
                  <td class="cell-strong">{{ record.veterinarian || '—' }}</td>
                  <td class="cell-actions">
                    <button class="btn btn--sm" @click="selectHealthRecord(record)">
                      {{ selectedHealthRecord === record ? 'Fechar' : 'Descritivo' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- VACINAS -->
            <table v-else-if="activeTab === 'vacinas'" class="table">
              <thead><tr><th>Data de aplicação</th><th>Vacina</th><th>Situação</th></tr></thead>
              <tbody>
                <tr v-for="vaccine in vaccineHistory" :key="vaccine.id">
                  <td class="mono nowrap">{{ formatDate(vaccine.vaccination_date || vaccine.date || vaccine.date_applied) }}</td>
                  <td class="cell-strong">{{ vaccine.vaccine_name || vaccine.name }}</td>
                  <td><span class="badge badge--ok"><span class="badge__dot"></span> Protegido</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="activeTab === 'veterinario' && selectedHealthRecord" class="descritivo">
            <div class="row--between">
              <h3 class="card__title">Descritivo da consulta</h3>
              <div class="row">
                <button class="btn btn--sm btn--danger" @click="deleteHealthRecord(selectedHealthRecord)">Excluir</button>
                <button class="btn btn--sm" @click="selectedHealthRecord = null">Fechar</button>
              </div>
            </div>
            <div class="kv">
              <div class="kv__row"><span class="kv__key">Motivo</span><span class="kv__val">{{ selectedHealthRecord.consultation_reason || '—' }}</span></div>
              <div class="kv__row"><span class="kv__key">Tratativa</span><span class="kv__val">{{ selectedHealthRecord.consultation_solution || '—' }}</span></div>
              <div class="kv__row"><span class="kv__key">Veterinário</span><span class="kv__val">{{ selectedHealthRecord.veterinarian || '—' }}</span></div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <div v-else class="page">
      <div class="card">
        <div v-if="loading" class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Carregando a ficha do animal...
        </div>
        <!-- Se a busca falha, `animal` fica nulo: antes o spinner girava para
             sempre, sem dizer que tinha dado errado. -->
        <div v-else class="empty">
          <AppIcon name="alert" :size="30" />
          <p class="empty__title">Ficha não carregada</p>
          <p class="empty__desc">
            Não foi possível buscar este animal. Ele pode ter sido excluído,
            ou o servidor não respondeu.
          </p>
          <div class="row">
            <button class="btn" @click="loadCompleteAnimalData">Tentar de novo</button>
            <button class="btn btn--primary" @click="$router.push('/animais')">Ver lista de animais</button>
          </div>
        </div>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import { confirmar } from '@/services/confirmService';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { SITUACOES, ativoPara, badgeSituacao, rotuloSituacao } from '@/utils/statusUtils';

const route = useRoute();
const router = useRouter();

const animal = ref(null);
const loading = ref(true);
const saving = ref(false);
const deleting = ref(false);
const activeTab = ref('geral');
const isEditing = ref(false);

const isFemaleAnimal = (animalData) => String(animalData?.sex || '').toLowerCase() === 'f';
const showMilkTab = computed(() => animal.value ? isFemaleAnimal(animal.value) : false);

const milkHistory = ref([]);
const vaccineHistory = ref([]);
const weightHistory = ref([]);
const feedings = ref([]);
const healthRecords = ref([]);
const selectedHealthRecord = ref(null);

const editData = ref({
  name: '',
  birth_date: '',
  sex: '',
  status: 'ativo',
  active: true
});

/*
 * O AnimalSerializer e `fields = '__all__'`: devolve so os ids das chaves
 * estrangeiras, nunca `specie_name`, `breed_name` ou `quadrant_name`. A ficha
 * lia esses tres campos e por isso mostrava "—" mesmo com o animal cadastrado
 * corretamente.
 *
 * Resolvemos os nomes aqui, cruzando com os cadastros — e o que a tela de
 * Consulta ja fazia.
 */
const cadastros = ref({ species: [], breeds: [], quadrants: [], purposes: [] });

const idDe = (valor) => (valor && typeof valor === 'object' ? valor.id : valor);

const nomeEm = (lista, valor) => {
  const id = idDe(valor);
  if (id === null || id === undefined || id === '') return '—';
  const achado = lista.find((item) => String(item.id) === String(id));
  return achado?.name || achado?.tipo || '—';
};

const rotulos = computed(() => ({
  specie: nomeEm(cadastros.value.species, animal.value?.specie),
  breed: nomeEm(cadastros.value.breeds, animal.value?.breed),
  quadrant: nomeEm(cadastros.value.quadrants, animal.value?.quadrant),
  purpose: nomeEm(cadastros.value.purposes, animal.value?.purpose),
}));

const carregarCadastros = async () => {
  const lista = (resposta) => resposta.data?.results || resposta.data || [];
  const vazio = { data: [] };
  const [sp, br, qd, pp] = await Promise.all([
    api.get('species/').catch(() => vazio),
    api.get('breeds/').catch(() => vazio),
    api.get('quadrants/').catch(() => vazio),
    api.get('purpose_types/').catch(() => vazio),
  ]);
  cadastros.value = {
    species: lista(sp), breeds: lista(br), quadrants: lista(qd), purposes: lista(pp),
  };
};

// As abas eram seis blocos de marcação repetida, cada um com o seu cabeçalho
// e o seu estado vazio copiado. Aqui viram dados; a marcação sobrou uma vez.
const abas = computed(() => [
  { id: 'geral', rotulo: 'Geral' },
  {
    id: 'leite',
    rotulo: 'Ordenha',
    tabela: true,
    icone: 'milk',
    titulo: 'Histórico de produção de leite',
    vazio: 'Nenhuma ordenha lançada para este animal.',
    registros: milkHistory.value,
    somenteFemea: true,
  },
  {
    id: 'peso',
    rotulo: 'Pesagens',
    tabela: true,
    icone: 'scale',
    titulo: 'Histórico de pesagens',
    vazio: 'Nenhuma pesagem registrada para este animal.',
    registros: weightHistory.value,
  },
  {
    id: 'nutricao',
    rotulo: 'Alimentação',
    tabela: true,
    icone: 'feed',
    titulo: 'Registro de alimentação',
    descricao: 'Rações e suplementos fornecidos ao animal.',
    vazio: 'Nenhum registro de alimentação encontrado.',
    registros: feedings.value,
  },
  {
    id: 'veterinario',
    rotulo: 'Veterinário',
    tabela: true,
    icone: 'stethoscope',
    titulo: 'Atendimentos veterinários',
    descricao: 'Consultas, medicamentos e tratativas aplicadas.',
    vazio: 'Nenhum atendimento veterinário encontrado.',
    registros: healthRecords.value,
  },
  {
    id: 'vacinas',
    rotulo: 'Vacinas',
    tabela: true,
    icone: 'syringe',
    titulo: 'Histórico de vacinação',
    vazio: 'Nenhuma vacina aplicada registrada.',
    registros: vaccineHistory.value,
  },
]);

const abasVisiveis = computed(() => abas.value.filter((aba) => !aba.somenteFemea || showMilkTab.value));
const abaAtual = computed(() => abas.value.find((aba) => aba.id === activeTab.value));

// Pesagens da mais recente para a mais antiga, para calcular a variação.
const pesoNumerico = (registro) => parseFloat(registro?.weight) || 0;
const dataPesagem = (registro) => new Date(registro.weighing_date || registro.date || registro.date_weighed || 0);

const pesagensOrdenadas = computed(() =>
  [...weightHistory.value].sort((a, b) => dataPesagem(b) - dataPesagem(a))
);

const variacao = (indice) => {
  const anterior = pesagensOrdenadas.value[indice + 1];
  if (!anterior) return '—';
  const delta = pesoNumerico(pesagensOrdenadas.value[indice]) - pesoNumerico(anterior);
  if (!delta) return '0,0 kg';
  return `${delta > 0 ? '+' : '−'}${Math.abs(delta).toFixed(1)} kg`;
};

const classeVariacao = (indice) => {
  const anterior = pesagensOrdenadas.value[indice + 1];
  if (!anterior) return 'text-subtle';
  const delta = pesoNumerico(pesagensOrdenadas.value[indice]) - pesoNumerico(anterior);
  if (delta > 0) return 'variacao--ganho';
  if (delta < 0) return 'variacao--perda';
  return 'text-subtle';
};

onMounted(async () => {
  carregarCadastros();
  await loadCompleteAnimalData();
});

const loadCompleteAnimalData = async () => {
  loading.value = true;
  const id = route.params.id;
  try {
    const response = await api.get(`animals/${id}/`);
    animal.value = response.data;
    editData.value = { ...response.data };

    try {
      const milkRes = await api.getMilkProductionByAnimal(id);
      const data = milkRes.data.historico || milkRes.data.results || milkRes.data;
      milkHistory.value = Array.isArray(data) ? data : [];
    } catch (e) { milkHistory.value = []; }

    try {
      const weightRes = await api.getWeightHistoryByAnimal(id);
      const data = weightRes.data.historico || weightRes.data.results || weightRes.data;
      weightHistory.value = Array.isArray(data) ? data : [];
    } catch (e) { weightHistory.value = []; }

    try {
      const feedingRes = await api.getFeedingsByAnimal(id);
      const data = feedingRes.data.results || feedingRes.data;
      feedings.value = Array.isArray(data) ? data : [];
    } catch (e) { feedings.value = []; }

    try {
      const vaccineRes = await api.getVaccinationsByAnimal(id);
      const data = vaccineRes.data.results || vaccineRes.data;
      vaccineHistory.value = Array.isArray(data) ? data : [];
    } catch (e) { vaccineHistory.value = []; }

    try {
      const healthRes = await api.getVeterinaryRecords(id);
      const data = healthRes.data.results || healthRes.data;
      healthRecords.value = Array.isArray(data) ? data : [];
    } catch (e) { healthRecords.value = []; }

  } catch (error) {
    console.error("Erro ao carregar dados:", error);
  } finally {
    loading.value = false;
  }
};

const selectHealthRecord = (record) => {
  selectedHealthRecord.value = selectedHealthRecord.value === record ? null : record;
};

const deleteHealthRecord = async (record) => {
  if (!record?.id) return;
  const ok = await confirmar({
    titulo: 'Excluir este atendimento?',
    texto: 'O registro sai da ficha do animal e do histórico veterinário.',
    acao: 'Excluir',
  });
  if (!ok) return;
  try {
    await api.deleteVeterinaryRecord(record.id);
    healthRecords.value = healthRecords.value.filter(item => item.id !== record.id);
    selectedHealthRecord.value = null;
  } catch (error) {
  }
};

const toggleEdit = () => {
  isEditing.value = !isEditing.value;
  if (!isEditing.value && animal.value) {
    editData.value = { ...animal.value };
  }
};

const updateAnimalInfo = async () => {
  saving.value = true;
  try {
    // `active` acompanha o `status`, como no cadastro.
    const dados = { ...editData.value, active: ativoPara(editData.value.status) };
    await api.patch(`animals/${animal.value.id}/`, dados);
    animal.value = { ...animal.value, ...dados };
    isEditing.value = false;
  } catch (error) {
  } finally {
    saving.value = false;
  }
};

const deleteAnimal = async () => {
  if (deleting.value) return;
  const ok = await confirmar({
    titulo: `Excluir ${animal.value?.name || 'este animal'}?`,
    texto: 'A ficha e todo o histórico de pesagem, ordenha e vacinação são removidos.',
    acao: 'Excluir registro',
  });
  if (ok) {
    deleting.value = true;
    try {
      await api.deleteAnimal(animal.value.id);
      router.push('/animais');
    } catch (error) {
      // "Erro ao excluir registro" nao dizia nada. O backend devolve o motivo
      // no corpo da resposta; mostrar isso e a diferenca entre a pessoa
      // entender o que houve e abrir um chamado.
    } finally {
      deleting.value = false;
    }
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
};

/** Extrai o motivo que o backend mandou; cai no padrão quando não há um. */
function motivoDoErro(erro, padrao) {
  const status = erro?.response?.status;
  if (status >= 500) {
    return 'O servidor falhou ao excluir este animal. Avise o suporte técnico.';
  }
  const dados = erro?.response?.data;
  if (!dados) return padrao;
  if (typeof dados === 'string') return dados;
  if (dados.detail) return dados.detail;
  const campos = Object.entries(dados)
    .map(([campo, msgs]) => `${campo}: ${[].concat(msgs).join(' ')}`)
    .join(' · ');
  return campos || padrao;
}
</script>

<style scoped>
.conteudo { margin-top: 20px; }

.nota {
  align-items: flex-start;
  justify-content: flex-start;
  gap: 9px;
  color: var(--text-3);
  font-size: var(--fs-sm);
}

.nota svg { flex: none; }

.variacao--ganho { color: var(--ok); }
.variacao--perda { color: var(--danger); }

.descritivo {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 18px 20px;
  border-top: 1px solid var(--line);
  background: var(--surface-2);
  border-radius: 0 0 var(--r-lg) var(--r-lg);
}
</style>
