a = 10
b = 20
c = 30

print(a < b and b < c)
print(a > b and b < c)
print(a > b or b < c and c > a)

fruits = ["apple" , "banana" , "cherry"]

print("banana" in fruits)
print("grape" in fruits)

fruits

alien_color = ['green' , 'yellow' , 'red']
value = input("enter a guess color ")
congo = value.strip()
for  color in alien_color:
      if color == congo:
            print("10 points added")

if alien_color == 'green':
      print('color is green')
elif alien_color == 'yellow':
      print('color is yellow')
elif alien_color == 'red':
      print('color is red')
else:
      print('not found match')




age = int(input('enter your age'))
if age <= 2:
      print(" oyee cute baby")
elif age >= 2 and age <= 4:
      print("he is a little champ ")
elif age >= 4 and age <=  13:
      print("yeo bacha bada horahai")
elif age >= 13 and age <= 20:
      print("bhai tenager bangaya")
elif age >= 20 and age <= 30:
      print("girlfriend banale bhai")
elif age >= 30 and age <= 60:
      print('elder')
else :
      print('atleast give me a valid input')