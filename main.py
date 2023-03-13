from enum import Enum
from asciimatics.screen import Screen
from asciimatics.event import MouseEvent

class BlockType(Enum):
    HASHTAG = "#"
    CIRCLE = "O"
    EMPTY = ""

class LineDirection(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

line_direction = LineDirection.HORIZONTAL

mouse1 = None
mouse2 = None

def draw_block_on_mouse(screen, posX, posY, BlockType: BlockType):
    screen.print_at(BlockType.value, # Enum BlockType, which value represents characters, e.g.: '#' or 'O'
                            posX, posY, # Represents the x and y value of a currently selected 2d array (in order)
                            colour=screen.COLOUR_WHITE,
                            bg=screen.COLOUR_BLACK)

def draw_line_from_positions(screen, mouseX, mouseY):
    global mouse1
    global mouse2

    global line_direction

    if(mouse1 == None):
        mouse1 = [mouseX, mouseY] # Set first position
        screen.print_at("W", # Prints starting point
                            mouseX, mouseY,
                            colour=screen.COLOUR_WHITE,
                            bg=screen.COLOUR_BLACK)
    elif(mouse2 == None):
        mouse2 = [mouseX, mouseY] # Set second position
        if line_direction == LineDirection.HORIZONTAL:
            screen.print_at("W", # Prints ending point on X-Axis
                                    mouseX, mouse1[1],
                                    colour=screen.COLOUR_WHITE,
                                    bg=screen.COLOUR_BLACK)
            screen.move(mouse1[0], mouse1[1])
            screen.draw(mouse2[0], mouse1[1], char="#")

        else:
            screen.print_at("W", # Prints ending point on Y-Axis
                                    mouse1[0], mouseY,
                                    colour=screen.COLOUR_WHITE,
                                    bg=screen.COLOUR_BLACK)
            screen.move(mouse1[0], mouse1[1])
            screen.draw(mouse1[0], mouse2[1], char="#")
            
    if(mouse1 != None and mouse2 != None):
                    mouse1 = None
                    mouse2 = None
    

def draw_map(screen):
    while True:
        global line_direction

        mouseInput = screen.get_event()
        keyboardInput = screen.get_key()

        if keyboardInput == screen.KEY_RIGHT or keyboardInput == screen.KEY_LEFT:
            line_direction = LineDirection.HORIZONTAL

        if keyboardInput == screen.KEY_UP or keyboardInput == screen.KEY_DOWN:
            line_direction = LineDirection.VERTICAL
        
        if mouseInput is not None and isinstance(mouseInput, MouseEvent):
            if mouseInput.buttons == MouseEvent.LEFT_CLICK:
                #draw_block_on_mouse(screen, mouseInput.x, mouseInput.y, BlockType.HASHTAG)
                draw_line_from_positions(screen, mouseInput.x, mouseInput.y)

        screen.refresh()
        

Screen.wrapper(draw_map)