# JEFFREY ANDERSON 001397587

from datetime import datetime, timedelta
import csv

from package import Package
from truck import Truck
from hashtable import HashTable


# Calling this function reads the provided  WGUPS Package File
# and hashes the package id's to place the packages into the
# hash table. Initialization of a HashTable allows for an array
# of any size to be created.

# TIME COMPLEXITY: O(N)     --runs with the number of rows in the csv file--
# SPACE COMPLEXITY: the number of rows of data * the size of a package object
def getDailyPackages(packageTable):
    with open('WGUPS Package File.csv', 'r') as package_file:
        csv_reader = csv.reader(package_file)
        line = 0
        status = 'at hub'
        note = ''
        for row in csv_reader:
            if line == 0 or line == 1:
                line += 1
                continue
            else:
                # check the CSV file special notes per package and assign packages accordingly
                if row[7] == 'Delayed on flight---will not arrive to depot until 9:05 am':
                    status = 'delayed'
                    note = row[7]
                elif row[7] == 'Can only be on truck 2':
                    note = 'truck 2'
                elif row[7] == '"Must be delivered with 13, 15"':
                    note = '13 15 19'
                elif row[7] == '"Must be delivered with 13, 19"':
                    note = '13 15 19'
                elif row[7] == '"Must be delivered with 15, 19"':
                    note = '13 15 19'
                elif row[7] == 'Wrong address listed':
                    note = 'wrong address'
                else:
                    note = row[7]

                address = cleanAddress(row[1])
                p = Package(row[0], address, row[2], row[3], row[4], row[5], row[6], note, status)
                packageTable.insert(p.getId(), p)

                status = 'at hub'
                note = ''
                line += 1


# this function goes though all the rows in the distance table
# and retrieves the values storing them in a 2d list

# TIME COMPLEXITY: O(N)     --runs with the number of rows in the csv file--
# SPACE COMPLEXITY: the number of rows in the file^2 then / 2 because only half the values are stored
def getDeliveryDistances(addresses, distances):
    with open('WGUPS Distance Table.csv', 'r') as distance_file:
        csv_reader = csv.reader(distance_file)
        line = 0    # to track which row of csv is being used
        index = 0   # to track the row number of the address to store as the dict value
        first = 2   # distances always start at row[2]
        last = 2    # number of distances grow by 1 for each subsequent row of the csv file
        i = 2       # to iterate through each column of each row without accessing out of bounds data
        # temporary list of distances to be built per row of the csv file and appended to the distances parameter
        csvDistance = []

        for row in csv_reader:
            # this is to skip the header rows of the file
            if line < 7:
                line += 1
                continue
            else:
                keyaddr = cleanAddress(row[1])
                if line == 7:
                    addresses[keyaddr] = index
                    line += 1
                else:
                    addresses[keyaddr] = index    # trim the zip code off the address and store it as the key
                index += 1
                while i <= last:
                    csvDistance.append(row[i])
                    i += 1
                distances.append(csvDistance)
                csvDistance = []
                last += 1
                i = first


# a greedy algorithm to determine which packages to load
# onto each truck. packages will be chosen by shortest
# distance to next delivery from the packages that still
# need to be assigned to a route

# TIME COMPLEXITY: O(N)     --loops through the number of objects to sort up to 16 times: 16*n--
# SPACE COMPLEXITY: 8 variables to hold temp data
def sortByShortestDistance(currentAddress, currentRoute, sortFrom):
    currLoc = currentAddress
    while len(currentRoute) < 16 and len(sortFrom) > 0:
        nextLoc = sortFrom[0].getAddress()
        closest = distanceBetween(currLoc, nextLoc)
        for i in sortFrom:
            if distanceBetween(currLoc, i.getAddress()) <= closest:
                nextStop = i
                index = sortFrom.index(i)
                closest = distanceBetween(currLoc, i.getAddress())
                nextLoc = i.getAddress()
        currentRoute.append(nextStop)
        sortFrom.pop(index)
        currLoc = nextLoc
        nextStop.setStatus('en route')


