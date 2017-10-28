from random import randint

tablelist = []

name = input("What is your name? ")

print("Hello ", name, " let's learn the tables!")

table = int(input("Which table do you want to learn?"))

for x in range(0, 3):
    for y in range(1, 10):
        tablelist.insert(len(tablelist), y)

while len(tablelist) != 0:
    x = randint(0, len(tablelist) - 1)
    num = tablelist[x]
    print("list size: ", len(tablelist))
    print("What is the answer of ", num, " * ", table)
    inp = int(input())
    ans = num * table
    if inp == ans:
        print("That's good!")
        del tablelist[x]
    else:
        print("That's not so good :(")
        print("The answer was: ", ans)


print("Good job! You've finished our lesson for today")