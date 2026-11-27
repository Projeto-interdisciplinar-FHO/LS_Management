<!--
  Diálogo do sistema.

  As telas tinham cinco modais copiados, cada um com um tom de fundo e um
  raio diferente, e nenhum fechava com Esc nem travava a rolagem da página
  atrás. Este resolve os três de uma vez.

  Revisão de UX:
  - o foco entra no diálogo ao abrir, fica preso nele (Tab) e volta ao botão
    de origem ao fechar;
  - clicar e arrastar para selecionar texto e soltar fora do diálogo não fecha
    mais por engano (só fecha se o clique começou e terminou no fundo);
  - com mais de um diálogo aberto, Esc fecha só o de cima.
  Para escolher o primeiro foco, use o atributo data-autofocus no elemento.
-->
<template>
  <Teleport to="body">
    <div
      class="modal-backdrop"
      @pointerdown="comecouNoFundo = $event.target === $event.currentTarget"
      @click.self="aoClicarNoFundo"
    >
      <div
        ref="dialogo"
        class="modal"
        :class="{ 'modal--lg': largo }"
        role="dialog"
        aria-modal="true"
        tabindex="-1"
        :aria-labelledby="idTitulo"
      >
        <header class="modal__head">
          <h2 :id="idTitulo" class="modal__title">{{ titulo }}</h2>
          <button type="button" class="btn btn--icon" aria-label="Fechar" @click="$emit('fechar')">
            <AppIcon name="close" :size="16" />
          </button>
        </header>

        <div class="modal__body">
          <slot />
        </div>

        <footer v-if="$slots.rodape" class="modal__foot">
          <slot name="rodape" />
        </footer>
      </div>
    </div>
  </Teleport>
</template>

<script>
// Compartilhado entre todos os diálogos abertos ao mesmo tempo.
let contador = 0;
const pilha = [];
</script>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue';
import AppIcon from './AppIcon.vue';

defineProps({
  titulo: { type: String, required: true },
  largo: { type: Boolean, default: false },
});

const emit = defineEmits(['fechar']);

const idModal = `modal-${(contador += 1)}`;
const idTitulo = `${idModal}-titulo`;
const dialogo = ref(null);
const comecouNoFundo = ref(false);
let focoAnterior = null;

const FOCAVEIS = 'a[href], button:not(:disabled), input:not(:disabled):not([type="hidden"]), select:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex="-1"])';

function focaveis() {
  return [...(dialogo.value?.querySelectorAll(FOCAVEIS) ?? [])].filter((el) => el.offsetParent !== null);
}

function aoClicarNoFundo() {
  if (comecouNoFundo.value) emit('fechar');
  comecouNoFundo.value = false;
}

function aoTeclar(evento) {
  if (pilha[pilha.length - 1] !== idModal) return;

  if (evento.key === 'Escape') {
    evento.stopPropagation();
    emit('fechar');
    return;
  }

  if (evento.key !== 'Tab') return;
  const lista = focaveis();
  if (!lista.length) {
    evento.preventDefault();
    dialogo.value?.focus();
    return;
  }
  const primeiro = lista[0];
  const ultimo = lista[lista.length - 1];
  const ativo = document.activeElement;
  if (evento.shiftKey && (ativo === primeiro || !dialogo.value.contains(ativo))) {
    evento.preventDefault();
    ultimo.focus();
  } else if (!evento.shiftKey && (ativo === ultimo || !dialogo.value.contains(ativo))) {
    evento.preventDefault();
    primeiro.focus();
  }
}

onMounted(() => {
  focoAnterior = document.activeElement;
  pilha.push(idModal);
  document.addEventListener('keydown', aoTeclar);
  document.body.style.overflow = 'hidden';

  nextTick(() => {
    const preferido = dialogo.value?.querySelector('[data-autofocus]');
    const corpo = dialogo.value?.querySelector('.modal__body');
    const primeiroCampo = corpo ? [...corpo.querySelectorAll(FOCAVEIS)][0] : null;
    (preferido || primeiroCampo || dialogo.value)?.focus();
  });
});

onBeforeUnmount(() => {
  document.removeEventListener('keydown', aoTeclar);
  const posicao = pilha.indexOf(idModal);
  if (posicao >= 0) pilha.splice(posicao, 1);
  if (!pilha.length) document.body.style.overflow = '';
  if (focoAnterior && document.contains(focoAnterior)) focoAnterior.focus?.();
});
</script>
