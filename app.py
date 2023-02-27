#!/usr/bin/env python
from tkinter import *
import subprocess


def list_outputs():
	""" Récupération de la liste des sorties disponibles """
	interfaces = {}

	interfaces_list_raw = subprocess.run("echo $(sudo -u pi XDG_RUNTIME_DIR=/run/user/1000 pacmd list-sinks)"
	, shell=True, capture_output=True).stdout.decode()

	interfaces_list_raw = '''2 sink(s) available. index: 0 name: <alsa_output.platform-bcm2835_audio.analog-stereo> driver: <module-alsa-card.c> flags: HARDWARE DECIBEL_VOLUME LATENCY state: SUSPENDED suspend cause: IDLE priority: 9009 volume: front-left: 65536 / 100% / 0,00 dB, front-right: 65536 / 100% / 0,00 dB balance 0,00 base volume: 65536 / 100% / 0,00 dB volume steps: 65537 muted: no current latency: 0,00 ms max request: 0 KiB max rewind: 0 KiB monitor source: 0 sample spec: s16le 2ch 44100Hz channel map: front-left,front-right Stéréo used by: 0 linked by: 0 fixed latency: 59,95 ms card: 0 <alsa_card.platform-bcm2835_audio> module: 6 properties: alsa.resolution_bits = "16" device.api = "alsa" device.class = "sound" alsa.class = "generic" alsa.subclass = "generic-mix" alsa.name = "bcm2835 Headphones" alsa.id = "bcm2835 Headphones" alsa.subdevice = "0" alsa.subdevice_name = "subdevice #0" alsa.device = "0" alsa.card = "0" alsa.card_name = "bcm2835 Headphones" alsa.long_card_name = "bcm2835 Headphones" alsa.driver_name = "snd_bcm2835" device.bus_path = "platform-bcm2835_audio" sysfs.path = "/devices/platform/soc/3f00b840.mailbox/bcm2835_audio/sound/card0" device.form_factor = "internal" device.string = "hw:0" device.buffering.buffer_size = "10576" device.buffering.fragment_size = "2640" device.access_mode = "mmap" device.profile.name = "analog-stereo" device.profile.description = "Analog Stereo" device.description = "Audio interne Analog Stereo" module-udev-detect.discovered = "1" device.icon_name = "audio-card" ports: analog-output: Analog Output (priority 9900, latency offset 0 usec, available: unknown) properties: active port: <analog-output> README.md app.py raspi-config index: 1 name: <bluez_sink.03_08_3E_0F_0C_20.a2dp_sink> driver: <module-bluez5-device.c> flags: HARDWARE DECIBEL_VOLUME LATENCY state: SUSPENDED suspend cause: IDLE priority: 9050 volume: front-left: 65536 / 100% / 0,00 dB, front-right: 65536 / 100% / 0,00 dB balance 0,00 base volume: 65536 / 100% / 0,00 dB volume steps: 65537 muted: no current latency: 0,00 ms max request: 2 KiB max rewind: 0 KiB monitor source: 1 sample spec: s16le 2ch 44100Hz channel map: front-left,front-right Stéréo used by: 0 linked by: 0 fixed latency: 39,51 ms card: 1 <bluez_card.03_08_3E_0F_0C_20> module: 24 properties: bluetooth.protocol = "a2dp_sink" device.description = "BT SPEAKER " device.string = "03:08:3E:0F:0C:20" device.api = "bluez" device.class = "sound" device.bus = "bluetooth" device.form_factor = "headset" bluez.path = "/org/bluez/hci0/dev_03_08_3E_0F_0C_20" bluez.class = "0x340404" bluez.alias = "BT SPEAKER " device.icon_name = "audio-headset-bluetooth" device.intended_roles = "phone" ports: headset-output: Casque (priority 0, latency offset 0 usec, available: unknown) properties: active port: <headset-output>'''

	for interface in interfaces_list_raw.split("index: ")[1:]:
		name = ""

		if "alsa.name = " in interface:
			name = interface.split('alsa.name = "')[1].split('"')[0].replace("bcm2835 ", "").strip()
		elif "bluetooth" in interface:
			name = interface.split('device.description = "')[1].split('"')[0].strip()

		interfaces[interface.split(" ")[0]] = name

	return interfaces

def change_output(id):
	""" Changement de la sortie """
	result = subprocess.run(f"sudo -u pi XDG_RUNTIME_DIR=/run/user/1000 pactl set-default-sink {id}", shell=True)
	if result.returncode != 0:
		return False
	else:
		return True


window = Tk()
window.title = "Changement de sortie audio"
width = window.winfo_screenwidth()               
height = window.winfo_screenheight()               
window.geometry("%dx%d" % (width, height))

outputs = list_outputs()

for id, name in outputs.items():
	Button(window, text=name, command=lambda: change_output(id)).pack()







window.mainloop()

