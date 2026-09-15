<!--
  Diálogo do sistema.

  As telas tinham cinco modais copiados, cada um com um tom de fundo e um
  raio diferente, e nenhum fechava com Esc nem travava a rolagem da página
  atrás. Este resolve os três de uma vez.
-->
<template>
  <Teleport to="body">
    <div class="modal-backdrop" @click.self="$emit('fechar')">
      <div
        class="modal"
        :class="{ 'modal--lg': largo }"
        role="dialog"
        aria-modal="true"
        :aria-label="titulo"
      >
        <header class="modal__head">
          <h2 class="modal__title">{{ titulo }}</h2>
          <button class="btn btn--icon" aria-label="Fechar" @click="$emit('fechar')">
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

<script setup>
import { onBeforeUnmount, onMounted } from 'vue';
import AppIcon from './AppIcon.vue';

defineProps({
  titulo: { type: String, required: true },
  largo: { type: Boolean, default: false },
});

const emit = defineEmits(['fechar']);

function aoTeclar(evento) {
  if (evento.key === 'Escape') emit('fechar');
}

onMounted(() => {
  document.addEventListener('keydown', aoTeclar);
  document.body.style.overflow = 'hidden';
});

onBeforeUnmount(() => {
  document.removeEventListener('keydown', aoTeclar);
  document.body.style.overflow = '';
});
</script>
