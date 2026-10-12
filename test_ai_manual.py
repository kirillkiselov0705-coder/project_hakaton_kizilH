import asyncio

from finbot.llm.ollama_assistant import OllamaAssistant


async def main():

    ai = OllamaAssistant()

    question = "Проаналізуйте мої витрати за цей місяць"

    result = await ai.is_finance_topic(question)

    print("Фінансова тема:", result)

    
    transactions = [
        {
            "description": "АТБ",
            "amount": 1200,
            "category": "Продукти",
        },
        {
            "description": "Кав'ярня",
            "amount": 450,
            "category": "Кафе",
        },
        {
            "description": "Online Casino",
            "amount": 800,
            "category": "Розваги",
        },
        {
            "description": "Netflix",
            "amount": 300,
            "category": "Підписки",
        },
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
