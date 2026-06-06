import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserSelectionView from '../views/UserSelectionView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardAdm from '../views/DashboardAdm.vue'
import DashboardOp from '../views/DashboardOp.vue'
import AnimalListView from '../views/AnimalListView.vue'
import AnimalFormView from '../views/AnimalFormView.vue'
import AnimalDetailView from '../views/AnimalDetailView.vue'
import LancamentoLeiteView from '@/views/LancamentoLeiteView.vue'
import PesagemView from '@/views/PesagemView.vue'
import ManejoView from '@/views/ManejoView.vue'
import RelatoriosView from '@/views/RelatoriosView.vue'
import SaudeView from '@/views/SaudeView.vue'
import VaccinationOperatorView from '@/views/VaccinationOperatorView.vue'
import AnimalConsultationView from '@/views/AnimalConsultationView.vue'
import TasksManagementView from '@/views/TasksManagementView.vue'
import EstabulosView from '@/views/EstabulosView.vue'
import SpeciesListView from '@/views/SpeciesListView.vue'
import BreedsListView from '@/views/BreedsListView.vue'
import VaccinesListView from '@/views/VaccinesListView.vue'
import LancamentoAlimentacaoView from '@/views/LancamentoAlimentacaoView.vue';
import DashboardAlimentacaoView from '@/views/DashboardAlimentacaoView.vue';
import VeterinaryRecordsView from '@/views/VeterinaryRecordsView.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/selection', name: 'selection', component: UserSelectionView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/dashboard-adm', name: 'dashboard-adm', component: DashboardAdm },
    { path: '/dashboard-op', name: 'dashboard-op', component: DashboardOp },
    
    // Rotas de Rebanho (CRUD)
    { path: '/animais', name: 'animal-list', component: AnimalListView },
    { path: '/animais/novo', name: 'animal-create', component: AnimalFormView }, 
    { path: '/animais/editar/:id', name: 'animal-edit', component: AnimalFormView }, 
    { path: '/animal/:id', name: 'animal-detail', component: AnimalDetailView },
    
    { path: '/lancamento-leite', name: 'lancamento-leite', component: LancamentoLeiteView },
    { path: '/pesagem', name: 'pesagem', component: PesagemView },
    { path: '/manejo', name: 'manejo', component: ManejoView },
    { path: '/relatorios', name: 'relatorios', component: RelatoriosView },
    { path: '/saude', name: 'saude', component: SaudeView },
    { path: '/especies', name: 'especies', component: SpeciesListView },
    { path: '/racas', name: 'racas', component: BreedsListView },
    { path: '/vacinas', name: 'vacinas', component: VaccinesListView },
    
    // Novas rotas do Operador
    { path: '/vaccination-operator', name: 'vaccination-operator', component: VaccinationOperatorView },
    { path: '/animal-consultation', name: 'animal-consultation', component: AnimalConsultationView },
    { path: '/tasks-management', name: 'tasks-management', component: TasksManagementView },
    { path: '/tarefas', name: 'tarefas', component: TasksManagementView },
    { path: '/vacinacao', name: 'vacinacao', component: VaccinationOperatorView },
    { path: '/rebanho', name: 'rebanho', component: AnimalConsultationView },
    { path: '/estabulos', name: 'estabulos', component: EstabulosView },
    {path: '/lancamento-alimentacao',name: 'lancamento-alimentacao', component: LancamentoAlimentacaoView},
    {path: '/dashboard-alimentacao',name: 'dashboard-alimentacao',component: DashboardAlimentacaoView},
    { path: '/veterinario', name: 'veterinario', component: VeterinaryRecordsView },
  ]
})

export default router