import subprocess
import time
import pyautogui
import sys
import shlex
import pandas as pd
import psutil

import threading

def get_zoom_pid_with_highest_resource_usage():
    zoom_processes = []
    
    # Iterate through all running processes
    for process in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']):
        if "zoom" in process.info['name'].lower():  # Check if process name contains "zoom"
            zoom_processes.append(process)
    
    if not zoom_processes:
        return None
    # Find the Zoom process with the highest CPU usage
    highest_cpu_usage_process = max(zoom_processes, key=lambda process: process.info['memory_percent'])
    
    return highest_cpu_usage_process.info['pid']

def send_a_message_zoom(message):
    global measurement_running
    time.sleep(5)
    print('going to click chat')
    # Click on the chat button to open the chat window
    pyautogui.click(x=881, y=94)  # Replace with the actual coordinates
    print('chat-clicked')

    time.sleep(2)
    # Click here to select contact
    pyautogui.click(x=488, y=390)  # Replace with the actual coordinates

    time.sleep(2)
    #click here to select message box
    pyautogui.click(x=1293, y=1014)  # Replace with the actual coordinates


    time.sleep(3)
    # Type your message (optional)
    pyautogui.typewrite(message)

    time.sleep(3)
    # #click here to send message
    # pyautogui.click(x=200, y=200)  # Replace with the actual coordinates

    # # Attach the file (click the "Attach" button and choose a file)
    # pyautogui.click(x=300, y=300)  # Replace with the actual coordinates for the "Attach" button
    # time.sleep(2)  # Wait for the file dialog to open
    # pyautogui.write('/path/to/your/file')  # Replace with the actual file path
    # pyautogui.press('enter')

    # Send the message
    pyautogui.press('enter')

    time.sleep(2)
    # Signal the measurement thread to stop
    measurement_running = False



def send_an_image_zoom():
    global measurement_running
    time.sleep(5)
    print('going to click chat')
    # Click on the chat button to open the chat window
    pyautogui.click(x=881, y=94)  # Replace with the actual coordinates
    print('chat-clicked')

    time.sleep(2)
    # Click here to select contact
    pyautogui.click(x=488, y=390)  # Replace with the actual coordinates

    time.sleep(2)
    # Click here to select attach a file
    pyautogui.click(x=683, y=1011)  # Replace with the actual coordinates

    time.sleep(3)
    # select image
    pyautogui.click(x=877, y=412)  # Replace with the actual coordinates

    time.sleep(3)
    # Send the message
    pyautogui.press('enter')

    time.sleep(2)
    pyautogui.press('enter')

    time.sleep(8)

    # Signal the measurement thread to stop
    measurement_running = False


def send_a_pdf_zoom():
    global measurement_running
    time.sleep(5)
    print('going to click chat')
    # Click on the chat button to open the chat window
    pyautogui.click(x=881, y=94)  # Replace with the actual coordinates
    print('chat-clicked')

    time.sleep(2)
    # Click here to select contact
    pyautogui.click(x=488, y=390)  # Replace with the actual coordinates

    time.sleep(2)
    # Click here to select attach a file
    pyautogui.click(x=683, y=1011)  # Replace with the actual coordinates

    time.sleep(3)
    # select a pdf
    pyautogui.click(x=877, y=432)  # Replace with the actual coordinates

    time.sleep(3)
    # Send the message
    pyautogui.press('enter')

    time.sleep(2)
    pyautogui.press('enter')

    time.sleep(8)

    # Signal the measurement thread to stop
    measurement_running = False




def send_a_zip_zoom():
    global measurement_running
    time.sleep(5)
    print('going to click chat')
    # Click on the chat button to open the chat window
    pyautogui.click(x=881, y=94)  # Replace with the actual coordinates
    print('chat-clicked')

    time.sleep(2)
    # Click here to select contact
    pyautogui.click(x=488, y=390)  # Replace with the actual coordinates

    time.sleep(2)
    # Click here to select attach a file
    pyautogui.click(x=683, y=1011)  # Replace with the actual coordinates

    time.sleep(3)
    # select zip
    pyautogui.click(x=877, y=452)  # Replace with the actual coordinates

    time.sleep(3)
    # Send the message
    pyautogui.press('enter')

    time.sleep(2)
    pyautogui.press('enter')

    time.sleep(8)

    # Signal the measurement thread to stop
    measurement_running = False


def powerjoular_measurement_function(p_id):
    global measurement_running
    powerjoular_command = f'echo " " | sudo -S -k powerjoular -l -p {p_id} -f zoom_send_pdf_energy.csv'
    powerjoular_process = subprocess.Popen(powerjoular_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print('Measurement started')

    # Monitor the shared variable to stop the measurement
    while measurement_running:
        time.sleep(1)

    # Terminate the powerjoular process
    powerjoular_process.terminate()
    


lorum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"




for i in range(20):

    # Shared variable to signal the measurement thread to stop
    measurement_running = True

    #open zoom
    subprocess.Popen(['zoom'])
    time.sleep(5)
    # Get the Zoom PID and start powerjoular measurement
    p_id = get_zoom_pid_with_highest_resource_usage()

    if p_id is not None:
        print(f"Zoom meeting with the highest resource consumption is running with PID: {p_id}")
        powerjoular_thread = threading.Thread(target=powerjoular_measurement_function, args=(p_id,))
        powerjoular_thread.start()
    else:
        print("No Zoom meeting is running.")

    #time.sleep(2)
    print(f"Zoom process started with PID: {p_id}")

    # Start sending the file
    #send_a_message_zoom(lorum)
    #send_an_image_zoom()
    #send_a_zip_zoom()
    send_a_pdf_zoom()

    # Wait for the measurement thread to finish
    powerjoular_thread.join()

    subprocess.Popen(['pkill','zoom'])
    time.sleep(2)








