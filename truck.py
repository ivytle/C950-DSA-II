import datetime

# currentLocation, packages.


# REQUIREMENTS:
# maximum of 16 packages
# ID of each package is unique
# Travel at avtg speed of 18mph (no gas/collisions)
# Leave hub earliest 8:00AM
# Day ends when all 40 are delivered
class Truck:
    def __init__(
        self,
        truckID,
        timeDelivered,
        packages,
        truckCapacity=16,
        speed=18,
        milesDriven=0,
        currentAddress="4001 South 700 East",
    ):
        self.truckCapacity = truckCapacity
        self.truckID = truckID
        self.packages = packages
        self.speed = speed
        self.milesDriven = milesDriven
        self.currentAddress = currentAddress

        self.departureTime = timeDelivered  # Used to Reference for Package.UpdateStatus
        self.timeDelivered = timeDelivered  # Default to truck departure time
        self.timeElapsed = datetime.timedelta(hours=0)

    def __str__(self):
        return (
            "truck capacity %s\n truckID %s\n packages %s\n milesDriven %s\n currentAddress  %s\n timeDelivered %s\n timeElapsed: %s\n departureTime: %s\n"
            % (
                self.truckCapacity,
                self.truckID,
                self.packages,
                self.milesDriven,
                self.currentAddress,
                self.timeDelivered,
                self.timeElapsed,
                self.departureTime,
            )
        )
