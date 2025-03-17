""" A list is a collection of items in a particular order. You can make a list that 
includes the letters of the alphabet, the digits from 0–9, or the names of 
all the people in your family. You can put anything you want into a list"""


bicycles = ['trek , cannondale', 'redline' , 'specialized']
print(bicycles)

print(bicycles[1])
print(bicycles[0].title())
print(bicycles[-1])

message = f"my first bicycle was a {bicycles[0].title()}" + "."
print(message)

#try It yourself
friends = ['amon' ,'satan', ' paimon', 'bail', 'balial', 'wine' ,'asmodis' ]
print(friends[0], friends[1],friends[2],friends[3],friends[4],friends[5])


#Changing, adding, and removing elements
#modifing elements 
motorcycles = ['honda ', 'yamaha', 'Suzuki']
print(motorcycles)

motorcycles[0] = 'ducati'
print(motorcycles)
 #this will add value from back of the array
motorcycles.append('duke')
print(motorcycles)

motorcycles.insert(0, 'bugati')
print(motorcycles)

motorcyclese = [] 
motorcyclese.append('honda') 
motorcyclese.append('yamaha') 
motorcyclese.append('suzuki') 
print(motorcyclese)

"""emoving Elements from a List
removing an Item Using the del Statement"""

motor = ['honda' , 'yamaha' , 'suzuki']
print(motor)

del motor[0]
print(motor)

#this will basically delete from the back the last value 
poped_item = motor.pop()
# print(motor)

# #Popping Items from any Position in a List
# poped_item = motor
# poped_item.pop(2)
# print(poped_item)

car = [ 'bmw' , 'mercedies' , 'rr','porse']
print(car)

car.remove('bmw')
print(car)

#python with loops 
magicians = ['alice' , 'david' , 'caroline']
for magician in magicians:
      print(magician)

      print(magician.title() 
            +", that was a great trick!")
      print("I can't wait to see your next trick," + magician.title() + ".\n")

numbers = list(range(1,8))
print(numbers)

even_numbers = list(range(2,11,2))
print(even_numbers)

squares = []
for value in range(1,11):
      squares = value**2

print(squares)

#List Comprehensions

counts = []
for count in range(1,21,2):
      counts.append(count)
       

# million = []
# for numbers in range(1, 1000000000):
#       million.append(numbers)
#       # print(million)
#       print(min(million))
#       print(max(million))
#       print(sum(million))
# cubes = [x**3 for x in range(1, 11)]  # Cubing numbers from 1 to 10
# print(cubes)

#  Slicing a List
players = ['charles', 'martina', 'michael', 'florence', 'eli']
print(players[0:3])
print(players[1:4])
print(players[:4])
print(players[2:])


players = ['charles', 'martina', 'michael', 'florence', 'eli'] 
print("Here are the first three players on my team:")
for player in players[:3]:
      print(player.title())


#copying a list 
my_foods = ['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods[:]

print("my favorite foood are:")
print(my_foods)



