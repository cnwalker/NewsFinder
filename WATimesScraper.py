import urllib
from bs4 import BeautifulSoup
from Utilities import checkVal, checkElement, getTime, makeReadable

def scrapeArticle(URL):
    #Scrapes article at given url
    #Returns title, author, source, and body_text in dictionary
    bText = ''
    soup = BeautifulSoup(urllib.urlopen(URL))
    date_source = ' '.join(soup.find('span', attrs = {'class' : 'source'}).get_text().split())[1:].split('-')
    linkList = map(lambda x: x.get_text(), soup.find_all('a'))
    articleDict ={
        'title' :  checkElement(soup.find('h1', attrs = {'class' : 'page-headline'}), 'title'),
         'author' : checkElement(soup.find('span', attrs = {'class':'byline'}), 'author'),
         'source' : date_source[0].strip(),
         'date' : date_source[1].strip(),
         'timestamp' : getTime(date_source[1].strip(), [','], [], '%A %B %d %Y'),
         'URL' : URL}
    body_soup = BeautifulSoup(str(soup.find('div', attrs = {'class' : 'article-text'})))
    for para in body_soup.find_all('p'):
        if para.get_text() not in linkList:
            bText += para.get_text().strip() + '\n\n'
    articleDict['body_text'] = bText
    image = soup.find('div', attrs = {'class' : 'photo'})
    if image != None and image.img != None:
        if image.img.get('src') != None:
            articleDict['image'] = image.img.get('src')
    return articleDict

def scrapeSection(URL):
    soup = BeautifulSoup(urllib.urlopen(URL))
    return (list(set(map(lambda x: checkVal(x, False),
                         soup.find_all('h2', attrs = {'class': 'article-headline'})))))


                
     
                   
                   
