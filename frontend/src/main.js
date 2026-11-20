import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { iniciarTema } from './services/theme'
import { iniciarEfeitosDeClique } from './utils/clickEffects'
import './assets/styles/index.css'

iniciarTema()
iniciarEfeitosDeClique()

const app = createApp(App)
app.use(router)
app.mount('#app')
