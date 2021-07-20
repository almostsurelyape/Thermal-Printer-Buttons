from gpiozero import Button
import funprint
import time


def pressed_0():  # Red
    p = funprint.Printer()
    p.print_title('Movie Choice')
    p.print_random_plex()
    p.close()


def pressed_1():  # Yellow
    p = funprint.Printer()
    p.print_title('Cat')
    p.print_cat()
    p.close()


def pressed_2():  # Blue
    p = funprint.Printer()
    p.print_title('Monster')
    p.print_pixel_monster()
    p.close()


def pressed_3():  # Green
    p = funprint.Printer()
    p.print_title('On This Day')
    p.print_on_this_day()
    p.close()


def pressed_4():  # Black
    p = funprint.Printer()
    p.print_title('Weather')
    p.print_weather_hourly()
    p.close()


def pressed_5():  # White
    p = funprint.Printer()
    p.print_title('Jeopardy Q')
    p.print_jeopardy()
    p.close()


buttons = [
    Button(17),
    Button(18),
    Button(21),
    Button(22),
    Button(23),
    Button(24)
]

buttons[0].when_pressed = pressed_0
buttons[1].when_pressed = pressed_1
buttons[2].when_pressed = pressed_2
buttons[3].when_pressed = pressed_3
buttons[4].when_pressed = pressed_4
buttons[5].when_pressed = pressed_5

while True:
    time.sleep(1)
