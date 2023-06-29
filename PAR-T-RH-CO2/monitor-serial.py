import serial
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Configure serial communication
ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace with your Arduino's serial port

# Configure Google Drive authentication and API access
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Create a file on Google Drive
file_name = 'measured_data.txt'
file_content = ''

# Monitor and upload data
while True:
    # Read data from Arduino
    line = ser.readline().decode().strip()
    
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Append data with timestamp to file content
    file_content += f'{timestamp} {line}\n'
    
    # Print data to the console
    print(f'{timestamp} {line}')
    
    # Upload file to Google Drive every 10 data points
    if len(file_content.split('\n')) >= 10:
        with open(file_name, 'w') as file:
            file.write(file_content)
        gfile = drive.CreateFile({'title': file_name})
        gfile.SetContentFile(file_name)
        gfile.Upload()
        file_content = ''
