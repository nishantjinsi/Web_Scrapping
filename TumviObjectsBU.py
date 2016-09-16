__author__ = 'sbeltran'

from datetime import datetime


class Item(object):

    name = ""


    def __init__(self, name):
        self.id = id
        self.name = name

    def __str__(self):
        return str([ self.name])


class Menu(object):
    validDate = datetime
    mealTime = ""
    stationItems = {}

    def __init__(self, validDate, mealTime, stationItems):
        self.validDate = validDate
        self.mealTime = mealTime
        self.stationItems = stationItems

    def __str__(self):
        return str([self.validDate, self.mealTime, self.stationItems])


