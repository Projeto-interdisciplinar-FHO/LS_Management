<!--
  Casca da aplicação: barra fixa com marca, navegação por papel e conta.

  Antes só os dois painéis tinham navegação. Todas as outras telas abriam
  isoladas, com um "← Voltar" solto no topo — quem entrava em Pesagem tinha
  de voltar ao painel para ir a Ordenha. A navegação agora acompanha a
  pessoa em toda tela autenticada.

  O menu é montado a partir do papel guardado na sessão. Isso é conveniência
  de tela, não controle de acesso: quem autoriza é o backend, a cada
  requisição. Esconder um item não protege nada.
-->
<template>
  <div class="shell">
    <header class="bar">
      <RouterLink :to="painel" class="brand">
        <span class="brand__mark" aria-hidden="true">LS</span>
        <span class="brand__text">
          <span class="brand__name">L.S Management</span>
          <span class="brand__role">{{ ehAdmin ? 'Gestão' : 'Campo' }}</span>
        </span>
      </RouterLink>

      <nav class="nav" aria-label="Navegação principal">
        <template v-for="item in menu" :key="item.label">
          <RouterLink v-if="item.to" :to="item.to" class="nav__link">
            {{ item.label }}
          </RouterLink>

          <div v-else class="nav__group" @click.stop>
            <button
              class="nav__link nav__trigger"
              :class="{ 'is-open': aberto === item.label }"
              :aria-expanded="aberto === item.label"
              @click="alternar(item.label)"
            >
              {{ item.label }}
              <AppIcon name="chevron-down" :size="14" />
            </button>

            <div v-if="aberto === item.label" class="menu" role="menu">
              <RouterLink
                v-for="filho in item.children"
                :key="filho.to"
                :to="filho.to"
                class="menu__item"
                role="menuitem"
                @click="aberto = null"
              >
                <AppIcon :name="filho.icon" :size="16" />
                <span>{{ filho.label }}</span>
              </RouterLink>
            </div>
          </div>
        </template>
      </nav>

      <div class="bar__end">
        <button class="btn btn--icon" :title="rotuloTema" :aria-label="rotuloTema" @click="alternarTema">
          <AppIcon :name="tema === 'dark' ? 'sun' : 'moon'" :size="16" />
        </button>

        <div class="conta" @click.stop>
          <button class="conta__botao" :aria-expanded="contaAberta" @click="contaAberta = !contaAberta">
            <span class="conta__inicial" aria-hidden="true">{{ iniciais }}</span>
            <span class="conta__nome">{{ nomeExibido }}</span>
            <AppIcon name="chevron-down" :size="14" />
          </button>

          <div v-if="contaAberta" class="menu menu--right" role="menu">
            <div class="menu__cabecalho">
              <strong>{{ nomeExibido }}</strong>
              <span>{{ papelAtual || 'Sessão ativa' }}</span>
            </div>
            <button class="menu__item menu__item--acao" role="menuitem" @click="sair">
              <AppIcon name="logout" :size="16" />
              <span>Encerrar sessão</span>
            </button>
          </div>
        </div>

        <button
          class="btn btn--icon bar__hamburguer"
          :aria-label="gavetaAberta ? 'Fechar menu' : 'Abrir menu'"
          @click.stop="gavetaAberta = !gavetaAberta"
        >
          <AppIcon :name="gavetaAberta ? 'close' : 'menu'" :size="18" />
        </button>
      </div>
    </header>

    <!-- No celular a navegação vira uma gaveta plana: sem submenu para caçar. -->
    <div v-if="gavetaAberta" class="gaveta">
      <template v-for="item in menu" :key="`g-${item.label}`">
        <RouterLink v-if="item.to" :to="item.to" class="gaveta__link" @click="gavetaAberta = false">
          {{ item.label }}
        </RouterLink>
        <template v-else>
          <p class="gaveta__titulo">{{ item.label }}</p>
          <RouterLink
            v-for="filho in item.children"
            :key="`g-${filho.to}`"
            :to="filho.to"
            class="gaveta__link"
            @click="gavetaAberta = false"
          >
            <AppIcon :name="filho.icon" :size="16" />
            <span>{{ filho.label }}</span>
          </RouterLink>
        </template>
      </template>
    </div>

    <main>
      <slot />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref } from 'vue';
