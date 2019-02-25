from PIL import ImageGrab
import time
from pynput.keyboard import Key, Controller, Listener
import threading

keyboard = Controller()

play_area_coords = [753, 675, 1163, 744]

green_coords = [753, 675, 790, 744]
red_coords = [841, 675, 893, 744]
yellow_coords = [935, 675, 983, 744]
blue_coords = [1031, 675, 1075, 744]
orange_coords = [1134, 675, 1163, 744]

GRAY = (160, 160, 160)

RED = (200, 0, 0, 's')
GREEN = (0, 200, 0, 'a')
BLUE = (0, 0, 200, 'k')
YELLOW = (200, 200, 0, 'j')
ORANGE = (200, 128, 0, 'l')

green_detected = False
red_detected = False
yellow_detected = False
blue_detected = False
orange_detected = False

green_note = False
red_note = False
yellow_note = False
blue_note = False
orange_note = False

running = False
prog_running = True

class noteHoldingThread (threading.Thread):
    def __init__(self, colour):
        threading.Thread.__init__(self)
        self.colour = colour
        self.note_length = 0

    def check_for_colour(self):
        global GRAY
        global RED
        global GREEN
        global BLUE
        global YELLOW
        global ORANGE
        global red_coords
        global green_coords
        global blue_coords
        global yellow_coords
        global orange_coords
        global play_area_coords
        global cap
        
        if self.colour == RED:
            start_x = red_coords[0]
            start_y = red_coords[1]
            width = red_coords[2] - red_coords[0]
            height = red_coords[3] - red_coords[1]
        elif self.colour == GREEN:
            start_x = green_coords[0]
            start_y = green_coords[1]
            width = green_coords[2] - green_coords[0]
            height = green_coords[3] - green_coords[1]
        elif self.colour == BLUE:
            start_x = blue_coords[0]
            start_y = blue_coords[1]
            width = blue_coords[2] - blue_coords[0]
            height = blue_coords[3] - blue_coords[1]
        elif self.colour == YELLOW:
            start_x = yellow_coords[0]
            start_y = yellow_coords[1]
            width = yellow_coords[2] - yellow_coords[0]
            height = yellow_coords[3] - yellow_coords[1]
        elif self.colour == ORANGE:
            start_x = orange_coords[0]
            start_y = orange_coords[1]
            width = orange_coords[2] - orange_coords[0]
            height = orange_coords[3] - orange_coords[1]
        
        for y in range(start_y - play_area_coords[1], start_y - play_area_coords[1] + height):
            for x in range(start_x - play_area_coords[0], start_x - play_area_coords[0] + width):
                if ((cap.getpixel((x, y))[0] >= self.colour[0] and
                     cap.getpixel((x, y))[1] >= self.colour[1] and
                     cap.getpixel((x, y))[2] >= self.colour[2]) and not
                    (cap.getpixel((x, y))[0] > GRAY[0] and
                     cap.getpixel((x, y))[1] > GRAY[1] and
                     cap.getpixel((x, y))[2] > GRAY[2])):
                    #print("{0} | {1} | {2} | {3}".format(self.colour, cap.getpixel((x, y)), x + play_area_coords[0], y + play_area_coords[1]))
                    return True
        return False

    def run(self):
        global keyboard

        #start = time.time()
        while self.check_for_colour():
            pass
            #self.note_length += 0.01
        #self.note_length += 0.1

        time.sleep(0.1)
        keyboard.release(self.colour[3])


class notePlayingThread (threading.Thread):
    def __init__(self, key):
        threading.Thread.__init__(self)
        self.key = key

    def run(self):
        play_note(self.key)

def on_press(key):
    global prog_running
    global running
    
    try:
        if key.char == 'p':
            running = not running
            print("Playing= {0}".format(running))
        if key.char == 'c':
            prog_running = False
    except AttributeError:
        pass

def on_release(key):
    pass

