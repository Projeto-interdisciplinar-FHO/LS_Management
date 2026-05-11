import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/', 
  headers: {
    'Content-Type': 'application/json'
  }
});

// =========================================================
// INTERCEPTOR DE SEGURANÇA
// Pega o token do localStorage e injeta em todas as chamadas
// =========================================================
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default {
  // -------------------------------------------------------
  // FUNÇÕES GENÉRICAS (Garante que api.get e api.post funcionem nas Views)
  // -------------------------------------------------------
  get(url, config) {
    return apiClient.get(url, config);
  },
  post(url, data, config) {
    return apiClient.post(url, data, config);
  },

  // -------------------------------------------------------
  // AUTENTICAÇÃO
  // -------------------------------------------------------
  login(credentials) {
    // Rota padrão do SimpleJWT ou Knox do Django (Ajuste se sua URL for diferente)
    return apiClient.post('api/token/', credentials); 
  },

  // -------------------------------------------------------
  // FUNCIONALIDADES EXISTENTES (NÃO ALTERADAS)
  // -------------------------------------------------------
  
  // Quadrantes (Mapa)
  getQuadrants() {
    return apiClient.get('quadrants/');
  },
  
  // Animais
  getAnimals() {
    return apiClient.get('animals/');
  },
  
  getAnimalById(id) {
    const url = `animals/${id}/`;
    console.log("Requisitando URL:", url);
    return apiClient.get(url);
  },
  
  createAnimal(animalData) {
    console.log("Criando animal com dados:", animalData);
    return apiClient.post('animals/', animalData);
  },
  
  // Produção de Leite
  registrarProducaoLeite(data) {
    return apiClient.post('historico-prod-leite/', data);
  }
};