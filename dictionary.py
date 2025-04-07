alien = { 'color' : ' green' , 'points' : 5 }

print(alien['color'])
new_points = alien['points']
print(f"You just earned {new_points} points!")
print(alien['points'])

# adding new value to dictionary

alien_0 = {'x_position': 0, 'y_position': 25, 'speed': 'medium'}
print(f"Original position: {alien_0['x_position']}")

if alien_0['speed'] == 'slow':
    x_increment = 1
elif alien_0['speed'] == 'medium':
    x_increment = 2
else:
      x_increment = 3

alien_0['x_position'] = alien_0['x_position'] + x_increment
print(f"New position: {alien_0['x_position']}")

# Removing Key-Value Pairs

alien_0 = {'color': 'green', 'points': 5}
print(alien_0)

del alien_0['points']
print(alien_0)

favorite_languages = {
      'jen': 'python',
      'sarah': 'c',
      'edward': 'ruby',
      'phil': 'python',
      }

print(f"sarah favorite language is {favorite_languages['sarah'].title()}")

# looping through dictionary

user_0 = {
     'username' : 'efermi',
      'first' : 'enrico',
      'last' : 'fermi',
      }

for key , value in user_0.items():
      print(f"\nKey: {key}")
      print(f"Value: {value}")

favorite_languages = {
 'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python',
    }
for name in favorite_languages.keys():
    print(name.title())

friends = ['phil', 'sarah']
for name in favorite_languages.keys():
    print(f"Hi {name.title()}")
    if name in friends:
        language = favorite_languages[name].title()
        print(f"\t{name.title()}, I see you love {language}!")

        for name in sorted(favorite_languages.values()):
            print(f"{name.title()}, thank you for taking the poll.")