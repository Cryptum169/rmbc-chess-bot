import numpy as np
import random
import traceback
from movement import *
import time
pieces  =['k','p1','p2','p3','p4','p5','p6','p7','p8','b1','b2','n1','n2','r1','r2','q']
pound = ['p' + str(i) for i in range(1,9)]
epound = ['ep' + str(i) for i in range(1,9)]
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
	def __init__(self,board):
		#self.status = status
		#self.board = board 
		self.color = None
		self.score = 0
		self.children = []

class ChessPlay:
	'''
	initialize the memory of board for player
	initialize piece status tracker
	'''
	def __init__(self, color):
		self.time_check = 0
		self.onConflict = False
		self.depth = 3
		self.pieces_status = dict() 
		self.current_board = np.zeros((8,8), dtype= object) # init board with numpy
		#init as color 
		print('color', color )
		if color == 'b':
			for i in range(1,9):
				self.current_board[1][i-1] = 'p'+str(i)
				self.pieces_status['p'+str(i)]  = (1,i-1)
			self.current_board[0][0] = 'r1'
			self.current_board[0][7] = 'r2'
			self.current_board[0][1] = 'n1'
			self.current_board[0][6] = 'n2'
			self.current_board[0][2] = 'b1'
			self.current_board[0][5] = 'b2'
			self.current_board[0][3] = 'q'
			self.current_board[0][4] = 'k'
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
				self.current_board[6][i-1] = 'p'+str(i)
				self.pieces_status['p'+str(i)]  = (6,i-1)
			self.current_board[7][0] = 'r1'
			self.current_board[7][7] = 'r2'
			self.current_board[7][1] = 'n1'
			self.current_board[7][6] = 'n2'
			self.current_board[7][2] = 'b1'
			self.current_board[7][5] = 'b2'
			self.current_board[7][3] = 'q'
			self.current_board[7][4] = 'k'
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
		self.deadpos = None


	def s2ind(self,uci_move_string):
		out = (7-int(str(uci_move_string)[1])+1, ord(str(uci_move_string)[0]) - 97)
		#print(str(uci_move_string), '->', out)
		return out
	def s2ind_end(self, uci_move_string):
		out = (7-int(str(uci_move_string)[3])+1, ord(str(uci_move_string)[2]) - 97)
		#print(str(uci_move_string), '->', out)
		return out
	def eliminate(self, loc):
		try:
			#print('location change', loc)
			l = np.unravel_index(int(str(loc)), self.current_board.shape)
			#l = self.s2ind(loc)
			self.pieces_status[self.current_board[l[0]][l[1]]] = 0
			self.current_board[l[0]][l[1]] = 0
			self.killed = 1
			self.dead_pos = l
		except :
			traceback.print_exc()
			self.onConflict = 1
			#exit()
	def update(self, move):
		try:
			if move == None:
				return 
			src=self.s2ind(move)
			to= self.s2ind_end(move)
			self.current_board[to[0]][to[1]] = self.current_board[src[0]][src[1]]
			self.current_board[src[0]][src[1]] = 0
			self.pieces_status[self.current_board[to[0]][to[1]]] = (to[0],to[1])
			#promotion
			if (self.color == 'b' and self.pieces_status[self.current_board[to[0]][to[1]]][0] == 7) or (self.color == 'w' and self.pieces_status[self.current_board[to[0]][to[1]]][0] == 0):
				p = self.current_board[to[0]][to[1]]
				del self.pieces_status[p]
				self.current_board[to[0]][to[1]] = 'q'+ p
				self.pieces_status[self.current_board[to[0]][to[1]]] = to
		except :
			traceback.print_exc()
			self.onConflict = 1
			#exit()

	def form_board_node(self, pieceDistr):

		pieces = dict()
		out = np.array(self.current_board)
		#print(out)
		#print(self.pieces_status)
		unassigned_pieces = []
		enemy_status = dict()
		pieceDistr = pieceDistr
		for p in pieceDistr:
			ind = np.unravel_index(np.argmax(pieceDistr[p], axis=None), pieceDistr[p].shape)
			if pieceDistr[p][ind[0]][ind[1]] >0:
				pieces[p] = ind

		for p in pieces:
			
			r = pieces[p][0]
			c = pieces[p][1]
			if out[r][c] == 0:
				p = 'e'+p
				out[r][c] = p
				enemy_status[p] = (r,c)
			else:
				tmp = (r,c)
				while not out[tmp[0]][tmp[1]] == 0: 
					pieceDistr[p][tmp[0]][tmp[1]] = -1
					ind = np.unravel_index(np.argmax(pieceDistr[p], axis=None), pieceDistr[p].shape)
					tmp = ind
				p = 'e'+p
				enemy_status[p] = tmp
				out[tmp[0]][tmp[1]] = p

		#n = Node(out, enemy_status)
		#print(out)
		#print(enemy_status)
		return out, enemy_status
	'''
	def scorer(self, board, my_status, enemy_status, kill, negation):
		if negation: #enemy
			out = random.randint(1,3)
			if killing == 1:
				#I kill piece
				out -= 15
		else:
			out = random.randint(1,3)
			if killing == 1:
				#I kill piece
				out -= 15

		if negation:
			out = 0 -out
		return out
	'''
	def init_tree(self, possible_moves,pd,tlimit = 20):
		# init minmax tree with scorring
		self.time_check = time.time()
		self.time_limit = tlimit
		board, enemy_status = self.form_board_node(pd)
		my_status = dict(self.pieces_status)
		# match possible moves to pin
		nxt_color = 'w' if self.color == 'b' else 'b'
		node = Node(self.color)
		mx = None
		#s=self.scorer(board, my_status, enemy_status, False)
		#node.score = s
		for move in possible_moves:
			loc_start = self.s2ind(move)
			loc_end = self.s2ind_end(move)
			kill = False
			killed = None
			if not board[loc_start[0]][loc_start[1]] == 0:
				if board[loc_start[0]][loc_start[1]][0] == 'e':
					continue
				#print("valid start")
				#--begin work on updating board
				if not board[loc_end[0]][loc_end[1]] == 0 and board[loc_end[0]][loc_end[1]][0] == 'e':
					kill = True
					enemy_status[board[loc_end[0]][loc_end[1]]] = 0
					#print("凉了1")
				elif not board[loc_end[0]][loc_end[1]] == 0:
					#print("凉了2")
					continue
				elif board[loc_start[0]][loc_start[1]] in pound and not loc_start[1] == loc_end[1]: #pawn incline
					#print("凉了3")
					continue

				board[loc_end[0]][loc_end[1]] = board[loc_start[0]][loc_start[1]]
				board[loc_start[0]][loc_start[1]] = 0
				my_status[board[loc_end[0]][loc_end[1]]] =loc_end 
				promotion = False
				if board[loc_end[0]][loc_end[1]] in pound:
					if (self.color == 'b' and my_status[board[loc_end[0]][loc_end[1]]][0] == 7) or (self.color == 'w' and my_status[board[loc_end[0]][loc_end[1]]][0] == 0):
						promotion = True
						p = board[loc_end[0]][loc_end[1]]
						del my_status[p]
						board[loc_end[0]][loc_end[1]] = 'q'+ p
						my_status[board[loc_end[0]][loc_end[1]]] = loc_end

				nxt_node = self.init_tree_helper(nxt_color, board, my_status, enemy_status,3, kill)
				if not nxt_node == None:
					node.children.append(nxt_node)
				if promotion:
					p = board[loc_end[0]][loc_end[1]]
					if p == 0:
						break
					board[loc_end[0]][loc_end[1]] = p[1:]
					my_status[p[1:]] = my_status[p]
					del my_status[p]
				p = board[loc_end[0]][loc_end[1]]
				my_status[p] = loc_start
				board[loc_start[0]][loc_start[1]] = p
				board[loc_end[0]][loc_end[1]] = 0
				if not killed == None:
					board[loc_end[0]][loc_end[1]] = killed 
					enemy_status[killed] = loc_end
				#print("============recovered===============")
				#print(board)
				#print("===================================")
				#recover

				#check max
				if not nxt_node == None and (mx == None or nxt_node.score > mx):
					out_action = (loc_start, loc_end)
					mx = nxt_node.score
		#collect children score for minimax
		node.score = mx
		return node, out_action
	def scorer(self, board, my_status, enemy_status, current_color):
		#check king 
		#print(enemy_status)
		if not 'ek' in enemy_status:
			return 2
		if  enemy_status['ek'] == 0 and my_status['k'] == 0 :
			return 5000
		if my_status['k'] == 0:
			return -9999
		if enemy_status['ek'] == 0:
			return 9999
		out = 0
		my_survive = 0
		enemy_survive = 0
		for x in my_status:
			if not my_status[x] == 0:
				my_survive+=1
		for x in enemy_status:
			if not enemy_status[x] == 0:
				enemy_survive+=1
		if my_survive > enemy_survive:
			out = 3
		elif my_survive < enemy_survive:
			out = -2
		else:
			out = 1

		interactive = 0
		'''
		for i in range(2,6):
			for j in range(2,6):
				if not board[i][j] == 0 and board[i][j][0] == 'e':
					interactive -= 1
				else: 
					interactive += 1
		'''

		e_dest = []
		m_dest = []
		for e in my_status:
			if my_status[e] == 0:
				continue
			if e ==0:
				continue
			
			loc_start = my_status[e]
			dest = []
			if e == 'q' or e[0:2] == 'qp':
				dest = possible_queen_move(board, loc_start)
			elif e in ['n1', 'n2']:
				dest = possible_knight_move(board, loc_start)
			elif e in ['r1', 'r2']:
				dest = possible_rook_move(board, loc_start)
			elif e in ['b1', 'b2']:
				dest = possible_bishop_move(board, loc_start)
			elif e in ['k']:
				dest = possible_king_move(board, loc_start)
			elif e in pound:
				dest = possible_pawn_move(board, loc_start, current_color)
			else:
				continue 
			m_dest += dest
		for e in enemy_status:
			if enemy_status[e] == 0:
				continue
			
			loc_start = enemy_status[e]
			dest = []

			if e == 'eq' or e[0:3] == 'eqp':
				dest = possible_queen_move(board, loc_start)
			elif e in ['en1', 'en2']:
				dest = possible_knight_move(board, loc_start)
			elif e in ['er1', 'er2']:
				dest = possible_rook_move(board, loc_start)
			elif e in ['eb1', 'eb2']:
				dest = possible_bishop_move(board, loc_start)
			elif e in ['ek']:
				dest = possible_king_move(board, loc_start)
			elif e in epound:
				dest = possible_pawn_move(board, loc_start, current_color)
			else:
				continue 
			e_dest += dest
		e_set =set(e_dest)
		m_set =set(m_dest)
		if current_color == self.color:
			interactive = len(m_dest)/len(m_set)- len(e_dest)/len(e_set)
		else:
			interactive = 0 - len(m_dest)/len(m_set) + len(e_dest)/len(e_set)
		return out+interactive

		#check lost pieces
		return out
	def init_tree_helper(self, current_color, board, my_status, enemy_status, depth, kill):
		node = Node(current_color)
		mn = None
		mx = None
		if not self.color == current_color: # need neggation
			#node.score =scorer(board, my_status, enemy_status, True, kill)
			#print("============expanded===============")
			#print(board)
			#print("===================================")
			if depth <= 0 or (time.time()-self.time_check) > self.time_limit:
				s = self.scorer(board, my_status, enemy_status,current_color)
				node.score = s
				return node

			for e in list(enemy_status):
				if not e in enemy_status or enemy_status[e] == 0:
					continue
				
				loc_start = enemy_status[e]
				dest = []

				if e == 'eq' or e[0:3] == 'eqp':
					dest = possible_queen_move(board, loc_start)
					random.shuffle(dest)
					if len(dest)> 10:
						dest = [dest[i] for i in range(0,10)]
				elif e in ['en1', 'en2']:
					dest = possible_knight_move(board, loc_start)
					random.shuffle(dest)
					if len(dest)> 6:
						dest = [dest[i] for i in range(0,6)]
				elif e in ['er1', 'er2']:
					dest = possible_rook_move(board, loc_start)
					random.shuffle(dest)
					if len(dest)> 6:
						dest = [dest[i] for i in range(0,6)]
				elif e in ['eb1', 'eb2']:
					dest = possible_bishop_move(board, loc_start)
					random.shuffle(dest)
					if len(dest)> 4:
						dest = [dest[i] for i in range(0,4)]
				elif e in ['ek']:
					dest = possible_king_move(board, loc_start)
				elif e in epound:
					dest = possible_pawn_move(board, loc_start, current_color)
					if random.randint(1,10) < 7:
						dest = []
				else:
					continue 
				#print('dest ', e, ' ', dest)

				for loc_end in dest:
					kill = False
					killed = None
					if not board[loc_end[0]][loc_end[1]] == 0 and not board[loc_end[0]][loc_end[1]][0] == 'e':
						kill = True
						my_status[board[loc_end[0]][loc_end[1]]] = 0
						killed = board[loc_end[0]][loc_end[1]]
					elif not board[loc_end[0]][loc_end[1]] == 0:
						#print("凉了2")
						continue
					elif board[loc_start[0]][loc_start[1]] in pound and not loc_start[1] == loc_end[1]: #pawn incline
						#print("凉了3")
						continue

					board[loc_end[0]][loc_end[1]] = board[loc_start[0]][loc_start[1]]
					board[loc_start[0]][loc_start[1]] = 0
					enemy_status[board[loc_end[0]][loc_end[1]]] =loc_end 
					nxt_color = self.color
					promotion = False
					if board[loc_end[0]][loc_end[1]] in epound:
						if (current_color == 'b' and enemy_status[board[loc_end[0]][loc_end[1]]][0] == 7) or (current_color == 'w' and enemy_status[board[loc_end[0]][loc_end[1]]][0] == 0):
							promotion = True
							p = board[loc_end[0]][loc_end[1]]
							del enemy_status[p]
							board[loc_end[0]][loc_end[1]] = 'eq'+ p
							enemy_status[board[loc_end[0]][loc_end[1]]] = loc_end	

					nxt_node = self.init_tree_helper(nxt_color, board, my_status, enemy_status, depth-1, kill)
					#recover
					if not nxt_node == None:
						node.children.append(nxt_node)
					if promotion:
						p = board[loc_end[0]][loc_end[1]]
						print('recover promotion',p)
						board[loc_end[0]][loc_end[1]] = p[2:]
						enemy_status[p[1:]] = enemy_status[p]
						del enemy_status[p]
					p = board[loc_end[0]][loc_end[1]]
					enemy_status[p] = loc_start
					board[loc_start[0]][loc_start[1]] = p
					board[loc_end[0]][loc_end[1]] = 0
					if not killed == None:
						board[loc_end[0]][loc_end[1]] = killed 
						my_status[killed] = loc_end
					#print("============recovered===============")
					#print(board)
					#print("===================================")
					if not nxt_node == None and (mn == None or nxt_node.score < mn):
						mn = nxt_node.score				
			node.score = mn
			return node
		else:
			#print("============expanded===============")
			#print(board)
			#print("===================================")
			if depth <= 0 or (time.time()-self.time_check) > self.time_limit:
				s = self.scorer(board, my_status, enemy_status, current_color)
				node.score = s
				return node

			for e in list(my_status):
				if my_status[e] == 0:
					continue
				
				loc_start = my_status[e]
				dest = []
				#print(my_status)
				if e == 'q' or e[0:2] == 'qp':
					dest = possible_queen_move(board, loc_start)
					random.shuffle(dest)
					if len(dest)> 10:
						dest = [dest[i] for i in range(0,7)]
				elif e in ['n1', 'n2']:
					dest = possible_knight_move(board, loc_start)
					random.shuffle(dest)
					if len(dest)> 6:
						dest = [dest[i] for i in range(0,3)]
				elif e in ['r1', 'r2']:
					dest = possible_rook_move(board, loc_start)
					random.shuffle(dest)
					if len(dest)> 6:
						dest = [dest[i] for i in range(0,3)]
				elif e in ['b1', 'b2']:
					dest = possible_bishop_move(board, loc_start)
					random.shuffle(dest)
					if len(dest)> 4:
						dest = [dest[i] for i in range(0,3)]
				elif e in ['k']:
					dest = possible_king_move(board, loc_start)
				elif e in pound:
					dest = possible_pawn_move(board, loc_start, current_color)
					if random.randint(1,10) < 7:
						dest = []
				else:
					continue 


				for loc_end in dest:
					kill = False
					killed = None
					if not board[loc_end[0]][loc_end[1]] == 0 and board[loc_end[0]][loc_end[1]][0] == 'e':
						kill = True
						enemy_status[board[loc_end[0]][loc_end[1]]] = 0
						killed = board[loc_end[0]][loc_end[1]]
					elif not board[loc_end[0]][loc_end[1]] == 0:
						#print("凉了2")
						continue
					elif board[loc_start[0]][loc_start[1]] in pound and not loc_start[1] == loc_end[1]: #pawn incline
						#print("凉了3")
						continue
					original = (loc_start,board[loc_start[0]][loc_start[1]])
					board[loc_end[0]][loc_end[1]] = board[loc_start[0]][loc_start[1]]
					board[loc_start[0]][loc_start[1]] = 0
					'''
					if(board[loc_end[0]][loc_end[1]]==0):

						print(my_status)
						print(board)
						print(dest)
						print(e)
						print('loc_start->',loc_start)
						print('loc_end->',loc_end)
						print('issue')
						exit()
					'''
					my_status[board[loc_end[0]][loc_end[1]]] =loc_end 
					#print(loc_end,'my_s write', my_status[board[loc_end[0]][loc_end[1]]])
					promotion = False
					if board[loc_end[0]][loc_end[1]] in pound:
						if (self.color == 'b' and my_status[board[loc_end[0]][loc_end[1]]][0] == 7) or (self.color == 'w' and my_status[board[loc_end[0]][loc_end[1]]][0] == 0):
							promotion = True
							p = board[loc_end[0]][loc_end[1]]
							del my_status[p]
							board[loc_end[0]][loc_end[1]] = 'q'+ p
							#print('qp->',board[loc_end[0]][loc_end[1]] )
							my_status[board[loc_end[0]][loc_end[1]]] = loc_end
					nxt_color = 'w' if not current_color == 'w' else 'b'
					nxt_node = self.init_tree_helper(nxt_color, board, my_status, enemy_status, depth-1, kill)
					if not nxt_node == None:
						node.children.append(nxt_node)
					if promotion:
						p = board[loc_end[0]][loc_end[1]]
						board[loc_end[0]][loc_end[1]] = p[1:]
						my_status[p[1:]] = my_status[p]
						del my_status[p]
					p = board[loc_end[0]][loc_end[1]]
					'''
					if(board[loc_end[0]][loc_end[1]]==0):
						print('dp',depth)
						print('original',original)
						print(my_status)
						print('loc_start',loc_start)
						print('loc_end',loc_end)
						print(board)
						print('aha')
						exit()
					'''
					my_status[p] = loc_start
					board[loc_start[0]][loc_start[1]] = p
					board[loc_end[0]][loc_end[1]] = 0
					if not killed == None:
						board[loc_end[0]][loc_end[1]] = killed 
						enemy_status[killed] = loc_end
					#print("============recovered===============")
					#print(board)
					#print("===================================")
					#recover

					#check max
					if not nxt_node == None and (mx == None or nxt_node.score > mx):
						out_action = (loc_start, loc_end)
						mx = nxt_node.score
			#collect children score for minimax
			node.score = mx
			return node
		return node
	
	def scan_attacker(self, pos):
		board = np.array(self.current_board)
		board[pos[0]][pos[1]] = 'e'

		for e in ['p'+str(i) for i in range(1,9)] + ['n1', 'n2', 'b1', 'b2', 'r1', 'r2','q', 'k']:
			dest = []
			if not e in self.pieces_status:
				continue
			if e == 'q' or e[0:2] == 'qp':
					dest = possible_queen_move(board, loc_start)
			elif e in ['n1', 'n2']:
				dest = possible_knight_move(board, loc_start)
			elif e in ['r1', 'r2']:
				dest = possible_rook_move(board, loc_start)
			elif e in ['b1', 'b2']:
				dest = possible_bishop_move(board, loc_start)
			elif e in ['k']:
				dest = possible_king_move(board, loc_start)
			elif e in pound:
				dest = possible_pawn_move(board, loc_start, current_color)
			else:
				continue
			if pos in dest:
				return (self.pieces_status[e], pos) 

		return None
	
	def counter_attack(self):
		print('counter_attack')
		self.scan_attacker(self.deadpos)

	def decision_make(self, possible_moves,pd):
		action = None
		try:
			#if scan king
			#with some chance  attack scanned box
			if self.killed == 1:
				if not self.deadpos == None:
					action = self.counter_attack()
					self.killed = 0
					self.deadpos = None
					return action
				else:
					self.killed = 0
					self.deadpos = None
			#self.king_scan(board)
			
			
			_, action =self.init_tree(possible_moves, pd)
			#print("==========","下一步走", action[0], '->', action[1],"=======")
					
		except :
			#random move
			traceback.print_exc()
			self.onConflict = True
			#exit()
			return None
			
		return action





