import datetime
import math


class Vehicle:
    def __init__(self, license_plate, vehicle_type):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.entry_time = datetime.datetime.now()


class Bike(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, "Bike")


class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, "Car")


class Truck(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, "Truck")


class ParkingSpot:
    def __init__(self, spot_id, vehicle_type):
        self.spot_id = spot_id
        self.vehicle_type = vehicle_type
        self.is_available = True
        self.current_vehicle = None

    def assign_vehicle(self, vehicle):
        self.is_available = False
        self.current_vehicle = vehicle

    def remove_vehicle(self):
        self.is_available = True
        self.current_vehicle = None


class Ticket:
    RATES = {"Bike": 10, "Car": 20, "Truck": 50}  # Hourly rates

    def __init__(self, ticket_id, vehicle, spot_id):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot_id = spot_id
        self.entry_time = vehicle.entry_time
        self.exit_time = None
        self.fee = 0

    def calculate_fee(self):
        self.exit_time = datetime.datetime.now()
        # For demonstration, we'll simulate 2 hours if exit is immediate
        duration = self.exit_time - self.entry_time
        hours = max(1, math.ceil(duration.total_seconds() / 3600))
        self.fee = hours * self.RATES.get(self.vehicle.vehicle_type, 20)
        return self.fee


class ParkingLot:
    def __init__(self, bike_spots, car_spots, truck_spots):
        self.spots = []
        self.active_tickets = {}
        self.total_earnings = 0

        # Initialize spots
        for i in range(bike_spots): self.spots.append(ParkingSpot(f"B{i + 1}", "Bike"))
        for i in range(car_spots): self.spots.append(ParkingSpot(f"C{i + 1}", "Car"))
        for i in range(truck_spots): self.spots.append(ParkingSpot(f"T{i + 1}", "Truck"))

    def park_vehicle(self, vehicle):
        for spot in self.spots:
            if spot.is_available and spot.vehicle_type == vehicle.vehicle_type:
                spot.assign_vehicle(vehicle)
                ticket_id = f"TKT-{vehicle.license_plate}"
                ticket = Ticket(ticket_id, vehicle, spot.spot_id)
                self.active_tickets[vehicle.license_plate] = ticket
                print(f"Vehicle parked at spot {spot.spot_id}. Ticket: {ticket_id}")
                return
        print(f"No available spots for {vehicle.vehicle_type}.")

    def release_vehicle(self, license_plate):
        if license_plate in self.active_tickets:
            ticket = self.active_tickets[license_plate]
            fee = ticket.calculate_fee()
            self.total_earnings += fee

            # Free the spot
            for spot in self.spots:
                if spot.spot_id == ticket.spot_id:
                    spot.remove_vehicle()
                    break

            del self.active_tickets[license_plate]
            print(f"Vehicle released. Fee to pay: ${fee}. Total hours: 1 (min)")
        else:
            print("Vehicle not found.")

    def display_status(self):
        available = {"Bike": 0, "Car": 0, "Truck": 0}
        for spot in self.spots:
            if spot.is_available:
                available[spot.vehicle_type] += 1
        print("\n--- Lot Status ---")
        for k, v in available.items(): print(f"{k} spots available: {v}")



def main():
    lot = ParkingLot(bike_spots=5, car_spots=10, truck_spots=2)

    while True:
        print("\n--- Parking System ---")
        print("1. Park Vehicle\n2. Remove Vehicle\n3. View Lot Status\n4. View Earnings\n5. Exit")
        choice = input("Select: ")

        if choice == '1':
            v_type = input("Type (Bike/Car/Truck): ").capitalize()
            lp = input("License Plate: ")
            if v_type == "Bike":
                v = Bike(lp)
            elif v_type == "Car":
                v = Car(lp)
            elif v_type == "Truck":
                v = Truck(lp)
            else:
                print("Invalid type"); continue
            lot.park_vehicle(v)

        elif choice == '2':
            lp = input("Enter License Plate to remove: ")
            lot.release_vehicle(lp)

        elif choice == '3':
            lot.display_status()

        elif choice == '4':
            print(f"Total Earnings: ${lot.total_earnings}")

        elif choice == '5':
            break


if __name__ == "__main__":
    main()