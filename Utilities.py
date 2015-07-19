import datetime

def removeTxt(input_text, rlist):
    #removes all the text in the input list from the input text
    for cell in rlist:
        input_text.replace(cell, '')
    return input_text

def groomString(string, elimList, spaceList):
    #Grooms a date string to a format acceptable to striptime
    #Groomed strings are then turned into datetime objects
    for element in elimList:
        string = string.replace(element,'')
    for element in spaceList:
        string = string.replace(element, ' ')
    string = string.replace('ET', 'EST').replace('Updated', '')
    return string


def checkElement(soup_ob, txt_type):
    #returns messages if scraped soup object is none
    #grooms date strings
    if soup_ob == None:
        return {'title' : 'No title avaliable',
                'author' : 'Source News Staff',
                'date' : 'Unknown',
                'header' : ''}[txt_type]
    else:
        if txt_type == 'date':
            return removeTxt(soup_ob.get_text(), ['updated', '(AP)']).strip()
        else:
            return soup_ob.get_text().strip()
            

def getTime(date, elimList, spaceList, strp_input):
    # Takes input of a CNN date string, returns the corresponding datetime
    try:
        if date != 'Unknown':
            return datetime.datetime.strptime(
                groomString(date, elimList, spaceList), strp_input)
        else:
            return datetime.datetime.now()
    except:
        return datetime.datetime.now()

def checkVal(URL_ob, external_permission):
    #Checks to see if a link is scrapable by the scraper
    #May allow or prohibit external links
    URL = ''
    if URL_ob != None:
        if URL_ob.a != None:
            URL = URL_ob.a.get('href')
    bannedList = ['http:','video', 'gallery', 'slideshow']
    if external_permission == True:
        bannedList.remove('http:')
    for banned in bannedList:
        if banned in URL:
            return None
    else:
        return URL

def groomArticles(articleList):
    #Does a final combover of the given dictionary
    #Replaces all sources written in ForbiddenNames.txt with the word Source
    fList = ['The Associated Press',' AP ','(AP)','CBS','CNN',
             'ABC','Al Jazeera','Washington Times','Washington Free Beacon',
             'New York Times','Associated Press','Health.com',
             'Slate','cnn','Forbes','forbes'] 
    for i in range(0, len(articleList)):
       curDict = articleList[i]
       for key in curDict.keys():
           if key in ['title', 'author', 'body_text']:
               for forbidden in fList:
                   curDict[key] = curDict[key].replace(forbidden, 'Source')
    articleList[i] = curDict
    return articleList

def makeReadable(in_string):
    #Replaces non with Unicode equivalents
    return in_string.decode('unicode_escape').encode('ascii', 'ignore').strip()
