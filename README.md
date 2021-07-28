# py_scrolly : v1.0 (27 Jul 2021)

## Description:

py_scrolly is a python script that provides a graphical and musical desktop toy. It takes lines from a text file and animates them on the system’s screen.

## Dependencies:

py_scrolly uses the following external modules:
- pygame – v2.0.1
- numpy – v1.20.3

These modules can be installed using pip, if needed:

`pip install pygame`

`pip install numpy`

..but you knew that already, right?

## Using py_scrolly:

Using py_scrolly is pretty easy to do. Provided the module dependencies are installed then launching py_scrolly is as easy as typing:

`python py_scrolly.py`

….but you knew that already, right?

On starting up, py_scrolly will open a window on your system’s desktop *[1]* showing a line of text scrolling, right to left, across the screen. When the live of text scrolls off the left-hand end of the screen the next line of text will start scrolling, right to left, across the screen.

*[1]*: While the py_scrolly.py can provide a fullscreen display it is designed to start up with windowed output. Pressing the ‘f’ key kicks the output into, and out of fullscreen mode.

Each line of text will be displayed using a different animation ‘effect’. Currently, the effects that are available to py_scrolly are:

- sinus – the text will form a rolling sinewave across the screen
- slider – the text will scroll across the screen in the style of a news screen textual tickertape
- magnify – similar to the slider effect but the middle of the line will appear magnified

These effects are applied to the different lines of text in a round-robin fashion. The current setup uses these effects in the order show above. The effects list ‘rolls over’ so after the magnify effect is used the script will start again with the sinus effect.

## Runtime user interaction:

As this is intended as a “toy” there is little real input to the script. However the user does have some options that they can apply to affect the operation of the script. These are shown in the on-screen menu.

The options are, as follow:
| Key | Action |
| --- | ----- |
| q | quit the script |
| f | flip the program between windowed and fullscreen view |
| m | mute, or unmute the music file that is playing |
| backspace | Hide or reveal the on-screen menu |
|spacebar | pressing the spacebar will pause or resume the scrolling of the text across the screen. This does not affect the background animations or the playing of music|

## The message.txt file:

There are some options are available to the user to change the operation of the py_scrolly script.

The main change that the user can set the message lines that scroll across the screen. These are held in the message.txt file which is a plaintext file. The lines read from this file are displayed to screen in a rolling FIFO fashion so when the script reaches the end of the message lines it starts again with the first line.

The change of graphical text effect is triggered when the py_scrolly script reaches the end of the line it is currently displaying. Whole paragraphs or a single letter can be made to scroll across the screen, being displayed with the currently available effect.

No message will be displayed onscreen if the script encounters an empty line in the message.txt file. It will just cause an apparent ‘pause’ before the next line of text is displayed. This is a design feature as it allows each displayed line time to get clear of the screen before the next line is displayed.

If the message.txt file is not present in the same directory as the py_scrolly script is launched from then an error/’nag’ message will appear onscreen to inform the user that the script could not find this text file.

## MP3 file:

The music file that is included with the py_scrolly.py script is called “Mellow strain”. It is an MP3  transcoding of a MOD-format file that was produced by the artist and long time collaborator and friend U4iaF8. It has been included in the release of the py_scrolly.py script with his permission. More of U4iaF8’s work is available for download from https://modarchive.org/index.php?request=view_profile&query=69242

The py_scrolly script is written so that it will play the first MP3 file that it finds in its current working directory. The user can play any MP3 file that they choose by putting the file into the directory with the py_scrolly.py script.

Please note: the py_scrolly script will play the FIRST MP3 file that it discovers in this directory. So an MP3 file with a filename that appears lower down a directory listing will be ignored. The user can either remove the mellow_strains.mp3 file or give their own MP3 file a name that starts with a letter in the range A-l.

## Displayed message font:

The TrueType font file included with the py_scrolly.py script is called |Rubik. It is available on an Open Fonts Licence which allows the font to be used freely in products. It can be downloaded from https://fonts.google.com/specimen/Rubik

## The PyGame module:

The PyGame module is the engine that drives the graphical output generated by py_scrolly.py. It can installed easily by typing the following into a terminal/command shell:

`pip install pygame`

py_scrolly uses the latest version of PyGame, which is currently V2.0.1 . 


### Notes
This is a learning project for me. I just couldn't face having to write yet another 'Hello world!' script to get started on a new language.

The initial targets for this script were just to get a python script up and running and, to see if I could get it to open a window on the screen. Once those targets were met, the design targets expanded. Below are some of the features I was aiming to incorporate in the code:

- [x] Multiple lines of differing text scrolling across a screen
- [x] Initial text effects are to "slide" the text across the screen and, to make the text follow a "sinus"
- [x] Make it so the script can autoload new 'effects' when it is run
- [x] Provide a shifting backdrop filled with stars
- [x] Add stars streaming from the visual centre of the scene
- [x] Make it easy to change the text that is being scrolled on the screen
- [x] Make it easy to change the music playing in the background
- [x] Have the mouse pointer autohide after ten seconds

There are also "failsafe" routines in the code. These do things like trap if there is no file containing the text messages or, there is no music file (an MP3) to play. It also is designed to use a certain font to display the messages. That font is supplied with the script and is open source. The script will check to see if the font is  already installed on the system. If it is not then the script will access the font direct from the file, without installing it to your system.
