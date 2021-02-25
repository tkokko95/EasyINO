# EasyINO
A wrapper for arduino-cli, providing an interactive command-line UI for compiling and uploading programs.


# Usage

`easyino [options] [arguments] [file]`

## Options:
  *-b, --board [filter]*
	
	Filters boards by ID (e.g due, uno...)
  
  *-u, --upload*
	
	Uploads the program (only compiles as default)
	
  *-p, --arduinopath [path]*
  
  	Sets the path to arduino-cli, needed if it's not in your PATH

# Requirements
  * [arduino-cli](https://github.com/arduino/arduino-cli)

# Building

Built using pyinstaller. Requires [colorama](https://pypi.org/project/colorama/).

If you're using Linux, you may need to modify `pyinstaller/depend/utils.py` as described [here](https://github.com/pyinstaller/pyinstaller/issues/5540) (or use the current develop build). Hence, using a virtual environment is even more highly recommended than usual.










	
