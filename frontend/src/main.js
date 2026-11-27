import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { iniciarTema } from './services/theme'
import { iniciarEfeitosDeClique } from './utils/clickEffects'
import { iniciarDicasDeTextoCortado } from './utils/textoCortado'
import './assets/styles/index.css'

iniciarTema()
iniciarEfeitosDeClique()
iniciarDicasDeTextoCortado()

const app = createApp(App)
app.use(router)
app.mount('#app')