def check_for_note(colour):
    global cap
    
    if colour == RED:
        start_x = red_coords[0]
        start_y = red_coords[1]
        width = red_coords[2] - red_coords[0]
        height = red_coords[3] - red_coords[1]
    elif colour == GREEN:
        start_x = green_coords[0]
        start_y = green_coords[1]
        width = green_coords[2] - green_coords[0]
        height = green_coords[3] - green_coords[1]
    elif colour == BLUE:
        start_x = blue_coords[0]
        start_y = blue_coords[1]
        width = blue_coords[2] - blue_coords[0]
        height = blue_coords[3] - blue_coords[1]
    elif colour == YELLOW:
        start_x = yellow_coords[0]
        start_y = yellow_coords[1]
        width = yellow_coords[2] - yellow_coords[0]
        height = yellow_coords[3] - yellow_coords[1]
    elif colour == ORANGE:
        start_x = orange_coords[0]
        start_y = orange_coords[1]
        width = orange_coords[2] - orange_coords[0]
        height = orange_coords[3] - orange_coords[1]
        
    for y in range(start_y - play_area_coords[1], start_y - play_area_coords[1] + height):
        for x in range(start_x - play_area_coords[0], start_x - play_area_coords[0] + width):
            if (cap.getpixel((x, y))[0] >= 230 and
                 cap.getpixel((x, y))[1] >= 230 and
                 cap.getpixel((x, y))[2] >= 230):
                #print("{0} {1}".format(x, y))
                return True
    return False

def play_note(key):
    global keyboard

    keyboard.press(key)
    #time.sleep(0.002)
    keyboard.press(Key.down)
    #time.sleep(0.02)
    keyboard.release(Key.down)
    #time.sleep(0.1)
    #keyboard.release(key)

def do_note(colour):
    playing_note = notePlayingThread(colour[3])
    playing_note.start()

    holding_note = noteHoldingThread(colour)
    holding_note.start()

class noteChecker(threading.Thread):
    def __init__(self, colour):
        threading.Thread.__init__(self)
        self.colour = colour

    def find_note(self):
        global green_detected
        global red_detected
        global yellow_detected
        global blue_detected
        global orange_detected

        global green_note
        global red_note
        global yellow_note
        global blue_note
        global orange_note

        if self.colour == GREEN:
            if green_detected:
                green_detected = check_for_note(GREEN)
                if not green_detected:
                    # Strum green
                    green_note = True

                    print("Green!")
            else:
                green_detected = check_for_note(GREEN)
        elif self.colour == RED:
            if red_detected:
                red_detected = check_for_note(RED)
                if not red_detected:
                    # Strum red
                    red_note = True

                    print("Red!")
            else:
                red_detected = check_for_note(RED)
        elif self.colour == YELLOW:
            if yellow_detected:
                yellow_detected = check_for_note(YELLOW)
                if not yellow_detected:
                    # Strum yellow
                    yellow_note = True

                    print("Yellow!")
            else:
                yellow_detected = check_for_note(YELLOW)
        elif self.colour == BLUE:
            if blue_detected:
                blue_detected = check_for_note(BLUE)
                if not blue_detected:
                    # Strum blue
                    blue_note = True

                    print("Blue!")
            else:
                blue_detected = check_for_note(BLUE)
        elif self.colour == ORANGE:
            if orange_detected:
                orange_detected = check_for_note(ORANGE)
                if not orange_detected:
                    # Strum orange
                    orange_note = True

                    print("Orange!")
            else:
                orange_detected = check_for_note(ORANGE)
                
    def run(self):
        self.find_note()

with Listener(on_press=on_press, on_release=on_release) as listener:
    global cap

    # Start the main script
    while prog_running:
        while running:
            start = time.time()
            # Capture the incoming notes
            cap = ImageGrab.grab(bbox=play_area_coords)
            
            green_note = False
            red_note = False
            yellow_note = False
            blue_note = False
            orange_note = False
        
            note1 = noteChecker(GREEN)
            note1.start()
            note2 = noteChecker(RED)
            note2.start()
            note3 = noteChecker(YELLOW)
            note3.start()
            note4 = noteChecker(BLUE)
            note4.start()
            note5 = noteChecker(ORANGE)
            note5.start()

            if green_note:
                do_note(GREEN)
            if red_note:
                do_note(RED)
            if yellow_note:
                do_note(YELLOW)
            if blue_note:
                do_note(BLUE)
            if orange_note:
                do_note(ORANGE)


            print("{0}ms".format(time.time() - start))
    
listener.stop()
