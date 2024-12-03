import random
from datetime import datetime, timedelta

def generate_data(count):
    base_time = datetime.now()
    return [(base_time + timedelta(seconds=i), f"value_{i}") for i in range(count)]