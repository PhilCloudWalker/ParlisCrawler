##########################################
#  Test for Output files
###########################################
import pytest
from ParlisCrawler.Content import ContentOverview

########################################################
# Unit test for content overview
########################################################

#1) check year function
@pytest.mark.content
def test_cv_year():
    test = ContentOverview('title', 'link', '2019-06-02')
    assert ( test.year == 2019)

@pytest.mark.content
def test_cv_title_input():
    test = ContentOverview('title', 'link', '2019-06-02')
    with pytest.raises(ValueError):
        test.title=2

@pytest.mark.content
def test_cv_date_input():
    test = ContentOverview('title', 'link', '2019-06-02')
    with pytest.raises(ValueError):
        test.date='20100219'




