<template>
  <div class="register">
    <div class="register__coluna">
      <RouterLink to="/login" class="register__voltar">
        <AppIcon name="arrow-left" :size="14" />
        <span>Voltar para entrar</span>
      </RouterLink>

      <div class="register__caixa">
        <header class="register__topo">
          <img :src="logoImage" alt="" class="register__logo">
          <h1>Criar conta</h1>
          <p>Preencha seus dados para cadastrar seu acesso à plataforma.</p>
        </header>

        <form class="stack" novalidate @submit.prevent="handleRegister">
          <div class="field">
            <label class="field__label" for="cad-usuario">Login *</label>
            <input
              id="cad-usuario"
              v-model.trim="form.username"
              class="input"
              :class="{ 'input--error': fieldErrors.username }"
              type="text"
              autocomplete="username"
              placeholder="ex.: joao.campo"
              :aria-invalid="Boolean(fieldErrors.username)"
              required
            >
            <span v-if="fieldErrors.username" class="field__error" role="alert">{{ fieldErrors.username }}</span>
          </div>

          <div class="grid grid--2">
            <div class="field">
              <label class="field__label" for="cad-nome">Nome *</label>
              <input
                id="cad-nome"
                v-model.trim="form.first_name"
                class="input"
                :class="{ 'input--error': fieldErrors.first_name }"
                type="text"
                autocomplete="given-name"
                placeholder="João"
                required
              >
              <span v-if="fieldErrors.first_name" class="field__error" role="alert">{{ fieldErrors.first_name }}</span>
            </div>

            <div class="field">
              <label class="field__label" for="cad-sobrenome">Sobrenome</label>
              <input
                id="cad-sobrenome"
                v-model.trim="form.last_name"
                class="input"
                type="text"
                autocomplete="family-name"
                placeholder="da Silva"
              >
            </div>
          </div>

          <div class="field">
            <label class="field__label" for="cad-email">E-mail</label>
            <input
              id="cad-email"
              v-model.trim="form.email"
              class="input"
              :class="{ 'input--error': fieldErrors.email }"
              type="email"
              autocomplete="email"
              placeholder="joao@fazenda.com.br"
            >
            <span v-if="fieldErrors.email" class="field__error" role="alert">{{ fieldErrors.email }}</span>
          </div>

          <div class="field">
            <label class="field__label" for="cad-senha">Senha *</label>
            <div class="senha">
              <input
                id="cad-senha"
                v-model="form.password"
                class="input"
                :class="{ 'input--error': fieldErrors.password }"
                :type="mostrarSenha ? 'text' : 'password'"
                autocomplete="new-password"
                placeholder="Mínimo 8 caracteres"
                :aria-invalid="Boolean(fieldErrors.password)"
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
            <span v-if="fieldErrors.password" class="field__error" role="alert">{{ fieldErrors.password }}</span>
            <span v-else class="field__hint">Use pelo menos 8 caracteres, evitando senhas comuns ou apenas números.</span>
          </div>

          <div class="field">
            <label class="field__label" for="cad-confirmar-senha">Confirmar senha *</label>
            <input
              id="cad-confirmar-senha"
              v-model="confirmPassword"
              class="input"
              :class="{ 'input--error': fieldErrors.confirmPassword }"
              :type="mostrarSenha ? 'text' : 'password'"
              autocomplete="new-password"
              placeholder="Repita a senha"
              :aria-invalid="Boolean(fieldErrors.confirmPassword)"
              required
            >
            <span v-if="fieldErrors.confirmPassword" class="field__error" role="alert">{{ fieldErrors.confirmPassword }}</span>
          </div>

          <p v-if="errorMessage" class="alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ errorMessage }}</span>
          </p>

          <p v-if="successMessage" class="alert alert--ok" role="status">
            <AppIcon name="check-circle" :size="16" />
            <span>{{ successMessage }}</span>
          </p>

          <button type="submit" class="btn btn--primary btn--lg btn--block" :disabled="loading">
            <span v-if="loading" class="spinner" aria-hidden="true"></span>
            {{ loading ? 'Cadastrando...' : 'Criar conta' }}
          </button>
        </form>
      </div>

      <p class="register__rodape">
        Já possui uma conta?
        <RouterLink to="/login" class="register__link">Entrar</RouterLink>
      </p>
    </div>

    <aside class="register__lateral">
      <div class="register__lateral-texto">
        <p class="register__lateral-titulo">L.S Management</p>
        <p class="register__lateral-sub">Acompanhamento sanitário, produtivo, nutricional e reprodutivo do rebanho.</p>
      </div>
      <img :src="backgroundImage" alt="">
    </aside>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import authService from '@/services/authService';
