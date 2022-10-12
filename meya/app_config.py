from meya.util.context_var import ScopedContextVar
from meya.util.yaml import from_yaml
from pathlib import Path
from typing import ClassVar
from typing import Optional
from typing import cast


class AppConfig(dict):
    current: ClassVar = cast(ScopedContextVar["AppConfig"], ScopedContextVar())

    @property
    def package(self) -> Optional[str]:
        return self.get("package")

    @package.setter
    def package(self, package: str):
        self["package"] = package

    @property
    def package_path(self) -> Path:
        if self.package:
            return Path(self.package)
        else:
            return Path(".")

    @classmethod
    def from_path(cls, base_path: Path) -> "AppConfig":
        config_path = base_path / "config.yaml"
        if config_path.exists():
            with config_path.open("r") as config_file:
                config = from_yaml(config_file)
        else:
            config = {}
        return cls(config)
