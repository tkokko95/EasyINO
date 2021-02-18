from colorama import init, Fore, Back
import subprocess
from sys import argv
import argparse

def get_output(cmd : str):
    """Get output of a command as utf8"""

    return subprocess.run(cmd.split( ), capture_output=True, encoding='utf8').stdout

def parse_boards(cmd_out_str : str, board_filter : str):
    """A terrible mess of a function to parse the boards and their IDs into a list of dicts"""

    #Split the output by lines, remove the first (titles) and the last (empty) elements from the list
    lines = cmd_out_str.splitlines()

    #Strip whitespaces
    stripped_lines = []
    for line in lines[1:-1]:
        stripped_lines.append(line.strip())

    #Append the names and IDs as dictionaries into a list
    boardlist = []
    for line in stripped_lines:
        if not board_filter or line.lower().find(board_filter) != -1:
            splitline = line.split(' ')
            boardlist.append({
                'id'   : splitline.pop(-1),
                'name' : ' '.join(splitline)
                })
    return(boardlist)

def choose_board(boardlist : list):
    """List available boards, ask for choice and return the selected board"""
    for board in boardlist:
        print(Fore.BLACK + Back.WHITE + f'\n{boardlist.index(board)}: ' + Fore.WHITE + Back.BLACK)
        print('Name: ' + board['name'])
        print('FQBN: ' + board['id'] + '\n')

    while True:
        try:
            boardnum = int(input('Enter the # of the board: '))
        except ValueError:
            print('Invalid input')
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
        cmd = ''
        if args.upload:
         cmd +='arduino-cli board list'
        else:
            cmd += 'arduino-cli board listall'

        cmdout = get_output(cmd)
        boardlist = parse_boards(cmdout,args.board)
        if boardlist:
            board = choose_board(boardlist)
            if args.upload:
                pass
            else:
                pass

        else:
            print(Fore.RED + 'No boards found')
    except KeyboardInterrupt:
        print(Fore.RED + '\nAborted (CTRL + C)')




