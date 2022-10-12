from abc import ABC
from abc import abstractmethod
from colored import fg
from colored import stylize

palette = []


class Logger(ABC):
    @abstractmethod
    def log(self, icon: str, text: str):
        pass

    @abstractmethod
    def info(self, text: str):
        pass

    @abstractmethod
    def warn(self, text: str):
        pass

    @abstractmethod
    def error(self, text: str):
        pass

    @abstractmethod
    def success(self, text: str):
        pass

    @classmethod
    @abstractmethod
    def init(cls):
        pass

    @abstractmethod
    def stop(self):
        pass


class TextLogger(Logger):
    ICON_WIDTH = 5

    def log(self, icon: str, text: str):
        print(f"{icon}  {text}")

    def _icon(self, icon: str):
        return f"[{icon}]"

    def info(self, text: str):
        self.log(self._icon("i"), text)

    def warn(self, text: str):
        style = fg("yellow")
        icon = stylize(self._icon("w"), style)
        text = stylize(text, style)
        self.log(icon, text)

    def error(self, text: str):
        style = fg("red")
        icon = stylize(self._icon("e"), style)
        text = stylize(text, style)
        self.log(icon, text)

    def success(self, text: str):
        style = fg("green")
        icon = stylize(self._icon("✓"), style)
        text = stylize(text, style)
        self.log(icon, text)

    def stop(self):
        pass

    @classmethod
    def init(cls):
        pass


logger = TextLogger()
