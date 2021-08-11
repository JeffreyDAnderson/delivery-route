from datetime import datetime, timedelta


# TIME COMPLEXITY: O(1)     --all getters/setters and adding methods run in O(1)--
# SPACE COMPLEXITY: the size of all the data combined
class Truck:
    def __init__(self, tid, time):
        self.tid = tid
        self.packages = []
        self.miles = 0.0
        self.time = time

    def getTid(self):
        return self.tid

    def getPackages(self):
        return self.packages

    def setPackages(self, packageList):
        self.packages = packageList

    def getMiles(self):
        return self.miles

    def setMiles(self, miles):
        self.miles = miles

    def getTime(self):
        return self.time.strftime('%I:%M %p')

    def setTime(self, time):
        self.time = time

    def addMiles(self, mileage):
        self.miles += float(mileage)

    def addTime(self, additionalTime):
        self.time = self.time + additionalTime
