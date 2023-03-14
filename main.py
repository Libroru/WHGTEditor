from enum import Enum
import pyperclip
from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent

# Used for storing the ASCII block type
class BlockType(Enum):
    HASHTAG = "#"
    CIRCLE = "O"
    LINE_POINT = "W"
    EMPTY = " "

# Used for collision checking
class LineDirection(Enum):
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"

# Used for specifying the current drawing mode
class DrawingMode(Enum):
    SINGLE = "SINGLE"
    LINE = "LINE"


line_direction = LineDirection.HORIZONTAL

drawing_mode = DrawingMode.LINE

level = []

selected_block = BlockType.HASHTAG

mouse1 = None
mouse2 = None


def print_at(screen, posX: int, posY: int, text_color = None, background_color = None, text = None):
    """
    A function that draws a pixel onto the screen.

    This is a wrapper function, that makes the code more readble in the end.
    """
    global selected_block

    if not text_color: text_color = screen.COLOUR_WHITE
    if not background_color: background_color = screen.COLOUR_BLACK
    if not text: text = selected_block.value
    elif isinstance(text, BlockType):
        text = text.value 

    screen.print_at(
        text, # Prints ending point on X-Axis
        posX, posY,
        colour=text_color,
        bg=background_color)
    

def append_array(posX: int, posY: int, BlockType: BlockType):
    """
    A function that manipulates the final level array every time, that a block is placed.
    It first gathers the level array and then checks if the given BlockType is an empty or not.
    Depending on that data it either adds a new entry to the given level array or removes one.
    
    If it decides to remove an entry it first checks if the given entry of the level array
    contains the X and Y coordinates of the given points or not. If it does then it deletes this entry.
    """

    global level # Add array entry on mouse click
                 # Remove array entry on mouse click with empty building block
    if(not BlockType == BlockType.EMPTY):
         level.append([posX, posY, BlockType])
    else:
        for i in level:
            if posX in i and posY in i:
                del level[level.index(i)]

    formatted_string = str(level).replace("<BlockType.HASHTAG: '#'>", "BlockType.HASHTAG")
    pyperclip.copy(formatted_string)



def draw_block_on_mouse(screen, posX, posY, BlockType: BlockType):
    """
    A function that draws a single block given by the BlockType onto the screen at posX and posY
    """

    append_array(posX, posY, BlockType)
    print_at(screen, posX, posY, text=BlockType)


def draw_line_from_positions(screen, mouseX, mouseY):
    """
    A function that calculates and draws a line onto the screen.
    To do this, the function saves the coordinates of the starting point (mouse1),
    when used for the first time and then saves the coordinates of the end point (mouse2), when used a second time.

    It then resets the mouse1 and mouse2 coordinates, so that they don't interefere with the new coordinates
    if the function is used again afterwards.
    """

    global mouse1
    global mouse2

    global selected_block

    global line_direction

    if(mouse1 == None):
        mouse1 = [mouseX, mouseY] # Set first position
        print_at(screen, mouseX, mouseY, text=BlockType.LINE_POINT) # Prints the first point of the line

    elif(mouse2 == None):
        mouse2 = [mouseX, mouseY] # Set second position
        if line_direction == LineDirection.HORIZONTAL:
            
            # A while loop that places `index` blocks
            index = 0
            while index <= abs(mouse2[0] - mouse1[0]):
                if mouse2[0] >= mouse1[0]:
                    append_array(mouse1[0] + index, mouse1[1], selected_block)
                elif mouse2[0] < mouse1[0]:
                    append_array(mouse1[0] - index, mouse1[1], selected_block)
                index += 1

            print_at(screen, mouseX, mouse1[1], text=BlockType.LINE_POINT) # Prints the end point of a line bound to the x-axis
            screen.move(mouse1[0], mouse1[1])
            screen.draw(mouse2[0], mouse1[1], char=selected_block.value)

            # Prints over "W", which is used to mark the beginning and end point of a line
            print_at(screen, mouse1[0], mouse1[1])
            print_at(screen, mouse2[0], mouse1[1])

        else:
            # A while loop that places `index` blocks
            index = 0
            while index <= abs(mouse2[1] - mouse1[1]):
                if mouse2[1] >= mouse1[1]:
                    append_array(mouse1[0], mouse1[1] + index, selected_block)
                elif mouse2[1] < mouse1[1]:
                    append_array(mouse1[0], mouse1[1] - index, selected_block)
                index += 1


            print_at(screen, mouse1[0], mouseY, text=BlockType.LINE_POINT) # Prints end of the line bound to the y-axis
            screen.move(mouse1[0], mouse1[1])
            screen.draw(mouse1[0], mouse2[1], char=selected_block.value)
            
            # Prints over "W", which is used to mark the beginning and end point of a line
            print_at(screen, mouse1[0], mouse1[1])
            print_at(screen, mouse1[0], mouse2[1])
            
    # Resets point values
    if(mouse1 != None and mouse2 != None):
                    mouse1 = None
                    mouse2 = None


def draw_map(screen):
    """
    This is the main function that controls the program loop.

    It handles the input and outputs the currently selected BlockType and `line_direction` on the bottom left.
    """

    while True:
        global line_direction
        global selected_block

        global drawing_mode
        
        # Calculates the full width of the frame and then creats a string that fills the entire line
        width = screen.width
        blank_line = ' ' * width


        event = screen.get_event()

        # Checks if the incoming event is a keyboard triggered event
        if event is not None and isinstance(event, KeyboardEvent):

            # Draws a blank line at the coordinates 0, screen.height - 1.
            # This is necessary, since longer words like "horizontal" or "empty" would still be visible
            # if a shorter word is printed over it, e.g.: "VERTICAL L" and "# PTY"
            screen.move(0, screen.height - 1)
            screen.print_at(blank_line, 0, screen.height - 1)
            screen.refresh()


            if event.key_code == screen.KEY_RIGHT or event.key_code == screen.KEY_LEFT:
                line_direction = LineDirection.HORIZONTAL
            elif event.key_code == screen.KEY_UP or event.key_code == screen.KEY_DOWN:
                line_direction = LineDirection.VERTICAL
            elif event.key_code == screen.KEY_TAB:
                drawing_mode = DrawingMode.LINE if (drawing_mode == DrawingMode.SINGLE) else DrawingMode.SINGLE
            elif event.key_code == ord('1'):
                selected_block = BlockType.HASHTAG
            elif event.key_code == ord('2'):
                selected_block = BlockType.CIRCLE
            elif event.key_code == ord('0'):
                selected_block = BlockType.EMPTY

        # Checks if the incoming event is a mouse triggered event
        if event is not None and isinstance(event, MouseEvent):
            if event.buttons == MouseEvent.LEFT_CLICK:
                if drawing_mode == DrawingMode.SINGLE:
                    draw_block_on_mouse(screen, event.x, event.y, BlockType.HASHTAG)
                else:
                    draw_line_from_positions(screen, event.x, event.y)

        # Prints the menu at the bottom of the screen
        print_at(screen, 0, screen.height - 1, background_color=screen.COLOUR_BLUE, text=(" Block: {block} ".format(block = selected_block.value if selected_block != BlockType.EMPTY else "EMPTY")))
        print_at(screen, 15, screen.height - 1, background_color=screen.COLOUR_BLUE, text=(" Line: {direction} ".format(direction = str(line_direction.value))))
        print_at(screen, 34, screen.height - 1, background_color=screen.COLOUR_BLUE, text=(" Mode: {mode} ".format(mode = str(drawing_mode.value))))

        screen.refresh()


Screen.wrapper(draw_map)