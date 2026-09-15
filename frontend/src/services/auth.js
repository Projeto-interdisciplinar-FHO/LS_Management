/**
 * Quem está logado, num lugar só.
 *
 * Antes cada tela lia `localStorage` na mão, e o papel era deduzido de
 * `is_superuser` — o que dava dois defeitos: só existiam dois perfis
 * possíveis, e um "Operador" cadastrado como superusuário entrava como
 * administrador. Agora o papel vem do backend, que o calcula pelos grupos.
 *
 * O `user_role` continua sendo gravado como 'adm'/'op' porque dez telas já
 * o consomem nesse formato. Trocar o valor quebraria todas de uma vez, sem
 * ganho — o que precisava mudar era a ORIGEM do papel, não o rótulo.
 *
 * Isto NÃO é controle de acesso: serve para a tela saber o que desenhar.
 * Quem autoriza de verdade é o backend, que confere o usuário do token a
 * cada requisição. Esconder um botão não protege nada.
 */

const CHAVE_TOKEN = 'access_token';
const CHAVE_REFRESH = 'refresh_token';
const CHAVE_PAPEL = 'papel';
const CHAVE_ROLE = 'user_role';   // legado: 'adm' | 'op'
const CHAVE_NOME = 'nome_usuario';

export const ADMINISTRADOR = 'Administrador';
export const OPERADOR = 'Operador';

export function guardarSessao(dados) {
  localStorage.setItem(CHAVE_TOKEN, dados.access);
  if (dados.refresh) localStorage.setItem(CHAVE_REFRESH, dados.refresh);

  // Se o backend for antigo e não mandar `papel`, cai no is_superuser —
  // assim a tela nova funciona contra uma API que ainda não subiu.
  const papel = dados.papel || (dados.is_superuser ? ADMINISTRADOR : OPERADOR);
  localStorage.setItem(CHAVE_PAPEL, papel);
  localStorage.setItem(CHAVE_ROLE, papel === ADMINISTRADOR ? 'adm' : 'op');
  localStorage.setItem(CHAVE_NOME, dados.nome || dados.username || '');
}

export function limparSessao() {
  [CHAVE_TOKEN, CHAVE_REFRESH, CHAVE_PAPEL, CHAVE_ROLE, CHAVE_NOME]
    .forEach((c) => localStorage.removeItem(c));
}

export function token() {
  return localStorage.getItem(CHAVE_TOKEN);
}

export function estaLogado() {
  return Boolean(token());
}

export function papel() {
  return localStorage.getItem(CHAVE_PAPEL) || '';
}

export function nome() {
  return localStorage.getItem(CHAVE_NOME) || '';
}

export function ehAdministrador() {
  return papel() === ADMINISTRADOR;
}

/** Para onde mandar alguém que acabou de entrar, ou que errou de porta. */
export function painelDoPapel() {
  return ehAdministrador() ? '/dashboard-adm' : '/dashboard-op';
}
