<template>
  <AppShell>
    <div class="page page--narrow">
      <PageHeader
        titulo="Usuários"
        descricao="Quem acessa a plataforma e o que cada perfil pode fazer."
        voltar-rotulo="Painel"
        voltar-para="/dashboard-adm"
      >
        <template #acoes>
          <button class="btn btn--primary" @click="abrirNovo">
            <AppIcon name="plus" :size="16" />
            Adicionar usuário
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

      <section class="card">
        <header class="card__head">
          <div>
            <h2 class="card__title">Cadastrados</h2>
            <p class="card__desc">O perfil define o que cada pessoa enxerga e pode fazer.</p>
          </div>
          <span class="badge">{{ usuarios.length }}</span>
        </header>

        <div v-if="carregando" class="loading">
          <span class="spinner" aria-hidden="true"></span>
          Carregando usuários...
        </div>

        <div v-else-if="usuarios.length === 0" class="empty">
          <AppIcon name="users" :size="30" />
          <p class="empty__title">Nenhum usuário cadastrado</p>
          <p class="empty__desc">Cadastre os operadores de campo e os administradores da fazenda.</p>
          <button class="btn btn--primary" @click="abrirNovo">Adicionar usuário</button>
        </div>

        <div v-else class="list">
          <article
            v-for="u in usuarios"
            :key="u.id"
            class="list__item"
            :class="{ 'is-muted': !u.is_active }"
          >
            <div class="list__main">
              <span class="icon-tile" :class="u.papel === 'Administrador' ? 'icon-tile--accent' : ''">
                <AppIcon :name="u.papel === 'Administrador' ? 'users' : 'worker'" :size="16" />
              </span>
              <div>
                <span class="list__title">
                  {{ u.username }}
                  <span class="badge" :class="u.papel === 'Administrador' ? 'badge--info' : ''">{{ u.papel }}</span>
                  <span v-if="!u.is_active" class="badge badge--warn">inativo</span>
                </span>
                <span class="list__sub">{{ descricao(u) }}</span>
              </div>
            </div>

            <div class="row">
              <button class="btn btn--sm" @click="abrirEdicao(u)">Editar</button>
              <button class="btn btn--sm" :class="{ 'btn--danger': u.is_active }" @click="alternarAtivo(u)">
                {{ u.is_active ? 'Desativar' : 'Reativar' }}
              </button>
            </div>
          </article>
        </div>

        <footer class="card__foot nota">
          <AppIcon name="info" :size="15" />
          <span>
            Usuário não é excluído: desativar bloqueia o acesso e preserva o histórico
            de quem lançou cada pesagem e vacinação.
          </span>
        </footer>
      </section>

      <AppModal
        v-if="modalAberto"
        :titulo="editando ? 'Editar usuário' : 'Novo usuário'"
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
/*
 * Cadastro de usuarios — a tela que faltava.
 *
 * O `authService.js` ja chamava `users/register/`, mas a rota nunca existiu
 * no backend: havia um comentario dizendo "ajuste a URL conforme seu Django".
 * Na pratica so dava para criar gente rodando `manage.py createsuperuser` no
 * terminal do servidor.
 */
import { onMounted, reactive, ref } from 'vue'
import authService from '@/services/authService'
import AppShell from '@/components/layout/AppShell.vue'
import AppIcon from '@/components/ui/AppIcon.vue'
import AppModal from '@/components/ui/AppModal.vue'
import PageHeader from '@/components/layout/PageHeader.vue'

const usuarios = ref([])
const carregando = ref(true)
const salvando = ref(false)
const modalAberto = ref(false)
const editando = ref(null)
const mensagem = ref('')
const erro = ref('')
const erroModal = ref('')

const vazio = () => ({
  username: '',
  first_name: '',
  last_name: '',
  email: '',
  papel: 'Operador',
  password: '',
})

const form = reactive(vazio())

function descricao(u) {
  const nome = [u.first_name, u.last_name].filter(Boolean).join(' ')
  return [nome, u.email].filter(Boolean).join(' · ') || 'sem nome ou e-mail informado'
}

function avisar(texto, ehErro = false) {
  mensagem.value = ehErro ? '' : texto
  erro.value = ehErro ? texto : ''
  setTimeout(() => {
    mensagem.value = ''
    erro.value = ''
  }, 6000)
}

// O backend valida senha e login e devolve o motivo campo a campo. Mostrar
// isso e o que permite a pessoa corrigir sozinha — "erro ao salvar" obriga
// a chamar alguem.
function motivo(err, padrao) {
  const d = err.response?.data
  if (!d) return padrao
  if (typeof d === 'string') return d
  const partes = Object.entries(d).map(
    ([campo, msgs]) => campo + ': ' + [].concat(msgs).join(' ')
  )
  return partes.join(' · ') || padrao
}

async function carregar() {
  carregando.value = true
  try {
    const { data } = await authService.listarUsuarios()
    usuarios.value = data
  } catch (err) {
    avisar(motivo(err, 'Não foi possível carregar os usuários.'), true)
  } finally {
    carregando.value = false
  }
}

function abrirNovo() {
  Object.assign(form, vazio())
  editando.value = null
  erroModal.value = ''
  modalAberto.value = true
}

function abrirEdicao(u) {
  Object.assign(form, {
    username: u.username,
    first_name: u.first_name,
    last_name: u.last_name,
    email: u.email,
    papel: u.papel,
    password: '',
  })
  editando.value = u.id
  erroModal.value = ''
  modalAberto.value = true
}

function fechar() {
  modalAberto.value = false
  editando.value = null
  erroModal.value = ''
}

async function salvar() {
  salvando.value = true
  erroModal.value = ''
  try {
    const dados = { ...form }
    if (!dados.password) delete dados.password // editar sem trocar a senha
    if (editando.value) {
      await authService.atualizarUsuario(editando.value, dados)
      avisar('Usuário atualizado.')
    } else {
      await authService.cadastrarUsuario(dados)
      avisar('Usuário ' + dados.username + ' cadastrado.')
    }
    fechar()
    await carregar()
  } catch (err) {
    // Erro fica DENTRO do modal: o formulario continua preenchido e a pessoa
    // corrige o campo apontado sem digitar tudo de novo.
    erroModal.value = motivo(err, 'Não foi possível salvar.')
  } finally {
    salvando.value = false
  }
}

async function alternarAtivo(u) {
  try {
    await authService.definirAtivo(u.id, !u.is_active)
    avisar(u.username + (u.is_active ? ' desativado.' : ' reativado.'))
    await carregar()
  } catch (err) {
    avisar(motivo(err, 'Não foi possível alterar a situação.'), true)
  }
}

onMounted(carregar)
</script>

<style scoped>
.nota {
  align-items: flex-start;
  justify-content: flex-start;
  gap: 9px;
  color: var(--text-3);
  font-size: var(--fs-sm);
  line-height: 1.5;
}

.nota svg { flex: none; margin-top: 2px; }
</style>
