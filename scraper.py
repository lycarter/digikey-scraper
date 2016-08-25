from lxml import html
import requests
import time

import secrets  # My own secrets file, contains Octopart API key

import json

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

class DigikeyScraper():
  def __init__(self, qtyPerPage, numPages):
    self.qtyPerPage = qtyPerPage
    self.parts = []
    for i in range(numPages):
      self.parts.extend(self.getPartNums(i+1))

  def htmlFromNum(self, pageNum):
    return 'http://www.digikey.com/product-search/en/discrete-semiconductor-products/transistors-fets-mosfets-single/1376381/page/%d?quantity=10&pageSize=%d' % (pageNum, self.qtyPerPage)

  @timing
  def getPartNums(self, pageNum):
    page = requests.get(self.htmlFromNum(pageNum))
    tree = html.fromstring(page.content)
    parts = []
    for i in range(self.qtyPerPage):
      part = tree.xpath('//*[@id="lnkPart"]/tr[%d]/td[5]/a/span/text()' % (i + 1))
      if part:
        parts.append(str(part[0]))
      else:
        break
    return parts

class Octopart():
  def __init__(self, apiKey):
    self._apiKey = apiKey

  def getPart(self, partNum):
    url = 'http://octopart.com/api/v3/parts/match?'
    url += 'apikey=%s' % self._apiKey
    url += '&queries=[{"mpn":"%s"}]' % partNum
    url += '&pretty_print=true'

    print 'making query to %s' % url

    page = requests.get(url)
    response = json.loads(page.content)
    print json.dumps(response, sort_keys=True, indent=4)

scraper = DigikeyScraper(10, 1)

octo = Octopart(secrets.getOctopartApi())

octo.getPart(scraper.parts[0])