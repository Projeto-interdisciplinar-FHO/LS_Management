import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserSelectionView from '../views/UserSelectionView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import DashboardAdm from '../views/DashboardAdm.vue'
import DashboardOp from '../views/DashboardOp.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/dashboard', name: 'dashboard', component: DashboardView },
    { path: '/dashboard-adm', name: 'dashboard-adm', component: DashboardAdm },
    { path: '/selection', name: 'selection', component: UserSelectionView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/dashboard-op', name: 'dashboard-op', component: DashboardOp }
  ]
})

export default router