<template>
  <div class="selecao">
    <div class="card selecao__caixa">
      <div class="card__body">
        <h1>Acessar o sistema</h1>
        <p>
          O painel é definido pelo perfil da sua conta. Entre com seu usuário
          e você cai na tela certa.
        </p>
        <RouterLink to="/login" class="btn btn--primary btn--lg btn--block">
          Ir para o login
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
.selecao {
  display: grid;
  place-items: center;
  min-height: 100vh;
  padding: 24px;
  background: var(--bg);
}

.selecao__caixa {
  width: 100%;
  max-width: 380px;
  text-align: center;
}

.selecao__caixa h1 {
  font-size: var(--fs-xl);
  font-weight: 600;
}

.selecao__caixa p {
  margin: 8px 0 22px;
  color: var(--text-2);
}

.selecao__caixa .btn { text-decoration: none; }
</style>
