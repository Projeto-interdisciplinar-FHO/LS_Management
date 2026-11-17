<template>
  <div @click.stop>
    <AppTabs
      :model-value="abaAtual"
      id-base="manejo-peso"
      label="Pesagem e desenvolvimento"
      :tabs="abas"
      @update:model-value="selecionarAba"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AppTabs from '@/components/ui/AppTabs.vue';

const route = useRoute();
const router = useRouter();

const abas = [
  { id: 'pesagem', label: 'Pesagem', icon: 'scale' },
  { id: 'desenvolvimento', label: 'Desenvolvimento', icon: 'chart' },
];

const abaAtual = computed(() => route.name === 'desenvolvimento' ? 'desenvolvimento' : 'pesagem');

function selecionarAba(id) {
  if (id !== abaAtual.value) router.push({ name: id });
}
</script>
