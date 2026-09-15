<template>
  <div class="notifications-container">
    <!-- Sininho no header -->
    <div class="notification-bell-wrapper">
      <button 
        @click="toggleNotificationPanel"
        class="bell-button"
        :class="{ 'has-unread': unreadCount > 0 }"
        title="Notificações"
      >
        <span class="bell-icon">🔔</span>
        <span v-if="unreadCount > 0" class="notif-badge">{{ unreadCount }}</span>
      </button>

      <!-- Painel de notificações (modal) -->
      <transition name="slide-left">
        <div v-if="showPanel" class="notification-panel" v-click-outside="closePanel">
          <div class="panel-header">
            <h3>Notificações</h3>
            <button @click="closePanel" class="close-btn">✕</button>
          </div>

          <div class="panel-tabs">
            <button 
              @click="activeTab = 'unread'" 
              :class="{ active: activeTab === 'unread' }"
            >
              Não Lidas ({{ unreadCount }})
            </button>
            <button 
              @click="activeTab = 'all'" 
              :class="{ active: activeTab === 'all' }"
            >
              Todas
            </button>
          </div>

          <div class="panel-content">
            <!-- Carregando -->
            <div v-if="loading" class="loading-state">
              <span>Carregando notificações...</span>
            </div>

            <!-- Notificações vazias -->
            <div v-else-if="displayedNotifications.length === 0" class="empty-state">
              <span class="empty-icon">📭</span>
              <p>{{ activeTab === 'unread' ? 'Nenhuma notificação não lida' : 'Nenhuma notificação' }}</p>
            </div>

            <!-- Lista de notificações -->
            <div v-else class="notifications-list">
              <div
                v-for="notification in displayedNotifications"
                :key="notification.id"
                @click="markAsRead(notification.id)"
                :class="['notification-item', { 'unread': !notification.read }]"
              >
                <div class="notif-icon">{{ getNotificationIcon(notification.notification_type) }}</div>
                <div class="notif-content">
                  <p class="notif-message">{{ notification.message }}</p>
                  <span class="notif-time">{{ formatTime(notification.created_at) }}</span>
                </div>
                <div class="notif-status">
                  <span v-if="!notification.read" class="unread-dot"></span>
                </div>
              </div>
            </div>
          </div>

          <div class="panel-footer">
            <button 
              v-if="unreadCount > 0"
              @click="markAllAsRead"
              class="btn-mark-all"
            >
              Marcar tudo como lido
            </button>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import api from '@/services/api';

const showPanel = ref(false);
const loading = ref(false);
const activeTab = ref('unread');
const notifications = ref([]);
const unreadCount = ref(0);
let pollInterval = null;

// Ícones para cada tipo de notificação
const notificationIcons = {
  'weight': '⊡',
  'vaccination': '✛',
  'feeding': '🍽',
  'health': '♥',
  'movement': '↔',
  'milk': '🥛',
  'batch_vaccination': '✛✛',
  'animal_created': '➕'
};

const getNotificationIcon = (type) => {
  return notificationIcons[type] || '📌';
};

const displayedNotifications = computed(() => {
  if (activeTab.value === 'unread') {
    return notifications.value.filter(n => !n.read);
  }
  return notifications.value;
});

const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return 'agora';
  if (diffMins < 60) return `${diffMins}m atrás`;
  if (diffHours < 24) return `${diffHours}h atrás`;
  if (diffDays < 7) return `${diffDays}d atrás`;
  
  return date.toLocaleDateString('pt-BR');
};

// Buscar apenas contagem de não lidas (rápido para polling)
const fetchUnreadCount = async () => {
  try {
    const response = await api.get('/notifications/unread-count/');
    unreadCount.value = response.data.unread_count;
  } catch (error) {
    console.error('Erro ao buscar contagem de notificações:', error);
  }
};

// Buscar todas as notificações
const fetchNotifications = async () => {
  loading.value = true;
  try {
    const endpoint = activeTab.value === 'unread' 
      ? '/notifications/unread/' 
      : '/notifications/';
    
    const response = await api.get(endpoint);
    notifications.value = Array.isArray(response.data) ? response.data : response.data.results || [];
    
    // Atualizar contagem
    const unread = notifications.value.filter(n => !n.read).length;
    unreadCount.value = unread;
  } catch (error) {
    console.error('Erro ao buscar notificações:', error);
  } finally {
    loading.value = false;
  }
};

