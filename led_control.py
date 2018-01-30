import time
import pigpio
import math

pi1 = pigpio.pi()

def is_int(s):
        try:
                x = int(s)
                if(x > 255 or x < 0):
                        return False
                else:
                        return True
        except ValueError:
                return False


def single_color(t, step_size):

        red_led = raw_input("value for red led (0-255) ")
        while is_int(red_led) != True:
                print("invalid input for the red LEDs")
                red_led = raw_input("please enter a value between 0 and 255: ")
        green_led = raw_input("value for green led (0-255) ")
        while is_int(green_led) != True:
                print("invalid input for the green LEDs")
                green_led = raw_input("please enter a value between 0 and 255: ")

        blue_led = raw_input("value for blue led (0-255) ")
        while is_int(blue_led) != True:
                print("invalid input for the blue LEDs")
                blue_led = raw_input("please enter a value between 0 and 255: ")
        color_box = (0, red_led, green_led, blue_led)
        color_fade(color_box, t, step_size)
        #pi1.set_PWM_dutycycle(17, red_led)
        #pi1.set_PWM_dutycycle(22, green_led)
        #pi1.set_PWM_dutycycle(24, blue_led)



def named_color(t, step_size):

        fhand = open("colors.txt")
        color_string = "NULL"
        input_name = raw_input("enter a color name ")
        for line in fhand:
                if line.startswith(input_name):
                        color_string = line

        if(color_string != "NULL"):
                color_string = color_string.split(",")
                color_box = (0,int(color_string[1]),int(color_string[2]),
                             int(color_string[3]))
                color_fade(color_box, t, step_size)

                #pi1.set_PWM_dutycycle(17, int(color_string[1]))
                #pi1.set_PWM_dutycycle(22, int(color_string[2]))
                #pi1.set_PWM_dutycycle(24, int(color_string[3]))
        else:
                cont = raw_input("invalid input, try again? y/n\n")
                if cont == "y":
                        named_color(t, step_size)


def color_fade(r, t, step_size):
        duty_17 = pi1.get_PWM_dutycycle(red_pin)
        duty_22 = pi1.get_PWM_dutycycle(green_pin)
        duty_24 = pi1.get_PWM_dutycycle(blue_pin)

        if(duty_17 < r[1]):
                x17 = step_size
        else:
                x17 = -step_size

        if(duty_22 < r[2]):
                x22 = step_size
        else:
                x22 = -step_size

        if(duty_24 < r[3]):
                x24 = step_size
        else:
                x24 = -step_size

        dif_17 = abs(duty_17 - r[1])
        dif_22 = abs(duty_22 - r[2])
        dif_24 = abs(duty_24 - r[3])

        steps_17 = int(math.floor(dif_17/step_size))
        steps_22 = int(math.floor(dif_22/step_size))
        steps_24 = int(math.floor(dif_24/step_size))

        iter_17 = 0
        iter_22 = 0
        iter_24 = 0

        for i in range(1,51):
                if(iter_17 != steps_17):
                        duty_17 = duty_17 + x17
                        pi1.set_PWM_dutycycle(red_pin, duty_17)
                        iter_17 = iter_17 + 1
                if(iter_22 != steps_22):
                        duty_22 = duty_22 + x22
                        pi1.set_PWM_dutycycle(green_pin, duty_22)
                        iter_22 = iter_22 + 1
                if(iter_24 != steps_24):
                        duty_24 = duty_24 + x24
                        pi1.set_PWM_dutycycle(blue_pin, duty_24)
                        iter_24 = iter_24 + 1
                time.sleep(t)

        pi1.set_PWM_dutycycle(red_pin, r[1])
        pi1.set_PWM_dutycycle(green_pin, r[2])
        pi1.set_PWM_dutycycle(blue_pin, r[3])


def oscillate(s, r, t, step_size):
        try:
                while True:
                        color_fade(s, t, step_size)
                        color_fade(r, t, step_size)
        except KeyboardInterrupt:
                pass


def menu_options():
        print("OPTIONS:")
        print("named - will let you select a saved color")
        print("manual - you put in the values for R,G, and B manually")
        print("settings - this is for advanced options like oscillating")
        print("between two colors, choosing pre-programed dynamic light")
        print("routines, and adjusting variables like speed")
        print("honestly, just don't go in there")
        print("mode - change the mode (ceiling or table)")
        print("quit - quit the program\n\n")


