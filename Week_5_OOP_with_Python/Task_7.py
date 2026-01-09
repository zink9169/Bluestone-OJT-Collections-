from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from abc import ABC


def read_nonempty(prompt: str) -> str:
    s = input(prompt).strip()
    if not s:
        raise ValueError("Input cannot be empty.")
    return s

def read_choice(prompt: str, allowed: List[str]) -> str:
    c = input(prompt).strip()
    if c not in allowed:
        raise ValueError(f"Invalid choice. Allowed: {', '.join(allowed)}")
    return c

def read_int(prompt: str) -> int:
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        raise ValueError("Please enter a valid integer.")

def parse_dt(dt_str: str) -> str:
    """
    Accept: 'YYYY-MM-DD HH:MM'  or 'YYYY-MM-DDTHH:MM'
    Store ISO 'YYYY-MM-DDTHH:MM:SS'
    """
    dt_str = dt_str.strip()
    fmts = ["%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]
    last = None
    for f in fmts:
        try:
            return datetime.strptime(dt_str, f).isoformat(timespec="seconds")
        except ValueError as e:
            last = e
    raise ValueError("Invalid datetime format. Use 'YYYY-MM-DD HH:MM' (e.g., 2026-01-05 14:30).") from last

def pretty_dt(iso_str: str) -> str:
    try:
        return datetime.fromisoformat(iso_str).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return iso_str

def extract_date(iso_dt: str) -> str:
    try:
        return datetime.fromisoformat(iso_dt).strftime("%Y-%m-%d")
    except ValueError:
        return iso_dt[:10]




@dataclass
class Person(ABC):
    name: str
    email: str
    passport_id: str

    @property
    def role(self) -> str:
        return "PERSON"


@dataclass
class Passenger(Person):
    @property
    def role(self) -> str:
        return "PASSENGER"


@dataclass
class AirlineStaff(Person):
    @property
    def role(self) -> str:
        return "STAFF"


@dataclass
class Admin(AirlineStaff):
    @property
    def role(self) -> str:
        return "ADMIN"


@dataclass
class CheckInAgent(AirlineStaff):
    @property
    def role(self) -> str:
        return "CHECKIN_AGENT"


@dataclass
class Pilot(AirlineStaff):
    @property
    def role(self) -> str:
        return "PILOT"




@dataclass
class Route:
    route_id: int
    origin: str
    destination: str
    distance_km: float
    estimated_time: str 

    def calculate_flight_duration(self) -> str:
     
        return self.estimated_time




@dataclass
class Aircraft:
    aircraft_id: int
    model: str
    capacity: int
    seat_map: Set[str] = field(default_factory=set)  

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("Aircraft capacity must be > 0.")
        if not self.seat_map:
            
            self.seat_map = self._generate_seats(self.capacity)

    @staticmethod
    def _generate_seats(capacity: int) -> Set[str]:
        letters = ["A", "B", "C", "D", "E", "F"]
        seats: Set[str] = set()
        row = 1
        while len(seats) < capacity:
            for l in letters:
                if len(seats) >= capacity:
                    break
                seats.add(f"{row}{l}")
            row += 1
        return seats

    def get_available_seats(self, taken_seats: Set[str]) -> List[str]:
        return sorted(list(self.seat_map - taken_seats))

    def assign_seat(self, taken_seats: Set[str]) -> str:
        avail = self.get_available_seats(taken_seats)
        if not avail:
            raise ValueError("No available seats.")
        return avail[0]  




@dataclass
class Flight:
    flight_id: int
    origin: str
    destination: str
    departure_time: str  
    arrival_time: str    
    aircraft_id: int
    passenger_manifest: Set[str] = field(default_factory=set)  
    status: str = "SCHEDULED"  

    def add_passenger(self, passenger: Passenger) -> None:
        if self.status == "CANCELLED":
            raise ValueError("Cannot add passenger to a cancelled flight.")
        self.passenger_manifest.add(passenger.passport_id)

    def cancel_passenger(self, passenger: Passenger) -> None:
        self.passenger_manifest.discard(passenger.passport_id)

    def check_seat_availability(self, aircraft_capacity: int) -> bool:
        return len(self.passenger_manifest) < aircraft_capacity




@dataclass
class Ticket:
    ticket_id: int
    passenger_passport: str
    flight_id: int
    seat_number: str
    status: str = "ACTIVE"  

    def generate_ticket(self) -> str:
        return f"TICKET#{self.ticket_id} | Flight {self.flight_id} | Seat {self.seat_number} | Status {self.status}"

    def cancel_ticket(self) -> None:
        self.status = "CANCELLED"

    def reschedule_ticket(self, new_flight_id: int, new_seat: str) -> None:
        self.flight_id = new_flight_id
        self.seat_number = new_seat
        self.status = "RESCHEDULED"




class ReservationSystem:
    def __init__(self) -> None:
        self.users: Dict[str, Person] = {}         
        self.flights: Dict[int, Flight] = {}       
        self.routes: Dict[int, Route] = {}          
        self.tickets: Dict[int, Ticket] = {}       
        self.aircrafts: Dict[int, Aircraft] = {}    

        self._next_route_id = 2001
        self._next_aircraft_id = 3001
        self._next_flight_id = 4001
        self._next_ticket_id = 5001


    def register_user(self, person: Person) -> None:
        if person.passport_id in self.users:
            # overwrite or raise; choose raise for safety
            raise ValueError("A user with this passport_id already exists.")
        self.users[person.passport_id] = person

    def get_user(self, passport_id: str) -> Person:
        u = self.users.get(passport_id)
        if not u:
            raise ValueError("User not found.")
        return u

    # ---- Admin methods ----

    def add_aircraft(self, model: str, capacity: int) -> Aircraft:
        aid = self._next_aircraft_id
        self._next_aircraft_id += 1
        a = Aircraft(aircraft_id=aid, model=model.strip(), capacity=capacity)
        self.aircrafts[aid] = a
        return a

    def add_flight(
        self,
        origin: str,
        destination: str,
        departure_time_iso: str,
        arrival_time_iso: str,
        aircraft_id: int,
    ) -> Flight:
        if aircraft_id not in self.aircrafts:
            raise ValueError("Aircraft not found.")

        fid = self._next_flight_id
        self._next_flight_id += 1

        f = Flight(
            flight_id=fid,
            origin=origin.strip().upper(),
            destination=destination.strip().upper(),
            departure_time=departure_time_iso,
            arrival_time=arrival_time_iso,
            aircraft_id=aircraft_id,
            passenger_manifest=set(),
            status="SCHEDULED",
        )
        self.flights[fid] = f
        return f

    def view_all_tickets(self) -> None:
        if not self.tickets:
            print("No tickets found.")
            return
        print("\nAll Tickets")
        print("-" * 90)
        for t in sorted(self.tickets.values(), key=lambda x: x.ticket_id):
            print(t.generate_ticket(), f"| Passenger {t.passenger_passport}")
        print("-" * 90)


    def search_flights(self, origin: str, destination: str, date_yyyy_mm_dd: str) -> List[Flight]:
        origin = origin.strip().upper()
        destination = destination.strip().upper()
        date_yyyy_mm_dd = date_yyyy_mm_dd.strip()

        results = []
        for f in self.flights.values():
            if f.status == "CANCELLED":
                continue
            if f.origin == origin and f.destination == destination and extract_date(f.departure_time) == date_yyyy_mm_dd:
                results.append(f)
        return sorted(results, key=lambda x: x.departure_time)

    def book_ticket(self, passenger: Passenger, flight_id: int) -> Ticket:
        flight = self.flights.get(flight_id)
        if not flight:
            raise ValueError("Flight not found.")
        if flight.status == "CANCELLED":
            raise ValueError("Cannot book a cancelled flight.")

        aircraft = self.aircrafts.get(flight.aircraft_id)
        if not aircraft:
            raise ValueError("Aircraft not found for this flight (data error).")

        if not flight.check_seat_availability(aircraft.capacity):
            raise ValueError("No seats available for this flight.")

        taken = {t.seat_number for t in self.tickets.values() if t.flight_id == flight_id and t.status != "CANCELLED"}
        seat = aircraft.assign_seat(taken)

        flight.add_passenger(passenger)

        tid = self._next_ticket_id
        self._next_ticket_id += 1

        ticket = Ticket(
            ticket_id=tid,
            passenger_passport=passenger.passport_id,
            flight_id=flight_id,
            seat_number=seat,
            status="ACTIVE",
        )
        self.tickets[tid] = ticket
        return ticket

    def cancel_ticket(self, ticket_id: int) -> None:
        t = self.tickets.get(ticket_id)
        if not t:
            raise ValueError("Ticket not found.")
        if t.status == "CANCELLED":
            raise ValueError("Ticket already cancelled.")

        flight = self.flights.get(t.flight_id)
        passenger = self.users.get(t.passenger_passport)
        if isinstance(flight, Flight) and isinstance(passenger, Passenger):
            flight.cancel_passenger(passenger)

        t.cancel_ticket()

    def get_passenger_bookings(self, passport_id: str) -> List[Ticket]:
        return sorted(
            [t for t in self.tickets.values() if t.passenger_passport == passport_id],
            key=lambda x: x.ticket_id,
        )


    def generate_reports(self) -> Dict[str, int]:
        total_flights = len(self.flights)
        total_tickets = len(self.tickets)
        active_tickets = sum(1 for t in self.tickets.values() if t.status != "CANCELLED")
        cancelled_tickets = total_tickets - active_tickets
        return {
            "total_flights": total_flights,
            "total_tickets": total_tickets,
            "active_tickets": active_tickets,
            "cancelled_tickets": cancelled_tickets,
        }




class AirFlowApp:
    def __init__(self) -> None:
        self.system = ReservationSystem()
        self._seed_data()

    def _seed_data(self) -> None:
        self.system.register_user(Admin(name="Admin", email="admin@airflow.com", passport_id="ADMIN-001"))
        self.system.register_user(CheckInAgent(name="Agent", email="agent@airflow.com", passport_id="AGENT-001"))

        a1 = self.system.add_aircraft("Boeing 737", 30)
        a2 = self.system.add_aircraft("Airbus A320", 24)

        self.system.add_flight("YGN", "BKK", parse_dt("2026-01-10 09:00"), parse_dt("2026-01-10 11:10"), a1.aircraft_id)
        self.system.add_flight("YGN", "BKK", parse_dt("2026-01-10 15:00"), parse_dt("2026-01-10 17:10"), a2.aircraft_id)
        self.system.add_flight("YGN", "SIN", parse_dt("2026-01-11 08:30"), parse_dt("2026-01-11 11:45"), a2.aircraft_id)

    def run(self) -> None:
        while True:
            print("\nWelcome to AirFlow - Airline Booking System")
            print("Choose your role:")
            print("1. Passenger")
            print("2. Check-In Agent")
            print("3. Admin")
            print("4. Exit")

            try:
                choice = read_choice("Choose: ", ["1", "2", "3", "4"])
                if choice == "1":
                    self.passenger_flow()
                elif choice == "2":
                    self.checkin_agent_flow()
                elif choice == "3":
                    self.admin_flow()
                elif choice == "4":
                    print("Goodbye.")
                    return
            except ValueError as e:
                print(f"Error: {e}")



    def passenger_flow(self) -> None:
        print("\nPassenger Login/Register")
        passport = read_nonempty("Passport ID: ").strip().upper()

        user: Optional[Person] = self.system.users.get(passport)
        if not user:
            name = read_nonempty("Name: ")
            email = read_nonempty("Email: ")
            p = Passenger(name=name, email=email, passport_id=passport)
            self.system.register_user(p)
            user = p
            print("Passenger registered successfully.")

        if not isinstance(user, Passenger):
            raise ValueError("This passport ID is not a Passenger account.")

        passenger = user

        while True:
            print(f"\nPassenger Menu ({passenger.name} | {passenger.passport_id})")
            print("1. Search Flights")
            print("2. Book Ticket")
            print("3. Cancel Ticket")
            print("4. View My Bookings")
            print("5. Back")

            choice = read_choice("Choose: ", ["1", "2", "3", "4", "5"])
            try:
                if choice == "1":
                    self._passenger_search()
                elif choice == "2":
                    self._passenger_book(passenger)
                elif choice == "3":
                    self._passenger_cancel(passenger)
                elif choice == "4":
                    self._passenger_view_bookings(passenger)
                elif choice == "5":
                    return
            except ValueError as e:
                print(f"Error: {e}")

    def _passenger_search(self) -> None:
        origin = read_nonempty("Origin (e.g., YGN): ")
        dest = read_nonempty("Destination (e.g., BKK): ")
        date = read_nonempty("Date (YYYY-MM-DD): ")

        flights = self.system.search_flights(origin, dest, date)
        self._print_flights(flights)

    def _passenger_book(self, passenger: Passenger) -> None:
        print("\nBook Ticket")
        fid = read_int("Flight ID: ")
        ticket = self.system.book_ticket(passenger, fid)
        print("Ticket booked successfully.")
        print(ticket.generate_ticket())

    def _passenger_cancel(self, passenger: Passenger) -> None:
        self._passenger_view_bookings(passenger)
        tid = read_int("Ticket ID to cancel: ")
        # Basic check: passenger can cancel only own tickets
        t = self.system.tickets.get(tid)
        if not t or t.passenger_passport != passenger.passport_id:
            raise ValueError("Ticket not found for this passenger.")
        self.system.cancel_ticket(tid)
        print("Ticket cancelled successfully.")

    def _passenger_view_bookings(self, passenger: Passenger) -> None:
        bookings = self.system.get_passenger_bookings(passenger.passport_id)
        if not bookings:
            print("No bookings.")
            return
        print("\nMy Bookings")
        print("-" * 90)
        for t in bookings:
            flight = self.system.flights.get(t.flight_id)
            route = f"{flight.origin}->{flight.destination}" if flight else "Unknown"
            dep = pretty_dt(flight.departure_time) if flight else "Unknown"
            print(f"{t.generate_ticket()} | Route {route} | Dep {dep}")
        print("-" * 90)


    def checkin_agent_flow(self) -> None:
        print("\nCheck-In Agent Login")
        passport = read_nonempty("Agent passport ID: ").strip().upper()
        user = self.system.users.get(passport)
        if not isinstance(user, CheckInAgent):
            raise ValueError("Invalid Check-In Agent credentials (seed: AGENT-001).")

        while True:
            print("\nCheck-In Agent Menu")
            print("1. Search Flights")
            print("2. View Passenger Bookings")
            print("3. Back")

            choice = read_choice("Choose: ", ["1", "2", "3"])
            try:
                if choice == "1":
                    self._passenger_search()
                elif choice == "2":
                    pid = read_nonempty("Passenger passport ID: ").strip().upper()
                    bookings = self.system.get_passenger_bookings(pid)
                    if not bookings:
                        print("No bookings for that passenger.")
                    else:
                        print("\nPassenger Bookings")
                        print("-" * 90)
                        for t in bookings:
                            print(t.generate_ticket())
                        print("-" * 90)
                elif choice == "3":
                    return
            except ValueError as e:
                print(f"Error: {e}")


    def admin_flow(self) -> None:
        print("\nAdmin Login")
        passport = read_nonempty("Admin passport ID: ").strip().upper()
        user = self.system.users.get(passport)
        if not isinstance(user, Admin):
            raise ValueError("Invalid Admin credentials (seed: ADMIN-001).")

        while True:
            print("\nAdmin Menu")
            print("1. Add Flight")
            print("2. Add Aircraft")
            print("3. View All Tickets")
            print("4. View Report Summary")
            print("5. Back")

            choice = read_choice("Choose: ", ["1", "2", "3", "4", "5"])
            try:
                if choice == "1":
                    self._admin_add_flight()
                elif choice == "2":
                    self._admin_add_aircraft()
                elif choice == "3":
                    self.system.view_all_tickets()
                elif choice == "4":
                    r = self.system.generate_reports()
                    print("\nSystem Report")
                    print("-" * 70)
                    for k, v in r.items():
                        print(f"{k}: {v}")
                    print("-" * 70)
                elif choice == "5":
                    return
            except ValueError as e:
                print(f"Error: {e}")

    def _admin_add_aircraft(self) -> None:
        model = read_nonempty("Aircraft model: ")
        capacity = read_int("Capacity: ")
        a = self.system.add_aircraft(model, capacity)
        print(f"Aircraft added: ID {a.aircraft_id} | {a.model} | Capacity {a.capacity}")

    def _admin_add_flight(self) -> None:
        origin = read_nonempty("Origin (e.g., YGN): ")
        dest = read_nonempty("Destination (e.g., BKK): ")
        dep = parse_dt(read_nonempty("Departure (YYYY-MM-DD HH:MM): "))
        arr = parse_dt(read_nonempty("Arrival   (YYYY-MM-DD HH:MM): "))

        self._print_aircrafts()
        aid = read_int("Aircraft ID: ")

        f = self.system.add_flight(origin, dest, dep, arr, aid)
        print(f"Flight added: ID {f.flight_id} | {f.origin}->{f.destination} | Dep {pretty_dt(f.departure_time)}")

    # ------------------
    # Print helpers
    # ------------------

    def _print_aircrafts(self) -> None:
        if not self.system.aircrafts:
            print("No aircrafts.")
            return
        print("\nAircrafts")
        print("-" * 70)
        for a in self.system.aircrafts.values():
            print(f"ID {a.aircraft_id} | {a.model} | Capacity {a.capacity}")
        print("-" * 70)

    def _print_flights(self, flights: List[Flight]) -> None:
        if not flights:
            print("No flights found.")
            return
        print("\nFlights")
        print("-" * 100)
        for f in flights:
            aircraft = self.system.aircrafts.get(f.aircraft_id)
            cap = aircraft.capacity if aircraft else 0
            seats_ok = f.check_seat_availability(cap)
            print(
                f"Flight {f.flight_id} | {f.origin}->{f.destination} | "
                f"Dep {pretty_dt(f.departure_time)} | Arr {pretty_dt(f.arrival_time)} | "
                f"Aircraft {f.aircraft_id} | Seats Available: {seats_ok} | Status {f.status}"
            )
        print("-" * 100)


if __name__ == "__main__":
    AirFlowApp().run()
