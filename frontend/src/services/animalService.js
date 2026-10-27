import api from './api';

export default {
  // Busca todos os animais do rebanho
  getAnimals() {
    return api.get('cows/');
  },
  // Busca um animal específico por ID
  getAnimal(id) {
    return api.get(`cows/${id}/`);
  },

  // Busca as raças cadastradas[cite: 17]
  getBreeds() {
    return api.get('breeds/');
  }
};