def main_menu():
        continue_variable = "HELL YEAH"
        fade_time = .05
        step_size = 5
        wrong_counter = 0
        global red_pin
        global green_pin
        global blue_pin
        red_pin = 17
        green_pin = 22
        blue_pin = 24
        print("YOU'VE MANAGED TO FIND THE")
        print("MOTHERFUCKING GAMEROOM LIGHT CONTROLS\n\n")
        print("YOU READY TO GET EYE FUCKED BY SOME COLORS?!?\n")
        user_input = raw_input("y/n: ")
        if user_input == "y":
                print("\nGOOD")
        else:
                print("\nTOO BAD")
        time.sleep(.5)
        print("BECAUSE THERE WAS NEVER ANY CHOICE\n")
        time.sleep(.5)
        menu_options()
        while continue_variable != "quit":
                user_input = raw_input("make selection or type '?' for help:\n")
                if user_input == "?":
                        menu_options()
                elif user_input == "named":
                        named_color(fade_time, step_size)
                elif user_input == "manual":
                        single_color(fade_time, step_size)
                elif user_input == "mode":
                        print("Enter either 'ceiling' for the ceiling")
                        print("LED strip, or 'table' for the table strip")
                        user_input = raw_input()
                        if(user_input == "ceiling"):
                                red_pin = 17
                                green_pin = 22
                                blue_pin = 24
                                print("mode changed to 'ceiling'")
                                time.sleep(.25)
                        elif(user_input == "table"):
                                red_pin = 5
                                green_pin = 13
                                blue_pin = 26
                                print("mode changed to 'table'")
                                time.sleep(.25)
                        else:
                                print("invalid input")
                                time.sleep(.25)
                elif user_input == "settings":
                        print("YOU'VE GOT SOME BALLS COMING INTO THIS MENU")
                        print("I LIKE THAT! HERE'S WHAT WE HAVE FOR YOU")
                        print("OPTIONS:")
                        print("mode - change the light strip mode")
                        print("fade - adjust fade time")
                        print("step - adjust step size")
                        print("siren - a shitty siren effect")
                        print("alarm - a shitty alarm")
                        print("oscillate - diy oscillation")
                        user_input = raw_input()
                        if(user_input == "mode"):
                                print("Enter either 'ceiling' for the ceiling")
                                print("LED strip, or 'table' for the table strip")
                                user_input = raw_input()
                                if(user_input == "ceiling"):
                                        red_pin = 17
                                        blue_pin = 22
                                        green_pin = 24
                                        print("mode changed to 'ceiling'")
                                        time.sleep(.25)
                                elif(user_input == "table"):
                                        red_pin = 5
                                        blue_pin = 13
                                        green_pin = 26
                                        print("mode changed to 'table'")
                                        time.sleep(.25)
                                else:
                                        print("invalid input")
                                        time.sleep(.25)
                        elif(user_input == "fade"):
                                fade_time = raw_input("input new fade time:\n")
                        elif(user_input == "step"):
                                step_size = raw_input("input new step size:\n")
                        elif(user_input == "siren"):
                                color_box1 = (0,255,0,0)
                                color_box2 = (0,0,0,255)
                                oscillate(color_box1,color_box2,.02,10)
                        elif(user_input == "alarm"):
                                color_box1 = (0,255,100,0)
                                color_box2 = (0,100,0,0)
                                oscillate(color_box1,color_box2,.02,5)
                        elif(user_input == "oscillate"):
                                print("work in progress")
                        else:
                                print("please enter valid input")
                elif user_input == "quit":
                        print("YOU THINK YOU CAN EVER LEAVE THIS PLACE?")
                        user_input = raw_input("y/n ")
                        if user_input == "y":
                                print("Oh, you have a point.")
                                continue_variable = "quit"
                        else:
                                print("YOU WILL NEVER BE FREE. EVEN DEATH WILL ONLY")
                                print("BE AN OMINOUS SUNRISE, A SWELLING CHROMATIC")
                                print("BRILLIANCE - A RAINBOW IN WHICH ALL NATURAL COLOR")
                                print("HAS BEEN MUTATED INTO A PAINFULLY LUSH IRIDESCENCE")
                                print("BY SOME PRISM FANTASTICALLY CORRUPTED IN ITS FORM.")
                                time.sleep(.5)
                else:

                        print("\n\nLISTEN HERE FUCK BOY")
                        time.sleep(.5)
                        print("DO YOU THINK THIS IS A GAME?!?")
                        print("YOU HAD ONE JOB - JUST ENTER A FUCKING MENU OPTION")
                        print("YOU HAD A WHOLE FUCKING LIST OF THEM - ARE YOU ILLITERATE?")
                        print("I SWEAR TO GOD, YOU HAVE ONE MORE CHANCE NOT TO FUCK IT")
                        print("UP - OTHERWISE WHEN YOU GO TO SLEEP TONIGHT, I'LL BE")
                        print("UNDER YOUR BED.\n")
                        print("CHOOSE A MOTHERFUCKING MENU OPTION OR HIT '?'")
                        wrong_counter = wrong_counter + 1


main_menu()

#pi1.set_PWM_dutycycle(
#oscillate(color_box1, color_box2, .03)
#color_fade(color_box1, .08, 5)
#single_color()
#named_color(0)

# def color_fade(r):
