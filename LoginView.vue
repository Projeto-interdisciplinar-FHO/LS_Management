<script setup>
const handleLogin = async () => {
  // Add your login logic here
  console.log('Login attempt');
};
</script>

<template>
  <div class="login-wrapper">
    <div class="form-section">
      <div class="login-card">
        <h2 class="welcome-text">Bem-vindo de volta!</h2>
        <p class="subtitle">Acesse sua conta para gerenciar o rebanho.</p>

        <form @submit.prevent="handleLogin">
          <div class="input-container">
            <label>Email</label>
            <input type="email" placeholder="exemplo@ls.com" required>
          </div>

          <div class="input-container">
            <label>Senha</label>
            <input type="password" placeholder="••••••••" required>
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

<style scoped>
.login-wrapper {
  display: flex;
  height: 100vh;
  width: 100vw;
}

/* Lado do Formulário */
.form-section {
  flex: 1;
  background-color: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  background: #ffffff;
  padding: 44px;
  border-radius: 12px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 10px 35px rgba(70, 163, 80, 0.24), inset 0 0 0 2px rgba(70, 163, 80, 0.18);
}

.welcome-text { color: #051a05; margin-bottom: 8px; font-size: 1.8rem; }
.subtitle { color: #64748b; margin-bottom: 30px; font-size: 0.9rem; }

.input-container { margin-bottom: 20px; text-align: left; }
.input-container label { display: block; font-weight: bold; margin-bottom: 8px; color: #334155; font-size: 0.85rem; }
.input-container input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  outline: none;
  transition: border-color 0.3s;
}
.input-container input:focus { border-color: #46a350; }

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  font-size: 0.85rem;
}
.forgot-link { color: #46a350; text-decoration: none; font-weight: bold; }

.btn-login {
  width: 100%;
  padding: 14px;
  background-color: #46a350;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}
.btn-login:hover { background-color: #357a3d; }

/* Lado do Branding */
.branding-section {
  flex: 1.2;
  background-color: #051a05;
  background-image: url('@/assets/background_fazenda.jpg'); /* Reutilizando o fundo limpo */
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(5, 26, 5, 0.85);
}

.brand-content { position: relative; z-index: 2; color: white; text-align: center; }
.brand-logo { width: 150px; margin-bottom: 20px; }
.brand-content h1 { font-size: 3rem; margin: 0; }
.divider { width: 60px; height: 4px; background: #46a350; margin: 20px auto; border-radius: 2px; }
</style>