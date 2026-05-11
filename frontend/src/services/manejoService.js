import api from './api';

export default {
  // Registra um novo peso no histórico (app weight_history)
  registrarPeso(data) {
    return api.post('weight-history/', data);
  },

  // Registra uma vacinação (app vaccinations)[cite: 17]
  registrarVacina(data) {
    return api.post('vaccinations/', data);
  },

  // Busca os planos de vacinação ativos para preencher o formulário[cite: 17]
  getPlanosVacina() {
    return api.get('vaccination-plans/');
  },

  // Busca as vacinas disponíveis[cite: 17]
  getVaccines() {
    return api.get('vaccines/');
  }
};