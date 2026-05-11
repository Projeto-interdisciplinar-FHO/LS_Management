<template>
  <div class="login-wrapper">
    <div class="form-section">
      <div class="login-card">
        <h2 class="welcome-text">Bem-vindo de volta!</h2>
        <p class="subtitle">
          Entre com suas credenciais para acessar o painel.
        </p>

        <form @submit.prevent="handleLogin">
          <div class="input-container">
            <label>Usuário</label>
            <input 
              v-model="username" 
              type="text" 
              placeholder="Digite seu usuário..." 
              required
            >
          </div>

          <div class="input-container">
            <label>Senha</label>
            <input 
              v-model="password" 
              type="password" 
              placeholder="••••••••" 
              required
            >
          </div>

          <div class="form-options">
            <label class="remember-me">
              <input type="checkbox"> Lembrar acesso
            </label>
            <a href="#" class="forgot-link">Esqueceu a senha?</a>
          </div>

          <p v-if="errorMessage" class="error-msg">
            {{ errorMessage }}
          </p>

          <button type="submit" class="btn-login" :disabled="loading">
            {{ loading ? 'Autenticando...' : 'ENTRAR NO SISTEMA' }}
          </button>
        </form>

        <p class="footer-text">Não possui conta? <a href="#">Solicite acesso</a></p>
      </div>
    </div>

    <div class="branding-section">
      <div class="overlay"></div>
      <div class="brand-content">
        <img src="@/assets/logo-vaca-ls.png" class="brand-logo" alt="Logo L.S">
        <h1>L.S Management</h1>
        <div class="divider"></div>
        <p>Tecnologia e precisão no manejo pecuário.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const router = useRouter();

const username = ref('');
const password = ref('');
const loading = ref(false);
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

    // 1. Salva os tokens no navegador
    localStorage.setItem('access_token', response.data.access);
    if (response.data.refresh) {
      localStorage.setItem('refresh_token', response.data.refresh);
    }

    // 2. Lógica de Redirecionamento Dinâmico
    // O backend agora precisa retornar o campo 'is_superuser' ou 'role'
    const isSuperUser = response.data.is_superuser;
    const role = isSuperUser ? 'adm' : 'op';
    
    localStorage.setItem('user_role', role);

    // 3. Redireciona conforme o perfil
    if (role === 'adm') {
      console.log("Redirecionando Administrador...");
      router.push('/dashboard-adm');
    } else {
      console.log("Redirecionando Operador...");
      router.push('/dashboard-op');
    }

  } catch (error) {
    console.error("Erro no login:", error);
    if (error.response && error.response.status === 401) {
      errorMessage.value = "Usuário ou senha incorretos.";
    } else {
      errorMessage.value = "Erro ao conectar com o servidor.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-wrapper { display: flex; height: 100vh; width: 100vw; }
.form-section { flex: 1; background-color: #f8fafc; display: flex; align-items: center; justify-content: center; padding: 20px; }
.login-card { background: #ffffff; padding: 40px; border-radius: 12px; width: 100%; max-width: 400px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
.welcome-text { color: #051a05; margin-bottom: 8px; font-size: 1.8rem; }
.subtitle { color: #64748b; margin-bottom: 30px; font-size: 0.9rem; }
.input-container { margin-bottom: 20px; text-align: left; }
.input-container label { display: block; font-weight: bold; margin-bottom: 8px; color: #334155; font-size: 0.85rem; }
.input-container input { width: 100%; padding: 12px 16px; border-radius: 8px; border: 1px solid #e2e8f0; outline: none; }
.input-container input:focus { border-color: #46a350; }
.form-options { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; font-size: 0.85rem; }
.forgot-link { color: #46a350; text-decoration: none; font-weight: bold; }
.error-msg { color: #f85149; font-size: 0.85rem; margin-bottom: 15px; font-weight: bold; text-align: center; background: rgba(248, 81, 73, 0.1); padding: 10px; border-radius: 6px; }
.btn-login { width: 100%; padding: 14px; background-color: #46a350; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
.btn-login:hover:not(:disabled) { background-color: #357a3d; transform: translateY(-2px); }
.btn-login:disabled { background-color: #94a3b8; cursor: not-allowed; }
.footer-text { text-align: center; margin-top: 30px; font-size: 0.85rem; color: #64748b; }
.footer-text a { color: #46a350; font-weight: bold; text-decoration: none; }
.branding-section { flex: 1.2; background-color: #051a05; background-image: url('@/assets/background_fazenda.jpg'); background-size: cover; background-position: center; position: relative; display: flex; align-items: center; justify-content: center; }
.overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(5, 26, 5, 0.85); }
.brand-content { position: relative; z-index: 2; color: white; text-align: center; }
.brand-logo { width: 150px; margin-bottom: 20px; }
.brand-content h1 { font-size: 3rem; margin: 0; }
.divider { width: 60px; height: 4px; background: #46a350; margin: 20px auto; border-radius: 2px; }

@media (max-width: 900px) {
  .branding-section { display: none; }
}
</style>