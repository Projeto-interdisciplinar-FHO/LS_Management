# ls-management-vue

This template should help get you started developing with Vue 3 in Vite.

## Estrutura de pastas

```
src/
├── main.js, App.vue      ponto de entrada
├── router/               rotas e guarda de login/perfil
├── assets/
│   ├── images/           logos e fundos
│   └── styles/           tokens, base e componentes globais (index.css junta tudo)
├── components/
│   ├── layout/           moldura das telas (AppShell, PageHeader)
│   ├── ui/               peças genéricas (AppIcon, AppModal, ConfirmDialog)
│   ├── notifications/    toast, sino e banner de alertas
│   └── animals/          cartões, gráficos e badges da ficha do animal
├── services/             chamadas à API, sessão, tema, notificações
├── utils/                funções puras (situação do animal etc.)
└── views/                uma pasta por área do menu
    ├── public/           início, escolha de perfil, login
    ├── dashboards/       painel do administrador e do operador
    ├── herd/             animais, ficha, consulta, estábulos
    ├── handling/         pesagem, ordenha, alimentação, tarefas
    ├── health/           saúde, vacinação, veterinário
    ├── registry/         espécies, raças, vacinas, alimentos, usuários
    └── reports/          relatórios e assistente de IA
```

Imports usam o atalho `@/` (aponta para `src/`), assim mover um arquivo não quebra caminhos relativos.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```
