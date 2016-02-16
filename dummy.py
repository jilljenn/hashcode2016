from collections import Counter
from math import sqrt, floor, ceil
# from heapq import heappush, heappop

FILE_IN = 'test.in'
FILE_OUT = 'test.out'
FILE_IN = 'busy_day.in'
FILE_IN = 'mother_of_all_warehouses.in'
FILE_IN = 'redundancy.in'
FILE_OUT = 'bidon.out'
SCORE = 0

lines = open(FILE_IN).read().splitlines()

R, C, nb_drones, T, max_payload = map(int, lines[0].split())

nb_types = int(lines[1])
weights = list(map(int, lines[2].split()))

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

def heuristic(order_id):
    warehouses = range(nb_warehouses)
    todo = request[order_id].copy()
    kept_warehouses = {}
    for w in sorted(warehouses, key=lambda w: dist(coords_w[w], coords_o[order_id])):
        for product_type in todo:
            quantity = min(stocks[w][product_type], todo[product_type])
            if quantity:
                todo[product_type] -= quantity
                if w not in kept_warehouses:
                    kept_warehouses[w] = Counter()
                kept_warehouses[w][product_type] += quantity
        if sum(todo.values()) == 0:
            break
    nb_travels_required = {}
    for w in kept_warehouses:
        # Dispatch deliveries between drones
        nb_drones_per_warehouse = Counter()
        for product_type, requested_quantity in kept_warehouses[w].items():
            max_quantity_per_drone = floor(max_payload / weights[product_type])
            nb_travels_required[w] = ceil(requested_quantity / max_quantity_per_drone)
    return sum(nb_travels_required[w] * dist(coords_w[w], coords_o[order_id]) for w in kept_warehouses)

orders = range(nb_orders)
warehouses = range(nb_warehouses)
deliveries = []
for o in sorted(orders, key=lambda o: heuristic(o)):
    todo = request[o].copy()
    kept_warehouses = {}
    for w in sorted(warehouses, key=lambda w: dist(coords_w[w], coords_o[o])):
        for product_type in todo:
            quantity = min(stocks[w][product_type], todo[product_type])
            if quantity:
                todo[product_type] -= quantity
                if w not in kept_warehouses:
                    kept_warehouses[w] = Counter()
                kept_warehouses[w][product_type] += quantity
        if sum(todo.values()) == 0:
            break
    # print(o, kept_warehouses)
    # On répartit les commandes comme des sales
    # print(kept_warehouses)
    for w in kept_warehouses:
        # print(w, todo)
        for product_type, requested_quantity in kept_warehouses[w].items():
            max_quantity_per_drone = floor(max_payload / weights[product_type])
            quantity = min(requested_quantity, max_quantity_per_drone)
            while requested_quantity:
                deliveries.append((w, o, product_type, quantity))
                stocks[w][product_type] -= quantity
                requested_quantity -= quantity

drone_id = 0
print(2 * len(deliveries))
for w, o, product_type, quantity in deliveries:
    print('%d L %d %d %d' % (drone_id, w, product_type, quantity))
    print('%d D %d %d %d' % (drone_id, o, product_type, quantity))
    drone_id = (drone_id + 1) % nb_drones
