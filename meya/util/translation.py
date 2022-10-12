import gettext as gettext_module

from meya.db.view.user import UserView
from typing import Dict


class MeyaTranslations(gettext_module.GNUTranslations):
    LOADED: Dict[str, gettext_module.NullTranslations] = {}

    @classmethod
    def load(cls, language: str) -> "MeyaTranslations":
        translations = cls.LOADED.get(language)
        if not translations:
            locale = language.replace("-", "_")
            translations = gettext_module.translation(
                "app",
                "translation",
                languages=[locale],
                class_=cls,
                fallback=True,
            )
            cls.LOADED[language] = translations
        return translations

    @classmethod
    def current(cls) -> "MeyaTranslations":
        user = UserView.current.get()
        # TODO Read default language from app config
        language = user.language or "en"
        translations = cls.load(language)
        return translations

    @classmethod
    def unload_all(cls) -> None:
        gettext_module._translations.clear()
        cls.LOADED.clear()


def gettext(message):
    """Return the localized translation of message, based on current user language."""
    return MeyaTranslations.current().gettext(message)


def gettext_noop(message):
    """Return the message as is, for later translation. Import this function as _ or gettext to trigger translation extraction."""
    return message


def ngettext(singular, plural, n):
    """Like gettext(), but consider plural forms."""
    return MeyaTranslations.current().ngettext(singular, plural, n)
