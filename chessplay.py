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
	def __init__(board):

		self.status = board 
		self.children = []

class ChessPlay:
	def __init__(self, color):
		self.depth = 3
		self.pieces_status = np.array([1 for _ in range(16)]) # 1 is alive. 0 is dead
		self.current_board = numpy # init board with numpy
		self.aim_on_king = 0 #
		self.color = color # color
		self.killed = 1
		self.dead_pos = 1
	def form_board_node(self, pieceDistr, table_produced = 1):
		pieces = dict()
		out = np.zeros(8,8)
		unassigned_pieces = []
		for p in pieceDistr:
			ind = np.unravel_index(np.argmax(a, axis=None), a.shape)
			pieces[p] = ind

		for p in pieces:
			r = pieces[p][0]
			c = pieces[p][1]
			out[r][c] = p
				
		return collection
	def scorer(self, condition, kill, side):
		out = 0
		if killing == 1:
			#I kill piece
			out += 5
		return out

	def init_tree(self, board):
		# init minmax tree with scorring
		node = self.form_board_node(get_pieceDistr())
		init_tree_helper():
	def init_tree_helper(self,node,color):
		if self.color == color: #my_condition
			board = 
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





