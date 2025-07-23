import serial
import time

def validate_led_blinking(port, baud=9600, duration=5):
    print(" Script started")

    with serial.Serial(port, baud, timeout=1) as ser:
        print(" Serial port opened.")
        time.sleep(2)  # Wait for Arduino reset

        blink_states = []
        start_time = time.time()

        while time.time() - start_time < duration:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                print(f"[Serial] {line}")
                if "LED State:" in line:
                    blink_states.append(line.split(": ")[1])

        print(f"Collected LED states: {blink_states}")

        if len(blink_states) < 2:
            print(" Not enough LED toggles detected.")
            return False

        alternating = all(blink_states[i] != blink_states[i+1] for i in range(len(blink_states)-1))
        if alternating:
            print(" LED is blinking as expected, Validation successful")
            return True
        else:
            print(" LED states not alternating properly.")
            return False

# --- Call the function ---
validate_led_blinking("COM10", 9600, 6)  # Replace COM3 if needed
