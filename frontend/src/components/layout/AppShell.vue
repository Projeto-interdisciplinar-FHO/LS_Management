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
    <button
      v-if="gavetaAberta"
      type="button"
      class="sidebar__scrim"
      aria-label="Fechar menu"
      @click="gavetaAberta = false"
    />

    <aside class="sidebar" :class="{ 'sidebar--open': gavetaAberta }">
      <RouterLink :to="painel" class="brand" @click="gavetaAberta = false">
        <span class="brand__mark" aria-hidden="true">LS</span>
        <span class="brand__text">
          <span class="brand__name">L.S Management</span>
          <span class="brand__role">{{ ehAdmin ? 'Gestão' : 'Campo' }}</span>
        </span>
      </RouterLink>

      <nav class="sidebar__nav" aria-label="Navegação principal">
        <section v-for="secao in secoesMenu" :key="secao.label" class="sidebar__section">
          <p class="sidebar__section-title">{{ secao.label }}</p>
          <template v-for="item in secao.items" :key="item.label">
            <RouterLink
              v-if="item.to"
              :to="item.to"
              class="sidebar__link"
              @click="gavetaAberta = false"
            >
              <AppIcon :name="item.icon" :size="17" />
              <span>{{ item.label }}</span>
            </RouterLink>
            <div v-else class="sidebar__group" @click.stop>
              <button
                type="button"
                class="sidebar__link sidebar__trigger"
                :class="{ 'is-open': aberto === item.label }"
                :aria-expanded="aberto === item.label"
                @click="alternar(item.label)"
              >
                <AppIcon :name="item.icon" :size="17" />
                <span>{{ item.label }}</span>
                <AppIcon name="chevron-down" :size="14" class="sidebar__chevron" />
              </button>
              <div v-if="aberto === item.label" class="sidebar__children">
                <RouterLink
                  v-for="filho in item.children"
                  :key="filho.to"
                  :to="filho.to"
                  class="sidebar__link sidebar__link--child"
                  @click="gavetaAberta = false"
                >
                  <AppIcon :name="filho.icon" :size="16" />
                  <span>{{ filho.label }}</span>
                </RouterLink>
              </div>
            </div>
          </template>
        </section>
      </nav>

      <footer class="sidebar__footer">
        <div class="sidebar__profile">
          <span class="conta__inicial" aria-hidden="true">{{ iniciais }}</span>
          <span class="sidebar__profile-copy">
            <strong>{{ nomeExibido }}</strong>
            <small>{{ papelAtual || 'Sessão ativa' }}</small>
          </span>
          <button type="button" class="btn btn--icon" aria-label="Encerrar sessão" title="Encerrar sessão" @click="sair">
            <AppIcon name="logout" :size="15" />
          </button>
        </div>
        <button class="sidebar__theme" :title="rotuloTema" :aria-label="rotuloTema" @click="alternarTema">
          <AppIcon :name="tema === 'dark' ? 'sun' : 'moon'" :size="16" />
          <span>{{ tema === 'dark' ? 'Tema claro' : 'Tema escuro' }}</span>
        </button>
      </footer>
    </aside>

    <div class="shell__main">
      <header class="bar">
        <button
          class="btn btn--icon bar__hamburguer"
          :aria-label="gavetaAberta ? 'Fechar menu' : 'Abrir menu'"
          :aria-expanded="gavetaAberta"
          @click.stop="gavetaAberta = !gavetaAberta"
        >
          <AppIcon :name="gavetaAberta ? 'close' : 'menu'" :size="18" />
        </button>
        <div class="bar__context">
          <strong>{{ tituloPagina }}</strong>
          <span>Gestão integrada do rebanho</span>
        </div>
        <div v-if="mostrarExportacaoPainel" class="bar__actions">
          <div class="dashboard__action-menu" @click.stop>
            <button
              type="button"
              class="btn btn--primary"
              :aria-expanded="aberto === 'exportar'"
              @click="alternar('exportar')"
            >
              <AppIcon name="download" :size="15" />
              Exportar
              <AppIcon name="chevron-down" :size="14" />
            </button>
            <div v-if="aberto === 'exportar'" class="dashboard__action-popover dashboard__action-popover--right">
              <RouterLink to="/exportar-animais?tipo=animais" class="dashboard__action-option" @click="fecharTudo">
                <AppIcon name="animal" :size="16" /> Animais
              </RouterLink>
            </div>
          </div>
        </div>
      </header>
      <main>
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AppIcon from '@/components/ui/AppIcon.vue';
import { ehAdministrador, limparSessao, nome, painelDoPapel, papel } from '@/services/auth';
import { temaAtual, alternarTema as trocarTema } from '@/services/theme';