import { useRouter } from 'vue-router';
import AppIcon from '@/components/ui/AppIcon.vue';
import { ehAdministrador, limparSessao, nome, painelDoPapel, papel } from '@/services/auth';
import { temaAtual, alternarTema as trocarTema } from '@/services/theme';

const router = useRouter();

const aberto = ref(null);
const contaAberta = ref(false);
const gavetaAberta = ref(false);

const tema = temaAtual;
const rotuloTema = computed(() => (tema.value === 'dark' ? 'Usar tema claro' : 'Usar tema escuro'));
const alternarTema = () => trocarTema();

const ehAdmin = computed(() => ehAdministrador());
const painel = computed(() => painelDoPapel());
const papelAtual = computed(() => papel());
const nomeExibido = computed(() => nome() || (ehAdmin.value ? 'Administrador' : 'Operador'));

const iniciais = computed(() =>
  nomeExibido.value
    .split(/[\s.]+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((parte) => parte[0])
    .join('')
    .toUpperCase() || 'LS'
);

const MANEJO = [
  { to: '/pesagem', label: 'Pesagem', icon: 'scale' },
  { to: '/lancamento-leite', label: 'Ordenha', icon: 'milk' },
  { to: '/vacinacao', label: 'Vacinação', icon: 'syringe' },
  { to: '/lancamento-alimentacao', label: 'Alimentação', icon: 'feed' },
  { to: '/veterinario', label: 'Veterinário', icon: 'stethoscope' },
];

const menu = computed(() => {
  if (ehAdmin.value) {
    return [
      { to: '/dashboard-adm', label: 'Painel' },
      {
        label: 'Rebanho',
        children: [
          { to: '/animais', label: 'Animais', icon: 'animal' },
          { to: '/estabulos', label: 'Estábulos', icon: 'barn' },
          { to: '/saude', label: 'Saúde e vacinação', icon: 'stethoscope' },
        ],
      },
      { label: 'Manejo', children: MANEJO },
      {
        label: 'Cadastros',
        children: [
          { to: '/especies', label: 'Espécies', icon: 'dna' },
          { to: '/racas', label: 'Raças', icon: 'tag' },
          { to: '/vacinas', label: 'Vacinas', icon: 'syringe' },
          { to: '/dashboard-alimentacao', label: 'Alimentos', icon: 'feed' },
          { to: '/usuarios', label: 'Usuários', icon: 'users' },
        ],
      },
      { to: '/relatorios', label: 'Relatórios' },
    ];
  }

  return [
    { to: '/dashboard-op', label: 'Painel' },
    { label: 'Manejo', children: MANEJO },
    { to: '/rebanho', label: 'Rebanho' },
    { to: '/saude', label: 'Saúde' },
  ];
});

function alternar(rotulo) {
  aberto.value = aberto.value === rotulo ? null : rotulo;
  contaAberta.value = false;
}

function fecharTudo() {
  aberto.value = null;
  contaAberta.value = false;
  gavetaAberta.value = false;
}

function aoTeclar(evento) {
  if (evento.key === 'Escape') fecharTudo();
}

function sair() {
  limparSessao();
  router.push('/');
}

onMounted(() => {
  window.addEventListener('click', fecharTudo);
  window.addEventListener('keydown', aoTeclar);
});

onBeforeUnmount(() => {
  window.removeEventListener('click', fecharTudo);
  window.removeEventListener('keydown', aoTeclar);
});
</script>

<style scoped>
.shell {
  min-height: 100vh;
  background: var(--bg);
}

.bar {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 20px;
  height: var(--header-h);
  padding: 0 20px;
  background: var(--surface);
  border-bottom: 1px solid var(--line);
}

/* Marca */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: none;
  color: var(--text);
  text-decoration: none;
}

.brand:hover { text-decoration: none; }

