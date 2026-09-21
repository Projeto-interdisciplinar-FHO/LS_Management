import { createRouter, createWebHistory } from 'vue-router'
import { estaLogado, ehAdministrador, painelDoPapel } from '@/services/auth'

// public — Início, escolha de perfil, login
import HomeView from '@/views/public/HomeView.vue'
import UserSelectionView from '@/views/public/UserSelectionView.vue'
import LoginView from '@/views/public/LoginView.vue'

// dashboards — Painéis
import DashboardAdm from '@/views/dashboards/DashboardAdm.vue'
import DashboardOp from '@/views/dashboards/DashboardOp.vue'

// herd — Rebanho
import AnimalListView from '@/views/herd/AnimalListView.vue'
import AnimalFormView from '@/views/herd/AnimalFormView.vue'
import AnimalDetailView from '@/views/herd/AnimalDetailView.vue'
import AnimalConsultationView from '@/views/herd/AnimalConsultationView.vue'
import EstabulosView from '@/views/herd/EstabulosView.vue'

// handling — Manejo
import ManejoView from '@/views/handling/ManejoView.vue'
import PesagemView from '@/views/handling/PesagemView.vue'
import LancamentoLeiteView from '@/views/handling/LancamentoLeiteView.vue'
import LancamentoAlimentacaoView from '@/views/handling/LancamentoAlimentacaoView.vue'

// health — Saúde
import SaudeView from '@/views/health/SaudeView.vue'
import VaccinationOperatorView from '@/views/health/VaccinationOperatorView.vue'
import VeterinaryRecordsView from '@/views/health/VeterinaryRecordsView.vue'

// registry — Cadastros
import SpeciesListView from '@/views/registry/SpeciesListView.vue'
import BreedsListView from '@/views/registry/BreedsListView.vue'
import VaccinesListView from '@/views/registry/VaccinesListView.vue'
import DashboardAlimentacaoView from '@/views/registry/DashboardAlimentacaoView.vue'
import UsuariosView from '@/views/registry/UsuariosView.vue'

// reports — Relatórios
import RelatoriosView from '@/views/reports/RelatoriosView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView, meta: { publico: true } },
    { path: '/selection', name: 'selection', component: UserSelectionView, meta: { publico: true } },
    { path: '/login', name: 'login', component: LoginView, meta: { publico: true } },
    { path: '/dashboard-adm', name: 'dashboard-adm', component: DashboardAdm, meta: { requerLogin: true, soAdmin: true } },
    { path: '/dashboard-op', name: 'dashboard-op', component: DashboardOp, meta: { requerLogin: true } },
    
    // Rotas de Rebanho (CRUD)
    { path: '/animais', name: 'animal-list', component: AnimalListView, meta: { requerLogin: true } },
    { path: '/animais/novo', name: 'animal-create', component: AnimalFormView, meta: { requerLogin: true, soAdmin: true } }, 
    { path: '/animais/editar/:id', name: 'animal-edit', component: AnimalFormView, meta: { requerLogin: true, soAdmin: true } }, 
    { path: '/animal/:id', name: 'animal-detail', component: AnimalDetailView, meta: { requerLogin: true } },
    
    { path: '/lancamento-leite', name: 'lancamento-leite', component: LancamentoLeiteView, meta: { requerLogin: true } },
    { path: '/pesagem', name: 'pesagem', component: PesagemView, meta: { requerLogin: true } },
    { path: '/manejo', name: 'manejo', component: ManejoView, meta: { requerLogin: true } },
    { path: '/relatorios', name: 'relatorios', component: RelatoriosView, meta: { requerLogin: true, soAdmin: true } },
    { path: '/saude', name: 'saude', component: SaudeView, meta: { requerLogin: true } },
    { path: '/especies', name: 'especies', component: SpeciesListView, meta: { requerLogin: true, soAdmin: true } },
    { path: '/racas', name: 'racas', component: BreedsListView, meta: { requerLogin: true, soAdmin: true } },
    { path: '/vacinas', name: 'vacinas', component: VaccinesListView, meta: { requerLogin: true, soAdmin: true } },
    
    // Novas rotas do Operador
    { path: '/vaccination-operator', name: 'vaccination-operator', component: VaccinationOperatorView, meta: { requerLogin: true } },
    { path: '/animal-consultation', name: 'animal-consultation', component: AnimalConsultationView, meta: { requerLogin: true } },
    { path: '/vacinacao', name: 'vacinacao', component: VaccinationOperatorView, meta: { requerLogin: true } },
    { path: '/rebanho', name: 'rebanho', component: AnimalConsultationView, meta: { requerLogin: true } },
    { path: '/estabulos', name: 'estabulos', component: EstabulosView, meta: { requerLogin: true, soAdmin: true } },
    {path: '/lancamento-alimentacao',name: 'lancamento-alimentacao', component: LancamentoAlimentacaoView, meta: { requerLogin: true } },
    {path: '/dashboard-alimentacao',name: 'dashboard-alimentacao',component: DashboardAlimentacaoView, meta: { requerLogin: true } },
    { path: '/veterinario', name: 'veterinario', component: VeterinaryRecordsView, meta: { requerLogin: true } },
    { path: '/usuarios', name: 'usuarios', component: UsuariosView, meta: { requerLogin: true, soAdmin: true } },
  ]
})

// Sem isto, digitar /dashboard-adm na barra de endereco entrava direto, sem
// login e sem ser administrador — as telas existiam separadas, mas nada
// impedia de abrir a do outro perfil.
//
// Isto e conveniencia de navegacao, NAO seguranca: quem protege o dado e o
// backend, que confere o usuario do token a cada requisicao. Uma guarda de
// rota so evita que a pessoa veja uma tela que nao vai conseguir usar.
router.beforeEach((para, de, segue) => {
  if (para.meta?.publico) return segue()

  if (para.meta?.requerLogin && !estaLogado()) {
    return segue({ path: '/login', query: { destino: para.fullPath } })
  }

  if (para.meta?.soAdmin && !ehAdministrador()) {
    return segue(painelDoPapel())
  }

  return segue()
})


export default router