import os
import shelve
from pathlib import Path
import aocd

sh_path = Path(__file__).with_name("cache_data")

session = os.environ["AOC_SESSION"]

def data(day):
    key_day = str(day)
    with shelve.open(sh_path) as cache:
        if key_day in cache:
            return cache[key_day]
        d = aocd.get_data(session=session, day=day, year=2024)
        cache[key_day] = d
        return d
