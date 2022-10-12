import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.salesforce.knowledge.component.display import (
    SalesforceKnowledgeArticleDisplay,
)
from meya.salesforce.knowledge.integration import (
    SalesforceKnowledgeIntegration,
)
from meya.salesforce.knowledge.integration import (
    SalesforceKnowledgeIntegrationRef,
)
from meya.salesforce.knowledge.payload.article import (
    SalesforceKnowledgeArticle,
)
from meya_private.salesforce.fixtures import salesforce_search_article_response


@pytest.mark.asyncio
async def test_salesforce_knowledge_display_component(
    salesforce_search_article_response,
):
    article = salesforce_search_article_response["articles"][0]
    integration = SalesforceKnowledgeIntegration(
        id="salesforce_integration",
        instance_base_url="",
        client_id="",
        client_secret="",
        username="",
        password="",
        knowledge_base_url="",
    )
    component = SalesforceKnowledgeArticleDisplay(
        integration=SalesforceKnowledgeIntegrationRef(integration.id),
        search_response=[SalesforceKnowledgeArticle.from_dict(article)],
    )
    component_start_entry = create_component_start_entry(component)
    flow_next_entry = create_flow_next_entry(
        component_start_entry,
        data=dict(
            result=[
                {
                    "title": "Meya BFML",
                    "description": "BFML is a proprietary language created by Meya that helps create highly advanced conversational AI. It's based on YAML and is...",
                    "image": None,
                    "rows": [],
                    "url": None,
                    "javascript": None,
                    "button_id": None,
                    "context": {},
                    "default": None,
                    "disabled": None,
                    "divider": None,
                    "icon": None,
                    "action": None,
                    "data": None,
                    "magic": None,
                    "type": None,
                    "menu": None,
                    "buttons": [
                        {
                            "url": "/articles/Knowledge/Meya-BFML",
                            "javascript": None,
                            "button_id": None,
                            "context": {},
                            "default": None,
                            "disabled": None,
                            "divider": None,
                            "icon": None,
                            "action": None,
                            "data": None,
                            "magic": None,
                            "type": "url",
                            "menu": None,
                            "text": "Read article",
                        }
                    ],
                }
            ]
        ),
    )

    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[flow_next_entry],
        extra_elements=[integration],
    )
