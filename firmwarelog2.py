import serial
import time

def log_result(result, blink_states, port, log_file="led_validation_log.txt"):
    with open(log_file, "a") as f:
        f.write("\n==== LED Blink Validation Log ====\n")
        f.write(f"Timestamp     : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"COM Port      : {port}\n")
        f.write(f"Blink States  : {blink_states}\n")
        f.write(f"Result        : {'PASS' if result else 'FAIL'}\n")
        f.write("===================================\n")

def validate_led_blinking(port, baud=9600, duration=5):
    print("Script started")

    with serial.Serial(port, baud, timeout=1) as ser:
        print("Serial port opened.")
        time.sleep(2)  # Wait for Arduino reset
        ser.reset_input_buffer()  # 🧹 Flush any old data from Arduino


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
            print("Not enough LED toggles detected.")
            log_result(False, blink_states, port)
            return False

        # Check if ON and OFF alternate
        alternating = all(blink_states[i] != blink_states[i+1] for i in range(len(blink_states)-1))
        if alternating:
            print("LED is blinking as expected, Validation successful")
            log_result(True, blink_states, port)
            return True
        else:
            print("LED states not alternating properly.")
            log_result(False, blink_states, port)
            return False

# --- Call the function ---
validate_led_blinking("COM10", 9600,5)  # Replace COM10 with your actual port if needed
