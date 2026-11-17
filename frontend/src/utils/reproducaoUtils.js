// Prazos estimados para orientar o acompanhamento; não confirmam prenhez.

export const DIAS_ATE_ULTRASSOM = 30;
export const DIAS_LIMITE_ULTRASSOM = 90;

const DIA_MS = 24 * 60 * 60 * 1000;

export function hojeIso() {
  const agora = new Date();
  return new Date(agora.getTime() - agora.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

function dataLocal(iso) {
  const texto = String(iso || '').slice(0, 10);
  const data = new Date(`${texto}T00:00:00`);
  return Number.isNaN(data.getTime()) ? null : data;
}

export function diasEntre(inicioIso, fimIso) {
  const inicio = dataLocal(inicioIso);
  const fim = dataLocal(fimIso);
  if (!inicio || !fim) return null;
  return Math.round((fim.getTime() - inicio.getTime()) / DIA_MS);
}

/**
 * Situação de acompanhamento calculada pela data, nunca uma confirmação clínica.
 * fase: 'aguardando' | 'ultrassom' | 'diagnostico-atrasado'
 */
export function situacaoDaInseminacao(dataInseminacao, hoje = hojeIso()) {
  const dias = diasEntre(dataInseminacao, hoje);
  if (dias === null) return null;

  const diasParaUltrassom = DIAS_ATE_ULTRASSOM - dias;

  let fase = 'aguardando';
  if (dias > DIAS_LIMITE_ULTRASSOM) fase = 'diagnostico-atrasado';
  else if (dias >= DIAS_ATE_ULTRASSOM) fase = 'ultrassom';

  return { dias, diasParaUltrassom, fase };
}

/** Mantém apenas a inseminação mais recente de cada matriz. */
export function ultimaInseminacaoPorMatriz(inseminacoes, idRelacao) {
  const mapa = new Map();
  for (const registro of inseminacoes) {
    const matriz = String(idRelacao(registro.mother ?? registro.mother_id));
    const atual = mapa.get(matriz);
    if (!atual || String(registro.date) > String(atual.date)) mapa.set(matriz, registro);
  }
  return mapa;
}
