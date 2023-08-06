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
    string = "Stern"
    print(string.swapcase())
    print(string.lower())
    print(string.upper())
def listletters():
    s = "stern"
    print(list(s))
def unique():
    x = [1,9,9,1]
    if(len(x) == len(set(x))):
        print("The list is unique")
    else:
        print("The list is NOT unique")
def forelse():
    numbers = [2,4,6,8,1]
    for number in numbers:
        if number % 2 == 1:
            print(number)
            break
        else:
            print("No odd numbers")
def difference():
    first = [1,2,3]
    second = [1,2,3]
    print(first == second)
    print(first is second)
    third = first
    print(first is third)
def duplicates():
    list_numbers = [20,22,24,26,28,28,20,30,24]
    print('Before:',list_numbers)
    list_numbers = list(set(list_numbers))
    print('After:',list_numbers)
while True:
    print("1. Welcome")
    print("2. sum0391")
    print("3. SealN")
    print("4. Flip")
    print("5. In-Place Swapping")
    print("6. Case of Letters")
    print("7. Word to spell")
    print("8. Unique")
    print("9. For Else construct")
    print("10. Difference between == u is")
    print("11. Removing duplicates")
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
    elif cmd == "9":
        forelse()
    elif cmd == "10":
        difference()
    elif cmd == "11":
        duplicates()
    elif cmd == "0":
        exit()
    else:
        print("You entered an invalid value")