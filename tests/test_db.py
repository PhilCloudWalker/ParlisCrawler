import pytest
from Support.Database import Database
from ParlisCrawler.Website import Website
from ParlisCrawler.Crawler import CrawlerArticle

# --- Init -----------------------------#

@pytest.fixture(scope="module")
def db():
    print('--- DB Setup ----')
    db = Database()
    db.connect()
    yield db
    print('---- DB Close ----')
    db.close()

def test_upload(db):
    link3 = 'https://www.stvv.frankfurt.de/PARLISLINK/DDW?VORLAGEART=&NUMMER=&JAHR=2017&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und&?9749?7?'

    article_page = Website(link3, None)
    crawler_art = CrawlerArticle()
    article = crawler_art.parse(article_page)
    db.insert_article(article, "Crawler", "Articles")
    item = db.query_id("Crawler", "Articles", article.id)

    assert (item["id"] == "ST 2532")
