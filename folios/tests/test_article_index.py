#!/usr/bin/env python3
# encoding: utf-8

import mock
import random
from datetime import datetime

from folios.core.settings import Settings
from folios.core.indexes import ArticlesIndex

user_sett = {
    "site": {
        "name": "Testing site"
        },
    'indexes': {
        'articles': {
            'page_size': 5,
            }
        },
    'log': {
        'file': {
            'enabled': False,
            }
        },
    }


class DummyArticle(object):
    def __init__(self, date):
        self.metadata = {'date': date}

test_articles = [
    DummyArticle(datetime.strptime("2015/01/01", "%Y/%m/%d")),
    DummyArticle(datetime.strptime("2015/01/02", "%Y/%m/%d")),
    DummyArticle(datetime.strptime("2015/01/03", "%Y/%m/%d")),
    DummyArticle(datetime.strptime("2015/01/04", "%Y/%m/%d")),
    DummyArticle(datetime.strptime("2015/01/05", "%Y/%m/%d")),
    DummyArticle(datetime.strptime("2015/01/06", "%Y/%m/%d")),
    DummyArticle(datetime.strptime("2015/01/07", "%Y/%m/%d")),
    DummyArticle(datetime.strptime("2015/01/08", "%Y/%m/%d")),
    DummyArticle(datetime.strptime("2015/01/09", "%Y/%m/%d")),
    DummyArticle(datetime.strptime("2015/01/10", "%Y/%m/%d")),
    DummyArticle(datetime.strptime("2015/01/11", "%Y/%m/%d")),
    DummyArticle(datetime.strptime("2015/01/12", "%Y/%m/%d")),
    ]

random.shuffle(test_articles)
sett = Settings(from_dict=user_sett)
for article in test_articles:
    ArticlesIndex.add(article)

def test_article_index_bootstrap():
    articles_index = ArticlesIndex(sett)

    day = 12
    for article in articles_index.__contents__:
        assert article.metadata['date'].day == day
        day -= 1

def test_article_index_pagination():
    articles_index = ArticlesIndex(sett)

    pages = articles_index.pages
    assert len(pages) == 3
    assert len(pages[0].contents) == 5
    assert len(pages[1].contents) == 5
    assert len(pages[2].contents) == 2

    assert pages[0].page_number == 1
    assert pages[1].page_number == 2
    assert pages[2].page_number == 3

    assert pages[0].next.page_number == 2
    assert pages[1].next.page_number == 3
    assert pages[2].next == None

    assert pages[0].previews == None
    assert pages[1].previews.page_number == 1
    assert pages[2].previews.page_number == 2

    day = 12
    for article in pages[0].contents:
        assert article.metadata['date'].day == day
        day -= 1

    for article in pages[1].contents:
        assert article.metadata['date'].day == day
        day -= 1

    for article in pages[2].contents:
        assert article.metadata['date'].day == day
        day -= 1
    assert day == 0


def test_article_index_url():
    articles_index = ArticlesIndex(sett)
    site_mock = mock.MagicMock()
    site_mock.theme.write.return_value = True
    articles_index.deploy(site_mock)
    pages = articles_index.pages

    assert pages[0].url == "/"
    assert pages[1].url == "page/2"
    assert pages[2].url == "page/3"

    assert pages[0].out_path == "/FAKE/output/index.html"
    assert pages[1].out_path == "/FAKE/output/page/2/index.html"
    assert pages[2].out_path == "/FAKE/output/page/3/index.html"


