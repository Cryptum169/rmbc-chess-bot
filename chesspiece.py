import random
import numpy as np
import chess
import datetime
import copy
from scipy.stats import entropy

EXISTENCE_THRESHOLD = 0.9
PROPAGATION_THRESHOLD = 0.0001

class EnemyChessBoard:

    # Done
    def __init__(self, ourcolor):
        # Color of us
        self.color = ourcolor
        self.chessPiece = ['r1','n1','b1','q','k','b2','n2','r2',
        'p1','p2','p3','p4','p5','p6','p7','p8']
        self.pieceDistri = dict()
        self.survivingCount = 16

        self.rook_count = 2
        self.knight_count = 2
        self.mightBeAlive = dict()
        self.markedDead = dict()

        self.allyCapturedPosition = -1
        self.allyCaptured = False

        self.lastSense = None

        empty_board = np.zeros((6,8), dtype = np.float_)
        occupied_space = np.ones((2,8), dtype = np.float_)
        self.allyBoard = np.concatenate((empty_board,occupied_space), axis = 0)
        if (self.color == chess.BLACK):
            self.allyBoard = np.rot90(np.rot90(self.allyBoard))

        for piece_index, piece in enumerate(self.chessPiece):
            initial_distribution = np.zeros((8,8), dtype = np.float_)
            y_idx = piece_index % 8
            x_idx = (int)(piece_index / 8)
            initial_distribution[x_idx][y_idx] = 1
            if (self.color == chess.BLACK):
                initial_distribution = np.rot90(np.rot90(initial_distribution))
            self.pieceDistri[piece] = initial_distribution
            if piece[0] != 'p':
                self.mightBeAlive[piece] = 1
                self.markedDead[piece] = 0


    # Done
    def getColor(self):
        return copy.copy(self.color)
        
    # Done
    def updateEnemyMove(self, captured, location):
        if not captured:
            return

        # Update ally casulty
        self.allyCapturedPosition = location
        self.allyCaptured = True
        location = (location % 8, 7 - (int(location / 8)))
        self.allyBoard[location[0]][location[1]] = 0
        # Handle distribution update in later methods
        return

    # Done
    def postCaptureUpdate(self, location):
        if not self.allyCaptured:
            return

        location = (location % 8, 7 - (int(location / 8)))

        # idk if we'll need this
        max_key = ""
        sum_dist = 0
        sum = 0

        for k, v in self.pieceDistri.items():
            prob = v[location[0]][location[1]]
            sum += prob

        if sum == 0:
            sum = 1

        for k, v in self.pieceDistri.items():
            prob_at_location = v[location[0]][location[1]]
            post_distri = prob_at_location / sum
            remaining_probability = 1 - post_distri
            if (1 - prob_at_location) == 0:
                v[location[0]][location[1]] = 1
                continue
            v *= (remaining_probability / (1 - prob_at_location))
            v[location[0]][location[1]] = post_distri

        return

    # Done
    def generateSensing(self):
        if self.allyCaptured:
            self.allyCaptured = False
            return self.allyCapturedPosition

        min_entropy = []

        for k,v in self.pieceDistri.items():
            if np.sum(v) == 0:
                continue
            entro_mat = np.asarray(v).reshape(-1)
            min_entropy.append((entropy(entro_mat), k))

        # Uniformity maximizes Entropy
        keyValue = max(min_entropy, key = lambda item:item[0])[1]
        matrix = self.pieceDistri[keyValue]
        ind = np.unravel_index(np.argmax(matrix, axis=None), matrix.shape)
        this_sense = chess.square(file_index = ind[1], rank_index = 7 - ind[0])
        if this_sense == self.lastSense:
            return None
        else:
            self.lastSense = this_sense
            return this_sense

    # Done
    def updateSensing(self, observation):
        self._current_observation = observation
        for idx, piece in observation:
            column = idx % 8
            row = 7 - (int(idx / 8))

            if not piece is None:
                result_piece = piece.symbol()
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
                v = self.pieceDistri['p' + str(column + 1)]
                v.fill(0)
                v[row][column] = 1
            elif piece.piece_type == chess.BISHOP:
                if (row + column) % 2 == 0:
                    v = self.pieceDistri['b1']
                else:
                    v = self.pieceDistri['b2']
                v.fill(0)
                v[row][column] = 1
            elif piece.piece_type == chess.ROOK:
                if self.rook_count == 1:
                    v = self.pieceDistri['r1']
                    v.fill(0)
                    v[row][column] = 1
                else:
                    r1 = self.pieceDistri['r1']
                    r2 = self.pieceDistri['r2']

                    prob1 = r1[row][column]
                    prob2 = r2[row][column]
                    sum_rook = prob1 + prob2

                    if sum_rook == 0:
                        new_prob1 = 1
                        sum_rook = 1

                    new_prob1 = prob1 / sum_rook
                    new_prob2 = prob2 / sum_rook

                    if (1 - new_prob1) != 0:
                        r1 *= ((1 - prob1) / (1 - new_prob1))

                    if (1 - new_prob2) != 0:
                        r2 *= ((1 - prob2) / (1 - new_prob2))

            elif piece.piece_type == chess.KNIGHT:
                if self.knight_count == 1:
                    v = self.pieceDistri['n1']
                    v.fill(0)
                    v[row][column] = 1
                else:
                    n1 = self.pieceDistri['n1']
                    n2 = self.pieceDistri['n2']

                    prob1 = n1[row][column]
                    prob2 = n2[row][column]
                    sum_rook = prob1 + prob2

                    if sum_rook == 0:
                        new_prob1 = 1
                        sum_rook = 1

                    new_prob1 = prob1 / sum_rook
                    new_prob2 = prob2 / sum_rook

                    if (1 - new_prob1) != 0:
                        n1 *= ((1 - prob1) / (1 - new_prob1))

                    if (1 - new_prob2) != 0:
                        n2 *= ((1 - prob2) / (1 - new_prob2))

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
            if np.sum(v) == 0:
                continue
            v /= np.sum(v)
        
        return

    # Done
    def returnDistribution(self):
        return copy.deepcopy(self.pieceDistri)

    # Done
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
                print("See abnormal chess piece")

            self.pieceDistri[item] = updated_distribution

    # Call upon making a move
    def updateAllyBoard(self, move, captured_piece, captured_square):
        if (move is None):
            return 

        move_string = move.uci()
        (start, end) = self._move_string_to_idx(move_string)
        self.allyBoard[start[0]][start[1]] = 0
        self.allyBoard[end[0]][end[1]] = 1

        # If in this observation
        if captured_piece:
            self.survivingCount -= 1
            last_sense = [x for x, piece in self._current_observation]
            location = (captured_square % 8, 7 - int(captured_square / 8))
            if captured_square in last_sense:
                # welp, this is rare
                # Captured Square in last Sense
                # 100% Sure situation, somehow implement and test it
                ind = last_sense.index(captured_square)
                piece_type = self._current_observation[ind][1].symbol().lower()
                if piece_type == 'q':
                    self.pieceDistri['q'].fill(0)
                    self.mightBeAlive['q'] = 0
                elif piece_type == 'b':
                    if (location[0] + location[1]) % 2 == 0:
                        v = self.pieceDistri['b1']
                        self.mightBeAlive['b1'] = 0
                    else:
                        v = self.pieceDistri['b2']
                        self.mightBeAlive['b2'] = 0
                    v.fill(0)
                elif piece_type == 'p':
                    # This pawn has died
                    v = self.pieceDistri['p' + str(location[1] + 1)]
                    v.fill(0)
                elif piece_type == 'n':
                    self.knight_count -= 1
                    if self.knight_count != 0:
                        self.pieceDistri['n1'] += self.pieceDistri['n2']
                        self.pieceDistri['n1'] /= 2
                        self.pieceDistri['n2'].fill(0)
                        self.mightBeAlive['n2'] = 0
                    else:
                        self.pieceDistri['r1'].fill(0)
                        self.mightBeAlive['n1'] = 0
                elif piece_type == 'r':
                    # This is absolute
                    self.rook_count -= 1
                    if self.rook_count != 0:
                        self.pieceDistri['r1'] += self.pieceDistri['r2']
                        self.pieceDistri['r1'] /= 2
                        self.pieceDistri['r2'].fill(0)
                        self.mightBeAlive['r2'] = 0
                    else:
                        self.pieceDistri['r1'].fill(0)
                        self.mightBeAlive['r1'] = 0
                else:
                    # Probably gonna be king, but it's not gonna do anything now
                    # Cuz we won?
                    pass
            else:
                prob = [v[location[0]][location[1]] for k, v in self.pieceDistri.items()]

                indices = [i for i, v in enumerate(prob) if v > 0.8]
                # Very high probability
                # This should be absolute
                if len(indices) > 0:
                    piece_type = self.chessPiece[max(indices)]
                    # self.pieceDistri[piece_type].fill(0)
                    if piece_type[0] == 'p':
                        self.pieceDistri[piece_type].fill(0)
                    elif piece_type[0] == 'r':
                        self.rook_count -= 1
                        if self.rook_count == 0:
                            self.pieceDistri['r1'].fill(0)
                            self.mightBeAlive['r1'] = 0
                        else:
                            self.pieceDistri['r1'] += self.pieceDistri['r2']
                            self.pieceDistri['r1'] /= 2
                            self.pieceDistri['r2'].fill(0)
                            self.mightBeAlive['r2'] = 0
                        
                    elif piece_type == 'n':
                        self.knight_count -= 1
                        if self.knight_count == 0:
                            self.pieceDistri['n1'].fill(0)
                            self.mightBeAlive['n1'] = 0
                        else:
                            self.pieceDistri['n1'] += self.pieceDistri['n2']
                            self.pieceDistri['n1'] /= 2
                            self.pieceDistri['n2'].fill(0)
                            self.mightBeAlive['n2'] = 0

                    elif piece_type == 'q':
                        self.pieceDistri['q'].fill(0)
                        self.mightBeAlive['q'] = 0
                    elif piece_type == 'b':
                        # bishop
                        if (location[0] + location[1]) % 2 == 0:
                            v = self.pieceDistri['b1']
                            self.mightBeAlive['b1'] = 0
                        else:
                            v = self.pieceDistri['b2']
                            self.mightBeAlive['b2'] = 0
                        v.fill(0)
                    else:
                        pass
                else:
                    max_prob_value = max(prob)
                    if max_prob_value == 0:
                        piece_type = 'p4'
                    else:
                        idx = prob.index(max_prob_value)
                        piece_type = self.chessPiece[idx]
                    self.pieceDistri[piece_type].fill(0)

    # Done
    def _move_string_to_idx(self, uci_move_string):
        start = (7 - (int(uci_move_string[1]) - 1), ord(uci_move_string[0]) - 97)
        end = (7 - (int(uci_move_string[3]) - 1), ord(uci_move_string[2]) - 97)
        return (start, end)

    # Done
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

    # Done
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

        if np.sum(return_mat) == 0:
            return return_mat
        return return_mat / np.sum(return_mat)
    
    # Done
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

        if np.sum(return_mat) == 0:
            return return_mat
        return return_mat / np.sum(return_mat)

    # Done
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

    # Done
    def _knight_available_moves(self, location):
        candidate_location = []
        movement = [-2,-1,1,2]
        for x_movement in movement:
            for y_movement in movement:
                if abs(y_movement) == abs(x_movement):
                    continue
                
                candidate_location.append((location[0] + x_movement, location[1] + y_movement))

        return self._check_possibility(candidate_location)
    
    # Done
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
    
    # Done
    def _queen_available_moves(self, location):
        diag = self._biship_available_moves(location)
        grid = self._rook_available_moves(location)
        return grid + diag

    # Done
    def _king_available_moves(self, location):
        # First of all, king is very unlikely to move until danger close
        # IDK, danger close implement later ?

        candidate_locations = []
        for i in range(location[0] - 1, location[0] + 2):
            for k in range(location[1] - 1, location[0] + 2):
                candidate_locations.append((i,k))

        return self._check_possibility(candidate_locations)

    # Done
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

    # Done
    def biasFunction(self, location):
        return random.uniform(0.5,1)

    # Deprecated
    def boardBound(self, value):
        return min(max(value, 0), 7)

    # Done
    def testEnvironment(self):
        print(self.pieceDistri['q'])
        print(np.sum(self.pieceDistri['q']))

