import json
import random

cycles = 100000  # 1초 @ 10ns per cycle

def random_levels():
    return [random.choice([0, 1]) for _ in range(cycles)]

def random_data():
    return [format(random.randint(0, 255), "02X") for _ in range(cycles)]

signals = [
    {"name": "CLE", "type": "level", "levels": random_levels()},
    {"name": "ALE", "type": "level", "levels": random_levels()},
    {"name": "WE#", "type": "level", "levels": random_levels()},
    {"name": "RE#", "type": "level", "levels": random_levels()},
    {"name": "CE#", "type": "level", "levels": random_levels()},
    {"name": "R/B#", "type": "level", "levels": random_levels()},
    {"name": "IO", "type": "data", "values": random_data()}
]

data = {"signals": signals}

filename = "./nand_flash_1s_random.json"
with open(filename, "w") as f:
    json.dump(data, f, indent=4)
