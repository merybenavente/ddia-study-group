import math
import random
from typing import Tuple

AVG_SPEED_KMH = 30


def estimate_eta_minutes(origin: Tuple[float, float], destination: Tuple[float, float]) -> float:
    # Haversine distance in km, then divide by avg city speed, with +/-20% randomness
    lat1, lon1 = math.radians(origin[0]), math.radians(origin[1])
    lat2, lon2 = math.radians(destination[0]), math.radians(destination[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    km = 6371 * 2 * math.asin(math.sqrt(a))

    minutes = (km / AVG_SPEED_KMH) * 60
    noise = random.uniform(0.8, 1.2)
    return minutes * noise
