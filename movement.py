import numpy as np
pound = ['p' + str(i) for i in range(1,9)]
epound = ['ep' + str(i) for i in range(1,9)]

def possible_pawn_move(board, pos, side):
	out = []
	if board[pos] in pound:
		pos_r = pos[0]
		pos_c = pos[1]
		if side == 'b':
			pos_r += 1

			if 0<= pos_r<=7 and board[pos_r][pos_c] == 0:
				out.append((pos_r, pos_c))
			if pos[0] == 1:
				pos_r += 1
				if 0<= pos_r<=7 and board[pos_r][pos_c] == 0:
					out.append((pos_r, pos_c))
			#kill
			for delta in [1,-1]:
				pos_r = pos[0]
				pos_c = pos[1]
				pos_r += 1
				pos_c += delta
				if 0<= pos_r<=7 and 0<= pos_c<=7 and board[pos_r][pos_c] in epound:
					out.append((pos_r, pos_c))
			
		elif side == 'w':
			pos_r -= 1

			if 0<= pos_r<=7 and board[pos_r][pos_c] == 0:
				out.append((pos_r, pos_c))
			if pos[0] == 6:
				pos_r -= 1
				if 0<= pos_r<=7 and board[pos_r][pos_c] == 0:
					out.append((pos_r, pos_c))
			#kill
			for delta in [1,-1]:
				pos_r = pos[0]
				pos_c = pos[1]
				pos_r -= 1
				pos_c += delta
				if 0<= pos_r<=7 and 0<= pos_c<=7 and board[pos_r][pos_c] in epound:
					out.append((pos_r, pos_c))

	elif board[pos] in epound:
		pos_r = pos[0]
		pos_c = pos[1]
		if side == 'b':
			pos_r += 1

			if 0<= pos_r<=7 and board[pos_r][pos_c] == 0:
				out.append((pos_r, pos_c))
			if pos[0] == 1:
				pos_r += 1
				if 0<= pos_r<=7 and 0<= pos_c<=7 and board[pos_r][pos_c] == 0:
					out.append((pos_r, pos_c))
			#kill
			for delta in [1,-1]:
				pos_r = pos[0]
				pos_c = pos[1]
				pos_r += 1
				pos_c += delta
				if 0<= pos_r<=7 and 0<= pos_c<=7 and board[pos_r][pos_c] in pound:
					out.append((pos_r, pos_c))
			
		elif side == 'w':
			pos_r -= 1

			if 0<= pos_r<=7 and board[pos_r][pos_c] == 0:
				out.append((pos_r, pos_c))
			if pos[0] == 6:
				pos_r -= 1
				if 0<= pos_r<=7 and 0<= pos_c<=7 and board[pos_r][pos_c] == 0:
					out.append((pos_r, pos_c))
			#kill
			for delta in [1,-1]:
				pos_r = pos[0]
				pos_c = pos[1]
				pos_r -= 1
				pos_c += delta
				if 0<= pos_r<=7 and 0<= pos_c<=7 and board[pos_r][pos_c] in pound:
					out.append((pos_r, pos_c))
	return out
		
def possible_king_move(board, pos):
	out = [] 
	if board[pos[0]][pos[1]] == 'k':
		for delta in [(0,1),(1,1),(1,0),(-1,1),(1,-1),(-1,-1),(0,-1),(-1,0)]:
			pos_r = pos[0]+delta[0]
			pos_c = pos[1]+delta[1]
			if 0<= pos_r <=7 and 0<= pos_c <=7 and (board[pos_r][pos_c] == 0 or board[pos_r][pos_c][0] =='e'):
				out.append((pos_r, pos_c))
	elif board[pos[0]][pos[1]] == 'ek':
		for delta in [(0,1),(1,1),(1,0),(-1,1),(1,-1),(-1,-1),(0,-1),(-1,0)]:
			pos_r = pos[0]+delta[0]
			pos_c = pos[1]+delta[1]
			if 0<= pos_r <=7 and 0<= pos_c <=7 and (board[pos_r][pos_c] == 0 or not board[pos_r][pos_c][0] =='e'):
				out.append((pos_r, pos_c))
	return out 
def possible_knight_move(board, pos):
	out = [] 
	if board[pos[0]][pos[1]] in ['n1','n2']:
		for delta in [(2,1),(1,2),(2,-1),(-1,2),(-2,1),(-2,-1),(1,-2),(-1,-2)]:
			pos_r = pos[0]
			pos_c = pos[1]
			pos_r += dr
			pos_c += dc
			if 0<= pos_r <=7 and 0<= pos_c <=7 and (board[pos_r][pos_c] == 0 or board[pos_r][pos_c][0] =='e'):
				out.append((pos_r, pos_c))
	elif board[pos[0]][pos[1]] in ['en1','en2']:
		for dr, dc in [(2,1),(1,2),(2,-1),(-1,2),(-2,1),(-2,-1),(1,-2),(-1,-2)]:
			pos_r = pos[0]
			pos_c = pos[1]
			pos_r += dr
			pos_c += dc
			if 0<= pos_r <=7 and 0<= pos_c <=7 and (board[pos_r][pos_c] == 0 or not board[pos_r][pos_c][0] =='e'):
				out.append((pos_r, pos_c))
	return out
