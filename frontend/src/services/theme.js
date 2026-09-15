/**
 * Tema claro/escuro, num lugar só.
 *
 * Antes o tema era uma classe no <html> e cada tela tentava adivinhar se ela
 * estava lá — três telas montavam um MutationObserver só para reagir à
 * troca, e o App.vue carregava umas 200 linhas de sobrescrita com
 * `!important` para repintar componente por componente.
 *
 * Agora o tema é um atributo `data-theme` no <html> e a paleta inteira é
 * redefinida em tokens.css. Nenhum componente precisa saber qual tema está
 * ativo: ele só usa `var(--surface)`, `var(--text)` e afins.
 */
import { ref } from 'vue';

const CHAVE = 'appTheme';

function preferidoDoSistema() {
  return window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function guardado() {
  const valor = localStorage.getItem(CHAVE);
  return valor === 'dark' || valor === 'light' ? valor : null;
}

export const temaAtual = ref(guardado() || preferidoDoSistema());

export function aplicarTema(tema) {
  temaAtual.value = tema;
  document.documentElement.setAttribute('data-theme', tema);
  localStorage.setItem(CHAVE, tema);
}

export function alternarTema() {
  aplicarTema(temaAtual.value === 'dark' ? 'light' : 'dark');
}

/** Chamado uma vez na subida do app, antes do primeiro render. */
export function iniciarTema() {
  document.documentElement.setAttribute('data-theme', temaAtual.value);

  // Enquanto a pessoa não escolher um tema à mão, o app acompanha o sistema.
  window.matchMedia?.('(prefers-color-scheme: dark)').addEventListener?.('change', (evento) => {
    if (guardado()) return;
    temaAtual.value = evento.matches ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', temaAtual.value);
  });
}
