import urllib
from bs4 import BeautifulSoup
from Utilities import checkElement, checkVal, getTime

def scrapeArticle(URL):
    #Indexes title, date, body, and author of given article
    #returns values in a dictionary
    bText = ''
    soup = BeautifulSoup(urllib.urlopen(URL))
    linkList = map(lambda x: x.get_text(), soup.find_all('a'))
    pageStatus = soup.find('div', attrs = {'class':'singlepage'})
    if pageStatus != None:
        soup = BeautifulSoup(urllib.urlopen('http://abcnews.go.com' + pageStatus.a.get('href')))
    for paragraph in soup.find_all('p', attrs = {'itemprop':'articleBody'}):
        if paragraph.a not in linkList:
            bText += paragraph.get_text()
    date = checkElement(soup.find('div', attrs = {'class':'date'}), 'date')
    image = soup.find('div', attrs = {'class' : 'main_media'})
    ArticleDict = {'title' : checkElement(soup.find('h1', True), 'title'),
                   'author' : " ".join(checkElement(
                       soup.find('div', attrs = {'class':'byline'}), 'author')
                                       .split('\n\n')[0].lower().title().split())
                                       .replace('And', 'and').replace('Abc', 'Source'),
                   'body_text' : bText.replace('\n', '\n\n').strip(),
                   'URL' : URL,
                   'source' : 'ABC News',
                   'date' : date,
                   'timestamp' : getTime(date, [',',':','.'], [], '%b %d %Y')}                  
    if image != None and image.img != None:
        if image.img.get('src') != None:
            ArticleDict['image'] = image.img.get('src')
    return ArticleDict

def scrapeSection(URL):
    #Scrapes given section, returns a list of article links
    linkList = []
    soup = BeautifulSoup(urllib.urlopen(URL))
    header = soup.find('div', attrs = {'id':'s4a_headline'})
    if header != None:
        headerLink = soup.find('div', attrs = {'id':'s4a_headline'}).a.get('href').encode('utf-8')
        if 'slideshow' not in headerLink and 'blogs' not in headerLink:
            linkList.append(headerLink)
    soup = BeautifulSoup(str(soup.find('div', attrs = {'class':'b_col'})))
    soup = BeautifulSoup(str(soup.find('div', attrs = {'class':'midcontainer'})))
    for story in soup.find_all(id='h_default'):
        story = story.a.get('href').encode('utf-8')
        if 'slideshow' not in story and 'blogs' not in story:
            linkList.append(story)
    return linkList

def scrapeLongSection(URL):
    #scrapes section with a big photo and header (Tech, Living etc.)
    #returns a list of article links
    linkList = []
    soup = BeautifulSoup(urllib.urlopen(URL))
    headerLink = soup.find('div', attrs = {'class':'headline spev8-medium'}).a.get('href').encode('utf-8')
    if 'slideshow' not in headerLink:
        linkList.append(headerLink)
    soup = BeautifulSoup(str(soup.find('div', attrs = {'class':'midcontainer'})))
    for story in soup.find_all(id='h_default'):
        story = story.a.get('href').encode('utf-8')
        if 'slideshow' not in story and 'entertainment' not in story:
            if 'http' not in story:
                linkList.append(story)
    return linkList

def scrapeFrontPage(URL):
    #scrapes front page, returns a list of article links
    linkList = []
    soup = BeautifulSoup(urllib.urlopen(URL))
    carousel = BeautifulSoup(str(soup.find('div', attrs = {'class':'carousel carousel-center'})))
    for link in carousel.find_all('a'):
        curCell = link.get('href')
        if curCell not in linkList:
            linkList.append(curCell.encode('utf-8'))
    soup = BeautifulSoup(str(soup.find('div', attrs = {'class':'a_cont'})))
    for story in soup.find_all('div', attrs = {'class':'h'}):
        story = story.a.get('href').encode('utf-8')
        if 'slideshow' not in story and 'video' not in story:
            if 'social-climber' not in story and 'blogs' not in story:
                if 'http' not in story:
                    linkList.append(story)
    return linkList
        
