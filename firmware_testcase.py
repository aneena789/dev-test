import serial
import serial.tools.list_ports
import time

BAUD = 9600
TIMEOUT = 5  # Seconds to wait for boot message
EXPECTED = "Firmware Version: v1.0.3"

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "USB" in port.description:
            print(f" Arduino detected on {port.device} - {port.description}")
            return port.device
    print(" No Arduino device found, bootup failed")
    return None

def validate_bootup(port, baud, timeout):
    try:
        print(f"\nConnecting to {port}...")
        with serial.Serial(port, baud, timeout=timeout) as ser:
            time.sleep(2)  # Allow Arduino to reset after Serial connection
            lines = []
            start_time = time.time()

            while time.time() - start_time < timeout:
                if ser.in_waiting:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    lines.append(line)
                    print(f"[Serial] {line}")
                    if EXPECTED in line:
                        print("\n Bootup validation successful.")
                        return True

            print("\n Firmware version not found. Validation failed.")
            return False

    except serial.SerialException as e:
        print(f"Serial Error: {e}")
        return False

# ---------- Main Script ----------
arduino_port = find_arduino_port()
if arduino_port:
    validate_bootup(arduino_port, BAUD, TIMEOUT)
