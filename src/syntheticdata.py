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
