<!--
  Cabeçalho de tela: título, uma linha de contexto e as ações da página.
  Existe para que as 20 telas parem de reinventar a mesma faixa com
  medidas e pesos ligeiramente diferentes em cada arquivo.
-->
<template>
  <header class="page__head">
    <div>
      <button v-if="voltar" class="voltar" @click="aoVoltar">
        <AppIcon name="arrow-left" :size="14" />
        <span>{{ voltarRotulo }}</span>
      </button>
      <h1 class="page__title">{{ titulo }}</h1>
      <p v-if="descricao" class="page__desc">{{ descricao }}</p>
    </div>

    <div v-if="$slots.acoes" class="page__actions">
      <slot name="acoes" />
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router';
import AppIcon from '@/components/ui/AppIcon.vue';

const props = defineProps({
  titulo: { type: String, required: true },
  descricao: { type: String, default: '' },
  /** Mostra o botão de voltar. Use `false` em telas de topo de fluxo. */
  voltar: { type: Boolean, default: true },
  voltarRotulo: { type: String, default: 'Voltar' },
  /** Destino fixo; sem ele, volta um passo no histórico. */
  voltarPara: { type: String, default: '' },
});

const router = useRouter();

function aoVoltar() {
  if (props.voltarPara) router.push(props.voltarPara);
  else router.back();
}
</script>

<style scoped>
.voltar {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 10px;
  padding: 0;
  border: 0;
  background: none;
  color: var(--text-3);
  font-family: inherit;
  font-size: var(--fs-sm);
  font-weight: 500;
  transition: color var(--dur) var(--ease);
}

.voltar:hover { color: var(--text); }
</style>