const markAsRead = async (notificationId) => {
  try {
    await api.put(`/notifications/${notificationId}/mark-as-read/`, {});
    
    // Atualizar localmente
    const notification = notifications.value.find(n => n.id === notificationId);
    if (notification) {
      notification.read = true;
    }
    
    // Recalcular contagem
    unreadCount.value = notifications.value.filter(n => !n.read).length;
  } catch (error) {
    console.error('Erro ao marcar notificação como lida:', error);
  }
};

const markAllAsRead = async () => {
  try {
    const unreadIds = notifications.value
      .filter(n => !n.read)
      .map(n => n.id);
    
    if (unreadIds.length === 0) return;
    
    await api.post('/notifications/bulk-mark-as-read/', {
      notification_ids: unreadIds
    });
    
    // Atualizar localmente
    notifications.value.forEach(n => {
      if (!n.read) n.read = true;
    });
    unreadCount.value = 0;
  } catch (error) {
    console.error('Erro ao marcar todas como lidas:', error);
  }
};

const toggleNotificationPanel = async () => {
  showPanel.value = !showPanel.value;
  if (showPanel.value) {
    await fetchNotifications();
  }
};

const closePanel = () => {
  showPanel.value = false;
};

// Iniciar polling automático de contagem (a cada 15 segundos)
onMounted(() => {
  fetchUnreadCount();
  
  pollInterval = setInterval(() => {
    fetchUnreadCount();
  }, 15000); // 15 segundos
});

// Limpar interval ao desmontar
onUnmounted(() => {
  if (pollInterval) {
    clearInterval(pollInterval);
  }
});

// Diretiva customizada
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event);
      }
    };
    document.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent);
  }
};
</script>

<style scoped>
.notifications-container {
  position: relative;
}

.notification-bell-wrapper {
  position: relative;
}

.bell-button {
  position: relative;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  transition: transform 0.2s;
  padding: 0.5rem;
}

.bell-button:hover {
  transform: scale(1.1);
}

.bell-button.has-unread {
  animation: ring 0.6s ease-in-out;
}

@keyframes ring {
  0%, 100% { transform: rotate(0); }
  15% { transform: rotate(-15deg); }
  30% { transform: rotate(15deg); }
  45% { transform: rotate(-15deg); }
  60% { transform: rotate(15deg); }
  75% { transform: rotate(0); }
}

.notif-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #ff4444;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
  border: 2px solid white;
}

.notification-panel {
  position: absolute;
  top: 50px;
  right: 0;
  width: 380px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  max-height: 600px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #eee;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.close-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #999;
}

.panel-tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  padding: 0;
}

.panel-tabs button {
  flex: 1;
  padding: 12px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #666;
  font-size: 0.9rem;
  transition: all 0.3s;
  border-bottom: 3px solid transparent;
}

.panel-tabs button.active {
  color: #333;
  border-bottom-color: #4CAF50;
  font-weight: 600;
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  min-height: 200px;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #999;
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.notifications-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notification-item {
  display: flex;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
  gap: 12px;
}

.notification-item:hover {
  background: #f9f9f9;
}

.notification-item.unread {
  background: #f0f8ff;
}

.notif-icon {
  font-size: 1.5rem;
  min-width: 24px;
  text-align: center;
}

.notif-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.notif-message {
  margin: 0;
  color: #333;
  font-size: 0.95rem;
  line-height: 1.4;
}

.notif-time {
  color: #999;
  font-size: 0.85rem;
  margin-top: 4px;
}

.notif-status {
  display: flex;
  align-items: center;
}

.unread-dot {
  width: 8px;
  height: 8px;
  background: #4CAF50;
  border-radius: 50%;
}

.panel-footer {
  padding: 12px 16px;
  border-top: 1px solid #eee;
}

.btn-mark-all {
  width: 100%;
  padding: 8px 12px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.btn-mark-all:hover {
  background: #45a049;
}

.slide-left-enter-active,
.slide-left-leave-active {
  transition: all 0.3s ease;
}

.slide-left-enter-from {
  transform: translateX(380px);
  opacity: 0;
}

.slide-left-leave-to {
  transform: translateX(380px);
  opacity: 0;
}
</style>
