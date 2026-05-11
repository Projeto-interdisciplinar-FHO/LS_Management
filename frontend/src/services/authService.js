import api from './api';

export default {
  // Faz o login e retorna o Token
  async login(credentials) {
    const response = await api.post('api/token/', credentials);
    return response;
  },
  
  // Exemplo de rota de cadastro de novos usuários (ajuste a URL conforme seu Django)
  async register(userData) {
    const response = await api.post('users/register/', userData);
    return response;
  }
};