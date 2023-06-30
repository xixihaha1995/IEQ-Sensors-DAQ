import serial
import csv
from datetime import datetime, timedelta

# Configure serial communication
# ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace with your Arduino's serial port on Linux
ser = serial.Serial('COM13', 9600)  # View from device manager or Arduino; Replace with your Arduino's serial port on Windows

# Data collection configuration
last_save_time = datetime.now()
save_frequency_seconds = 20  # Adjust the save frequency in seconds

# CSV file configuration
csv_filename = datetime.now().strftime('measured_data_%Y%m%d%H%M%S.csv')
csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Temperature (C)', 'Relative Humidity (%)', 'PAR (ppfd)', 'CO2 (ppm)'])

# Read and save data
while True:
    # Read data from Arduino
    line = ser.readline().decode().strip()

    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Extract data values and remove units
    values = [item.split(':')[1].split()[0] for item in line.split(',')]

    # Check if it's time to create a new file
    current_time = datetime.now()
    if current_time >= last_save_time + timedelta(seconds=save_frequency_seconds):
        # Close previous CSV file
        csv_file.close()

        # Create new CSV file with updated filename
        csv_filename = current_time.strftime('measured_data_%Y%m%d%H%M%S.csv')
        csv_file = open(csv_filename, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Timestamp', 'Temperature (C)', 'Relative Humidity (%)', 'PAR (ppfd)', 'CO2 (ppm)'])

        # Update last save time
        last_save_time = current_time

    # Write data to CSV file
    csv_writer.writerow([timestamp] + values)
    csv_file.flush()
