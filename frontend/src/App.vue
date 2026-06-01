<template>
  <div id="ls-app-root" :class="themeClass">
    <button
      v-if="showThemeToggle"
      class="theme-toggle-button"
      @click="toggleTheme"
      :aria-label="themeButtonLabel"
      :title="themeButtonLabel"
    >
      {{ themeIcon }}
    </button>
    <RouterView />
    <NotificationToast />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import NotificationToast from '@/components/NotificationToast.vue';

const route = useRoute();
const theme = ref('light');

const isLightOnlyPage = computed(() => {
  return route.name === 'home' || route.name === 'login' || route.path === '/login' || route.path === '/';
});
const themeClass = computed(() => {
  if (isLightOnlyPage.value) return 'theme-light';
  return theme.value === 'dark' ? 'theme-dark' : 'theme-light';
});
const themeButtonLabel = computed(() => theme.value === 'dark' ? 'Usar modo claro' : 'Usar modo escuro');
const themeIcon = computed(() => theme.value === 'dark' ? '☀️' : '🌙');
const showThemeToggle = computed(() => {
  const routeName = route.name ? String(route.name) : '';
  return routeName.startsWith('dashboard');
});

const toggleTheme = () => {
  theme.value = theme.value === 'dark' ? 'light' : 'dark';
  localStorage.setItem('appTheme', theme.value);
};

onMounted(() => {
  const savedTheme = localStorage.getItem('appTheme');
  if (savedTheme === 'dark' || savedTheme === 'light') {
    theme.value = savedTheme;
  } else if (window.matchMedia?.('(prefers-color-scheme: dark)').matches) {
    theme.value = 'dark';
  }
});

const applyDocumentTheme = () => {
  const useDarkTheme = theme.value === 'dark' && !isLightOnlyPage.value;
  document.documentElement.classList.toggle('theme-dark', useDarkTheme);
  document.documentElement.classList.toggle('theme-light', !useDarkTheme);
};

watch([theme, isLightOnlyPage], applyDocumentTheme, { immediate: true });
</script>

<style>
html, body, #app, #ls-app-root {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  min-height: 100% !important;
  overflow-x: hidden;
  background-color: #f8fafc;
  color: #0f172a;
  transition: background-color 0.3s ease, color 0.3s ease;
}

html.theme-dark,
html.theme-dark body,
html.theme-dark #app,
html.theme-dark #ls-app-root,
.theme-dark {
  background-color: #0b1220;
  color: #e5e7eb;
}

/* BACKGROUNDS E CONTAINERS */
.theme-dark .dashboard-wrapper,
.theme-dark .main-layout,
.theme-dark .dashboard-content,
.theme-dark .stables-wrapper,
.theme-dark .content-container,
.theme-dark .page-header,
.theme-dark .modal-overlay,
.theme-dark .modal-content,
.theme-dark .taxonomy-page,
.theme-dark .taxonomy-list,
.theme-dark .taxonomy-item,
.theme-dark .taxonomy-main,
.theme-dark .content-card,
.theme-dark .taxonomy-form,
.theme-dark .input-grid,
.theme-dark .input-group,
.theme-dark .section-header,
.theme-dark .header-copy {
  background-color: #0f172a !important;
}

/* TEXTO GERAL */
.theme-dark p,
.theme-dark span,
.theme-dark label,
.theme-dark h1,
.theme-dark h2,
.theme-dark h3,
.theme-dark h4,
.theme-dark h5,
.theme-dark h6,
.theme-dark .taxonomy-item p,
.theme-dark .header-copy p,
.theme-dark .title-text,
.theme-dark .form-status {
  color: #e5e7eb !important;
}

/* CARDS E ELEMENTOS */
.theme-dark .stable-card,
.theme-dark .action-card,
.theme-dark .card,
.theme-dark .task-item,
.theme-dark .main-highlight-card,
.theme-dark .table-container,
.theme-dark .form-container,
.theme-dark .data-form {
  background-color: #111827 !important;
  border-color: #1f2937 !important;
  color: #e5e7eb !important;
}

.theme-dark .main-highlight-card {
  background: #111827 !important;
}

.theme-dark .highlight-copy-side,
.theme-dark .highlight-visual-side,
.theme-dark .highlight-copy-badge,
.theme-dark .highlight-copy-text,
.theme-dark .highlight-copy-dot,
.theme-dark .highlight-cover-image {
  background: #111827 !important;
  color: #e5e7eb !important;
}

.theme-dark .highlight-visual-side::before,
.theme-dark .highlight-visual-side::after {
  background: none !important;
}

