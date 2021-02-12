# EasyINO
A wrapper for arduino-cli, providing an interactive command-line UI for compiling and uploading programs.


# Usage

`easyino [options] [arguments] [file]`

## Options:
  *-b, --board [filter]*
	
	Filters the list of boards
  
  *-u, --upload*
	
	Uploads the program (only verifies as default)
  
  *-v, --verbose*
	
	Verbose output
	


# Requirements
  * Python (Tested on 3.9.1)
  * [arduino-cli](https://github.com/arduino/arduino-cli) (Make sure that it's included in your PATH. Alternatively, you can modify the .py file to point at the executable.)
	
