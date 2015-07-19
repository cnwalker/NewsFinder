import ForbesScraper, WATimesScraper
import CNNScraper, ABCScraper, AlJazeeraScraper, CBSScraper
from Utilities import groomArticles

def getPage(URL, base_URL, getSection, getArticle):
    articleList = []
    article_links = getSection(URL)
    for i in range(0, len(article_links)):
        if 'money.cnn.com' in article_links[i]:
            getArticle = CNNScraper.scrapeMoney
        curArticle = getArticle(base_URL + article_links[i])
        if curArticle != None and len(curArticle['body_text']) >= 30:
            curArticle['status'] = i
            articleList.append(curArticle)
    return groomArticles(articleList)

def getCNN(section):
    if section == 'front':
        section = '/'
    return getPage('http://www.cnn.com/' + section.lower(),
                   'http://www.cnn.com',
                   CNNScraper.scrapeSection,
                   CNNScraper.scrapeArticle)

def getCNNMoney(section):
    if section == 'business':
        section = 'news'
    return getPage('http://money.cnn.com/' + section.lower(),
                   'http://money.cnn.com/',
                   CNNScraper.scrapeMoneySection,
                   CNNScraper.scrapeMoney)

def getABC(section):
    if section == 'front':
        sectionSifter = ABCScraper.scrapeFrontPage
        section = ''
    elif section.lower() in ['politics', 'tech', 'lifestyle']:
        sectionSifter = ABCScraper.scrapeLongSection
    else:
        sectionSifter = ABCScraper.scrapeSection
    return getPage('http://abcnews.go.com/' + section.lower(),
                   'http://abcnews.go.com',
                   sectionSifter,
                   ABCScraper.scrapeArticle)

def getAlJazeera(section):
    if section == 'front':
        sectionSifter = AlJazeeraScraper.scrapeFront
        sectionURL = 'http://america.aljazeera.com/'
    else:
        sectionURL = ('http://america.aljazeera.com/topics/topic/categories/'
                      + section.upper() + '.html')
        sectionSifter = AlJazeeraScraper.scrapeSection
    return getPage(sectionURL,
                   'http://america.aljazeera.com',
                   sectionSifter,
                   AlJazeeraScraper.scrapeArticle)

def getCBS(section):
    if section == 'front':
        sectionSifter = CBSScraper.scrapeMainPage
        section = '/'
    else:
        sectionSifter = CBSScraper.scrapeSection
    return getPage('http://www.cbsnews.com/' + section.lower(),
                   'http://www.cbsnews.com',
                   sectionSifter,
                   CBSScraper.scrapeArticle)
                   
def getForbes(section):
    return getPage('http://www.forbes.com/' + section.lower(),
                   'http://www.forbes.com/',
                   ForbesScraper.scrapeSection,
                   ForbesScraper.scrapeArticle)

def getWATimes(section):
    if section == 'front':
        section = ''
    if section in ['health', 'technology']:
        section = 'culture/' + section
    return getPage('http://www.washingtontimes.com/news/' + section.lower(),
                   'http://www.washingtontimes.com',
                   WATimesScraper.scrapeSection,
                   WATimesScraper.scrapeArticle)
                   



                   
        
