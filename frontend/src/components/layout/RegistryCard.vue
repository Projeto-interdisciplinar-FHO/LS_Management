<template>
  <section class="card">
    <header v-if="titulo || $slots.cabecalho" class="card__head">
      <slot name="cabecalho">
        <div>
          <h2 class="card__title">{{ titulo }}</h2>
          <p v-if="descricao" class="card__desc">{{ descricao }}</p>
        </div>
        <span v-if="total !== null" class="badge">{{ total }}</span>
      </slot>
    </header>

    <div v-if="carregando" class="loading">
      <span class="spinner" aria-hidden="true"></span>
      {{ textoCarregando }}
    </div>

    <div v-else-if="vazio" class="empty">
      <AppIcon :name="iconeVazio" :size="30" />
      <p class="empty__title">{{ tituloVazio }}</p>
      <p v-if="descricaoVazia" class="empty__desc">{{ descricaoVazia }}</p>
      <slot name="acao-vazio">
        <button
          v-if="rotuloAcaoVazio"
          type="button"
          class="btn btn--primary"
          @click="$emit('cadastrar')"
        >
          <AppIcon name="plus" :size="15" />
          {{ rotuloAcaoVazio }}
        </button>
      </slot>
    </div>

    <div v-else-if="vazioFiltrado" class="empty">
      <AppIcon name="search" :size="30" />
      <p class="empty__title">{{ tituloVazioFiltrado }}</p>
      <p class="empty__desc">{{ descricaoVazioFiltrado }}</p>
      <button type="button" class="btn" @click="$emit('limpar-filtros')">Limpar filtros</button>
    </div>

    <slot v-else />

    <footer v-if="$slots.rodape" class="card__foot">
      <slot name="rodape" />
    </footer>
  </section>
</template>

<script setup>
import AppIcon from '@/components/ui/AppIcon.vue';

defineProps({
  titulo: { type: String, default: '' },
  descricao: { type: String, default: '' },
  total: { type: [Number, String], default: null },
  carregando: { type: Boolean, default: false },
  textoCarregando: { type: String, default: 'Carregando registros...' },
  vazio: { type: Boolean, default: false },
  vazioFiltrado: { type: Boolean, default: false },
  iconeVazio: { type: String, default: 'inbox' },
  tituloVazio: { type: String, default: 'Nenhum registro cadastrado' },
  descricaoVazia: { type: String, default: '' },
  rotuloAcaoVazio: { type: String, default: '' },
  tituloVazioFiltrado: { type: String, default: 'Nada encontrado' },
  descricaoVazioFiltrado: { type: String, default: 'Nenhum registro corresponde aos filtros atuais.' },
});

defineEmits(['cadastrar', 'limpar-filtros']);
</script>