.brand__mark {
  display: grid;
  place-items: center;
  width: 28px;
  height: 28px;
  border-radius: var(--r);
  background: var(--accent);
  color: #fff;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

:root[data-theme='dark'] .brand__mark { color: #0c1410; }

.brand__text { display: flex; flex-direction: column; line-height: 1.2; }

.brand__name {
  font-size: var(--fs-sm);
  font-weight: 600;
  letter-spacing: -0.01em;
}

.brand__role {
  color: var(--text-3);
  font-size: 10px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

/* Navegação */
.nav {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
  min-width: 0;
}

.nav__group { position: relative; }

.nav__link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  height: 30px;
  padding: 0 10px;
  border: 0;
  border-radius: var(--r);
  background: transparent;
  color: var(--text-2);
  font-family: inherit;
  font-size: var(--fs-md);
  font-weight: 500;
  white-space: nowrap;
  text-decoration: none;
  transition: background var(--dur) var(--ease), color var(--dur) var(--ease);
}

.nav__link:hover,
.nav__trigger.is-open {
  background: var(--surface-3);
  color: var(--text);
  text-decoration: none;
}

.nav__link.router-link-active { color: var(--text); }

.nav__trigger svg { color: var(--text-3); }

/* Menus suspensos */
.menu {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  z-index: 110;
  min-width: 216px;
  padding: 5px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  box-shadow: var(--shadow-md);
}

.menu--right { left: auto; right: 0; }

.menu__item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 7px 9px;
  border: 0;
  border-radius: var(--r);
  background: none;
  color: var(--text-2);
  font-family: inherit;
  font-size: var(--fs-md);
  text-align: left;
  text-decoration: none;
  transition: background var(--dur) var(--ease), color var(--dur) var(--ease);
}

.menu__item svg { color: var(--text-3); flex: none; }

.menu__item:hover,
.menu__item.router-link-active {
  background: var(--surface-3);
  color: var(--text);
  text-decoration: none;
}

.menu__item:hover svg,
.menu__item.router-link-active svg { color: var(--accent); }

.menu__item--acao:hover { color: var(--danger); }
.menu__item--acao:hover svg { color: var(--danger); }

.menu__cabecalho {
  display: flex;
  flex-direction: column;
  gap: 1px;
  padding: 8px 9px 10px;
  margin-bottom: 4px;
  border-bottom: 1px solid var(--line);
}

.menu__cabecalho strong { font-size: var(--fs-md); font-weight: 600; }
.menu__cabecalho span { color: var(--text-3); font-size: var(--fs-xs); }

/* Conta e controles à direita */
.bar__end {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: none;
}

.conta { position: relative; }

.conta__botao {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 32px;
  padding: 0 8px 0 5px;
  border: 1px solid transparent;
  border-radius: var(--r);
  background: transparent;
  color: var(--text);
  font-family: inherit;
  font-size: var(--fs-md);
  transition: background var(--dur) var(--ease);
}

.conta__botao:hover { background: var(--surface-3); }
.conta__botao svg { color: var(--text-3); }

.conta__inicial {
  display: grid;
  place-items: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--surface-3);
  border: 1px solid var(--line);
  color: var(--text-2);
  font-size: 10px;
  font-weight: 600;
}

.conta__nome {
  max-width: 130px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

.bar__hamburguer { display: none; }

/* Gaveta do celular */
.gaveta {
  position: sticky;
  top: var(--header-h);
  z-index: 99;
  display: none;
  flex-direction: column;
  gap: 1px;
  padding: 8px;
  background: var(--surface);
  border-bottom: 1px solid var(--line);
  box-shadow: var(--shadow-md);
  max-height: calc(100vh - var(--header-h));
  overflow-y: auto;
}

.gaveta__titulo {
  padding: 12px 10px 5px;
  color: var(--text-3);
  font-size: var(--fs-xs);
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.gaveta__link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: var(--r);
  color: var(--text-2);
  font-size: var(--fs-md);
  font-weight: 500;
  text-decoration: none;
}

.gaveta__link svg { color: var(--text-3); }
.gaveta__link:hover,
.gaveta__link.router-link-active { background: var(--surface-3); color: var(--text); text-decoration: none; }

@media (max-width: 940px) {
  .nav { display: none; }
  .conta__nome { display: none; }
  .bar__hamburguer { display: inline-flex; }
  .gaveta { display: flex; }
}
</style>
