from colorama import init, Fore, Style
import subprocess
from sys import argv
import argparse

def get_output(cmd : str):
    """Get output of a command as utf8"""

    return subprocess.run(cmd.split( ), capture_output=True, encoding='utf8').stdout

def parse_boards():
    """A terrible mess of a function to parse the boards and their IDs into a list of dicts"""
    stripped_lines = []
    boardlist = []

    # Split the output by lines
    lines = cmdout.splitlines()

    # Strip whitespaces
    # The first and the last entries in the list are useless so cut them
    for line in lines[1:-1]:
            stripped_lines.append(line.strip())

    # Get the board FQBN
    for line in stripped_lines:
        if not args.board or line.lower().find(args.board) != -1:
            line = line.split(' ')

            # If we list all, we only need the last column and we don't care
            # about the port

            # If we list connected, we need the first (port) and second
            # from the right (FBQN)
            if not args.upload:
                boardlist.append((line[-1], None))
            else:
                if line[-2]:
                    boardlist.append((line[-2], line[0]))
                else:
                    boardlist.append(('[UNKNOWN]', line[0]))

    #Return a tuple, in format (FBQN, Port)
    return(boardlist)

def choose_board():
    """List available boards, ask for choice and return the selected board"""
    for board in boardlist:
        print(Style.BRIGHT + f'\n{boardlist.index(board)}: {board[0]}' + Style.RESET_ALL)
        if args.upload:
            print(Style.BRIGHT + f'Port: {board[1]}' + Style.RESET_ALL)

    while True:
        try:
            boardnum = int(input('\nEnter the # of the board: '))
        except ValueError:
            print(Fore.YELLOW + 'Invalid input' + Fore.WHITE)
        else:
            if boardnum < len(boardlist):
                return boardlist[boardnum]
            else:
                print(Fore.YELLOW + 'Invalid input' + Fore.WHITE)

def compile(file, board, verbose):
    pass

def upload(file, board, verbose):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('file', help='sketch to compile or upload')
    parser.add_argument('-v', '--verbose', help='enable verbose output', action='store_true')
    parser.add_argument('-u', '--upload', help='upload sketch', action='store_true')
    parser.add_argument('-b', '--board', help='filter boards by name')
    args = parser.parse_args()

    #Initialize colorama to work on Windows
    init()

    try:
        if args.upload:
            cmd ='arduino-cli board list'
        else:
            cmd = 'arduino-cli board listall'

        cmdout = get_output()
        boardlist = parse_boards()
        if boardlist:
            board = choose_board()
            if args.upload:
                pass
            else:
                pass

        else:
            print(Fore.RED + 'No boards found' + Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.RED + '\nAborted (CTRL + C)' + Style.RESET_ALL)




