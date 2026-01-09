from abc import ABC, abstractmethod
from datetime import datetime

class Person(ABC):
    def __init__(self, name, email, passport_id):
        self.name = name
        self.email = email
        self.passport_id = passport_id

class Passenger(Person):
    def __init__(self, name, email, passport_id):
        super().__init__(name, email, passport_id)
        self.bookings = []  # list of Ticket

class AirlineStaff(Person):
    def __init__(self, name, email, passport_id):
        super().__init__(name, email, passport_id)

class Admin(AirlineStaff):
    pass
class CheckInAgent(AirlineStaff):
    pass
class Pilot(AirlineStaff):
    pass

class Aircraft:
    def __init__(self, aircraft_id, model, capacity):
        self.aircraft_id = aircraft_id
        self.model = model
        self.capacity = capacity
        self.seat_map = [f"{r}{c}" for r in range(1, (capacity//6)+1) for c in "ABCDEF"][:capacity]

    def get_available_seats(self, booked_seats):
        return [s for s in self.seat_map if s not in booked_seats]

class Flight:
    def __init__(self, flight_id, origin, destination, departure_time, arrival_time, aircraft):
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.aircraft = aircraft
        self.passenger_manifest = []
        self.status = "Scheduled"

    def check_seat_availability(self):
        booked_seats = [t.seat_number for t in self.passenger_manifest]
        return self.aircraft.get_available_seats(booked_seats)

    def add_passenger(self, ticket):
        if ticket.seat_number in self.check_seat_availability():
            self.passenger_manifest.append(ticket)
            return True
        return False

    def cancel_passenger(self, ticket):
        if ticket in self.passenger_manifest:
            self.passenger_manifest.remove(ticket)
            return True
        return False

class Ticket:
    def __init__(self, ticket_id, passenger, flight, seat_number):
        self.ticket_id = ticket_id
        self.passenger = passenger
        self.flight = flight
        self.seat_number = seat_number
        #Encapsulation
        #status ကို class အတွင်းမှာ control လုပ်နိုင်ပါတယ်။ နောက်ပိုင်း cancel_ticket() method က status ကို update လုပ်တာက Encapsulation လုပ်ထားတာဖြစ်ပါတယ်။
        self.status = "Booked"

    def cancel_ticket(self):
        self.status = "Cancelled"
        self.flight.cancel_passenger(self)
        print(f"Ticket {self.ticket_id} cancelled.")

    def generate_ticket(self):
        print(f"Ticket {self.ticket_id} for {self.passenger.name}: Flight {self.flight.flight_id}, Seat {self.seat_number}")

class Route:
    def __init__(self, route_id, origin, destination, distance_km, estimated_time):
        self.route_id = route_id
        self.origin = origin
        self.destination = destination
        self.distance_km = distance_km
        self.estimated_time = estimated_time  # in hours

class ReservationSystem:
    def __init__(self):
        self.users = {}
        self.flights = {}
        self.aircrafts = {}
        self.tickets = {}
        self.ticket_counter = 1

    def add_passenger(self, passenger):
        self.users[passenger.passport_id] = passenger

    def add_aircraft(self, aircraft):
        self.aircrafts[aircraft.aircraft_id] = aircraft

    def add_flight(self, flight):
        self.flights[flight.flight_id] = flight

    def search_flights(self, origin, destination):
        result = [f for f in self.flights.values() if f.origin==origin and f.destination==destination]
        return result

    def book_ticket(self, passport_id, flight_id):
        passenger = self.users.get(passport_id)
        flight = self.flights.get(flight_id)
        if passenger and flight:
            available_seats = flight.check_seat_availability()
            if available_seats:
                seat = available_seats[0]
                ticket_id = f"T{self.ticket_counter:03d}"
                self.ticket_counter += 1
                ticket = Ticket(ticket_id, passenger, flight, seat)
                if flight.add_passenger(ticket):
                    passenger.bookings.append(ticket)
                    self.tickets[ticket_id] = ticket
                    print(f"Ticket booked successfully! Ticket ID: {ticket_id}, Seat: {seat}")
                else:
                    print("Failed to add passenger to flight.")
            else:
                print("No available seats on this flight.")
        else:
            print("Passenger or flight not found.")

    def cancel_ticket(self, ticket_id):
        ticket = self.tickets.get(ticket_id)
        if ticket and ticket.status=="Booked":
            ticket.cancel_ticket()
        else:
            print("Ticket not found or already cancelled.")

    def generate_reports(self):
        print("\n--- All Tickets ---")
        for t in self.tickets.values():
            print(f"{t.ticket_id}: {t.passenger.name}, Flight {t.flight.flight_id}, Seat {t.seat_number}, Status {t.status}")

def main_menu():
    system = ReservationSystem()


    ac1 = Aircraft("AC001", "Boeing 737", 30)
    system.add_aircraft(ac1)
    fl1 = Flight("FL001", "NYC", "LAX", "2026-01-05 08:00", "2026-01-05 11:00", ac1)
    fl2 = Flight("FL002", "NYC", "LAX", "2026-01-05 15:00", "2026-01-05 18:00", ac1)
    system.add_flight(fl1)
    system.add_flight(fl2)


    p1 = Passenger("John Doe", "john@example.com", "P001")
    system.add_passenger(p1)

    while True:
        print("\nWelcome to AirFlow - Airline Booking System")
        print("Choose your role:")
        print("1. Passenger")
        print("2. Check-In Agent (Not implemented)")
        print("3. Admin")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice=='1':
            passenger_menu(system, p1.passport_id)
        elif choice=='3':
            admin_menu(system)
        elif choice=='4':
            break
        else:
            print("Invalid choice.")

def passenger_menu(system, passport_id):
    passenger = system.users.get(passport_id)
    if not passenger:
        print("Passenger not found.")
        return

    while True:
        print(f"\nPassenger Menu ({passenger.name})")
        print("1. Search Flights")
        print("2. Book Ticket")
        print("3. Cancel Ticket")
        print("4. View My Bookings")
        print("5. Back")
        choice = input("Enter choice: ")

        if choice=='1':
            origin = input("Origin: ")
            destination = input("Destination: ")
            flights = system.search_flights(origin, destination)
            if flights:
                for f in flights:
                    print(f"{f.flight_id}: {f.origin}->{f.destination}, Departure: {f.departure_time}, Available Seats: {len(f.check_seat_availability())}")
            else:
                print("No flights found.")
        elif choice=='2':
            flight_id = input("Flight ID: ")
            system.book_ticket(passport_id, flight_id)
        elif choice=='3':
            ticket_id = input("Ticket ID: ")
            system.cancel_ticket(ticket_id)
        elif choice=='4':
            print("My Bookings:")
            for t in passenger.bookings:
                print(f"{t.ticket_id}: Flight {t.flight.flight_id}, Seat {t.seat_number}, Status {t.status}")
        elif choice=='5':
            break
        else:
            print("Invalid choice.")
def admin_menu(system):
    while True:
        print("Admin Menu")
        print("1. Add Flight")
        print("2. Add Aircraft")
        print("3. View All Tickets")
        print("4. Back")
        choice = input("Enter choice: ")
        if choice=='1':
            fid = input("Flight ID: ")
            origin = input("Origin: ")
            destination = input("Destination: ")
            dep = input("Departure (YYYY-MM-DD HH:MM): ")
            arr = input("Arrival (YYYY-MM-DD HH:MM): ")
            ac_id = input("Aircraft ID: ")
            ac = system.aircrafts.get(ac_id)
            if ac:
                flight = Flight(fid, origin, destination, dep, arr, ac)
                system.add_flight(flight)
                print("Flight added successfully.")
            else:
                print("Aircraft not found.")
        elif choice=='2':
            aid = input("Aircraft ID: ")
            model = input("Model: ")
            capacity = int(input("Capacity: "))
            aircraft = Aircraft(aid, model, capacity)
            system.add_aircraft(aircraft)
            print("Aircraft added successfully.")
        elif choice=='3':
            system.generate_reports()
        elif choice=='4':
            break
        else:
            print("Invalid choice.")

if __name__=="__main__":
    main_menu()