const router = useRouter();
const route = useRoute();

const aberto = ref(null);
const contaAberta = ref(false);
const gavetaAberta = ref(false);

const tema = temaAtual;
const rotuloTema = computed(() => (tema.value === 'dark' ? 'Usar tema claro' : 'Usar tema escuro'));
const alternarTema = () => trocarTema();

const ehAdmin = computed(() => ehAdministrador());
const mostrarExportacaoPainel = computed(() =>
  ehAdmin.value && ['dashboard-adm', 'dashboard-op'].includes(route.name)
);
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

const secaoRebanho = computed(() => [
  {
    to: ehAdmin.value ? '/animais' : '/rebanho',
    label: 'Lista de Animais',
    icon: 'herd',
  },
  { to: '/saude', label: 'Saúde & Vacinas', icon: 'syringe' },
  {
    label: 'Reprodução & IA',
    icon: 'dna',
    children: [
      { to: '/inseminacoes', label: 'Inseminações', icon: 'dna' },
      { to: '/nascimento-genealogia', label: 'Nascimentos & genealogia', icon: 'animal' },
    ],
  },
  { to: '/lancamento-leite', label: 'Ordenha (Produção)', icon: 'milk' },
  {
    label: 'Manejo',
    icon: 'move',
    children: [
      { to: '/manejo', label: 'Manejo rápido', icon: 'move' },
      { to: '/pesagem', label: 'Pesagem', icon: 'scale' },
      { to: '/desenvolvimento', label: 'Desenvolvimento', icon: 'chart' },
      { to: '/lancamento-alimentacao', label: 'Alimentação', icon: 'feed' },
      { to: '/veterinario', label: 'Veterinário', icon: 'stethoscope' },
    ],
  },
]);

const secoesMenu = computed(() => {
  const secoes = [
    {
      label: 'Visão geral',
      items: [{ to: painel.value, label: 'Painel Principal', icon: 'chart' }],
    },
    { label: 'Gestão de rebanho', items: secaoRebanho.value },
  ];

  if (ehAdmin.value) {
    secoes.push({
      label: 'Sistema',
      items: [
        { to: '/relatorios', label: 'Relatórios', icon: 'report' },
        {
          label: 'Cadastros',
          icon: 'clipboard',
          children: [
            { to: '/estabulos', label: 'Estábulos', icon: 'barn' },
            { to: '/racas', label: 'Raças', icon: 'tag' },
            { to: '/vacinas', label: 'Vacinas', icon: 'syringe' },
            { to: '/dashboard-alimentacao', label: 'Alimentos', icon: 'feed' },
            { to: '/usuarios', label: 'Usuários', icon: 'users' },
          ],
        },
      ],
    });
  }
  return secoes;
});

const titulosPagina = {
  'dashboard-adm': 'Painel Principal',
  'dashboard-op': 'Painel Principal',
  'animal-list': 'Lista de Animais',
  'animal-detail': 'Ficha do Animal',
  'inseminacoes': 'Inseminações',
  'nascimento-genealogia': 'Nascimentos & genealogia',
  'lancamento-leite': 'Ordenha (Produção)',
  'saude': 'Saúde & Vacinas',
  'manejo': 'Manejo',
  'pesagem': 'Pesagem',
  'desenvolvimento': 'Desenvolvimento',
  'relatorios': 'Relatórios',
};
const tituloPagina = computed(() => titulosPagina[route.name] || 'Gestão do Rebanho');

function alternar(rotulo) {
  aberto.value = aberto.value === rotulo ? null : rotulo;
}

function fecharTudo() {
  aberto.value = null;
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

.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 120;
  display: flex;
  width: 236px;
  flex-direction: column;
  background: var(--surface);
  border-right: 1px solid var(--line);
}

.sidebar > .brand {
  min-height: 72px;
  padding: 0 20px;
  border-bottom: 1px solid var(--line);
}

.sidebar__nav {
  flex: 1;
  overflow: auto;
  padding: 12px;
}

.sidebar__section { margin-bottom: 16px; }

