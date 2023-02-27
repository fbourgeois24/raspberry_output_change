from tkinter import *
import subprocess


def update_outputs():
	""" Récupération de la liste des sorties disponibles """
	interfaces_list_raw = subprocess.run("echo $(sudo -u pi XDG_RUNTIME_DIR=/run/user/1000 pacmd list-sinks)"
	, shell=True, capture_output=True)

	print(interfaces_list_raw)


# window = Tk()
# window.title = "Changement de sortie audio"
# width = window.winfo_screenwidth()               
# height = window.winfo_screenheight()               
# window.geometry("%dx%d" % (width, height))









# window.mainloop()

update_outputs()