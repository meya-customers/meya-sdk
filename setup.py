from setuptools import find_namespace_packages
from setuptools import setup

setup(
    name="meya-sdk",
    packages=find_namespace_packages(),
    version="2.8.0",
    description="Meya SDK",
    url="https://meya.ai",
    author="Meya",
    author_email="support@meya.ai",
    entry_points={
        "babel.extractors": [
            "bfml = meya.core.template_registry:extract_translations",
            "meya_jinja2 = meya.core.template_registry:extract_jinja2_translations",
        ]
    },
    install_requires=[
        "aiohttp>=3.5.4,<4",
        "appdirs>=1.4.4,<2",
        "Babel>=2.9.1,<3",
        "beautifulsoup4>=4.8.2,<5",
        "black==22.6.0",
        "colored==1.3.93",
        "email-validator>=1.1.1,<2",
        "fire>=0.1.3,<0.2",
        "freezegun>=0.3.12,<0.4",
        "hachiko>=0.2.0,<0.3",
        "isort>=4.3.4,<5",
        "Jinja2==2.11.3",
        "luqum>=0.9.0,<0.10",
        "markdownify>=0.7.2,<0.8",
        "MarkupSafe>=1.1.1,<2",
        "msgpack>=0.6.0,<0.7",
        "pathspec>=0.9.0,<0.10",
        "PyJWT>=2.1.0,<3",
        "pytest-asyncio>=0.18.3,<0.19",
        "pytest-watch>=4.2.0,<5",
        "pytest>=7.1.2,<8",
        "python-dateutil>=2.7.5,<3",
        "pytz>=2019.1",
        "ruamel.yaml>=0.17.21,<0.18",
        "sgqlc>=10.1,<11",
        "watchdog>=0.10.2,<0.11",
        "Werkzeug>=1.0.0,<2",
        "yarl>=1.3.0,<2",
    ],
)
