current_users  = ['raja' , 'admin' , 'mohan' , 'krisak' , 'rajesh', 'tilak']
new_users = ['anil', 'pratab','hasan' 'admin' , 'kauja' ]

# if current_users :
#       for username in current_users :
#             if username == 'admin':
#                   print(' hello admin welcome to the portal ')
#                   print(f'welcome to our website {username} have a nice day')
# else:
#       print('we need to find some users')

for new_user in new_users:
    duplicate = False  # Flag to track if a duplicate is found
    for current_user in current_users:
        if new_user.lower() == current_user.lower():  # Convert both to lowercase for case-insensitive comparison
            duplicate = True
            break  # Stop checking once a duplicate is found
    if duplicate:
        print(f"Username '{new_user}' already exists. Please choose a different one.")
    else:
        print(f"Username '{new_user}' is available.")

numbers = [ 1 , 2 , 3 , 4, 5, 6 , 7 ,8 , 9]

for number in numbers:
    if number == 1 :
        print(f"{number}st")
    elif number == 2:
        print(f"{number}nd")
    elif number == 3:
        print(f"{number}3rd")
    else :
        print(f"{number}th")