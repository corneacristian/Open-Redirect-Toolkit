import sys
import os
import urllib2
import socket
import time
import gzip
import StringIO
import re
import random
import types
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
try:
    load_dotenv(find_dotenv(usecwd=True))
    base_url = os.environ.get('BASE_URL')
    results_per_page = int(os.environ.get('RESULTS_PER_PAGE'))
except:
    sys.exit(1)

user_agents = list()

class SearchResult:
    def __init__(self):
        self.url = ''

    def getURL(self):
        return self.url

    def setURL(self, url):
        self.url = url

    def printIt(self, prefix=''):
        print (self.url)
        
    def writeFile(self, filename):
        file = open(filename, 'a')
        try:
            file.write('url:' + self.url + '\n')
        except IOError, e:
            print ('file error:', e)
        finally:
            file.close()


class GoogleAPI:
    def __init__(self):
        timeout = 40
        socket.setdefaulttimeout(timeout)

    def randomSleep(self):
        sleeptime = random.randint(60, 120)
        time.sleep(sleeptime)

    def extractDomain(self, url):
        domain = ''
        pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M)
        url_match = pattern.search(url)
        if(url_match and url_match.lastindex > 0):
            domain = url_match.group(1)

        return domain

    def extractUrl(self, href):
 
        url = ''
        pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
        url_match = pattern.search(href)
        if(url_match and url_match.lastindex > 0):
            url = url_match.group(1)

        return url

    def extractSearchResults(self, html):

        results = list()
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', id='main')
        if (type(div) == types.NoneType):
            div = soup.find('div', id='center_col')
        if (type(div) == types.NoneType):
            div = soup.find('body')
        if (type(div) != types.NoneType):
            lis = div.findAll('a')
            if(len(lis) > 0):
                for link in lis:
                    if (type(link) == types.NoneType):
                        continue
                    
                    url = link['href']
                    if url.find(".google") > 6:
                        continue
                        
                    url = self.extractUrl(url)
                    if(cmp(url, '') == 0):
                        continue
                    result = SearchResult()
                    result.setURL(url)
                    span = link.find('div')
                    results.append(result)
        return results

    def search(self, query, lang='en', num=results_per_page):
        search_results = list()
        query = urllib2.quote(query)
        if(num % results_per_page == 0):
            pages = num / results_per_page
        else:
            pages = num / results_per_page + 1

        for p in range(0, pages):
            start = p * results_per_page
            url = '%s/search?hl=%s&num=%d&start=%s&q=%s' % (
                base_url, lang, results_per_page, start, query)
            retry = 3
            while(retry > 0):
                try:
                    request = urllib2.Request(url)
                    length = len(user_agents)
                    index = random.randint(0, length-1)
                    user_agent = user_agents[index]
                    request.add_header('User-agent', user_agent)
                    request.add_header('connection', 'keep-alive')
                    request.add_header('Accept-Encoding', 'gzip')
                    request.add_header('referer', base_url)
                    response = urllib2.urlopen(request)
                    html = response.read()
                    if(response.headers.get('content-encoding', None) == 'gzip'):
                        html = gzip.GzipFile(
                            fileobj=StringIO.StringIO(html)).read()

                    results = self.extractSearchResults(html)
                    search_results.extend(results)
                    break
                except urllib2.URLError, e:
                    print ('url error:', e)
                    self.randomSleep()
                    retry = retry - 1
                    continue

                except Exception, e:
                    print ('error:', e)
                    retry = retry - 1
                    self.randomSleep()
                    continue
        return search_results


def load_user_agent():
    fp = open('./user_agents', 'r')

    line = fp.readline().strip('\n')
    while(line):
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()


def crawler():
    load_user_agent()

    api = GoogleAPI()

    expect_num = 10
    domain_to_search = '{}{}'.format('site:*.', sys.argv[1])
    if(1 == 1):
        keywords = open('./keywords', 'r')
        keyword = keywords.readline()
        while(keyword):
            results = api.search('{} {}'.format(domain_to_search, keyword), num=expect_num)
            for r in results:
                r.printIt()
            keyword = keywords.readline()
        keywords.close()



if __name__ == '__main__':
    crawler()
