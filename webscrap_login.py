# marvin
# date:2018/2/7

import getpass
# login stage preparation

def login_values():
    login="https://www.tianyancha.com/login"
    username = input("Please insert your username: ") 
    password = getpass.getpass("Please type in your password: ")
    #host="www.tianyancha.com"
    #store login screts
    data = {
        "username": username, 
        "password": password, 
    }
    return login,data