import blinkt
from time import sleep

def main():
    blinkt.clear()
    while True:
        # Up Green
        for i in range(8):
            blinkt.set_pixel(i, 0, 250, 0, 0.1)
            blinkt.show()
            sleep(0.2)
        # Up Red
        for i in range(8, 0, -1):
            blinkt.set_pixel(i - 1, 250, 0, 0, 0.1)
            blinkt.show()
            sleep(0.2)

main()