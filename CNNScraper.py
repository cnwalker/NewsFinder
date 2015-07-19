import urllib, datetime
from bs4 import BeautifulSoup
from Utilities import checkElement, checkVal, getTime

def scrapeArticle(URL):
    #scrapes CNN article
    #removes links that are not part of the main article
    #returns author, last updated date, title, image link, and the body text in a dictionary
    soup = BeautifulSoup(urllib.urlopen(URL))
    linkList = map(lambda x: x.get_text(), soup.find_all('a'))
    inText = ''
    for para in soup.find_all('p', attrs = {'class': 'zn-body__paragraph'}):
        if para.get_text() not in linkList:
            if para.q == None and para.em == None:
                inText += (para.get_text().strip() + '\n\n')
    date = checkElement(soup.find('div', attrs = {'class': 'cnn_strytmstmp'}), 'date')
    ArticleDict =  {'title' : checkElement(soup.find('h2', attrs = {'class': 'pg-headline'}), 'title'),
                    'author' : checkElement(
                            soup.find('span', attrs = {'class': 'metadata__byline__author'}), 'author'),
                    'source' : 'CNN',
                    'body_text' : inText,
                    'date' : date,
                    'URL' : URL,
                    'timestamp' : getTime('0' + date.replace('Update', ''),
                                          [','] ,[':'],
                                          '%I %M %p %Z %a %B %d %Y')}
    image = soup.find('div', attrs = {'class' : 'cnn_stryimg640captioned'})
    if image != None:
        image = BeautifulSoup(str(image)).prettify()
        for cell in image.split(' '):
            if 'src' in cell:
               ArticleDict['image'] = cell[cell.find('http'):].replace('"', '')
    elif soup.find('div', attrs = {'class':'cnnStryVidCont'}) != None:
        image = soup.prettify().split('\n')
        for cell in image:
            if 'thumb:' in cell:
                image = cell[cell.find('http'):]
        if image != None:
            ArticleDict['image'] = image[:-1*(len(image) - image.find("'"))]
    else:
        image = soup.find('div', attrs = {'class' : 'cnnArticleGalleryPhotoContainer'})
        if image != None:
            image = BeautifulSoup(str(image)).prettify().split(' ')
            for cell in image:
                if 'src' in cell:
                   ArticleDict['image'] = cell[cell.find('http'):].replace('"', '')
    return ArticleDict

def scrapeSection(URL):
    #scrapes any section of CNN.com except for the tech section
    #returns a list of all article links
    linkList = []
    soup = BeautifulSoup(urllib.urlopen(URL))
    header = checkVal(soup.find('div', attrs = {'class' : 'zn-banner'}), False)
    if header != None:
        linkList.append(header)
    for link in soup.find_all('h3', attrs = {'class':'cd__headline'}):
        link = checkVal(link, False)
        if link != None:
            linkList.append(link)
    return linkList       
            
def scrapeMoney(URL):
    #scrapes CNN Money article
    #returns author, last updated date, title, and body text in a dictionary
    #strips the links that are not part of the main article
    soup = BeautifulSoup(urllib.urlopen(URL))
    image = soup.find('div', attrs = {'id': 'ie_dottop'})
    linkList = map(lambda x: x.get_text(), soup.find_all('a'))
    body_soup = BeautifulSoup(str(soup.find('div', attrs = {'id': 'storytext'})))
    date = checkElement(soup.find('span', attrs = {'class' : 'cnnDateStamp'}), 'date')
    inText = checkElement(soup.find('h2'), 'header') + '\n\n' 
    for paragraph in body_soup.find_all('p')[1:]:
        if paragraph.find('span') == None:
            if paragraph.a != None:
                if paragraph.a.get_text() != linkList:
                    inText += paragraph.get_text()[1:] + '\n\n'
            else:
                inText += paragraph.get_text()[1:] + '\n\n'
    in_soup = BeautifulSoup(str(soup.find('div', attrs = {'id': 'storycontent'})))
    moneyDict = {'title' : checkElement(in_soup.find('h1'), 'title'),
                 'author' : checkElement(
                     soup.find('span', attrs = {'class' : 'byline'}), 'author'),
                 'date' : date,
                 'source' : 'CNN Money',
                 'body_text' : inText,
                 'URL' : URL,
                 'timestamp' : getTime(date, [','] ,[':'],
                                       '%B %d %Y %I %M %p %Z')}
    if image != None and image.img != None:
        src = image.img.get('src')
        if src != None:
            moneyDict['image'] = image.img.get('src')
    else:
        img2 = soup.find('figure', attrs = {'class': 'body_img body_img--620'})
        if img2 != None:
            moneyDict['image'] = img2.img.get('src')
    return moneyDict

def scrapeMoneySection(URL):
    #scrapes a section page of CNN Money
    #returns a list of all article links
    linkList = []
    soup = BeautifulSoup(urllib.urlopen(URL))
    header = checkVal(soup.find('div', attrs = {'class' : 'cnnHeadline'}), True)
    if header != None:
        linkList.append(header)
    for link in soup.find_all('h2'):
        link = checkVal(link, True)
        if link != None:
            linkList.append(link)
    return linkList

