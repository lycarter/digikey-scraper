from lxml import html
import requests
import time

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
      self.parts.extend(self.getPartNums(i))

  def htmlFromNum(self, pageNum):
    return 'http://www.digikey.com/product-search/en/discrete-semiconductor-products/transistors-fets-mosfets-single/1376381/page/%d?quantity=10&pageSize=%d' % (pageNum, self.qtyPerPage)

  @timing
  def getPartNums(self, pageNum):
    page = requests.get(htmlFromNum(pageNum))
    tree = html.fromstring(page.content)
    parts = []
    for i in range(self.qtyPerPage):
      part = tree.xpath('//*[@id="lnkPart"]/tr[%d]/td[5]/a/span/text()' % (i + 1))
      if part:
        parts.append(str(part[0]))
      else:
        break
    return parts

DigikeyScraper(500, 83)