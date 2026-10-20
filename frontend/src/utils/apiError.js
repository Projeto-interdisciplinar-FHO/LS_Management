const fieldLabels = {
  animal: 'Animal',
  vaccine: 'Vacina',
  sex: 'Sexo',
  specie: 'Espécie',
  breed: 'Raça',
  quadrant: 'Estábulo',
  purpose: 'Finalidade',
  name: 'Nome',
  birth_date: 'Data de nascimento',
  register_number: 'Brinco',
  weight: 'Peso',
  weighing_date: 'Data da pesagem',
  milk_production: 'Quantidade de leite',
  production_date: 'Data da ordenha',
  dosage: 'Dosagem',
  consultation_date: 'Data da consulta',
  consultation_reason: 'Motivo da consulta',
  consultation_solution: 'Tratativa',
  veterinarian: 'Veterinário',
  feeding_time: 'Data do trato',
  meal_weight: 'Quantidade de alimento',
  food: 'Alimento',
  next_vaccination_date: 'Data da próxima dose',
  vaccination_date: 'Data da vacinação',
};

function mensagensDoCampo(valor) {
  if (Array.isArray(valor)) return valor.flatMap(mensagensDoCampo);
  if (typeof valor === 'string' || typeof valor === 'number') return [String(valor)];
  if (valor && typeof valor === 'object') return Object.values(valor).flatMap(mensagensDoCampo);
  return [];
}

function rotuloDoCampo(campo) {
  return fieldLabels[campo] || campo.replaceAll('_', ' ');
}

export function apiErrorMessage(error, fallback = 'Não foi possível concluir a operação.') {
  const status = error?.response?.status;
  const data = error?.response?.data;

  if (!error?.response) return 'Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.';
  if (status === 401) return 'Sua sessão expirou. Entre novamente para continuar.';
  if (status === 403) return 'Você não tem permissão para realizar esta ação.';
  if (status === 404) return 'O registro solicitado não foi encontrado. Atualize a tela e tente novamente.';
  if (status === 409) return 'Os dados entraram em conflito com outro registro. Atualize a tela e tente novamente.';
  if (status === 429) return 'Muitas tentativas em pouco tempo. Aguarde e tente novamente.';
  if (status >= 500) return 'O servidor não conseguiu concluir a operação. Tente novamente em instantes.';

  if (typeof data === 'string' && data.trim()) return data;
  if (data && typeof data.detail === 'string') return data.detail;

  if (data && typeof data === 'object') {
    const mensagens = Object.entries(data).flatMap(([campo, valor]) => {
      const detalhes = mensagensDoCampo(valor);
      if (!detalhes.length) return [];
      if (campo === 'non_field_errors' || campo === 'detail') return detalhes;
      return [`${rotuloDoCampo(campo)}: ${detalhes.join(' ')}`];
    });
    if (mensagens.length) return mensagens.join(' ');
  }

  return fallback;
}