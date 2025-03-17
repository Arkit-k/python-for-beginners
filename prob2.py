place = ['america' , 'japan', 'koria','hydrabad']

print(place.sort())
print(place.sort(reverse=True))
print(place.reverse())


pizzas = ["chicken" , "barbique" , "montoriko"]
for pizza in pizzas:
      print(pizza)
      print(f"i like {pizza} pizza")

animals = ["dogs" , "cats" , "mota mila"]
for animal in animals:
      print(animal)
      print(f"this will be a great {animal} pet")
      print(f"this animals are cute {animal}")

for value in range(1,5):
      print(value)

year = 2025 
if year == 2025-1:
      print("julala")
elif year == 2024+1:
      print("new year")

valuedo = []
country = ["india" , "japan" , "myanmar" , "malasiya" , "singapor"]
for value in (country[0:3]):
      valuedo.append(value)
      print(value)

print("Final list:", valuedo)

friend_pizza = []
for pizza in pizzas:
      friend_pizza.append(pizza)
      print(friend_pizza)

friend_pizza.append("cheesey")
print (f"my favrate pizza is {pizzas}")
print( f" my friends favrate pizza is {friend_pizza}")