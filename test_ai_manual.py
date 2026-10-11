import asyncio

from finbot.llm.ollama_assistant import OllamaAssistant


async def main():

    ai = OllamaAssistant()

    question = "Хто написав Гаррі Поттера?"

    result = await ai.is_finance_topic(question)

    print("Фінансова тема:", result)

    transactions = [
        {"description": "Продукти", "amount": 1200},
        {"description": "Кафе", "amount": 600},
        {"description": "Казино", "amount": 800},
    ]

    if result:
        answer = await ai.answer(question, transactions)
        print("\nВідповідь ШІ:")
        print(answer)
    else:
        print(
            "Я не розрахован на такі питання, "
            "В МЕНЕ ХИТРЕ ЛИЦЕ"
        )


if __name__ == "__main__":
    asyncio.run(main())
