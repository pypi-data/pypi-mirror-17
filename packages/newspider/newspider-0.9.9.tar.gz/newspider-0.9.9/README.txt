##Example.py

# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq

from newspider.interfaces import *
from newspider.spider import Newspider


class DemoFetcher(IntFetcher):
    def __init__(self):
        self.next_page = []

    def fetch_detail_urls(self,html):
        d = pq(html)
        list = []

        for a in d('.post-title a'):
            url = d(a).attr('href')
            extras = {"category": "Test for %s" % url}
            list.append((url,extras))

        for l in d('.page-navigator a'):
            self.next_page.append(d(l).attr('href'))

        return list

    def start_page(self):
        return ['http://www.typechodev.com/','http://www.typechodev.com/index.php/category/questions/']

    def next_pages(self):
        return self.next_page


class DemoParser(IntParser):
    def parse(self,tag,html,extras):
        print "Receive content from url %s for tag %s|%s" % (extras.get('_url'),extras.get('category'),tag)


if __name__ == '__main__':
    sp = Newspider()
    sp.config('GUARD_INTERVAL', 0)

    sp.add_parser(DemoParser())
    sp.add_fetcher(DemoFetcher())

    sp.run()

