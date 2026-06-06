<template>
  <div class="hero-wrapper">
    <div class="hero-grid-container">
      
      <main class="brand-text-side">
        <div class="brand-header-badge">
          <span class="badge-dot"></span>
          <span class="badge-text">Plataforma Tecnológica Agro 4.0</span>
        </div>

        <header class="main-brand-title">
          <div class="logo-inline">
            <img :src="logoImage" alt="Logo L.S" class="embedded-logo">
            <span class="brand-subname">L.S. Management</span>
          </div>
          <h1>O cérebro da sua fazenda.</h1>
          <p class="brand-description">
            Centralize o controle do rebanho, otimize o manejo nutricional e monitore a produtividade em tempo real com inteligência artificial integrada.
          </p>
        </header>

        <div class="action-buttons-group">
          <router-link to="/login" class="btn-entry btn-admin-tech">
            <div class="btn-icon">⊞</div>
            <div class="btn-text">
              <strong>Painel Administrativo</strong>
              <span>Gestão técnica e relatórios</span>
            </div>
          </router-link>

          <router-link to="/login" class="btn-entry btn-operator-field">
            <div class="btn-icon">🌾</div>
            <div class="btn-text">
              <strong>Operador de Campo</strong>
              <span>Lançamentos rápidos e manejos</span>
            </div>
          </router-link>
        </div>

        <footer class="brand-footer-notice">
          <p>© 2026 L.S. Management. Inteligência que nutre o campo.</p>
        </footer>
      </main>

      <section class="visual-cover-side">
        <div class="cover-overlay-gradient"></div>
        <img :src="backgroundImage" alt="Pecuária de Precisão" class="main-cover-image">
        
      </section>

    </div>
  </div>
</template>

<script setup>
import logoImage from '../assets/logo-vaca-ls.png';
import backgroundImage from '../assets/background_fazenda.jpeg';

// Configuração limpa e padronizada enviando perfis para a rota de autenticação comum
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700;800&display=swap');

/* RESET E BASE DA HOME VUE */
.hero-wrapper {
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  background-color: #0b1220;
  font-family: 'Lexend', sans-serif;
  overflow: hidden;
  display: flex;
}

.hero-grid-container {
  display: grid;
  grid-template-columns: 55% 45%;
  width: 100%;
  height: 100%;
}

/* COLUNA DA ESQUERDA - TEXTO E ENTRADAS */
.brand-text-side {
  padding: 60px 80px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  background-color: #0b1220;
  position: relative;
  box-sizing: border-box;
}

.brand-header-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: rgba(15, 23, 42, 0.85);
  border: 1px solid #1f2937;
  padding: 8px 16px;
  border-radius: 50px;
  width: max-content;
}

.badge-dot {
  width: 8px;
  height: 8px;
  background-color: #22c55e;
  border-radius: 50%;
}

.badge-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: #d9f8e8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.main-brand-title {
  margin-top: 40px;
}

.logo-inline {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.embedded-logo {
  height: 40px;
  width: auto;
}

.brand-subname {
  font-family: 'Lexend', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #f8fafc;
  letter-spacing: -0.5px;
}

.main-brand-title h1 {
  font-family: 'Lexend', sans-serif;
  font-size: 3.5rem;
  font-weight: 800;
  color: #f8fafc;
  line-height: 1.1;
  margin: 0 0 16px 0;
  letter-spacing: -1.5px;
}

.brand-description {
  font-size: 1.1rem;
  color: #cbd5e1;
  line-height: 1.6;
  max-width: 520px;
  margin: 0;
  font-weight: 400;
}

/* BOTÕES ESTILO CARDS PROFISSIONAIS */
.action-buttons-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 32px;
  max-width: 520px;
}

.btn-entry {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #1f2937;
  background-color: #111827;
  color: #f8fafc;
}

.btn-admin-tech:hover,
.btn-operator-field:hover {
  border-color: #22c55e;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.18);
}

.btn-operator-field {
  background-color: #111827;
}

.btn-icon {
  font-size: 1.8rem;
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background-color: #0f1725;
  border: 1px solid #1f2937;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
  color: #22c55e;
}

.btn-admin-tech .btn-icon,
.btn-operator-field .btn-icon {
  color: #22c55e;
  background-color: #0f1725;
  border-color: #1f2937;
}

.btn-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.btn-text strong {
  font-size: 1.1rem;
  color: #f8fafc;
  font-weight: 600;
}

.btn-text span {
  font-size: 0.85rem;
  color: #94a3b8;
}

.brand-footer-notice p {
  font-size: 0.85rem;
  color: #94a3b8;
  margin: 0;
  font-weight: 500;
}

/* COLUNA DA DIREITA - COBERTURA VISUAL */
.visual-cover-side {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: transparent;
}

.main-cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
}

.cover-overlay-gradient {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, rgba(11,18,32,0.96) 0%, rgba(11,18,32,0.92) 10%, rgba(11,18,32,0.72) 25%, transparent 100%);
  z-index: 1;
}


/* RESPONSIVIDADE PARA TELAS MENORES */
@media (max-width: 1024px) {
  .hero-grid-container {
    grid-template-columns: 1fr;
  }
  .visual-cover-side {
    display: none;
  }
  .brand-text-side {
    padding: 40px;
  }
  .main-brand-title h1 {
    font-size: 2.8rem;
  }
}
</style>