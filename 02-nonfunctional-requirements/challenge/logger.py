import json
import random
from dataclasses import asdict
from datetime import datetime, timedelta

from models import LedgerEntry


DRIVER_LOG = "drivers.jsonl"
RIDER_LOG = "riders.jsonl"
LEDGER_LOG = "ledger.jsonl"


def log_and_enqueue(entity, queue, log_file):
    # Append to log and add to queue as a single operation
    with open(log_file, "a") as f:
        f.write(json.dumps(asdict(entity)) + "\n")
    queue.append(entity)


def log_match(rider, driver, eta_minutes):
    # 15% chance of a 0-30% delay on top of estimated pickup time
    now = datetime.now()
    estimated_pickup = now + timedelta(minutes=eta_minutes)

    if random.random() < 0.15:
        delay_factor = random.uniform(0, 0.3)
        real_pickup = estimated_pickup + timedelta(minutes=eta_minutes * delay_factor)
    else:
        real_pickup = estimated_pickup

    entry = LedgerEntry(
        ride_id=f"{driver.id[:8]}-{rider.id[:8]}",
        driver_id=driver.id,
        rider_id=rider.id,
        assignation_time=now,
        pickup_estimated_time=estimated_pickup,
        pickup_location=rider.pickup_point,
        num_riders=rider.num_riders,
        destination=rider.destination,
        real_pickup_time=real_pickup,
    )

    with open(LEDGER_LOG, "a") as f:
        f.write(json.dumps(asdict(entry), default=str) + "\n")

    return entry
