import api from './api';

export default {
  // Busca todos os animais do rebanho
  getAnimals() {
    return api.get('animals/');
  },
  // Busca um animal específico por ID
  getAnimal(id) {
    return api.get(`animals/${id}/`);
  },

  // Busca as raças cadastradas
  getBreeds() {
    return api.get('breeds/');
  }
};