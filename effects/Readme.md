# Effects modules and, how to roll your own.

py_scrolly tries to implement a dynamic effects list. Each module in the 'effects' subdir will be loaded at runtime into a FIFO/rolling list of visual effects that will be applied to the text stream.

## RYO (Roll Your Own)
The basics of an effects module is meant to be fairly easy.

- make a module in this subdir with an appropriate name
- it's probably a good idea to import the 'config' module, though it is not required
- the module MUST have a function called 'effect' (without the quotes)
- the module will take two inputs which are PyGame Surfaces, my_canvas and txt_img
- Do what you want with txt_mg. Really, flip 'it, roll 'it, squeeze 'it, whatever you want.
- Paint your txt_img results onto the my_canvas Surface
- When the routine has ended, return the my_canvas and txt_img Surfaces

The file included in this subdir, template_py.txt should give you a good starting point.

## Naming the effects module
It is strongly suggested that you give your effects module an appropriate name. So a module that makes the text form a zig-zag pattern should be named something like 'zigzag.py'. This is to make it easier for the user to track which effects they have and to make it easier to find them if they need re-coding.

Effects modules are dynamically loaded into the rolling effects roster at runtime. The py_scrolly script takes a directory listing of the 'effects' subdir and loads those modules, one at a time, into memory.

This means that you can arrange the order in which the effects are used if you want. When the py_scrolly script first loads it loads in the 01_sinus.py and 02_slider.py as standard. This way, the first effect that is used when the script is run is always the 01_sinus effect. "Extra" effects are held in the 'effects' subdir and it is from here that the py_scrolly script dynamically loads its effects.

As the modules are loaded alphabetically, an effect module with a name starting '04' will be used before one with a name starting '05' and so on.
