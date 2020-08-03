'''
Created on 19.02.2019
@author: Philipp
'''

'''
This modul defines the structure of the output files

'''
#inspiration https://www.oreilly.com/library/view/web-scraping-with/9781491985564/ch04.html
from datetime import datetime


class ContentOverview():
    '''
    Result Object. Return overview of articles
    '''
    def __init__(self, title, link, date = '1900-01-01', district = None):
        self.title = title
        self.link = link
        self.date = date
        self.district = district

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if type(title) == str:
            self._title = title
        else:
            raise ValueError('title has to be a string')

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        #check whether input is already a timestamp
        if type(date) == datetime:
            self._date = date
        elif type(date) == str:
            self._date = datetime.strptime(date, '%Y-%m-%d')
        else:
            raise ValueError('date {} does not match format \'%Y-%m-%d\''.format(date))

    @property
    def year(self):
        return self.date.year



class ContentArticle():
    '''
    Result Object. Structures Articles
    '''

    def __init__(self, doc_type, id, date, text,
                 committee = None , party = None, co_id = None, co_link = None, city_area = None,
                 _no_match = False):
        #header : should have every article
        self.doc_type = doc_type
        self.id = id
        self.date = date

        #get text
        self.text = text

        #optional
        self.party = party
        self.city_area = city_area
        self.committee = committee
        self.co_id = co_id
        self.co_link = co_link
        self._no_match = _no_match

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        #check whether input is already a timestamp
        if type(date) == datetime:
            self._date = date.strftime("%Y-%m-%d")
        elif type(date) == str:
            self._date = datetime.strptime(date, '%d.%m.%Y').strftime("%Y-%m-%d")
        else:
            raise ValueError('date {} does not match format \'%d.%m.%Y\''.format(date))




