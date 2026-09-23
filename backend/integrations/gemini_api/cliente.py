import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
class NutritionPromptBuilder:
    """Builder do prompt nutricional enviado ao provedor de IA."""

    def __init__(self):
        self._animal_name = None
        self._alimento = None
        self._periodicidade = None
        self._peso_atual = None

    def para_animal(self, animal_name):
        self._animal_name = animal_name
        return self

    def com_alimento(self, alimento):
        self._alimento = alimento
        return self

    def com_periodicidade(self, periodicidade):
        self._periodicidade = periodicidade
        return self

    def com_peso(self, peso_atual):
        self._peso_atual = peso_atual
        return self

    def build(self):
        return (
            "Atue como um zootecnista especialista em nutrição bovina. "
            f"Avalie o seguinte plano alimentar: O animal '{self._animal_name}', "
            f"que atualmente pesa {self._peso_atual} kg, receberá o alimento "
            f"'{self._alimento}' com uma periodicidade de "
            f"{self._periodicidade} vezes ao dia. "
            "Forneça uma recomendação curta ou alerta nutricional sobre a "
            "adequação dessa dieta para o peso dele. "
            "Seja direto e limite-se a no máximo 250 caracteres."
        )


class GeminiNutritionAdapter:
    """Adapta o cliente Gemini ao contrato de análise nutricional do sistema."""

    MODEL = "gemini-2.5-flash"

    def __init__(self, client=None):
        api_key = os.getenv("API_KEY")
        self.client = client or (genai.Client(api_key=api_key) if api_key else None)

    def gerar_alerta(self, animal_name, alimento, periodicidade, peso_atual):
        if not self.client:
            return "Análise indisponível: Chave de API não configurada."

        prompt = (
            NutritionPromptBuilder()
            .para_animal(animal_name)
            .com_alimento(alimento)
            .com_periodicidade(periodicidade)
            .com_peso(peso_atual)
            .build()
        )

        try:
            response = self.client.models.generate_content(
                model=self.MODEL,
                contents=prompt,
            )
            return response.text
        except Exception as error:
            return f"Não foi possível gerar o alerta nutricional: {error}"


_nutrition_adapter = GeminiNutritionAdapter()


def gerar_alerta_nutricional(animal_name, alimento, periodicidade, peso_atual):
    """Mantém o contrato usado pelos sinais e delega ao Adapter do Gemini."""
    return _nutrition_adapter.gerar_alerta(
        animal_name=animal_name,
        alimento=alimento,
        periodicidade=periodicidade,
        peso_atual=peso_atual,
    )