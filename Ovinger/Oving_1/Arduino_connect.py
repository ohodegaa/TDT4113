__author__ = 'hakon0601'

import serial



class Arduino_Connect:

    # Connects to the arduino via a COM port (USB).
    # Does not work if the serial monitor in arduino is open.

    def __init__(self, COM = '/dev/cu.usbmodem1411'):
        self.COM = COM

    def pc_connect(self):

        for i in range(100):
            try:
                arduino = serial.Serial(self.COM, 9600, timeout=.1)
                print("Connected to arduino")
                return arduino
            except serial.SerialException:
                pass
        exit("Arduino was not found")

    # arport = Arduino device port, which you can find at the bottom of your arduino window or via Arduino menu options tools/port.
    #   The default will probably NOT work for your machine, but it may look quite similar (for Mac users), differing only
    #  in the final 4 digits.

    def basic_connect(self):
        return serial.Serial(self.COM,9600,timeout=.1)