import AppIcon from '@/components/ui/AppIcon.vue';
import { apiErrorMessage, apiFieldErrors } from '@/utils/apiError';
import logoImage from '@/assets/images/logo-vaca-ls.png';
import backgroundImage from '@/assets/images/background_fazenda.jpeg';

const router = useRouter();

const form = ref({
  username: '',
  first_name: '',
  last_name: '',
  email: '',
  password: '',
});
const confirmPassword = ref('');
const mostrarSenha = ref(false);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const fieldErrors = ref({});

function validar() {
  const errors = {};
  if (!form.value.username.trim()) errors.username = 'Informe um login de acesso.';
  if (!form.value.first_name.trim()) errors.first_name = 'Informe seu nome.';
  if (!form.value.password) errors.password = 'Informe uma senha.';
  else if (form.value.password.length < 8) errors.password = 'A senha deve ter pelo menos 8 caracteres.';
  if (form.value.password !== confirmPassword.value) {
    errors.confirmPassword = 'As senhas não coincidem.';
  }
  fieldErrors.value = errors;
  return Object.keys(errors).length === 0;
}

async function handleRegister() {
  if (loading.value) return;
  errorMessage.value = '';
  successMessage.value = '';
  if (!validar()) {
    errorMessage.value = 'Confira os campos destacados antes de continuar.';
    return;
  }

  loading.value = true;
  try {
    await authService.cadastrarContaPublica({
      username: form.value.username.trim(),
      first_name: form.value.first_name.trim(),
      last_name: form.value.last_name.trim(),
      email: form.value.email.trim(),
      password: form.value.password,
    });
    successMessage.value = 'Conta criada com sucesso! Redirecionando para o login...';
    const createdUsername = form.value.username.trim();
    setTimeout(() => {
      router.push({ path: '/login', query: { usuario: createdUsername } });
    }, 1200);
  } catch (error) {
    console.error('Erro ao cadastrar usuário:', error);
    fieldErrors.value = apiFieldErrors(error);
    errorMessage.value = apiErrorMessage(error, 'Não foi possível concluir o cadastro. Confira os dados informados.');
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.register {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 0.9fr);
  min-height: 100vh;
  background: var(--bg);
}

.register__coluna {
  display: grid;
  grid-template-rows: auto 1fr auto;
  justify-items: center;
  gap: 20px;
  padding: 28px 24px;
}

.register__voltar {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  justify-self: start;
  color: var(--text-3);
  font-size: var(--fs-sm);
  font-weight: 500;
  text-decoration: none;
}

.register__voltar:hover { color: var(--text); text-decoration: none; }

.register__caixa {
  align-self: center;
  width: 100%;
  max-width: 420px;
  animation: rise 520ms var(--ease-out) backwards;
}

.register__topo { margin-bottom: 22px; }

.register__logo {
  height: 36px;
  width: auto;
  margin-bottom: 16px;
  filter: invert(1);
}

:root[data-theme='dark'] .register__logo { filter: none; }

.register__topo h1 {
  font-size: var(--fs-2xl);
  font-weight: 600;
  letter-spacing: -0.02em;
}

.register__topo p {
  margin-top: 5px;
  color: var(--text-2);
}

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

.register__caixa .spinner {
  border-color: rgba(255, 255, 255, 0.35);
  border-top-color: currentColor;
}

.register__rodape {
  color: var(--text-3);
  font-size: var(--fs-sm);
  text-align: center;
}

.register__link {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
}

.register__link:hover { text-decoration: underline; }

.register__lateral {
  position: relative;
  overflow: hidden;
  border-left: 1px solid var(--line);
  background: var(--surface-3);
}

.register__lateral img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.6) saturate(0.85);
  animation: hero-zoom 16s ease-out forwards;
}

.register__lateral::after {
  content: '';
  position: absolute;
  inset: 40% 0 0;
  background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.6));
  pointer-events: none;
}

.register__lateral-texto {
  position: absolute;
  left: 40px;
  bottom: 40px;
  right: 40px;
  z-index: 1;
  color: #fff;
  animation: rise 700ms 160ms var(--ease-out) backwards;
}

.register__lateral-titulo {
  font-size: var(--fs-xl);
  font-weight: 600;
  letter-spacing: -0.02em;
}

.register__lateral-sub {
  margin-top: 4px;
  max-width: 34ch;
  color: rgba(255, 255, 255, 0.78);
  font-size: var(--fs-md);
}

@media (max-width: 900px) {
  .register { grid-template-columns: 1fr; }
  .register__lateral { display: none; }
}
</style>
