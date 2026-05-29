from dataclasses import dataclass, field
from typing import Optional, Tuple
from datetime import datetime


@dataclass
class Driver:
    id: str
    current_position: Tuple[float, float]
    available_seats: int


@dataclass
class Rider:
    id: str
    pickup_point: Tuple[float, float]
    destination: Tuple[float, float]
    num_riders: int


@dataclass
class LedgerEntry:
    ride_id: str
    driver_id: str
    rider_id: str
    assignation_time: datetime
    pickup_estimated_time: datetime
    pickup_location: Tuple[float, float]
    num_riders: int
    destination: Tuple[float, float]
    real_pickup_time: Optional[datetime] = None
    estimated_dropoff_time: Optional[datetime] = None
    real_dropoff_time: Optional[datetime] = None
    incident: Optional[str] = None
