// Quando um texto é cortado com "…" (nome de animal, vacina, descrição),
// mostra o texto completo ao passar o mouse. Um único ouvinte no documento:
// funciona para qualquer elemento cortado, inclusive os que forem criados depois.
// Elementos que já têm um title próprio não são alterados.

function estaCortado(elemento) {
  const estilo = getComputedStyle(elemento);
  const porLargura = estilo.textOverflow === 'ellipsis' && elemento.scrollWidth > elemento.clientWidth + 1;
  const linhas = estilo.webkitLineClamp;
  const porLinhas = linhas && linhas !== 'none' && elemento.scrollHeight > elemento.clientHeight + 1;
  return porLargura || porLinhas;
}

export function iniciarDicasDeTextoCortado() {
  if (typeof document === 'undefined') return;

  document.addEventListener('mouseover', (evento) => {
    let elemento = evento.target instanceof Element ? evento.target : null;
    for (let nivel = 0; elemento && nivel < 4; nivel += 1, elemento = elemento.parentElement) {
      const automatico = elemento.dataset.dicaAuto === '1';
      if (elemento.hasAttribute('title') && !automatico) return;

      if (estaCortado(elemento)) {
        const texto = (elemento.innerText || elemento.textContent || '').trim();
        if (texto) {
          elemento.title = texto;
          elemento.dataset.dicaAuto = '1';
        }
        return;
      }
      if (automatico) {
        elemento.removeAttribute('title');
        delete elemento.dataset.dicaAuto;
      }
    }
  }, { passive: true });
}
