<template>
  <AppShell>
    <div class="page page--narrow chat-page">
      <PageHeader
        titulo="Assistente"
        descricao="Consultoria zootécnica sobre manejo, nutrição e sanidade do rebanho."
        voltar-rotulo="Painel"
        :voltar-para="painel"
      />

      <section class="card chat">
        <div ref="chatHistoryRef" class="chat__historico">
          <div v-if="messages.length === 0" class="empty">
            <AppIcon name="sparkle" :size="30" />
            <p class="empty__title">Como posso ajudar hoje?</p>
            <p class="empty__desc">
              Pergunte sobre manejo, nutrição ou sanidade — ou peça uma leitura dos dados do rebanho.
            </p>
            <div class="chat__sugestoes">
              <button
                v-for="sugestao in sugestoes"
                :key="sugestao"
                class="btn btn--sm"
                @click="sendSuggestion(sugestao)"
              >
                {{ sugestao }}
              </button>
            </div>
          </div>

          <div
            v-for="(msg, index) in messages"
            :key="index"
            class="mensagem"
            :class="msg.role === 'user' ? 'mensagem--pessoa' : 'mensagem--assistente'"
          >
            <span class="mensagem__autor">{{ msg.role === 'user' ? 'Você' : 'Assistente' }}</span>
            <div class="mensagem__balao" v-html="formatText(msg.text)"></div>
          </div>

          <div v-if="loading" class="mensagem mensagem--assistente">
            <span class="mensagem__autor">Assistente</span>
            <div class="mensagem__balao mensagem__digitando">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>

        <form class="chat__entrada" @submit.prevent="sendMessage">
          <input
            v-model="userInput"
            class="input"
            type="text"
            placeholder="Digite sua pergunta sobre manejo ou gestão..."
            aria-label="Sua pergunta"
            :disabled="loading"
            required
          >
          <button type="submit" class="btn btn--primary" :disabled="loading || !userInput.trim()">
            <AppIcon name="send" :size="15" />
            Enviar
          </button>
        </form>
      </section>
    </div>
  </AppShell>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue';
import { askGemini } from '@/services/gemini';
import api from '@/services/api';
import { painelDoPapel } from '@/services/auth';
import AppShell from '@/components/layout/AppShell.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import PageHeader from '@/components/layout/PageHeader.vue';

const painel = computed(() => painelDoPapel());

const userInput = ref('');
const messages = ref([]);
const loading = ref(false);
const chatHistoryRef = ref(null);

const sugestoes = [
  'Quais os primeiros sintomas da Febre Aftosa?',
  'Qual a lotação ideal de gado por hectare?',
  'Como montar um calendário de vacinação anual?',
];

// Função para enviar mensagem pré-pronta
const sendSuggestion = (text) => {
  userInput.value = text;
  sendMessage();
};

const sendMessage = async () => {
  if (!userInput.value.trim()) return;

  const question = userInput.value;
  // Adiciona a pergunta do usuário na tela
  messages.value.push({ role: 'user', text: question });
  userInput.value = '';
  loading.value = true;
  scrollToBottom();

  try {
    // Passamos quantos animais a fazenda tem para o modelo entender a escala
    // real da propriedade antes de responder.
    let farmContext = "";
    try {
      const animalsRes = await api.get('animals/');
      const totalAnimais = animalsRes.data.length || animalsRes.data.results?.length || 0;
      farmContext = `A fazenda atualmente possui ${totalAnimais} animais cadastrados no sistema.`;
    } catch (e) {
      // Se a API falhar, segue sem contexto extra
    }

    // Chama o arquivo gemini.js
    const aiResponse = await askGemini(question, farmContext);

    // Adiciona a resposta da IA na tela
    messages.value.push({ role: 'ai', text: aiResponse });
  } catch (error) {
    messages.value.push({ role: 'ai', text: "Desculpe, ocorreu um erro de conexão com o servidor da IA. Verifique sua chave de API no arquivo .env." });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};

// Formata texto com Markdown básico (negrito e quebras de linha) para HTML
const formatText = (text) => {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>');
};

// Rola o chat para baixo automaticamente
const scrollToBottom = () => {
  nextTick(() => {
    if (chatHistoryRef.value) {
      chatHistoryRef.value.scrollTop = chatHistoryRef.value.scrollHeight;
    }
  });
};
</script>

<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  height: calc(100vh - var(--header-h) - 190px);
  min-height: 420px;
}

.chat__historico {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.chat__sugestoes {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 8px;
}

.mensagem {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: 78%;
}

.mensagem--pessoa { align-self: flex-end; align-items: flex-end; }
.mensagem--assistente { align-self: flex-start; }

.mensagem__autor {
  color: var(--text-3);
  font-size: var(--fs-xs);
  font-weight: 500;
}

.mensagem__balao {
  padding: 10px 14px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--surface-2);
  line-height: 1.6;
}

.mensagem--pessoa .mensagem__balao {
  background: var(--accent-soft);
  border-color: var(--accent-line);
}

/* Três pontos em vez do texto "digitando": ocupa o mesmo lugar da resposta
   que está por vir, então a lista não pula quando ela chega. */
.mensagem__digitando {
  display: inline-flex;
  gap: 4px;
  align-items: center;
}

.mensagem__digitando span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--text-3);
  animation: pulsar 1.2s ease-in-out infinite;
}

.mensagem__digitando span:nth-child(2) { animation-delay: 0.15s; }
.mensagem__digitando span:nth-child(3) { animation-delay: 0.3s; }

@keyframes pulsar {
  0%, 60%, 100% { opacity: 0.25; }
  30% { opacity: 1; }
}

.chat__entrada {
  display: flex;
  gap: 8px;
  padding: 14px 20px;
  border-top: 1px solid var(--line);
}
</style>
