def greet_user():
      print('Hello')

greet_user()

# passing information in the function

def greet_user(username):
      print(f'hello {username.title()}')
greet_user('jeede')

def display_message(language):
      print(f'i am learning {language}')
display_message('python')

def favorite_book(book):
      print(f' my favorite books is {book}')

favorite_book('girl with the dragon tattoo')

# positional argument
def describe_pet(animal_type, pet_name):
      print(f"\n my breed of animal is {animal_type} and pet name is {pet_name}")
describe_pet('hamster' , 'harry')

def Tshirt(size='l' , printed='i love python'):
      print(f"my size is {size} and you have to print {printed} in the tshirt ")
Tshirt(22 , ' i am tyler derdn')

def get_formatted_name(first_name , last_name):
      full_name = first_name + ' ' + last_name
      return full_name.title()
musician = get_formatted_name('jimi', 'hendrix')
print(musician)

def get_formatted_name(first_name, last_name, middle_name=''):
     if middle_name:
          full_name = first_name + ' ' + middle_name + ' ' + last_name
     else:
          full_name = first_name + ' ' + last_name
          return full_name.title()
musiciane = get_formatted_name('jimi', 'hendrix')
print(musician)
musiciane = get_formatted_name('john', 'hooker', 'lee')