import pygame as pg

level = 2                                           # Number of discs

window_width = 500
window_height = 500

stick_l_x = window_width*.25                        # Left stick 25% in
stick_m_x = window_width*.5                         # Middle stick 50% in
stick_r_x = window_width*.75                        # Right stick 75% in
stick_x_list = [stick_l_x, stick_m_x, stick_r_x]

disc_width_max = (window_width*.25) - 5
disc_height = 15

stacks = [dict(), dict(), dict()]                   # {disc_number: rect}
disc_move = None                                    # Default none, used to track whether user has selected a piece to move
move_counter = 0
win_flag = False

# RGB Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GOLD = (190, 145, 25)
SILVER = (90, 90, 90)
GREY = (220, 220, 220)

# Create the window display
pg.init()
window = pg.display.set_mode((window_width, window_height))
pg.display.set_caption('Hanoi by B-First')
clock = pg.time.Clock()
GAME_FONT = pg.font.SysFont('Comic Sans MS', 30)

# Create Rect to draw Ellipse
def createEllipseRect(disc_num, stick_x, stick_i):
    discs_in_stack = stacks[stick_i].keys()
    num_discs_in_stack = len(discs_in_stack)
    disc_width = (
        disc_width_max - ((disc_width_max / (level+1)) * (level - disc_num))
    )   # Make each disc slightly smaller than the last
    
    ellipse_rect = pg.Rect(                                     # Rects that ellipses are inscribed into
        stick_x - disc_width/2,                                 # px from left, center on left stick
        window_height - (disc_height*(num_discs_in_stack+1)),   # px from top, stack discs on each other
        disc_width,
        disc_height
    )
    return ellipse_rect

# Draw ellipse
def drawEllipse(disc_num, stack):
    if disc_num % 2 == 0: disc_color = SILVER                   # Even discs are silver
    else: disc_color = GOLD                                     # Odd discs are gold
    pg.draw.ellipse(window, disc_color, stack[disc_num], 0)
    pg.draw.ellipse(window, BLACK, stack[disc_num], 2)          # Add a border

# Return top piece in the stack, 0 if no pieces
def getTopPiece(stack):
    try: return min(stack.keys())
    except: return 0

# Select a piece - return stack index and disc number, None if no pieces in stack
def selectPiece(stack_i):
    stack = stacks[stack_i]
    disc_num = getTopPiece(stack)
    if not disc_num: return None                        # If no piece in the stack
    pg.draw.ellipse(window, BLUE, stack[disc_num], 0)   # Redraw with blue color
    disc_move = [stack_i, disc_num]                     # Stack index and top piece's number
    return disc_move

# Move the selected piece, return 1 if successful or 0 if invalid
def movePiece(disc_move, stick_target_i):
    stack_source = stacks[disc_move[0]]
    disc_num = disc_move[1]
    stick_source_x = stick_x_list[disc_move[0]]
    stack_target = stacks[stick_target_i]
    stick_target_x = stick_x_list[stick_target_i]
    disc_target = getTopPiece(stack_target)

    if disc_num < disc_target or disc_target == 0:              # If the piece being moved is less than the top of the target stack
        pg.draw.ellipse(window, GREY, stack_source[disc_num])   # Clear existing to background color
        stack_source.pop(disc_num)                              # Remove piece from stack

        stack_target[disc_num] = createEllipseRect(disc_num, stick_target_x, stick_target_i)
        drawEllipse(disc_num, stack_target)
    
        pg.draw.line(
            window,
            BLACK,
            (stick_source_x, window_height*.2),
            (stick_source_x, window_height)
        )   # Redraw line so there's no gap from the piece that moved

        # Redraw remaining discs in source stack to cover the redrawn line
        for disc_num in stack_source:                           # Loop through dict keys (disc_nums)
            drawEllipse(disc_num, stack_source)
        
        return 1                                                # Return 1 to increment move counter
    else:
        drawEllipse(disc_num, stack_source)                     # Turn it from selected (blue) to not
        return 0                                                # Return 0 to not increment move counter

# Set up the game
def resetGame():
    stacks[0].clear()
    stacks[1].clear()
    stacks[2].clear()
    global win_flag; win_flag = False
    global move_counter; move_counter = 0
    window.fill(GREY)
    
    # Draw the 3 sticks
    pg.draw.line(window, BLACK, (stick_l_x, window_height*.2), (stick_l_x, window_height))
    pg.draw.line(window, BLACK, (stick_m_x, window_height*.2), (stick_m_x, window_height))
    pg.draw.line(window, BLACK, (stick_r_x, window_height*.2), (stick_r_x, window_height))

    for i in reversed(range(1, level+1)):                   # Loop through from level down to 1
        stacks[0][i] = createEllipseRect(i, stick_l_x, 0)   # Create each ellipse rect in the first stack
        drawEllipse(i, stacks[0])


# Game Loop
resetGame()                         # Set up the discs on the first stack
win_stack = list(stacks[0].keys())  # List to define winning state
while True:
    
    # Update move counter drawn on surface
    pg.draw.rect(window, WHITE, (0, 0, window_width, 80))                   # Draw rect to cover previous count - left, top, width, height
    text_move_counter = GAME_FONT.render(str(move_counter), True, BLACK)    # Create a text surface
    window.blit(text_move_counter, (window_width/2-10, 40))                 # Draw the text surface

    # Check if player won and print win message
    if list(stacks[2].keys()) == win_stack:                                 # If the 3rd stack has the same keys as the original stack
        text_win = GAME_FONT.render('Congrats!!!', False, BLACK)
        window.blit(text_win, (window_width/2-70, 0))
        win_flag = True
    
    # Get pygame events (like key presses)
    for event in pg.event.get():

        if event.type == pg.QUIT:                                       # If X-ed out, exit the game and terminate the program
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:     # If Enter is pressed, reset the game
            resetGame()
        
        if win_flag: continue                                           # If already won, don't check for moves

        if event.type == pg.KEYDOWN:                                    # If a button is pressed
            # Stack index
            if event.key == pg.K_LEFT: stack_i = 0
            elif event.key == pg.K_DOWN: stack_i = 1
            elif event.key == pg.K_RIGHT: stack_i = 2
            else: continue
            
            if not disc_move:                                   # If no piece selected, select it
                disc_move = selectPiece(stack_i)
            else:                                               # If piece selected, move it
                move_counter += movePiece(disc_move, stack_i)   # Increment move counter (0 if failed move)
                disc_move = None                                # Clear variable after move
                print('Move:', move_counter)
    
    clock.tick(20)                  # Game FPS
    #print(pg.time.get_ticks())
    pg.display.update()