# this function builds delivery routes for the truck passed in by
# searching through the req_packages and sorting them by priority
# of when the deadline is. when a package with a deadline is found
# and added to the route or priorityRoute then the remaining packages
# are searched for other packages that are available to deliver
# to the same address. When the lists are assembled then they are passed
# to the sort function to be sorted with a greedy algorithm (nearest neighbor)

# TIME COMPLEXITY: O(N^2)       --loops through packages to pick ones with delivery times then again to pick the same delivery addresses--
# SPACE COMPLEXITY: nothing is added. data is moved from one list to another
def buildDeliveryRoute(route, req_packages, rest_packages):
    priorityRoute = []
    eodRoute = []

    # find priority packages and assign to route or priorityRoute
    # when a package is assigned look for other packages that share the same address
    for i in req_packages:
        if i.getDeadline() == '9:00 AM':
            route.append(i)
            for j in rest_packages:
                if i.getAddress() == j.getAddress():
                    route.append(j)
        elif i.getDeadline() == '10:30 AM':
            priorityRoute.append(i)
            for j in rest_packages:
                if i.getAddress() == j.getAddress():
                    priorityRoute.append(j)
        else:
            eodRoute.append(i)

    if len(route) == 0:
        currLoc = 'HUB'
    else:
        currLoc = route[-1].getAddress()

    if len(priorityRoute) > 0:
        sortByShortestDistance(currLoc, route, priorityRoute)
        sortByShortestDistance(route[-1].getAddress(), route, eodRoute)
    else:
        sortByShortestDistance(currLoc, route, eodRoute)


# this function loops through a trucks set delivery route and
# 'delivers' the packages in order. mileage is determined and
# added to the trucks total. delivery time is set based on the
# amount of time it took to travel from previous location to
# current location

# TIME COMPLEXITY: O(1)     --runs equal to the number of packages in the truck, max of 16--
# SPACE COMPLEXITY: data is altered in a package object but nothing is added
def deliverPackages(truck):
    currentLocation = 'HUB'
    nextLocation = ''
    for package in truck.getPackages():
        nextLocation = package.getAddress()
        travelDistance = distanceBetween(currentLocation, nextLocation)
        truck.addMiles(travelDistance)
        truck.addTime(timedelta(minutes=(float(travelDistance) / float(MPS))))
        package.setStatus('delivered')
        package.setDelivered(truck.getTime())
        currentLocation = nextLocation


# this function is to make the program more reliable. It
# will clean addresses pulled in from the distance table
# or package file and normalize data points. Zip codes
# will also be removed leaving a plain street address. For
# example 'North' in one of the files will become 'N'

# TIME COMPLEXITY: O(1)     --only conditionals and assignments are included--
# SPACE COMPLEXITY: data is only altered
def cleanAddress(address):
    if address.find('North'):
        address = address.replace('North', 'N')
    if address.find('East'):
        address = address.replace('East', 'E')
    if address.find('South'):
        address = address.replace('South', 'S')
    if address.find('West'):
        address = address.replace('West', 'W')
    if address.endswith(')'):
        address = address[:-7]
    address = address.strip()
    return address


# given 2 addresses this function checks the distance
# table and returns the value located there

# TIME COMPLEXITY: O(1)     --checks the distance table with given indexes--
# SPACE COMPLEXITY: no data is added
def distanceBetween(fromAdd, toAdd):
    fromIndex = deliveryAddresses[fromAdd]
    toIndex = deliveryAddresses[toAdd]

    try:
        if fromIndex >= toIndex:
            return deliveryDistances[fromIndex][toIndex]
        else:
            return deliveryDistances[toIndex][fromIndex]
    except IndexError:
        print('Bad Index in distanceBetween()')


# checks all the remaining packages to see which ones
# have a status of 'at hub' and adds them to a list

# TIME COMPLEXITY: O(N)     --runs for each item in a list of packages--
# SPACE COMPLEXITY: a list is built from an existing list
def getAvailable():
    availablePackages.clear()
    for i in remainingPackages:
        if i.getStatus() == 'at hub':
            availablePackages.append(i)


