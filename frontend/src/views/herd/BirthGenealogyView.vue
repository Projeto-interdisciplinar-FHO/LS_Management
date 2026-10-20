<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Nascimento e genealogia"
        descricao="Protótipo do registro de nascimento e da consulta de ascendentes."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <p class="alert alert--info" role="status">
        <AppIcon name="info" :size="16" />
        <span>Protótipo visual. Consulta e gravação serão conectadas após a definição do contrato da API.</span>
      </p>

      <div class="grid grid--wide">
        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Dados do nascimento</h2>
              <p class="card__desc">Identificação do animal e informações registradas ao nascer.</p>
            </div>
            <span class="badge"><AppIcon name="animal" :size="13" /> Nascimento</span>
          </header>

          <div class="card__body grid grid--2">
            <div class="field">
              <label class="field__label" for="birth-name">Nome ou apelido</label>
              <input id="birth-name" class="input" type="text" placeholder="A definir" disabled>
            </div>
            <div class="field">
              <label class="field__label" for="birth-tag">Brinco</label>
              <input id="birth-tag" class="input" type="text" placeholder="A definir" disabled>
            </div>
            <div class="field">
              <label class="field__label" for="birth-sex">Sexo</label>
              <select id="birth-sex" class="select" disabled>
                <option value="">Aguardando integração</option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="birth-date">Data de nascimento</label>
              <input id="birth-date" class="input" type="date" disabled>
            </div>
            <div class="field">
              <label class="field__label" for="birth-father">Pai</label>
              <select id="birth-father" class="select" disabled>
                <option value="">Selecione o pai...</option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="birth-mother">Mãe</label>
              <select id="birth-mother" class="select" disabled>
                <option value="">Selecione a mãe...</option>
              </select>
            </div>
            <div class="field">
              <label class="field__label" for="birth-weight">Peso ao nascer (kg)</label>
              <input id="birth-weight" class="input" type="number" step="0.1" placeholder="A definir" disabled>
            </div>
            <div class="field">
              <label class="field__label" for="birth-ecc">ECC</label>
              <input id="birth-ecc" class="input" type="number" placeholder="Escala a definir" disabled>
            </div>
            <div class="field span-full">
              <label class="field__label" for="birth-type">Tipo de nascimento</label>
              <select id="birth-type" class="select" disabled>
                <option value="">A definir com a fazenda</option>
              </select>
            </div>
          </div>

          <footer class="card__foot">
            <button type="button" class="btn btn--primary" disabled>Registrar nascimento</button>
          </footer>
        </section>

        <section class="card">
          <header class="card__head">
            <div>
              <h2 class="card__title">Árvore genealógica</h2>
              <p class="card__desc">Visualização planejada até os bisavós.</p>
            </div>
            <span class="badge">4 gerações</span>
          </header>

          <div class="card__body ancestry">
            <div class="ancestry__subject">
              <AppIcon name="animal" :size="16" />
              <span>Animal selecionado</span>
              <strong>—</strong>
            </div>

            <section v-for="generation in generations" :key="generation.label" class="ancestry__generation">
              <h3 class="ancestry__label">{{ generation.label }}</h3>
              <div class="ancestry__nodes">
                <div v-for="ancestor in generation.ancestors" :key="ancestor" class="ancestry__node">
                  <span>{{ ancestor }}</span>
                  <strong>—</strong>
                </div>
              </div>
            </section>
          </div>
        </section>
      </div>
    </div>
  </AppShell>
</template>

<script setup>
import { computed } from 'vue';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import { painelDoPapel } from '@/services/auth';

const painel = computed(() => painelDoPapel());

const generations = [
  { label: 'Pais', ancestors: ['Pai', 'Mãe'] },
  { label: 'Avós', ancestors: ['Avô paterno', 'Avó paterna', 'Avô materno', 'Avó materna'] },
  {
    label: 'Bisavós',
    ancestors: [
      'Bisavô paterno-paterno', 'Bisavó paterno-paterna',
      'Bisavô paterno-materno', 'Bisavó paterno-materna',
      'Bisavô materno-paterno', 'Bisavó materno-paterna',
      'Bisavô materno-materno', 'Bisavó materno-materna',
    ],
  },
];
</script>

<style scoped>
.ancestry { display: flex; flex-direction: column; gap: 18px; }

.ancestry__subject,
.ancestry__node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  min-width: 0;
  padding: 10px 12px;
  border: 1px solid var(--line);
  border-radius: var(--r);
  background: var(--surface-2);
}

.ancestry__subject { justify-content: flex-start; }
.ancestry__subject strong { margin-left: auto; }
.ancestry__label { margin-bottom: 8px; color: var(--text-2); font-size: var(--fs-sm); font-weight: 600; }
.ancestry__nodes { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
.ancestry__node { align-items: flex-start; flex-direction: column; font-size: var(--fs-sm); }
.ancestry__node strong { color: var(--text-3); }

@media (max-width: 600px) {
  .ancestry__nodes { grid-template-columns: 1fr; }
}
</style>