.sidebar__section-title {
  padding: 8px 8px 6px;
  color: var(--text-3);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.sidebar__group { display: grid; }

.sidebar__link {
  display: flex;
  width: 100%;
  min-height: 40px;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border: 0;
  border-radius: var(--r-md);
  background: transparent;
  color: var(--text-2);
  font: inherit;
  font-size: var(--fs-sm);
  font-weight: 500;
  text-align: left;
  text-decoration: none;
  transition: background var(--dur) var(--ease), color var(--dur) var(--ease);
}

.sidebar__link > svg { flex: none; color: var(--text-3); }
.sidebar__link > span { min-width: 0; flex: 1; }
.sidebar__link:hover,
.sidebar__link.router-link-active,
.sidebar__trigger.is-open {
  background: var(--accent-soft);
  color: var(--accent);
  text-decoration: none;
}

.sidebar__link:hover > svg,
.sidebar__link.router-link-active > svg,
.sidebar__trigger.is-open > svg { color: var(--accent); }

.sidebar__trigger { cursor: pointer; }
.sidebar__chevron { transition: transform var(--dur) var(--ease); }
.sidebar__trigger.is-open .sidebar__chevron { transform: rotate(180deg); }
.sidebar__children { padding: 2px 0 4px 14px; }
.sidebar__link--child { min-height: 36px; font-size: var(--fs-xs); }

.sidebar__footer {
  display: grid;
  gap: 6px;
  padding: 12px;
  border-top: 1px solid var(--line);
}

.sidebar__profile {
  display: flex;
  min-width: 0;
  align-items: center;
  gap: 9px;
  padding: 4px;
}

.sidebar__profile-copy {
  display: grid;
  min-width: 0;
  flex: 1;
  gap: 1px;
}

.sidebar__profile-copy strong,
.sidebar__profile-copy small {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sidebar__profile-copy strong { font-size: var(--fs-sm); font-weight: 600; }
.sidebar__profile-copy small { color: var(--text-3); font-size: var(--fs-xs); }

.sidebar__theme {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 10px;
  border: 0;
  border-radius: var(--r);
  background: transparent;
  color: var(--text-2);
  font: inherit;
  font-size: var(--fs-sm);
  text-align: left;
}

.sidebar__theme:hover { background: var(--surface-3); color: var(--text); }

.shell__main {
  min-width: 0;
  min-height: 100vh;
  margin-left: 236px;
}

.bar {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 72px;
  padding: 10px 24px;
  background: var(--surface);
  border-bottom: 1px solid var(--line);
}

.bar__context { display: grid; min-width: 0; gap: 2px; }
.bar__context strong { font-size: var(--fs-lg); font-weight: 600; }
.bar__context span { color: var(--text-3); font-size: var(--fs-xs); }
.bar__actions { display: flex; align-items: center; gap: 8px; margin-left: auto; }
.bar__actions .dashboard__action-menu { position: relative; }
.bar__actions .dashboard__action-popover {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  z-index: 20;
  min-width: 180px;
  padding: 5px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface);
  box-shadow: var(--shadow-md);
}
.bar__actions .dashboard__action-popover--right { right: 0; left: auto; }
.bar__actions .dashboard__action-option {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 9px 10px;
  border-radius: var(--r);
  color: var(--text-2);
  font-size: var(--fs-sm);
  text-decoration: none;
}
.bar__actions .dashboard__action-option:hover {
  background: var(--surface-3);
  color: var(--text);
  text-decoration: none;
}
.bar__actions .dashboard__action-option svg { color: var(--accent); }
.bar__hamburguer { display: none; }
.sidebar__scrim { display: none; }

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
  overflow: visible;
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

@media (max-width: 940px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform var(--dur) var(--ease);
  }
  .sidebar--open { transform: translateX(0); }
  .sidebar__scrim {
    position: fixed;
    inset: 0;
    z-index: 119;
    display: block;
    border: 0;
    background: rgba(0, 0, 0, 0.35);
  }
  .shell__main { margin-left: 0; }
  .bar__hamburguer { display: inline-flex; }
}

@media (max-width: 560px) {
  .bar { min-height: 62px; gap: 10px; padding: 8px 12px; }
  .bar__context strong { font-size: var(--fs-md); }
  .bar__context span { display: none; }
  .bar__actions { gap: 5px; }
  .bar__actions .btn { min-height: 34px; padding-inline: 8px; font-size: var(--fs-xs); }
  .bar__actions .btn svg:last-child { display: none; }
}
</style>
