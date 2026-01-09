from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Vehicle(ABC):

    def __init__(self, license_plate, entry_time=None):
        self.license_plate = license_plate
        self.entry_time = entry_time or datetime.now()

    @property
    #Vehicle class ကို object မဖန်တီးနိုင်/ Subclass တွေမှာ မဖြစ်မနေ implement လုပ်ရမယ်
    @abstractmethod
    def vehicle_type(self):
        pass

#inheritance
class Bike(Vehicle):
    @property
    def vehicle_type(self):
        return "Bike"
#inheritance
class Car(Vehicle):
    @property
    def vehicle_type(self):
        return "Car"
#inheritance
class Truck(Vehicle):
    @property
    def vehicle_type(self):
        return "Truck"

#Encapsulation (Data + Behavior ကို စုထား)
class ParkingSpot:
    def __init__(self, spot_id, vehicle_type):
        self.spot_id = spot_id
        #Polymorphism (Method တူ၊ Result မတူ)
        self.vehicle_type = vehicle_type
        self.is_available = True
        self.current_vehicle = None

    def assign_vehicle(self, vehicle):
        if self.is_available and vehicle.vehicle_type == self.vehicle_type:
            self.current_vehicle = vehicle
            self.is_available = False
            return True
        return False

    def remove_vehicle(self):
        vehicle = self.current_vehicle
        self.current_vehicle = None
        self.is_available = True
        return vehicle


#Object Collaboration (Class အချင်းချင်းပူးပေါင်း)
#Ticket က Vehicle ကို သိ Spot ကို သိ Fee ကို တွက်
class Ticket:
    def __init__(self, ticket_id, vehicle, spot_id):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot_id = spot_id
        self.entry_time = vehicle.entry_time
        self.exit_time = None
        self.fee = 0

    def calculate_fee(self, fee_calculator):
        if not self.exit_time:
            self.exit_time = datetime.now()
        hours = (self.exit_time - self.entry_time).total_seconds() / 3600
        self.fee = fee_calculator.calculate(self.vehicle.vehicle_type, hours)
        return self.fee

#Fee calculation logic ကို သီးခြား class ထဲခွဲထား
class FeeCalculator:
    rates = {"Bike": 1, "Car": 2, "Truck": 3}  # per hour

    def calculate(self, vehicle_type, hours):
        return round(hours * self.rates.get(vehicle_type, 2), 2)

#Aggregation (HAS-A Relationship)
class ParkingLot:
    def __init__(self):
        self.spots = []
        self.tickets = {}  # active tickets
        self.earnings = 0
        self.fee_calculator = FeeCalculator()

    def add_spot(self, spot):
        self.spots.append(spot)

    def find_available_spot(self, vehicle_type):
        for spot in self.spots:
            if spot.is_available and spot.vehicle_type == vehicle_type:
                return spot
        return None

    def park_vehicle(self, vehicle):
        spot = self.find_available_spot(vehicle.vehicle_type)
        if spot:
            spot.assign_vehicle(vehicle)
            ticket_id = f"T{len(self.tickets)+1:03d}"
            ticket = Ticket(ticket_id, vehicle, spot.spot_id)
            self.tickets[vehicle.license_plate] = ticket
            print(f"Vehicle parked at spot {spot.spot_id}. Ticket ID: {ticket_id}")
        else:
            print("No available spot for this vehicle type.")

    def release_vehicle(self, license_plate):
        ticket = self.tickets.get(license_plate)
        if ticket:
            spot = next(s for s in self.spots if s.spot_id == ticket.spot_id)
            vehicle = spot.remove_vehicle()
            fee = ticket.calculate_fee(self.fee_calculator)
            self.earnings += fee
            print(f"Vehicle {vehicle.license_plate} exited. Fee: ${fee}")
            del self.tickets[license_plate]
        else:
            print("No active ticket found for this license plate.")

    def generate_report(self):
        print("\n--- Parking Lot Status ---")
        for spot in self.spots:
            status = "Available" if spot.is_available else f"Occupied by {spot.current_vehicle.license_plate}"
            print(f"Spot {spot.spot_id} ({spot.vehicle_type}): {status}")
        print("\n--- Active Tickets ---")
        for t in self.tickets.values():
            print(f"Ticket {t.ticket_id}: {t.vehicle.vehicle_type} {t.vehicle.license_plate} at Spot {t.spot_id}")
        print(f"\nTotal Earnings: ${self.earnings}\n")


def main_menu():
    parking_lot = ParkingLot()

    # Add some spots
    for i in range(1, 6):
        parking_lot.add_spot(ParkingSpot(f"B{i}", "Bike"))
    for i in range(1, 11):
        parking_lot.add_spot(ParkingSpot(f"C{i}", "Car"))
    for i in range(1, 4):
        parking_lot.add_spot(ParkingSpot(f"T{i}", "Truck"))

    while True:
        print("\n--- Parking Lot Management ---")
        print("1. Park Vehicle")
        print("2. Remove Vehicle")
        print("3. View Lot Status")
        print("4. View Active Tickets")
        print("5. View Earnings Report")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            v_type = input("Vehicle type (Bike/Car/Truck): ").capitalize()
            plate = input("License Plate: ")
            if v_type == "Bike":
                vehicle = Bike(plate)
            elif v_type == "Car":
                vehicle = Car(plate)
            elif v_type == "Truck":
                vehicle = Truck(plate)
            else:
                print("Invalid vehicle type.")
                continue
            parking_lot.park_vehicle(vehicle)

        elif choice == '2':
            plate = input("License Plate: ")
            parking_lot.release_vehicle(plate)

        elif choice == '3':
            parking_lot.generate_report()

        elif choice == '4':
            print("\n--- Active Tickets ---")
            for t in parking_lot.tickets.values():
                print(f"{t.ticket_id}: {t.vehicle.vehicle_type} {t.vehicle.license_plate} at Spot {t.spot_id}")

        elif choice == '5':
            print(f"Total Earnings: ${parking_lot.earnings}")

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main_menu()
