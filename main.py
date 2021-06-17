# Brandon Fuerst
# Hanoi Game
# Playable and Compute Player

import time

level = 5

if level < 1:
    print('\nMust be level 2 or higher\n')
    exit()

def setUpStacks(level):
    stack_1 = []
    for i in reversed(range(level)):
        stack_1.append(i+1)
    win_stack = stack_1[:]      # Copy list, this is the winning state on stack 3
    return ([stack_1, [], []], win_stack)

def printStacks(stacks, level):
    #max_len = max(len(stacks[0]), len(stacks[1]), len(stacks[2]))
    print()
    for i in reversed(range(level)):
        try:
            print(stacks[0][i], end=' ')
        except IndexError:
            print(0, end=' ')
        try:
            print(stacks[1][i], end=' ')
        except IndexError:
            print(0, end=' ')
        try:
            print(stacks[2][i], end=' ')
        except IndexError:
            print(0, end=' ')
        print()

def checkOdd(num):
    return num % 2

def move1to2(stacks):
    stacks[1].append(stacks[0].pop())
    return [0, 1]
def move1to3(stacks):
    stacks[2].append(stacks[0].pop())
    return [0, 2]
def move2to1(stacks):
    stacks[0].append(stacks[1].pop())
    return [1, 0]
def move2to3(stacks):
    stacks[2].append(stacks[1].pop())
    return [1, 2]
def move3to1(stacks):
    stacks[0].append(stacks[2].pop())
    return [2, 0]
def move3to2(stacks):
    stacks[1].append(stacks[2].pop())
    return [2, 1]

def CPUFirstMove(stacks, level):
    if level % 2 == 1:
        last_move = move1to3(stacks)
        return last_move
    elif level % 2 == 0:
        last_move = move1to2(stacks)
        return last_move

def CPUMove(stacks, last_move):
    try:
        one = stacks[0][len(stacks[0])-1]
    except IndexError:
        one = 0
    try:
        two = stacks[1][len(stacks[1])-1]
    except IndexError:
        two = 0
    try:
        three = stacks[2][len(stacks[2])-1]
    except IndexError:
        three = 0
    
    # Look at stack 1
    if last_move[1] != 0:
        if (
            (
                one < two and 
                checkOdd(one) != checkOdd(two)
            ) or
            (two == 0 and one > three)
        ):
            last_move = move1to2(stacks)
            return last_move
        elif (
            one < three and
            (
                (two == 0) or
                (three == 0 and one > two) or
                (three == 0 and checkOdd(one) == checkOdd(two))
            )
        ):
            last_move = move1to3(stacks)
            return last_move

    # Look at stack 2
    if last_move[1] != 1:
        if (
            two < one and
            checkOdd(two) != checkOdd(one)
        ):
            last_move = move2to1(stacks)
            return last_move
        elif (
            two < three and
            checkOdd(two) != checkOdd(three)
        ):
            last_move = move2to3(stacks)
            return last_move

    # Look at stack 3
    if last_move[1] != 2:
        if checkOdd(three) != checkOdd(two) and three < two:
            last_move = move3to2(stacks)
            return last_move
        elif checkOdd(three) != checkOdd(one) and three < one:
            last_move = move3to1(stacks)
            return last_move
        
    return last_move
        
    '''
    # If moved to stack 3 and stack 2 is empty
    if last_move[1] == 2:                   # Last move ended at stack 3

        if not stacks[0]:                   # Stack 1 is empty
            last_move = move2to1(stacks)    # Move stack 2 to 1
            return last_move

        if not stacks[1]:                   # Stack 2 is empty
            last_move = move1to2(stacks)    # Move stack 1 to 2
            return last_move
        
        if last_move[0] == 1:               # Last move started at 1 so it won't fit on stack 3
            if stacks[0][len(stacks[0]-1)] < stacks[1][len(stacks[1]-1)]:   # Last on stack 1 less than last on stack 2
                last_move = move1to2(stacks)    # 2 > 3 > 1, 1 must got to 2
            else:                           # Stack 2 can go to either stack 1 or 3
                if stack[1][]

    
    # If moved to stack 2 and stack 3 is empty
    elif last_move[1] == 1:
        if not stacks[2]:
            last_move = move1to3(stacks)
            return last_move
    

    return last_move
    '''
            

print('\nLevel', str(level) + ':')

stacks, win_stack = setUpStacks(level)
printStacks(stacks, level)

last_move = CPUFirstMove(stacks, level)

game_over = False
counter = 0
while not game_over:
    printStacks(stacks, level)
    print('counter', counter, 'last move', last_move)
    last_move = CPUMove(stacks, last_move)
    
    if stacks[2] == win_stack:
        game_over = True
    
    counter += 1
    if counter == 15:
        exit()
    #time.sleep(.5)

