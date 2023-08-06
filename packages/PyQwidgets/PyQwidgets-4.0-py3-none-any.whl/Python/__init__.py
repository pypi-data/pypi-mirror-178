# Name: PyQwidgets
# Version: 4.0

from tkinter import *
from tkinter import messagebox

import webbrowser
import pyautogui
import keyboard
import hashlib
import wget
import os

class Widgets:

    def Error(name, text):
        messagebox.showerror(name, text)

    def Warning(name, text):
        messagebox.showwarning(name, text)

    def Info(name, text):
        messagebox.showinfo(name, text)

    def Screenshot(name):
        pyautogui.screenshot(name)

class Browser:

    def Download(url, name):
        wget.download(url, name)

    def Open(url):
        webbrowser.open(url)
