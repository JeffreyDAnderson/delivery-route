# TIME COMPLEXITY: O(1)     --all getters/setters and retrieval methods run in O(1)--
# SPACE COMPLEXITY: the size of all the data combined
class Package:
    def __init__(self, pid, address, city, state, zipcode, deadline, weight, note, status, delivered=''):
        self.pid = pid
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.status = status
        self.delivered = delivered

    def getId(self):
        return self.pid

    def setId(self, pid):
        self.pid = pid

    def getAddress(self):
        return self.address

    def setAddress(self, address):
        self.address = address

    def getCity(self):
        return self.city

    def setCity(self, city):
        self.city = city

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getZipcode(self):
        return self.zipcode

    def setZipcode(self, zipcode):
        self.zipcode = zipcode

    def getDeadline(self):
        return self.deadline

    def setDeadline(self, deadline):
        self.deadline = deadline

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def getNote(self):
        return self.note

    def setNote(self, note):
        self.note = note

    # STATUSES
    # at hub: ready to be assigned to a truck
    # delayed: not available to assign to a truck yet
    # en route: assigned to a truck but not delivered yet
    # delivered: successfully delivered
    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def getDelivered(self):
        return self.delivered

    def setDelivered(self, time):
        self.delivered = time

    def printInfo(self):
        print('{: <4} {: <40} {: <12} {: <20} {: <8} {: <5} {: <12} {: <12}'
              .format(self.pid, self.address, self.deadline, self.city, self.zipcode, self.weight, self.status, self.delivered))

    def printUpdate(self, stat):
        print('{: <4} {: <40} {: <12} {: <20} {: <8} {: <5} {: <12}'
              .format(self.pid, self.address, self.deadline, self.city, self.zipcode, self.weight, stat))