"""
LocaleManager — loads a JSON translation file and provides t(key, **fmt).
Supported language codes: "ru", "en", "ky".
"""
import json
import os


class LocaleManager:
    # Endonyms: always shown in their own script (never translated)
    LANGS: dict[str, str] = {
        "ru": "Русский",
        "en": "English",
        "ky": "Кыргызча",
    }

    def __init__(self, default: str = "ru") -> None:
        self._strings: dict[str, str] = {}
        self._lang: str = default
        # locales/ lives one level above core/
        self._base = os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "locales")
        )
        self._load(default)

    # ──────────────────────────────────────────────────────────────
    def _load(self, lang: str) -> None:
        path = os.path.join(self._base, f"{lang}.json")
        with open(path, encoding="utf-8") as fh:
            self._strings = json.load(fh)
        self._lang = lang

    def set_lang(self, lang: str) -> None:
        """Switch language.  No-op if lang is not supported."""
        if lang in self.LANGS:
            self._load(lang)

    # ──────────────────────────────────────────────────────────────
    @property
    def current(self) -> str:
        return self._lang

    def t(self, key: str, **fmt) -> str:
        """
        Return the translated string for *key*.
        Optional keyword arguments are substituted via str.format(**fmt).
        Falls back to "[key]" if the key is missing.
        """
        val = self._strings.get(key, f"[{key}]")
        if fmt:
            try:
                val = val.format(**fmt)
            except (KeyError, ValueError, IndexError):
                pass
        return val

    # ──────────────────────────────────────────────────────────────
    def month_suffix(self, n: int) -> str:
        """
        Return the correct month word for *n* months.
        Handles Russian grammatical declension; other languages just use
        month_1 / month_2 / month_5 keys as needed.
        """
        mod10, mod100 = n % 10, n % 100
        if mod10 == 1 and mod100 != 11:
            return self.t("goals_month_1")
        if 2 <= mod10 <= 4 and not (12 <= mod100 <= 14):
            return self.t("goals_month_2")
        return self.t("goals_month_5")
