# Car Garage
# OOP based question: Design a car garage with 2 methods — one for checking cars into the garage
# and one for cars exiting. Return the rate (cost) of the car staying in the garage in the second
# method. In the first method, make sure to check if there are any spots available for that specific
# car type (truck, SUV, van, etc.) in the garage for it to enter. If it cannot enter, return False.

from typing import Literal
from datetime import datetime, timezone

VehicleType = Literal["COMPACT", "SEDAN", "SUV", "VAN", "TRUCK"]


class Ticket:
    def __init__(
        self, ticket_id: int, vehicle_type: VehicleType, vehicle_id: str = None
    ):
        self.ticket_id = ticket_id
        self.vehicle_id = vehicle_id
        self.entry_time = datetime.now(timezone.utc)
        self.vehicle_type = vehicle_type
        self.vehicle_to_ticket_map: dict[str, int] = {}


class Garage:
    def __init__(
        self,
        capacity: dict[VehicleType, int],
        price_per_minute: dict[VehicleType, float],
    ):
        self.capacity = capacity
        self.price_per_minute = price_per_minute
        self.next_ticket_id = 1
        self.parked_vehicles: dict[int, Ticket] = {}

    def _find_available_spot(self, vehicle_type: VehicleType) -> bool:
        if vehicle_type is None:
            raise ValueError("vehicle type is required")
        if self.capacity[vehicle_type] > 0:
            self.capacity[vehicle_type] -= 1
            return True
        return False

    def _issue_ticket(
        self, vehicle_type: VehicleType, vehicle_id: str = None
    ) -> Ticket:
        ticket = Ticket(
            ticket_id=self.next_ticket_id,
            vehicle_type=vehicle_type,
            vehicle_id=vehicle_id,
        )
        self.next_ticket_id += 1
        return ticket

    def find_available_spots_by_vehicle_type(self, vehicle_type: VehicleType) -> int:
        return self.capacity[vehicle_type]

    def check_in(
        self, vehicle_type: VehicleType, vehicle_id: str = None
    ) -> Ticket | None:
        if vehicle_type is None:
            raise ValueError("vehicle type must be provided")

        if self._find_available_spot(vehicle_type):
            ticket = self._issue_ticket(
                vehicle_id=vehicle_id, vehicle_type=vehicle_type
            )
            self.parked_vehicles[ticket.ticket_id] = ticket
            if vehicle_id is not None:
                self.vehicle_to_ticket_map[vehicle_id] = ticket_id
            return ticket
        return None

    def _calculate_price(self, ticket: Ticket) -> float | None:
        current_time = datetime.now(timezone.utc)
        delta = current_time - ticket.entry_time
        total_minutes = delta.total_seconds() / 60
        if total_minutes > 1440:
            raise ValueError("Ticket expired - parked for more than 24 hours")
        else:
            rate_per_minute = self.price_per_minute[ticket.vehicle_type]
            return total_minutes * rate_per_minute
        return None

    def _check_out_by_ticket_id(self, ticket_id: int) -> float | None:
        ticket = self.parked_vehicles.pop(ticket_id)
        self.capacity[ticket.vehicle_type] += 1
        return self._calculate_price(ticket)

    def _check_out_by_vehicle_id(self, vehicle_id: str) -> float | None:
        ticket_id = self.vehicle_to_ticket_map[vehicle_id]
        return self._check_out_by_ticket_id(ticket_id)

    def check_out(self, ticket_id: int, vehicle_id: str = None) -> str:
        price = (
            self._check_out_by_ticket_id(ticket_id)
            if ticket_id
            else self._check_out_by_vehicle_id(vehicle_id)
        )
        return f"{(f'Total cost is {price}' if price else 'Old ticket please see assistant')}"


# Write your solution here
def solve():
    capacity: dict[VehicleType, int] = {
        "COMPACT": 5,
        "SEDAN": 5,
        "SUV": 4,
        "VAN": 4,
        "TRUCK": 2,
    }
    price_per_minute: dict[VehicleType, float] = {
        "COMPACT": 0.3,
        "SEDAN": 0.3,
        "SUV": 0.5,
        "VAN": 0.5,
        "TRUCK": 1.0,
    }
    garage = Garage(capacity, price_per_minute)
    print(
        f"checking in Compact Vehicle and ticket id is: {garage.check_in('COMPACT').ticket_id} and available spot is {garage.find_available_spots_by_vehicle_type('COMPACT')}"
    )
    print(
        f"checking in Compact Vehicle and ticket id is: {garage.check_in('COMPACT').ticket_id} and available spot is {garage.find_available_spots_by_vehicle_type('COMPACT')}"
    )
    print(
        f"checking in Truck Vehicle and ticket id is: {garage.check_in('TRUCK').ticket_id} and available spot is {garage.find_available_spots_by_vehicle_type('TRUCK')}"
    )
    print(
        f"checking in Truck Vehicle and ticket id is: {garage.check_in('TRUCK').ticket_id} and available spot is {garage.find_available_spots_by_vehicle_type('TRUCK')}"
    )
    print(f"checking out ticket id {garage.check_out(1)}")


solve()
