# Jarvis Wu, 2019
# Duolingo Command Line App
# Dependency: duolingo-api (https://github.com/KartikTalwar/Duolingo)

import duolingo
import sys

lingo = None
username = ""
password = ""

def welcome():
    print("Welcome to Lingo, the Duolingo CLI app.")
    getCredentials()

def getCredentials():
    global username, password
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    askLogin()

def askLogin():
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}
    choice = input("Do you want to log in? [y/n]: ").lower()
    if choice in yes:
        login()
    elif choice in no:
        print("Login aborted.")
        welcome()
    else:
        print("Please respond with 'y' or 'n'")
        askLogin()

def login():
    global lingo
    lingo = duolingo.Duolingo(username, password=password)
    print("Login successful!")
    printUserInfo()

def printUserInfo():
    userInfo = lingo.get_user_info()
    print("Name:", userInfo["fullname"])
    print("Id:", userInfo["id"])
    print("Languages:", userInfo["learning_language_string"])
    print("Try out the 'help' command now!")
    waitForCommand()

def waitForCommand():
    command = input(">>> ")
    handle(command)
    waitForCommand()
    # or use while true?

def handle(command):
    print("Command", command, "called.")
    if command == "help":
        print("Try one of the following commands: words, exit")
    elif command == "words":
        words = lingo.get_known_words('es')
        for (index, word) in enumerate(words):
            print(index + 1, "\t", word)
    elif command == "exit":
        sys.exit(0)

welcome()
