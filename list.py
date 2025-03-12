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
print(motor)

#Popping Items from any Position in a List
poped_item = motor.pop(3)
print(motor)

car = [ 'bmw' , 'mercedies' , 'rr','porse']
print(car)

car.remove('bmw')
print(car)
