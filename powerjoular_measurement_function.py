#THESE 4 LIBRARIES ARE NEEDED FOR THIS PART OF CODE, SO MAKE SURE THESE HAS BEEN ADDED TO THE MAIN CODE
import subprocess
import time
import csv
from datetime import datetime

def powerjoular_measurement_function(p_id):
    global measurement_running
    powerjoular_command = (
        f'echo " " | sudo -S -k powerjoular -l -p {p_id} -f element_image_energy.csv'
    )
    powerjoular_process = subprocess.Popen(
        powerjoular_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    print("Measurement started")

    # Initialize the sum variable for saving this round value
    sum_total_power = 0.0

    #Initialize the starting time
    start_time = datetime.now().strftime('%d.%m.%Y_%H:%M:%S')

    # Monitor the shared variable to stop the measurement
    while measurement_running:
        # Read the output of powerjoular command
        output = powerjoular_process.stdout.readline().strip()
        
        # Split the output into column name and value
        column, value = output.split(',')
        
        # Check if the column name ends with "_total_power"
        if column.endswith('_total_power'):
            sum_total_power += float(value)

        time.sleep(1)

    # Terminate the powerjoular process and calculate end time
    powerjoular_process.terminate()
    end_time = datetime.now().strftime('%d.%m.%Y_%H:%M:%S')

    # Print the final sum
    print(f'Total_power of this round : {sum_total_power}')

    # Write the results to Total_Power.csv
    with open('Total_Power.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([start_time, end_time, sum_total_power])