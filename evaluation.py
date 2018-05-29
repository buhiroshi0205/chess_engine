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

midgamevalues = '''[[[ 100  100  100  100  100  100  100  100]
  [  74  105   82   53   61  107  120   75]
  [  75  103   96   92  104   93  116   86]
  [  70  106  100  126  123   98  107   99]
  [  86  115  116  123  129  114  133  109]
  [ 134  151  147  158  160  184  177  136]
  [ 195  204  207  198  187  181  227  164]
  [ 100  100  100  100  100  100  100  100]]

 [[ 237  309  313  318  298  306  309  249]
  [ 311  353  347  347  340  368  304  318]
  [ 326  353  366  374  379  364  356  309]
  [ 335  362  392  388  399  399  365  333]
  [ 368  372  388  415  412  431  377  383]
  [ 371  421  416  449  474  421  440  369]
  [ 331  371  397  392  382  431  360  351]
  [ 309  349  358  375  381  344  339  308]]

 [[ 391  400  371  371  366  367  377  382]
  [ 381  422  407  398  392  411  416  396]
  [ 395  402  417  416  408  412  405  390]
  [ 361  425  418  429  426  409  415  367]
  [ 391  419  416  454  445  424  421  413]
  [ 426  425  421  457  450  426  456  426]
  [ 411  425  418  400  429  422  458  418]
  [ 373  386  368  407  397  387  368  378]]

 [[ 506  522  528  527  540  523  538  503]
  [ 507  527  516  509  521  510  507  494]
  [ 507  531  521  523  533  534  547  546]
  [ 526  538  522  533  552  540  537  540]
  [ 550  533  547  551  560  560  585  570]
  [ 547  572  559  573  560  579  578  596]
  [ 588  599  585  598  603  584  617  603]
  [ 566  586  575  576  573  541  531  582]]

 [[1034 1026 1023 1034 1026 1010 1010 1011]
  [1023 1045 1038 1036 1041 1050 1076 1084]
  [1038 1041 1043 1050 1038 1060 1054 1062]
  [1025 1036 1049 1079 1065 1060 1069 1065]
  [1062 1056 1079 1096 1110 1090 1078 1077]
  [1055 1087 1076 1094 1126 1163 1160 1141]
  [1070 1051 1074 1096 1115 1135 1107 1117]
  [1069 1086 1113 1115 1110 1090 1079 1083]]

 [[  46   73   55  -13   25    1   80   66]
  [  71   54   22    8  -12   26   65   42]
  [   5   15  -24  -80  -70  -51  -15   -7]
  [  -9  -34  -63  -74  -83  -86  -49    4]
  [   5  -77  -39  -80 -115  -79  -24    3]
  [ -33  -28  -33  -16  -64   11  -37   -9]
  [   1  -12  -62    8  -17  -33   -6  -18]
  [   5   -3    3  -16   -9  -29  -10    0]]]'''


endgamevalues = '''[[[ 100  100  100  100  100  100  100  100]
  [ 144  146  118  113   90  119  148  155]
  [ 150  162  135  119  120  150  176  174]
  [ 192  149  142  143  145  169  178  212]
  [ 222  187  169  129  145  173  202  244]
  [ 286  323  243  185  196  221  315  340]
  [ 424  436  361  273  287  406  496  449]
  [ 100  100  100  100  100  100  100  100]]

 [[ 415  361  443  443  453  444  389  477]
  [ 375  418  435  439  456  469  464  420]
  [ 398  422  466  463  478  442  453  433]
  [ 442  421  442  451  470  453  473  446]
  [ 443  418  467  463  455  467  448  438]
  [ 412  424  416  465  474  432  434  460]
  [ 348  431  404  461  416  420  411  389]
  [ 286  421  406  371  386  377  364  360]]

 [[ 470  492  430  469  466  441  517  482]
  [ 483  444  487  470  457  476  476  476]
  [ 457  473  479  492  467  482  469  427]
  [ 459  486  472  478  479  435  482  501]
  [ 417  492  496  538  479  453  442  444]
  [ 430  443  478  479  517  463  450  426]
  [ 466  478  429  454  469  446  431  490]
  [ 394  439  492  390  444  443  461  448]]

 [[ 661  753  749  734  744  720  783  663]
  [ 756  759  790  777  760  752  764  786]
  [ 795  792  791  765  762  776  788  795]
  [ 803  813  819  771  786  776  846  839]
  [ 830  818  822  798  811  818  809  820]
  [ 794  822  788  808  801  781  813  810]
  [ 781  791  775  796  768  765  764  797]
  [ 822  852  816  830  800  847  876  813]]

 [[1358 1379 1415 1373 1405 1418 1386 1330]
  [1411 1414 1427 1416 1433 1419 1418 1408]
  [1427 1439 1464 1434 1456 1446 1444 1448]
  [1410 1467 1490 1516 1494 1457 1460 1466]
  [1350 1451 1501 1499 1497 1470 1491 1460]
  [1379 1424 1477 1472 1467 1475 1419 1433]
  [1338 1416 1425 1433 1407 1423 1358 1379]
  [1504 1572 1527 1513 1544 1620 1729 1601]]

 [[ -88  -52  -53  -57  -53  -37  -56  -56]
  [ -73  -10   15  -18   -3    4   -5  -40]
  [ -64    8   62   38   14   35    4    5]
  [ -70   35   60   71   68   40   81   -9]
  [-107   14   96   84  105   93   98  -20]
  [-169   53   85   91  168  174  122  -22]
  [-248 -124  -11   30  108   81   84 -133]
  [-395 -414 -349 -313 -288 -303 -288 -237]]]'''

midgamevalues = midgamevalues.replace('[','')
midgamevalues = midgamevalues.replace(']','')
midgamevalues = list(map(int, midgamevalues.split()))

endgamevalues = endgamevalues.replace('[','')
endgamevalues = endgamevalues.replace(']','')
endgamevalues = list(map(int, endgamevalues.split()))

mpst = [None]
epst = [None]

#Add king mate value
for i in range(5*64,6*64):
	midgamevalues[i] += 60000
	endgamevalues[i] += 60000

#load values data into pst
for i in range(6):
	temp1, temp2 = [], []
	for j in range(8):
		idx = j*8+i*64
		temp1.extend(midgamevalues[idx:idx+8])
		temp2.extend(endgamevalues[idx:idx+8])
		temp1.extend([None]*8)
		temp2.extend([None]*8)
	mpst.append(temp1)
	epst.append(temp2)
for i in range(6,0,-1):
	temp1, temp2 = [], []
	for j in range(128):
		temp1.append(None if j&0x88 else -mpst[i][j^0x70])
		temp2.append(None if j&0x88 else -epst[i][j^0x70])
	mpst.append(temp1)
	epst.append(temp2)

  
SQUARES = []
for i in range(8):
  SQUARES.extend(range(i * 16, i * 16 + 8))


class Eval():

	def __init__(self, state):
		self.state = state
		self.midvalue = self.endvalue = 0
		for i in SQUARES:
			piece = state.board[i]
			if piece != 0:
				self.midvalue += mpst[piece][i]
				self.endvalue += epst[piece][i]

	def update(self, move):
		for piece, square in move.off:
			self.midvalue -= mpst[piece][square]
			self.endvalue -= epst[piece][square]
		for piece, square in move.on:
			self.midvalue += mpst[piece][square]
			self.endvalue += epst[piece][square]

	def restore(self, mid, end):
		self.midvalue = mid
		self.endvalue = end

	def get_score(self):
		phase = self.state.getPhase()
		return self.endvalue*phase + self.midvalue*(1-phase)