def possible_bishop_move(board, pos):
	out = [] 
	if board[pos[0]][pos[1]] in ['b1','b2']:
		for dr,dc in [(1,1),(-1,-1),(-1,1),(1,-1)]:
			pos_r = pos[0]
			pos_c = pos[1]
			pos_r += dr
			pos_c += dc
			while 0<=pos_r<=7 and 0<=pos_c<=7:
				if board[pos_r][pos_c] == 0:
					out.append((pos_r,pos_c))
				elif board[pos_r][pos_c][0] == 'e':
					out.append((pos_r,pos_c))
					break
				else:
					break
				pos_r += dr
				pos_c += dc

	elif board[pos[0]][pos[1]] in ['eb1', 'eb2']:
		for dr,dc in [(1,1),(-1,-1),(-1,1),(1,-1)]:
			pos_r = pos[0]
			pos_c = pos[1]
			pos_r += dr
			pos_c += dc
			while 0<=pos_r<=7 and 0<=pos_c<=7:
				if board[pos_r][pos_c] == 0:
					out.append((pos_r,pos_c))
				elif not board[pos_r][pos_c][0] == 'e':
					out.append((pos_r,pos_c))
					break
				else:
					break
				pos_r += dr
				pos_c += dc
	return out 	
def possible_rook_move(board, pos):
	out = [] 
	if board[pos[0]][pos[1]] in ['r1','r2']:
		for dr,dc in [(0,1),(-1,0),(0,-1),(1,0)]:
			pos_r = pos[0]
			pos_c = pos[1]
			pos_r += dr
			pos_c += dc
			while 0<=pos_r<=7 and 0<=pos_c<=7:
				if board[pos_r][pos_c] == 0:
					out.append((pos_r,pos_c))
				elif board[pos_r][pos_c][0] == 'e':
					out.append((pos_r,pos_c))
					break
				else:
					break
				pos_r += dr
				pos_c += dc

	elif board[pos[0]][pos[1]] in ['er1', 'er2']:
		for dr,dc in [(0,1),(-1,0),(0,-1),(1,0)]:
			pos_r = pos[0]
			pos_c = pos[1]
			pos_r += dr
			pos_c += dc
			while 0<=pos_r<=7 and 0<=pos_c<=7:
				if board[pos_r][pos_c] == 0:
					out.append((pos_r,pos_c))
				elif not board[pos_r][pos_c][0] == 'e':
					out.append((pos_r,pos_c))
					break
				else:
					break
				pos_r += dr
				pos_c += dc
	return out		
def possible_queen_move(board, pos):
	out = []

	if board[pos[0]][pos[1]] == 'q' or board[pos[0]][pos[1]][0:2] == 'qp':
		pos_r = pos[0]
		pos_c = pos[1]
		pos_r +=1 
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r +=1 

		pos_r = pos[0]
		pos_c = pos[1]
		pos_c +=1 
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_c +=1 

		pos_r = pos[0]
		pos_c = pos[1]
		pos_r +=1 
		pos_c +=1 
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r +=1 
			pos_c +=1  

		pos_r = pos[0]
		pos_c = pos[1]
		pos_r -=1 
		pos_c -=1
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r -=1 
			pos_c -=1

		pos_r = pos[0]
		pos_c = pos[1]
		pos_r +=1 
		pos_c -=1
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r +=1 
			pos_c -=1

		pos_r = pos[0]
		pos_c = pos[1]
		pos_r -=1 
		pos_c +=1
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r -=1 
			pos_c +=1

		pos_r = pos[0]
		pos_c = pos[1]
		pos_c -=1 
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_c -=1 

		pos_r = pos[0]
		pos_c = pos[1]
		pos_r -=1 
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r -=1 
#=======================================================
	elif board[pos[0]][pos[1]] == 'eq' or board[pos[0]][pos[1]][0:3] == 'eqp':
		pos_r = pos[0]
		pos_c = pos[1]
		pos_r +=1 
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif not board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r +=1 

		pos_r = pos[0]
		pos_c = pos[1]
		pos_c +=1 
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif not board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_c +=1 

		pos_r = pos[0]
		pos_c = pos[1]
		pos_r +=1 
		pos_c +=1 
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif not board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r +=1 
			pos_c +=1  

		pos_r = pos[0]
		pos_c = pos[1]
		pos_r -=1 
		pos_c -=1
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif not board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r -=1 
			pos_c -=1

		pos_r = pos[0]
		pos_c = pos[1]
		pos_r +=1 
		pos_c -=1
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif not board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r +=1 
			pos_c -=1

		pos_r = pos[0]
		pos_c = pos[1]
		pos_r -=1 
		pos_c +=1
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif not board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r -=1 
			pos_c +=1

		pos_r = pos[0]
		pos_c = pos[1]
		pos_c -=1 
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif not board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_c -=1 

		pos_r = pos[0]
		pos_c = pos[1]
		pos_r -=1 
		while 0<=pos_r<=7 and 0<=pos_c<=7:
			if board[pos_r][pos_c] == 0:
				out.append((pos_r,pos_c))
			elif not board[pos_r][pos_c][0] == 'e':
				out.append((pos_r,pos_c))
				break
			else:
				break
			pos_r -=1 
	return out