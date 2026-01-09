from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, List, Tuple

def now() -> datetime:
    return datetime.now()

def hours_between(start: datetime, end: datetime) -> float:
    seconds = (end - start).total_seconds()

    hours = seconds / 3600.0
    return max(1.0, hours)

class Vehicle(ABC):
    def __init__(self, license_plate: str) -> None:
        self.license_plate = license_plate.strip().upper()
        self.entry_time: Optional[datetime] = None

    @property
    @abstractmethod
    def vehicle_type(self) -> str:
        """Return vehicle type: BIKE / CAR / TRUCK."""
        raise NotImplementedError


class Bike(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "BIKE"


class Car(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "CAR"


class Truck(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "TRUCK"




@dataclass
class ParkingSpot:
    spot_id: int
    vehicle_type: str                
    is_available: bool = True
    current_vehicle: Optional[Vehicle] = None

    def assign_vehicle(self, vehicle: Vehicle) -> None:
        if not self.is_available:
            raise ValueError("Spot is not available.")
        if vehicle.vehicle_type != self.vehicle_type:
            raise ValueError("Vehicle type does not match spot type.")
        self.current_vehicle = vehicle
        self.is_available = False

    def remove_vehicle(self) -> Vehicle:
        if self.is_available or self.current_vehicle is None:
            raise ValueError("No vehicle to remove from this spot.")
        v = self.current_vehicle
        self.current_vehicle = None
        self.is_available = True
        return v


class FeeCalculator:
    """
    Define rates here (per hour).
    You can change these numbers freely.
    """
    RATES = {
        "BIKE": 0.50,
        "CAR": 1.50,
        "TRUCK": 3.00,
    }

    @classmethod
    def calculate(cls, vehicle_type: str, hours: float) -> float:
        if vehicle_type not in cls.RATES:
            raise ValueError("Unknown vehicle type for fee calculation.")
        return cls.RATES[vehicle_type] * hours

@dataclass
class Ticket:
    ticket_id: int
    vehicle_plate: str
    vehicle_type: str
    spot_id: int
    entry_time: datetime
    exit_time: Optional[datetime] = None
    fee: float = 0.0

    def calculate_fee(self, exit_time: datetime) -> float:
        self.exit_time = exit_time
        hrs = hours_between(self.entry_time, self.exit_time)
        self.fee = round(FeeCalculator.calculate(self.vehicle_type, hrs), 2)
        return self.fee


class ParkingLot:
    def __init__(self, spots: List[ParkingSpot]) -> None:
        self.spots: Dict[int, ParkingSpot] = {s.spot_id: s for s in spots}
        self.tickets_active: Dict[str, Ticket] = {} 
        self.tickets_closed: List[Ticket] = []
        self._next_ticket_id: int = 10001

    def find_available_spot(self, vehicle_type: str) -> Optional[ParkingSpot]:
        for s in self.spots.values():
            if s.is_available and s.vehicle_type == vehicle_type:
                return s
        return None

    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        plate = vehicle.license_plate
        if not plate:
            raise ValueError("License plate cannot be empty.")
        if plate in self.tickets_active:
            raise ValueError("This vehicle is already parked (active ticket exists).")

        spot = self.find_available_spot(vehicle.vehicle_type)
        if not spot:
            raise ValueError(f"No available spot for vehicle type: {vehicle.vehicle_type}")

        vehicle.entry_time = now()
        spot.assign_vehicle(vehicle)

        ticket = Ticket(
            ticket_id=self._next_ticket_id,
            vehicle_plate=plate,
            vehicle_type=vehicle.vehicle_type,
            spot_id=spot.spot_id,
            entry_time=vehicle.entry_time,
        )
        self._next_ticket_id += 1
        self.tickets_active[plate] = ticket
        return ticket

    def release_vehicle(self, license_plate: str) -> Ticket:
        plate = license_plate.strip().upper()
        ticket = self.tickets_active.get(plate)
        if not ticket:
            raise ValueError("No active ticket found for this license plate.")

        spot = self.spots.get(ticket.spot_id)
        if not spot:
            raise ValueError("Parking spot for this ticket no longer exists (data error).")

        
        spot.remove_vehicle()

 
        ticket.calculate_fee(now())
        self.tickets_closed.append(ticket)
        del self.tickets_active[plate]
        return ticket

    def generate_report(self) -> Dict[str, float]:
        total_earned = round(sum(t.fee for t in self.tickets_closed), 2)
        active_count = len(self.tickets_active)
        available_count = sum(1 for s in self.spots.values() if s.is_available)
        total_spots = len(self.spots)
        return {
            "total_spots": total_spots,
            "available_spots": available_count,
            "occupied_spots": total_spots - available_count,
            "active_tickets": active_count,
            "total_earned": total_earned,
        }

    def lot_status(self) -> None:
        # Summary by type
        types = ["BIKE", "CAR", "TRUCK"]
        print("\nParking Lot Status")
        print("-" * 70)
        for t in types:
            total = sum(1 for s in self.spots.values() if s.vehicle_type == t)
            avail = sum(1 for s in self.spots.values() if s.vehicle_type == t and s.is_available)
            occ = total - avail
            print(f"{t:<6} | Total: {total:<3} Available: {avail:<3} Occupied: {occ:<3}")
        print("-" * 70)

      
        print("Occupied Spots:")
        any_occ = False
        for s in sorted(self.spots.values(), key=lambda x: x.spot_id):
            if not s.is_available and s.current_vehicle:
                any_occ = True
                print(f"Spot {s.spot_id} ({s.vehicle_type}) -> {s.current_vehicle.license_plate}")
        if not any_occ:
            print("None")
        print("-" * 70)

    def show_active_tickets(self) -> None:
        if not self.tickets_active:
            print("No active tickets.")
            return
        print("\nActive Tickets")
        print("-" * 70)
        for plate, t in self.tickets_active.items():
            print(f"Ticket {t.ticket_id} | {plate} | {t.vehicle_type} | Spot {t.spot_id} | Entry {t.entry_time}")
        print("-" * 70)

    def show_earnings(self) -> None:
        report = self.generate_report()
        print("\nEarnings Report")
        print("-" * 70)
        print(f"Total earned: {report['total_earned']:.2f}")
        print(f"Closed tickets: {len(self.tickets_closed)}")
        print("-" * 70)
        if self.tickets_closed:
            print("Closed Ticket Details:")
            for t in self.tickets_closed[-10:]:  # show last 10
                exit_dt = t.exit_time.isoformat(timespec="seconds") if t.exit_time else "N/A"
                print(f"Ticket {t.ticket_id} | {t.vehicle_plate} | {t.vehicle_type} | Fee {t.fee:.2f} | Exit {exit_dt}")
        else:
            print("No closed tickets yet.")
        print("-" * 70)




class ParkingLotApp:
    def __init__(self) -> None:
        self.lot = ParkingLot(self._create_default_spots())

    @staticmethod
    def _create_default_spots() -> List[ParkingSpot]:
        """
        You can change spot counts here.
        Example setup:
          - 5 BIKE spots (1-5)
          - 7 CAR spots  (6-12)
          - 3 TRUCK spots (13-15)
        """
        spots: List[ParkingSpot] = []
        sid = 1
        for _ in range(5):
            spots.append(ParkingSpot(spot_id=sid, vehicle_type="BIKE"))
            sid += 1
        for _ in range(7):
            spots.append(ParkingSpot(spot_id=sid, vehicle_type="CAR"))
            sid += 1
        for _ in range(3):
            spots.append(ParkingSpot(spot_id=sid, vehicle_type="TRUCK"))
            sid += 1
        return spots

    def run(self) -> None:
        while True:
            print("\nTask 5: Parking Lot Management")
            print("1. Park Vehicle")
            print("2. Remove Vehicle")
            print("3. View Lot Status")
            print("4. View Active Tickets")
            print("5. View Earnings Report")
            print("6. Exit")

            try:
                choice = self._read_int("Choose: ")
                if choice == 1:
                    self._park_flow()
                elif choice == 2:
                    self._remove_flow()
                elif choice == 3:
                    self.lot.lot_status()
                elif choice == 4:
                    self.lot.show_active_tickets()
                elif choice == 5:
                    self.lot.show_earnings()
                elif choice == 6:
                    print("Goodbye.")
                    return
                else:
                    print("Invalid option.")
            except ValueError as e:
                print(f"Error: {e}")

    def _park_flow(self) -> None:
        print("\nVehicle Type:")
        print("1. Bike")
        print("2. Car")
        print("3. Truck")
        vt = self._read_int("Choose: ")

        plate = input("License plate: ").strip().upper()
        if not plate:
            raise ValueError("License plate cannot be empty.")

        if vt == 1:
            vehicle = Bike(plate)
        elif vt == 2:
            vehicle = Car(plate)
        elif vt == 3:
            vehicle = Truck(plate)
        else:
            raise ValueError("Invalid vehicle type selection.")

        ticket = self.lot.park_vehicle(vehicle)
        print("\nParked Successfully")
        print("-" * 70)
        print(f"Ticket ID : {ticket.ticket_id}")
        print(f"Plate     : {ticket.vehicle_plate}")
        print(f"Type      : {ticket.vehicle_type}")
        print(f"Spot ID   : {ticket.spot_id}")
        print(f"Entry     : {ticket.entry_time.isoformat(timespec='seconds')}")
        print("-" * 70)

    def _remove_flow(self) -> None:
        plate = input("License plate to remove: ").strip().upper()
        if not plate:
            raise ValueError("License plate cannot be empty.")

        ticket = self.lot.release_vehicle(plate)
        print("\nVehicle Released")
        print("-" * 70)
        print(f"Ticket ID : {ticket.ticket_id}")
        print(f"Plate     : {ticket.vehicle_plate}")
        print(f"Type      : {ticket.vehicle_type}")
        print(f"Spot ID   : {ticket.spot_id}")
        print(f"Entry     : {ticket.entry_time.isoformat(timespec='seconds')}")
        print(f"Exit      : {ticket.exit_time.isoformat(timespec='seconds') if ticket.exit_time else 'N/A'}")
        print(f"Fee       : {ticket.fee:.2f}")
        print("-" * 70)

    @staticmethod
    def _read_int(prompt: str) -> int:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            raise ValueError("Please enter a valid integer.")


if __name__ == "__main__":
    ParkingLotApp().run()
