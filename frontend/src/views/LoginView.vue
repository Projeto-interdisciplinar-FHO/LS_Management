<template>
  <div class="login-wrapper">
    <div class="form-section">
      <div class="login-card">
        <h2 class="welcome-text">Bem-vindo de volta!</h2>
        <p class="subtitle">
          Fazendo login como: <strong>{{ userType.toUpperCase() }}</strong>
        </p>

        <!-- Formulário com validação local -->
        <form @submit.prevent="handleMockLogin">
          <div class="input-container">
            <label>Email</label>
            <input 
              v-model="email" 
              type="email" 
              placeholder="exemplo@ls.com" 
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

          <button type="submit" class="btn-login">ENTRAR NO SISTEMA</button>
        </form>

        <p class="footer-text">Não possui conta? <a href="#">Solicite acesso</a></p>
      </div>
    </div>

    <!-- Lado do Branding (Visual) -->
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
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const email = ref('');
const password = ref('');
const userType = ref(route.query.user || 'usuário');

const handleMockLogin = () => {
  if (email.value && password.value.length >= 4) {
    // 1. Pegamos o papel que foi definido na UserSelectionView
    const role = localStorage.getItem('user_role');

    // 2. Redirecionamento condicional baseado no papel[cite: 2]
    if (role === 'adm') {
      router.push('/dashboard-adm');
    } else if (role === 'op') {
      router.push('/dashboard-op');
    } else {
      // Caso algo dê errado, volta para seleção
      router.push('/selection');
    }
  } else {
    alert("Por favor, preencha as credenciais corretamente.");
  }
};
</script>

<style scoped>
/* Mantendo o seu design elegante */
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
.btn-login { width: 100%; padding: 14px; background-color: #46a350; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
.btn-login:hover { background-color: #357a3d; transform: translateY(-2px); }
.branding-section { flex: 1.2; background-color: #051a05; background-image: url('@/assets/background_fazenda.jpg'); background-size: cover; background-position: center; position: relative; display: flex; align-items: center; justify-content: center; }
.overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(5, 26, 5, 0.85); }
.brand-content { position: relative; z-index: 2; color: white; text-align: center; }
.brand-logo { width: 150px; margin-bottom: 20px; }
.brand-content h1 { font-size: 3rem; margin: 0; }
.divider { width: 60px; height: 4px; background: #46a350; margin: 20px auto; border-radius: 2px; }
</style>