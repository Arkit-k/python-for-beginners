cars = ['audi' , 'bwm' , 'subaru' , 'toyota']

for car in cars:
      if car == 'bmw':
            print(car.upper())
      else:
            print(car.title())

# difference between this 2 

# this will assign a new value 
car = 'bmw'
"""check the value is equal and return true or false"""
car == 'bmw'
#true

car = 'audi'
car == 'bmw'
#False

"""Ignoring Case When Checking for Equality
 Testing for equality is case sensitive in Python. For example, two values with 
different capitalization are not considered equal:"""
car = 'Audi'
car == 'audi'
#False

car = 'Audi'
car.lower() == 'audi'
True

"""  
Car = 'Audi'
car.lower() == 'audi'
True
car
 'Audi'    """

"""Checking for Inequality"""

requested_topping = 'mushrooms'

if requested_topping != 'anchovies':
      print("Hold the anchovies!")


answer = 17 
if answer != 42:
    print("that is not the correct answer")

age = 34
age >= 24
age <= 54

"""Checking Multiple Conditions
 You may want to check multiple conditions at the same time. For example, 
sometimes you might need two conditions to be True to take an action. Other 
times you might be satisfied with just one condition being True. The keywords 
and and or can help you in these situations"""

age_0 = 22
age_1 = 34
age_0 >= 21 and age_1 >= 21
age_1 = 22
age_0 >= 21 and age_1 >= 21

#better do this
(age_0 >= 21) and (age_1 >= 21) 

"""Using or to Check Multiple Conditions
 The keyword or allows you to check multiple conditions as well, but it 
passes when either or both of the individual tests pass. An or expression 
fails only when both individual tests fail."""

age_0 = 22
age_1 = 18
age_0 >= 21 or age_1 >= 22