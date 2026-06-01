import random
from collections import deque
from datetime import datetime, timedelta

MAX_WAIT_MINUTES = 3
GPS_FAILURE_PROBABILITY = 0.05
SERVICE_CRASH_PROBABILITY = 0.02


def check_rider_timeouts(rider_queue: deque, rider_entry_times: dict) -> list:
    # Remove riders who have waited more than 3 minutes; return them so we can notify
    timed_out = []
    remaining = deque()

    while rider_queue:
        rider = rider_queue.popleft()
        entered_at = rider_entry_times.get(rider.id)
        if entered_at and (datetime.now() - entered_at) > timedelta(minutes=MAX_WAIT_MINUTES):
            timed_out.append(rider)
            del rider_entry_times[rider.id]
        else:
            remaining.append(rider)

    rider_queue.extend(remaining)
    return timed_out


def simulate_gps_failures(driver_queue: deque) -> list:
    # 5% chance per driver per cycle that their GPS stops updating; remove them from queue
    removed = []
    remaining = deque()

    while driver_queue:
        driver = driver_queue.popleft()
        if random.random() < GPS_FAILURE_PROBABILITY:
            removed.append(driver)
        else:
            remaining.append(driver)

    driver_queue.extend(remaining)
    return removed


def is_service_crashed() -> bool:
    # 2% chance per cycle the matching service is temporarily unavailable
    return random.random() < SERVICE_CRASH_PROBABILITY
