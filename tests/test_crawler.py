import pytest, datetime
from ParlisCrawler.Website import Website
from ParlisCrawler.Crawler import CrawlerArticle, CrawlerOverview


# ---------- Overview ------------------#
def test_content_generator():
    url = r'https://www.stvv.frankfurt.de/PARLISLINK/SDF?VORLAGEART=&NUMMER=&JAHR=2019&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und'
    overview_page = Website(url, None)

    crawler = CrawlerOverview()
    overview = crawler.parse(overview_page)
    counter = 0
    urls = []
    for element in overview:
        if counter == 3:
            break
        counter += 1
        urls.append(element.link)
    assert (len(urls) == 3)

def test_content_components():
    url = r'https://www.stvv.frankfurt.de/PARLISLINK/SDF?VORLAGEART=&NUMMER=&JAHR=2017&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und'
    overview_page = Website(url, None)

    crawler = CrawlerOverview()
    overview = crawler.parse(overview_page)
    example = overview.__next__()

    assert (example.title == 'Ortsbezirk 6: Gleichbehandlung der Betreuungszeiten von Tagesmüttern')
    assert (example.link == 'https://www.stvv.frankfurt.de/PARLISLINK/DDW?VORLAGEART=&NUMMER=&JAHR=2017&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und&?9749?1?')

# ------- Article -------------------------#
def test_article_components_1():

    link = 'https://www.stvv.frankfurt.de/PARLISLINK/DDW?VORLAGEART=ST&NUMMER=479&JAHR=2019&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und&?1?1?'
    article_page = Website(link, None)
    crawler_art = CrawlerArticle()
    article = crawler_art.parse(article_page)

    #test
    assert (article.doc_type == 'Vorlage')
    assert (article.id == 'ST 479')
    assert (article.committee == 'Ortsbeirat 1')
    assert (article.date == "2019-02-22")
    assert (article.co_id == r'OF 1038/1')
    assert (article.co_link == 'https://www.stvv.frankfurt.de/PARLISLINK/DDW?W=DOK_NAME=%27OF_1038-1_2019%27')
    assert (article.city_area == 'Bockenheim;Europaviertel')

def test_article_components_2():

    link = 'https://www.stvv.frankfurt.de/PARLISLINK/DDW?VORLAGEART=&NUMMER=&JAHR=2017&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und&?9749?9745?'
    article_page = Website(link, None)
    crawler_art = CrawlerArticle()
    article = crawler_art.parse(article_page)

    #test
    assert (article.doc_type == 'Vorlage')
    assert (article.id == 'E 5')
    assert (article.committee == None)
    assert (article.date == "2017-04-26")
    assert (article.city_area == None)
    assert (article.party == 'CDU, SPD, GRÜNE')

    #TODO: to be adjusted
    #assert (article.co_id == 'OM 4005')
    #assert (article.co_link == 'https://www.stvv.frankfurt.de/PARLISLINK/DDW?W=DOK_NAME=%27OM_4005_2018%27')