import time
import math
import board
import busio
import usb_hid
from adafruit_hid.mouse import Mouse
import adafruit_adxl34x
import digitalio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
i2c = busio.I2C(scl=board.GP5, sda=board.GP4)
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
    '----.': '9', '-----': '0'
}
sequence = ""
message = ""
last_press = 0
last_release = 0
is_pressed = False
while not i2c.try_lock():
    pass
left_button = digitalio.DigitalInOut(board.GP14)
left_button.direction = digitalio.Direction.INPUT
left_button.pull = digitalio.Pull.DOWN
center_button = digitalio.DigitalInOut(board.GP15)
center_button.direction = digitalio.Direction.INPUT
center_button.pull = digitalio.Pull.UP
right_button = digitalio.DigitalInOut(board.GP2)
right_button.direction = digitalio.Direction.INPUT
right_button.pull = digitalio.Pull.UP
i2c.unlock()
accelerometer = adafruit_adxl34x.ADXL345(i2c)
m = Mouse(usb_hid.devices)
velocity_x, velocity_y, velocity_z = 0.0, 0.0, 0.0

position_x, position_y, position_z = 0.0, 0.0, 0.0
# --- Drift Correction Variables ---
avg_ax, avg_ay, avg_az = 0.0, 0.0, 0.0
alpha = 0.98  # Smoothing factor

# --- Timekeeping ---
last_time = time.monotonic()
dampFactor = 0.95

print("Starting location tracking...")
print("Ensure the device is mostly stationary to reduce drift. ")

while True:
    try:
        if not left_button:
            m.press(Mouse.LEFT_BUTTON)
        if not center_button:
            m.press(Mouse.CENTER_BUTTON)
        if not right_button:
            m.press(Mouse.RIGHT_BUTTON)
        now = time.monotonic()
        delta_time = now - last_time
        last_time = now
        raw_ax, raw_ay, raw_az = accelerometer.acceleration

        # Calculate pitch and roll (theyre reversed since the accelerometer is 90 degrees from where it should be.
        roll = math.atan2(-raw_ax, math.sqrt(raw_ay**2 + raw_az**2)) * 180 / math.pi
        pitch = math.atan2(raw_ay, raw_az) * 180 / math.pi

        print(f"Pitch: {pitch:.2f}°, Roll: {roll:.2f}°")
        m.move(x=round(roll/10), y=round(pitch/10))
    except Exception as e:
        print(f"Sensor error: {e}")


    # Click the left mouse button.
    #m.click(Mouse.LEFT_BUTTON)

    # Move the mouse diagonally to the upper left.


    # Move the mouse while holding down the left button. (click-drag).
    #m.press(Mouse.LEFT_BUTTON)

    #m.release_all()       # or m.release(Mouse.LEFT_BUTTON)
    time.sleep(0.01)
