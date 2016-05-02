import sqlite3
from datetime import datetime
from BrowserData import * 
import logging
import os 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('readFireFox')

def readAll(path):
    browserData = BrowserData()
    browserData.formInput = readFormHistory(path)
    browserData.browserInfo = browserInfo(path)
    browserData.places = readPlacesData(path)
    browserData.cookies = readCookiesData(path)
    return browserData

def browserInfo(path):
    dbPath = os.path.join(path, 'compatibility.ini')
    
    if os.path.exists(dbPath):
        f = open(dbPath)
        return [line for line in f]
    else:
        logger.warn('Cannot read ' + dbPath)
        return ['No browser info was found']


def readFormHistoryDb(path):
    logger.info('reading formhistory.sqlite ...')
    return readDB(path, 'formhistory.sqlite', 'select * from moz_formhistory')

def readFormHistory(path):
    data = readFormHistoryDb(path)
    
    def m(data):
        formInput = FormInput()
        formInput.text = data['value']
        formInput.count = data['timesUsed']
        formInput.firstUsedDate = timeConverter(data['firstUsed'])
        formInput.lastUsedDate = timeConverter(data['lastUsed'])
        formInput.fieldName = data['fieldName']
        return formInput
    
    return [m(i) for i in data]

def readPlacesDataDb(path):
    logger.info('reading places.sqlite ...')
    return readDB(path, 'places.sqlite', 'select * from moz_places')

def readPlacesData(path):
    data = readPlacesDataDb(path)
    def m(data):
        place = Place()
        place.text = data['title'] or ''
        place.url = data['url']
        place.host = data['rev_host'][-2::-1] # reverse the string and drop leading period
        place.count = data['visit_count']
        place.lastUsedDate = timeConverter(data['last_visit_date'])
        place.hidden = data['hidden']
        place.typed = data['typed']
        return place
    
    return [m(i) for i in data]

def readCookiesDataDb(path):
    logger.info('reading cookies.sqlite ...')
    return readDB(path, 'cookies.sqlite', 'select * from moz_cookies')

def readCookiesData(path):
    data = readCookiesDataDb(path)
    def m(data):
        cookie = Place()
        cookie.name = data['name']
        cookie.value = data['value']
        cookie.host = cookie.url = data['baseDomain']
        return cookie
    
    return [m(i) for i in data]

    
def readDB(path, dataBase, query):
    dbPath = os.path.join(path, dataBase)
    
    if os.path.exists(dbPath):
        conn = sqlite3.connect(dbPath)
        conn.row_factory = sqlite3.Row
        cur = conn.execute(query)
        data = cur.fetchall()
        conn.close()
        return data
    else:
        logger.warn(dpPath + ' does not exist')
        return []

def printData(data):
      for d in data:
        print([{k:d[k]} for k in d.keys()])
    
def timeConverter(microSec):
    d = None
    try:
        d = datetime.fromtimestamp(microSec / 1000000)
    except:
        logger.warn('Cannot parse ' + str(microSec) + ' to date.')
    return d

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Read SQLite')
    parser.add_argument('--path')
    args = parser.parse_args()
    path = args.path if args.path else ''
    logger.setLevel(logging.INFO)
    print('<***********************Form History DATA*************************>')
    printData(readFormHistoryDb(path))
    print('<***********************Places DATA*************************>')
    printData(readPlacesDataDb(path))
    print('<***********************Cookies DATA*************************>')
    printData(readCookiesDataDb(path))

