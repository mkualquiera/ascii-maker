from termcolor import colored

origins = []

def pushOrigin(name):
    origins.append(name)

def popOrigin():
    origins.pop()

def printLogNormal(text):
    print("[",colored(origins[len(origins)-1], "cyan"),"]",text)

def printLogWarning(text):
    print("[",colored(origins[len(origins)-1], "yellow"),"]",text)

def printLogError(text):
    print("[",colored(origins[len(origins)-1], "red"),"]",text)
