import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/', 
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
  
  // Produção de Leite
  getMilkProductionByAnimal(animalId) { return apiClient.get(`milk_production_history/animal/${animalId}/`); },
  registrarProducaoLeite(data) { return apiClient.post('milk_production_history/', data); },
  
  // Histórico de Peso
  getWeightHistoryByAnimal(animalId) { return apiClient.get(`weight_history/animal/${animalId}/`); },
  registrarPeso(data) { return apiClient.post('weight_history/', data); },

  // Vacinação (Requisito 6)
  getVaccines() { return apiClient.get('vaccines/'); },
  getVaccinationsByAnimal(animalId) { 
    if (animalId === 0) {
      // Trazer todas as vacinações
      return apiClient.get('vaccinations/');
    }
    return apiClient.get(`vaccinations/animal/${animalId}/`);
  },
  createVaccination(data) { return apiClient.post('vaccinations/', data); },
  updateVaccination(id, data) { return apiClient.put(`vaccinations/${id}/`, data); },
  getVaccinationPlans() { return apiClient.get('vaccination_plans/'); },
  getUpcomingVaccinations() { return apiClient.get('vaccinations/upcoming/'); }
};