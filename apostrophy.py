"""Avoiding Syntax Errors with Strings
 One kind of error that you might see with some regularity is a syntax error. 
A syntax error occurs when Python doesn’t recognize a section of your pro
gram as valid Python code. For example, if you use an apostrophe within 
single quotes, you’ll produce an error. This happens because Python inter
prets everything between the first single quote and the apostrophe as a 
string. It then tries to interpret the rest of the text as Python code, which 
causes errors. """

"""Here’s how to use single and double quotes correctly. Save this program 
as apostrophe.py and then run it:"""

message = "one of the python's strength is its diverse community"
print(message)
#"one of the python's strength is its diverse community"

""" However, if you use single quotes, Python can’t identify where the string 
should end"""

#message = 'One of Python's strengths is its diverse community.'
#print(message)

#see in the above the python found error int single quote 