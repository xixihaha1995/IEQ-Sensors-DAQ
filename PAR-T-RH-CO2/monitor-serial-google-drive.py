import serial
import csv
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from pathlib import Path

# Configure serial communication
ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace with your Arduino's serial port

# Data collection configuration
last_save_time = datetime.now()
save_frequency_seconds = 20  # Adjust the save frequency in seconds

# CSV file configuration
csv_filename = datetime.now().strftime('measured_data_%Y%m%d%H%M%S.csv')
csv_file = open(csv_filename, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Timestamp', 'Temperature (C)', 'Relative Humidity (%)', 'PAR (ppfd)', 'CO2 (ppm)'])

# Google Drive configuration
credentials = service_account.Credentials.from_service_account_file('service_account.json')
drive_service = build('drive', 'v3', credentials=credentials)
drive_folder_id = '152CuCIGQxotbvbjCL7kS2e5cL8vrKaV-'  # Replace with the ID of your Google Drive folder

# Function to upload a file to Google Drive
def upload_file_to_drive(file_path, folder_id):
    file_metadata = {'name': file_path.name, 'parents': [folder_id]}
    media = MediaFileUpload(str(file_path))
    drive_service.files().create(body=file_metadata, media_body=media).execute()

# Read and save data
while True:
    # Read data from Arduino
    line = ser.readline().decode().strip()

    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Extract data values if the line has enough elements
    if len(line.split(',')) == 4:
        values = line.split(',')
        temp = values[0].split(':')[1].strip()
        rh = values[1].split(':')[1].strip()
        par = values[2].split(':')[1].strip()
        co2 = values[3].split(':')[1].strip()

        # Check if it's time to create a new file
        current_time = datetime.now()
        if current_time >= last_save_time + timedelta(seconds=save_frequency_seconds):
            # Close previous CSV file
            csv_file.close()

            # Upload the last created old file to Google Drive (except the first file)
            if last_save_time != datetime.min:
                upload_file_to_drive(Path(csv_filename), drive_folder_id)

            # Create new CSV file with updated filename
            csv_filename = current_time.strftime('measured_data_%Y%m%d%H%M%S.csv')
            csv_file = open(csv_filename, 'w', newline='')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Timestamp', 'Temperature (C)', 'Relative Humidity (%)', 'PAR (ppfd)', 'CO2 (ppm)'])

            # Update last save time
            last_save_time = current_time

        # Write data to CSV file
        csv_writer.writerow([timestamp, temp, rh, par, co2])
        csv_file.flush()
