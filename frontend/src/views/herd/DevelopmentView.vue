<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Desenvolvimento"
        descricao="Protótipo de acompanhamento de pesagens e crescimento do animal."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <p class="alert alert--info" role="status">
        <AppIcon name="info" :size="16" />
        <span>Protótipo visual. Consulta, critérios de crescimento e gravação dependem da integração e validação das regras.</span>
      </p>

      <section class="card">
        <header class="card__head">
          <div>
            <h2 class="card__title">Animal acompanhado</h2>
            <p class="card__desc">Seleção do animal para consultar e registrar os marcos de desenvolvimento.</p>
          </div>
          <span class="badge"><AppIcon name="scale" :size="13" /> Pesagens</span>
        </header>
        <div class="card__body grid grid--2">
          <div class="field">
            <label class="field__label" for="development-animal">Animal</label>
            <select id="development-animal" class="select" disabled>
              <option value="">Seleção disponível após integração</option>
            </select>
          </div>
          <div class="field">
            <label class="field__label" for="development-birth-date">Data de nascimento</label>
            <input id="development-birth-date" class="input" type="date" disabled>
          </div>
        </div>
      </section>

      <section class="card development__section">
        <header class="card__head">
          <div>
            <h2 class="card__title">Marcos de pesagem</h2>
            <p class="card__desc">Registros previstos aos 30 dias, 60 dias e no desmame.</p>
          </div>
          <span class="badge">3 marcos</span>
        </header>

        <div class="table-wrap">
          <table class="table">
            <thead>
              <tr>
                <th>Marco</th>
                <th>Data da pesagem</th>
                <th>Peso (kg)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(milestone, index) in milestones" :key="milestone">
                <td class="cell-strong">{{ milestone }}</td>
                <td>
                  <input :id="`milestone-date-${index}`" class="input" type="date" :aria-label="`Data da pesagem: ${milestone}`" disabled>
                </td>
                <td>
                  <input :id="`milestone-weight-${index}`" class="input" type="number" step="0.1" :aria-label="`Peso em quilos: ${milestone}`" disabled>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <footer class="card__foot">
          <button type="button" class="btn btn--primary" disabled>Salvar pesagens</button>
        </footer>
      </section>

      <section class="card development__section">
        <header class="card__head">
          <div>
            <h2 class="card__title">Curva de crescimento</h2>
            <p class="card__desc">Histórico de peso por animal e comparação com o padrão esperado.</p>
          </div>
          <span class="badge">Aguardando dados</span>
        </header>
        <div class="empty">
          <AppIcon name="chart" :size="28" />
          <p class="empty__title">Sem pesagens para exibir</p>
          <p class="empty__desc">A curva e os critérios de comparação serão definidos na integração.</p>
        </div>
      </section>
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
const milestones = ['30 dias', '60 dias', 'Desmame'];
</script>

<style scoped>
.development__section { margin-top: 20px; }

.table .input { min-width: 150px; }

@media (max-width: 600px) {
  .table .input { min-width: 130px; }
}
</style>