"""Lists work well for storing sets of items that can change throughout the 
life of a program. The ability to modify lists is particularly important when 
you’re working with a list of users on a website or a list of characters in a 
game. However, sometimes you’ll want to create a list of items that cannot 
change. Tuples allow you to do just that. Python refers to values that cannot 
change as immutable, and an immutable list is called a tuple."""

dimension = ("past" , "present" , "Future")
print(dimension[0])
print(dimension[1])

""" its immutable we can chnage value 
dimension[0] =  150
print(dimension) """

for dimension in dimension:
      print(dimension)
"""overwriting a value is valid"""
dimension = (200 , 300)
print(dimension)