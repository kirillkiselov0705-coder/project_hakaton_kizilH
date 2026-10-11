
from finbot.llm.risk_repository import RiskRepository


def test_repository():
    repository = RiskRepository()

    casino = repository.find_by_url(
        "https://cosmolot.ua"
    )

    assert casino is not None
    assert casino["category"] == "gambling"

    adult = repository.find_by_url(
        "https://www.pornhub.com/"
    )

    assert adult is not None
    assert adult["category"] == "adult"

    trusted = repository.find_by_url(
        "https://netflix.com"
    )

    assert trusted is not None
    assert trusted["category"] == "trusted"

    fake = repository.find_by_url(
        "https://notpornhub.com"
    )

    assert fake is None

    print("Усі перевірки SQLite пройдено успішно.")


if __name__ == "__main__":
    test_repository()
