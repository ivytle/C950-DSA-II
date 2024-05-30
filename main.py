# STUDENT ID: 010681661
# C950: Ivy Le

import csv
import datetime
from hashtable import HashTable
from package import Package
from truck import Truck
from matrix import Matrix


# Convert Package CSV data to hash_table
def decodePackageCSV(hash_table, fileName):
    with open(fileName, mode="r", newline="") as package_file:
        csv_reader = csv.reader(package_file)
        for row in csv_reader:
            packageId = int(row[0])
            package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            hash_table.insert(packageId, package)


# converts Distance CSV data to 2d Adjacency Matrix
def decodeDistanceCSV(fileName):
    matrix = []
    with open(fileName, mode="r", newline="") as package_file:
        csv_reader = csv.reader(package_file)
        for row in csv_reader:
            matrix.append(row)
    return matrix


# Converts Address CSV to dictionary
# Dictionary Structure
# map[Address] = (packageIndex, packageName)
def decodeAddressCSV(fileName):
    addrMap = {}
    with open(fileName, mode="r", newline="") as package_file:
        csv_reader = csv.reader(package_file)
        for row in csv_reader:
            addrMap[row[2]] = (int(row[0]), row[1])
    return addrMap


# -- UI FUNCTIONS --


# Color terminal outputs
class colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    ENDC = "\033[0m"


# Get Time For UI Reports
def timeInputUI():
    while True:
        inputTime = input("Input Time HH:MM ")
        if len(inputTime) != 5:
            print(
                colors.WARNING + "Invalid input format. Please try again" + colors.ENDC
            )
            continue
        try:
            (h, m) = inputTime.split(":")
            h, m = int(h), int(m)
            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError
            return (inputTime, h, m)
        except ValueError:
            print(colors.WARNING + "Invalid Time. Please try again" + colors.ENDC)


# Formatting Output
def printPackageUIFormat(truckId, package):
    fullAddress = (
        package.addr + " " + package.city + ", " + package.state + " " + package.zip
    )
    print(truckId + " - " + colors.OKBLUE + "Package %s : " % (package.id) + colors.ENDC, end="")
    if package.status == "DELIVERED":
        print(
            colors.OKGREEN + "\tStatus: %s\n" % (package.status) + colors.ENDC, end=""
        )
        print("\tDelivered at: %s" % (package.deliveryTime), end="")
        print("\tTotal Transit Time: %s\n" % (package.deliveryDuration), end="")
    else:
        print("\tStatus: %s\n" % (package.status), end="")
    print("\tDue: %s \n" % (package.deadline), end="")
    print("\tWeight: %s \n" % (package.mass), end="")
    print("\tDestination: %s\n" % (fullAddress), end="")
    print()

"""
Resubmission for task 2, checks to see if the delivery time is before the due time of delivery

def printPackageUIFormat(truckId, package):
    # Create a full address string from the package attributes
    fullAddress = (
        package.addr + " " + package.city + ", " + package.state + " " + package.zip
    )
    # Print the truck ID and package ID with coloring for the package part
    print(truckId + " - " + colors.OKBLUE + "Package %s : " % (package.id) + colors.ENDC, end="")
    
    # Check the delivery status of the package and print accordingly
    if package.status == "DELIVERED":
        print(
            colors.OKGREEN + "\tStatus: %s\n" % (package.status) + colors.ENDC, end=""
        )
        print("\tDelivered at: %s" % (package.deliveryTime), end="")
        print("\tTotal Transit Time: %s\n" % (package.deliveryDuration), end="")
    else:
        print("\tStatus: %s\n" % (package.status), end="")
    
    # Print the package deadline
    print("\tDue: %s \n" % (package.deadline), end="")
    
    # Additional handling for deadline timing to determine punctuality
    if package.deadline != "EOD":
        deadlineArchive = package.deadline
        package.deadline = package.deadline.split()
        del package.deadline[-1]
        package.deadline = ''.join(package.deadline)
        package.deadline = package.deadline.split(":")
        htime = int(package.deadline[0])
        mtime = int(package.deadline[1])
        deadlineTimeValue = datetime.timedelta(hours=htime, minutes=mtime)
        print("DEADLINE VALUE ", deadlineTimeValue)
        print("DELIVERY VALUE ", package.deliveryTime)
        if (deadlineTimeValue < package.deliveryTime):
            print(colors.WARNING + "\tNOT ON TIME!!!!!!!!" + colors.ENDC)
        package.deadline = deadlineArchive

    # Print the package weight and destination
    print("\tWeight: %s \n" % (package.mass), end="")
    print("\tDestination: %s\n" % (fullAddress), end="")
    print()  # Adds an extra newline for better separation of entries
"""

