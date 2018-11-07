import requests
from lxml import html

class Scraper:

    def __init__(self, project):
        self.project = project

    def scrape(self):

        response = requests.get(self.project['url'])
        tree = html.fromstring(response.content)
        path = tree.xpath(self.project['xpath'] + "/text()")
        raw = path[0]
        if len(path) > 1:
            for r in path:
                r_clean = r.strip().replace('\n', '').replace('\r', '')
                if len (r_clean) > 0:
                    raw = r_clean
        raw_version = raw.strip().replace('\n', ' ').replace('\r', '')

        version = ""
        first = -1
        last = 0
        for i, c in enumerate(raw_version):
            if c.isdigit():
                if first == -1:
                    first = i
                last = i

        version = raw_version[first:last+1]
        return version
