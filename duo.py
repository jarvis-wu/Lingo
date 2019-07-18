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
currentLanguage = ""

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
    global currentLanguage
    lingo = duolingo.Duolingo(username, password=password)
    currentLanguage = lingo.get_languages(abbreviations=True)[0]
    print(colored("Login successful!", 'green', attrs = ['bold']))
    printUserInfo()

def printUserInfo():
    userInfo = lingo.get_user_info()
    print("Name:", colored(userInfo["fullname"], 'red', attrs = ['bold']), end=" ")
    print("Languages:", colored(userInfo["learning_language_string"], 'red', attrs = ['bold']))
    print("Try out the 'help' command now!")
    waitForCommand()

def waitForCommand():
    command = input(colored('>>> ', 'cyan', attrs = ['bold']))
    handle(command)
    waitForCommand()

def handle(command):
    mainCommand = command.split()[0]
    # TDDO: how to parse parameters?
    if mainCommand == "help":
        print("Try one of the following commands: words, related, vocabulary, exit")
    elif mainCommand == "version":
        print("Lingo v0.1 2019")
    elif mainCommand == "words":
        words = lingo.get_known_words('es')
        for (index, word) in enumerate(words):
            print(index + 1, "\t", word, "\t", "")
    elif mainCommand == "exit":
        print("Quitting Lingo. See ya!")
        sys.exit(0)
    elif mainCommand == "related":
        originalWord = command.split()[1]
        relatedWords = lingo.get_related_words(originalWord)
        printWordList(relatedWords)
    elif mainCommand == "vocabulary":
        words = lingo.get_vocabulary()["vocab_overview"]
        printWordList(words)
    elif mainCommand == "translate":
        originalWord = command.split()[1]
        translations = lingo.get_translations([originalWord], source="en", target="es")[originalWord]
        for translation in translations:
            print(translation)
    else:
        print("Unrecognized command.")

def printWordList(words):
    for (index, word) in enumerate(words):
        coloredIndex = colored(str(index + 1).zfill(5), 'magenta', attrs = ['bold'])
        bar = ""
        numOfBars = round(word["strength"] * 10)
        if numOfBars <= 4:
            bar = colored(numOfBars * "█", 'red')
        elif numOfBars <= 7:
            bar = colored(numOfBars * "█", 'yellow')
        else:
            bar = colored(numOfBars * "█", 'green')
        print('{:<19}{:<20s}{}'.format(coloredIndex, bar, word["word_string"]))

welcome()
