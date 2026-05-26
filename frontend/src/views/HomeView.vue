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
            <img src="@/assets/logo-vaca-ls.png" alt="Logo L.S" class="embedded-logo">
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
        <img src="@/assets/background_fazenda.jpeg" alt="Pecuária de Precisão" class="main-cover-image">
        
        <div class="floating-ia-card">
          <div class="ia-card-header">
            <span class="ia-spark">✨</span>
            <span class="ia-title">L.S. Assistente IA</span>
          </div>
          <p class="ia-sample-text">"A conversão alimentar do Lote Engorda A aumentou 12% após a introdução da nova ração lactação."</p>
          <div class="ia-status-dot-row">
            <span class="status-pulse"></span>
            <span class="status-label">Análise preditiva activa</span>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
// Configuração limpa e padronizada enviando perfis para a rota de autenticação comum
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@500;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* RESET E BASE DA HOME VUE */
.hero-wrapper {
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  background-color: #ffffff;
  font-family: 'Inter', sans-serif;
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
  background-color: #ffffff;
  position: relative;
  box-sizing: border-box;
}

.brand-header-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #f0fdf4;
  border: 1px solid #dcfce7;
  padding: 8px 16px;
  border-radius: 50px;
  width: max-content;
}

.badge-dot {
  width: 8px;
  height: 8px;
  background-color: #16a34a;
  border-radius: 50%;
}

.badge-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: #166534;
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
  font-family: 'Urbanist', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #64748b;
  letter-spacing: -0.5px;
}

.main-brand-title h1 {
  font-family: 'Urbanist', sans-serif;
  font-size: 3.5rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.1;
  margin: 0 0 16px 0;
  letter-spacing: -1.5px;
}

.brand-description {
  font-size: 1.1rem;
  color: #475569;
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
  border: 1px solid #e2e8f0;
}

.btn-admin-tech {
  background-color: #ffffff;
}

.btn-admin-tech:hover {
  border-color: #16a34a;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(22, 163, 74, 0.08);
}

.btn-operator-field {
  background-color: #f8fafc;
}

.btn-operator-field:hover {
  border-color: #16a34a;
  background-color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(22, 163, 74, 0.05);
}

.btn-icon {
  font-size: 1.8rem;
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.btn-admin-tech .btn-icon {
  color: #16a34a;
  background-color: #f0fdf4;
  border-color: #dcfce7;
}

.btn-operator-field .btn-icon {
  color: #16a34a;
  background-color: #f0fdf4;
  border-color: #dcfce7;
}

.btn-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.btn-text strong {
  font-size: 1.1rem;
  color: #0f172a;
  font-weight: 600;
}

.btn-text span {
  font-size: 0.85rem;
  color: #64748b;
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
  background-color: #0f172a;
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
  background: linear-gradient(to right, rgba(255,255,255,1) 0%, rgba(255,255,255,0.1) 20%, transparent 100%);
  z-index: 1;
}

/* CARD INTEGRADO DA IA (GLASSMORPHISM) */
.floating-ia-card {
  position: absolute;
  bottom: 60px;
  right: 60px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  padding: 24px;
  border-radius: 16px;
  max-width: 340px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  z-index: 2;
  animation: floatEffect 6s ease-in-out infinite;
}

@keyframes floatEffect {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.ia-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.ia-spark {
  font-size: 1.1rem;
  color: #8b5cf6;
}

.ia-title {
  font-weight: 700;
  font-size: 0.95rem;
  color: #7c3aed;
  font-family: 'Urbanist', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.ia-sample-text {
  font-size: 0.9rem;
  color: #334155;
  line-height: 1.5;
  margin: 0 0 14px 0;
  font-style: italic;
  font-weight: 500;
}

.ia-status-dot-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-pulse {
  width: 6px;
  height: 6px;
  background-color: #8b5cf6;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
}

.status-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
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