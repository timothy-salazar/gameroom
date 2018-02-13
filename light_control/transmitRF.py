import time
import sys
import RPi.GPIO as GPIO



def transmit_outlet(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    code_dict = {'five_on':'0001000001110101000000110',
                'five_off':'0001000001110101000011000',
                'four_on':'0001000001011101000000110',
                'four_off':'0001000001011101000011000',
                'three_on':'0001000001010111000000110',
                'three_off':'0001000001010111000011000',
                'two_on': '0001000001010101110000110',
                'two_off':'0001000001010101110011000',
                'one_on':'0001000001010101001100110',
                'one_off': '0001000001010101001111000'}
    try:
        code = code_dict[code]
        
        extended_delay = 0.00569055813953
        short_sleep = 0.000571339403974
        short_impulse = 0.000162708126036
        long_impulse = 0.000512304038005
        long_sleep = 0.000220728215768
        
        NUM_ATTEMPTS = 4
        NUM_REPS = 4
        TRANSMIT_PIN = 27

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

        for t in range(NUM_ATTEMPTS):
            for r in range(NUM_REPS):
                for i in code:
                    if i == '0':
                        GPIO.output(TRANSMIT_PIN, 1)
                        time.sleep(short_impulse)
                        GPIO.output(TRANSMIT_PIN, 0)
                        time.sleep(short_sleep)
                    elif i == '1':
                        GPIO.output(TRANSMIT_PIN, 1)
                        time.sleep(long_impulse)
                        GPIO.output(TRANSMIT_PIN, 0)
                        time.sleep(long_sleep)
                    else:
                        continue
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(extended_delay)
        GPIO.cleanup()
    except KeyError:
        print('invalid input')


def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    code_dict = {'a_on':'011101110101101111111010111',
                'a_off':'101101110101101111111010111',
                'b_on':'011101110101110111111010111',
                'b_off':'101101110101110111111010111',
                'c_on':'011101110101100111111010111',
                'c_off':'101101110101100111111010111',
                'd_on':'011110110101111111111010111',
                'd_off':'101110110101111111111010111'}
    try:
        code = code_dict[code]
        short_impulse = 0.0005
        short_sleep = 0.0011
        long_impulse = 0.00125
        long_sleep = 0.00035
        extended_delay = 0.01130
        init_delay = 0.01125

        NUM_ATTEMPTS = 4
        NUM_REPS = 4
        TRANSMIT_PIN = 27

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

        for t in range(NUM_ATTEMPTS):
            GPIO.output(TRANSMIT_PIN, 1)
            time.sleep(short_impulse)
            GPIO.output(TRANSMIT_PIN,0)
            time.sleep(init_delay)
            for r in range(NUM_REPS):
                for i in code:
                    if i == '1':
                        GPIO.output(TRANSMIT_PIN, 1)
                        time.sleep(short_impulse)
                        GPIO.output(TRANSMIT_PIN, 0)
                        time.sleep(short_sleep)
                    elif i == '0':
                        GPIO.output(TRANSMIT_PIN, 1)
                        time.sleep(long_impulse)
                        GPIO.output(TRANSMIT_PIN, 0)
                        time.sleep(long_sleep)
                    else:
                        continue
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(extended_delay)
        GPIO.cleanup()
    except KeyError:
        print('invalid input')




if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')
