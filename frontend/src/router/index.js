import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserSelectionView from '../views/UserSelectionView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardAdm from '../views/DashboardAdm.vue'
import DashboardOp from '../views/DashboardOp.vue'
import MapaView from '../views/MapaView.vue'
import AnimalListView from '../views/AnimalListView.vue'
import AnimalFormView from '../views/AnimalFormView.vue'
import AnimalDetailView from '../views/AnimalDetailView.vue'
import LancamentoLeiteView from '@/views/LancamentoLeiteView.vue'
import PesagemView from '@/views/PesagemView.vue'
import ManejoView from '@/views/ManejoView.vue'
import RelatoriosView from '@/views/RelatoriosView.vue'
import SaudeView from '@/views/SaudeView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/selection', name: 'selection', component: UserSelectionView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/dashboard-adm', name: 'dashboard-adm', component: DashboardAdm },
    { path: '/dashboard-op', name: 'dashboard-op', component: DashboardOp },
    { path: '/mapa', name: 'mapa', component: MapaView },
    
    // Rotas de Rebanho (CRUD)
    { path: '/animais', name: 'animal-list', component: AnimalListView },
    { path: '/animais/novo', name: 'animal-create', component: AnimalFormView }, 
    { path: '/animais/editar/:id', name: 'animal-edit', component: AnimalFormView }, 
    { path: '/animal/:id', name: 'animal-detail', component: AnimalDetailView },
    
    { path: '/lancamento-leite', name: 'lancamento-leite', component: LancamentoLeiteView },
    { path: '/pesagem', name: 'pesagem', component: PesagemView },
    { path: '/manejo', name: 'manejo', component: ManejoView },
    { path: '/relatorios', name: 'relatorios', component: RelatoriosView },
    { path: '/saude', name: 'saude', component: SaudeView }
  ]
})

export default router