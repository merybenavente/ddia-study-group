import time
from collections import deque
from datetime import datetime

from simulation import get_new_drivers, get_new_riders
from matching import match_riders_to_drivers
from logger import log_and_enqueue, log_match, DRIVER_LOG, RIDER_LOG
from faults import check_rider_timeouts, simulate_gps_failures, is_service_crashed


driver_queue = deque()
rider_queue = deque()
rider_entry_times = {}


def main():
    while True:
        new_drivers = get_new_drivers()
        new_riders = get_new_riders()

        for driver in new_drivers:
            log_and_enqueue(driver, driver_queue, DRIVER_LOG)
        for rider in new_riders:
            log_and_enqueue(rider, rider_queue, RIDER_LOG)
            rider_entry_times[rider.id] = datetime.now()

        # Simulate GPS failures — remove affected drivers
        gps_failed = simulate_gps_failures(driver_queue)
        for driver in gps_failed:
            print(f"GPS failure: driver {driver.id[:8]} removed from queue")

        # Check if matching service is crashed this cycle
        if is_service_crashed():
            print("SERVICE UNAVAILABLE — matching service crashed, retrying next cycle")
        else:
            matches = match_riders_to_drivers(rider_queue, driver_queue)
            for rider, driver, eta in matches:
                log_match(rider, driver, eta)
                if rider.id in rider_entry_times:
                    del rider_entry_times[rider.id]
                print(f"Matched rider {rider.id[:8]} with driver {driver.id[:8]} (ETA: {eta:.1f} min)")

        # Check for riders who have waited too long
        timed_out = check_rider_timeouts(rider_queue, rider_entry_times)
        for rider in timed_out:
            print(f"Timeout: rider {rider.id[:8]} waited >3 min — notified to stay or leave")

        time.sleep(1)


if __name__ == "__main__":
    main()
