import serial
import serial.tools.list_ports
import time

BAUD = 9600
TIMEOUT = 5  # Seconds to wait for boot message
EXPECTED = "Firmware Version: v1.0.3"
LOG_FILE = "bootup_validation_lognew.txt"

# --- Logging Function ---
def log_bootup_result(result, port, matched_line=None, reason=""):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("\n==== Arduino Bootup Validation Log ====\n")
        f.write(f"Timestamp     : {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"COM Port      : {port if port else 'N/A'}\n")
        f.write(f"Expected Line : {EXPECTED}\n")
        f.write(f"Matched Line  : {matched_line if matched_line else 'N/A'}\n")
        f.write(f"Result        : {'PASS' if result else 'FAIL'}\n")
        f.write(f"Reason        : {reason if reason else 'N/A'}\n")
        f.write("========================================\n")

# --- Auto-Detect Arduino Port ---
def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "USB" in port.description:
            print(f"Arduino detected on {port.device} - {port.description}")
            return port.device
    print("No Arduino device found.")
    return None

# --- Validate Bootup Firmware Message ---
def validate_bootup(port, baud, timeout):
    try:
        print(f"\n Connecting to {port}...")
        with serial.Serial(port, baud, timeout=timeout) as ser:
            time.sleep(2)  # Wait for Arduino to reset
            start_time = time.time()

            while time.time() - start_time < timeout:
                if ser.in_waiting:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    print(f"[Serial] {line}")
                    if EXPECTED in line:
                        print("\nBootup validation successful.")
                        log_bootup_result(True, port, line)
                        return True

            print("\nFirmware version not found in serial output.")
            log_bootup_result(False, port, reason="Firmware version missing")
            return False

    except serial.SerialException as e:
        print(f"Serial Error: {e}")
        log_bootup_result(False, port, reason=str(e))
        return False

# ---------- Main Script ----------
arduino_port = find_arduino_port()
if arduino_port:
    validate_bootup(arduino_port, BAUD, TIMEOUT)
else:
    log_bootup_result(False, None, reason="No Arduino COM port detected")
