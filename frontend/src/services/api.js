import axios from 'axios';
import { limparSessao } from './auth';

// A URL do backend vem do ambiente, com o padrao apontando para a maquina
// local. Estava fixa aqui enquanto os componentes ja liam VITE_API_URL — as
// duas metades discordavam, e publicar em qualquer lugar que nao fosse
// 127.0.0.1 quebrava metade das telas em silencio.
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const API_BASE_URL = API_URL.replace(/\/$/, '');

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/`,
  headers: {
    'Content-Type': 'application/json'
  }
});

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

let refreshRequest = null;

const renovarAccessToken = () => {
  if (!refreshRequest) {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) return Promise.reject(new Error('Refresh token não encontrado.'));

    refreshRequest = axios
      .post(`${API_BASE_URL}/api/token/refresh/`, { refresh })
      .then(({ data }) => {
        if (!data.access) throw new Error('A renovação não retornou um access token.');
        localStorage.setItem('access_token', data.access);
        if (data.refresh) localStorage.setItem('refresh_token', data.refresh);
        return data.access;
      })
      .finally(() => {
        refreshRequest = null;
      });
  }

  return refreshRequest;
};

const encerrarSessao = () => {
  limparSessao();
  if (window.location.pathname !== '/login') window.location.href = '/login';
};

apiClient.interceptors.response.use(
  (resposta) => resposta,
  async (erro) => {
    const rota = window.location.pathname;
    const requisicao = erro.config;

    if (
      erro.response?.status !== 401 ||
      !requisicao ||
      rota === '/login' ||
      requisicao.url?.includes('api/token/')
    ) {
      return Promise.reject(erro);
    }

    if (requisicao._retry) {
      encerrarSessao();
      return Promise.reject(erro);
    }

    requisicao._retry = true;

    try {
      const access = await renovarAccessToken();
      requisicao.headers.Authorization = `Bearer ${access}`;
      return apiClient(requisicao);
    } catch (erroRenovacao) {
      encerrarSessao();
      return Promise.reject(erroRenovacao);
    }
  }
);

export default {
  // Funções genéricas expandidas para o CRUD completo
  get(url, config) { return apiClient.get(url, config); },
  post(url, data, config) { return apiClient.post(url, data, config); },
  put(url, data, config) { return apiClient.put(url, data, config); },
  patch(url, data, config) { return apiClient.patch(url, data, config); },
  delete(url, config) { return apiClient.delete(url, config); },

  login(credentials) {
    return apiClient.post('api/token/', credentials); 
  },
  getQuadrants() { return apiClient.get('quadrants/'); },
  getAnimals() { return apiClient.get('animals/'); },
  getAnimalById(id) { return apiClient.get(`animals/${id}/`); },
  createAnimal(animalData) { return apiClient.post('animals/', animalData); },
  updateAnimal(id, animalData) { return apiClient.put(`animals/${id}/`, animalData); },
  deleteAnimal(id) { return apiClient.delete(`animals/${id}/`); },
  getFeedings() { return apiClient.get('feedings/'); },
  getFeedingsByAnimal(animalId) { return apiClient.get(`feedings/?animal_id=${animalId}`); },
  createFeeding(feedingData) { return apiClient.post('feedings/', feedingData); },
  getFoods() { return apiClient.get('foods/'); },
    createFood(foodData) { return apiClient.post('foods/', foodData); },
    getVeterinaryRecords(animalId = null) {
      const url = animalId ? `animal_health/?animal_id=${animalId}` : 'animal_health/';
      return apiClient.get(url);
    },
    createVeterinaryRecord(data) { return apiClient.post('animal_health/', data); },
    deleteVeterinaryRecord(id) { return apiClient.delete(`animal_health/${id}`); },
  
  // Produção de Leite
  getMilkProductionByAnimal(animalId) { return apiClient.get(`milk_production_history/?animal_id=${animalId}`); },
  registrarProducaoLeite(data) { return apiClient.post('milk_production_history/', data); },
  
  // Histórico de Peso
  getWeightHistoryByAnimal(animalId) { return apiClient.get(`weight_history/?animal_id=${animalId}`); },
  registrarPeso(data) { return apiClient.post('weight_history/', data); },

  // Vacinação (Requisito 6)
  getVaccines() { return apiClient.get('vaccines/'); },
  getVaccinationsByAnimal(animalId) { 
    if (animalId === 0) {
      // Trazer todas as vacinações
      return apiClient.get('vaccinations/');
    }
    return apiClient.get(`vaccinations/?animal_id=${animalId}`);
  },
  createVaccination(data) { return apiClient.post('vaccinations/', data); },
  updateVaccination(id, data) { return apiClient.put(`vaccinations/${id}/`, data); },
  getVaccinationPlans() { return apiClient.get('vaccination_plans/'); },
  getUpcomingVaccinations() { return apiClient.get('vaccinations/upcoming/'); }
};