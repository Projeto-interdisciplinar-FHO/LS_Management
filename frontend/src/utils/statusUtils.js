/**
 * Situação do animal, num lugar só.
 *
 * O modelo `Animal` do backend tem DOIS campos para a mesma ideia: `status`,
 * com cinco opções (ativo, doente, vendido, obito, inativo), e `active`, um
 * booleano marcado no próprio código como "mantido para compatibilidade".
 *
 * A tela de cadastro só mexia no booleano, e a de consulta só filtrava pelo
 * `status` — dava para filtrar por "doente" e não havia onde marcar um animal
 * como doente. Agora a interface expõe um controle só, o `status`, e o
 * booleano é derivado dele na hora de salvar.
 *
 * As cores saem dos tokens do design system; este arquivo não escolhe
 * hexadecimal nenhum.
 */

export const SITUACOES = [
  { valor: 'ativo',   rotulo: 'Ativo',   badge: 'badge--ok',     noRebanho: true },
  { valor: 'doente',  rotulo: 'Doente',  badge: 'badge--warn',   noRebanho: true },
  { valor: 'vendido', rotulo: 'Vendido', badge: '',              noRebanho: false },
  { valor: 'obito',   rotulo: 'Óbito',   badge: 'badge--danger', noRebanho: false },
  { valor: 'inativo', rotulo: 'Inativo', badge: '',              noRebanho: false },
];

const PADRAO = SITUACOES[0];

export function situacao(status) {
  return SITUACOES.find((s) => s.valor === String(status || '').toLowerCase()) || PADRAO;
}

export function rotuloSituacao(status) {
  return situacao(status).rotulo;
}

export function badgeSituacao(status) {
  return situacao(status).badge;
}

/**
 * O valor do booleano legado para um dado status.
 *
 * Doente continua ativo: o animal segue no rebanho e nas rotinas de manejo,
 * só que precisando de atenção. Quem sai do rebanho é vendido, óbito e o
 * inativo explícito.
 */
export function ativoPara(status) {
  return situacao(status).noRebanho;
}
