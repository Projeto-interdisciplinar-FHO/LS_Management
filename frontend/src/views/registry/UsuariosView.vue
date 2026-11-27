<template>
  <AppShell>
    <div class="page">
      <PageHeader
        titulo="Usuários"
        descricao="Quem acessa a plataforma e o que cada perfil pode fazer."
        voltar-rotulo="Painel"
        voltar-para="/dashboard-adm"
      >
        <template #acoes>
          <button type="button" class="btn btn--primary" @click="abrirNovo">
            <AppIcon name="plus" :size="16" />
            Cadastrar usuário
          </button>
        </template>
      </PageHeader>

      <p v-if="mensagem" class="alert alert--ok" role="status">
        <AppIcon name="check-circle" :size="16" />
        <span>{{ mensagem }}</span>
      </p>
      <p v-if="erro" class="alert alert--danger" role="alert">
        <AppIcon name="alert" :size="16" />
        <span>{{ erro }}</span>
      </p>

      <section v-if="usuarios.length > 0" class="registry-toolbar" aria-label="Buscar e filtrar usuários">
        <label class="search">
          <AppIcon name="search" :size="16" />
          <input
            v-model="busca"
            class="input"
            type="search"
            placeholder="Buscar por login, nome ou e-mail"
            aria-label="Buscar usuário"
          >
        </label>
        <select v-model="filtroPerfil" class="select usuarios__filtro" aria-label="Filtrar por perfil">
          <option value="">Todos os perfis</option>
          <option value="Administrador">Administrador</option>
          <option value="Operador">Operador</option>
        </select>
        <span class="registry-toolbar__count">{{ filtrados.length }} resultado(s)</span>
      </section>

      <RegistryCard
        titulo="Usuários cadastrados"
        descricao="O perfil define o que cada pessoa enxerga e pode fazer."
        :total="usuarios.length"
        :carregando="carregando"
        texto-carregando="Carregando usuários..."
        :vazio="usuarios.length === 0"
        :vazio-filtrado="usuarios.length > 0 && filtrados.length === 0"
        icone-vazio="users"
        titulo-vazio="Nenhum usuário cadastrado"
        descricao-vazia="Cadastre os operadores de campo e os administradores da fazenda."
        rotulo-acao-vazio="Cadastrar usuário"
        descricao-vazio-filtrado="Nenhum usuário corresponde aos filtros atuais."
        @cadastrar="abrirNovo"
        @limpar-filtros="limparFiltros"
      >
        <div class="table-wrap">
          <table class="table">
            <thead>
              <tr>
                <th>Usuário</th>
                <th>Nome e e-mail</th>
                <th>Perfil</th>
                <th>Situação</th>
                <th class="cell-actions">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="u in filtrados" :key="u.id" :class="{ 'is-muted': !u.is_active }">
                <td class="truncate" :title="u.username">
                  <div class="registry-item">
                    <span class="icon-tile" :class="u.papel === 'Administrador' ? 'icon-tile--accent' : ''">
                      <AppIcon :name="u.papel === 'Administrador' ? 'users' : 'worker'" :size="16" />
                    </span>
                    <span class="registry-item__name">{{ u.username }}</span>
                  </div>
                </td>
                <td class="text-muted truncate" :title="descricao(u)">{{ descricao(u) }}</td>
                <td>
                  <span class="badge" :class="u.papel === 'Administrador' ? 'badge--info' : ''">{{ u.papel }}</span>
                </td>
                <td>
                  <span class="badge" :class="u.is_active ? 'badge--ok' : 'badge--warn'">
                    <span class="badge__dot"></span>
                    {{ u.is_active ? 'Ativo' : 'Inativo' }}
                  </span>
                </td>
                <td class="cell-actions">
                  <div class="registry-actions">
                    <button
                      type="button"
                      class="btn btn--icon"
                      aria-label="Editar usuário"
                      title="Editar usuário"
                      @click="abrirEdicao(u)"
                    >
                      <AppIcon name="edit" :size="15" />
                    </button>
                    <button
                      type="button"
                      class="btn btn--sm"
                      :class="{ 'btn--danger': u.is_active }"
                      @click="alternarAtivo(u)"
                    >
                      {{ u.is_active ? 'Desativar' : 'Reativar' }}
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <template #rodape>
          <div class="nota">
            <AppIcon name="info" :size="15" />
            <span>
              Usuário não é excluído: desativar bloqueia o acesso e preserva o histórico
              de quem lançou cada pesagem e vacinação.
            </span>
          </div>
        </template>
      </RegistryCard>

      <AppModal
        v-if="modalAberto"
        :titulo="editando ? 'Editar usuário' : 'Cadastrar usuário'"
        @fechar="fechar"
      >
        <form id="form-usuario" class="stack" @submit.prevent="salvar">
          <div class="field">
            <label class="field__label" for="login">Login</label>
            <input
              id="login"
              v-model.trim="form.username"
              class="input"
              required
              :disabled="!!editando"
              placeholder="joao.campo"
              autocomplete="off"
            >
          </div>

          <div class="field">
            <label class="field__label" for="perfil">Perfil</label>
            <select id="perfil" v-model="form.papel" class="select" required>
              <option value="Operador">Operador</option>
              <option value="Administrador">Administrador</option>
            </select>
            <span class="field__hint">
              {{ form.papel === 'Administrador'
                ? 'Acesso total, incluindo cadastros e relatórios.'
                : 'Lança pesagem, ordenha, vacinação e alimentação no campo.' }}
            </span>
          </div>

          <div class="grid grid--2">
            <div class="field">
              <label class="field__label" for="primeiro-nome">Nome</label>
              <input id="primeiro-nome" v-model.trim="form.first_name" class="input" placeholder="João">
            </div>
            <div class="field">
              <label class="field__label" for="sobrenome">Sobrenome</label>
              <input id="sobrenome" v-model.trim="form.last_name" class="input" placeholder="da Silva">
            </div>
          </div>

          <div class="field">
            <label class="field__label" for="email">E-mail</label>
            <input id="email" v-model.trim="form.email" class="input" type="email" placeholder="joao@fazenda.com.br">
          </div>

          <div class="field">
            <label class="field__label" for="senha">{{ editando ? 'Nova senha' : 'Senha' }}</label>
            <input
              id="senha"
              v-model="form.password"
              class="input"
              type="password"
              :required="!editando"
              autocomplete="new-password"
              :placeholder="editando ? 'deixe vazio para manter a atual' : 'mínimo 8 caracteres'"
            >
            <span class="field__hint">Não pode ser só números nem uma senha comum.</span>
          </div>

          <p v-if="erroModal" class="alert alert--danger" role="alert">
            <AppIcon name="alert" :size="16" />
            <span>{{ erroModal }}</span>
          </p>
        </form>

        <template #rodape>
          <button type="button" class="btn" @click="fechar">Cancelar</button>
          <button type="submit" form="form-usuario" class="btn btn--primary" :disabled="salvando">
            {{ salvando ? 'Salvando...' : (editando ? 'Salvar alterações' : 'Cadastrar usuário') }}
          </button>
        </template>
      </AppModal>
    </div>
  </AppShell>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue';
