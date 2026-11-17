<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Nascimento e genealogia"
        descricao="Registre nascimentos e consulte a ascendência direta disponível na API."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <p v-if="error" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ error }}</span>
      </p>
      <p v-if="notice" class="alert alert--warn" role="status">
        <AppIcon name="alert" :size="16" />
        <span>{{ notice }}</span>
      </p>

      <nav class="tabs birth-genealogy__tabs" role="tablist" aria-label="Nascimento e genealogia">
        <button
          id="tab-birth"
          type="button"
          role="tab"
          class="tabs__item"
          :class="{ 'is-active': activeTab === 'birth' }"
          :aria-selected="activeTab === 'birth'"
          aria-controls="panel-birth"
          :tabindex="activeTab === 'birth' ? 0 : -1"
          @keydown.right.prevent="activeTab = 'genealogy'"
          @click="activeTab = 'birth'"
        >
          <AppIcon name="animal" :size="15" />
          Nascimento
        </button>
        <button
          id="tab-genealogy"
          type="button"
          role="tab"
          class="tabs__item"
          :class="{ 'is-active': activeTab === 'genealogy' }"
          :aria-selected="activeTab === 'genealogy'"
          aria-controls="panel-genealogy"
          :tabindex="activeTab === 'genealogy' ? 0 : -1"
          @keydown.left.prevent="activeTab = 'birth'"
          @click="activeTab = 'genealogy'"
        >
          <AppIcon name="dna" :size="15" />
          Árvore genealógica
        </button>
      </nav>

      <div
        v-if="activeTab === 'birth'"
        id="panel-birth"
        class="birth-genealogy__panel"
        role="tabpanel"
        aria-labelledby="tab-birth"
        tabindex="0"
      >
        <p class="alert alert--info" role="status">
          <AppIcon name="info" :size="16" />
          <span>Registre a data, o peso e como foi o nascimento. Quando o bezerro vem de uma inseminação cadastrada, a mãe e o pai aparecem automaticamente na lista.</span>
        </p>

        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Registrar nascimento</h2>
              <p class="card__desc">O registro será associado ao bovino escolhido após ser criado.</p>
            </div>
          </header>

          <form class="card__body stack" @submit.prevent="saveBirth">
            <div class="grid grid--2">
              <div class="field">
                <label class="field__label" for="calf">Bovino</label>
                <select id="calf" v-model.number="form.animalId" class="select" required :disabled="loading || saving || Boolean(pendingLink)">
                  <option value="" disabled>Selecione um bovino sem nascimento vinculado...</option>
                  <option v-for="animal in animalsWithoutBirth" :key="animal.id" :value="animal.id">
                    {{ animal.name }} · #{{ animal.register_number }}
                  </option>
                </select>
              </div>
              <div class="field">
                <label class="field__label" for="birth-occurrence">Ocorrência</label>
                <select id="birth-occurrence" v-model.number="form.occurrence" class="select" required :disabled="loading || saving">
                  <option value="" disabled>Selecione...</option>
                  <option v-for="occurrence in occurrences" :key="occurrence.id" :value="occurrence.id">{{ occurrence.description }}</option>
                </select>
              </div>
              <div class="field">
                <label class="field__label" for="birth-date">Data do nascimento</label>
                <input id="birth-date" v-model="form.date" class="input" type="date" required :disabled="saving">
              </div>
              <div class="field">
                <label class="field__label" for="birth-weight">Peso ao nascer (kg)</label>
                <input id="birth-weight" v-model.number="form.weight" class="input" type="number" min="0" step="0.01" required :disabled="saving">
              </div>
              <div class="field span-full">
                <label class="field__label" for="birth-insemination">Inseminação relacionada (opcional)</label>
                <select id="birth-insemination" v-model.number="form.insemination" class="select" :disabled="loading || saving">
                  <option value="">Não informada</option>
                  <option v-for="item in inseminations" :key="item.id" :value="item.id">
                    {{ inseminationLabel(item) }}
                  </option>
                </select>
              </div>
            </div>

            <div v-if="pendingLink" class="alert alert--warn" role="status">
              Nascimento {{ pendingLink.birthId }} criado, mas ainda não foi vinculado ao bovino.
              <button type="button" class="btn btn--sm" :disabled="saving" @click="retryLink">Tentar vincular</button>
            </div>

            <footer class="row row--between">
              <span class="text-muted">{{ animalsWithoutBirth.length }} bovino(s) sem nascimento vinculado</span>
              <button type="submit" class="btn btn--primary" :disabled="loading || saving || !ready">
                {{ saving ? 'Salvando...' : pendingLink ? 'Vínculo pendente' : 'Registrar nascimento' }}
              </button>
            </footer>
          </form>
        </section>

        <section class="card birth-list">
          <header class="card__head">
            <div>
              <h2 class="card__title">Nascimentos vinculados</h2>
              <p class="card__desc">Ascendência limitada aos dados de inseminação disponíveis.</p>
            </div>
            <span class="badge">{{ linkedBirths.length }}</span>
          </header>
          <div v-if="loading" class="loading"><span class="spinner" aria-hidden="true"></span>Carregando nascimentos...</div>
          <div v-else-if="!linkedBirths.length" class="empty">
            <AppIcon name="dna" :size="28" />
            <p class="empty__desc">Nenhum nascimento está vinculado a um bovino.</p>
          </div>
          <div v-else class="table-wrap">
            <table class="table">
              <thead>
                <tr><th>Bovino</th><th>Data</th><th>Peso</th><th>Ocorrência</th><th>Mãe</th><th>Pai</th></tr>
              </thead>
              <tbody>
                <tr v-for="item in linkedBirths" :key="item.animal.id">
                  <td class="cell-strong">{{ item.animal.name }} <span class="mono">#{{ item.animal.register_number }}</span></td>
                  <td class="mono nowrap">{{ formatDate(item.birth.date) }}</td>
                  <td class="mono">{{ item.birth.weight }} kg</td>
                  <td>{{ occurrenceName(item.birth.occurrence) }}</td>
                  <td>{{ parentName(item.insemination?.mother, animals) }}</td>
                  <td>{{ parentName(item.insemination?.father, bulls) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>

      <section
        v-if="activeTab === 'genealogy'"
        id="panel-genealogy"
        class="card genealogy-card"
        role="tabpanel"
        aria-labelledby="tab-genealogy"
        tabindex="0"
      >
        <header class="card__head genealogy-card__head">
          <div>
            <h2 class="card__title">Árvore genealógica</h2>
            <p class="card__desc">Consulte a ascendência disponível até bisavós.</p>
          </div>
          <div class="field genealogy-card__select">
            <label class="field__label" for="genealogy-animal">Animal</label>
            <select id="genealogy-animal" v-model="selectedAnimalId" class="select" :disabled="loading || !animals.length">
              <option value="">Selecione um bovino...</option>
              <option v-for="animal in animals" :key="animal.id" :value="String(animal.id)">
                {{ animal.name || 'Sem nome' }} · #{{ animal.register_number }}
              </option>
            </select>
          </div>
        </header>

        <div v-if="loading" class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Carregando ascendência...
        </div>
        <div v-else-if="!animals.length" class="empty">
          <AppIcon name="dna" :size="28" />
          <p class="empty__title">Nenhum bovino disponível</p>
          <p class="empty__desc">Cadastre animais para consultar a genealogia.</p>
        </div>
        <div v-else-if="!selectedAnimal" class="empty genealogy-card__empty">
          <AppIcon name="dna" :size="28" />
          <p class="empty__title">Selecione um animal</p>
          <p class="empty__desc">A árvore será montada com os vínculos de ascendência registrados.</p>
        </div>
        <div v-else class="genealogy__layout">
          <section class="genealogy__tree-panel" aria-labelledby="genealogy-tree-title">
            <header class="genealogy__tree-head">
              <div>
                <h3 id="genealogy-tree-title" class="card__title">{{ selectedAnimal.name || 'Sem nome' }} — árvore genealógica</h3>
                <p class="card__desc">Selecione uma vaca da árvore para consultar sua ascendência.</p>
              </div>
              <span class="badge">{{ ascendentesConhecidos }} de 14 ascendentes</span>
            </header>

            <p class="alert alert--warn genealogy__notice" role="status">
              <AppIcon name="info" :size="16" />
              <span>
                {{ ascendentesAusentes
                  ? `Ascendência incompleta: ${ascendentesAusentes} vínculo(s) não informado(s) ou indisponível(is). A ausência de dados não confirma que um cruzamento seja seguro.`
                  : 'A árvore é baseada nos vínculos de nascimento e inseminação disponíveis na API.' }}
              </span>
            </p>

            <div class="genealogy__canvas" role="group" :aria-label="`Árvore genealógica de ${selectedAnimal.name || 'animal selecionado'}`">
              <section
                v-for="generation in treeRows"
                :key="generation.label"
                class="genealogy__generation"
                :aria-label="generation.label"
              >
                <h4 class="genealogy__generation-label">{{ generation.label }}</h4>
                <div class="genealogy__nodes">
                  <button
                    v-for="node in generation.nodes"
                    :key="node.key"
                    type="button"
                    class="genealogy__node"
                    :class="{
                      'genealogy__node--root': node.generation === 0,
                      'genealogy__node--missing': !node.animal,
                      'genealogy__node--cycle': node.cycle,
                      'genealogy__node--current': node.animal && String(node.animal.id) === selectedAnimalId,
                    }"
                    :style="{ gridColumn: `span ${node.columnSpan}` }"
                    :disabled="!node.animal || node.kind !== 'cow' || String(node.animal.id) === selectedAnimalId"
                    :aria-label="node.cycle
                      ? `${node.relationship}: ciclo de parentesco detectado para ${node.animal.name || 'animal sem nome'}, brinco ${node.animal.register_number}.`
                      : node.animal
                      ? `${node.relationship}: ${node.animal.name || 'Sem nome'}, brinco ${node.animal.register_number}.${node.kind === 'cow' ? ' Consultar esta vaca.' : ' Ascendência do touro indisponível.'}`
                      : `${node.relationship}: ${node.missingReason}`"
                    @click="selectedAnimalId = String(node.animal.id)"
                  >
                    <span class="genealogy__relation">{{ node.relationship }}</span>
                    <strong>{{ node.animal?.name || 'Ascendente não cadastrado' }}</strong>
                    <small v-if="node.cycle">Ciclo de parentesco detectado</small>
                    <small v-else-if="node.animal">#{{ node.animal.register_number }}</small>
                    <small v-else>{{ node.missingReason }}</small>
                  </button>
                </div>
              </section>
            </div>
          </section>

          <aside class="card genealogy__facts" aria-label="Dados do nascimento">
            <header class="card__head">
              <div>
                <h3 class="card__title">Nascimento</h3>
                <p class="card__desc">Dados disponíveis do animal selecionado.</p>
              </div>
            </header>
            <div class="card__body">
              <dl class="genealogy__details">
                <div>
                  <dt>Brinco</dt>
                  <dd>#{{ selectedAnimal.register_number }}</dd>
                </div>
                <div>
                  <dt>Data</dt>
                  <dd>{{ selectedBirth ? formatDate(selectedBirth.date) : 'Não informada' }}</dd>
                </div>
                <div>
                  <dt>Tipo</dt>
                  <dd>{{ selectedBirth ? occurrenceName(selectedBirth.occurrence) : 'Não informado' }}</dd>
                </div>
                <div>
                  <dt>Peso ao nascer</dt>
                  <dd>{{ selectedBirth ? `${selectedBirth.weight} kg` : 'Não informado' }}</dd>
                </div>
              </dl>
              <p v-if="!selectedBirth" class="genealogy__facts-note">
                Não há nascimento vinculado a este bovino na API.
              </p>
            </div>
          </aside>
        </div>
      </section>

    </div>
  </AppShell>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import api from '@/services/api';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { painelDoPapel } from '@/services/auth';
import { idRelacao } from '@/utils/animalMovementUtils';
import { apiErrorMessage } from '@/utils/apiError';

const painel = computed(() => painelDoPapel());
const animals = ref([]);
const births = ref([]);
const occurrences = ref([]);
const inseminations = ref([]);
const bulls = ref([]);
const loading = ref(true);
const saving = ref(false);
const error = ref('');
const notice = ref('');
const pendingLink = ref(null);
const selectedAnimalId = ref('');
const activeTab = ref('birth');

function todayIso() {
  const date = new Date();
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

const form = ref({ animalId: '', occurrence: '', date: todayIso(), weight: '', insemination: '' });
const ready = computed(() => Boolean(
  form.value.animalId
  && form.value.occurrence
  && form.value.date
  && form.value.weight !== ''
  && Number(form.value.weight) >= 0
));
const animalsWithoutBirth = computed(() => animals.value.filter((animal) => !animal.birth));
const selectedAnimal = computed(() =>
  animals.value.find((animal) => String(animal.id) === selectedAnimalId.value) || null
);
const selectedBirth = computed(() => {
  const birthId = idRelacao(selectedAnimal.value?.birth);
  return births.value.find((item) => String(item.id) === String(birthId)) || null;
});

const ancestorsByRelationship = {
  F: 'Pai',
  M: 'Mãe',
  FF: 'Avô paterno',
  FM: 'Avó paterna',
  MF: 'Avô materno',
  MM: 'Avó materna',
};

function relationshipName(path) {
  if (ancestorsByRelationship[path]) return ancestorsByRelationship[path];
  const grandparentGender = path[1] === 'F' ? 'avô' : 'avó';
  const grandparentSide = path[0] === 'F'
    ? (grandparentGender === 'avó' ? 'paterna' : 'paterno')
    : (grandparentGender === 'avó' ? 'materna' : 'materno');
  const grandparent = `${grandparentGender} ${grandparentSide}`;
  const parentOfGrandparent = path.endsWith('F') ? 'pai' : 'mãe';
  const relation = `${parentOfGrandparent} ${grandparentGender === 'avó' ? 'da' : 'do'} ${grandparent}`;
  const greatGrandparent = path.endsWith('F') ? 'Bisavô' : 'Bisavó';
  return `${greatGrandparent} — ${relation}`;
}

function findAncestor(animal, kind, relationship, path, generation, parentError = '', ancestorIds = []) {
  const animalKey = animal ? `${kind}:${animal.id}` : null;
  const cycle = animalKey ? ancestorIds.includes(animalKey) : false;
  const node = {
    key: path || 'root',
    animal,
    kind,
    relationship,
    generation,
    columnSpan: 8 / (2 ** generation),
    missingReason: cycle ? 'Ciclo de parentesco detectado' : animal ? '' : parentError,
    cycle,
    children: [],
  };
  if (generation === 3) return node;

  if (cycle) {
    const reason = 'Ascendência não expandida por vínculo circular';
    node.children = [
      findAncestor(null, 'bull', relationshipName(`${path}F`), `${path}F`, generation + 1, reason, ancestorIds),
      findAncestor(null, 'cow', relationshipName(`${path}M`), `${path}M`, generation + 1, reason, ancestorIds),
    ];
    return node;
  }

  if (!animal) {
    const reason = parentError || 'Ascendência não disponível';
    node.children = [
      findAncestor(null, 'bull', relationshipName(`${path}F`), `${path}F`, generation + 1, reason, ancestorIds),
      findAncestor(null, 'cow', relationshipName(`${path}M`), `${path}M`, generation + 1, reason, ancestorIds),
    ];
    return node;
  }

  const nextAncestorIds = [...ancestorIds, animalKey];
  if (kind !== 'cow') {
    node.children = [
      findAncestor(null, 'bull', relationshipName(`${path}F`), `${path}F`, generation + 1, 'Ascendência não disponível', nextAncestorIds),
      findAncestor(null, 'cow', relationshipName(`${path}M`), `${path}M`, generation + 1, 'Ascendência não disponível', nextAncestorIds),
    ];
    return node;
  }

  const birthId = idRelacao(animal.birth);
  const birth = births.value.find((item) => String(item.id) === String(birthId));
  const inseminationId = idRelacao(birth?.insemination);
  const insemination = inseminations.value.find((item) => String(item.id) === String(inseminationId));
  const missingReason = !birth
    ? 'Vínculo de nascimento ausente'
    : !insemination
      ? 'Pais não informados'
      : 'Ascendente não encontrado';
  const fatherId = idRelacao(insemination?.father);
  const motherId = idRelacao(insemination?.mother);
  const father = bulls.value.find((item) => String(item.id) === String(fatherId)) || null;
  const mother = animals.value.find((item) => String(item.id) === String(motherId)) || null;

  node.children = [
    findAncestor(father, 'bull', relationshipName(`${path}F`), `${path}F`, generation + 1, missingReason, nextAncestorIds),
    findAncestor(mother, 'cow', relationshipName(`${path}M`), `${path}M`, generation + 1, missingReason, nextAncestorIds),
  ];
  return node;
}

const treeRows = computed(() => {
  if (!selectedAnimal.value) return [];
  const root = findAncestor(selectedAnimal.value, 'cow', 'Animal', '', 0);
  const labels = ['Animal', 'Pais', 'Avós', 'Bisavós'];
  const rows = [];
  let generationNodes = [root];
  for (let generation = 0; generation < labels.length; generation += 1) {
    rows.push({ label: labels[generation], nodes: generationNodes });
    generationNodes = generationNodes.flatMap((node) => node.children);
  }
  return rows;
});

const ascendentesConhecidos = computed(() =>
  treeRows.value.slice(1).flatMap((generation) => generation.nodes).filter((node) => node.animal && !node.cycle).length
);
const ascendentesAusentes = computed(() => 14 - ascendentesConhecidos.value);

const linkedBirths = computed(() => animals.value.flatMap((animal) => {
  const birthId = idRelacao(animal.birth);
  if (!birthId) return [];
  const birth = births.value.find((item) => String(item.id) === String(birthId));
  if (!birth) return [];
  const inseminationId = idRelacao(birth.insemination);
  return [{
    animal,
    birth,
    insemination: inseminations.value.find((item) => String(item.id) === String(inseminationId)) || null,
  }];
}));

function listFromResponse(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  throw new Error('A API retornou um formato de lista inesperado.');
}

function formatDate(value) {
  if (!value) return '—';
  return new Date(`${value}T00:00:00`).toLocaleDateString('pt-BR');
}

function occurrenceName(id) {
  return occurrences.value.find((item) => String(item.id) === String(idRelacao(id)))?.description || '—';
}

function parentName(id, list) {
  const parent = list.find((item) => String(item.id) === String(idRelacao(id)));
  return parent ? `${parent.name} · #${parent.register_number}` : 'Não informado';
}

function inseminationLabel(item) {
  return `Inseminação #${item.id} · ${formatDate(item.date)}`;
}

async function linkBirth(animalId, birthId) {
  await api.patch(`animals/${animalId}/`, { birth: birthId });
}

async function saveBirth() {
  if (!ready.value || saving.value || pendingLink.value) return;
  saving.value = true;
  error.value = '';
  notice.value = '';
  try {
    const response = await api.post('births/', {
      date: form.value.date,
      weight: Number(form.value.weight),
      occurrence: Number(form.value.occurrence),
      insemination: form.value.insemination ? Number(form.value.insemination) : null,
    });
    const birthId = response.data?.id;
    if (!birthId) throw new Error('O nascimento foi criado, mas a API não retornou o identificador.');
    try {
      await linkBirth(Number(form.value.animalId), birthId);
      form.value = { animalId: '', occurrence: '', date: todayIso(), weight: '', insemination: '' };
      await loadData();
    } catch (linkError) {
      pendingLink.value = { animalId: Number(form.value.animalId), birthId };
      notice.value = `O nascimento #${birthId} foi criado, mas o vínculo ao bovino falhou. Use “Tentar vincular”; não envie o formulário novamente.`;
      error.value = apiErrorMessage(linkError, 'Não foi possível vincular o nascimento ao bovino.');
    }
  } catch (saveError) {
    console.error('Erro ao registrar nascimento:', saveError);
    error.value = apiErrorMessage(saveError, 'Não foi possível registrar o nascimento.');
  } finally {
    saving.value = false;
  }
}

async function retryLink() {
  if (!pendingLink.value || saving.value) return;
  saving.value = true;
  error.value = '';
  try {
    await linkBirth(pendingLink.value.animalId, pendingLink.value.birthId);
    pendingLink.value = null;
    notice.value = '';
    form.value = { animalId: '', occurrence: '', date: todayIso(), weight: '', insemination: '' };
    await loadData();
  } catch (linkError) {
    console.error('Erro ao vincular nascimento:', linkError);
    error.value = apiErrorMessage(linkError, 'Não foi possível vincular o nascimento ao bovino.');
  } finally {
    saving.value = false;
  }
}

async function loadData() {
  loading.value = true;
  error.value = '';
  try {
    const [animalsResponse, birthsResponse, occurrencesResponse, inseminationsResponse, bullsResponse] = await Promise.all([
      api.getAnimals(),
      api.get('births/'),
      api.get('birth_occurrences/'),
      api.get('inseminations/'),
      api.get('bulls/'),
    ]);
    animals.value = listFromResponse(animalsResponse.data);
    births.value = listFromResponse(birthsResponse.data);
    occurrences.value = listFromResponse(occurrencesResponse.data);
    inseminations.value = listFromResponse(inseminationsResponse.data);
    bulls.value = listFromResponse(bullsResponse.data);
  } catch (loadError) {
    console.error('Erro ao carregar dados de nascimento e genealogia:', loadError);
    error.value = apiErrorMessage(loadError, 'Não foi possível carregar os dados de nascimento e genealogia.');
  } finally {
    loading.value = false;
  }
}

onMounted(loadData);
</script>

<style scoped>
.birth-list { margin-top: 20px; }
.birth-genealogy__tabs { margin-bottom: 18px; }
.row--between { justify-content: space-between; flex-wrap: wrap; }
.genealogy-card { margin-bottom: 20px; }
.genealogy-card__head { align-items: flex-end; gap: 20px; }
.genealogy-card__select { width: min(340px, 100%); margin: 0; }
.genealogy-card__empty { padding: 30px 20px; }
.genealogy__layout {
  display: grid;
  grid-template-columns: minmax(0, 1.8fr) minmax(230px, 0.8fr);
  gap: 16px;
  padding: 20px;
}
.genealogy__tree-panel,
.genealogy__facts { min-width: 0; }
.genealogy__tree-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 14px;
}
.genealogy__tree-head .card__title { margin: 0 0 5px; }
.genealogy__tree-head .card__desc { margin: 0; }
.genealogy__notice { align-items: flex-start; margin-bottom: 18px; }
.genealogy__canvas { overflow-x: auto; padding: 4px 2px 10px; }
.genealogy__generation + .genealogy__generation { margin-top: 14px; }
.genealogy__generation-label {
  margin: 0 0 8px;
  color: var(--text-3);
  font-size: var(--fs-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.genealogy__nodes {
  display: grid;
  grid-template-columns: repeat(8, minmax(78px, 1fr));
  gap: 8px;
  min-width: 700px;
}
.genealogy__node {
  display: flex;
  min-width: 0;
  min-height: 76px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 10px 6px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface);
  color: var(--text);
  text-align: center;
  cursor: pointer;
  transition: border-color var(--dur) var(--ease), background var(--dur) var(--ease);
}
.genealogy__node:hover:not(:disabled) {
  border-color: var(--accent);
  background: var(--accent-soft);
}
.genealogy__node:focus-visible { outline: none; box-shadow: var(--focus-ring); }
.genealogy__node:disabled { cursor: default; }
.genealogy__node--root,
.genealogy__node--current {
  border-color: var(--accent-line);
  background: var(--accent-soft);
}
.genealogy__node--missing {
  border-style: dashed;
  color: var(--text-3);
}
.genealogy__node--cycle {
  border-color: var(--warn-line);
  background: var(--warn-soft);
}
.genealogy__node strong {
  max-width: 100%;
  overflow-wrap: anywhere;
  font-size: var(--fs-sm);
}
.genealogy__node small {
  color: var(--text-3);
  font-size: var(--fs-xs);
  line-height: 1.3;
}
.genealogy__relation {
  color: var(--text-3);
  font-size: 0.68rem;
  line-height: 1.25;
}
.genealogy__facts.card { align-self: start; }
.genealogy__facts .card__head { padding: 16px 18px; }
.genealogy__facts .card__body { padding: 8px 18px 18px; }
.genealogy__details { margin: 0; }
.genealogy__details > div {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 11px 0;
  border-bottom: 1px dashed var(--line);
}
.genealogy__details > div:last-child { border-bottom: 0; }
.genealogy__details dt { color: var(--text-2); }
.genealogy__details dd { margin: 0; text-align: right; }
.genealogy__facts-note {
  margin: 12px 0 0;
  color: var(--text-2);
  font-size: var(--fs-sm);
}
@media (max-width: 900px) {
  .genealogy__layout { grid-template-columns: 1fr; }
  .genealogy__facts { order: -1; }
}
@media (max-width: 600px) {
  .genealogy-card__head { align-items: stretch; flex-direction: column; }
  .genealogy-card__select { width: 100%; }
  .genealogy__layout { padding: 14px; }
  .genealogy__tree-head { flex-direction: column; }
}
</style>
