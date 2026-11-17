<!--
  Abas de tela: usadas para dividir telas longas (painel, reprodução, IA)
  no mesmo padrão de "Nascimento / Árvore genealógica".
  Teclado: setas, Home e End trocam de aba. Cada tela monta o seu painel
  com role="tabpanel" e aria-labelledby="{idBase}-tab-{id}".
-->
<template>
  <nav class="tabs app-tabs" role="tablist" :aria-label="label">
    <button
      v-for="(tab, indice) in tabs"
      :id="`${idBase}-tab-${tab.id}`"
      :key="tab.id"
      type="button"
      role="tab"
      class="tabs__item app-tabs__item"
      :class="{ 'is-active': tab.id === modelValue }"
      :aria-selected="tab.id === modelValue"
      :aria-controls="`${idBase}-panel-${tab.id}`"
      :tabindex="tab.id === modelValue ? 0 : -1"
      @click="$emit('update:modelValue', tab.id)"
      @keydown="aoTeclar($event, indice)"
    >
      <AppIcon v-if="tab.icon" :name="tab.icon" :size="15" />
      {{ tab.label }}
      <span v-if="tab.count" class="count app-tabs__count" :class="{ 'is-warn': tab.warn }">{{ tab.count }}</span>
    </button>
  </nav>
</template>

<script setup>
import { nextTick } from 'vue';
import AppIcon from '@/components/ui/AppIcon.vue';

const props = defineProps({
  modelValue: { type: String, required: true },
  tabs: { type: Array, required: true },
  label: { type: String, default: 'Seções da tela' },
  idBase: { type: String, required: true },
});
const emit = defineEmits(['update:modelValue']);

function aoTeclar(evento, indice) {
  const total = props.tabs.length;
  let destino = null;
  if (evento.key === 'ArrowRight') destino = (indice + 1) % total;
  else if (evento.key === 'ArrowLeft') destino = (indice - 1 + total) % total;
  else if (evento.key === 'Home') destino = 0;
  else if (evento.key === 'End') destino = total - 1;
  if (destino === null) return;
  evento.preventDefault();
  const id = props.tabs[destino].id;
  emit('update:modelValue', id);
  nextTick(() => document.getElementById(`${props.idBase}-tab-${id}`)?.focus());
}
</script>

<style scoped>
.app-tabs { margin-bottom: 20px; }
.app-tabs__item { display: inline-flex; align-items: center; gap: 7px; }
.app-tabs__item > svg { color: var(--text-3); transition: color var(--dur) var(--ease); }
.app-tabs__item.is-active > svg { color: var(--accent); }
.app-tabs__count.is-warn { background: var(--warn-soft); color: var(--warn); }
</style>