if __name__ == '__main__':
    # create necessary elements: 2 trucks, hashtable, distance chart, address dict, and get packages
    truck1 = Truck(1, datetime(2020, 1, 1, 8))
    truck2 = Truck(2, datetime(2020, 1, 1, 9, 5))
    truck3 = Truck(3, datetime(2020, 1, 1, 11, 30))

    deliveryAddresses = {}      # dictionary of indexes for the distance chart; key is address: value is index
    deliveryDistances = []      # list of lists for distances between addresses, values between are symmetric
    getDeliveryDistances(deliveryAddresses, deliveryDistances)

    packages = HashTable()
    getDailyPackages(packages)

    # list of packages that will be on each truck
    t1packages = []
    t2packages = []
    t3packages = []

    # each trucks packages in order by nearest neighbor
    t1route = []
    t2route = []
    t3route = []

    TIME = datetime(2020, 1, 1, 8)     # start date and time for deliveries
    MPS = 18 / 60       # mph = 18 / 60 minutes per hour to get speed in miles per minute

    # update address for package 9
    (packages.retrieve(str(9))).setAddress('410 S State St')

    try:
        allPackages = []
        remainingPackages = []
        availablePackages = []
        for i in range(1, 41):
            allPackages.append(packages.retrieve(str(i)))

        for i in allPackages:
            if i.getId() in ('1', '13', '14', '15', '16', '19', '20', '34', '40', '29'):
                t1packages.append(i)
            elif i.getId() in ('3', '6', '8', '18', '25', '28', '32', '36', '38', '30', '31', '37'):
                t2packages.append(i)
            elif i.getId() in ('5', '9'):
                t3packages.append(i)
            else:
                remainingPackages.append(i)

        #  TRUCK 1
        getAvailable()

        buildDeliveryRoute(t1route, t1packages, availablePackages)
        buildDeliveryRoute(t1route, availablePackages, availablePackages)
        truck1.setPackages(t1route)
        deliverPackages(truck1)

        # TRUCK 2
        getAvailable()

        buildDeliveryRoute(t2route, t2packages, availablePackages)
        buildDeliveryRoute(t2route, availablePackages, availablePackages)
        truck2.setPackages(t2route)
        deliverPackages(truck2)

        # TRUCK 3
        getAvailable()

        buildDeliveryRoute(t3route, t3packages, availablePackages)
        buildDeliveryRoute(t3route, availablePackages, availablePackages)
        truck3.setPackages(t3route)
        deliverPackages(truck3)

    except KeyError:
        print('Something wrong')

    selection = 1
    while selection != 0:
        print('MENU\n')
        print('1: Get a specific packages information by ID')
        print('2: Get all package information at a specific time')
        print('0: Exit program\n')
        selection = int(input('Enter a menu selection number: '))

        if selection == 1:
            print('\nPACKAGE INFORMATION\n')
            package = int(input('Enter a Package ID: '))
            packages.retrieve(str(package)).printInfo()
            input('\nPress enter to continue...')

        elif selection == 2:
            print('\nPACKAGE OVERVIEW\n')
            time = input('Enter a time to view Packages (Ex: 09:30 AM): ')
            for i in range(1, 41):
                p = packages.retrieve(str(i))
                if time < '08:00 AM':
                    p.printUpdate('at hub')
                elif time < '09:05 AM':
                    if p in t2route or p in t3route:
                        p.printUpdate('at hub')
                    elif p.getDelivered() > time:
                        p.printUpdate('en route')
                    else:
                        p.printInfo()
                elif time < '11:30 AM':
                    if p in t3route:
                        p.printUpdate('at hub')
                    elif p.getDelivered() > time:
                        p.printUpdate('en route')
                    else:
                        p.printInfo()
                elif p.getDelivered() > time:
                    p.printUpdate('en route')
                else:
                    p.printInfo()
            print()
            print('Total miles traveled: {:.2f}'.format(truck1.getMiles() + truck2.getMiles() + truck3.getMiles()))
            print()
            input('Press enter to continue...')
