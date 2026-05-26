<template>
  <div class="page-wrapper">
    <header class="page-header">
      <button @click="$router.push('/dashboard-adm')" class="btn-back">← Voltar</button>
      <div class="header-content">
        <h1>✨ Assistente IA (Gemini)</h1>
        <p>Consultoria zootécnica e análise inteligente da sua fazenda.</p>
      </div>
    </header>

    <div class="chat-container">
      <div class="chat-history" ref="chatHistoryRef">
        <div v-if="messages.length === 0" class="empty-chat">
          <span class="ai-icon-large">✨</span>
          <h3>Como posso ajudar com a sua fazenda hoje?</h3>
          <p>Faça perguntas sobre manejo, nutrição, vacinas ou peça para eu analisar os dados do seu rebanho.</p>
          
          <div class="suggestions">
            <button @click="sendSuggestion('Quais os primeiros sintomas da Febre Aftosa?')" class="btn-suggestion">
              Quais os sintomas da Febre Aftosa?
            </button>
            <button @click="sendSuggestion('Qual a lotação ideal de gado por hectare?')" class="btn-suggestion">
              Lotação ideal por hectare?
            </button>
          </div>
        </div>

        <div 
          v-for="(msg, index) in messages" 
          :key="index" 
          class="message-bubble"
          :class="msg.role === 'user' ? 'message-user' : 'message-ai'"
        >
          <div class="bubble-avatar">{{ msg.role === 'user' ? '👤' : '✨' }}</div>
          <div class="bubble-content" v-html="formatText(msg.text)"></div>
        </div>

        <div v-if="loading" class="message-bubble message-ai typing-indicator">
          <div class="bubble-avatar">✨</div>
          <div class="bubble-content">
            <span class="dot"></span><span class="dot"></span><span class="dot"></span>
          </div>
        </div>
      </div>

      <form @submit.prevent="sendMessage" class="chat-input-area">
        <input 
          v-model="userInput" 
          type="text" 
          placeholder="Digite sua pergunta sobre manejo ou gestão..." 
          :disabled="loading"
          required
        >
        <button type="submit" class="btn-send" :disabled="loading || !userInput.trim()">
          Enviar ➔
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { askGemini } from '@/services/gemini';
import api from '@/services/api'; // Para podermos ler o banco de dados no futuro

const userInput = ref('');
const messages = ref([]);
const loading = ref(false);
const chatHistoryRef = ref(null);

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
    // Truque Avançado: Podemos buscar quantos animais a fazenda tem direto da API do Vue
    // e passar para o Gemini entender a realidade da fazenda!
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.page-wrapper { padding: 40px; background-color: #f8fafc; height: 100vh; font-family: 'Inter', sans-serif; color: #0f172a; display: flex; flex-direction: column; box-sizing: border-box; }
.page-header { margin-bottom: 24px; flex-shrink: 0; }
.btn-back { background: transparent; border: 1px solid #e2e8f0; color: #64748b; padding: 8px 16px; border-radius: 8px; cursor: pointer; margin-bottom: 16px; font-weight: 500; transition: 0.2s; }
.btn-back:hover { background: #f1f5f9; color: #0f172a; }
.header-content h1 { font-size: 2rem; font-weight: 700; margin-bottom: 8px; color: #8b5cf6; } /* Cor roxa para IA */
.header-content p { color: #64748b; }

/* CHAT CONTAINER */
.chat-container { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); display: flex; flex-direction: column; flex: 1; overflow: hidden; max-width: 1000px; }

/* CHAT HISTORY */
.chat-history { flex: 1; padding: 32px; overflow-y: auto; display: flex; flex-direction: column; gap: 24px; background: #f8fafc; }
.empty-chat { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; color: #64748b; }
.ai-icon-large { font-size: 4rem; margin-bottom: 16px; opacity: 0.8; }
.empty-chat h3 { color: #0f172a; font-size: 1.25rem; margin-bottom: 8px; }

.suggestions { display: flex; gap: 12px; margin-top: 24px; }
.btn-suggestion { background: #ffffff; border: 1px solid #e2e8f0; padding: 12px 20px; border-radius: 20px; color: #8b5cf6; font-weight: 600; cursor: pointer; transition: 0.2s; font-size: 0.9rem; }
.btn-suggestion:hover { border-color: #8b5cf6; background: #f5f3ff; }

/* BUBBLES */
.message-bubble { display: flex; gap: 16px; max-width: 85%; }
.message-user { align-self: flex-end; flex-direction: row-reverse; }
.message-ai { align-self: flex-start; }

.bubble-avatar { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0; }
.message-user .bubble-avatar { background: #e2e8f0; }
.message-ai .bubble-avatar { background: #f5f3ff; color: #8b5cf6; }

.bubble-content { padding: 16px 20px; border-radius: 12px; font-size: 1rem; line-height: 1.5; }
.message-user .bubble-content { background: #16a34a; color: #ffffff; border-top-right-radius: 0; }
.message-ai .bubble-content { background: #ffffff; border: 1px solid #e2e8f0; color: #0f172a; border-top-left-radius: 0; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }

/* LOADING DOTS */
.typing-indicator .bubble-content { display: flex; gap: 4px; align-items: center; padding: 20px; }
.dot { width: 8px; height: 8px; background: #8b5cf6; border-radius: 50%; animation: bounce 1.4s infinite ease-in-out; }
.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }

/* INPUT AREA */
.chat-input-area { padding: 20px 32px; background: #ffffff; border-top: 1px solid #e2e8f0; display: flex; gap: 16px; align-items: center; }
.chat-input-area input { flex: 1; padding: 16px 24px; border: 1px solid #cbd5e1; border-radius: 30px; font-size: 1rem; outline: none; transition: 0.2s; font-family: inherit; }
.chat-input-area input:focus { border-color: #8b5cf6; box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1); }
.btn-send { background: #8b5cf6; color: white; border: none; padding: 0 28px; height: 50px; border-radius: 25px; font-weight: 600; cursor: pointer; transition: 0.2s; font-size: 1rem; }
.btn-send:hover:not(:disabled) { background: #7c3aed; }
.btn-send:disabled { background: #cbd5e1; cursor: not-allowed; }
</style>