/* HEADERS E BARRAS */
.theme-dark .top-bar,
.theme-dark .page-header,
.theme-dark .modal-header,
.theme-dark .stable-card-header {
  background: #111827 !important;
  border-color: #1f2937 !important;
}

/* TABELAS */
.theme-dark .data-table,
.theme-dark .animals-sub-table {
  background: #111827 !important;
  color: #e5e7eb !important;
}

.theme-dark .data-table th,
.theme-dark .animals-sub-table th {
  background: #0f172a !important;
  color: #e5e7eb !important;
  border-color: #1f2937 !important;
}

.theme-dark .data-table td,
.theme-dark .animals-sub-table td {
  color: #e5e7eb !important;
  border-color: #1f2937 !important;
}

.theme-dark .data-table tr:hover,
.theme-dark .animals-sub-table tr:hover {
  background: #1f2937 !important;
}

/* DROPDOWN E MENUS */
.theme-dark .dropdown-menu {
  background: #111827 !important;
  border-color: #1f2937 !important;
  box-shadow: 0 12px 24px -12px rgba(0, 0, 0, 0.6) !important;
}

.theme-dark .dropdown-item {
  color: #e5e7eb !important;
}

.theme-dark .dropdown-item:hover,
.theme-dark .dropdown-item.router-link-active {
  background: #1f2937 !important;
  color: #ffffff !important;
}

.theme-dark .nav-trigger {
  background: #111827 !important;
  color: #e5e7eb !important;
  border-color: #1f2937 !important;
}

.theme-dark .nav-trigger:hover {
  background: #1f2937 !important;
}

/* INPUTS E FORMS */
.theme-dark input,
.theme-dark textarea,
.theme-dark select {
  background-color: #111827 !important;
  color: #e5e7eb !important;
  border-color: #1f2937 !important;
}

.theme-dark input:focus,
.theme-dark textarea:focus,
.theme-dark select:focus {
  border-color: #7c3aed !important;
  outline: none !important;
}

.theme-dark input::placeholder {
  color: #6b7280 !important;
}

/* BOTÕES */
.theme-dark .btn-primary {
  background: #7c3aed !important;
  color: #ffffff !important;
  border-color: #7c3aed !important;
}

.theme-dark .btn-primary:hover {
  background: #6d28d9 !important;
}

.theme-dark .btn-logout,
.theme-dark .btn-back,
.theme-dark .btn-secondary-restored {
  background: #1f2937 !important;
  border-color: #374151 !important;
  color: #e5e7eb !important;
}

.theme-dark .btn-logout:hover,
.theme-dark .btn-back:hover,
.theme-dark .btn-secondary-restored:hover {
  background: #374151 !important;
}

.theme-dark .btn-icon-action {
  color: #e5e7eb !important;
  background: transparent !important;
}

.theme-dark .btn-icon-action:hover {
  background: #1f2937 !important;
  color: #ffffff !important;
}

.theme-dark .btn-toggle-animals {
  background: #111827 !important;
  color: #e5e7eb !important;
  border-color: #1f2937 !important;
}

.theme-dark .btn-toggle-animals:hover {
  background: #1f2937 !important;
}

.theme-dark .btn-text-action {
  color: #e5e7eb !important;
}

.theme-dark .btn-text-action.text-red {
  color: #f87171 !important;
}

.theme-dark .btn-text-action.text-green {
  color: #86efac !important;
}

/* PROGRESS BARS */
.theme-dark .progress-bar-bg {
  background: #1f2937 !important;
  border-color: #374151 !important;
}

.theme-dark .progress-bar-fill {
  background: #7c3aed !important;
}

/* MODALS */
.theme-dark .modal-overlay {
  background-color: rgba(0, 0, 0, 0.75) !important;
}

.theme-dark .modal-form,
.theme-dark .modal-content {
  background: #111827 !important;
  color: #e5e7eb !important;
  border-color: #1f2937 !important;
}

/* OVERRIDES PARA FUNDO BRANCO */
.theme-dark .page-wrapper,
.theme-dark .list-wrapper,
.theme-dark .detail-wrapper,
.theme-dark .form-wrapper,
.theme-dark .reports-wrapper,
.theme-dark .stables-wrapper,
.theme-dark .report-card,
.theme-dark .form-card,
.theme-dark .data-card,
.theme-dark .content-card,
.theme-dark .section-card,
.theme-dark .table-container,
.theme-dark .animals-sub-table-wrapper,
.theme-dark .content-container,
.theme-dark .chat-container,
.theme-dark .chat-history,
.theme-dark .chat-input-area,
.theme-dark .modal-content,
.theme-dark .empty-selection-placeholder,
.theme-dark .empty-state,
.theme-dark .loading-state {
  background: #0f172a !important;
  color: #e5e7eb !important;
  border-color: #1f2937 !important;
  box-shadow: none !important;
}

