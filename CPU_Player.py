# Return top piece in the stack, 0 if no pieces
def getTopPiece(stack):
    try: return min(stack.keys())
    except: return 0

def checkOdd(num):
    return num % 2

# CPU Move
def CPUMove(stacks, last_move):
    # Get the number top of stack or 0 if empty stack
    one = getTopPiece(stacks[0])
    two = getTopPiece(stacks[1])
    three = getTopPiece(stacks[2])
    
    # First move
    if two == 0 and three == 0:             # If two and three are empty, then it's the first turn
        level = len(stacks[0])              # Check level
        if checkOdd(level):                 # If odd
            return 0, 2                     # Move 0 to 2
        elif not checkOdd(level):           # If even
            return 0, 1                     # Move 0 to 1
    # Stack 1 Moves
    if last_move != 0 and one != 0:                             # last move wasn't to this stack and it has at least one piece
        if one < two and checkOdd(one) != checkOdd(two):        # stack1 less than stack2 and not both odd or even
            return 0, 1
        elif one < three and checkOdd(one) != checkOdd(three):  # stack1 less than stack3 and not both odd or even
            return 0, 2
        elif two == 0:                                          # stack 2 is empty
            return 0, 1
        elif three == 0:                                        # stack 3 is empty
            return 0, 2
    # Stack 2 Moves
    if last_move != 1 and two != 0:
        if two < one and checkOdd(two) != checkOdd(one):
            return 1, 0
        elif two < three and checkOdd(two) != checkOdd(three):
            return 1, 2
        elif one == 0:
            return 1, 0
        elif three == 0:
            return 1, 2
    # Stack 3 Moves
    if last_move != 2 and 3 != 0:
        if three < two and checkOdd(three) != checkOdd(two):
            return 2, 1
        elif three < one and checkOdd(three) != checkOdd(one):
            return 2, 0
        elif one == 0:
            return 2, 0
        elif two == 0:
            return 2, 1
