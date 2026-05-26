<template>
  <div class="login-wrapper">
    <div class="form-section">
      <div class="login-card">
        <h2 class="welcome-text">Acesso ao Sistema</h2>
        <p class="subtitle">
          Insira suas credenciais para gerenciar a fazenda.
        </p>

        <form @submit.prevent="handleLogin">
          <div class="input-container">
            <label>Usuário</label>
            <input 
              v-model="username" 
              type="text" 
              placeholder="Digite o seu usuário" 
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
            {{ loading ? 'Autenticando...' : 'ENTRAR' }}
          </button>
        </form>
      </div>
    </div>

    <div class="branding-section">
      <div class="brand-content">
        <img src="@/assets/logo-vaca-ls.png" class="brand-logo" alt="Logo L.S">
        <h1>L.S Management</h1>
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

    localStorage.setItem('access_token', response.data.access);
    if (response.data.refresh) {
      localStorage.setItem('refresh_token', response.data.refresh);
    }

    const isSuperUser = response.data.is_superuser;
    const role = isSuperUser === true ? 'adm' : 'op';
    
    localStorage.setItem('user_role', role);

    if (role === 'adm') {
      router.push('/dashboard-adm');
    } else {
      router.push('/dashboard-op');
    }

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
/* Importação da nova fonte profissional (Inter) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.login-wrapper { 
  display: flex; 
  height: 100vh; 
  width: 100vw; 
  font-family: 'Inter', sans-serif; /* Fonte aplicada globalmente aqui */
  background-color: #ffffff;
}

/* FORMULÁRIO (ESQUERDA) */
.form-section { 
  flex: 1; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  padding: 40px; 
  background-color: #ffffff; 
}

.login-card { 
  width: 100%; 
  max-width: 380px; 
}

.welcome-text { 
  color: #0f172a; 
  margin-bottom: 8px; 
  font-size: 2rem; 
  font-weight: 700;
  letter-spacing: -0.5px;
}

.subtitle { 
  color: #64748b; 
  margin-bottom: 40px; 
  font-size: 1rem; 
}

.input-container { margin-bottom: 24px; text-align: left; }
.input-container label { display: block; font-weight: 600; margin-bottom: 8px; color: #334155; font-size: 0.9rem; }
.input-container input { 
  width: 100%; 
  padding: 14px 16px; 
  border-radius: 8px; 
  border: 1px solid #cbd5e1; 
  outline: none; 
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  transition: all 0.2s;
  box-sizing: border-box;
}
.input-container input:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1); }

.form-options { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; font-size: 0.9rem; color: #475569; }
.remember-me { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.forgot-link { color: #16a34a; text-decoration: none; font-weight: 600; }
.forgot-link:hover { text-decoration: underline; }

.error-msg { color: #ef4444; font-size: 0.9rem; margin-bottom: 16px; font-weight: 500; text-align: center; background: #fef2f2; padding: 12px; border-radius: 8px; border: 1px solid #fecaca; }

.btn-login { 
  width: 100%; 
  padding: 16px; 
  background-color: #16a34a; 
  color: white; 
  border: none; 
  border-radius: 8px; 
  font-weight: 600; 
  font-size: 1rem;
  cursor: pointer; 
  transition: 0.2s; 
  font-family: 'Inter', sans-serif;
}
.btn-login:hover:not(:disabled) { background-color: #15803d; }
.btn-login:disabled { background-color: #94a3b8; cursor: not-allowed; }

/* BRANDING (DIREITA) - CLEAN FLAT DESIGN (Sem gradientes) */
.branding-section { 
  flex: 1.2; 
  background-color: #1f2937; /* Verde escuro */
  display: flex; 
  align-items: center; 
  justify-content: center; 
  border-left: 1px solid #e2e8f0;
}

.brand-content { 
  text-align: center; 
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.brand-logo { 
  width: 180px; 
  margin-bottom: 30px; 
  /* Sem filtros de drop-shadow pesados para manter o visual limpo */
}

.brand-content h1 { 
  font-size: 2.5rem; 
  margin: 0 0 16px 0; 
  color: #ffffff; /* Branco */
  font-weight: 800;
  letter-spacing: -1px;
}

.brand-content p {
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 500;
}

@media (max-width: 900px) {
  .branding-section { display: none; }
  .form-section { background-color: #f8fafc; }
  .login-card { background: white; padding: 40px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
}
</style>