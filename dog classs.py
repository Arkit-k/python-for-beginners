class Dog():

      def __init__(self, name, breed):
          self.name = name
          self.breed = breed

      def sit(self):
          print(self.name.title() + " is now sitting.")

      def roll_over(self):
          print(self.name.title() + " rolled over!")

my_dog = Dog('willie', 'bulldog')
print("My dog's name is " + my_dog.name.title() + ".")
print("My dog is " + my_dog.breed + ".")

my_dog.sit()
my_dog.roll_over()
