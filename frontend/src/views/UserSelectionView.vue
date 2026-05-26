<template>
  <div class="user-selection-container">
    <div class="selection-content">
      <h1>Selecione seu Perfil</h1>
      <div class="button-group">
        <router-link to="/login" class="btn btn-admin">
          <span>Administrador</span>
        </router-link>
        <router-link to="/login" class="btn btn-operator">
          <span>Operador</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.user-selection-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #0d1117 0%, #1c2128 100%);
}

.selection-content {
  text-align: center;
  padding: 40px;
  border-radius: 12px;
  background: rgba(30, 35, 42, 0.8);
  border: 1px solid #30363d;
}

h1 {
  color: #e6edf3;
  margin-bottom: 40px;
  font-size: 28px;
}

.button-group {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.btn {
  padding: 15px 40px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  display: inline-block;
}

.btn-admin {
  background-color: #238636;
  color: #ffffff;
  border-color: #238636;
}

.btn-admin:hover {
  background-color: #2ea043;
  border-color: #3fb950;
  transform: translateY(-2px);
}

.btn-operator {
  background-color: #0969da;
  color: #ffffff;
  border-color: #0969da;
}

.btn-operator:hover {
  background-color: #0860ca;
  border-color: #54aeff;
  transform: translateY(-2px);
}
</style>
