import serial

# Open serial connection to Arduino
arduino = serial.Serial('COM14', 9600)  # Replace 'COM3' with your Arduino's port
print("Listening for signals from Arduino...")

while True:
    if arduino.in_waiting > 0:  # Check if data is available
        signal = arduino.readline().decode().strip()  # Read and decode the signal

        if signal == "button1_pressed":
            print("Button 1 was pressed!")
            # Perform an action for button 1

        elif signal == "button2_pressed":
            print("Button 2 was pressed!")
            # Perform an action for button 2

        elif signal == "button3_pressed":
            print("Button 3 was pressed!")
            # Perform an action for button 3
