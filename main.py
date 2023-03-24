from enum import Enum
from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent

# Used for storing the ASCII block type
class BlockType(Enum):
    HASHTAG = "#"
    CIRCLE = "O"
    LINE_POINT = "W"
    PLAYER = "P"
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
    
    
def format_level(list_object, direction):
    list_object = str(list_object)
    if direction == 0:
        list_object = list_object.replace("<BlockType.HASHTAG: '#'>", "BlockType.HASHTAG")
        list_object = list_object.replace("<BlockType.CIRCLE: 'O'>", "BlockType.CIRCLE")
        list_object = list_object.replace("<BlockType.PLAYER: 'P'>", "BlockType.PLAYER")
        return list_object
    elif direction == 1:
        list_object = list_object.replace("BlockType.HASHTAG", "<BlockType.HASHTAG: '#'>")
        list_object = list_object.replace("BlockType.CIRCLE", "<BlockType.CIRCLE: 'O'>")
        list_object = list_object.replace("BlockType.PLAYER", "<BlockType.PLAYER: 'P'>")
        return list_object

def save_level():
    global level

    file = open("level.txt", "w")
    file.write(format_level(level, 0))
    file.close()



def assign_new_array(string: str):
    """
    Transforms the given string into a list of 3D arrays.
    """

    new_array = []
    for i in range(0, len(string), 3):
        temp_array = string[i:i+3]
        new_array.append(temp_array)
    return new_array

def load_level(screen):
    """
    Loads the level.txt file inside of the runtime directory and then
    firstly transforms the string and then passes it to assing_new_array().
    After that it loops through the retrieved list and places a BlockType for every entry.
    """

    global level
    
    file = open("level.txt", "r")

    if file.read() == "":
        return
    file.seek(0) # Making sure that we are not reaching EOF

    # This transforms the save into a for the algorithm readable format.
    no_brackets = file.read().replace("[", "").replace("]", "").split(", ")

    for i in assign_new_array(no_brackets):
        # We are using __members__[] because assign_new_array returns e.g.: `BlockType.HASHTAG` as a string
        # This then has to be transformed into a BlockType. To do this we first split the string at the period.
        # Then we take the second half of the string: `HASHTAG` and then assign that to a BlockType value.
        print_at(screen, int(i[0]), int(i[1]), text=BlockType.__members__[str(i[2]).split(".")[1]])
        append_array(int(i[0]), int(i[1]), BlockType.__members__[str(i[2]).split(".")[1]])

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

    save_level()

def check_if_player_exists(screen):
    """
    This function checks if another player block is already placed and then deletes that if a new one is placed
    """

    global level

    for i in level:
        if BlockType.PLAYER in i:
            print_at(screen, i[0], i[1], text=BlockType.EMPTY)
            del level[level.index(i)]

def check_for_boundaries(posX, posY):
    if posX > 90:
        return False
    if posY > 15:
        return False
    return True


def draw_block_on_mouse(screen, posX: int, posY: int):
    """
    A function that draws a single block given by the BlockType onto the screen at posX and posY
    """

    global selected_block

    if selected_block == BlockType.PLAYER:
        check_if_player_exists(screen)
    if check_for_boundaries(posX, posY):
        print_at(screen, posX, posY, text=selected_block)
        append_array(posX, posY, BlockType=selected_block)
        save_level()


def draw_line_from_positions(screen, posX: int, posY: int):
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

    if check_for_boundaries(posX, posY):
        if(mouse1 == None):
            mouse1 = [posX, posY] # Set first position
            print_at(screen, posX, posY, text=BlockType.LINE_POINT) # Prints the first point of the line

        elif(mouse2 == None):
            mouse2 = [posX, posY] # Set second position
            if line_direction == LineDirection.HORIZONTAL:
                
                # A while loop that places `index` blocks
                index = 0
                while index <= abs(mouse2[0] - mouse1[0]):
                    if mouse2[0] >= mouse1[0]:
                        append_array(mouse1[0] + index, mouse1[1], selected_block)
                    elif mouse2[0] < mouse1[0]:
                        append_array(mouse1[0] - index, mouse1[1], selected_block)
                    index += 1

                print_at(screen, posX, mouse1[1], text=BlockType.LINE_POINT) # Prints the end point of a line bound to the x-axis
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


                print_at(screen, mouse1[0], posY, text=BlockType.LINE_POINT) # Prints end of the line bound to the y-axis
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

    load_level(screen)

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
                if selected_block == BlockType.PLAYER:
                    selected_block = BlockType.HASHTAG
            elif event.key_code == ord('1'):
                selected_block = BlockType.HASHTAG
            elif event.key_code == ord('2'):
                selected_block = BlockType.CIRCLE
            elif event.key_code == ord('p'):
                if drawing_mode == DrawingMode.SINGLE:
                    selected_block = BlockType.PLAYER
            elif event.key_code == ord('0'):
                selected_block = BlockType.EMPTY

        # Checks if the incoming event is a mouse triggered event
        if event is not None and isinstance(event, MouseEvent):
            if event.buttons == MouseEvent.LEFT_CLICK:
                if drawing_mode == DrawingMode.SINGLE:
                    draw_block_on_mouse(screen, event.x, event.y)
                else:
                    draw_line_from_positions(screen, event.x, event.y)

        # Prints the menu at the bottom of the screen
        print_at(screen, 0, screen.height - 1, background_color=screen.COLOUR_BLUE, text=(" Block: {block} ".format(block = selected_block.value if selected_block != BlockType.EMPTY else "EMPTY")))
        print_at(screen, 15, screen.height - 1, background_color=screen.COLOUR_BLUE, text=(" Line: {direction} ".format(direction = str(line_direction.value))))
        print_at(screen, 34, screen.height - 1, background_color=screen.COLOUR_BLUE, text=(" Mode: {mode} ".format(mode = str(drawing_mode.value))))

        screen.refresh()


Screen.wrapper(draw_map)