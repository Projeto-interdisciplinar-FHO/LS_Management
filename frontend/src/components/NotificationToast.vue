<template>
  <transition name="toast-fade">
    <div v-if="visible" :class="['notification-toast', typeClass]">
      <div class="toast-icon">{{ icon }}</div>
      <div class="toast-content">
        <p class="toast-title">{{ title }}</p>
        <p class="toast-message">{{ message }}</p>
      </div>
      <button class="toast-close" @click="close">×</button>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const visible = ref(false);
const message = ref('');
const type = ref('success');
const duration = ref(4000);
let timeoutId = null;

const typeClass = computed(() => {
  return type.value === 'error'
    ? 'toast-error'
    : type.value === 'warning'
    ? 'toast-warning'
    : 'toast-success';
});

const icon = computed(() => {
  if (type.value === 'error') return '✖';
  if (type.value === 'warning') return '⚠';
  return '✓';
});

const title = computed(() => {
  if (type.value === 'error') return 'Erro';
  if (type.value === 'warning') return 'Aviso';
  return 'Sucesso';
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
.notification-toast {
  position: fixed;
  right: 24px;
  top: 24px;
  width: min(420px, calc(100vw - 40px));
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px 18px;
  border-radius: 14px;
  box-shadow: 0 18px 50px rgba(15, 23, 42, 0.15);
  backdrop-filter: blur(12px);
  z-index: 2000;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.toast-success { background: #ecfdf5; color: #166534; }
.toast-warning { background: #fef3c7; color: #713f12; }
.toast-error { background: #fee2e2; color: #991b1b; }

.toast-icon {
  font-size: 1.35rem;
  line-height: 1;
  padding-top: 4px;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-weight: 700;
  margin: 0 0 6px;
}

.toast-message {
  margin: 0;
  line-height: 1.5;
  word-break: break-word;
}

.toast-close {
  background: transparent;
  border: none;
  color: inherit;
  font-size: 1.1rem;
  cursor: pointer;
  line-height: 1;
  padding: 0;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
</style>