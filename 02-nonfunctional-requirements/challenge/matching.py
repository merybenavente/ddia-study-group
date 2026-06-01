from collections import deque
from eta import estimate_eta_minutes

MAX_ETA_MINUTES = 7


def match_riders_to_drivers(rider_queue: deque, driver_queue: deque) -> list:
    # Iterate riders; for each, find first driver within 7 min ETA with enough seats
    matched = []
    unmatched_riders = deque()

    while rider_queue:
        rider = rider_queue.popleft()
        found = False

        for i, driver in enumerate(driver_queue):
            eta = estimate_eta_minutes(driver.current_position, rider.pickup_point)
            if eta <= MAX_ETA_MINUTES and driver.available_seats >= rider.num_riders:
                driver_queue.remove(driver)
                matched.append((rider, driver, eta))
                found = True
                break

        if not found:
            unmatched_riders.append(rider)

    rider_queue.extend(unmatched_riders)
    return matched
