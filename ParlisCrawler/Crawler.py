import requests, time
from bs4 import  BeautifulSoup
from urllib.parse import urljoin
import datetime

from ParlisCrawler.Content import ContentOverview, ContentArticle
from unicodedata import normalize
import re

class Crawler:

    def getPage(self, url):
        '''
        Exctract html code of a given url
        :param url:
        :return:
        '''
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def getTag(self, bsObj, selector):
        '''
        Utility function used to get a content string from a
​    ​    Beautiful Soup object and a selector. Returns an empty
​    ​    string if no object is found for the given selector
        :param bsObj:
        :param selector:
        :return:
        '''

        selectedItems = bsObj.find_all(selector)

        if selectedItems is not None and len(selectedItems) > 0:
            return selectedItems
        else:
            return ''

    def parse(self):
        ''' To be defined for each sub-class'''
        pass


    def _text_corrector(self, string):
        '''
        correct strings
        :param string:
        :return:
        '''
        #remove whitespaces
        string = normalize('NFKD', string).strip()
        string = re.sub('[\t\n\r\f\v]',' ', string)
        string = re.sub('\s{2,}', ' ', string)
        #ß
        string = string.replace('Ã\x9f', 'ß')
        #ö
        string = string.replace('Ã¶', 'ö')
        #ä
        string = string.replace('Ã¤', 'ä')
        #ü
        string = string.replace('Ã1⁄4', 'ü')
        #Ö
        #string = string.replace('', 'Ö')
        #Ä
        #string = string.replace('', 'Ä')
        #Ü
        string = string.replace('Ã\x9c', 'Ü')
        #§
        string = string.replace('Â§', '§')

        return string


class CrawlerOverview(Crawler):

    def parse(self, website):
        '''
        Extract content
        :param website:
        :param url:
        :return: a generator for crawled pages
        '''

        url = website.url
        count_error = 0
        counter = 0

        while url != "":

            bsObj = self.getPage(url)

            if bsObj is not None:
                #iterate overall elements --> ignore first since it is only the headline
                for item in bsObj.select('tr'):
                    content = item.select_one('a[href]')
                    if content is not None:
                        text = self._text_corrector(content.text)
                        link = content.attrs['href']
                        link = urljoin(website.url, link).replace(' ', '')
                        counter += 1
                        yield ContentOverview(text, link)

                    else:
                        #should just be the first element
                        count_error +=1


            #check for additional website
            next_button = bsObj.find(title='Nach unten blättern')
            if next_button:
                print('---------------- Next Page - Links collected {} --------------------------'.format(counter))
                next_href = next_button.attrs["href"]
                next_href = urljoin(website.url, next_href).replace(' ', '') #remove ' ' at the end otherwise the next side is not correctly scrapped
                url = next_href
                time.sleep(1)
            else:
                url = ""


class CrawlerArticle(Crawler):

    def parse(self, website):
        '''
        extract content of the individual articles
        :param website:
        :return:
        '''

        bsObj = self.getPage(website.url)

        header_table = bsObj.select('.maske21')
        article_dict ={}

        #investiagte each header element - using dict since it is unclear which elements are given
        for element in header_table:
            article_dict.update( self._header_selection(element) )

        #Include the text
        article_dict['text'] =  self._text_corrector(bsObj.select_one('.WordSection1').text)

        #get co link - if exists
        a_href = bsObj.select_one('.WordSection1').select('a[href]')
        for element in a_href:
            if 'PARLISLINK' in element.attrs['href']:
                article_dict['co_link'] = urljoin(r'https://www.stvv.frankfurt.de/', element.attrs['href'])
                article_dict['co_id'] =  self._text_corrector( element.text )

        return ContentArticle(**article_dict)

    def _header_selection(self, element):
        '''
        Sort all given header information into correct categories
        :param element:
        :return:
        '''

        category = self._head_cat_string_adjust( element.select('td')[0].text )

        if category == 'vorlage':
            category = 'id'
            text = self._text_corrector( element.select('td')[1].text )
        elif category == 'dokumentart':
            category = 'doc_type'
            text = self._text_corrector( element.select('td')[1].text )
        elif category == 'gremium':
            category = 'committee'
            text = self._text_corrector(element.select('td')[1].text)
        elif category == 'fraktion/partei':
            category = 'party'
            text = self._text_corrector(element.select('td')[1].text)
        elif category == 'stadtteil':
            category = 'city_area'
            text = self._text_corrector(element.select('td')[1].text)
        elif category == 'datum':
            category = 'date'
            text = element.select('td')[1].text[:10]
        else:
            print('No header match for: {}'.format(category))
            category = '_no_match'
            text = True


        return {category:text}

    def _head_cat_string_adjust(self, text):
        return re.sub( '[: ]', '', self._text_corrector(text).lower() )



if __name__ == '__main__':

    from ParlisCrawler.Website import Website

    #---------- Overview ------------------#
    url =r'https://www.stvv.frankfurt.de/PARLISLINK/SDF?VORLAGEART=&NUMMER=&JAHR=2019&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und'
    overview_page = Website(url, None)

    crawler = CrawlerOverview()
    overview = crawler.parse(overview_page)
    counter = 0
    urls = []
    for element in overview:
        if counter == 5:
            break
        counter += 1
        urls.append(element.link)


    #------ Article -------------------------#
    link = 'https://www.stvv.frankfurt.de/PARLISLINK/DDW?VORLAGEART=ST&NUMMER=479&JAHR=2019&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und&?1?1?'
    link2 = 'https://www.stvv.frankfurt.de/PARLISLINK/DDW?VORLAGEART=&NUMMER=&JAHR=2017&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und&?9749?9745?'
    link3 = 'https://www.stvv.frankfurt.de/PARLISLINK/DDW?VORLAGEART=&NUMMER=&JAHR=2017&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und&?9749?7?'

    print(link)
    article_page = Website(link2, None)
    crawler_art = CrawlerArticle()
    article = crawler_art.parse(article_page)
    print('Dokumentart: {}'.format(article.doc_type))
    print('Vorlage: {}'.format(article.id))
    print('Committee: {}'.format(article.committee))
    print('Date: {}'.format(article.date))
    print('-'*10, '\n', article.text, '\n', '-'*10)
    print('Vorlage: {}'.format(article.co_id))

    #---------- anders ----------------------#
    link2 = 'https://www.stvv.frankfurt.de/PARLISLINK/DDW?VORLAGEART=&NUMMER=&JAHR=2017&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und&?9749?9745?'
    link3 = 'https://www.stvv.frankfurt.de/PARLISLINK/DDW?VORLAGEART=&NUMMER=&JAHR=2017&GREMIUM=&FRAKTION=&DOKUMENTTYP=VORL&FORMFL_OB=SORTFELD&FORM_SO=Absteigend&FORM_C=und&?9749?7?'

    bsObj2 = crawler.getPage(link2)
    bsObj3 = crawler.getPage(link3)
