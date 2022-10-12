from bs4 import BeautifulSoup
from dataclasses import dataclass
from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonType
from meya.component.element import Component
from meya.element.field import element_field
from meya.element.field import response_field
from meya.entry import Entry
from meya.salesforce.knowledge.integration import (
    SalesforceKnowledgeIntegration,
)
from meya.salesforce.knowledge.integration import (
    SalesforceKnowledgeIntegrationRef,
)
from meya.salesforce.knowledge.payload.article import (
    SalesforceKnowledgeArticle,
)
from meya.tile.spec import TileElementSpec
from typing import List
from typing import Union


@dataclass
class SalesforceKnowledgeArticleDisplay(Component):
    @dataclass
    class Response:
        result: List[TileElementSpec] = response_field(sensitive=True)

    search_response: List[SalesforceKnowledgeArticle] = element_field(
        help=(
            "The response from the Salesforce Knowledge search API. "
            "This is usually available in flow scope, (@ flow.get('result')), "
            "after using the "
            "`meya.salesforce.knowledge.component.search.component`."
        )
    )

    locale: str = element_field(default="en-US")

    url_button_text: str = element_field(
        default="Read article",
        help=(
            "The text of the link button which is displayed with each "
            "article tile."
        ),
    )

    snippet_length: int = element_field(
        default=125,
        help="Length of the article snippet displayed in the tile body.",
    )

    button_type: ButtonType = element_field(
        default=ButtonType.URL, help="Tile button type"
    )

    integration: SalesforceKnowledgeIntegrationRef = element_field()

    async def start(self) -> List[Entry]:
        integration: SalesforceKnowledgeIntegration = await self.resolve(
            self.integration
        )
        tiles = []

        for article in self.search_response:
            tiles.append(
                TileElementSpec(
                    title=article.title,
                    description=self.snippet_format(
                        article.summary or article.body, self.snippet_length
                    ),
                    buttons=[
                        ButtonElementSpec(
                            text=self.url_button_text,
                            url=f"{integration.knowledge_base_url}/articles/Knowledge/{article.url_name}",
                            type=self.button_type,
                        )
                    ],
                )
            )

        return self.respond(data=self.Response(result=tiles))

    @staticmethod
    def snippet_format(
        description: str, snippet_length: int
    ) -> Union[str, None]:
        if not description:
            return

        description = BeautifulSoup(description, "html.parser").text
        return (
            (description[:snippet_length] + "...")
            if len(description) > snippet_length
            else description
        )
