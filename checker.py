from collections import Counter
from math import sqrt, ceil
# from heapq import heappush, heappop

FILE_IN = 'test.in'
FILE_OUT = 'test.out'
FILE_IN = 'busy_day.in'
FILE_OUT = 'bd.out'
SCORE = 0

lines = open(FILE_IN).read().splitlines()

R, C, nb_drones, T, max_payload = map(int, lines[0].split())

nb_types = int(lines[1])
weights = map(int, lines[2].split())

nb_warehouses = int(lines[3])
coords_w = [None] * nb_warehouses
stocks = [None] * nb_warehouses
for w in range(nb_warehouses):
    coords_w[w] = list(map(int, lines[4 + 2 * w].split()))
    stocks[w] = list(map(int, lines[4 + 2 * w + 1].split()))

nb_orders = int(lines[4 + 2 * nb_warehouses])
coords_o = [None] * nb_orders
request = [None] * nb_orders
for o in range(nb_orders):
    coords_o[o] = list(map(int, lines[4 + 2 * nb_warehouses + 1 + 3 * o].split()))
    request[o] = Counter(map(int, lines[4 + 2 * nb_warehouses + 1 + 3 * o + 2].split()))

# All drones start at 0
coords_d = [coords_w[0]] * nb_drones
time_d = [-1] * nb_drones
load_d = [Counter() for _ in range(nb_drones)]

delivery_times = {}

def dist(c1, c2):
    return sqrt(pow(c1[0] - c2[0], 2) + pow(c1[1] - c2[1], 2))

def load(drone_id):
    return sum(nb * weights[product_type] for product_type, nb in enumerate(load_d[drone_id]))

with open(FILE_OUT) as f:
    next(f)
    for line in f:
        if 'W' in line or 'U' in line:
            pass
        else:
            drone_id, command, place_id, product_type, quantity = map(lambda x: int(x) if x not in 'DL' else x, line.split())
        if command == 'L':
            time_d[drone_id] += ceil(dist(coords_d[drone_id], coords_w[place_id]))
            # TODO verify there is sufficient stock in warehouse
            coords_d[drone_id] = coords_w[place_id]
            load_d[drone_id][product_type] += quantity
            # TODO verify max_payload
            time_d[drone_id] += 1
            # print('Drone %d loads from warehouse %d at turn %d' % (drone_id, place_id, time_d[drone_id]))
        else:
            time_d[drone_id] += ceil(dist(coords_d[drone_id], coords_o[place_id]))
            coords_d[drone_id] = coords_o[place_id]
            # TODO verify order is respected
            load_d[drone_id][product_type] -= quantity
            request[place_id][product_type] -= quantity
            time_d[drone_id] += 1
            current_time = time_d[drone_id]
            delivery_times.setdefault(place_id, []).append(current_time)
            if all(quantity == 0 for quantity in request[place_id].values()):
                # print('Order %d is satisfied by drone %d at turn %d' % (place_id, drone_id, time_d[drone_id]))
                SCORE += ceil((T - max(delivery_times[place_id])) * 100 / T)
    print('SCORE:', SCORE)
