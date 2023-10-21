import subprocess
import time
import sys
import shlex
import pandas as pd
import psutil

def get_skype_pid_with_highest_resource_usage(app_name):
	skype_processes = []
	
	# Iterate through all running processes
	for process in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']):
		if app_name in process.info['name'].lower():  # Check if process name contains "skype"
			skype_processes.append(process)
	
	if not skype_processes:
		return None
	# Find the skype process with the highest CPU usage
	highest_cpu_usage_process = max(skype_processes, key=lambda process: process.info['memory_percent'])
	
	return highest_cpu_usage_process.info['pid']
	
def open_skype_chat(chat_partner_x, chat_partner_y, paragraph):
	subprocess.Popen(["skype"])
	#subprocess.Popen(["xdg-open", meeting_url])
	time.sleep(10)
	subprocess.Popen(["xdotool", "search", "--name", "skype", "windowactivate"])
	time.sleep(2)
	print("SKYPE OPENED")
	subprocess.Popen(["xdotool", "mousemove", str(chat_partner_x), str(chat_partner_y), "click", "1"])
	print("FOUND chat_partner")
	time.sleep(2)

	#sending message
	subprocess.Popen(["xdotool", "type", paragraph]) # Type the passage
	time.sleep(10)
	subprocess.Popen(["xdotool", "key", "Return"]) # Press Enter
	time.sleep(2)
	
	try:
		time.sleep(3)  # Wait for the skype window to open

		skype_pid = get_skype_pid_with_highest_resource_usage("skype")

		if skype_pid is not None:
			print(f"skype meeting with the highest resource consumption is running with PID: {skype_pid}")
		else:
			print("No skype meeting is running.")
			
		time.sleep(2)
		print(f"skype process started with PID: {skype_pid}")
		
		for i in range(10):
			try :
				#powerjoular_command = f'echo " " | sudo -S -k timeout 10 powerjoular -l -p {skype_pid} -f skype_energy.csv'
				powerjoular_command = f'echo " " | sudo -S -k timeout 20 powerjoular -l -p {skype_pid} -f skype_energy.csv'
				powerjoular_process = subprocess.run(powerjoular_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

				#sending message
				subprocess.Popen(["xdotool", "type", paragraph]) # Type the passage
				time.sleep(10)
				subprocess.Popen(["xdotool", "key", "Return"]) # Press Enter
				time.sleep(2)

			except subprocess.CalledProcessError as e:
				# PowerJoular is force kill due to timeout - Calculation finish
				print("Finish measurement")
			except e:
				print(f"Subprocess returned a non-zero exit status: {e.returncode}")

			print("------")
			print(skype_pid)
			
			time.sleep(2)
			# Create the CSV file
			#with open("skype_energy.csv", "a") as f:
			#	f.write(powerjoular_process.stdout)
			#	# Add a new line for separation
			#	f.write("\n")
	except KeyboardInterrupt:
		print("Measurement interrupted.")

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python skypeMsg.py <chat_partner_x> <chat_partner_y>") #240 #522
	else:
		chat_partner_x = sys.argv[1]
		chat_partner_y = sys.argv[2]
		convo = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed felis eu ligula consequat accumsan. Aenean dapibus, tortor at volutpat elementum, ligula sapien fringilla justo, at scelerisque metus lectus vel elit. Maecenas posuere ac arcu at malesuada. Integer vehicula urna quis ante varius, vel interdum lorem scelerisque. Vivamus a turpis at libero tincidunt egestas in vel ipsum. Nulla facilisi. In laoreet massa justo, non hendrerit elit fringilla a. Curabitur at nunc ac justo laoreet lacinia ac sit amet turpis. Cras ut odio ac orci volutpat euismod eu eget urna. Sed vulputate lacinia turpis, eu laoreet elit dapibus in."
		open_skype_chat(chat_partner_x, chat_partner_y, convo)

