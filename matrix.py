import datetime


# Use data from CSV to load trucks and calculate optimal delivery routes
class Matrix:
    # Constructor Initializing Variables to contain CSV data
    def __init__(
        self,
        addressData,
        distanceData,
        hashTable,
    ):
        self.addressData = addressData
        self.distanceData = distanceData
        self.hashTable = hashTable

    # getter function for addressID
    def getAddressID(self, addr):
        return self.addressData[addr][0]

    # getter function for addressName
    def getAddressName(self, addr):
        return self.addressData[addr][1]

    # Search and compare addresses to find distance between two points
    def distanceBetween(self, addr1, addr2):
        id1 = self.getAddressID(addr1)
        id2 = self.getAddressID(addr2)
        diff = self.distanceData[id2][id1]
        if diff == "":
            diff = self.distanceData[id1][id2]

        # print("distance between %i and %i is %s" % (id1, id2, diff))
        return float(diff)

    # Load truck packages
    def loadPackage(self, enqueue, truck):
        # Iterates through each package ID in truck's package list
        for ID in truck.packages:
            # Gets package object by its ID from hashtable
            # Appends to the enqueue list
            enqueue.append(self.hashTable.search(ID))

    # Helper function to print Deliveries
    def printToDeliverHelper(self, arr):
        for x in arr:
            print(x)
            # print(x.id)

    # Nearest Neighbor Alogrithm
    def deliver(self, truck):
        """
        Implements the Nearest Neighbor Algorithm to find best route to deliver packages

        Finds and delivers the nearest package until all packages are delivered.
        Delivery status, package list, and truck mileage are updated on each delivery.

        Args:
            truck: The truck object perform the deliveries
                   Contains initial package list and state.

        Process:
            1. Initialize the delivery list and load packages from the truck.
            2. Clear the initial list of packages from the truck 
            3. Finds the nearest package and delivers it until all packages are delivered.
        
        """        
        
        # load packages
        toDeliver = [] # Initialize a list, keeps track of packages that need to be delivered by truck
        self.loadPackage(toDeliver, truck) # Load all packages assigned to truck into toDeliver List
        truck.packages.clear() # Clears Initial list of packages from trucks after loading into toDeliver

        # Continue delivering packages until no more is left
        while len(toDeliver) > 0:
            # Initialize variables to find the closest next package 
            nextAddressDist = 9999  # Start with a high number to ensure any actual distance will be less
            nextPackage = None # Placeholder for the next package to be delivered

            # Find Shortest path to neighboring addresses
            # Iterate through each package still to be delivered
            for package in toDeliver:
                # Calculate distance from current truck location to package address
                destDiff = self.distanceBetween(truck.currentAddress, package.addr) 
                # print(truck.currentAddress, " --> ", package.addr, " : ", destDiff)
                
                # If distsance is the shortest, update to make this next delivery location
                if destDiff <= nextAddressDist:
                    nextAddressDist = destDiff
                    nextPackage = package

            # simulate truck delivery
            # If a next package to deliver is found
            if nextPackage:
                # update arrays
                truck.packages.append(nextPackage.id) # Add this package ID back to the truck's package list
                toDeliver.remove(nextPackage) # Remove the package from the list still to be delivered
                
                # update truck member functions
                truck.milesDriven += nextAddressDist # Updates truck's total milage for this delivery
                truck.currentAddress = nextPackage.addr # Set truck's current address to the address of the package just delivered

                # Calculate the time taken for segment of trip
                transitTime = datetime.timedelta(hours=nextAddressDist / truck.speed) # Calculations based on distance and speed
                # print("transitTime: ", transitTime)

                # Update total time the truck has been in transit and the time since it left the hub
                truck.timeElapsed += transitTime
                truck.timeDelivered += transitTime

                # save time values in package for UI datalookup functions
                nextPackage.deliveryTime = truck.timeDelivered
                nextPackage.deliveryDuration = truck.timeElapsed
                # Update status to DELIVERED and pass the truck object