# Prints route that specific truck took to deliver packages
def printDeliveryRoute(ID, depart, packages, ht):
    print("=====================")
    print(colors.HEADER)
    print("%s Delivery Route" % (ID))
    print(colors.ENDC)
    print("%s departed from hub at %s\n" % (ID, depart))
    print("Hub --> ", end="")
    for package in packages:
        address = ht.search(int(package)).addr
        pid = ht.search(int(package)).id
        print("ID: ", pid, " & ", address)
        print(address, " --> ", end="")
    print("Hub")
    print("=====================")


# output packages for each truck
def printTruckPackage(truckID, departureTime, packages, ht, time=None):
    if time is None:
        timeTuple = timeInputUI()
    else:
        timeTuple = time
    print("=====================")
    print(colors.HEADER)
    print("Truck Packages Report")
    print("Time: ", timeTuple[0], "\n")
    print("Truck: %s" % (truckID))
    print(colors.ENDC)
    for package in packages:
        p = ht.search(int(package))
        p.updateStatus(departureTime, timeTuple[1], timeTuple[2])
        printPackageUIFormat(truckID, p)
    print("=====================")


# Prints All Package Information at x Time
def printAllPackages(t1, t2, t3, ht):
    timeTuple = timeInputUI()
    print("=====================")
    print(colors.HEADER)
    print("All Packages Report")
    print(colors.ENDC)
    printTruckPackage(t1.truckID, t1.departureTime, t1.packages, ht, timeTuple)
    printTruckPackage(t2.truckID, t2.departureTime, t2.packages, ht, timeTuple)
    printTruckPackage(t3.truckID, t3.departureTime, t3.packages, ht, timeTuple)
    print("=====================")


# Prints X Package at Y time
def printSinglePackage(truckId, departureTime, packageID, ht):
    package = ht.search(int(packageID)) # Calls the search function to retrieve the package based on its ID
    timeTuple = timeInputUI()  # get a specific time input from the user
    print("=====================")
    print(colors.HEADER)
    print("Package %s Report" % (package.id))
    print("Time: ", timeTuple[0], "\n")
    print(colors.ENDC)
    package.updateStatus(departureTime, timeTuple[1], timeTuple[2])
    printPackageUIFormat(truckId, package) #Prints out package details
    print("=====================")


# Return mileage between three trucks
def getTotalMileage(truck1, truck2, truck3):
    return truck1.milesDriven + truck2.milesDriven + truck3.milesDriven


# Helper function. User Input truck
def selectTruckUI(truck1, truck2, truck3):
    flag = True
    truckReport = truck1
    while flag:
        truckNumber = input("Which Truck? (1,2,3) ")
        if truckNumber == "1":
            truckReport = truck1
            flag = False
        elif truckNumber == "2":
            truckReport = truck2
            flag = False
        elif truckNumber == "3":
            truckReport = truck3
            flag = False
        else:
            print(colors.WARNING + "Invalid Response. Please Try Again\n" + colors.ENDC)
    return truckReport


# --- END of UI Functions ---


