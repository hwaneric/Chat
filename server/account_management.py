def username_exists(username):
    return username in existing_users

# check that username exists, if not wah prompt them again with a 
# false success message, if yes then create account and give true 
# success message
def create_account(username, password): 
    if username_exists(username):
        return {success: False, message: "Username already exists. Please try again."}
    else:
        return {success: True, message: "Account created successfully."}

# same thing as create_account but additionally check that password 
# matches the username 
def login(username, password):
    