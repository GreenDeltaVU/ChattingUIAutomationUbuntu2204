import subprocess
import time
import sys
import shlex
import pandas as pd
import psutil

def get_zoom_pid_with_highest_resource_usage(app_name):
	zoom_processes = []
	
	# Iterate through all running processes
	for process in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']):
		if app_name in process.info['name'].lower():  # Check if process name contains "zoom"
			zoom_processes.append(process)
	
	if not zoom_processes:
		return None
	# Find the zoom process with the highest CPU usage
	highest_cpu_usage_process = max(zoom_processes, key=lambda process: process.info['memory_percent'])
	
	return highest_cpu_usage_process.info['pid']
	
def open_zoom_chat(chat_partner, paragraph):
	subprocess.Popen(["zoom"])
	#subprocess.Popen(["xdg-open", meeting_url])
	time.sleep(10)
	subprocess.Popen(["xdotool", "search", "--name", "zoom", "windowactivate"])
	time.sleep(2)
	print("zoom")
	#subprocess.Popen(["xdotool", "mousemove", str(chat_partner_x), str(chat_partner_y), "click", "1"])
	#print("FOUND chat_partner")
	subprocess.Popen(["xdotool", "key", "ctrl+f"])
	time.sleep(2)
	subprocess.Popen(["xdotool", "type", chat_partner]) # Type the passage
	time.sleep(4)
	subprocess.Popen(["xdotool", "key", "Down"])
	time.sleep(2)
	subprocess.Popen(["xdotool", "key", "KP_Enter"]) #IN ROBEL LAPTOP THIS KP_ENTER MIGHT BE RETURN.. THERE ARE 2 TYPE OF ENTER DEPEND OF THE LAPTOP
	time.sleep(2)
	print("FIND CHATPARTNER")

	#sending message
	subprocess.Popen(["xdotool", "type", paragraph]) # Type the passage
	time.sleep(15)
	subprocess.Popen(["xdotool", "key", "KP_Enter"])
	time.sleep(2)
	
	
	try:
		time.sleep(3)  # Wait for the zoom window to open

		zoom_pid = get_zoom_pid_with_highest_resource_usage("zoom")

		if zoom_pid is not None:
			print(f"zoom meeting with the highest resource consumption is running with PID: {zoom_pid}")
		else:
			print("No zoom meeting is running.")
			
		time.sleep(2)
		print(f"zoom process started with PID: {zoom_pid}")
		
		for i in range(10):
			try :
				#powerjoular_command = f'echo " " | sudo -S -k timeout 10 powerjoular -l -p {zoom_pid} -f zoom_energy.csv'
				powerjoular_command = f'echo " " | sudo -S -k timeout 20 powerjoular -l -p {zoom_pid} -f zoom_energy.csv'
				powerjoular_process = subprocess.run(powerjoular_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

				#sending message
				subprocess.Popen(["xdotool", "type", paragraph]) # Type the passage
				time.sleep(15)
				subprocess.Popen(["xdotool", "key", "KP_Enter"]) # Press Enter
				time.sleep(2)

			except subprocess.CalledProcessError as e:
				# PowerJoular is force kill due to timeout - Calculation finish
				print("Finish measurement")
			except e:
				print(f"Subprocess returned a non-zero exit status: {e.returncode}")

			print("------")
			print(zoom_pid)
			
			time.sleep(2)
			# Create the CSV file
			#with open("zoom_energy.csv", "a") as f:
			#	f.write(powerjoular_process.stdout)
			#	# Add a new line for separation
			#	f.write("\n")
	except KeyboardInterrupt:
		print("Measurement interrupted.")
	

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python zoomMsg.py <chat_partner> ") #CINDY
	else:
		chat_partner = sys.argv[1]
		convo = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed felis eu ligula consequat accumsan. Aenean dapibus, tortor at volutpat elementum, ligula sapien fringilla justo, at scelerisque metus lectus vel elit. Maecenas posuere ac arcu at malesuada. Integer vehicula urna quis ante varius, vel interdum lorem scelerisque. Vivamus a turpis at libero tincidunt egestas in vel ipsum. Nulla facilisi. In laoreet massa justo, non hendrerit elit fringilla a. Curabitur at nunc ac justo laoreet lacinia ac sit amet turpis. Cras ut odio ac orci volutpat euismod eu eget urna. Sed vulputate lacinia turpis, eu laoreet elit dapibus in."
		open_zoom_chat(chat_partner, convo)

