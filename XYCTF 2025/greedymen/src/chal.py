import math
import random
from secret import level1,level2,level3
def menu():
    print("1.Play")
    print("2.Rules")
    print("3.Quit")
def rule():
    print("There are 3 levels, level 1/2/3 has number 1 to 50/100/200 on board to choose from")
    print("Each number you choose, you get the corresponding points")
    print("However, your opponent will choose all the factors of the number you choose, and get the points of each factor")
    print("You can not choose numbers that are already assigned to a player")
    print("You are only allow to choose the number if it has at least one factor not choosen")
    print("If you can't choose anymore, the rest of the board goes to your opponent")
    print(f"To make the challenge harder, there is a counter that starts with {len(level1)}/{len(level2)}/{len(level3)} in level 1/2/3, each time you choose a number, the counter decreases by 1")
    print("When it reaches 0, and the game will end, and the unassigned numbers will go to your opponent")
    print("The challenge is always solvable")
    print("Player with highest score wins")
    print("Good Luck!")

def choosable(num):
    for i in range(1,len(num)):
        if num[i]==0:
            for j in range(1,i//2+1):
                if num[j]==0 and i%j==0:
                    return True 

    return False

def can(arr,num):
    for j in range(1,num//2+1):
        if arr[j]==0 and num%j==0:
            return True
    return False

def game(level):
    player=0
    opp=0
    num=[0 for _ in range(level+1)]
    if level==50:
        counter = len(level1)
    elif level==100:
        counter = len(level2)
    elif level==200:
        counter = len(level3)
    while choosable(num):
        num_list = [i for i in range(1,level+1) if num[i]==0]
        print("Unassigned Numbers:",num_list)
        print("Counter:", counter)
        print("Your Score:", player)
        print("Opponent Score:", opp)
        try:
            choice=int(input("Choose a Number:"))
        except ValueError:
            print("Invalid Input!")
            continue
        if choice<=0 or choice>level:
            print("BAD CHOICE!")
        elif num[choice]==0 and can(num,choice):
            num[choice]=1
            player+=choice
            for i in range(1, choice//2+1):
                if num[i] == 0 and choice % i == 0:
                    num[i] = 1
                    opp += i
            counter -= 1
            if counter == 0:
                break
        else:
            if not num[choice]==0:
                print(f"BAD CHOICE! The number {choice} has already been assigned!")
            else:
                print(f"BAD CHOICE! All factors of the number {choice} has been assigned!")
    for i in range(1,level+1):
        if num[i]==0:
            num[i]= 1
            opp+=i
    print("Your Score:", player)
    print("Opponent Score:", opp)
    if player>opp:
        print("You Win!")
        return True
    else:
        print("You Lost!")
        return False


print("Welcome to the Greedy Game")
print("Your goal is to be as greedy as possible")
while True:
    menu()
    choice=int(input())
    if choice==1:
        flag=True
        for i in range(3):
            print("Level "+str(i+1)+"/"+"3",25*i**2+25*i+50,"Numbers")
            if not game(25*i**2+25*i+50):
                flag=False
                break
        if flag:
            print("Congratulations!, Here's Your Flag " + 'flag{Greed, is......key of the life.}')
            exit()
    elif choice==2:
        rule()
    elif choice==3:
        exit()
    else:
        print("HEY!")