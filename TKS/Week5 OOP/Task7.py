
#Classes
class Passenger:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.bookings = []


class Aircraft:
    def __init__(self, aircraft_id, model, capacity):
        self.aircraft_id = aircraft_id
        self.model = model
        self.capacity = capacity


class Flight:
    def __init__(self, flight_id, origin, destination, aircraft):
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.aircraft = aircraft
        self.passengers = []

    def seats_available(self):
        return len(self.passengers) < self.aircraft.capacity

    def add_passenger(self, passenger):
        if self.seats_available():
            self.passengers.append(passenger)
            passenger.bookings.append(self)
            return True
        return False

    def remove_passenger(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)
            passenger.bookings.remove(self)
            return True
        return False

#System
class ReservationSystem:
    def __init__(self):
        self.flights = []
        self.aircrafts = []

    def add_aircraft(self, aircraft):
        self.aircrafts.append(aircraft)

    def add_flight(self, flight):
        self.flights.append(flight)

    def search_flights(self, origin, destination):
        return [f for f in self.flights if f.origin == origin and f.destination == destination]



#Menu Simulation
def main():
    system = ReservationSystem()

    # Sample Data
    aircraft1 = Aircraft(1, "Boeing 737", 5)
    system.add_aircraft(aircraft1)
    flight1 = Flight(101, "NYC", "LA", aircraft1)
    system.add_flight(flight1)
    passenger1 = Passenger("John Doe", "john@example.com")

    while True:
        print("\n--- AirFlow Airline Booking System ---")
        print("1. Passenger")
        print("2. Admin")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":  # Passenger
            print("\n--- Passenger Menu ---")
            print("1. Search Flights")
            print("2. Book Flight")
            print("3. Cancel Booking")
            print("4. View Bookings")
            p_choice = input("Enter choice: ")

            if p_choice == "1":
                origin = input("Origin: ")
                destination = input("Destination: ")
                flights = system.search_flights(origin, destination)
                for f in flights:
                    print(f"Flight {f.flight_id}: {f.origin} -> {f.destination}, Seats Available: {f.aircraft.capacity - len(f.passengers)}")

            elif p_choice == "2":
                flight_id = int(input("Flight ID to book: "))
                flight = next((f for f in system.flights if f.flight_id == flight_id), None)
                if flight and flight.add_passenger(passenger1):
                    print(f"Booked Flight {flight.flight_id} successfully!")
                else:
                    print("Booking failed! Flight full or not found.")

            elif p_choice == "3":
                flight_id = int(input("Flight ID to cancel: "))
                flight = next((f for f in passenger1.bookings if f.flight_id == flight_id), None)
                if flight and flight.remove_passenger(passenger1):
                    print("Booking cancelled.")
                else:
                    print("Booking not found.")

            elif p_choice == "4":
                for f in passenger1.bookings:
                    print(f"Flight {f.flight_id}: {f.origin} -> {f.destination}")

        elif choice == "2":
            print("\n--- Admin Menu ---")
            print("1. Add Aircraft")
            print("2. Add Flight")
            a_choice = input("Enter choice: ")

            if a_choice == "1":
                aircraft_id = int(input("Aircraft ID: "))
                model = input("Model: ")
                capacity = int(input("Capacity: "))
                aircraft = Aircraft(aircraft_id, model, capacity)
                system.add_aircraft(aircraft)
                print("Aircraft added.")

            elif a_choice == "2":
                flight_id = int(input("Flight ID: "))
                origin = input("Origin: ")
                destination = input("Destination: ")
                aircraft_id = int(input("Aircraft ID: "))
                aircraft = next((a for a in system.aircrafts if a.aircraft_id == aircraft_id), None)
                if aircraft:
                    flight = Flight(flight_id, origin, destination, aircraft)
                    system.add_flight(flight)
                    print("Flight added.")
                else:
                    print("Aircraft not found.")

        elif choice == "3":
            print("Exiting System. Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
