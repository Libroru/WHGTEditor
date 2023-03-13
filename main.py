from enum import Enum
from asciimatics.screen import Screen
from asciimatics.event import MouseEvent

class BlockType(Enum):
    HASHTAG = "#"
    CIRCLE = "O"
    EMPTY = ""

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
    if(mouse1 == None):
        mouse1 = [mouseX, mouseY]
    elif(mouse2 == None):
        mouse2 = [mouseX, mouseY]
        screen.move(mouse1[0], mouse1[1])
        screen.draw(mouse2[0], mouse1[1], char="#")
        mouse1 = None
        mouse2 = None
    screen.print_at("W", # Enum BlockType, which value represents characters, e.g.: '#' or 'O'
                            mouseX, mouse1[1], # Represents the x and y value of a currently selected 2d array (in order)
                            colour=screen.COLOUR_WHITE,
                            bg=screen.COLOUR_BLACK)

def draw_map(screen):
    while True:
        mouseInput = screen.get_event()
        
        if mouseInput is not None and isinstance(mouseInput, MouseEvent):
            if mouseInput.buttons == MouseEvent.LEFT_CLICK:
                #draw_block_on_mouse(screen, mouseInput.x, mouseInput.y, BlockType.HASHTAG)
                draw_line_from_positions(screen, mouseInput.x, mouseInput.y)

        screen.refresh()
        

Screen.wrapper(draw_map)