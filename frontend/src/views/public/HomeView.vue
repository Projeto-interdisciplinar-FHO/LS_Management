<template>
  <div class="home">
    <section class="home__conteudo">
      <header class="home__marca">
        <img :src="logoImage" alt="" class="home__logo">
        <span>L.S Management</span>
      </header>

      <div class="home__miolo">
        <div class="home__texto">
          <h1>Gestão de rebanho, do curral ao relatório.</h1>
          <p>
            Cadastro dos animais, controle sanitário, lançamentos de pesagem,
            ordenha e alimentação — registrados no campo, consolidados na gestão.
          </p>
        </div>

        <ul class="home__capacidades">
          <li v-for="item in capacidades" :key="item.titulo">
            <span class="icon-tile icon-tile--accent"><AppIcon :name="item.icone" :size="17" /></span>
            <div>
              <strong>{{ item.titulo }}</strong>
              <span>{{ item.descricao }}</span>
            </div>
          </li>
        </ul>

        <div class="home__acoes">
          <RouterLink to="/login" class="btn btn--primary btn--lg">
            Entrar no sistema
            <AppIcon name="arrow-right" :size="16" />
          </RouterLink>
          <!-- O painel não é escolhido aqui: ele vem do perfil da conta. As
               duas portas que existiam antes levavam ao mesmo login. -->
          <p class="home__nota">
            O painel exibido depende do perfil da sua conta — administrador ou operador.
          </p>
        </div>
      </div>

      <footer class="home__rodape">© {{ ano }} L.S Management</footer>
    </section>

    <aside class="home__imagem">
      <img :src="backgroundImage" alt="Rebanho no pasto">
    </aside>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import logoImage from '@/assets/images/logo-vaca-ls.png';
import backgroundImage from '@/assets/images/background_fazenda.jpeg';

const ano = computed(() => new Date().getFullYear());

const capacidades = [
  { icone: 'animal', titulo: 'Rebanho', descricao: 'Ficha individual, espécie, raça e lotação por estábulo.' },
  { icone: 'syringe', titulo: 'Sanidade', descricao: 'Vacinação individual ou em lote, com controle de reforço.' },
  { icone: 'chart', titulo: 'Produção', descricao: 'Pesagem, ordenha e alimentação lançadas direto no campo.' },
];
</script>

<style scoped>
.home {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 0.85fr);
  min-height: 100vh;
  background: var(--bg);
}

/* O rodapé fica colado embaixo e o bloco central ocupa o resto: sem o
   `justify-content: center` brigando com o `margin-top: auto` do rodapé,
   que deixava um vão morto no meio da página. */
.home__conteudo {
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 36px;
  padding: 48px clamp(32px, 6vw, 88px);
  max-width: 720px;
}

.home__miolo {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 32px;
  min-width: 0;
}

.home__marca {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: var(--fs-md);
  font-weight: 600;
  letter-spacing: -0.01em;
}

/* A arte da marca é branca sobre transparente: no tema claro ela some.
   Invertida, o mesmo arquivo vira traço escuro sobre o fundo claro. */
.home__logo {
  height: 34px;
  width: auto;
  filter: invert(1);
}

:root[data-theme='dark'] .home__logo { filter: none; }

.home__texto h1 {
  font-size: clamp(1.9rem, 3.6vw, 2.75rem);
  font-weight: 600;
  line-height: 1.12;
  letter-spacing: -0.03em;
  text-wrap: balance;
}

.home__texto p {
  margin-top: 14px;
  max-width: 50ch;
  color: var(--text-2);
  font-size: var(--fs-lg);
  line-height: 1.6;
}

.home__capacidades {
  display: flex;
  flex-direction: column;
  gap: 14px;
  list-style: none;
  padding-top: 28px;
  border-top: 1px solid var(--line);
}

.home__capacidades li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.home__capacidades div {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.home__capacidades strong { font-size: var(--fs-md); font-weight: 600; }
.home__capacidades span { color: var(--text-2); font-size: var(--fs-sm); }

.home__acoes { display: flex; flex-direction: column; gap: 12px; align-items: flex-start; }

.home__acoes .btn { text-decoration: none; }

.home__nota {
  max-width: 46ch;
  color: var(--text-3);
  font-size: var(--fs-sm);
}

.home__rodape {
  padding-top: 8px;
  color: var(--text-3);
  font-size: var(--fs-xs);
}

.home__imagem {
  position: relative;
  overflow: hidden;
  border-left: 1px solid var(--line);
  background: var(--surface-3);
}

.home__imagem img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Sem lavagem de gradiente por cima da foto: ela é a foto, não um efeito. */
:root[data-theme='dark'] .home__imagem img { filter: brightness(0.82) saturate(0.9); }

@media (max-width: 900px) {
  .home { grid-template-columns: 1fr; }
  .home__imagem { display: none; }
  .home__conteudo { padding: 40px 24px 56px; gap: 28px; min-height: 100vh; }
}
</style>
