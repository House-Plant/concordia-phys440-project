import math

radius = 3.0
height = 5
area = math.pi * radius**2
volume = area * height
distance = math.sqrt(3**2 + 4**2)


def calculate_total(price, quantity=2, tax_rate=0.15):
    subtotal = price * quantity
    return subtotal * (1 + tax_rate)


measurements = [1, 2, 3, 4, 5]
average = sum(measurements) / len(measurements)
results = {
    "area": area,
    "volume": volume,
    "distance": distance,
    "average": average,
    "total": calculate_total(19.99, quantity=3),
}
print(results)
