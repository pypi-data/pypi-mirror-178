import stern
def sumAB(a,b):
    return a - b
def SealN():
    n=5
    string="Hello beautiful world of programming! "
    print(string * n)
def flip():
    a = "stern"
    print(a[::-1])
def IPS():
    x = 91
    y = 56
    print(x,y)
    x, y = y, x
    print(x,y)
def letters():
    s = "sTeRn"
    print(s.lower())
    print(s.upper())
def listletters():
    s = "stern"
    print(list(s))
def unique():
    x = [1,9,9,1]
    if(len(x) == len(set(x))):
        print("The list is unique")
    else:
        print("The list is NOT unique")
while True:
    print("1. Welcome")
    print("2. sum0391")
    print("3. SealN")
    print("4. Flip")
    print("5. In-Place Swapping")
    print("6. Case of Letters")
    print("7. Word to spell")
    print("8. Unique")
    print("0. Quit")
    cmd = input("Select an item: ")
    
    if cmd == "1":
        print("Welcome to the module Stern! Thank you for downloading this module!")
    elif cmd == "2":
        print(sumAB(2003, 1991))
    elif cmd == "3":
        SealN()
    elif cmd == "4":
        flip()
    elif cmd == "5":
        IPS()
    elif cmd == "6":
        letters()
    elif cmd == "7":
        listletters()
    elif cmd == "8":
        unique()
    elif cmd == "0":
        exit()
    else:
        print("You entered an invalid value")