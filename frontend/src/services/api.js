import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {

  getAnimals() {
    return apiClient.get('/animals');
  },
  createAnimal(data) {
    return apiClient.post('/animals', data);
  },
  updateAnimal(id, data) {
    return apiClient.put(`/animals/${id}`, data);
  },
  deleteAnimal(id) {
    return apiClient.delete(`/animals/${id}`);
  }
};