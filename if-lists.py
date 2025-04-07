"""You can do some interesting work when you combine lists and if state
ments. You can watch for special values that need to be treated differently 
than other values in the list"""

requested_toppings = ['mushrooms' , 'green peeppers', 'french fries' , 'extra cheese']
for requested_topping in requested_toppings:
      if requested_toppings == 'mushroom':
            print('sorry we are out of green pepper')
      else :
            print('are you sure you want a pizza')
      print("adding" + requested_toppings + ".")
print("\n Finised making your pizza! ")

available_toppings = ['mushrooms', 'olives', 'green peppers',
                      'pepperoni', 'pineapple', 'extra cheese']

for requested_topping in requested_toppings:
      if requested_toppings in available_toppings:
            print("adding" + requested_topping + ". ")
      else:
            print('sorry we dont have' + requested_topping + ".")
