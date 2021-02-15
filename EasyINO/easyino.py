import subprocess
from sys import argv

def get_output(cmd : str):
    """Get output of a command as utf8"""

    return subprocess.run(cmd.split( ), capture_output=True,encoding='utf8').stdout

def parse_boards(cmd_out_str : str):
    """A terrible mess of a function to parse the boards and their IDs into a list of dicts"""

    raw_boardlist = []
    boardlist = []
    cmd_out_lst = cmd_out_str.split('\n')[1:-2]

    for s in cmd_out_lst:
        s = s.strip()
        raw_boardlist.append(s)

    for board in raw_boardlist:
        board_split = board.split(' ')
        boardlist.append({
            'id' : board_split.pop(-1),
            'name' : ' '.join(board_split)
        })

    return boardlist

def choose_board(boardlist):
    """List available boards, ask for choice and return the selected board"""
    for board in boardlist:
        print(f'{boardlist.index(board)}: ')
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
                print('Invalid input')



if __name__ == '__main__':
    if '-u' not in argv and '--upload' not in argv:
        boardlist = parse_boards(get_output('arduino-cli board listall'))
        choose_board(boardlist)
        
        
        



