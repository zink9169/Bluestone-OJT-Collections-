from abc import ABC, abstractmethod
from datetime import datetime

#  Vehicle Classes
class Vehicle(ABC):
    def __init__(self, license_plate: str):
        self.license_plate = license_plate
        self.entry_time = datetime.now()
        self.vehicle_type = None

    @abstractmethod
    def get_type(self):
        pass

class Bike(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate)
        self.vehicle_type = "Bike"

    def get_type(self):
        return self.vehicle_type

class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate)
        self.vehicle_type = "Car"

    def get_type(self):
        return self.vehicle_type

class Truck(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate)
        self.vehicle_type = "Truck"

    def get_type(self):
        return self.vehicle_type

# Parking Spot
class ParkingSpot:
    def __init__(self, spot_id: int, vehicle_type: str):
        self.spot_id = spot_id
        self.vehicle_type = vehicle_type
        self.is_available = True
        self.current_vehicle = None

    def assign_vehicle(self, vehicle: Vehicle):
        if self.is_available and vehicle.vehicle_type == self.vehicle_type:
            self.current_vehicle = vehicle
            self.is_available = False
            return True
        return False

    def remove_vehicle(self):
        if not self.is_available:
            vehicle = self.current_vehicle
            self.current_vehicle = None
            self.is_available = True
            return vehicle
        return None

# Ticket
class Ticket:
    def __init__(self, ticket_id: int, vehicle: Vehicle, spot_id: int):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot_id = spot_id
        self.entry_time = vehicle.entry_time
        self.exit_time = None
        self.fee = 0

    def calculate_fee(self, rate_per_hour: float):
        self.exit_time = datetime.now()
        hours = (self.exit_time - self.entry_time).total_seconds() / 3600
        self.fee = round(rate_per_hour * max(1, hours), 2)
        return self.fee

# Fee Calculator
class FeeCalculator:
    rates = {
        "Bike": 1.0,
        "Car": 2.0,
        "Truck": 3.5
    }

    @staticmethod
    def calculate(vehicle_type: str, hours: float):
        rate = FeeCalculator.rates.get(vehicle_type, 2.0)
        return round(rate * max(1, hours), 2)

# - Parking Lot -
class ParkingLot:
    def __init__(self):
        self.spots = []
        self.tickets = {}
        self.ticket_counter = 1

    def add_parking_spot(self, spot: ParkingSpot):
        self.spots.append(spot)

    def find_available_spot(self, vehicle_type: str):
        for spot in self.spots:
            if spot.is_available and spot.vehicle_type == vehicle_type:
                return spot
        return None

    def park_vehicle(self, vehicle: Vehicle):
        spot = self.find_available_spot(vehicle.vehicle_type)
        if not spot:
            print("No available spot for this vehicle type!")
            return None
        spot.assign_vehicle(vehicle)
        ticket = Ticket(self.ticket_counter, vehicle, spot.spot_id)
        self.tickets[self.ticket_counter] = ticket
        self.ticket_counter += 1
        print(f"Vehicle parked! Ticket ID: {ticket.ticket_id}")
        return ticket

    def release_vehicle(self, license_plate: str):
        for spot in self.spots:
            if spot.current_vehicle and spot.current_vehicle.license_plate == license_plate:
                vehicle = spot.remove_vehicle()
                for ticket_id, ticket in list(self.tickets.items()):
                    if ticket.vehicle.license_plate == license_plate:
                        fee = ticket.calculate_fee(FeeCalculator.rates[vehicle.vehicle_type])
                        self.tickets.pop(ticket_id)
                        print(f"Vehicle removed. Fee: ${fee}")
                        return fee
        print("Vehicle not found!")
        return None

    def generate_report(self):
        total_earnings = sum(ticket.fee for ticket in self.tickets.values())
        active_tickets = len(self.tickets)
        available_spots = sum(1 for s in self.spots if s.is_available)
        print(f"Total Spots: {len(self.spots)}")
        print(f"Available Spots: {available_spots}")
        print(f"Active Tickets: {active_tickets}")
        print(f"Total Earnings: ${total_earnings}")


# --Menu Functions -
def park_vehicle_menu(parking_lot: ParkingLot):
    print("Select Vehicle Type:")
    print("1. Bike")
    print("2. Car")
    print("3. Truck")
    choice = input("Enter choice (1-3): ")
    license_plate = input("Enter license plate: ")

    vehicle = None
    if choice == "1":
        vehicle = Bike(license_plate)
    elif choice == "2":
        vehicle = Car(license_plate)
    elif choice == "3":
        vehicle = Truck(license_plate)
    else:
        print("Invalid choice!")
        return
    parking_lot.park_vehicle(vehicle)


def remove_vehicle_menu(parking_lot: ParkingLot):
    license_plate = input("Enter license plate to remove: ")
    parking_lot.release_vehicle(license_plate)


def view_lot_status(parking_lot: ParkingLot):
    for spot in parking_lot.spots:
        status = "Available" if spot.is_available else f"Occupied by {spot.current_vehicle.license_plate}"
        print(f"Spot {spot.spot_id} ({spot.vehicle_type}): {status}")


def view_active_tickets(parking_lot: ParkingLot):
    if not parking_lot.tickets:
        print("No active tickets.")
        return
    for ticket_id, ticket in parking_lot.tickets.items():
        print(f"Ticket {ticket_id}: Vehicle {ticket.vehicle.license_plate}, Spot {ticket.spot_id}")


def view_earnings_report(parking_lot: ParkingLot):
    parking_lot.generate_report()


# -- Main Program --
def main():
    parking_lot = ParkingLot()
    # Create spots for demo
    for i in range(1, 6):  # 5 bike spots
        parking_lot.add_parking_spot(ParkingSpot(i, "Bike"))
    for i in range(6, 11):  # 5 car spots
        parking_lot.add_parking_spot(ParkingSpot(i, "Car"))
    for i in range(11, 14):  # 3 truck spots
        parking_lot.add_parking_spot(ParkingSpot(i, "Truck"))

    while True:
        print("\n--- Parking Lot Menu ---")
        print("1. Park Vehicle")
        print("2. Remove Vehicle")
        print("3. View Lot Status")
        print("4. View Active Tickets")
        print("5. View Earnings Report")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            park_vehicle_menu(parking_lot)
        elif choice == "2":
            remove_vehicle_menu(parking_lot)
        elif choice == "3":
            view_lot_status(parking_lot)
        elif choice == "4":
            view_active_tickets(parking_lot)
        elif choice == "5":
            view_earnings_report(parking_lot)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
