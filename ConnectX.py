# Author: https://github.com/ForeverHaibara 
# Game Intro: https://www.kaggle.com/c/connectx 

from random import randint
from matplotlib import pyplot as plt

class ConnectXBoard():
    def __init__(self, players = None,
             width = 7, height = 6, connect = 4, turn = None):
        # initialize chess board with size width * height 
        # connect ''connect'' to win
        if width <= 0 or height <= 0 or connect <= 0:
            width , height , connect = 7 , 6 , 4
        self.w = width
        self.h = height
        self.c = connect


        # start with turn 0 / 1 (random if turn == None)
        self.t = (turn != 0) if turn is not None else randint(0,1)
        # self.end = 0: first player wins; 1: second player wins
        self.end = -1   

        self.board = [[-1 for _ in range(self.w)] for __ in range(self.h)]
        self.stack = [0 for _ in range(self.w)]
        self.total = 0 # total moves

        # record the names of players
        self.players = ['Player 1', 'Player 2'] if players is None else players 
        
    def play(self, x, player = None):
        # not current player
        if player is not None and self.players[self.t] != player:
            return None , -1
        try: 
            x = int(x) - 1
            if x < 0 or x >= self.w:
                return f'Input only figures integers in {1} ~ {self.w}' , 0
        except:
            return 'Error' , 0

        if self.stack[x] == self.h:
            return 'Cannot select this column because it is already full!' , 0
    
        self.stack[x] += 1
        self.board[-self.stack[x]][x] = self.t 
        self.total += 1
        self.check_win(self.h-self.stack[x], x)
        if self.end == -1: 
            self.t ^= 1
            return self.urge() , 1
        elif self.end < 2:
            return f'Congratulations to @{self.players[self.t]}!' , 1
        else:
            return f'Game Tied!' , 1
        
    def urge(self):
        return f"@{self.players[self.t]} It is {self.players[self.t]}'s turn"

    def count(self, x, y, d, t):
        # count how many consecutive chesses in color t is in the direction
        # (self-included)
        s = 0
        # reference / pointer but not copy here
        b = self.board
        while 0 <= x < self.h and 0 <= y < self.w:
            if b[x][y] != t:
                break 
            s += 1
            x += d[0]
            y += d[1]
        return s
    
    def check_win(self, x, y):
        c = self.c
        t = self.t
        if self.count(x,y,(1,0),t) >= c: self.end = t
        elif self.count(x,y,(0,-1),t) + self.count(x,y,(0,1),t) > c: self.end = t
        elif self.count(x,y,(-1,-1),t) + self.count(x,y,(1,1),t) > c: self.end = t 
        elif self.count(x,y,(-1,1),t) + self.count(x,y,(1,-1),t) > c: self.end = t

        if self.end == -1 and self.total >= self.w * self.h: # tie
            self.end = 2 
        #if self.end >= 0 : print('win type =', self.end, ' ; ', y + 1, self.h - x)
        return self.end
        

    def save_board(self, path = '', show = False, dpi = 500):
        # save the chessboard image to the path
        plt.figure()
        plt.pcolormesh(self.board[::-1], edgecolors = 'gray', linewidth = 1,
                cmap = 'inferno', vmin = -1., vmax = 1.)
        plt.axis('off')
        plt.gca().set_aspect('equal')
        if show: plt.show()
        if len(path) > 0:
            plt.savefig(path, bbox_inches = 'tight', dpi = dpi)
            plt.close()


class ConnectXManager():
    # a connectX chessboard manager with automatic memory management
    def __init__(self, maxhandle = 15, path = 'Figure.png'):
        # handle at most 15 chesses at one time
        # all chess boards
        self.maxhandle = maxhandle
        self.chesses = [None] * maxhandle

        # automatically save the chessboard image to path
        self.path = path

        # record the chessboard index a player is currently playing
        self.playing = {}
    
    def create(self, players = None,
            width = 7, height = 6, connect = 4, turn = None):
        # create a game with two players
        for player in players:
            if player in self.playing.keys():
                return

        for i in range(self.maxhandle):
            if self.chesses[i] == None:
                self.chesses[i] = ConnectXBoard(players, width, height, connect, turn) 
                for player in players:
                    self.playing[player] = i
                #print(self.playing)
                self.chesses[i].save_board(self.path)
                return self.chesses[i].urge()
        
    def play(self, player, x, save = True):
        if player not in self.playing.keys():
            return None
        # player plays x
        index = self.playing[player]
        result = self.chesses[index].play(x, player = player)
        if result[1] == 1: # valid move
            if save: self.chesses[index].save_board(self.path)
            
            if self.chesses[index].end != -1: # gameover and destroy the chessboard
                self.remove(index)
        elif result[1] == -1:
            return None

        return result[0]

    def remove(self, index):
        # remove chessboard
        for player in self.chesses[index].players:
            self.playing.pop(player)
        tmp = self.chesses[index] 
        self.chesses[index] = None
        del tmp
    
    def giveup(self, player):
        # give up the chess the player is currently playing
        if player not in self.playing.keys():
            return None
        self.remove(self.playing[player])




if __name__ == '__main__':
    #record = '1 1 1 1 5 2 2 3 4 3 3 4 6 7 4 2 4'
    record = '1 1 1 1 5 2 2 3 4 3 3 4 6 7 4 1 2'
    #record = '1 1 1 1 5 2 2 3 4 3 4 4 4 5 3'
    #record = '1 1 1 1 5 2 2 3 4 3 4 5 7 6 3 2 2'
    #record = '1 1 1 1 5 2 2 3 4 3 4 5 7 6 3 3 2 4'
    #record = '0 1 0 1 1 1 1 1 1 1 4 2 3 2 2 4 3 3'
    '''
    board = ConnectXBoard()
    print(board.urge())
    for x in record.split():
        print( board.play(x) )
    board.save_board('Figure.png')
    '''
    cntx_manager = ConnectXManager()
    cntx_manager.create(['playerA','playerB'])
    cntx_manager.create(['playerC','playerD'])
    print(cntx_manager.play('playerA',1))
    print(cntx_manager.play('playerB',4))
