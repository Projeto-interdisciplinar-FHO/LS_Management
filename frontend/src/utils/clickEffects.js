// Efeito de onda ao clicar em botões, atalhos e itens de menu.
// Um único ouvinte no documento; sem custo por componente.
// Respeita "reduzir movimento" do sistema operacional.

const ALVOS = [
  '.btn',
  '.segmented__item',
  '.dashboard-today__item',
  '.dashboard__shortcut',
  '.sidebar__link',
  '.genealogy__node',
].join(',');

export function iniciarEfeitosDeClique() {
  if (typeof document === 'undefined') return;
  const reduzir = window.matchMedia('(prefers-reduced-motion: reduce)');

  document.addEventListener('pointerdown', (evento) => {
    if (evento.button !== 0 || reduzir.matches) return;
    const alvo = evento.target instanceof Element ? evento.target.closest(ALVOS) : null;
    if (!alvo || alvo.disabled || alvo.getAttribute('aria-disabled') === 'true') return;

    const caixa = alvo.getBoundingClientRect();
    const diametro = Math.max(caixa.width, caixa.height) * 2;
    const onda = document.createElement('span');
    onda.className = 'ripple';
    onda.setAttribute('aria-hidden', 'true');
    onda.style.width = onda.style.height = `${diametro}px`;
    onda.style.left = `${evento.clientX - caixa.left - diametro / 2}px`;
    onda.style.top = `${evento.clientY - caixa.top - diametro / 2}px`;

    alvo.classList.add('has-ripple');
    alvo.appendChild(onda);
    onda.addEventListener('animationend', () => onda.remove(), { once: true });
  }, { passive: true });
}
