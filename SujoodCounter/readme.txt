Setup Instructions

Prerequisites

Ensure you have the following ready before you start:

-Raspberry Pi (any model that supports GPIO pins)
-SD Card with Raspberry Pi OS installed
-Internet connection for the Raspberry Pi

Step 1: System Update
Before you start, update your Raspberry Pi's package list and upgrade the existing software to the latest versions:

sudo apt update
sudo apt upgrade -y


Step 2: Install Python GPIO Library
Install the RPi.GPIO library, which allows you to control the Raspberry Pi GPIO channels:

sudo apt install python3-rpi.gpio


Step 3: Clone the Repository
Clone the project repository to your Raspberry Pi:

git clone https://github.com/debugdeem/CountYourBlessings.git
cd CountYourBlessings/SujoodCounter


Step 4: Install Required Python Packages
Install the necessary Python packages using pip:

python3 -m pip install flask zeroconf


Step 5: Running the Application
To start the application, run:

python3 app.py
This will start the Flask server and make the service available on the local network.

Step 6: Accessing the Application
Open a web browser and navigate to http://raspberrypi.local:5001 to view the application interface.

Troubleshooting
If you encounter issues accessing GPIO, make sure to run the script with sudo:

sudo python3 app.py

Ensure your Raspberry Pi is connected to the same network as your other devices when trying to access the Flask server.
