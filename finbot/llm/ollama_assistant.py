
from ollama import AsyncClient


class OllamaAssistant:

    def __init__(self):
        self.client = AsyncClient(
            host="http://127.0.0.1:11434"
        )
        self.model = "gemma3:1b"

    async def is_finance_topic(self, text: str) -> bool:
        response = await self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Визначте, чи стосується питання фінансів. "
                        "Відповідайте виключно YES або NO."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            options={"temperature": 0}
        )

        result = response.message.content.strip().upper()

        return result == "YES"

    async def answer(
        self,
        question: str,
        transactions: list
    ) -> str:

        system_prompt = """
        Ви — BankGuard AI, фінансовий помічник.

        Правила:
        1. Відповідайте тільки українською мовою.
        2. Завжди звертайтеся до користувача на "Ви".
        3. Не використовуйте емодзі.
        4. Аналізуйте витрати користувача.
        5. Оцінюйте раціональність витрат від 1 до 10.
        6. Пропонуйте способи економії.
        7. Попереджайте про витрати на азартні ігри.
        8. Не вважайте Spotify і Netflix автоматично
           небажаними підписками.
        9. Не вигадуйте транзакції.
        10. Не стверджуйте, що картку заблоковано.
        """

        response = await self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": (
                        f"Питання: {question}\n"
                        f"Транзакції: {transactions}"
                    )
                }
            ],
            options={"temperature": 0.2}
        )

        return response.message.content.strip()
