from meya.salesforce.knowledge.payload.article import (
    SalesforceKnowledgeArticle,
)
from meya.salesforce.knowledge.payload.search import (
    SalesforceKnowledgeSearchResponse,
)


def test_search_response():
    assert SalesforceKnowledgeSearchResponse.from_dict(
        {
            "articles": [
                {
                    "articleNumber": "000001003",
                    "categoryGroups": [
                        {
                            "groupLabel": "Integration",
                            "groupName": "Integration",
                            "selectedCategories": [
                                {
                                    "categoryLabel": "All",
                                    "categoryName": "All",
                                    "url": "/services/data/v51.0/support/dataCategoryGroups/Integration/dataCategories/All?sObjectName=KnowledgeArticleVersion",
                                }
                            ],
                        }
                    ],
                    "downVoteCount": 0,
                    "id": "kA01I000000ancBSAQ",
                    "lastPublishedDate": "2021-04-16T11:53:27Z",
                    "summary": None,
                    "title": "Meya BFML",
                    "upVoteCount": 0,
                    "url": "/services/data/v51.0/support/knowledgeArticles/kA01I000000ancBSAQ",
                    "urlName": "meya-bfml",
                    "viewCount": 0,
                    "viewScore": 0.0,
                },
                {
                    "articleNumber": "000001002",
                    "categoryGroups": [],
                    "downVoteCount": 0,
                    "id": "kA01I000000anbhSAA",
                    "lastPublishedDate": "2021-04-15T19:13:25Z",
                    "summary": None,
                    "title": "Price calculator",
                    "upVoteCount": 0,
                    "url": "/services/data/v51.0/support/knowledgeArticles/kA01I000000anbhSAA",
                    "urlName": "price-calculator",
                    "viewCount": 1,
                    "viewScore": 100.0,
                },
            ],
            "pageNumber": 1,
            "nextPageUrl": None,
            "currentPageUrl": "/services/data/v51.0/support/knowledgeArticles?q=WHERE+title+like+%27Price%27",
        }
    ) == SalesforceKnowledgeSearchResponse(
        articles=[
            SalesforceKnowledgeArticle.from_dict(
                {
                    "articleNumber": "000001003",
                    "categoryGroups": [
                        {
                            "groupLabel": "Integration",
                            "groupName": "Integration",
                            "selectedCategories": [
                                {
                                    "categoryLabel": "All",
                                    "categoryName": "All",
                                    "url": "/services/data/v51.0/support/dataCategoryGroups/Integration/dataCategories/All?sObjectName=KnowledgeArticleVersion",
                                }
                            ],
                        }
                    ],
                    "downVoteCount": 0,
                    "id": "kA01I000000ancBSAQ",
                    "lastPublishedDate": "2021-04-16T11:53:27Z",
                    "summary": None,
                    "title": "Meya BFML",
                    "upVoteCount": 0,
                    "url": "/services/data/v51.0/support/knowledgeArticles/kA01I000000ancBSAQ",
                    "urlName": "meya-bfml",
                    "viewCount": 0,
                    "viewScore": 0.0,
                }
            ),
            SalesforceKnowledgeArticle.from_dict(
                {
                    "articleNumber": "000001002",
                    "categoryGroups": [],
                    "downVoteCount": 0,
                    "id": "kA01I000000anbhSAA",
                    "lastPublishedDate": "2021-04-15T19:13:25Z",
                    "summary": None,
                    "title": "Price calculator",
                    "upVoteCount": 0,
                    "url": "/services/data/v51.0/support/knowledgeArticles/kA01I000000anbhSAA",
                    "urlName": "price-calculator",
                    "viewCount": 1,
                    "viewScore": 100.0,
                }
            ),
        ],
        page_number=1,
        next_page_url=None,
        current_page_url="/services/data/v51.0/support/knowledgeArticles?q=WHERE+title+like+%27Price%27",
    )
