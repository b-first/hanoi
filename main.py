# Brandon Fuerst's Hanoi Game - Computer Player

def setUpStacks(level):
    stack_1 = []
    for i in reversed(range(level)):
        stack_1.append(i+1)
    win_stack = stack_1[:]      # Copy list, this is the winning state on stack 3
    return ([stack_1, [], []], win_stack)

def printStacks(stacks, level):
    print()
    for i in reversed(range(level)):
        try:                print(stacks[0][i], end=' ')    # print with new line at the end
        except IndexError:  print(' ', end=' ')
        try:                print(stacks[1][i], end=' ')
        except IndexError:  print(' ', end=' ')
        try:                print(stacks[2][i], end=' ')
        except IndexError:  print(' ', end=' ')
        print()

def checkOdd(num):
    return num % 2

def move(stacks, start, end):
    stacks[end-1].append(stacks[start-1].pop())
    return end-1

def CPUMove(stacks, last_move):
    # Get the number top of stack or 0 if empty stack
    try:                one = stacks[0][len(stacks[0])-1]
    except IndexError:  one = 0
    try:                two = stacks[1][len(stacks[1])-1]
    except IndexError:  two = 0
    try:                three = stacks[2][len(stacks[2])-1]
    except IndexError:  three = 0
    
    # First move
    if two == 0 and three == 0:             # If two and three are empty, then it's the first turn
        level = len(stacks[0])              # Check level
        if checkOdd(level):                 # If odd
            return move(stacks, 1, 3)       # Move t to 3
        elif not checkOdd(level):           # If even
            return move(stacks, 1, 2)       # Move t to 2
    # Stack 1 Moves
    if last_move != 0 and one != 0:                             # last move wasn't to this stack and it has at least one piece
        if one < two and checkOdd(one) != checkOdd(two):        # stack1 less than stack2 and not both odd or even
            return move(stacks, 1, 2)                           # move 1 to 2
        elif one < three and checkOdd(one) != checkOdd(three):  # stack1 less than stack3 and not both odd or even
            return move(stacks, 1, 3)                           # move 1 to 3
        elif two == 0:                                          # stack 2 is empty
            return move(stacks, 1, 2)                           # move 1 to 2
        elif three == 0:                                        # stack 3 is empty
            return move(stacks, 1, 3)                           # move 1 to 3
    # Stack 2 Moves
    if last_move != 1 and two != 0:
        if two < one and checkOdd(two) != checkOdd(one):
            return move(stacks, 2, 1)
        elif two < three and checkOdd(two) != checkOdd(three):
            return move(stacks, 2, 3)
        elif one == 0:
            return move(stacks, 2, 1)
        elif three == 0:
            return move(stacks, 2, 3)
    # Stack 3 Moves
    if last_move != 2 and 3 != 0:
        if three < two and checkOdd(three) != checkOdd(two):
            return move(stacks, 3, 2)
        elif three < one and checkOdd(three) != checkOdd(one):
            return move(stacks, 3, 1)
        elif one == 0:
            return move(stacks, 3, 1)
        elif two == 0:
            return move(stacks, 3, 2)

if __name__ == '__main__':
    level = 4                                       # Number of pieces to play with
    if level < 1: print('\nMust be level 1 or higher\n'); exit()

    stacks, win_stack = setUpStacks(level)          # Set up the board based on level
    print('\nLevel', str(level) + ':')
    printStacks(stacks, level)

    game_over, counter, last_move = False, 1, 0     # last_move start with an arbitrary number, not used for first move
    while not game_over:
        last_move = CPUMove(stacks, last_move)      # CPU move, returns last stack moved to
        printStacks(stacks, level)
        print('Move Counter', counter)
        counter += 1
        if stacks[2] == win_stack:
            game_over = True
            print('\n\nYOU WON!!!\n\n')
            break
