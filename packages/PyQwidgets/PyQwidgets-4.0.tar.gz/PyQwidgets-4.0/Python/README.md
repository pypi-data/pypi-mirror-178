# PyQwidgets 4.0

In this brief description, I will introduce you to PyQwidgets!

With the help of this library, you can create a lot of things, 
for example, work with a browser or with widgets.

**Library installation:** <code>pip install PyQwidgets</code>

-----------------------------------------------------------------------------------------

## Functions

- Widgets
- Browser 

### Widgets

<code>Widgets.Error(name, text)</code> - This widget displays an error window.

<code>Widgets.Warning(name, text)</code> - This widget displays an alert box.

<code>Widgets.Info(name, text)</code> - This widget displays a window with information.

<code>Widgets.Screenshot(name)</code> - This widget takes a screenshot

**Code example**

<code>
	from PyQwidgets import *

	ERROR = Widgets.Error(name="Error", text="Error: You don't have Python installed!")

	WARNING = Widgets.Warning(Name="Warning", text="Warning: Without python, the program will not work for you")

	INFO = Widgets.Info(name="Information", text="Info: You have installed python!")

	SCREEN = Widgets.Screenshot(name="SCREEN.png")
</code>

-----------------------------------------------------------------------------------------

### Browser

<code>Browser.Download(url, name)</code> - Downloading files from the browser.

<code>Browser.Open(url)</code> - Open web page.

**Code example**

<code>
	from PyQwidgets import *

	DOWNLOAD = Browser.Download(url="https://youtube.com", name="YouTube.html")

	OPEN = Browser.Open(url="https://youtube.com")
</code>

----------------------------------------------------------------------------------------

ATTENTION!!! I'm new to python so don't judge too harshly!

Name: ***George***

Age: ***14 years old***

Email: zadvornow2908@gmail.com