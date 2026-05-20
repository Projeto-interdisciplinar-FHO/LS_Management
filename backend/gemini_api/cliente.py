import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

def gerar_alerta_nutricional(animal_name, alimento, periodicidade, peso_atual):
    if not client:
        return "Análise indisponível: Chave de API não configurada."

    prompt = (
        f"Atue como um zootecnista especialista em nutrição bovina. "
        f"Avalie o seguinte plano alimentar: O animal '{animal_name}', que atualmente pesa {peso_atual} kg, "
        f"receberá o alimento '{alimento}' com uma periodicidade de {periodicidade} vezes ao dia. "
        f"Forneça uma recomendação curta ou alerta nutricional sobre a adequação dessa dieta para o peso dele. "
        f"Seja direto e limite-se a no máximo 250 caracteres."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Não foi possível gerar o alerta nutricional: {str(e)}"