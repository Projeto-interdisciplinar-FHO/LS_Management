import api from './api';

/**
 * Sessao e usuarios.
 *
 * O `register` apontava para `users/register/` com um comentario dizendo
 * "ajuste a URL conforme seu Django" — a rota nao existia. Agora existe, e
 * as demais operacoes de usuario moram aqui junto.
 */
export default {
  login(credenciais) {
    return api.post('authentication/token/', credenciais);
  },

  listarUsuarios() {
    return api.get('users/');
  },

  cadastrarUsuario(dados) {
    return api.post('users/register/', dados);
  },

  atualizarUsuario(id, dados) {
    return api.patch(`users/${id}/`, dados);
  },

  // Nao ha exclusao de proposito: usuario apagado leva junto o historico de
  // quem lancou cada pesagem e cada vacinacao. Para tirar de circulacao,
  // desativa-se — o login para de funcionar e o rastro fica.
  definirAtivo(id, ativo) {
    return api.patch(`users/${id}/`, { is_active: ativo });
  },

  register(dados) {          // nome antigo, mantido para nao quebrar chamadas
    return this.cadastrarUsuario(dados);
  },
};
