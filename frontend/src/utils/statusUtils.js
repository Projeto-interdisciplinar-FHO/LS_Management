export const SITUACOES = [
  { valor: 'active', rotulo: 'Ativo', badge: 'badge--ok', noRebanho: true },
  { valor: 'inactive', rotulo: 'Inativo', badge: '', noRebanho: false },
  { valor: 'sold', rotulo: 'Vendido', badge: '', noRebanho: false },
  { valor: 'deceased', rotulo: 'Óbito', badge: 'badge--danger', noRebanho: false },
];

const PADRAO = {
  valor: 'unknown',
  rotulo: 'Não informado',
  badge: '',
  noRebanho: false,
};
const ALIASES = {
  ativo: 'active',
  inativo: 'inactive',
  vendido: 'sold',
  obito: 'deceased',
  óbito: 'deceased',
};

export function situacao(status) {
  const normalizado = String(status || '').toLowerCase();
  const valor = ALIASES[normalizado] || normalizado;
  return SITUACOES.find((item) => item.valor === valor) || PADRAO;
}

export function rotuloSituacao(status) {
  return situacao(status).rotulo;
}

export function badgeSituacao(status) {
  return situacao(status).badge;
}
