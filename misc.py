'''
Copyright (C) 2018 Bo Wu  All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import random
from collections import OrderedDict

# Square indices
SQUARES = []
for i in range(8):
	SQUARES.extend(range(i * 16, i * 16 + 8))
[a1, b1, c1, d1, e1, f1, g1, h1,
 a2, b2, c2, d2, e2, f2, g2, h2,
 a3, b3, c3, d3, e3, f3, g3, h3,
 a4, b4, c4, d4, e4, f4, g4, h4,
 a5, b5, c5, d5, e5, f5, g5, h5,
 a6, b6, c6, d6, e6, f6, g6, h6,
 a7, b7, c7, d7, e7, f7, g7, h7,
 a8, b8, c8, d8, e8, f8, g8, h8] = SQUARES

#Piece stuff
UNICODE_PIECE_SYMBOLS = u'.♟♞♝♜♛♚♔♕♖♗♘♙'
ASCII_PIECE_CHARS = '.PNBRQKkqrbnp'
[k, q, r, b, n, p, blank, P, N, B, R, Q, K] = range(-6,7)

# directions that pieces move in
DIRECTIONS = [None, None,
			  [33, 31, 18, 14, -14, -18, -31, -33],
			  [17, 15, -15, -17],
			  [16, 1, -1, -16],
			  [17, 16, 15, 1, -1, -15, -16, -17],
			  [17, 16, 15, 1, -1, -15, -16, -17]]
ISSLIDING = [None, None, False, True, True, True, False]

# Initialize Zobrist
ZOBRIST_KEYS = [None] * 0x80
for i in SQUARES:
	temp = [None]
	for piece in range(12):
		temp.append(random.getrandbits(64))
	ZOBRIST_KEYS[i] = temp
ZOBRIST_TURN = random.getrandbits(64)

# Simplify code for castling rights check
CASTLING_CHECK_SQ = [[e1, h1], [a1, e1], [e8, h8], [a8, e8]]

if '.' in __name__:
	from . import evaluation
else:
	import evaluation

class Snapshot():

	def __init__(self, state):
		self.zobrist = state.zobrist
		self.castling_rights = state.castling_rights.copy()
		self.majorpiecesleft = state.majorpiecesleft
		self.fullmove_number = state.fullmove_number
		self.midval = state.eval.midvalue
		self.endval = state.eval.endvalue

	def restore(self, state):
		state.zobrist = self.zobrist
		state.castling_rights = self.castling_rights
		state.majorpiecesleft = self.majorpiecesleft
		state.fullmove_number = self.fullmove_number
		state.eval.restore(self.midval, self.endval)


class State():

	def __str__(self):
		string = ''
		for i in range(7, -1, -1):
			for j in range(8):
				string += UNICODE_PIECE_SYMBOLS[self.board[i * 16 + j]]
			string += '\n'
		string += '\nvalue = %d\n\n' % self.eval.get_score()
		return string

	def fen(self):
		fen = ''
		for rank in range(7,-1,-1):
			blank = 0
			for piece in self.board[rank*16:rank*16+8]:
				if piece == 0:
					blank += 1
				else:
					if blank > 0:
						fen += str(blank)
						blank = 0
					fen += ASCII_PIECE_CHARS[piece]
			if blank > 0:
				fen += str(blank)
			if rank != 0: fen += '/'
		fen += ' w ' if self.turn == 1 else ' b '
		for i,j in enumerate(self.castling_rights):
			if j: fen += 'KQkq'[i]
		if fen[-1] == ' ': fen += '-'
		fen += ' - 0 '
		fen += str(self.fullmove_number)
		return fen


	def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
		blocks = fen.split()

		#Construct board
		ranks = blocks[0].split('/')
		ranks.reverse()
		board = []
		for i in range(8):
			for char in ranks[i]:
				try:
					board.extend([0] * int(char))
				except ValueError:
					board.append(eval(char))
			board.extend([None] * 8)
		self.board = board

		#Turn
		self.turn = 1 if blocks[1] == 'w' else -1

		#Castling rights
		self.castling_rights = []
		for castle in 'KQkq':
			self.castling_rights.append(True if castle in blocks[2] else False)

		#Fullmove number
		self.fullmove_number = int(blocks[5])

		#Iterate over the board to fill in remaining information
		self.zobrist = ZOBRIST_TURN if self.turn > 0 else 0
		self.majorpiecesleft = -2
		for i in SQUARES:
			if board[i] != 0:
				self.zobrist ^= ZOBRIST_KEYS[i][board[i]]
				if abs(board[i]) > 1: self.majorpiecesleft += 1

		#Initialize evaluation score
		self.eval = evaluation.Eval(self)

		#Dict for detecting threefold repetition, stores repetition count of current state
		self.repetition = {self.zobrist: 1}

	def generate_moves(self):

		# castling
		if self.turn > 0:  # white
			if self.castling_rights[0]:  # K
				if self.board[f1] == self.board[g1] == 0:
					yield Move(e1, g1, K, 0, 2)
			if self.castling_rights[1]:  # Q
				if self.board[b1] == self.board[c1] == self.board[d1] == 0:
					yield Move(e1, c1, K, 0, 2)
		else:  # black
			if self.castling_rights[2]:  # k
				if self.board[f8] == self.board[g8] == 0:
					yield Move(e8, g8, k, 0, 2)
			if self.castling_rights[3]:  # q
				if self.board[b8] == self.board[c8] == self.board[d8] == 0:
					yield Move(e8, c8, k, 0, 2)

		for i in SQUARES:
			piece = self.board[i]
			if piece * self.turn < 1: continue

			if abs(piece) == 1: #pawn moves
				# forward advances
				if self.board[i + 16*piece] == 0:
					yield Move(i, i + 16*piece, piece, 0)
					# two square advance
					if (i-piece*32) & 0x88 and self.board[i + 32*piece] == 0:
						yield Move(i, i + 32*piece, piece, 0)
				# diagonal captures
				target = self.board[i + 17*piece]
				if not i + 17*piece & 0x88 and target * self.turn < 0:
					yield Move(i, i + 17*piece, piece, self.board[i + 17*piece])
				target = self.board[i + 15*piece]
				if not i + 15*piece & 0x88 and target * self.turn < 0:
					yield Move(i, i + 15*piece, piece, self.board[i + 15*piece])

			elif ISSLIDING[abs(piece)]:
				for dest, capt in self.generate_sliding_moves(i, DIRECTIONS[abs(piece)]):
					yield Move(i, dest, piece, capt)
			else:
				for dest, capt in self.generate_nonslide_moves(i, DIRECTIONS[abs(piece)]):
					yield Move(i, dest, piece, capt)

	def make_move(self, move):
		snapshot = Snapshot(self)
		for piece, square in move.off:
			self.board[square] = 0
			self.zobrist ^= ZOBRIST_KEYS[square][piece]
		for piece, square in move.on:
			self.board[square] = piece
			self.zobrist ^= ZOBRIST_KEYS[square][piece]
		self.zobrist ^= ZOBRIST_TURN

		self.eval.update(move)
		if not self.turn: self.fullmove_number += 1
		if abs(move.captured) > 1: self.majorpiecesleft -= 1

		try:
			a = self.repetition[self.zobrist] + 1
		except KeyError:
			a = 1
		self.repetition[self.zobrist] = a

		for i in range(4):
			if self.castling_rights[i]:
				if move.from_sq in CASTLING_CHECK_SQ[i] or move.to_sq in CASTLING_CHECK_SQ[i]:
					self.castling_rights[i] = False

		self.turn *= -1

		return snapshot

	def unmake_move(self, move, snapshot):
		for piece, square in move.on:
			self.board[square] = 0
		for piece, square in move.off:
			self.board[square] = piece

		a = self.repetition[self.zobrist] - 1
		if a == 0:
			del self.repetition[self.zobrist]
		else:
			self.repetition[self.zobrist] = a

		self.turn *= -1

		snapshot.restore(self)

	def make_move_uci(self, uci):
		fsq, tsq = eval(uci[:2]), eval(uci[2:4])
		if len(uci) > 4:
			special = dict(zip('qrbn', [1, 4, 5, 6]))[uci[4]]
			self.make_move(Move(fsq, tsq, self.board[fsq], self.board[tsq], special))
		else:
			self.make_move(Move(fsq, tsq, self.board[fsq], self.board[tsq]))

	def leaf(self):
		try:
			if self.repetition[self.zobrist] == 3: return True
		except KeyError:
			return False
		return abs(self.eval.get_score()) > 40000

	def evaluate(self):
		if self.repetition[self.zobrist] == 3: return 0
		return self.eval.get_score()*self.turn

	def getPhase(self): # 0 = opening, 1 = endgame
		if self.majorpiecesleft > 11:
			return 0
		elif self.majorpiecesleft < 5:
			return 1
		else:	
			return -self.majorpiecesleft/8 + 1.5

	def generate_nonslide_moves(self, sq, moves):
		for i in moves:
			j = sq + i
			if not j & 0x88:
				target = self.board[j]
				if target * self.turn < 1:
					yield (j, target)

	def generate_sliding_moves(self, sq, directions):
		for i in directions:
			temp_sq = sq
			while True:
				temp_sq += i
				if temp_sq & 0x88:  # OOB
					break
				target = self.board[temp_sq]
				if target == 0:  # blank destination
					yield (temp_sq, 0)
				else:
					if target * self.turn < 0:  # if something can be captured
						yield (temp_sq, target)
					break



class Move():

	def __init__(self, from_sq, to_sq, piece, captured, special=0):
		self.from_sq = from_sq
		self.to_sq = to_sq
		self.piece = piece
		self.captured = captured
		self.special = special  # 1=promotion to Q, 2=castle, 3=en passant, 4-6=underpromotion to RBN (3-6 not done by the engine), 7=null move
		if special == 7:
			self.off = self.on = []
			return
		if abs(piece) == 1: # pawn special moves
			if (to_sq+piece*16) & 0x88: # pawn promotion
				self.special = 1
			elif captured == 0 and abs(from_sq - to_sq) % 16 != 0:  # en passant
				self.special = 3
		if abs(piece) == 6:#castling
			if abs(from_sq - to_sq) == 2: self.special = 2
		self.off, self.on = self.get_movements()

	def __str__(self):
		string = chr(self.from_sq % 16 + 97) + str(self.from_sq // 16 + 1) + chr(self.to_sq % 16 + 97) + str(self.to_sq // 16 + 1)
		if self.special == 1: string += 'q'
		return string

	def get_movements(self):
		off, on = [], []  # (Piece, sq)
		if self.special:
			if self.special == 1:
				off.append((self.piece, self.from_sq))
				on.append((Q*self.piece, self.to_sq))
			elif self.special == 2:
				off.append((self.piece, self.from_sq))
				on.append((self.piece, self.to_sq))
				if self.to_sq == g1:
					off.append((R, h1))
					on.append((R, f1))
				elif self.to_sq == c1:
					off.append((R, a1))
					on.append((R, d1))
				elif self.to_sq == g8:
					off.append((r, h8))
					on.append((r, f8))
				elif self.to_sq == c8:
					off.append((r, a8))
					on.append((r, d8))
			elif self.special == 3:
				off.append((self.piece, self.from_sq))
				on.append((self.piece, self.to_sq))
				if self.to_sq > self.from_sq:  # white en passanting black
					off.append((p, self.to_sq - 16))
				else:
					off.append((P, self.to_sq + 16))
			elif self.special == 4:
				off.append((self.piece, self.from_sq))
				on.append((R*self.piece, self.to_sq))
			elif self.special == 5:
				off.append((self.piece, self.from_sq))
				on.append((B*self.piece, self.to_sq))
			elif self.special == 6:
				off.append((self.piece, self.from_sq))
				on.append((N*self.piece, self.to_sq))
			elif self.special == 7:
				pass
		else:
			off.append((self.piece, self.from_sq))
			on.append((self.piece, self.to_sq))
		if self.captured != 0: off.append((self.captured, self.to_sq))
		return (off, on)


NULLMOVE = Move(-1, -1, 0, 0, 7)


class HashTable():

	def __init__(self, size):
		self.od = OrderedDict()
		self.size = size

	def get(self, key, default=None):
		try:
			self.od.move_to_end(key)
		except KeyError:
			return default
		return self.od[key]

	def set(self, key, value):
		if key not in self.od:
			if len(self.od) == self.size:
				self.od.popitem(last=False)
		self.od[key] = value


class HashTableWithDepth():

	def __init__(self, size):
		self.od = OrderedDict()
		self.size = size

	def get(self, key, depth, default=None):
		if key in self.od:
			self.od.move_to_end(key)
			entry = self.od[key]
			if entry[1] >= depth:
				return entry[0]
			else:
				return default
		else:
			return default

	def set(self, key, value, depth):
		if key in self.od:
			if depth > self.od[key][1]:
				del self.od[key]
				self.od[key] = (value, depth)
		else:
			if len(self.od) == self.size:
				self.od.popitem(last=False)
			self.od[key] = (value, depth)
