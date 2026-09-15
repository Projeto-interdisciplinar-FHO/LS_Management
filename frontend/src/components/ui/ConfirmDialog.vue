<!--
  Diálogo de confirmação do app. Montado uma vez na raiz e acionado pelo
  `confirmar()` do confirmService — as telas não precisam guardar estado
  nem repetir marcação para cada exclusão.
-->
<template>
  <AppModal v-if="aberto" :titulo="pedido.titulo" @fechar="responder(false)">
    <p v-if="pedido.texto" class="texto">{{ pedido.texto }}</p>
    <p v-else class="texto">Esta ação não pode ser desfeita.</p>

    <template #rodape>
      <button class="btn" @click="responder(false)">Cancelar</button>
      <button
        class="btn"
        :class="pedido.destrutivo ? 'btn--danger' : 'btn--primary'"
        @click="responder(true)"
      >
        {{ pedido.acao }}
      </button>
    </template>
  </AppModal>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import AppModal from './AppModal.vue';

const aberto = ref(false);
const pedido = ref({ titulo: '', texto: '', acao: 'Confirmar', destrutivo: true });
let resolver = null;

function aoPedir(evento) {
  if (!evento.detail) return;
  // Se um pedido ainda estiver aberto, ele é respondido com "não" — nunca
  // deixa uma promessa pendente para sempre.
  if (resolver) resolver(false);

  const { resolver: aguardando, ...dados } = evento.detail;
  pedido.value = dados;
  resolver = aguardando;
  aberto.value = true;
}

function responder(valor) {
  aberto.value = false;
  if (resolver) resolver(valor);
  resolver = null;
}

onMounted(() => window.addEventListener('app-confirm', aoPedir));
onUnmounted(() => window.removeEventListener('app-confirm', aoPedir));
</script>

<style scoped>
.texto {
  color: var(--text-2);
  line-height: 1.6;
}
</style>
