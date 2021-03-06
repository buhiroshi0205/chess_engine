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

import time, copy, chess

if __name__ == '__main__':
	from misc import State, HashTable, Move, NULLMOVE, SQUARES
else:
	from . import misc
	State, HashTable, Move, NULLMOVE, SQUARES = misc.State, misc.HashTable, misc.Move, misc.NULLMOVE, misc.SQUARES


class Engine():

	def __init__(self):
		self.root = State()
		self.bestmove = None
		#self.tt = HashTableWithDepth(10 ** 6)  # Transposition Table
		self.qtt = HashTable(10 ** 6)  # Quiescence Transposition Table
		self.bestmoves = HashTable(10 ** 6)


	def negamax(self, n, d, p, a, b, last_move, timelimit=None, legalmoves=None):
		#print(n)
		if timelimit is not None:
			if time.time() > timelimit: return None
		bestmove = None
		global nodes
		nodes += 1
		if n.leaf():
			return n.evaluate()
		elif d == 0:
			if last_move.captured == 0 and (last_move.special == 0 or last_move.special == 2):
				return n.evaluate()
			else:
				return self.quiescence(n,a,b,last_move.to_sq)

		pv = self.bestmoves.get(n.zobrist)
		#best = self.tt.get(n.zobrist,d,-100000)
		best = -100000
		#if best >= b: return best

		if pv is None:  # alphabeta
			for move in n.generate_moves():
				if legalmoves is not None and str(move) not in legalmoves: continue
				snapshot = n.make_move(move)
				v = -self.negamax(n, d - 1, p + 1, -b, -a, move, timelimit)
				n.unmake_move(move, snapshot)

				if v > best:
					best = v
					bestmove = move
					if best > a:
						a = best
						if a >= b: break

		else:  # pvs

			snapshot = n.make_move(pv)
			v = -self.negamax(n, d - 1, p + 1, -b, -a, pv, timelimit)
			n.unmake_move(pv, snapshot)

			best = v
			bestmove = pv
			if best > a:
				a = best

			if a < b:
				for move in n.generate_moves():
					if legalmoves is not None and str(move) not in legalmoves: continue
					if pv.to_sq == move.to_sq and pv.from_sq == move.from_sq: continue

					snapshot = n.make_move(move)
					v = -self.negamax(n, d - 1, p + 1, -a - 1, -a, move, timelimit)
					n.unmake_move(move, snapshot)

					if v >= b: # wtf why didn't you tell me you have such a good move?
						a = best = v
						bestmove = move
						break
					elif v > a: # there's a better move
						snapshot = n.make_move(move)
						v = -self.negamax(n, d - 1, p + 1, -b, -v, move, timelimit)
						n.unmake_move(move, snapshot)

						a = best = v
						bestmove = move
						if a >= b: break
					else: # nah non-pv move as bad as expected 
						if v > best: best = v

		if a < -40000:  # stalemate check:
			value1 = self.basic_negamax(n, 2)
			snapshot = n.make_move(NULLMOVE)
			stalemate = self.basic_negamax(n, 1) > -40000 and value1 < -40000
			n.unmake_move(NULLMOVE, snapshot)
			if stalemate: return 0

		if bestmove is not None and p < 7:
			self.bestmoves.set(n.zobrist, bestmove)
			#self.tt.set(n.zobrist,best,d)

		return best

	def quiescence(self,n,a,b,sq):
		global nodes_q
		nodes_q += 1

		v = n.evaluate()
		if v > a:
			a = v
			if a >= b: return a

		for move in n.generate_moves():
			if move.captured == 0 or move.to_sq != sq: continue

			snapshot = n.make_move(move)
			v = -self.quiescence(n, -b, -a, move)
			n.unmake_move(move, snapshot)

			if v > a:
				a = v
				if a >= b: return a

		return a

	def basic_negamax(self, n, d):
		if n.leaf() or d == 0: return n.evaluate()
		best = -100000
		for move in n.generate_moves():
			snapshot = n.make_move(move)
			v = -self.basic_negamax(n, d - 1)
			n.unmake_move(move, snapshot)
			if v > best: best = v
		return best

	def search(self, depth=None, movetime=None, params=None):
		global nodes, nodes_q
		if params is not None:
			depth, movetime = params
		timelimit = None if movetime is None else (time.time() + movetime)
		backup = copy.deepcopy(self.root)
		legalmoves = [move.uci() for move in chess.Board(self.root.fen()).legal_moves]
		d = 1
		while True:
			nodes = nodes_q = 0
			try:
				value = self.negamax(self.root, d, 0, -100000, 100000, None, timelimit, legalmoves=legalmoves)
			except TypeError:
				break
			bestmove = self.bestmoves.get(self.root.zobrist)
			pv = []
			mv = self.bestmoves.get(self.root.zobrist)
			while mv is not None:
				pv.append(str(mv))
				self.root.make_move(mv)
				if self.root.zobrist == backup.zobrist: break
				mv = self.bestmoves.get(self.root.zobrist)
			self.root = copy.deepcopy(backup)
			print(('depth=%d: value = %.2f, nodes = %d, quiescence nodes = %d, pv = ' % (d, value / 100, nodes, nodes_q)) + ' '.join(pv))
			d += 1
			if depth is not None and d > depth: break
		self.root = backup
		return bestmove, value

	def ssearch(self, d, n=None):
		if n is None: n = self.root
		return self.negamax(n,d,0,-100000,100000,None)

	def allocatetime(self, timeleft, inc):#both in milliseconds
		timeleft /= 1000
		inc /= 1000
		mvtm = (timeleft-inc) * 0.04 + inc - 1.2
		maxdepth = self.root.fullmove_number//5 + 6
		if mvtm < 0.1: return (4, 0.1)
		return (maxdepth, mvtm)




if __name__ == '__main__':
	engine = Engine()
	while True:
		print(engine.root)
		print('Engine thinking...')
		move, value = engine.search(6)
		engine.root.make_move(move)
		print('Engine made move ' + str(move))
		print(engine.root)
		print('Your turn, make a move:')
		move = None
		while move is None:
			try:
				move = input()
				fsq, tsq = eval(move[:2]), eval(move[2:])
				if fsq not in SQUARES or tsq not in SQUARES or engine.root.board[fsq] is None: move = None
			except Exception:
				pass
		engine.root.make_move(Move(fsq, tsq, engine.root.board[fsq], engine.root.board[tsq]))