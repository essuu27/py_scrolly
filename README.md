#Project name: py_scrolly
 ## Synopsis
 A graphical text scroller, written in python
 
### Description
This script aims to take the lines from a text file and scroll them across the screen. Each line will have a different effect applied 
to it, to make the display interesting to watch. It uses the PyGame library, written by Peter Shinners, to provide graphical functions.

It has been designed and developed on a desktop system.

### Notes
The initial targets for this script were just to get a python script up and running and, to see if I could get it to open a window on the screen. Once those targets were met, the design targets expanded. Below are some of the features I was aiming to incorporate in the code:

- [x] Multiple lines of differing text scrolling across a screen
- [x] Initial text effects are to "slide" the text across the screen and, to make the text follow a "sinus"
- [x] Make it so the script can autoload new 'effects' when it is run
- [x] Provide a shifting backdrop filled with stars
- [x] Add stars streaming from the visual centre of the scene
- [x] Make it easy to change the text that is being scrolled on the screen
- [x] Make it easy to change the music playing in the background
- [x] Have the mouse pointer autohide after ten seconds

There are also "failsafe" routines in the code. These do things like trap if there is no file containing the text messages or, there is no music file (an MP3) to play. It also is designed to use a certain font to display the messages. That font is supplied with the script and is open source. The script will check to see if the font is 
already installed on the system. If it is not then the script will access the font direct from the file, without installing it to your system.
