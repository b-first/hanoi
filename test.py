import pygame as pg
from CPU_Player import CPUMove
import time

# Game Vars (global)
level = 8                           # Number of discs
window_width = 500
window_height = 500
stick_x_list = [window_width*.25, window_width*.5, window_width*.75]    # List of stick locations (25%, 50%, 75%)
disc_width_max = (window_width*.25) - 5                                 # Max disc width just less than distance between sticks
disc_height = 15
stacks = [dict(), dict(), dict()]   # [stack0, stack1, stack2] - {disc_number: rect}
# User Vars (global)
disc_move = None                    # Default none, used to track whether user has selected a piece to move [source stack index, top piece's number]
move_counter = 0
win_flag = False
human_player = False
last_move = 0                       # Track CPU's last move
CPU_source = None                   # CPU move's source stick (index)
CPU_target = None                   # CPU move's target stick (index)
time_played = 0
time_reset = 0

# RGB Colors (global)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GOLD = (190, 145, 25)
SILVER = (90, 90, 90)
GREY = (220, 220, 220)
BACKGROUND = (50, 50, 50)

# Create the window display
pg.init()
window = pg.display.set_mode((window_width, window_height))
pg.display.set_caption('Hanoi by B-First')
clock = pg.time.Clock()
text_font = pg.font.SysFont('Comic Sans MS', 30)

# Create Rect to draw Ellipse (args: disc number, stick index)
def createEllipseRect(disc_num, stick_i):
    stick_x = stick_x_list[stick_i]                             # Stick x location
    num_discs_in_stack = len(stacks[stick_i].keys())
    disc_width = (disc_width_max - ((disc_width_max / (level+1)) * (level - disc_num)))     # Make each disc slightly smaller than the last
    ellipse_rect = pg.Rect(                                     # Create rect that ellipse is inscribed into
        stick_x - disc_width/2,                                 # px from left, center on stick
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
    pg.draw.ellipse(window, BLACK, stack[disc_num], 2)          # Add a disc border

# Return top piece in the stack, 0 if no pieces
def getTopPiece(stack):
    try: return min(stack.keys())
    except: return 0

# Select a piece - return stack index and disc number, None if no pieces in stack
def selectPiece(stack_i):
    stack = stacks[stack_i]
    disc_num = getTopPiece(stacks[stack_i])
    if not disc_num: return None                        # If no piece in the stack
    pg.draw.ellipse(window, BLUE, stack[disc_num], 0)   # Redraw with blue color
    disc_move = [stack_i, disc_num]                     # Stack index and top piece's number
    return disc_move

# Move the selected piece, return 1 if successful or 0 if invalid
def movePiece(disc_move, stick_target_i):
    stack_source = stacks[disc_move[0]]
    disc_num = disc_move[1]
    stick_source_x = stick_x_list[disc_move[0]]                         # Source stick's x location
    stack_target = stacks[stick_target_i]
    disc_target = getTopPiece(stack_target)

    if disc_num < disc_target or disc_target == 0:                              # If the piece being moved is less than the top of the target stack or no pieces on target stack
        pg.draw.ellipse(window, BACKGROUND, stack_source[disc_num])             # Clear existing to background color
        stack_source.pop(disc_num)                                              # Remove piece from stack
        stack_target[disc_num] = createEllipseRect(disc_num, stick_target_i)    # Create new ellipse rect
        drawEllipse(disc_num, stack_target)                                     # Draw new ellipse
        pg.draw.line(
            window,
            BLACK,
            (stick_source_x, window_height*.2),
            (stick_source_x, window_height)
        )                                                                       # Redraw line so there's no gap from the piece that moved
        # Redraw remaining discs in source stack to cover the redrawn line
        for disc_num in stack_source:                                           # Loop through dict keys (disc_nums)
            drawEllipse(disc_num, stack_source)
        return 1                                                                # Return 1 to increment move counter
    else:                                                                       # Invalide move
        drawEllipse(disc_num, stack_source)                                     # Turn it from selected (blue) to not
        return 0                                                                # Return 0 to not increment move counter

# Set up the game
def resetGame():
    # Clear game vars
    stacks[0].clear()
    stacks[1].clear()
    stacks[2].clear()
    global win_flag; win_flag = False
    global move_counter; move_counter = 0
    global time_reset; time_reset = pg.time.get_ticks()
    global time_played; time_played = 0
    window.fill(BACKGROUND)
    # Draw the 3 sticks
    pg.draw.line(window, BLACK, (stick_x_list[0], window_height*.2), (stick_x_list[0], window_height))
    pg.draw.line(window, BLACK, (stick_x_list[1], window_height*.2), (stick_x_list[1], window_height))
    pg.draw.line(window, BLACK, (stick_x_list[2], window_height*.2), (stick_x_list[2], window_height))
    # Create and draw pieces in
    for i in reversed(range(1, level+1)):       # Loop through from level down to 1
        stacks[0][i] = createEllipseRect(i, 0)  # Create each ellipse rect in the first stack
        drawEllipse(i, stacks[0])

# Game Loop
resetGame()                         # Set up the discs on the first stack
win_stack = list(stacks[0].keys())  # List to define winning state
while True:

    # Update move counter drawn on surface
    pg.draw.rect(window, WHITE, (0, 0, window_width, 80))                   # Draw rect to cover previous count - left, top, width, height
    move_counter_str = str(move_counter)
    move_counter_len = len(move_counter_str)
    text_move_counter = text_font.render(move_counter_str, True, BLACK)    # Create a text surface
    window.blit(text_move_counter, (window_width/2-(10*move_counter_len), 40))                 # Draw the text surface

    # Check if player won and print win message
    if list(stacks[2].keys()) == win_stack:                                 # If the 3rd stack has the same keys as the original stack
        text_win = text_font.render('Congrats!!!', False, BLACK)
        window.blit(text_win, (window_width/2-70, 0))
        win_flag = True
    
    # Get pygame events (like key presses)
    for event in pg.event.get():

        if event.type == pg.QUIT:                                       # If X-ed out, exit the game and terminate the program
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:     # If Enter is pressed, reset the game
            last_move = 0
            CPU_source = None
            CPU_target = None
            resetGame()
        
        if win_flag: continue                                           # If already won, don't check for moves

        if human_player:
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

    if not human_player and not win_flag:
        if CPU_source is None and CPU_target is None:               # If CPU needs to choose a move
            CPU_source, CPU_target = CPUMove(stacks, last_move)
        elif CPU_source is None:                                    # If piece is selected but not moved yet
            move_counter += movePiece(disc_move, CPU_target)
            last_move = CPU_target
            CPU_target = None
            disc_move = None
        else:                                                       # If piece isn't selected yet
            disc_move = selectPiece(CPU_source)
            CPU_source = None
    
    clock.tick(60)                  # Game FPS

    time_current = round((pg.time.get_ticks() - time_reset)/1000, 0)
    if time_current > time_played and not win_flag:
        time_played = time_current
        print(time_played)
    pg.display.update()
    #time.sleep(.01)

