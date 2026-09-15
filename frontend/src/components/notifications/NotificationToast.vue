<template>
  <Teleport to="body">
    <transition name="toast">
      <div v-if="visible" class="toast" :class="tipoClasse" role="status" aria-live="polite">
        <AppIcon :name="icone" :size="17" class="toast__icone" />
        <div class="toast__texto">
          <p class="toast__titulo">{{ title }}</p>
          <p class="toast__mensagem">{{ message }}</p>
        </div>
        <button class="toast__fechar" aria-label="Fechar aviso" @click="close">
          <AppIcon name="close" :size="14" />
        </button>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import AppIcon from '@/components/ui/AppIcon.vue';

const visible = ref(false);
const message = ref('');
const type = ref('success');
const duration = ref(4000);
let timeoutId = null;

const tipoClasse = computed(() => {
  if (type.value === 'error') return 'toast--erro';
  if (type.value === 'warning') return 'toast--aviso';
  return 'toast--ok';
});

const icone = computed(() => {
  if (type.value === 'error') return 'x-circle';
  if (type.value === 'warning') return 'alert';
  return 'check-circle';
});

const title = computed(() => {
  if (type.value === 'error') return 'Erro';
  if (type.value === 'warning') return 'Aviso';
  return 'Pronto';
});

const show = (payload) => {
  message.value = payload.message || '';
  type.value = payload.type || 'success';
  duration.value = payload.duration || 4000;
  visible.value = true;

  if (timeoutId) clearTimeout(timeoutId);
  timeoutId = setTimeout(close, duration.value);
};

const close = () => {
  visible.value = false;
  if (timeoutId) {
    clearTimeout(timeoutId);
    timeoutId = null;
  }
};

const onNotification = (event) => {
  if (!event.detail) return;
  show(event.detail);
};

onMounted(() => {
  window.addEventListener('app-notification', onNotification);
});

onUnmounted(() => {
  window.removeEventListener('app-notification', onNotification);
  if (timeoutId) clearTimeout(timeoutId);
});
</script>

<style scoped>
.toast {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 300;
  display: flex;
  align-items: flex-start;
  gap: 11px;
  width: min(380px, calc(100vw - 40px));
  padding: 13px 15px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-left: 3px solid var(--text-3);
  border-radius: var(--r-md);
  box-shadow: var(--shadow-lg);
}

.toast--ok    { border-left-color: var(--ok); }
.toast--aviso { border-left-color: var(--warn); }
.toast--erro  { border-left-color: var(--danger); }

.toast__icone { flex: none; margin-top: 1px; }
.toast--ok .toast__icone    { color: var(--ok); }
.toast--aviso .toast__icone { color: var(--warn); }
.toast--erro .toast__icone  { color: var(--danger); }

.toast__texto { flex: 1; min-width: 0; }

.toast__titulo {
  font-size: var(--fs-md);
  font-weight: 600;
}

.toast__mensagem {
  margin-top: 2px;
  color: var(--text-2);
  font-size: var(--fs-sm);
  line-height: 1.5;
}

.toast__fechar {
  flex: none;
  display: grid;
  place-items: center;
  width: 22px;
  height: 22px;
  border: 0;
  border-radius: var(--r-sm);
  background: none;
  color: var(--text-3);
}

.toast__fechar:hover { background: var(--surface-3); color: var(--text); }

.toast-enter-active,
.toast-leave-active { transition: opacity var(--dur) var(--ease), transform 200ms var(--ease); }

.toast-enter-from,
.toast-leave-to { opacity: 0; transform: translateY(10px); }
</style>