.theme-dark .page-header,
.theme-dark .content-header,
.theme-dark .page-section,
.theme-dark .section-header,
.theme-dark .card-header,
.theme-dark .stable-card,
.theme-dark .column-card,
.theme-dark .highlight-card,
.theme-dark .dashboard-card,
.theme-dark .report-card,
.theme-dark .data-card,
.theme-dark .content-card,
.theme-dark .table-card {
  background: #111827 !important;
  color: #e5e7eb !important;
  border-color: #1f2937 !important;
}

.theme-dark .data-table,
.theme-dark .animals-sub-table,
.theme-dark .table-container {
  background: #111827 !important;
  color: #e5e7eb !important;
}

.theme-dark .data-table th,
.theme-dark .animals-sub-table th,
.theme-dark .data-table td,
.theme-dark .animals-sub-table td {
  background: #0f172a !important;
  color: #e5e7eb !important;
  border-color: #1f2937 !important;
}

.theme-dark .data-table tr:hover,
.theme-dark .animals-sub-table tr:hover,
.theme-dark .table-row-hover:hover {
  background: #1f2937 !important;
}

.theme-dark .btn-back,
.theme-dark .btn-action,
.theme-dark .btn-secondary,
.theme-dark .btn-close,
.theme-dark .btn-icon-action,
.theme-dark .btn-toggle-animals,
.theme-dark .btn-text-action,
.theme-dark .tab-btn,
.theme-dark .tab-button,
.theme-dark .btn-suggestion,
.theme-dark .btn-primary {
  color: #e5e7eb !important;
}

.theme-dark .btn-back,
.theme-dark .btn-action,
.theme-dark .btn-secondary,
.theme-dark .btn-close,
.theme-dark .btn-icon-action,
.theme-dark .btn-toggle-animals,
.theme-dark .btn-text-action,
.theme-dark .tab-btn,
.theme-dark .tab-button,
.theme-dark .btn-suggestion {
  background: #111827 !important;
  border-color: #1f2937 !important;
}

.theme-dark .btn-primary {
  background: #7c3aed !important;
  color: #ffffff !important;
}

.theme-dark .btn-primary:hover {
  background: #6d28d9 !important;
}

.theme-dark .badge,
.theme-dark .status-badge,
.theme-dark .feed-tag,
.theme-dark .stable-type-tag,
.theme-dark .highlight-copy-badge,
.theme-dark .count-badge,
.theme-dark .empty-selection-placeholder {
  background: #1f2937 !important;
  color: #e5e7eb !important;
  border-color: #374151 !important;
}

.theme-dark .taxonomy-icon {
  background: #1f2937 !important;
  color: #a78bfa !important;
}

.theme-dark .taxonomy-item {
  border-color: #1f2937 !important;
}

.theme-dark .page-header,
.theme-dark .header-copy,
.theme-dark .section-header,
.theme-dark .taxonomy-main,
.theme-dark .taxonomy-list,
.theme-dark .taxonomy-item {
  color: #e5e7eb !important;
}

.theme-dark .status-badge.active {
  background: #22c55e !important;
  color: #0f172a !important;
}

.theme-dark .status-badge.inactive {
  background: #475569 !important;
  color: #f8fafc !important;
}

/* BADGES E TAGS */
.theme-dark .stable-type-tag,
.theme-dark .highlight-copy-badge {
  background: #1f2937 !important;
  color: #e5e7eb !important;
  border-color: #374151 !important;
}

/* TEMA TOGGLE */
.theme-dark .theme-toggle-button {
  position: fixed;
  bottom: 18px;
  right: 18px;
  z-index: 1000;
  width: 44px;
  height: 44px;
  background: #111827;
  border: 1px solid #374151;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 14px 30px rgba(0, 0, 0, 0.25);
}

.theme-toggle-button {
  position: fixed;
  bottom: 18px;
  right: 18px;
  z-index: 1000;
  width: 44px;
  height: 44px;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.1rem;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.theme-toggle-button:hover {
  background-color: #f1f5f9;
  transform: translateY(-1px);
}

* {
  box-sizing: border-box;
  -webkit-font-smoothing: antialiased;
}
</style>