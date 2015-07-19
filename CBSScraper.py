import urllib, datetime
from Utilities import checkVal, checkElement, getTime
from bs4 import BeautifulSoup

#scrapes given article and returns dictionary with title, date, body, author and source
def scrapeArticle(URL):
    bText = ''
    sList = []
    soup = BeautifulSoup(urllib.urlopen(URL))
    mainStory = BeautifulSoup(str(soup.find('div', attrs = {'class': 'entry'})))
    for paragraph in mainStory.find_all('p'):
        if paragraph.has_attr('class') != True and paragraph.get_text().strip() != '':           
            sList.append(' '.join(paragraph.get_text()
                                  .replace('CBS', 'Source').strip().split()))
    if len(sList) <= 1:
        return None
    for sentence in sList:
        bText += sentence.strip() + ('\n\n')
    date = checkElement(soup.find('span', attrs = {'class': 'time'}), 'date')
    
    ArticleDict = {'title' : checkElement(soup.find('h1', attrs = {'class': 'title'}), 'title'),
                   'author' : checkElement(soup.find('span', attrs = {'class':'author'}), 'author'),
                   'body_text' : bText[:-3],
                   'URL' : URL,
                   'date' : date,
                   'timestamp' : getTime(date.replace('AM', ' AM ').replace('PM', ' PM ').strip(),
                                         [',',':'], [], '%B %d %Y %I %M %p')}                  
    source = soup.find('span', attrs = {'class': 'source'})
    if source != None:
        ArticleDict['source'] = source.get_text()
    else:
        ArticleDict['source'] = 'CBS News'
    image = soup.find('div', attrs = {'class':'article-image'})
    if image != None and image.img != None:
        ArticleDict['image'] = image.img.get('src')
    return ArticleDict

#Scrapes the main page of CBSnews.com and returns a list of article links
def scrapeMainPage(URL):
    linkList = []
    soup = BeautifulSoup(urllib.urlopen(URL))
    header = soup.find('h1', attrs = {'class':'title'})
    if header != None:
        linkList.append(header.a.get('href'))
    soup = BeautifulSoup(str(soup.find('div', attrs = {'class':'col-5'})))
    for story in soup.find_all('li'):
        if '/' == story.a.get('href')[0] and 'news' in story.a.get('href'):
            linkList.append(story.a.get('href'))
    return linkList

#Scrapes given section of CBSnews.com and returns a list of article links
def scrapeSection(URL):
    linkList = []
    soup = BeautifulSoup(urllib.urlopen(URL))
    header = soup.find('h3', attrs = {'class':'title'}).a.get('href').encode('utf-8')
    if header != None:
        linkList.append(header)
    soup = BeautifulSoup(str(soup.find('div', attrs = {'class':'col-5'})))
    for story in soup.find_all('li'):
        if story != None:
            if '/' == story.a.get('href')[0] and 'news' in story.a.get('href'):
                linkList.append(story.a.get('href'))
    return linkList
