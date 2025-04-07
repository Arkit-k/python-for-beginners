message = input("Enter a message: ")
print("You entered:", message)
print("The message has", len(message), "characters.")
print("The message in uppercase is:", message.upper())
print("The message in lowercase is:", message.lower())
print("The message in title case is:", message.title())
print("The message in reverse is:", message[::-1])
print("The first character of the message is:", message[0])
print("The last character of the message is:", message[-1])
print("The message without leading spaces is:", message.lstrip())
print("The message without trailing spaces is:", message.rstrip())


print = "if you want to know more about python programming, please visit python.org"

height = input("Enter your height in cm: ")
height = int(height)

if height >= 150:
    print("You are tall enough to ride the roller coaster!")