import authService from '@/services/authService';
import { confirmar } from '@/services/confirmService';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppModal from '@/components/ui/AppModal.vue';
import PageHeader from '@/components/layout/PageHeader.vue';
import RegistryCard from '@/components/layout/RegistryCard.vue';

const usuarios = ref([]);
const busca = ref('');
const filtroPerfil = ref('');
const carregando = ref(true);
const salvando = ref(false);
const modalAberto = ref(false);
const editando = ref(null);
const mensagem = ref('');
const erro = ref('');
const erroModal = ref('');

const vazio = () => ({
  username: '',
  first_name: '',
  last_name: '',
  email: '',
  papel: 'Operador',
  password: '',
});

const form = reactive(vazio());

function descricao(u) {
  const nome = [u.first_name, u.last_name].filter(Boolean).join(' ');
  return [nome, u.email].filter(Boolean).join(' · ') || 'Sem nome ou e-mail informado';
}

const filtrados = computed(() => {
  const termo = busca.value.trim().toLowerCase();
  return usuarios.value.filter((u) => {
    if (filtroPerfil.value && u.papel !== filtroPerfil.value) return false;
    if (!termo) return true;
    return (
      String(u.username || '').toLowerCase().includes(termo)
      || String(u.first_name || '').toLowerCase().includes(termo)
      || String(u.last_name || '').toLowerCase().includes(termo)
      || String(u.email || '').toLowerCase().includes(termo)
    );
  });
});

