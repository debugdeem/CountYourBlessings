import os
import RPi.GPIO as GPIO
import time
import threading

# Setup
FSR_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(FSR_PIN, GPIO.IN)

# Global variables
sujood_count = 0
rakat_count = 0
press_detected = False
press_times = []  # List to keep track of press timestamps for reset
running = True
need_reset = False  # Flag to indicate a pending reset
reset_press_count = 0  # Count presses after reaching the reset condition

device_name = os.getenv("DEVICE_NAME", "SujoodCounter")  # Default device name

def read_FSR():
    num_readings = 10
    delay = 0.01
    count_high = 0
    for _ in range(num_readings):
        if GPIO.input(FSR_PIN):
            count_high += 1
        time.sleep(delay)
    return count_high > 5

def check_for_reset():
    global press_times
    current_time = time.time()
    press_times = [t for t in press_times if current_time - t <= 3]
    
    if len(press_times) >= 3:
        reset_counter()
        press_times = []

def reset_counter():
    global sujood_count, rakat_count, need_reset, reset_press_count
    sujood_count = 0
    rakat_count = 0
    need_reset = False
    reset_press_count = 0  # Reset the post-reset press counter
    print("Counter reset successfully.")

def update_rakat(is_pressed):
    global sujood_count, rakat_count, press_detected, press_times, need_reset, reset_press_count
    if need_reset:
        if is_pressed:
            reset_press_count += 1
            if reset_press_count >= 2:  # Reset on the second press after the condition is met
                reset_counter()
                return  # Return early to prevent further processing in this cycle

    if rakat_count < 4:
        if is_pressed and not press_detected:
            sujood_count += 1
            press_detected = True
            if sujood_count % 2 == 0:
                rakat_count += 1
                print(f"Current Rakat Count: {rakat_count}")
                if rakat_count == 4:
                    print("Maximum rakat count reached for typical obligatory prayers.")
                    need_reset = True  # Set flag to reset on next touch
        elif not is_pressed and press_detected:
            press_detected = False
            press_times.append(time.time())  # Log the time of this press
            check_for_reset()  # Check if a reset is due after releasing the pressure
    else:
        need_reset = True

def input_thread():
    global running
    while running:
        is_pressed = read_FSR()
        update_rakat(is_pressed)
        time.sleep(0.1)  # Reduce CPU load

def start_counter():
    thread = threading.Thread(target=input_thread)
    thread.start()

def get_rakat_count():
    global rakat_count
    return rakat_count

def main():
    print("Welcome to Count Your Blessings")
    start_counter()  # Simplify starting the counter

if __name__ == "__main__":
    main()