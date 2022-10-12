from meya.salesforce.knowledge.payload.article import (
    SalesforceKnowledgeArticleDetails,
)
from meya.salesforce.knowledge.payload.article import (
    SalesforceKnowledgeLayoutItems,
)


def test_article_details():
    assert SalesforceKnowledgeArticleDetails.from_dict(
        {
            "allViewCount": 2,
            "allViewScore": 100.00000000000001,
            "appDownVoteCount": 0,
            "appUpVoteCount": 0,
            "appViewCount": 2,
            "appViewScore": 100.00000000000001,
            "articleNumber": "000001003",
            "articleType": "Knowledge__kav",
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
            "createdBy": {
                "email": "amanie@meya.ai",
                "firstName": "Amanie",
                "id": "0051I000000QRyAQAW",
                "isActive": True,
                "lastName": "Ismail",
                "url": "/services/data/v51.0/chatter/users/0051I000000QRyAQAW",
                "userName": "amanie.dev@meya.ai",
            },
            "createdDate": "2021-04-16T13:20:33Z",
            "cspDownVoteCount": 0,
            "cspUpVoteCount": 0,
            "cspViewCount": 0,
            "cspViewScore": 0.0,
            "id": "kA01I000000ancBSAQ",
            "lastModifiedBy": {
                "email": "amanie@meya.ai",
                "firstName": "Amanie",
                "id": "0051I000000QRyAQAW",
                "isActive": True,
                "lastName": "Ismail",
                "url": "/services/data/v51.0/chatter/users/0051I000000QRyAQAW",
                "userName": "amanie.dev@meya.ai",
            },
            "lastModifiedDate": "2021-04-16T13:29:37Z",
            "lastPublishedDate": "2021-04-16T13:29:37Z",
            "layoutItems": [
                {
                    "label": "Title",
                    "name": "Title",
                    "type": "TEXT",
                    "value": "Meya BFML",
                },
                {
                    "label": "URL Name",
                    "name": "UrlName",
                    "type": "TEXT",
                    "value": "meya-bfml",
                },
                {
                    "label": "Question",
                    "name": "Question__c",
                    "type": "RICH_TEXT_AREA",
                    "value": None,
                },
                {
                    "label": "Answer",
                    "name": "Answer__c",
                    "type": "RICH_TEXT_AREA",
                    "value": '<p>BFML is a proprietary language created by Meya that helps create highly advanced conversational AI. It&#39;s based on YAML and is easy to learn and very powerful.</p>\n\n<ul><li>BFML is an acronym for <strong>B</strong>ot <strong>F</strong>low <strong>M</strong>arkup <strong>L</strong>anguage</li><li>BFML is to a conversational app as HTML is to a web app</li><li>Based on YAML</li></ul>\n\n<p>It looks like this...</p>\n\n<pre class="ckeditor_codeblock">\ntriggers:\n  - keyword: hi\n\nsteps:\n  - say: Hello!</pre>\n\n<p>Which produces this...</p>\n<img align="" alt="" height="auto" src="https://files.readme.io/47b25e3-hello-world.png" title="hello-world.png" width="80%"></img><img align="" alt="" height="auto" src="https://files.readme.io/47b25e3-hello-world.png" title="Click to close..." width="80%"></img>\n<p>Have a look at our <a href="https://github.com/meya-customers/demo-app" target="_blank" title="">demo-app source</a> (check out /flow folder) for lots of examples of BFML.</p>',
                },
                {
                    "label": "Article Created Date",
                    "name": "ArticleCreatedDate",
                    "type": "DATE_TIME",
                    "value": "2021-04-16T11:51:17Z",
                },
                {
                    "label": "Created By",
                    "name": "CreatedById",
                    "type": "LOOKUP",
                    "value": "0051I000000QRyAQAW",
                },
                {
                    "label": "Last Modified By",
                    "name": "LastModifiedById",
                    "type": "LOOKUP",
                    "value": "0051I000000QRyAQAW",
                },
                {
                    "label": "Last Published Date",
                    "name": "LastPublishedDate",
                    "type": "DATE_TIME",
                    "value": "2021-04-16T13:29:37Z",
                },
                {
                    "label": "Visible In Internal App",
                    "name": "IsVisibleInApp",
                    "type": "CHECKBOX",
                    "value": "true",
                },
                {
                    "label": "Visible to Customer",
                    "name": "IsVisibleInCsp",
                    "type": "CHECKBOX",
                    "value": "true",
                },
                {
                    "label": "Visible to Partner",
                    "name": "IsVisibleInPrm",
                    "type": "CHECKBOX",
                    "value": "true",
                },
                {
                    "label": "Visible In Public Knowledge Base",
                    "name": "IsVisibleInPkb",
                    "type": "CHECKBOX",
                    "value": "true",
                },
            ],
            "pkbDownVoteCount": 0,
            "pkbUpVoteCount": 0,
            "pkbViewCount": 0,
            "pkbViewScore": 0.0,
            "prmDownVoteCount": 0,
            "prmUpVoteCount": 0,
            "prmViewCount": 0,
            "prmViewScore": 0.0,
            "summary": "BFML is a proprietary language created by Meya that helps create highly advanced conversational AI. It's based on YAML and is easy to learn and very powerful.",
            "title": "Meya BFML",
            "url": "/services/data/v51.0/support/knowledgeArticles/kA01I000000ancBSAQ",
            "urlName": "meya-bfml",
            "versionNumber": 3,
        }
    ) == SalesforceKnowledgeArticleDetails(
        id="kA01I000000ancBSAQ",
        all_view_count=2,
        all_view_score=100.00000000000001,
        app_down_vote_count=0,
        app_up_vote_count=0,
        app_view_count=2,
        app_view_score=100.00000000000001,
        article_number="000001003",
        article_type="Knowledge__kav",
        category_groups=[
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
        created_by={
            "email": "amanie@meya.ai",
            "firstName": "Amanie",
            "id": "0051I000000QRyAQAW",
            "isActive": True,
            "lastName": "Ismail",
            "url": "/services/data/v51.0/chatter/users/0051I000000QRyAQAW",
            "userName": "amanie.dev@meya.ai",
        },
        created_date="2021-04-16T13:20:33Z",
        csp_down_vote_count=0,
        csp_up_vote_count=0,
        csp_view_count=0,
        csp_view_score=0.0,
        last_modified_by={
            "email": "amanie@meya.ai",
            "firstName": "Amanie",
            "id": "0051I000000QRyAQAW",
            "isActive": True,
            "lastName": "Ismail",
            "url": "/services/data/v51.0/chatter/users/0051I000000QRyAQAW",
            "userName": "amanie.dev@meya.ai",
        },
        last_modified_date="2021-04-16T13:29:37Z",
        last_published_date="2021-04-16T13:29:37Z",
        layout_items=[
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "Title",
                    "name": "Title",
                    "type": "TEXT",
                    "value": "Meya BFML",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "URL Name",
                    "name": "UrlName",
                    "type": "TEXT",
                    "value": "meya-bfml",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "Question",
                    "name": "Question__c",
                    "type": "RICH_TEXT_AREA",
                    "value": None,
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "Answer",
                    "name": "Answer__c",
                    "type": "RICH_TEXT_AREA",
                    "value": '<p>BFML is a proprietary language created by Meya that helps create highly advanced conversational AI. It&#39;s based on YAML and is easy to learn and very powerful.</p>\n\n<ul><li>BFML is an acronym for <strong>B</strong>ot <strong>F</strong>low <strong>M</strong>arkup <strong>L</strong>anguage</li><li>BFML is to a conversational app as HTML is to a web app</li><li>Based on YAML</li></ul>\n\n<p>It looks like this...</p>\n\n<pre class="ckeditor_codeblock">\ntriggers:\n  - keyword: hi\n\nsteps:\n  - say: Hello!</pre>\n\n<p>Which produces this...</p>\n<img align="" alt="" height="auto" src="https://files.readme.io/47b25e3-hello-world.png" title="hello-world.png" width="80%"></img><img align="" alt="" height="auto" src="https://files.readme.io/47b25e3-hello-world.png" title="Click to close..." width="80%"></img>\n<p>Have a look at our <a href="https://github.com/meya-customers/demo-app" target="_blank" title="">demo-app source</a> (check out /flow folder) for lots of examples of BFML.</p>',
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "Article Created Date",
                    "name": "ArticleCreatedDate",
                    "type": "DATE_TIME",
                    "value": "2021-04-16T11:51:17Z",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "Created By",
                    "name": "CreatedById",
                    "type": "LOOKUP",
                    "value": "0051I000000QRyAQAW",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "Last Modified By",
                    "name": "LastModifiedById",
                    "type": "LOOKUP",
                    "value": "0051I000000QRyAQAW",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "Last Published Date",
                    "name": "LastPublishedDate",
                    "type": "DATE_TIME",
                    "value": "2021-04-16T13:29:37Z",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "Visible In Internal App",
                    "name": "IsVisibleInApp",
                    "type": "CHECKBOX",
                    "value": "true",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "Visible to Customer",
                    "name": "IsVisibleInCsp",
                    "type": "CHECKBOX",
                    "value": "true",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "Visible to Partner",
                    "name": "IsVisibleInPrm",
                    "type": "CHECKBOX",
                    "value": "true",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "label": "Visible In Public Knowledge Base",
                    "name": "IsVisibleInPkb",
                    "type": "CHECKBOX",
                    "value": "true",
                }
            ),
        ],
        pkb_down_vote_count=0,
        pkb_up_vote_count=0,
        pkb_view_count=0,
        pkb_view_score=0.0,
        prm_down_vote_count=0,
        prm_up_vote_count=0,
        prm_view_count=0,
        prm_view_score=0.0,
        summary="BFML is a proprietary language created by Meya that helps create highly advanced conversational AI. It's based on YAML and is easy to learn and very powerful.",
        title="Meya BFML",
        url="/services/data/v51.0/support/knowledgeArticles/kA01I000000ancBSAQ",
        url_name="meya-bfml",
        version_number=3,
    )

    assert SalesforceKnowledgeArticleDetails.from_dict(
        {
            "id": "kA01I000000anbhSAA",
            "url": "/services/data/v51.0/support/knowledgeArticles/kA01I000000anbhSAA",
            "title": "Price calculator",
            "summary": None,
            "urlName": "price-calculator",
            "createdBy": {
                "id": "0051I000000QRyAQAW",
                "url": "/services/data/v51.0/chatter/users/0051I000000QRyAQAW",
                "email": "amanie@meya.ai",
                "isActive": None,
                "lastName": "Ismail",
                "userName": "amanie.dev@meya.ai",
                "firstName": "Amanie",
            },
            "articleType": "Knowledge__kav",
            "createdDate": "2021-04-15T19:13:08Z",
            "layoutItems": [
                {
                    "name": "Title",
                    "type": "TEXT",
                    "label": "Title",
                    "value": "Price calculator",
                },
                {
                    "name": "UrlName",
                    "type": "TEXT",
                    "label": "URL Name",
                    "value": "price-calculator",
                },
                {
                    "name": "Question__c",
                    "type": "RICH_TEXT_AREA",
                    "label": "Question",
                    "value": None,
                },
                {
                    "name": "Answer__c",
                    "type": "RICH_TEXT_AREA",
                    "label": "Answer",
                    "value": None,
                },
                {
                    "name": "ArticleCreatedDate",
                    "type": "DATE_TIME",
                    "label": "Article Created Date",
                    "value": "2021-04-15T19:08:53Z",
                },
                {
                    "name": "CreatedById",
                    "type": "LOOKUP",
                    "label": "Created By",
                    "value": "0051I000000QRyAQAW",
                },
                {
                    "name": "LastModifiedById",
                    "type": "LOOKUP",
                    "label": "Last Modified By",
                    "value": "0051I000000QRyAQAW",
                },
                {
                    "name": "LastPublishedDate",
                    "type": "DATE_TIME",
                    "label": "Last Published Date",
                    "value": "2021-04-15T19:13:25Z",
                },
                {
                    "name": "IsVisibleInApp",
                    "type": "CHECKBOX",
                    "label": "Visible In Internal App",
                    "value": "true",
                },
                {
                    "name": "IsVisibleInCsp",
                    "type": "CHECKBOX",
                    "label": "Visible to Customer",
                    "value": "true",
                },
                {
                    "name": "IsVisibleInPrm",
                    "type": "CHECKBOX",
                    "label": "Visible to Partner",
                    "value": "true",
                },
                {
                    "name": "IsVisibleInPkb",
                    "type": "CHECKBOX",
                    "label": "Visible In Public Knowledge Base",
                    "value": "true",
                },
            ],
            "allViewCount": 3,
            "allViewScore": 46.015746432281944,
            "appViewCount": 3,
            "appViewScore": 46.015746432281944,
            "cspViewCount": 0,
            "cspViewScore": 0,
            "pkbViewCount": 0,
            "pkbViewScore": 0,
            "prmViewCount": 0,
            "prmViewScore": 0,
            "articleNumber": "000001002",
            "versionNumber": 2,
            "appUpVoteCount": 0,
            "categoryGroups": [],
            "cspUpVoteCount": 0,
            "lastModifiedBy": {
                "id": "0051I000000QRyAQAW",
                "url": "/services/data/v51.0/chatter/users/0051I000000QRyAQAW",
                "email": "amanie@meya.ai",
                "isActive": True,
                "lastName": "Ismail",
                "userName": "amanie.dev@meya.ai",
                "firstName": "Amanie",
            },
            "pkbUpVoteCount": 0,
            "prmUpVoteCount": 0,
            "appDownVoteCount": 0,
            "cspDownVoteCount": 0,
            "lastModifiedDate": "2021-04-15T19:13:25Z",
            "pkbDownVoteCount": 0,
            "prmDownVoteCount": 0,
            "lastPublishedDate": "2021-04-15T19:13:25Z",
        }
    ) == SalesforceKnowledgeArticleDetails(
        id="kA01I000000anbhSAA",
        url="/services/data/v51.0/support/knowledgeArticles/kA01I000000anbhSAA",
        title="Price calculator",
        summary=None,
        url_name="price-calculator",
        created_by={
            "id": "0051I000000QRyAQAW",
            "url": "/services/data/v51.0/chatter/users/0051I000000QRyAQAW",
            "email": "amanie@meya.ai",
            "isActive": None,
            "lastName": "Ismail",
            "userName": "amanie.dev@meya.ai",
            "firstName": "Amanie",
        },
        article_type="Knowledge__kav",
        created_date="2021-04-15T19:13:08Z",
        layout_items=[
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "Title",
                    "type": "TEXT",
                    "label": "Title",
                    "value": "Price calculator",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "UrlName",
                    "type": "TEXT",
                    "label": "URL Name",
                    "value": "price-calculator",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "Question__c",
                    "type": "RICH_TEXT_AREA",
                    "label": "Question",
                    "value": None,
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "Answer__c",
                    "type": "RICH_TEXT_AREA",
                    "label": "Answer",
                    "value": None,
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "ArticleCreatedDate",
                    "type": "DATE_TIME",
                    "label": "Article Created Date",
                    "value": "2021-04-15T19:08:53Z",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "CreatedById",
                    "type": "LOOKUP",
                    "label": "Created By",
                    "value": "0051I000000QRyAQAW",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "LastModifiedById",
                    "type": "LOOKUP",
                    "label": "Last Modified By",
                    "value": "0051I000000QRyAQAW",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "LastPublishedDate",
                    "type": "DATE_TIME",
                    "label": "Last Published Date",
                    "value": "2021-04-15T19:13:25Z",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "IsVisibleInApp",
                    "type": "CHECKBOX",
                    "label": "Visible In Internal App",
                    "value": "true",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "IsVisibleInCsp",
                    "type": "CHECKBOX",
                    "label": "Visible to Customer",
                    "value": "true",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "IsVisibleInPrm",
                    "type": "CHECKBOX",
                    "label": "Visible to Partner",
                    "value": "true",
                }
            ),
            SalesforceKnowledgeLayoutItems.from_dict(
                {
                    "name": "IsVisibleInPkb",
                    "type": "CHECKBOX",
                    "label": "Visible In Public Knowledge Base",
                    "value": "true",
                }
            ),
        ],
        all_view_count=3,
        all_view_score=46.015746432281944,
        app_view_count=3,
        app_view_score=46.015746432281944,
        csp_view_count=0,
        csp_view_score=0,
        pkb_view_count=0,
        pkb_view_score=0,
        prm_view_count=0,
        prm_view_score=0,
        article_number="000001002",
        version_number=2,
        app_up_vote_count=0,
        category_groups=[],
        csp_up_vote_count=0,
        last_modified_by={
            "id": "0051I000000QRyAQAW",
            "url": "/services/data/v51.0/chatter/users/0051I000000QRyAQAW",
            "email": "amanie@meya.ai",
            "isActive": True,
            "lastName": "Ismail",
            "userName": "amanie.dev@meya.ai",
            "firstName": "Amanie",
        },
        pkb_up_vote_count=0,
        prm_up_vote_count=0,
        app_down_vote_count=0,
        csp_down_vote_count=0,
        last_modified_date="2021-04-15T19:13:25Z",
        pkb_down_vote_count=0,
        prm_down_vote_count=0,
        last_published_date="2021-04-15T19:13:25Z",
    )