function limparFiltros() {
  busca.value = '';
  filtroPerfil.value = '';
}

function avisar(texto, ehErro = false) {
  mensagem.value = ehErro ? '' : texto;
  erro.value = ehErro ? texto : '';
  setTimeout(() => {
    mensagem.value = '';
    erro.value = '';
  }, 6000);
}

function motivo(err, padrao) {
  const d = err.response?.data;
  if (!d) return padrao;
  if (typeof d === 'string') return d;
  const partes = Object.entries(d).map(
    ([campo, msgs]) => `${campo}: ${[].concat(msgs).join(' ')}`
  );
  return partes.join(' · ') || padrao;
}

async function carregar() {
  carregando.value = true;
  try {
    const { data } = await authService.listarUsuarios();
    usuarios.value = data;
  } catch (err) {
    avisar(motivo(err, 'Não foi possível carregar os usuários.'), true);
  } finally {
    carregando.value = false;
  }
}

function abrirNovo() {
  Object.assign(form, vazio());
  editando.value = null;
  erroModal.value = '';
  modalAberto.value = true;
}

function abrirEdicao(u) {
  Object.assign(form, {
    username: u.username,
    first_name: u.first_name,
    last_name: u.last_name,
    email: u.email,
    papel: u.papel,
    password: '',
  });
  editando.value = u.id;
  erroModal.value = '';
  modalAberto.value = true;
}

function fechar() {
  modalAberto.value = false;
  editando.value = null;
  erroModal.value = '';
}

async function salvar() {
  salvando.value = true;
  erroModal.value = '';
  try {
    const dados = { ...form };
    if (!dados.password) delete dados.password;
    if (editando.value) {
      await authService.atualizarUsuario(editando.value, dados);
      avisar('Usuário atualizado.');
    } else {
      await authService.cadastrarUsuario(dados);
      avisar(`Usuário ${dados.username} cadastrado.`);
    }
    fechar();
    await carregar();
  } catch (err) {
    erroModal.value = motivo(err, 'Não foi possível salvar.');
  } finally {
    salvando.value = false;
  }
}

async function alternarAtivo(u) {
  if (u.is_active) {
    const ok = await confirmar({
      titulo: `Desativar o usuário "${u.username}"?`,
      texto: 'O acesso será bloqueado, mas todo o histórico de lançamentos será preservado.',
      acao: 'Desativar usuário',
    });
    if (!ok) return;
  }
  try {
    await authService.definirAtivo(u.id, !u.is_active);
    avisar(u.username + (u.is_active ? ' desativado.' : ' reativado.'));
    await carregar();
  } catch (err) {
    avisar(motivo(err, 'Não foi possível alterar a situação.'), true);
  }
}

onMounted(carregar);
</script>

<style scoped>
.usuarios__filtro {
  width: auto;
  min-width: 170px;
  flex: none;
}

.nota {
  display: flex;
  width: 100%;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 9px;
  color: var(--text-3);
  font-size: var(--fs-sm);
  line-height: 1.5;
}

.nota svg { flex: none; margin-top: 2px; }
</style>
