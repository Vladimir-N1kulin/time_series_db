import random
from datetime import datetime, timedelta

# Function to generate a list of timestamped data
def generate_data(count):
    # Get the current date and time as the starting point for generating timestamps
    base_time = datetime.now()
    # Generate a list of tuples where each tuple contains:
    # - A timestamp incremented by `i` seconds from the base_time
    # - A string value in the format "value_i"
    return [(base_time + timedelta(seconds=i), f"value_{i}") for i in range(count)]


def generate_random_data(count):
    """
    Generate a list of random timestamped data.

    :param count: Number of data points to generate.
    :return: A list of tuples with random timestamps and associated string values.
    """
    base_time = datetime.now()  # Starting point for generating timestamps
    data = []

    # Generate `count` timestamps with random intervals and values
    for i in range(count):
        random_seconds = random.randint(1, 100)  # Random interval in seconds
        random_time = base_time + timedelta(seconds=random_seconds * i)  # Add random interval
        data.append((random_time, f"value_{i}"))  # Add timestamp and associated value

    # Shuffle the list to make the order of timestamps more random
    random.shuffle(data)
    return data
