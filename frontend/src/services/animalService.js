import api from './api';

export default {
  // Busca todos os animais do rebanho
getAnimals() {
  return api.get('species/');
},
  // Busca um animal específico por ID
  getAnimal(id) {
    return api.get(`animals/${id}/`);
  },

  // Busca as espécies cadastradas (Bovinos, Ovinos, etc)[cite: 17]
  getSpecies() {
    return api.get('species/');
  },

  // Busca as raças cadastradas[cite: 17]
  getBreeds() {
    return api.get('breeds/');
  }
};