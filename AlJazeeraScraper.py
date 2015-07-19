import urllib, datetime
from bs4 import BeautifulSoup
from Utilities import checkVal, checkElement, getTime

def scrapeArticle(URL):
    #Goes through an article indexes the title, date, body text and author if avaliable
    #Does not work on galleries and video
    #Strips name Aljazeera from body text
    inText = ''
    curImage = ''
    soup = BeautifulSoup(urllib.urlopen(URL))
    for section in soup.find_all('div', attrs = {'class':'text section'}):
        bodySoup = BeautifulSoup(str(section))
        for paragraph in bodySoup.find_all('p'):
            inText += paragraph.get_text().encode('utf-8').strip() + '\n\n'
    ArticleDict = {'title' : checkElement(
                                soup.find('div', attrs = {'class':'articleOpinion-title--container'}),'title'),
                   'author' : ' '.join(checkElement(
                                soup.find('span', attrs = {'class':'articleOpinion-byline'}), 'author').split()),
                   'body_text' : inText,
                   'source' : 'Al Jazeera',
                   'URL' : URL}
    date = soup.find('span', attrs = {'class':'date'})
    time = soup.find('span', attrs = {'class':'time'})
    if date != None:
        if time != None:
            ArticleDict['date'] = (date.get_text() + ' ' + time.get_text()).encode('utf-8')
            ArticleDict['timestamp'] = getTime(ArticleDict['date'].replace('AM', ' AM ').replace('PM', ' PM '),
                                           [','], [':'], '%B %d %Y %I %M %p %Z')
        else:
            ArticleDict['date'] = date.get_text().encode('utf-8')
            ArticleDict['timestamp'] = getTime(ArticleDict['date'].replace('AM', ' AM ').replace('PM', ' PM '),
                                           [','], [':'], '%B %d %Y')
    else:
        ArticleDict['date'] = 'Unknown'
        ArticleDict['timestamp'] = datetime.datetime.now()
            
    imageList = soup.prettify().split('\n')
    for cell in imageList:
        if 'background-image' in cell and '1460' in cell:
            curImage = cell
    curImage = curImage[(curImage.find("'") + 1):]
    curImage = curImage[:curImage.find("'")]
    if curImage.strip() != '':
        ArticleDict['image'] = 'http://america.aljazeera.com' + curImage
    return ArticleDict

def scrapeSection(URL):
    #Scrapes news section (US, International, Economy, Technology, Science, Environment etc.)
    #Retrieves all links to articles (excludes videos, galleries, and external links)
    linkList = []
    soup = BeautifulSoup(urllib.urlopen(URL))
    for story in soup.find_all('article', attrs = {'class':'news-item media'}):
        curLink = story.a.get('href')
        if curLink[0] == '/' and 'watch' not in curLink:
            linkList.append(curLink)
    return linkList
       
def scrapeFront(URL):
    #Scrapes front page of Aljazeera and returns all article links 
    linkList = []
    soup = BeautifulSoup(urllib.urlopen(URL))
    curLink = soup.find('h1', attrs = {'class':'topStories-headline'})
    if curLink != None and curLink.a != None:
        curLink = curLink.a.get('href').encode('utf-8')
        if curLink[0] == '/':
                linkList.append(curLink)
    for story in soup.find_all('h3', attrs = {'class':'headline'}):
        if story.a != None and story.a.get('href') != None:
            curStory = story.a.get('href')
            if curStory[0] == '/':
                linkList.append(story.a.get('href'))
    return linkList