# Simulate Truck Deliveries with given CSV data
def main():
    """
    Main function: the delivery process for all packages using three trucks.

    Function manually loads trucks with the a set delivery time & respected packages, grouped my their notes. 
    Takes the distance and address data from CSV files, uses the data to deliver the packages. 
    Organizes loaded data into data structure and delivers the package using the Matrix class's delivery method

    Process:
        1. Truck Initialization: Each truck is initialized with a set of packages and a specific departure time.
        2. Data Loading: Loads CSV files to their data structures
        3. Delivery Execution: Matrix class to calculate and execute the delivery routes for each truck.
    
    """

    # Manually Load and Initialize Trucks
    # May 9th, 2024 - Corrected packages loaded into trucks for attempt 2
    truck1 = Truck(
        "Truck1",
        datetime.timedelta(hours=8),
        [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40],
    )
    truck2 = Truck(
        "Truck2",
        datetime.timedelta(hours=9, minutes=5),
        [3, 6, 18, 25, 27, 28, 32, 33, 35, 36, 38, 39]
    )
    truck3 = Truck(
        "Truck3",
        datetime.timedelta(hours=10, minutes=20),
        [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 19, 21, 22, 23, 24, 26],
    )

    # CSV file paths
    packageFileName = "CSVFiles/packageCSV.csv"
    distanceFileName = "CSVFiles/distanceCSV.csv"
    addressFileName = "CSVFiles/addressCSV.csv"

    # Decode CSV files into hashtable, matrix, and dictionary
    ht = HashTable()
    decodePackageCSV(ht, packageFileName)
    distanceData = decodeDistanceCSV(distanceFileName)
    addressDict = decodeAddressCSV(addressFileName)
    map = Matrix(
        addressDict,
        distanceData,
        ht,
    )

    # Make Truck Deliveries
    # Execute deliveries for each truck based on their calculated routes 

    map.deliver(truck1)
    map.deliver(truck2)
    map.deliver(truck3)

    # --- User UI ---

    print("Welcome to the WGU Parcel Routing Service!\n")
    flag = True
    while flag:
        print(colors.OKBLUE)
        print("""Enter one of the following option #'s to proceed:

        (1) Single Package Report
        (2) Full Package Report
        (3) Truck Package Report
        (4) Single Truck Mileage
        (5) Total Truck Mileage
        (6) Delivery Route
        (X) Exit
              """)
        userInput = input()
        print(colors.ENDC)

        # Ends the loop and exits the program if the user inputs 'X' or 'x'
        if userInput == "X" or userInput == "x":
            flag = False
       
        # Displays the package report for the specific package at the specific time
        elif userInput == "1":
            packageReport = input("Package ID #? (1-40) ") # Prompt user for a package ID number from 1 to 40 inclusive
            if int(packageReport) < 1 or int(packageReport) > 40:  # Error if ID input is out of the valid range
                print(
                    colors.WARNING
                    + "Invalid Response. Please Try Again\n"
                    + colors.ENDC
                )
            
             # Determine which truck has the package and get its departure time
            if packageReport in truck1.packages:
                departureTime = truck1.departureTime
                tid = truck1.truckID
            elif packageReport in truck2.packages:
                departureTime = truck2.departureTime
                tid = truck2.truckID
            elif packageReport in truck3.packages:
                departureTime = truck3.departureTime
                tid = truck3.truckID
            else:
                print(colors.WARNING + "Package not Found" + colors.ENDC)
                continue
            printSinglePackage(tid, departureTime, packageReport, ht)
        
        #Displays all package details for all trucks
        elif userInput == "2":
            printAllPackages(truck1, truck2, truck3, ht)
        
        # Displays selected truck's packages and details
        elif userInput == "3":
            truckReport = selectTruckUI(truck1, truck2, truck3) 
            # Prints details for the selected truck's packages
            printTruckPackage(
                truckReport.truckID, truckReport.departureTime, truckReport.packages, ht
            )

        # Displays the total milage of the selected truck
        elif userInput == "4":
            truckReport = selectTruckUI(truck1, truck2, truck3)
            print(
                colors.HEADER
                + "%s's total Mileage: %.2f\n"
                % (truckReport.truckID, truckReport.milesDriven)
                + colors.ENDC
            )

        # Calculates and displays the total milage for all trucks
        elif userInput == "5":
            print(
                colors.HEADER
                + "Total Mileage: %.2f" % (getTotalMileage(truck1, truck2, truck3))
                + colors.ENDC
            )
        
        # Delivery route for the selected truck
        elif userInput == "6":
            truckReport = selectTruckUI(truck1, truck2, truck3)
            printDeliveryRoute(
                truckReport.truckID, truckReport.departureTime, truckReport.packages, ht
            )
        
        # Handles any inputs that do not match the expected commands listed
        else:
            print(colors.WARNING + "Invalid Response. Please Try Again\n" + colors.ENDC)


if __name__ == "__main__":
    main()
