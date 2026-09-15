/**
 * Confirmação de ações destrutivas.
 *
 * As quatro exclusões do app usavam o `confirm()` do navegador: uma caixa
 * cinza do sistema operacional, com os botões "OK/Cancelar" em inglês em
 * metade das máquinas, sem dizer o que exatamente ia sumir. Fora do lugar
 * numa tela que já tem os seus próprios diálogos.
 *
 * Mesmo formato do `notify`: a tela chama e espera a resposta, o diálogo
 * vive uma vez só, montado na raiz.
 *
 *   if (await confirmar({ titulo: 'Excluir animal?', acao: 'Excluir' })) { ... }
 */
export function confirmar({ titulo, texto = '', acao = 'Confirmar', destrutivo = true }) {
  if (typeof window === 'undefined') return Promise.resolve(false);

  return new Promise((resolver) => {
    window.dispatchEvent(new CustomEvent('app-confirm', {
      detail: { titulo, texto, acao, destrutivo, resolver },
    }));
  });
}
