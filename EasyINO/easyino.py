from subprocess import run
from argparse import ArgumentParser
from colorama import init, Fore, Style
from os import path
from sys import exit # Apparently the executable version doesn't like it if we use Python's exit()

def run_cmd(command : str):
    """Run command and UTF-8 encoded output. If there's an error, print it and terminate"""

    proc = run(command, capture_output=True, encoding='utf8', shell=True)
    if proc.stderr:
        print(Style.BRIGHT + Fore.RED +  'An error occurred:' + Style.RESET_ALL)
        print(proc.stderr)
        exit(proc.returncode)
    else:
        return proc.stdout

def parse_boards(output, board_filter, upload_mode):
    """Parses the output and return board IDs and ports"""
    stripped_lines = []
    boards = []

    # Split the output by lines
    lines = output.splitlines()

    # Strip whitespaces
    # The first and the last entries in the list are useless so cut them
    for line in lines[1:-1]:
        stripped_lines.append(line.strip())

    # Get the board FQBN
    for line in stripped_lines:
        if not board_filter or line.lower().find(board_filter) != -1:
            line = line.split(' ')

            # If we list all, we only need the last column and we don't care about the port
            # If we list connected, we need the first from the left (port) and second from the right (FBQN)
            if not upload_mode:
                boards.append({
                    'id' : line[-1],
                    'port' : None
                })
            else:
                if line[-2]:
                    boards.append({
                        'id' : line[-2],
                        'port' : line[0]
                    })
                else:
                    boards.append({
                        'id' : '[UNKNOWN]',
                        'port' : line[0]
                    })
    #Return the list of dictionaries
    return boards

def choose_board(boards):
    """List available boards, ask for choice and return the selected board"""
    for board in boards:
        print(Style.BRIGHT + f"\n{boards.index(board)}: {board['id']}" + Style.RESET_ALL)
        if args.upload:
            print(Style.BRIGHT + f"Port: {board['port']}" + Style.RESET_ALL)

    while True:
        try:
            boardnum = int(input('\nEnter the # of the board: '))
            return boards[boardnum]
        except (ValueError, IndexError):
            print(Fore.YELLOW + 'Invalid input' + Fore.WHITE)
            

if __name__ == '__main__':
    #Initialize colorama to work on Windows
    init()

    #Initialize argument parser
    parser = ArgumentParser()
    parser.add_argument('file', help='sketch to compile/upload')
    parser.add_argument('-u', '--upload', help='upload sketch', action='store_true')
    parser.add_argument('-b', '--board', help='filter boards by name')
    parser.add_argument('-p', '--arduinopath',help='needed if arduino-cli is not in PATH', default='arduino-cli')
    args = parser.parse_args()
    FILEPATH = path.abspath(args.file)
    ARDUINO_PATH = args.arduinopath

    try:
        if args.upload:
            cmdout = run_cmd(f'{ARDUINO_PATH} board list')
        else:
            cmdout = run_cmd(f'{ARDUINO_PATH} board listall')
        boardlist = parse_boards(cmdout, args.board, args.upload)
        if boardlist:
            sel_board = choose_board(boardlist)
            cmdout = run_cmd(f"{ARDUINO_PATH} compile -b {sel_board['id']} {FILEPATH}")
            print(Fore.GREEN + Style.BRIGHT + '\nSketch compiled successfully:' + Style.RESET_ALL)
            print(cmdout)
            if args.upload:
                input('Proceed to upload? (CTRL + C to cancel, any other key to continue)')
                print('Uploading...')
                run_cmd(f"{ARDUINO_PATH} upload -b {sel_board['id']} -p {sel_board['port']} {FILEPATH}")
                print(Fore.GREEN + Style.BRIGHT + 'Sketch successfully uploaded' + Style.RESET_ALL)
        else:
            print(Fore.RED + 'No boards found' + Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.RED + '\nAborted (CTRL + C)' + Style.RESET_ALL)
