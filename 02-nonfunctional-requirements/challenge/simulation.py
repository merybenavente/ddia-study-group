import random
import uuid
from models import Driver, Rider


def get_new_drivers():
    # 70% chance no driver appears; 30% chance one driver with weighted seats (1 most likely, 4 least)
    if random.random() < 0.7:
        return []

    driver = Driver(
        id=str(uuid.uuid4()),
        current_position=(
            random.uniform(40.40, 40.45),
            random.uniform(-3.72, -3.67),
        ),
        available_seats=random.choices([1, 2, 3, 4], weights=[4, 3, 2, 1])[0],
    )
    return [driver]


def get_new_riders():
    # 60% chance no rider appears; 40% chance one rider with weighted group size (1 most likely, 4 least)
    if random.random() < 0.6:
        return []

    rider = Rider(
        id=str(uuid.uuid4()),
        pickup_point=(
            random.uniform(40.40, 40.45),
            random.uniform(-3.72, -3.67),
        ),
        destination=(
            random.uniform(40.40, 40.45),
            random.uniform(-3.72, -3.67),
        ),
        num_riders=random.choices([1, 2, 3, 4], weights=[4, 3, 2, 1])[0],
    )
    return [rider]
