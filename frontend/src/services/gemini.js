import { GoogleGenerativeAI } from "@google/generative-ai";

// A chave vem do frontend/.env (fora do git). Ver .env.example.
const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
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