#!/usr/bin/env python
from tkinter import *
import subprocess


def list_outputs():
	""" Récupération de la liste des sorties disponibles """
	interfaces = {}

	interfaces_list_raw = subprocess.run("echo $(sudo -u pi XDG_RUNTIME_DIR=/run/user/1000 pacmd list-sinks)"
	, shell=True, capture_output=True).stdout.decode()

	for interface in interfaces_list_raw.split("index: ")[1:]:
		name = ""

		if "alsa.name = " in interface:
			# name = interface.split('alsa.name = "')[1].split('"')[0].replace("bcm2835 ", "").strip()
			name = "AV Jack"
		elif "bluetooth" in interface:
			name = interface.split('device.description = "')[1].split('"')[0].strip()

		interfaces[interface.split(" ")[0]] = name

	print(interfaces)
	return interfaces

def show_outputs():
	""" Afficher la liste des sorties """
	global frame
	frame.destroy()
	outputs = list_outputs()
	frame = Frame(window)
	frame.pack()
	for id, name in outputs.items():
		Button(frame, text=name, command=lambda id=id: change_output(id), width=width, height=height/len(outputs + 1)).pack()

def change_output(id):
	""" Changement de la sortie """
	print(f"sudo -u pi XDG_RUNTIME_DIR=/run/user/1000 pactl set-default-sink {id}")
	result = subprocess.run(f"sudo -u pi XDG_RUNTIME_DIR=/run/user/1000 pactl set-default-sink {id}", shell=True, capture_output=True)
	print(result)
	if result.returncode != 0:
		return False
	else:
		return True


window = Tk()
window.title = "Changement de sortie audio"
width = window.winfo_screenwidth()               
height = window.winfo_screenheight()               
window.geometry("%dx%d" % (width, height))



Button(window, text="Actualiser", command=show_outputs, width=width, height=200).pack()


show_outputs()



window.mainloop()

