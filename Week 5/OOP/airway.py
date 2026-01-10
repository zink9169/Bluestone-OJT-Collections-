class Person:
    def __init__(self, name, email, passport_id):
        self.name = name
        self.email = email
        self.passport_id = passport_id


class Passenger(Person):
    def __init__(self, name, email, passport_id):
        super().__init__(name, email, passport_id)
        self.bookings = []


class AirlineStaff(Person):
    def __init__(self, name, email, passport_id, role):
        super().__init__(name, email, passport_id)
        self.role = role


class Aircraft:
    def __init__(self, aircraft_id, model, capacity):
        self.aircraft_id = aircraft_id
        self.model = model
        self.capacity = capacity
        self.available_seats = capacity


class Route:
    def __init__(self, route_id, origin, destination, distance_km):
        self.route_id = route_id
        self.origin = origin
        self.destination = destination
        self.distance_km = distance_km


class Flight:
    def __init__(self, flight_id, route, aircraft, departure_time):
        self.flight_id = flight_id
        self.route = route
        self.aircraft = aircraft
        self.departure_time = departure_time
        self.passenger_manifest = []
        self.status = "Scheduled"

    def check_seat_availability(self):
        return self.aircraft.available_seats > 0


class Ticket:
    def __init__(self, ticket_id, passenger, flight):
        self.ticket_id = ticket_id
        self.passenger = passenger
        self.flight = flight
        self.seat_number = flight.aircraft.capacity - flight.aircraft.available_seats + 1
        self.status = "Confirmed"


class ReservationSystem:
    def __init__(self):
        self.flights = {}
        self.aircrafts = {}
        self.tickets = []
        self.passengers = {}

    def add_aircraft(self, a_id, model, cap):
        self.aircrafts[a_id] = Aircraft(a_id, model, cap)
        print(f"Aircraft {model} added.")

    def add_flight(self, f_id, route, a_id, time):
        if a_id in self.aircrafts:
            new_flight = Flight(f_id, route, self.aircrafts[a_id], time)
            self.flights[f_id] = new_flight
            print(f"Flight {f_id} to {route.destination} added.")

    def book_ticket(self, passenger, f_id):
        flight = self.flights.get(f_id)
        if flight and flight.check_seat_availability():
            t_id = f"TKT-{len(self.tickets) + 100}"
            ticket = Ticket(t_id, passenger, flight)
            self.tickets.append(ticket)
            flight.passenger_manifest.append(passenger)
            flight.aircraft.available_seats -= 1
            passenger.bookings.append(ticket)
            print(f"Booking Successful! Ticket ID: {t_id}")
            return ticket
        print("Booking failed: Flight full or not found.")



def main():
    system = ReservationSystem()
    # Pre-seed Data
    system.add_aircraft("A320", "Airbus A320", 150)
    route1 = Route("R1", "New York", "London", 5500)
    system.add_flight("AF101", route1, "A320", "2025-12-01 10:00")

    while True:
        print("\n=== Welcome to AirFlow Airline System ===")
        print("1. Passenger\n2. Admin\n3. Exit")
        role_choice = input("Select Role: ")

        if role_choice == '1':
            name = input("Enter Name: ")
            p_id = input("Passport ID: ")
            user = system.passengers.get(p_id) or Passenger(name, "n/a", p_id)
            system.passengers[p_id] = user

            while True:
                print(f"\n(Passenger: {user.name})\n1. Search Flights\n2. Book Ticket\n3. View My Bookings\n4. Logout")
                choice = input("Action: ")
                if choice == '1':
                    for f in system.flights.values():
                        print(f"Flight {f.flight_id}: {f.route.origin} -> {f.route.destination} at {f.departure_time}")
                elif choice == '2':
                    f_id = input("Enter Flight ID: ")
                    system.book_ticket(user, f_id)
                elif choice == '3':
                    for t in user.bookings:
                        print(f"Ticket {t.ticket_id} | Flight {t.flight.flight_id} | Seat {t.seat_number}")
                elif choice == '4':
                    break

        elif role_choice == '2':  # Admin
            while True:
                print("\n(Admin Menu)\n1. Add Flight\n2. View All Tickets\n3. Logout")
                choice = input("Action: ")
                if choice == '1':
                    f_id = input("New Flight ID: ")
                    dest = input("Destination: ")
                    route = Route("RX", "Local", dest, 1000)
                    system.add_flight(f_id, route, "A320", "2025-12-25")
                elif choice == '2':
                    for t in system.tickets:
                        print(f"Ticket: {t.ticket_id} | Passenger: {t.passenger.name} | Status: {t.status}")
                elif choice == '3':
                    break

        elif role_choice == '3':
            break


if __name__ == "__main__":
    main()