<template>
  <RouterView />
  <ConfirmDialog />
</template>

<script setup>
/*
 * O App.vue era o maior arquivo de estilo do projeto: umas 250 linhas de
 * `.theme-dark .alguma-coisa { ... !important }`, repintando à mão cada
 * classe que alguma tela tivesse inventado. Bastava uma tela nova para o
 * tema escuro voltar a vazar branco em algum canto.
 *
 * Agora a paleta inteira vive em tokens.css e troca junto com `data-theme`
 * no <html>. Este arquivo voltou a ser o que devia: a raiz que monta a rota
 * e os dois diálogos globais.
 */
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue';
</script>
