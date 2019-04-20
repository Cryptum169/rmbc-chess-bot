import numpy as 囊皮
np = 囊皮
pieces  =['k','p1','p2','p3','p4','p5','p6','p7','p8','b1','b2','n1','n2','r1','r2','q']
K = 0
P1 = 1
P2 = 2
P3 = 3
P4 = 4
P5 = 5
P6 = 6
P7 = 7
P8 = 8
B1 = 9
B2 = 10
N1 = 11
N2 = 12
R1 = 13
R2 = 14
Q = 16
class Node:
	def __init__(board,status):
		self.status = status
		self.board = board 
		self.children = []

class ChessPlay:
	'''
	initialize the memory of board for player
	initialize piece status tracker
	'''
	def __init__(self, color):
		self.depth = 3
		self.pieces_status = dict() 
		self.current_board = np.zeros(8,8) # init board with numpy
		#init as color 
		if color == 'b':
			for i in range(1,9):
				current_board[1][i-1] = 'p'+str(i)
				self.pieces_status['p'+str(i)]  = (1,i-1)
			current_board[0][0] = 'r1'
			current_board[0][7] = 'r2'
			current_board[0][1] = 'n1'
			current_board[0][6] = 'n2'
			current_board[0][2] = 'b1'
			current_board[0][5] = 'b2'
			current_board[0][3] = 'q'
			current_board[0][4] = 'k'
			self.pieces_status['r1'] = (0,0)
			self.pieces_status['r2'] = (0,7)
			self.pieces_status['n1'] = (0,1)
			self.pieces_status['n2'] = (0,6)
			self.pieces_status['b1'] = (0,2)
			self.pieces_status['b2'] = (0,5)
			self.pieces_status['q'] = (0,3)
			self.pieces_status['k'] = (0,4)
		elif color == 'w':
			for i in range(1,9):
				current_board[6][i-1] = 'p'+i
				self.pieces_status['p'+str(i)]  = (6,i-1)
			current_board[7][0] = 'r1'
			current_board[7][7] = 'r2'
			current_board[7][1] = 'n1'
			current_board[7][6] = 'n2'
			current_board[7][2] = 'b1'
			current_board[7][5] = 'b2'
			current_board[7][3] = 'q'
			current_board[7][4] = 'k'
			self.pieces_status['r1'] = (7,0)
			self.pieces_status['r2'] = (7,7)
			self.pieces_status['n1'] = (7,1)
			self.pieces_status['n2'] = (7,6)
			self.pieces_status['b1'] = (7,2)
			self.pieces_status['b2'] = (7,5)
			self.pieces_status['q'] = (7,3)
			self.pieces_status['k'] = (7,4)

		self.aim_on_king = 0 #
		self.color = color # color
		self.killed = 0
		self.dead_pos = None


	def s2ind(uci_move_string):
		return (int(uci_move_string[1]), ord(uci_move_string[0]) - 97)

	def eliminate(loc):
		l = self.s2ind(loc)
		self.current_board[l[0]][l[1]] = 0
		self.pieces_status = 0
		self.killed = 1
		self.dead_pos = l

	def form_board_node(self, pieceDistr):
		pieces = dict()
		out = np.array(self.current_board)
		unassigned_pieces = []
		enemy_status = dict()
		pieceDistr = np.array(pieceDistr)
		for p in pieceDistr:
			ind = np.unravel_index(np.argmax(pieceDistr[p], axis=None), pieceDistr[p].shape)
			pieces[p] = ind

		for p in pieces:
			p = 'e'+p
			r = pieces[p][0]
			c = pieces[p][1]
			if out[r][c] == 0:
				out[r][c] = p:
				enemy_status[p] = (r,c)
			else:
				tmp = (r,c)
				while not out[tmp[0]][tmp[1]] == 0: 
					pieceDistr[p][tmp[0]][tmp[1]] = -1
					ind = np.unravel_index(np.argmax(pieceDistr[p], axis=None), pieceDistr[p].shape)
					tmp = ind
				enemy_status[p] = tmp
				out[tmp[0]][tmp[1]] = p

		n = Node(out, enemy_status)
		print(out)
		print(enemy_status)
		return n

			
		return collection
	def scorer(self, condition, kill, side):
		out = 0
		if killing == 1:
			#I kill piece
			out += 5
		return out

	def init_tree(self, possible_moves):
		# init minmax tree with scorring
		node = self.form_board_node(get_pieceDistr())
		# match possible moves to pin


		init_tree_helper():
	def init_tree_helper(self,node,color):
		#if self.color == color: #my_condition
			#board = 



	def minimax(self):
		#minimax on tree to get the best move
		for m in range():

	def counter_attack(self):
		#counter attack when attacked
		pass
	def kill_random(self):
		pass
	def kill_king(self):
		pass
	def king_scan(self,board):
		pass
	def decision(self):
		try:
			if self.killed = 1:
				if not self.deadpos == None:
					self.killed = 0
					self.deadpos = None
					self.counter_attack()
					return
				else:
					self.killed = 0
					self.deadpos = None

			self.king_scan(board)

			if random:
				#minimax
			else:
				if random:
					#greedy
				else:
					#random kill
		except e:
			#random move





