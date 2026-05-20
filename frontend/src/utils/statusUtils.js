/**
 * Mapeamento de status de animais para cores, ícones e labels
 */
export const STATUS_CONFIG = {
  ativo: {
    label: 'Ativo',
    color: '#3fb950',
    bgColor: 'rgba(63, 185, 80, 0.1)',
    borderColor: '#3fb950',
    icon: '●',
    badgeClass: 'status-active'
  },
  doente: {
    label: 'Doente',
    color: '#d29922',
    bgColor: 'rgba(210, 153, 34, 0.1)',
    borderColor: '#d29922',
    icon: '⚠',
    badgeClass: 'status-sick',
    animation: 'pulse'
  },
  vendido: {
    label: 'Vendido',
    color: '#8b949e',
    bgColor: 'rgba(139, 148, 158, 0.1)',
    borderColor: '#8b949e',
    icon: '✓',
    badgeClass: 'status-sold'
  },
  obito: {
    label: 'Óbito',
    color: '#f85149',
    bgColor: 'rgba(248, 81, 73, 0.1)',
    borderColor: '#f85149',
    icon: '✗',
    badgeClass: 'status-dead'
  },
  inativo: {
    label: 'Inativo',
    color: '#656d76',
    bgColor: 'rgba(101, 109, 118, 0.1)',
    borderColor: '#656d76',
    icon: '○',
    badgeClass: 'status-inactive'
  }
};

/**
 * Retorna a configuração de status para um animal
 * @param {string} status - Status do animal (ativo, doente, vendido, obito, inativo)
 * @returns {object} Configuração com cor, ícone, label, etc.
 */
export function getStatusConfig(status) {
  return STATUS_CONFIG[status?.toLowerCase()] || STATUS_CONFIG.inativo;
}

/**
 * Retorna apenas a cor do status
 */
export function getStatusColor(status) {
  return getStatusConfig(status).color;
}

/**
 * Retorna apenas o ícone do status
 */
export function getStatusIcon(status) {
  return getStatusConfig(status).icon;
}

/**
 * Retorna apenas o label do status
 */
export function getStatusLabel(status) {
  return getStatusConfig(status).label;
}

/**
 * Retorna a classe CSS para o status
 */
export function getStatusBadgeClass(status) {
  return getStatusConfig(status).badgeClass;
}

/**
 * Lista de todas as opções de status para select/dropdown
 */
export const STATUS_OPTIONS = [
  { value: 'ativo', label: '✓ Ativo', icon: '●' },
  { value: 'doente', label: '⚠ Doente', icon: '⚠' },
  { value: 'vendido', label: '✓ Vendido', icon: '✓' },
  { value: 'obito', label: '✗ Óbito', icon: '✗' },
  { value: 'inativo', label: '○ Inativo', icon: '○' }
];

/**
 * Função para verificar se um status indica que o animal está "ativo para operações"
 */
export function isOperational(status) {
  return status === 'ativo';
}

/**
 * Função para verificar se um animal precisa de atenção (doente)
 */
export function needsAttention(status) {
  return status === 'doente';
}

/**
 * Função para contar animais por status em um array
 */
export function countByStatus(animals) {
  const counts = {
    ativo: 0,
    doente: 0,
    vendido: 0,
    obito: 0,
    inativo: 0
  };

  animals.forEach(animal => {
    const status = animal.status?.toLowerCase() || 'inativo';
    if (counts.hasOwnProperty(status)) {
      counts[status]++;
    }
  });

  return counts;
}
