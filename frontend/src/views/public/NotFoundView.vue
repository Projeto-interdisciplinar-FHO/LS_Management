<template>
  <div class="nao-encontrada">
    <div class="card nao-encontrada__caixa">
      <div class="card__body">
        <p class="nao-encontrada__codigo mono" aria-hidden="true">404</p>
        <h1>Página não encontrada</h1>
        <p>O endereço digitado não existe ou a página foi movida.</p>
        <div class="nao-encontrada__acoes">
          <button type="button" class="btn" @click="voltar">Voltar</button>
          <RouterLink :to="inicio" class="btn btn--primary">Ir para o início</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { estaLogado, painelDoPapel } from '@/services/auth';

const router = useRouter();
const inicio = computed(() => (estaLogado() ? painelDoPapel() : '/'));

// Sem histórico (página aberta direto pelo endereço), "Voltar" leva ao início.
function voltar() {
  if (window.history.length > 1) router.back();
  else router.push(inicio.value);
}
</script>

<style scoped>
.nao-encontrada {
  display: grid;
  place-items: center;
  min-height: 100vh;
  padding: 24px;
}

.nao-encontrada__caixa {
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.nao-encontrada__codigo {
  margin-bottom: 4px;
  color: var(--accent);
  font-size: 3rem;
  font-weight: 600;
  line-height: 1;
}

.nao-encontrada__caixa h1 { font-size: var(--fs-xl); }
.nao-encontrada__caixa p:not(.nao-encontrada__codigo) { margin-top: 8px; color: var(--text-2); }

.nao-encontrada__acoes {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 22px;
  flex-wrap: wrap;
}
</style>
