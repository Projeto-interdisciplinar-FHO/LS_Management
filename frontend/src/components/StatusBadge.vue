<template>
  <div 
    class="status-badge" 
    :class="badgeClass"
    :style="{ borderColor: config.borderColor, backgroundColor: config.bgColor }"
  >
    <span class="status-icon" :style="{ color: config.color }">{{ config.icon }}</span>
    <span class="status-label" :style="{ color: config.color }">{{ config.label }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { getStatusConfig } from '@/utils/statusUtils';

const props = defineProps({
  status: {
    type: String,
    required: true
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
});

const config = computed(() => getStatusConfig(props.status));

const badgeClass = computed(() => {
  return `badge-${props.size} ${config.value.badgeClass}`;
});
</script>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid;
  font-weight: 600;
  font-size: 0.85rem;
  white-space: nowrap;
  transition: all 0.2s;
}

.badge-sm {
  padding: 4px 8px;
  font-size: 0.75rem;
}

.badge-md {
  padding: 6px 12px;
  font-size: 0.85rem;
}

.badge-lg {
  padding: 8px 16px;
  font-size: 0.95rem;
}

.status-icon {
  font-size: 1em;
  display: inline-flex;
  align-items: center;
}

.status-label {
  display: inline;
}

.status-sick {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}
</style>
