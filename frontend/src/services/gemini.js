import { GoogleGenerativeAI } from "@google/generative-ai";

// Colocando a chave diretamente no código para garantir o funcionamento imediato no Front
const apiKey = "AIzaSyAsSZ2ETkXtmQWXmreIsMZak_EA2P99VUg";
const genAI = new GoogleGenerativeAI(apiKey);

export const askGemini = async (prompt, farmContext = null) => {
  try {
    // Inicializa o modelo de IA mais rápido e otimizado para chat
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    
    let finalPrompt = prompt;
    if (farmContext) {
      finalPrompt = `Você é um assistente especialista em pecuária e gestão de fazendas chamado L.S IA. 
      Contexto atual da fazenda: ${farmContext}. 
      Responda de forma clara, curta, profissional e direta à seguinte pergunta do administrador: ${prompt}`;
    }

    const result = await model.generateContent(finalPrompt);
    const response = await result.response;
    return response.text();
  } catch (error) {
    console.error("Erro interno na chamada do Gemini:", error);
    throw new Error("Não foi possível conectar à Inteligência Artificial.");
  }
};