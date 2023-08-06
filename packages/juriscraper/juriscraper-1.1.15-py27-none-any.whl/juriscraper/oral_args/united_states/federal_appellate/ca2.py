"""Scraper for Second Circuit
CourtID: ca2
Author: MLR
Reviewer: MLR
History:
  2016-09-09: Created by MLR
"""

from lxml import html
from lxml.html import html5parser, fromstring, tostring
from juriscraper.OralArgumentSite import OralArgumentSite
from juriscraper.lib.string_utils import convert_date_string


class Site(OralArgumentSite):
    def __init__(self, *args, **kwargs):
        super(Site, self).__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.url = 'http://www.ca2.uscourts.gov/decisions'
        self.method = 'POST'
        self.parameters = {
            'IW_SORT': '-DATE',
            'IW_BATCHSIZE': '100',
            'IW_FIELD_TEXT': '*',
            'IW_DATABASE': 'Oral Args'
        }
        self.uses_selenium = False
        self.base_xpath = '//tr[contains(.//a/@href, "mp3")]'

    def _make_html_tree(self, text):
        """ Grab the content using the html5parser and return it as HtmlElement.

        :param text: The html of the document
        :return: an lxml.HtmlElement object
        """
        e = html5parser.document_fromstring(text.encode('utf-8'))
        html_tree = fromstring(tostring(e))
        return html_tree

    def _get_download_urls(self):
        path = '//@href[contains(., "mp3")]'
        return list(self.html.xpath(path))

    def _get_case_names(self):
        case_names = []
        for e in self.html.xpath('%s/td[2]' % self.base_xpath):
            s = html.tostring(e, method='text', encoding='unicode')
            case_names.append(s)
        return case_names

    def _get_case_dates(self):
        path = '%s/td[3]' % self.base_xpath
        dates = []
        for e in self.html.xpath(path):
            s = html.tostring(e, method='text', encoding='unicode')
            dates.append(convert_date_string(s))
        return dates

    def _get_docket_numbers(self):
        path = '%s/td[1]//text()' % self.base_xpath
        return list(self.html.xpath(path))
