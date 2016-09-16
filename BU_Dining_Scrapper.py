from lxml import html
import requests
from datetime import datetime, timedelta
import time
import re

from lxml.html import tostring

from TumviObjectsBU import  Menu, Item
import multiprocessing as mp


def geturls():
    # baseURLS = {"Brower+Commons": "http://menuportal.dining.rutgers.edu/foodpro/pickmenu.asp?sName=Rutgers+University+Dining&locationNum=03&locationName=Livingston+Dining+Commons"}
    baseURLS = {
        "Brower+Commons": "http://www.bu.edu/dining/where-to-eat/residence-dining/warren-towers/menu/?dsd="}
    # Get next 7 days from today
    date_list = []
    for i in range(0, 7):
        # date_list.append((datetime.today() + timedelta(days=i)).strftime('%m/%d/%Y'))
        date_list.append(datetime.today() + timedelta(days=i))
    fullURLs = {}
    for name in baseURLS:
        # Add all 7 days to base URL for a location using list and then add it to a new dictionary with tuple date,url
        tl = []
        for date in date_list:
            datestr = date.strftime('%m/%d/%Y')
            if (datestr[0] is '0'):
                datestr = datestr[1:]
            tl.append((date, (baseURLS[name] + "&dtdate=" + datestr)))
        fullURLs[name] = tl

    return fullURLs

def getMenuItems(tree):
    menuItems = []
    stationItems = {}
    stationTag = None
    # HTMLelement tree of just the menu portion of the page
    menu = tree.xpath('//*[@class="dining-menu-meals"]')
    print len(menu)
    #print tostring(menu[0])
    menuItems = []
    stationItems = {}
    stationTag = None
    for child in menu[0]:
        if child.find_class('item-menu-name'):

            iName = child.find_class('item-menu-name')[0].text_content()
            item = Item( name=iName)
            menuItems.append(item)

    if menuItems: stationItems[stationTag] = menuItems
    #print stationItems
    return stationItems
            #nutlabel = getNutritionData(iID, iPortionSize)
    #print tostring(menu[1])



def getMealTimeMenu(data):
    name = mp.current_process().name
    st = time.time()
    print name, ': Starting -'
    page = requests.get(data[0] + "&mealName=" + data[1])
    station_items = getMenuItems(html.fromstring(page.text))
    menu = Menu(validDate=data[3], mealTime=data[4], stationItems=station_items)
    print menu
    print station_items
    print name, ': Exiting ',(time.time() - st)
    return (data[2], menu)
pool = mp.Pool(processes=1)
processes = []



def getDiningData(fullURLs):
    # Key is dining hall name, urlList is the [(dateValid, url),...]
    all_menus = []
    for key, urlList in fullURLs.iteritems():
        # urTup is a split between a dateValid and the baseURL with a date
        for urTup in urlList:
            valid = urTup[0]
            url = urTup[1]

            page = requests.get(url)



            tree = html.fromstring(page.text)

            # Get Meal Times avaiable at this location for day
            meal_times = tree.xpath(
                '//*[@id="mealnav"]/ul/li/a/text() ')

            for m in meal_times:
                if str(m) == 'Breakfast':
                    data = [url, 'Breakfast', key, valid, 'b']
                    processes.append(pool.apply_async(getMealTimeMenu, args=(data,)))
                elif str(m) == 'Lunch':
                    data = [url, 'Lunch', key, valid, 'l']
                    processes.append(pool.apply_async(getMealTimeMenu, args=(data,)))

                elif str(m) == 'Dinner':
                    data = [url, 'Dinner', key, valid, 'd']
                    processes.append(pool.apply_async(getMealTimeMenu, args=(data,)))

    all_menus = [p.get() for p in processes]

    if all_menus:
        return all_menus
    return None

def printMenuData():
    start_time = time.time()
    urls = geturls()
    data = getDiningData(urls)
    print data
    print("--- %s seconds ---" % (time.time() - start_time))


# Returns a list of Menu Objects
printMenuData()