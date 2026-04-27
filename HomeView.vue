<template>
  <div class="hero-container">
    <div class="overlay"></div>

    <div class="content">
      <header class="logo-box">
        <img src="@/assets/logo-vaca-ls.png" alt="Logo L.S" class="main-logo-hero">
        <div class="text-group">
          <h1>L.S Management</h1>
          <p>Cuidando do seu rebanho com inteligência</p>
        </div>
      </header>

      <main class="action-area">
        <router-link to="/selection" class="access-btn-minimal">
          ACESSAR SISTEMA
        </router-link>
      </main>
    </div>
  </div>
</template>

<style scoped>
.hero-container {
  position: relative;
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: url('@/assets/background_fazenda.png');
  background-size: cover;
  background-position: center;
  overflow: hidden;
}


.overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(255, 255, 255, 0.2); 
  z-index: 1;
}

.content {
  position: relative;
  z-index: 2;
  text-align: center;
}

.logo-box {
  display: flex;
  align-items: center;
  gap: 0px;
  margin-bottom: 50px;
}

.main-logo-hero {
  width: 270px;
  filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.1));
}

h1 {
  font-size: 5rem;
  margin: 5px 0;
  background: linear-gradient(to bottom, #051a05, #46a350);
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
}

.text-group p {
  color: #2c3e50; 
  font-size: 1.4rem;
  text-align: left;
  margin: 0;
  font-weight: 500;
}

.access-btn-minimal {
  display: inline-block;
  padding: 18px 80px;
  background-color: #46a350;
  color: #ffffff;
  text-decoration: none;
  border-radius: 50px;
  font-weight: bold;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(70, 163, 80, 0.3);
}

.access-btn-minimal:hover {
  transform: translateY(-3px);
  background-color: #051a05;
  box-shadow: 0 8px 25px rgba(5, 26, 5, 0.4);
}
</style>