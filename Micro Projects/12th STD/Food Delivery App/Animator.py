import os
import time


class Animation:

    TERMINAL_SIZE_COLUMN = os.get_terminal_size().columns
    PADDING_CHAR = "*"
    ANIMATION_PATTERN_LIST = [
        "--+++-+--+_=_++_=_+_=",
        ">>>>>--------->>>>>>>>>",
        "------------->>>>>",
        " - - - - - - - - - - - -",
        "-_-_-_________--_-_----__-_-___-_-_-__-___--",
        "<<<<<<<<<<<<<<<<<<<<<<<<<",
        ".........................",
        "'-'-->.-.-->'-'-->.-.",
        "############------"
        ".",
        ".    .    .    .   .   .",
        "..."
    ]

    # Prints message without newline
    def endless_print(self, message):
        print(message, end="")

    # Prints message slowly (Slow Type Animation)
    def slow_print(self, message, speed=100, newline=True):
        output = ""
        for letter in message:
            output += letter
            print(output, flush=True, end="\r")
            time.sleep(speed/1000)
        if(newline):
            print()

    # Prints the "PADDING_CHAR" as a complete line
    def print_full_line(self):
        print("".rjust(self.TERMINAL_SIZE_COLUMN, self.PADDING_CHAR), end="")
        return

    # Prints a Empty Lines
    def print_clear_line(self):
        print("".rjust(self.TERMINAL_SIZE_COLUMN, " "), end="")
        return

    # Set "PADDING_CHAR" which is used in various animation
    def set_padding_character(self, pad_char):
        self.PADDING_CHAR = pad_char
    
    # Reset "PADDING_CHAR"
    def reset_padding_character(self):
        self.PADDING_CHAR = "*"

    # Responsible for creating the heading bar
    def print_heading(self, heading, spacing=2):
        heading_length = len(heading) + (2*spacing)
        heading = (" " * spacing) + heading + (" " * spacing)
        no_of_stars = self.TERMINAL_SIZE_COLUMN - heading_length
        left_stars = 0
        right_stars = 0
        if (no_of_stars % 2) == 0:
            left_stars = right_stars = int(no_of_stars/2)
        else:
            left_stars = int((no_of_stars - 1)/ 2)
            right_stars = left_stars + 1
        
        heading = "".rjust(left_stars, self.PADDING_CHAR) + heading + "".rjust(right_stars, self.PADDING_CHAR)
        self.endless_print(heading)

    # Shows Processing Animation
    def print_processing(self, anim_type=2, limit=10, anim_data=None):
        i = 0
        if(anim_type == 1):
            anim_fun = self.slash_animation
            args = 200
        elif(anim_type == 2):
            anim_fun = self.arrow_animation
            args = 30
        elif(anim_type == 3):
            anim_fun = self.custom_animation
            if anim_data:
                args = anim_data["index"], anim_data["max_char"], anim_data["speed"]
            else:
                args = self.ANIMATION_PATTERN_LIST[6], 5, 10

        while i < limit:
            anim_fun(args)
            i += 1
        self.print_clear_line()

    # Prints Custom animation
    def custom_animation(self, anim_data):
        message = anim_data[0]
        max_word = anim_data[1]
        speed = anim_data[2]
        i = 0
        j = i + max_word
        l = len(message)
        no_of_times = int(l - j)
        for current_loop in range(no_of_times+1):
            i = current_loop
            j = i + max_word
            self.slow_print((" " * i) + message[i:j] + (" " * (l-j)), speed, False)
        return

    # Arrow =>>>>> Animation
    def arrow_animation(self, speed=30):
        self.slow_print("=    ", speed, False)
        self.slow_print("=>   ", speed, False)
        self.slow_print("=>>  ", speed, False)
        self.slow_print(" >>> ", speed, False)
        self.slow_print("  >>>", speed, False)
        self.slow_print("    >", speed, False)

    # Slash animation \-/
    def slash_animation(self, speed=200):
        self.slow_print("\\", speed, False)
        self.slow_print("-", speed, False)
        self.slow_print("/", speed, False)