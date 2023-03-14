from enum import Enum
import asyncio
import pyperclip
from asciimatics.screen import Screen
from asciimatics.event import MouseEvent, KeyboardEvent

class BlockType(Enum):
    HASHTAG = "#"
    CIRCLE = "O"
    EMPTY = ""

class LineDirection(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

line_direction = LineDirection.HORIZONTAL

level = []


mouse1 = None
mouse2 = None

def append_array(posX, posY, BlockType: BlockType):
    global level # Add array entry on mouse click
                 # Remove array entry on mouse click with empty building block
    if(not BlockType == BlockType.EMPTY):
         level.append([posX, posY, BlockType])
    else:
         level.remove([posX, posY])
    formatted_string = str(level).replace("<BlockType.HASHTAG: '#'>", "BlockType.HASHTAG")
    pyperclip.copy(formatted_string)

def draw_block_on_mouse(screen, posX, posY, BlockType: BlockType):
    append_array(posX, posY, BlockType.value)
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
            
            index = 0
            while index <= abs(mouse2[0] - mouse1[0]):
                if mouse2[0] >= mouse1[0]:
                    append_array(mouse1[0] + index, mouse1[1], BlockType.HASHTAG)
                elif mouse2[0] < mouse1[0]:
                    append_array(mouse1[0] - index, mouse1[1], BlockType.HASHTAG)
                index += 1

            screen.print_at("W", # Prints ending point on X-Axis
                                    mouseX, mouse1[1],
                                    colour=screen.COLOUR_WHITE,
                                    bg=screen.COLOUR_BLACK)
            screen.move(mouse1[0], mouse1[1])
            screen.draw(mouse2[0], mouse1[1], char="#")

        else:
            index = 0
            while index <= abs(mouse2[1] - mouse1[1]):
                if mouse2[1] >= mouse1[1]:
                    append_array(mouse1[0], mouse1[1] + index, BlockType.HASHTAG)
                elif mouse2[1] < mouse1[1]:
                    append_array(mouse1[0], mouse1[1] - index, BlockType.HASHTAG)
                index += 1

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
        

        event = screen.get_event()

        if event is not None and isinstance(event, KeyboardEvent):
            if event.key_code == screen.KEY_RIGHT or event.key_code == screen.KEY_LEFT:
                line_direction = LineDirection.HORIZONTAL
            elif event.key_code == screen.KEY_UP or event.key_code == screen.KEY_DOWN:
                line_direction = LineDirection.VERTICAL

        if event is not None and isinstance(event, MouseEvent):
            if event.buttons == MouseEvent.LEFT_CLICK:
                #draw_block_on_mouse(screen, mouseInput.x, mouseInput.y, BlockType.HASHTAG)
                draw_line_from_positions(screen, event.x, event.y)

        screen.refresh()


Screen.wrapper(draw_map)