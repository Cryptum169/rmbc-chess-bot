import random
import logging
import numpy as np
import chess
import datetime
import copy

EXISTENCE_THRESHOLD = 0.8
PROPAGATION_THRESHOLD = 0.001
np.set_printoptions(precision=5, suppress=True)

class EnemyChessBoard:

    def __init__(self, ourcolor):
        logging.basicConfig(filename='debug.log',level=logging.DEBUG)
        # Color of us
        self.color = ourcolor
        logging.info("Test at {}".format(datetime.datetime.now()))
        logging.info("Color: {}".format(self.color))
        self.chessPiece = ['r1','n1','b1','q','k','b2','n2','r2',
        'p1','p2','p3','p4','p5','p6','p7','p8']
        self.pieceDistri = dict()
        self.survivingCount = 16

        empty_board = np.zeros((6,8), dtype = np.float_)
        occupied_space = np.ones((2,8), dtype = np.float_)
        self.allyBoard = np.concatenate((empty_board,occupied_space), axis = 0)
        if (self.color == chess.BLACK):
            self.allyBoard = np.rot90(np.rot90(self.allyBoard))
        logging.info("Ally Initial Board")
        logging.info(self.allyBoard)

        for piece_index, piece in enumerate(self.chessPiece):
            initial_distribution = np.zeros((8,8), dtype = np.float_)
            y_idx = piece_index % 8
            x_idx = (int)(piece_index / 8)
            initial_distribution[x_idx][y_idx] = 1
            if (self.color == chess.BLACK):
                initial_distribution = np.rot90(np.rot90(initial_distribution))
            self.pieceDistri[piece] = initial_distribution
        
        logging.info('Board Initialization Complete')
        logging.info(sum([v for k,v in self.pieceDistri.items()]))
            
    def generateLookup(self):
        pass

    def update(self, observation):
        self.captured = False

    # Propagate Distribution
    def propagate(self):
        for item in self.chessPiece:
            current_distribution = self.pieceDistri[item]
            updated_distribution = np.zeros((8,8), dtype = np.float_)

            piece_type = item[0]
            available_move = []
            if (piece_type == 'p'):
                updated_distribution = self._pawn_propagate(current_distribution)
            elif (piece_type == 'r'):
                updated_distribution = self.piece_propagate(current_distribution, self._rook_available_moves)
            elif (piece_type == 'b'):
                continue
                # updated_distribution = self.piece_propagate(current_distribution, self._biship_available_moves)
            elif (piece_type == 'n'):
                updated_distribution = self.piece_propagate(current_distribution, self._knight_available_moves)
            elif (piece_type == 'q'):
                continue
                # updated_distribution = self.piece_propagate(current_distribution, self._queen_available_moves)
            elif (piece_type == 'k'):
                updated_distribution = self.piece_propagate(current_distribution, self._king_available_moves)
            else:
                logging.fatal("Abnormal Chess piece: {}".format(item))

            self.pieceDistri[item] = updated_distribution

    def returnDistribution(self):
        return copy.deepcopy(self.pieceDistri[item])

    def testEnvironment(self):
        print(self.pieceDistri['p1'])
        print(self.pieceDistri['r1'])
        print(np.sum(self.pieceDistri['n1']))
        
        # for item in self.chessPiece:
        #     if (item[0] == 'p'):
        #         print(self.pieceDistri[item])

    def allyCapturedNotify(self, location):
        self.captured = True
        self.captured_location = location

    # Call upon making a move
    def updateAllyBoard(self, move):
        move_string = move.uci()
        logging.info("My Move: {}".format(move_string))
        (start, end) = self._move_string_to_idx(move_string)
        self.allyBoard[start[0]][start[1]] = 0
        self.allyBoard[end[0]][end[1]] = 1
        logging.info("Update board:\n{}".format(self.allyBoard))

    def _move_string_to_idx(self, uci_move_string):
        start = (int(uci_move_string[1]), ord(uci_move_string[0]) - 97)
        end = (int(uci_move_string[3]), ord(uci_move_string[2]) - 97)
        return (start, end)

    def _pawn_available_moves(self, location):
        return_list = []
        if (self.color == chess.BLACK):
            step = -1
        else:
            step = 1

        candidate_location = [(location[0] + step,location[1])]
        ret_location = []
        if location[0] == 1 and step == 1 or location[0] == 6 and step == -1:
            candidate_location.append((location[0] + step * 2, location[1]))

        return self._check_possibility(candidate_location)

    def _pawn_propagate(self, distri):
        # Diagonal Case Handled else where
        if (self.color == chess.BLACK):
            iterator = list(reversed(range(8)))
            step = -1
        else:
            iterator = list(range(8))
            step = 1
        return_mat = np.zeros((8,8), dtype = np.float_)

        for column in iterator:
            for row in iterator:
                current_dist = distri[row][column]
                if current_dist < 0.01:
                    continue
                
                available_move = self._pawn_available_moves((row,column))
                if (len(available_move) == 0):
                    return_mat[row][column] += current_dist
                    continue

                prob_of_move = 1 / self.survivingCount
                bias = self.biasFunction((row, column))
                prob_of_move *= bias
                return_mat[row][column] += (1 - prob_of_move) * current_dist

                split = 1 / len(available_move)

                for position in available_move:
                    return_mat[position[0]][position[1]] += prob_of_move * current_dist * split

        return return_mat / np.sum(return_mat)
    
    def piece_propagate(self, distri, selection_algorithm):
        if (self.color == chess.BLACK):
            iterator = list(reversed(range(8)))
            step = -1
        else:
            iterator = list(range(8))
            step = 1
        return_mat = np.zeros((8,8), dtype = np.float_)

        for column in iterator:
            for row in iterator:
                current_dist = distri[row][column]
                if current_dist < PROPAGATION_THRESHOLD:
                    continue
                
                available_move = selection_algorithm((row,column))
                if (len(available_move) == 0):
                    return_mat[row][column] += current_dist
                    continue

                prob_of_move = 1 / self.survivingCount
                bias = self.biasFunction((row, column))
                prob_of_move *= bias
                return_mat[row][column] += (1 - prob_of_move) * current_dist

                split = 1 / len(available_move)

                for position in available_move:
                    return_mat[position[0]][position[1]] += prob_of_move * current_dist * split

        return return_mat / np.sum(return_mat)

    def _rook_available_moves(self, location):
        return_list = []

        if (self.color == chess.BLACK):
            step = -1
        else:
            step = 1

        for left_idx in reversed(range(0, location[0])):
            
            result = 1
            for k, v in self.pieceDistri.items():
                if (v[left_idx][location[1]] > EXISTENCE_THRESHOLD):
                    result = 0
                    break
            
            if (self.allyBoard[left_idx][location[1]] == 1):
                result = 0

            if result == 0:
                break
            else:
                return_list.append((left_idx, location[1]))

        for left_idx in range(location[0] + 1, 8):
            result = 1
            for k, v in self.pieceDistri.items():
                if (v[left_idx][location[1]] > EXISTENCE_THRESHOLD):
                    result = 0
                    break
            
            if (self.allyBoard[left_idx][location[1]] == 1):
                result = 0

            if result == 0:
                break
            else:
                return_list.append((left_idx, location[1]))

        for vertical_idx in reversed(range(0, location[1])):
            # print("This {}, {}".format(left_idx, location[1]))
            result = 1
            for k, v in self.pieceDistri.items():
                if (v[location[0]][vertical_idx] > EXISTENCE_THRESHOLD):
                    result = 0
                    break

            if (self.allyBoard[location[0]][vertical_idx] == 1):
                result = 0

            if result == 0:
                break
            else:
                return_list.append((location[0], vertical_idx))

        for vertical_idx in range(location[1] + 1, 8):
            result = 1
            for k, v in self.pieceDistri.items():
                if (v[location[0]][vertical_idx] > EXISTENCE_THRESHOLD):
                    result = 0
                    break
            
            if (self.allyBoard[location[0]][vertical_idx] == 1):
                result = 0

            if result == 0:
                break
            else:
                return_list.append((location[0], vertical_idx))

        return return_list

    def _knight_available_moves(self, location):
        candidate_location = []
        movement = [-2,-1,1,2]
        for x_movement in movement:
            for y_movement in movement:
                if y_movement == x_movement:
                    continue
                
                candidate_location.append((location[0] + x_movement, location[1] + y_movement))

        return self._check_possibility(candidate_location)
    
    def _biship_available_moves(self):
        return []
    
    def _queen_available_moves(self):
        return []

    def _king_available_moves(self, location):
        # First of all, king is very unlikely to move until danger close
        # IDK, danger close implement later ?

        candidate_locations = []
        for i in range(location[0] - 1, location[0] + 2):
            for k in range(location[1] - 1, location[0] + 2):
                candidate_locations.append((i,k))

        return self._check_possibility(candidate_locations)

    def _check_possibility(self, candidate_locations):
        return_list = []
        for x,y in candidate_locations:
            if x > 7 or x < 0 or y < 0 or y > 7:
                continue

            result = 1
            for k, v in self.pieceDistri.items():
                if (v[x][y] > EXISTENCE_THRESHOLD):
                    result = 0
                    break

            if (self.allyBoard[x][y] == 1):
                result = 0

            if result == 1:
                return_list.append((x,y))
        return return_list

    def biasFunction(self, location):
        return random.uniform(0.5,1)

    def boardBound(self, value):
        return min(max(value, 0), 7)

testBoard = EnemyChessBoard(ourcolor = chess.WHITE)

move = chess.Move.from_uci("a2a4")
move2 = chess.Move.from_uci("d2d4")

k = datetime.datetime.now()
testBoard.updateAllyBoard(move)
testBoard.updateAllyBoard(move2)
for i in range(70):
    testBoard.propagate()
testBoard.testEnvironment()