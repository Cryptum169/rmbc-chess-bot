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

        self.rook_count = 2
        self.knight_count = 2

        self.allyCaptured = False

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

    def getColor(self):
        return copy.copy(self.color)
            
    def generateLookup(self):
        pass

    def updateEnemyMove(self, captured, location):
        if not captured:
            return

        # Update ally casulty
        self.allyCaptured = True
        location = (location % 8, 7 - (int(location / 8)))
        self.allyBoard[location[0]][location[1]] = 0

        # Handle distribution update in later
        return

    def postCaptureUpdate(self, location):
        if not self.allyCaptured:
            return

        self.allyCaptured = False
        location = (location % 8, 7 - (int(location / 8)))

        # idk if we need this
        max_key = ""
        sum_dist = 0

        for k, v in self.pieceDistri.items():
            prob = v[location[0]][location[1]]
            sum += prob

        for k, v in self.pieceDistri.items():
            prob_at_location = v[location[0]][location[1]]
            post_distri = prob_at_location / sum
            remaining_probability = 1 - post_distri
            v *= (remaining_probability / (1 - prob_at_location))

        return

    def updateSensing(self, observation):
        for idx, piece in observation:
            column = idx % 8
            row = 7 - (int(idx / 8))

            if not piece is None:
                result_piece = piece.symbol()
                print(result_piece)
                # One of ours
                if (self.color == chess.WHITE) and result_piece.isupper():
                    continue
                elif (self.color == chess.BLACK) and result_piece.islower():
                    continue

            # First, update all others
            for k, v in self.pieceDistri.items():
                if piece is None or not k[0] == piece.symbol().lower():
                    v[row][column] = 0
            
            if piece is None:
                continue

            if piece.piece_type == chess.PAWN:
                pass
            elif piece.piece_type == chess.BISHOP:
                if (row + column) % 2 == 0:
                    v = self.pieceDistri['b1']
                else:
                    v = self.pieceDistri['b2']
                v.fill(0)
                v[row][column] = 1
            elif piece.piece_type == chess.ROOK:
                pass
            elif piece.piece_type == chess.KNIGHT:
                if self.knight_count == 1:
                    v = self.pieceDistri['n1']
                    v.fill(0)
                    

            elif piece.piece_type == chess.QUEEN:
                # There is only one queen
                v = self.pieceDistri['q']
                v.fill(0)
                v[row][column] = 1
            elif piece.piece_type == chess.KING:
                # There is only one queen
                v = self.pieceDistri['k']
                v.fill(0)
                v[row][column] = 1
            else:
                print("WHAT THE HECK DID I SEE?")

        # Scale up to normalize and offset difference in between
        for k,v in self.pieceDistri.items():
            v /= np.sum(v)
        
        return

    def generateSensing(self):
        pass

    def returnDistribution(self):
        return copy.deepcopy(self.pieceDistri)

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
                updated_distribution = self.piece_propagate(current_distribution, self._biship_available_moves)
            elif (piece_type == 'n'):
                updated_distribution = self.piece_propagate(current_distribution, self._knight_available_moves)
            elif (piece_type == 'q'):
                updated_distribution = self.piece_propagate(current_distribution, self._queen_available_moves)
            elif (piece_type == 'k'):
                updated_distribution = self.piece_propagate(current_distribution, self._king_available_moves)
            else:
                logging.fatal("Abnormal Chess piece: {}".format(item))
                print("See abnormal chess piece")

            self.pieceDistri[item] = updated_distribution

    # Call upon making a move
    def updateAllyBoard(self, move, captured_piece, captured_square):
        if (move is None):
            return 

        move_string = move.uci()
        logging.info("My Move: {}".format(move_string))
        (start, end) = self._move_string_to_idx(move_string)
        self.allyBoard[start[0]][start[1]] = 0
        self.allyBoard[end[0]][end[1]] = 1
        logging.info("Update board:\n{}".format(self.allyBoard))

        # TODO THIS IS NOT DONE YET

    def _move_string_to_idx(self, uci_move_string):
        start = (7 - (int(uci_move_string[1]) - 1), ord(uci_move_string[0]) - 97)
        end = (7 - (int(uci_move_string[3]) - 1), ord(uci_move_string[2]) - 97)
        return (start, end)

    def _pawn_available_moves(self, location):
        return_list = []
        if (self.color == chess.BLACK):
            step = -1
        else:
            step = 1

        candidate_location = [(location[0] + step,location[1])]

        if location[0] + step < 0 or location[0] + step > 7:
            return []

        location1 = location[1] - 1
        location2 = location[1] + 1

        if location1 > -1:
            if self.allyBoard[location[0] + step, location1] == 1:
                candidate_location.append((location[0] + step, location1))

        if location2 < 8:
            if self.allyBoard[location[0] + step, location2] == 1:
                candidate_location.append((location[0] + step, location2))

        ret_location = []
        if location[0] == 1 and step == 1 or location[0] == 6 and step == -1:
            candidate_location.append((location[0] + step * 2, location[1]))

        return self._check_possibility(candidate_location, pawn = True)

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
                if abs(y_movement) == abs(x_movement):
                    continue
                
                candidate_location.append((location[0] + x_movement, location[1] + y_movement))

        return self._check_possibility(candidate_location)
    
    def _biship_available_moves(self, location):
        candidate_location = []

        new_location = (0,0)
        for x in range(1, location[0]):
            new_location = (location[0] - x, location[1] - x)
            if new_location[0] > -1 and new_location[1] > -1:
                for k,v in self.pieceDistri.items():
                    if v[new_location[0]][new_location[1]] < EXISTENCE_THRESHOLD:
                        candidate_location.append(new_location)
            else:
                break;

        for x in range(1, location[0]):
            new_location = (location[0] - x, location[1] + x)
            if new_location[0] > -1 and new_location[1] < 8:
                for k,v in self.pieceDistri.items():
                    if v[new_location[0]][new_location[1]] < EXISTENCE_THRESHOLD:
                        candidate_location.append(new_location)
            else:
                break;

        for x in range(location[0] + 1, 7):
            new_location = (location[0] + x, location[1] + x)
            if new_location[0] < 8 and new_location[1] < 8:
                for k,v in self.pieceDistri.items():
                    if v[new_location[0]][new_location[1]] < EXISTENCE_THRESHOLD:
                        candidate_location.append(new_location)
            else:
                break;

        for x in range(location[0] + 1, 7):
            new_location = (location[0] + x, location[1] - x)
            if new_location[0] < 8 and new_location[1] > -1:
                for k,v in self.pieceDistri.items():
                    if v[new_location[0]][new_location[1]] < EXISTENCE_THRESHOLD:
                        candidate_location.append(new_location)
            else:
                break;

        return self._check_possibility(candidate_location)
    
    def _queen_available_moves(self, location):
        diag = self._biship_available_moves(location)
        grid = self._rook_available_moves(location)
        return grid + diag

    def _king_available_moves(self, location):
        # First of all, king is very unlikely to move until danger close
        # IDK, danger close implement later ?

        candidate_locations = []
        for i in range(location[0] - 1, location[0] + 2):
            for k in range(location[1] - 1, location[0] + 2):
                candidate_locations.append((i,k))

        return self._check_possibility(candidate_locations)

    def _check_possibility(self, candidate_locations, pawn = False):
        return_list = []

        if pawn:
            column = candidate_locations[0][1]

        for x,y in candidate_locations:
            if x > 7 or x < 0 or y < 0 or y > 7:
                continue

            result = 1
            for k, v in self.pieceDistri.items():
                if (v[x][y] > EXISTENCE_THRESHOLD):
                    result = 0
                    break

            if (self.allyBoard[x][y] == 1):
                if not pawn:
                    result = 0
                else:
                    if y == column:
                        result = 0

            if result == 1:
                return_list.append((x,y))
        return return_list

    def biasFunction(self, location):
        return random.uniform(0.5,1)

    # Deprecated
    def boardBound(self, value):
        return min(max(value, 0), 7)

    # Do not enable during testing
    def testEnvironment(self):
        print(self.pieceDistri['q'])
        print(np.sum(self.pieceDistri['q']))

testBoard = EnemyChessBoard(ourcolor = chess.BLACK)

print(testBoard.pieceDistri['b1'])

# move = chess.Move.from_uci("a2a4")
# move2 = chess.Move.from_uci("d2d4")

# k = datetime.datetime.now()
# testBoard.updateAllyBoard(move)
# testBoard.updateAllyBoard(move2)
# for i in range(7):
#     testBoard.propagate()
# # testBoard.testEnvironment()
