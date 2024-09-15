import time
import smbus
import csv

bus = smbus.SMBus(1)
addr = 0x60

def read_sensor_data():
    # Read coefficients
    a0 = (bus.read_byte_data(addr, 0x04) << 8) | bus.read_byte_data(addr, 0x05)
    b1 = (bus.read_byte_data(addr, 0x06) << 8) | bus.read_byte_data(addr, 0x07)
    b2 = (bus.read_byte_data(addr, 0x08) << 8) | bus.read_byte_data(addr, 0x09)
    c12 = (bus.read_byte_data(addr, 0x0A) << 8) | bus.read_byte_data(addr, 0x0B)

    # Two's complement conversion
    a0 = -((~a0 & 0xffff) + 1) if a0 & 0x8000 else a0
    b1 = -((~b1 & 0xffff) + 1) if b1 & 0x8000 else b1
    b2 = -((~b2 & 0xffff) + 1) if b2 & 0x8000 else b2
    c12 = -((~c12 & 0xffff) + 1) if c12 & 0x8000 else c12

    # Convert coefficients
    a0f = a0 / 8.0
    b1f = b1 / 8192.0
    b2f = b2 / 16384.0
    c12f = c12 / 16777216.0

    # Start conversion and wait 3 ms
    bus.write_byte_data(addr, 0x12, 0x00)
    time.sleep(0.003)

    # Read raw pressure and temperature
    rawpres = (bus.read_byte_data(addr, 0x00) << 2) | (bus.read_byte_data(addr, 0x01) >> 6)
    rawtemp = (bus.read_byte_data(addr, 0x02) << 2) | (bus.read_byte_data(addr, 0x03) >> 6)

    # Compute compensated pressure and temperature
    pcomp = a0f + (b1f + c12f * rawtemp) * rawpres + b2f * rawtemp
    pkpa = pcomp / 15.737 + 50
    temp = 25.0 - (rawtemp - 498.0) / 5.35

    return pkpa, temp

def log_data(filename='sensor_data.csv'):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        while True:
            pressure, temperature = read_sensor_data()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, pressure, temperature])
            print(f"Timestamp: {timestamp}, Pressure: {pressure} kPa, Temperature: {temperature} °C")
            time.sleep(5)  # Log data every minute

if __name__ == "__main__":
    log_data()
