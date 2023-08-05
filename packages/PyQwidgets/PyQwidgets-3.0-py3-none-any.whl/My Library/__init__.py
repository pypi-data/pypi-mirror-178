# Name: PyQwidgets
# Version: 3.0

import webbrowser as wb
import wget
import os

class PyQwidgets():
	
	def Browser(url):
		wb.open(url)
		
	def Download(url, name):
		wget.download(url, name)

	def pip(command, options):
		os.system(f"pip {command} {options}")