import datetime

# id, address, city, state, zip, deliveryTime, date, status.
class Package:
    def __init__(self, id, addr, city, state, zip, deadline, mass):
        self.id = id
        self.addr = addr
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.status = "IN HUB"
        self.deliveryTime = datetime.timedelta(hours=0)
        self.deliveryDuration = datetime.timedelta(hours=0)

    # Update status of package depending on H/M from User Input
    def updateStatus(self, departTime, h, m):
        """ 
        *** updateStatus ***
        
        Updates the delivery status of the package based on the current time and package constraints.

        Shows packages is still at the hub, in transit, or has been delivered based on the current 
        time the user inputs. Also it handles the address change for package ID '9' after a specific time.

        Args:
            departTime: The scheduled departure time of the package as a datetime.timedelta.
            h: Hour component of the current time, used to make the current time.
            m: Minute component of the current time, used to make the current time.

        Updates:
            status: Sets the package's status to 'IN HUB', 'EN ROUTE', or 'DELIVERED'.
            street, zip: Updates the address for package ID '9' based on the time.
        """


        currentTime = datetime.timedelta(hours=h, minutes=m)

        if self.deliveryTime == datetime.timedelta(hours=0) or currentTime < departTime:
            self.status = "IN HUB"
        elif self.deliveryTime > currentTime:
            self.status = "EN ROUTE"
        else:
            self.status = "DELIVERED"

        if self.id == "9":
            # package 9's address is updated at 10:20
            if currentTime > datetime.timedelta(hours=10, minutes=20):
                # Update address
                self.addr = "410 S State St"
                self.zip = "84111"
            else:
                # Return to default(wrong address) if userInput time is < 10:20
                self.addr = "300 State St"
                self.zip = "84103"

    def __str__(self):
        return (
            "ID: %s\nAddr: %s\nCity: %s\nState: %s\nZip: %s\nDeadline: %s\nMass %s\nStatus: %s\ndeliveryTime: %s\ndeliveryDuration: %s\n"
            % (
                self.id,
                self.addr,
                self.city,
                self.state,
                self.zip,
                self.deadline,
                self.mass,
                self.status,
                self.deliveryTime,
                self.deliveryDuration,
            )
        )
