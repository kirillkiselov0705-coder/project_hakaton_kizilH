
import sqlite3
from pathlib import Path
from urllib.parse import urlsplit


class RiskRepository:

    def __init__(self, db_path=None):
        if db_path is None:
            db_path = (
                Path(__file__).resolve().parents[2]
                / "data"
                / "risk_merchants.db"
            )

        self.db_path = Path(db_path)

        if not self.db_path.is_file():
            raise FileNotFoundError(
                f"Базу даних не знайдено: {self.db_path}"
            )

    def get_domain(self, url: str) -> str | None:
        url = url.strip()

        if not url:
            return None

        if "://" not in url:
            url = "https://" + url

        parsed = urlsplit(url)

        if parsed.scheme not in ("http", "https"):
            return None

        domain = parsed.hostname

        if not domain:
            return None

        return domain.lower().rstrip(".")

    def find_by_url(self, url: str) -> dict | None:
        domain = self.get_domain(url)

        if not domain:
            return None

        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row

            rows = connection.execute(
                """
                SELECT id, name, domain, category, risk_level
                FROM risk_merchants
                WHERE enabled = 1
                  AND domain IS NOT NULL
                """
            ).fetchall()

        for row in rows:
            saved_domain = row["domain"].lower().rstrip(".")

            if (
                domain == saved_domain
                or domain.endswith("." + saved_domain)
            ):
                return dict(row)

        return None
