export function notify(message, type = 'success', duration = 4000) {
  if (typeof window === 'undefined') return;

  window.dispatchEvent(new CustomEvent('app-notification', {
    detail: { message, type, duration }
  }));
}
