from bs4 import BeautifulSoup
from dataclasses import dataclass
from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonType
from meya.component.element import Component
from meya.element.field import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.tile.spec import TileElementSpec
from meya.zendesk.help_center.payload.article import ZendeskHelpCenterArticle
from meya.zendesk.help_center.payload.query import (
    ZendeskHelpCenterSearchResponse,
)
from typing import List
from typing import Union


@dataclass
class ZendeskHelpCenterArticlesDisplayComponent(Component):
    @dataclass
    class Response:
        result: List[TileElementSpec] = response_field(sensitive=True)

    search_response: Union[
        ZendeskHelpCenterSearchResponse, ZendeskHelpCenterArticle
    ] = element_field(
        help=(
            "The response from the Zendesk Help Center search API. "
            "This is usually available in flow scope, (@ flow.get('result')), "
            "after using the meya.zendesk.help_center.component.search or "
            "meya.zendesk.help_center.component.article.get component."
        )
    )

    url_button_text: str = element_field(
        default="Read article",
        help=(
            "The text of the link button which is displayed with each "
            "article tile."
        ),
    )

    snippet_length: int = element_field(
        default=125,
        help="Length of the article snippet displayed on the tile body",
    )

    button_type: ButtonType = element_field(
        default=ButtonType.URL, help="Tile button type"
    )

    async def start(self) -> List[Entry]:
        tiles = []
        if isinstance(self.search_response, ZendeskHelpCenterArticle):
            article = self.search_response
            tiles.append(
                self.create_tile(
                    article.title,
                    article.html_url,
                    self.snippet_format(article.body, self.snippet_length),
                    self.url_button_text,
                    self.button_type,
                )
            )
        else:
            for article in self.search_response.results:
                tiles.append(
                    self.create_tile(
                        article.title,
                        article.html_url,
                        self.snippet_format(
                            article.snippet, self.snippet_length
                        ),
                        self.url_button_text,
                        self.button_type,
                    )
                )

        return self.respond(data=self.Response(result=tiles))

    @staticmethod
    def create_tile(
        title: str,
        html_url: str,
        description: str,
        url_button_text: str,
        button_type: ButtonType,
    ) -> TileElementSpec:
        return TileElementSpec(
            title=title,
            description=description,
            buttons=[
                ButtonElementSpec(
                    text=url_button_text, url=html_url, type=button_type
                )
            ],
        )

    @staticmethod
    def snippet_format(description: str, snippet_length: int):
        description = BeautifulSoup(description, "html.parser").text
        return (
            (description[:snippet_length] + "...")
            if len(description) > snippet_length
            else description
        )
