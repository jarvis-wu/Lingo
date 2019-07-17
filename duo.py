# Jarvis Wu, 2019
# Duolingo Command Line App
# Dependency: duolingo-api (https://github.com/KartikTalwar/Duolingo)

import sys
import duolingo
from termcolor import colored
import getpass

lingo = None
username = ""
password = ""

def welcome():
    print("Welcome to Lingo, the Duolingo CLI app.")
    getCredentials()

def getCredentials():
    global username, password
    username = input(colored("Enter your username >>> ", 'cyan', attrs = ['bold']))
    password = getpass.getpass(prompt = colored("Enter your password >>> ", 'cyan', attrs = ['bold']))
    askLogin()

def askLogin():
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}
    choice = input(colored("Do you want to log in? [y/n] >>> ", 'cyan', attrs = ['bold'])).lower()
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
    print(colored("Login successful!", 'green', attrs = ['bold']))
    printUserInfo()

def printUserInfo():
    userInfo = lingo.get_user_info()
    print("Name:", userInfo["fullname"])
    print("Id:", userInfo["id"])
    print("Languages:", userInfo["learning_language_string"])
    print("Try out the 'help' command now!")
    waitForCommand()

def waitForCommand():
    command = input(colored('>>> ', 'cyan', attrs = ['bold']))
    handle(command)
    waitForCommand()

def handle(command):
    print("Command", command, "called.")
    if command == "help":
        print("Try one of the following commands: words, related, vocabulary, exit")
    elif command == "version":
        print("Lingo v0.1 2019")
    elif command == "words":
        words = lingo.get_known_words('es')
        for (index, word) in enumerate(words):
            print(index + 1, "\t", word, "\t", "")
    elif command == "exit":
        sys.exit(0)
    elif command.split()[0] == "related":
        originalWord = command.split()[1]
        relatedWords = lingo.get_related_words(originalWord)
        printWordList(relatedWords)
    elif command == "vocabulary":
        words = lingo.get_vocabulary()["vocab_overview"]
        printWordList(words)

def printWordList(words):
    for (index, word) in enumerate(words):
        print('{}\t{:<25s}'.format(index + 1, word["word_string"]), end="")
        numOfBars = round(word["strength"] * 10)
        if numOfBars <= 4:
            print(colored(numOfBars * "*", 'red', attrs = ['bold']))
        elif numOfBars <= 7:
            print(colored(numOfBars * "*", 'yellow', attrs = ['bold']))
        else:
            print(colored(numOfBars * "*", 'green', attrs = ['bold']))

welcome()
