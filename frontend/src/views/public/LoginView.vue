<template>
  <div class="login">
    <div class="login__coluna">
      <RouterLink to="/" class="login__voltar">
        <AppIcon name="arrow-left" :size="14" />
        <span>Início</span>
      </RouterLink>

      <div class="login__caixa">
        <header class="login__topo">
          <img :src="logoImage" alt="" class="login__logo">
          <h1>Entrar</h1>
          <p>Use as credenciais cadastradas para a fazenda.</p>
        </header>

        <form class="stack" @submit.prevent="handleLogin">
          <div class="field">
            <label class="field__label" for="usuario">Usuário</label>
            <input
              id="usuario"
              v-model="username"
              class="input"
              type="text"
              autocomplete="username"
              placeholder="seu.login"
              required
            >
          </div>

          <div class="field">
            <label class="field__label" for="senha">Senha</label>
            <div class="senha">
              <input
                id="senha"
                v-model="password"
                class="input"
                :type="mostrarSenha ? 'text' : 'password'"
                autocomplete="current-password"
                placeholder="••••••••"
                required
              >
              <button
                type="button"
                class="senha__alternar"
                :aria-label="mostrarSenha ? 'Ocultar senha' : 'Mostrar senha'"
                @click="mostrarSenha = !mostrarSenha"
              >
                {{ mostrarSenha ? 'ocultar' : 'mostrar' }}
              </button>
            </div>
          </div>

          <p v-if="errorMessage" class="alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ errorMessage }}</span>
          </p>

          <button type="submit" class="btn btn--primary btn--lg btn--block" :disabled="loading">
            <span v-if="loading" class="spinner" aria-hidden="true"></span>
            {{ loading ? 'Autenticando...' : 'Entrar' }}
          </button>
        </form>
      </div>

      <p class="login__rodape">
        Não tem acesso? Peça a um administrador para cadastrar seu usuário.
      </p>
    </div>

    <aside class="login__lateral">
      <div class="login__lateral-texto">
        <p class="login__lateral-titulo">L.S Management</p>
        <p class="login__lateral-sub">Controle sanitário, produtivo e de manejo do rebanho.</p>
      </div>
      <img :src="backgroundImage" alt="">
    </aside>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { guardarSessao, painelDoPapel } from '@/services/auth';
import api from '@/services/api';
import AppIcon from '@/components/ui/AppIcon.vue';
import logoImage from '@/assets/images/logo-vaca-ls.png';
import backgroundImage from '@/assets/images/background_fazenda.jpeg';

const router = useRouter();
const route = useRoute();

const username = ref('');
const password = ref('');
const loading = ref(false);
const mostrarSenha = ref(false);
const errorMessage = ref('');

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMessage.value = "Preencha todos os campos.";
    return;
  }

  loading.value = true;
  errorMessage.value = '';

  try {
    const response = await api.post('api/token/', {
      username: username.value,
      password: password.value
    });

    // O papel vem do backend, que o calcula pelos grupos do usuario. Antes
    // era deduzido de is_superuser aqui, o que fazia um Operador cadastrado
    // como superusuario cair no painel de administrador.
    guardarSessao(response.data);

    // Se a pessoa tentou abrir uma tela e foi mandada para o login, volta
    // para onde ela queria ir em vez de despeja-la no painel.
    const destino = route.query.destino;
    router.push(destino || painelDoPapel());

  } catch (error) {
    console.error("Erro no login:", error);
    if (error.response && error.response.status === 401) {
      errorMessage.value = "Usuário ou senha incorretos.";
    } else {
      errorMessage.value = "Falha ao conectar com o servidor.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 0.9fr);
  min-height: 100vh;
  background: var(--bg);
}

.login__coluna {
  display: grid;
  grid-template-rows: auto 1fr auto;
  justify-items: center;
  gap: 24px;
  padding: 32px 24px;
}

.login__voltar {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  justify-self: start;
  color: var(--text-3);
  font-size: var(--fs-sm);
  font-weight: 500;
  text-decoration: none;
}

.login__voltar:hover { color: var(--text); text-decoration: none; }

.login__caixa {
  align-self: center;
  width: 100%;
  max-width: 372px;
}

.login__topo { margin-bottom: 26px; }

/* Arte branca sobre transparente: invertida para aparecer no tema claro. */
.login__logo {
  height: 38px;
  width: auto;
  margin-bottom: 20px;
  filter: invert(1);
}

:root[data-theme='dark'] .login__logo { filter: none; }

.login__topo h1 {
  font-size: var(--fs-2xl);
  font-weight: 600;
  letter-spacing: -0.02em;
}

.login__topo p {
  margin-top: 5px;
  color: var(--text-2);
}

/* Ver o que se digitou evita metade dos "usuário ou senha incorretos". */
.senha { position: relative; }

.senha .input { padding-right: 74px; }

.senha__alternar {
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  height: 24px;
  padding: 0 8px;
  border: 0;
  border-radius: var(--r-sm);
  background: transparent;
  color: var(--text-3);
  font-family: inherit;
  font-size: var(--fs-xs);
  font-weight: 500;
}

.senha__alternar:hover { background: var(--surface-3); color: var(--text-2); }

.login__caixa .spinner {
  border-color: rgba(255, 255, 255, 0.35);
  border-top-color: currentColor;
}

.login__rodape {
  color: var(--text-3);
  font-size: var(--fs-sm);
  text-align: center;
}

/* Lateral com a foto: identidade, sem virar um bloco de cor chapada. */
.login__lateral {
  position: relative;
  overflow: hidden;
  border-left: 1px solid var(--line);
  background: var(--surface-3);
}

.login__lateral img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.6) saturate(0.85);
}

/* A foto muda de claro a escuro conforme a hora do dia; a legenda não pode
   depender de sorte para continuar legível. */
.login__lateral::after {
  content: '';
  position: absolute;
  inset: 40% 0 0;
  background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.6));
  pointer-events: none;
}

.login__lateral-texto {
  position: absolute;
  left: 40px;
  bottom: 40px;
  right: 40px;
  z-index: 1;
  color: #fff;
}

.login__lateral-titulo {
  font-size: var(--fs-xl);
  font-weight: 600;
  letter-spacing: -0.02em;
}

.login__lateral-sub {
  margin-top: 4px;
  max-width: 34ch;
  color: rgba(255, 255, 255, 0.78);
  font-size: var(--fs-md);
}

@media (max-width: 900px) {
  .login { grid-template-columns: 1fr; }
  .login__lateral { display: none; }
}
</style>
