export const idRelacao = (value) => (
  value && typeof value === 'object' ? value.id : value
);

export function ultimaMovimentacaoPorAnimal(movements) {
  const latest = new Map();
  for (const movement of movements) {
    const animalId = idRelacao(movement.animal);
    if (animalId === null || animalId === undefined) continue;

    const key = String(animalId);
    const current = latest.get(key);
    const date = String(movement.movement_date || '');
    const currentDate = String(current?.movement_date || '');
    if (
      !current
      || date > currentDate
      || (date === currentDate && Number(movement.id) > Number(current.id))
    ) {
      latest.set(key, movement);
    }
  }
  return latest;
}

export function nomeEstabulo(quadrants, quadrantId) {
  const id = idRelacao(quadrantId);
  const quadrant = quadrants.find((item) => String(item.id) === String(id));
  return quadrant?.name || (id ? `Estábulo ${id}` : 'Sem lotação');
}
