# Jarvis Wu, 2019
# Duolingo Command Line App
# Dependency: duolingo-api (https://github.com/KartikTalwar/Duolingo)

import duolingo

lingo = None

def welcome():
    print("Welcome to Lingo, the Duolingo CLI app.")
    askLogin()

def askLogin():
    myUsername = input("Enter your username: ")
    myPassword = input("Enter your password: ")
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}
    choice = input("Do you want to log in? [y/n]: ").lower()
    if choice in yes:
       login(myUsername, myPassword)
    elif choice in no:
       welcome()
    else:
       print("Please respond with 'y' or 'n'")

def login(username, password):
    global lingo
    lingo = duolingo.Duolingo(username, password=password)
    printUserInfo()

def printUserInfo():
    userInfo = lingo.get_user_info()
    for key, value in userInfo.items() :
        print(key)

welcome()
