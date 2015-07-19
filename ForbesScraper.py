import datetime, urllib
from bs4 import BeautifulSoup
from Utilities import checkVal, checkElement, getTime

def scrapeArticle(URL):
    paraList = []
    ArticleDict = {}
    soup = BeautifulSoup(urllib.urlopen(URL))
    rawList = soup.prettify().split('\n')
    for cell in rawList:
        if 'published_time' in cell:
            cell = cell[cell.find('content=') + 9:]
            cell = cell[:cell.find('"')]
            p = cell.split('-')
            ArticleDict['date'] = p[1] + '/' + p[2] + '/' + p[0]
        else:
            ArticleDict['date'] = 'Unknown'
    ArticleDict['timestamp'] = getTime(ArticleDict['date'], [','], ['/'], '%m %d %Y')
    soup2 = BeautifulSoup(str(soup.find('div', attrs = {'class':'body'})))
    for line in soup2.find_all('p'):
        if line.has_attr('class') == False:
            paraList.append(line.get_text())
    ArticleDict['author'] = checkElement(soup.find('p'),'author')
    ArticleDict['body_text'] = '\n\n'.join(paraList[:-2])
    ArticleDict['title'] = checkElement(soup.find('h1'), 'title')
    ArticleDict['source'] = 'Forbes'
    ArticleDict['URL'] = URL
    return ArticleDict

def scrapeSection(URL):
    linkList = []
    soup = BeautifulSoup(urllib.urlopen(URL))
    header = soup.find('h2', attrs = {'class':'editable editable-hed'})
    if header != None and header.a != None:
        linkList.append(header.a.get('href'))
    for link in soup.find_all('article'):
        if link.a != None:
            linkList.append(link.a.get('href'))
    soup = BeautifulSoup(str(soup.find('section', attrs = {'id':'mostPopular'})))
    for sect in soup.find_all('ol'):
        if sect['id'] == 'mP_business':
            soup = BeautifulSoup(str(sect))
    for story in soup.find_all('li'):
        if story.a != None:
            story = story.a.get('href')
            if 'forbes' in story:
                linkList.append(story)
    for cell in linkList:
        if 'netapp' in cell:
            linkList.remove(cell)
    return linkList
    
