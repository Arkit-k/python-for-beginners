person = { 'first_name': "John", 'last_name': "Doe", 'age': 30, 'city': "mumbai" }
print(person)

favorite_number = {
    'john': 10,
    'jane': 20,
    'jill': 30,
    'jack': 40,
    'james': 50,
    }  

for name, number in favorite_number.items():
    print(f"{name.title()}'s favorite number is {number}.")

