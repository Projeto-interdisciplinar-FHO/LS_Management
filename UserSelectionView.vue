<template>
  <div class="selection-wrapper">
    <div 
      class="select-section adm-side" 
      :class="{ active: selected === 'adm' }"
      @click="selected = 'adm'"
    >
      <div class="bg-photo adm-bg"></div>
      <div class="color-overlay"></div>
      <div class="content">
        <div class="avatar">
          <img src="@/assets/Adm_icon.jpg" alt="ADM">
        </div>
        <h2>ADM</h2>
        <div v-if="selected === 'adm'" class="reveal-text">
          <p>DASHBOARD COMPLETO E CONTROLE TOTAL DA PLATAFORMA.</p>
          <button class="confirm-btn" @click.stop="confirm('adm')">Confirmar Acesso</button>
        </div>
      </div>
    </div>

    <div 
      class="select-section op-side" 
      :class="{ active: selected === 'op' }"
      @click="selected = 'op'"
    >
      <div class="bg-photo op-bg"></div>
      <div class="color-overlay"></div>
      <div class="content">
        <div class="avatar">
          <img src="@/assets/Op_icon.jpg" alt="Operador">
        </div>
        <h2>OPERADOR</h2>
        <div v-if="selected === 'op'" class="reveal-text">
          <p>ACESSO SIMPLIFICADO E FOCO NO MANEJO DE CAMPO.</p>
          <button class="confirm-btn" @click.stop="confirm('op')">Confirmar Acesso</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const selected = ref(null);
const router = useRouter();

const confirm = (type) => {
  router.push({ name: 'login', query: { user: type } });
};
</script>

<style scoped>
.selection-wrapper {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #f0f0f0; /* Fundo neutro claro */
}

.select-section {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.active {
  flex: 1.8; /* Expansão mais suave */
}

/* IMAGENS SEMPRE VISÍVEIS */
.bg-photo {
  position: absolute;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  opacity: 0.7; /* Agora visível desde o início */
  transition: 0.8s;
  z-index: 1;
}

.adm-bg { background-image: url('@/assets/adm_background.jpg'); }
.op-bg { background-image: url('@/assets/op_background.jpg'); }

/* Ao selecionar, a foto ganha foco total */
.active .bg-photo {
  opacity: 1;
  filter: blur(4px); /* Desfoque menor para não sumir com a foto */
  transform: scale(1.05);
}

.color-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3); /* Overlay mais leve para mostrar a foto */
  z-index: 2;
  transition: 0.5s;
}

.active .color-overlay {
  background: rgba(0, 0, 0, 0.6); /* Escurece no clique para destacar o texto */
}

.content {
  position: relative;
  z-index: 3;
  text-align: center;
  color: white;
}

.avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid #46a350; /* Novo verde claro aplicado na borda */
  margin: 0 auto 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

h2 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #ffffff;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

/* BOTÃO COM A NOVA COR #46a350 */
.confirm-btn {
  margin-top: 20px;
  padding: 12px 40px;
  background: #46a350; /* Tom de verde solicitado */
  color: white;
  border: none;
  border-radius: 30px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s, background 0.3s;
}

.confirm-btn:hover {
  background: #357a3d;
  transform: scale(1.1);
}

.reveal-text p {
  font-weight: 500;
  max-width: 250px;
  margin: 0 auto;
}
</style>