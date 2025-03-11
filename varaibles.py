message = "hello world python"
print(message)
message = " Hello python "
print(message)

name = "ada lovelace"
#this will make the titile a and l capital 
print(name.title())
print(name.lower())
print(name.upper())

#concatinating strings 

first_name = "ada"
second_name = "loveable"
final_name = first_name + " " + second_name

print(final_name)

#This method of combining strings is called concatenation.

favrate_language = '    python     '

#To remove the whitespace from the string, you strip the whitespace 
#from the right side of the string and then store that value back in the origi
#nal variable
print(favrate_language.rstrip())
#this will strip from both left and right as well 
print(favrate_language.strip())
 