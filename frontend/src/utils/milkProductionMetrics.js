import { idRelacao } from '@/utils/animalMovementUtils';

function dataDaOrdenha(registro) {
  for (const campo of ['production_date', 'date_collected', 'date']) {
    if (!registro?.[campo]) continue;
    const valor = String(registro[campo]).slice(0, 10);
    const data = new Date(`${valor}T00:00:00`);
    if (!Number.isNaN(data.getTime())) return { data, valor };
  }
  return null;
}

export function ordenhasNosUltimosDias(registros, dias, hoje = new Date()) {
  const fim = new Date(hoje);
  fim.setHours(0, 0, 0, 0);
  const inicio = new Date(fim);
  inicio.setDate(inicio.getDate() - dias);

  return registros.filter((registro) => {
    const data = dataDaOrdenha(registro)?.data;
    return data && data >= inicio && data <= fim;
  });
}

export function ordenhasDoMesAtual(registros, hoje = new Date()) {
  const fim = new Date(hoje);
  fim.setHours(0, 0, 0, 0);
  const inicio = new Date(fim.getFullYear(), fim.getMonth(), 1);

  return registros.filter((registro) => {
    const data = dataDaOrdenha(registro)?.data;
    return data && data >= inicio && data <= fim;
  });
}

export function metricasProducaoPorAnimal(animais, registros) {
  const animaisPorId = new Map(animais.map((animal) => [String(animal.id), animal]));
  const totais = new Map();
  let totalLitros = 0;
  let totalOrdenhas = 0;

  for (const registro of registros) {
    const animalId = idRelacao(registro.animal ?? registro.animal_id);
    const animal = animaisPorId.get(String(animalId));
    const litros = Number(registro.milk_production ?? registro.milk_quantity ?? registro.quantity);
    if (!animal || !Number.isFinite(litros) || litros <= 0) continue;

    const data = dataDaOrdenha(registro)?.valor || '';
    const item = totais.get(String(animal.id)) || { animal, litros: 0, registros: 0, ultimaOrdenha: '' };
    item.litros += litros;
    item.registros += 1;
    item.ultimaOrdenha = data > item.ultimaOrdenha ? data : item.ultimaOrdenha;
    totais.set(String(animal.id), item);
    totalLitros += litros;
    totalOrdenhas += 1;
  }

  const mediaRebanho = totalOrdenhas ? totalLitros / totalOrdenhas : 0;
  const mediasPorAnimal = [...totais.values()].map((item) => ({
    ...item,
    media: item.litros / item.registros,
  }));
  const abaixoDaMedia = mediasPorAnimal
    .filter((item) => item.media < mediaRebanho)
    .sort((a, b) => b.ultimaOrdenha.localeCompare(a.ultimaOrdenha) || a.media - b.media);

  return { totalLitros, totalOrdenhas, mediaRebanho, mediasPorAnimal, abaixoDaMedia };
}
