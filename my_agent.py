#!/usr/bin/env python3

"""
File Name:      my_agent.py
Authors:        Zhangqi Liu, Ruoyang Xu
Date:           2019.4.14

Description:    Python wrapper for our sensing and motion agent.
Source:         Adapted from recon-chess (https://pypi.org/project/reconchess/)
"""

import random
import chess
from player import Player
from chesspiece import EnemyChessBoard
from chessplay import ChessPlay

# TODO: Rename this class to what you would like your bot to be named during the game.
class MaybeBetterThanRandom(Player):

    def __init__(self):
        self.enemyBoard = None
        self.prev_move_result = None
        self.position_of_capture = None
        self.player = None
        
    def handle_game_start(self, color, board):
        """
        This function is called at the start of the game.

        :param color: chess.BLACK or chess.WHITE -- your color assignment for the game
        :param board: chess.Board -- initial board state
        :return:
        """
        self.enemyBoard = EnemyChessBoard(ourcolor = color)
        c = 'w'
        if color == chess.BLACK:
            c = 'b'
        self.player = ChessPlay(c)

        
    def handle_opponent_move_result(self, captured_piece, captured_square):
        """
        This function is called at the start of your turn and gives you the chance to update your board.

        :param captured_piece: bool - true if your opponents captured your piece with their last move
        :param captured_square: chess.Square - position where your piece was captured
        """
        try:
            self.enemyBoard.updateEnemyMove(captured_piece, captured_square)
            self.enemyBoard.propagate()
            self.enemyBoard.postCaptureUpdate(captured_square)
        except:
            pass

        if captured_piece == True:
            self.player.eliminate(captured_square)

    def choose_sense(self, possible_sense, possible_moves, seconds_left):
        """
        This function is called to choose a square to perform a sense on.

        :param possible_sense: List(chess.SQUARES) -- list of squares to sense around
        :param possible_moves: List(chess.Moves) -- list of acceptable moves based on current board
        :param seconds_left: float -- seconds left in the game

        :return: chess.SQUARE -- the center of 3x3 section of the board you want to sense
        :example: choice = chess.A1
        """
        try:
            sensing_location = self.enemyBoard.generateSensing()
            if sensing_location in possible_sense:
                return sensing_location
            else:
                return random.choice(possible_sense)
        except:
            return random.choice(possible_sense)

        
    def handle_sense_result(self, sense_result):
        """
        This is a function called after your picked your 3x3 square to sense and gives you the chance to update your
        board.

        :param sense_result: A list of tuples, where each tuple contains a :class:`Square` in the sense, and if there
                             was a piece on the square, then the corresponding :class:`chess.Piece`, otherwise `None`.
        :example:
        [
            (A8, Piece(ROOK, BLACK)), (B8, Piece(KNIGHT, BLACK)), (C8, Piece(BISHOP, BLACK)),
            (A7, Piece(PAWN, BLACK)), (B7, Piece(PAWN, BLACK)), (C7, Piece(PAWN, BLACK)),
            (A6, None), (B6, None), (C8, None)
        ]
        """
        try:
            self.enemyBoard.updateSensing(sense_result)
        except:
            pass

    def choose_move(self, possible_moves, seconds_left):
        """
        Choose a move to enact from a list of possible moves.

        :param possible_moves: List(chess.Moves) -- list of acceptable moves based only on pieces
        :param seconds_left: float -- seconds left to make a move
        
        :return: chess.Move -- object that includes the square you're moving from to the square you're moving to
        :example: choice = chess.Move(chess.F2, chess.F4)
        
        :condition: If you intend to move a pawn for promotion other than Queen, please specify the promotion parameter
        :example: choice = chess.Move(chess.G7, chess.G8, promotion=chess.KNIGHT) *default is Queen
        """
        try:
            choose = self.player.decision_make(possible_moves, self.enemyBoard.returnDistribution(), seconds_left)
            
            if choose == None:
                return random.choice(possible_moves)
            #translate tuple to chess.Move
            tanslator = ['A','B','C','D','E','F','G','H']
            #print(choose)
            move = tanslator[choose[0][1]] + str(8-choose[0][0])+tanslator[choose[1][1]]+str(8-choose[1][0])
            #print(move[:2],move[2:])
            src = eval("chess."+move[:2])
            to = eval("chess."+move[2:])

            return chess.Move(src,to)
        except:
            return random.choice(possible_moves)

        
    def handle_move_result(self, requested_move, taken_move, reason, captured_piece, captured_square):
        """
        This is a function called at the end of your turn/after your move was made and gives you the chance to update
        your board.

        :param requested_move: chess.Move -- the move you intended to make
        :param taken_move: chess.Move -- the move that was actually made
        :param reason: String -- description of the result from trying to make requested_move
        :param captured_piece: bool - true if you captured your opponents piece
        :param captured_square: chess.Square - position where you captured the piece
        """
        try:
            self.player.update(taken_move)
            self.enemyBoard.updateAllyBoard(taken_move, captured_piece, captured_square)
        except:
            pass
        
    def handle_game_end(self, winner_color, win_reason):  # possible GameHistory object...
        """
        This function is called at the end of the game to declare a winner.

        :param winner_color: Chess.BLACK/chess.WHITE -- the winning color
        :param win_reason: String -- the reason for the game ending
        """
        # TODO: implement this method
        pass
