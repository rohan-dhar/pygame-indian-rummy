import random, copy, pygame, os, time, pickle, fpdf, subprocess, platform, pylab, numpy, pygame_textinput

# General game settings and configuration
conf = {
	'imageWidth': 87,
	'imageHeight': 130,
	'screenWidth': 1300,
	'screenHeight': 800
}

# Dist to store fonts once they are loaded
fonts = {
	'heading': None,
	'player': None,
	'hero': None
}

music = {
	'bg': None,
	'won': None,
	'lost': None,
	'stack': None,
	'card': None,
	'start': None
}

# Dict for RGB values of colors
colors = {
	'white': (255,255,255),
	'green': (48,195,136),
	'darkGreen': (33, 116, 82)
}

# Dict used to store images once they are loaded
images = {}

# Flattens a 2D list to a 1D list of values inside the 2D list
def flattenList(lst):
	ret = []
	for item in lst:
		for subItem in item:
			ret.append(subItem)
	
	return ret



def prompt(text):
	text = input(text)
	return text



def openPDF():
	if platform.system() == 'Darwin':
		subprocess.call(('open', 'Report.pdf'))
	elif platform.system() == 'Windows':
		os.startfile('Report.pdf')
	else:
		subprocess.call(('xdg-open', 'Report.pdf'))


class LeaderRecord:

	FILE_NAME = 'leaderboard.bin'

	def __init__(self, name):
		assert type(name) == str, 'Name must be a string'
		self.name = name
		self.moves = []
		self.hasWon = None
		self.gameTime = None

	def addMove(self):
		move = {
			'stack': None,
			'startTime': time.time(),
			'endTime': None
		}
		self.moves.append(move)

	def setMoveStack(self, stack):
		assert stack == 'pile' or stack == 'deck', 'Invalid stack for passed for adding'		
		self.moves[-1]['stack'] = stack

	def setMoveTime(self):		
		self.moves[-1]['endTime'] = time.time()

	def saveToFile(self, hasWon):
		assert type(hasWon) == bool, 'Invalid hasWon state passed'
		
		self.hasWon = hasWon
		self._setGameTime()
		
		file = open(LeaderRecord.FILE_NAME, 'ab')
		pickle.dump(self, file)
		file.close()

	def _setGameTime(self):
		self.gameTime = self.moves[-1]['endTime'] - self.moves[0]['startTime']

	def genPDF(self):
		assert self.gameTime != None, 'Can not generate a PDF of a game that is not over'
		deckMoves, pileMoves = 0, 0
		for m in self.moves:
			if m['stack'] == 'pile':
				pileMoves += 1
		deckMoves = len(self.moves) - pileMoves

		pdf = fpdf.FPDF('P', 'pt', 'A4')
		pdf.add_page()
		pdf.set_font('Arial', 'B', 40)
		pdf.cell(0, 120, 'Game Report', 0, 2, 'C')
		
		pdf.set_font('Arial', '', 13)
		pdf.cell(0, 15, 'Name', 0, 1, 'L')
		pdf.set_font('Arial', 'B', 18)		
		pdf.cell(0, 36, self.name, 0, 2, 'L')
		pdf.cell(0, 15, '', 0, 2, 'L')

		pdf.set_font('Arial', '', 13)
		pdf.cell(0, 15, 'Status', 0, 1, 'L')
		pdf.set_font('Arial', 'B', 18)
		
		if self.hasWon:
			pdf.cell(0, 36, 'Won', 0, 2, 'L')
			pdf.cell(0, 15, '', 0, 2, 'L')
		else:			
			pdf.cell(0, 36, 'Lost', 0, 2, 'L')
			pdf.cell(0, 15, '', 0, 2, 'L')

		pdf.set_font('Arial', '', 13)
		pdf.cell(0, 15, 'Started At ', 0, 1, 'L')
		pdf.set_font('Arial', 'B', 18)
		pdf.cell(0, 36, time.ctime(self.moves[0]['startTime']), 0, 2, 'L')
		pdf.cell(0, 15, '', 0, 2, 'L')
		
		pdf.set_font('Arial', '', 13)
		pdf.cell(0, 15, 'Ended At ', 0, 1, 'L')
		pdf.set_font('Arial', 'B', 18)
		pdf.cell(0, 36, time.ctime(self.moves[-1]['endTime']), 0, 2, 'L')
		pdf.cell(0, 15, '', 0, 2, 'L')
		
		pdf.set_font('Arial', '', 13)
		pdf.cell(0, 15, 'Duration ', 0, 1, 'L')
		pdf.set_font('Arial', 'B', 18)
		pdf.cell(0, 36, str(round(self.gameTime, 2)) + ' s', 0, 2, 'L')
		pdf.cell(0, 15, '', 0, 2, 'L')
		
		pdf.set_font('Arial', '', 13)
		pdf.cell(0, 15, 'Moves taken ' , 0, 1, 'L')
		pdf.set_font('Arial', 'B', 18)
		pdf.cell(0, 36, str(len(self.moves)) , 0, 2, 'L')
		pdf.cell(0, 15, '', 0, 2, 'L')
		
		pdf.set_font('Arial', '', 13)
		pdf.cell(0, 15, 'No. of times Deck used ', 0, 1, 'L')
		pdf.set_font('Arial', 'B', 18)
		pdf.cell(0, 36, str(deckMoves), 0, 2, 'L')
		pdf.cell(0, 15, '', 0, 2, 'L')
		
		pdf.set_font('Arial', '', 13)
		pdf.cell(0, 15, 'No. of times Pile used ', 0, 1, 'L')
		pdf.set_font('Arial', 'B', 18)
		pdf.cell(0, 36, str(pileMoves), 0, 2, 'L')
		pdf.cell(0, 15, '', 0, 2, 'L')
		
		pdf.set_font('Arial', '', 13)
		pdf.cell(0, 15, 'Experimental score ', 0, 1, 'L')
		pdf.set_font('Arial', 'B', 18)
		pdf.cell(0, 36, str(round(deckMoves/len(self.moves) * 100, 2)) + ' / 100', 0, 2, 'L')
		pdf.cell(0, 15, '', 0, 2, 'L')
		
		pdf.add_page()
		pdf.set_font('Arial', 'B', 40)
		pdf.cell(0, 120, 'MOVES', 0, 2, 'C')
		
		x = []
		y = []		

		for i in range(len(self.moves)):
			move = self.moves[i]
			pdf.set_font('Arial', 'B', 16)
			pdf.cell(0, 24, 'Move '+str(i+1)+': ' + str(round(move['endTime']-move['startTime'], 2)) +' s' , 0, 2, 'L')
			pdf.set_font('Arial', '', 16)
			pdf.cell(0, 24,  'Stack: '+move['stack'].upper(), 0, 2, 'L')
			pdf.cell(0, 16, '' , 0, 2, 'L')
			x.append(i+1)
			y.append(round(move['endTime']-move['startTime'], 2))			

		pylab.clf()
		pylab.title('Move v/s Time: Graphic Analysis')
		pylab.xlabel('Move number')
		pylab.ylabel('Time per move (sec)')
		pylab.plot(x, y)
		pylab.savefig('graph.png')
		pdf.image('graph.png')
		pdf.output('Report.pdf', 'F').encode('latin-1')






def getLeaderBoard(n = 7):
	assert type(n) == int and n > 0, 'Invalid top number passed'
	
	recs = []
	over = False
	
	try:
		file = open(LeaderRecord.FILE_NAME, 'rb')
	except FileNotFoundError:
		return []
	
	while not over:
		try:
			r = pickle.load(file)
			recs.append(r)
		
		except EOFError:
			over = True

	file.close()
	recs = list(filter(lambda x: x.hasWon, recs))
	recs.sort(key = lambda x: x.gameTime)
	recs = recs[:n]
	return recs

def text(text, font, color, x, y, screen):
	text = fonts[font].render(text, True, colors[color]) 
	textRect = text.get_rect()
	textRect.center = (x, y) 
	screen.blit(text, textRect)



# Class to abstract mouse click events
class EventHandler:
	def __init__(self):
		self._elems = []		

	def removeAllElems(self):
		self._elems.clear()

	# Adds elements to search mouse click for
	def addElem(self, name, x, y, width, height):
		assert type(x) == int and type(y) == int, 'Element position can only be integers'
		assert type(width) == int and type(width) == int, 'Element dimensions can only be integers'
		assert type(name) == str, 'Element name must be a string'
		
		e = {
			'name': name,
			'x': x,
			'y': y,
			'height': height,
			'width': width
		}
		self._elems.append(e)		

	def __len__(self):
		return len(self._elems)

	# Returns the element which is present at the given mouse co-ordinates
	def getClick(self, x, y):		
		for e in self._elems:
			if x in range(e['x'], e['x'] + e['width'] + 1) and y in range(e['y'], e['y'] + e['height'] + 1):
				return e['name']

		return 'none'

# Class to abstract playing cards
class Card:
	
	# Static dict of valid suits with their resoective names
	SUITS = {'H': 'Hearts', 'D': 'Diamonds', 'S': 'Spades', 'C': 'Clubs'}
	
	def __init__(self, rank, suit):
		
		assert suit in Card.SUITS, 'Invalid suit for the Card'
		assert type(rank) == int and rank >= 1 and rank <= 13 , 'Invalid rank for the Card'
		
		self._suit = suit
		self._rank = rank

	# Returns the rank of the card
	def getRank(self):
		return self._rank

	# Returns the suit of the card
	def getSuit(self):
		return self._suit

	# Overridding the eqality operator
	def __eq__(self, other):
		if self._rank == other._rank and self._suit == other._suit:
			return True
		else:
			return False

	# Str representation of card
	def __str__(self):
		return str(self._rank) + ' of ' + Card.SUITS[self._suit]

# Abstracts a stack of cards
class CardStack:
		
	# Static property denoting number of times to shuffle cards on calling the shuffle method
	SHUFFLE_DEPTH = 10
	
	# Creates a CardStack from a list of cards. Shuffles the stack if shuffle parameter is true
	def __init__(self, cards = [], shuffle = False):
		assert type(cards) == list and (len(cards) == 0 or type(cards[0]) == Card), "Invalid cards for CardStack"
		self._cards = copy.deepcopy(cards)
		if shuffle:
			self.shuffle()
	
	# Shuffles the card stack SHUFFLE_DEPTH times
	def shuffle(self):
		for _ in range(CardStack.SHUFFLE_DEPTH * len(self._cards)):		
			i1 = random.randint(0, len(self._cards) - 1)
			i2 = random.randint(0, len(self._cards) - 1)
			self._cards[i1], self._cards[i2] = self._cards[i2], self._cards[i1]


	# Sort cards in ascending order by suit and then by rank
	def sortBySuit(self):
		self._cards.sort(key = lambda x: (x.getSuit(), x.getRank()))

	# Sort cards in ascending order by rank
	def sortByRank(self):
		self._cards.sort(key = lambda x: x.getRank())


	# Adds the given card to the stack
	def addCard(self, v):
		assert type(v) == Card, 'Invalid card added to CardStack'
		self._cards.append(v)

	# Overriding len() of the card stack to return the number of cards
	def __len__(self):
		return len(self._cards)

	# Overriring index access to return the card at the given index
	def __getitem__(self, i):
		if i == len(self._cards) or i < 0:
			raise IndexError
		else:
			return self._cards[i]

	# Updates the card at the given index with the new card passed
	def __setitem__(self, i, v):		
		assert type(v) == Card, 'Invalid card added to CardStack'
		if i == len(self._cards) or i < 0:
			raise IndexError
		else:
			self._cards[i] = v
			return True

	# Overriding del to delete the card at the given index
	def __delitem__(self, i):
		if i == len(self._cards) or i < 0:
			raise IndexError
		else:
			self._cards.pop(i)

	# Get a string representation of each card in the stack
	def __str__(self):
		ret = ''
		for card in self._cards:
			ret += str(card) + ' \n'
		return ret

# Abstracts the game's player
class Player:
	
	# Static property denoting number of cards a player can have
	CARDS_NUM = 11
	
	# Constructor for Player. comp signifies if the player is computer controlled or not
	def __init__(self, stack, comp = False):
		assert type(stack) == CardStack and len(stack) == Player.CARDS_NUM, 'Invalid CardStack passed to player'
		assert type(comp) == bool, 'Invalid player type passed'
		self._stack = stack
		self._comp = comp

	# Draws the player on the screen and updates eventHandler to listen for events at the cards
	def render(self, screen, eventHandler = None):
		global conf, images, fonts, colors
		if self._comp:

			y = 150			
			text('COMPUTER', 'player', 'darkGreen', conf['screenWidth'] // 2, y + conf['imageHeight'] + 48, screen)
			if eventHandler == None:
				for i in range(len(self._stack)):
					x = conf['screenWidth']//2 - conf['imageWidth']//2 + (i-self.CARDS_NUM//2) * (conf['imageWidth'] + 7) - 10
					screen.blit(images[str(self._stack[i].getRank())+self._stack[i].getSuit()], (x, y))
			else:
				for i in range(len(self._stack)):
					x = conf['screenWidth']//2 - conf['imageWidth']//2 + (i-5) * (15)
					screen.blit(images['back'], (x, y))
			
		else:
			y = conf['screenHeight'] - conf['imageHeight'] - 100
			text('PLAYER 1', 'player', 'darkGreen', conf['screenWidth'] // 2, y + conf['imageHeight'] + 48, screen)			
			for i in range(len(self._stack)):
				x = conf['screenWidth']//2 - conf['imageWidth']//2 + (i-self.CARDS_NUM//2) * (conf['imageWidth'] + 7) - 10
				screen.blit(images[str(self._stack[i].getRank())+self._stack[i].getSuit()], (x, y))
				name = 'card-'+str(i)
				if eventHandler != None:
					if i < 9:
						legend = str(i + 1)
					else:
						legend = chr(56 + i)
					text(legend, 'player', 'darkGreen', x + conf['imageWidth']//2, y - 25, screen)								
					eventHandler.addElem(name, x, y, conf['imageWidth'], conf['imageHeight'])


	# Swaps cards at the given indices in the player's stack
	def swapStack(self, i, j):
		assert type(i) == int and type(j) == int, 'Card indices must be int'
		assert i >= 0 and i < len(self._stack) and j >= 0 and j < len(self._stack), 'Invalid card indices'

		self._stack[i], self._stack[j] = self._stack[j], self._stack[i]

	# Returns a list of distincs n-sized runs in the player's stack
	# Runs are found after removing cards present in the exclude list and adding cards present in the include list
	def getRuns(self, n, exclude, include):
		
		assert type(n) == int, 'Size of runs must be an int'
		assert type(exclude) == list, 'Excluded cards must be in a list'
		assert type(include) == list, 'Included cards must be in a list'

		cards = copy.deepcopy(self._stack)
		indexes = []	
		for i in range(len(cards)):
			if cards[i] in exclude:
				indexes.append(i)

		c = 0
		for i in indexes:
			del cards[i-c]
			c += 1

		for c in include:
			cards.addCard(c)
		
		cards.sortBySuit()

		groups = []
		i = 0
		while i < len(cards) - n + 1:
			flag = True
			g = []
			for j in range(i, i + n - 1):
				if cards[j].getRank() == cards[j+1].getRank() - 1 and cards[j].getSuit() == cards[j+1].getSuit():
					g.append(cards[j])
					if j == i+n-2:
						g.append(cards[j+1])
				else:
					flag = False
					break
			if flag:
				i += n
				groups.append(g)
			else:
				i += 1

		return groups
	
	# Returns a list of distincs n-sized books in the player's stack
	# Books are found after removing cards present in the exclude list and adding cards present in the include list
	def getBooks(self, n, exclude, include):
		
		assert type(n) == int, 'Size of books must be an int'
		assert type(exclude) == list, 'Excluded cards must be in a list'
		assert type(include) == list, 'Included cards must be in a list'
		
		cards = copy.deepcopy(self._stack)
		indexes = []	
		
		for i in range(len(cards)):
			if cards[i] in exclude:
				indexes.append(i)

		c = 0
		for i in indexes:
			del cards[i-c]
			c += 1

		for c in include:
			cards.addCard(c)

		cards.sortByRank()
		groups = []
		i = 0
		while i < len(cards) - n + 1:
			g = []
			flag = True
			for j in range(i, i+n-1):
				if cards[j].getRank() == cards[j+1].getRank():
					g.append(cards[j])
					if j == i+n-2:
						g.append(cards[j+1])
				else:
					flag = False
					break
			if flag:
				i += n
				groups.append(g)
			else:
				i += 1

		return groups

	# Adds a card to player's stack
	def addCard(self, card):
			self._stack.addCard(card)

	# Returns a card in player's stack at the given index
	def getCard(self, i):
		assert type(i) == int, 'Card index must be an int'
		return copy.deepcopy(self._stack[i])
	
	# Removes the card in player's stack at the given index
	def removeCard(self, i):
		assert type(i) == int, 'Card index must be an int'
		del self._stack[i]

	# Returns the number of cards the player currently possess
	def getCurrentCardsNum(self):
		return len(self._stack)


	# Checks if the computer player should choose the given card from the pile or choose a card from the deck
	# Returns a boolean value where True denotes choosing the given pile card
	def chooseCard(self, pileCard):
		
		assert self._comp == True, 'Only the computer player can choose a card'
		
		start4Books = len(self.getBooks(4, [], []))
		end4Books = len(self.getBooks(4, [], [pileCard]))

		start4Runs = len(self.getRuns(4, [], []))
		end4Runs = len(self.getRuns(4, [], [pileCard]))

		start3Books = len(self.getBooks(3, [], []))
		end3Books = len(self.getBooks(3, [], [pileCard]))

		start3Runs = len(self.getRuns(3, [], []))
		end3Runs = len(self.getRuns(3, [], [pileCard]))

		start2Runs = len(self.getRuns(2, [], []))
		end2Runs = len(self.getRuns(2, [], [pileCard]))

		start2Books = len(self.getBooks(2, [], []))
		end2Books = len(self.getBooks(2, [], [pileCard]))


		if self.hasWon([], [pileCard]):
			return True

		fourRunsUtility = 0
		if start4Runs == 0 and end4Runs > 0:
			fourRunsUtility = 2

		fourBooksUtility = 0
		if start4Books == 0 and end4Books > 0 and start4Runs == 0 and end4Runs == 0:
			fourBooksUtility = 4



		runsUtility = 0
		if start3Runs < 2:		
			runsUtility = (end3Runs - start3Runs) * 2 * (2 - start4Runs)
		
		booksUtility = 0		
		if end3Books > start3Books:
			if start4Books == 0:
				booksUtility = 2
			elif start3Books == 0:
				booksUtility = 1

		if start4Books == 0 and start3Books == 0 and start2Books < end2Books:
			booksUtility += 1

		if start4Books == 0 and start2Books < end2Books:
			booksUtility += 0.5

		if start4Runs == 0 and start3Runs == 0 and start2Runs < end2Runs:
			runsUtility += 1

		if start4Runs == 0 and start2Runs < end2Runs:
			runsUtility += 0.5


		return booksUtility + fourBooksUtility + runsUtility + fourRunsUtility > 2

	def _getCardUtil(self, card):

		assert self._comp == True, 'Only the computer player can choose a card'
		
		if self.hasWon([], []) and not self.hasWon([card], []):
			return 100

		start4Books = len(self.getBooks(4, [], []))
		end4Books = len(self.getBooks(4, [card], []))

		start4Runs = len(self.getRuns(4, [], []))
		end4Runs = len(self.getRuns(4, [card], []))

		start3Books = len(self.getBooks(3, [], []))
		end3Books = len(self.getBooks(3, [card], []))

		start3Runs = len(self.getRuns(3, [], []))
		end3Runs = len(self.getRuns(3, [card], []))

		start2Runs = len(self.getRuns(2, [], []))
		end2Runs = len(self.getRuns(2, [card], []))

		start2Books = len(self.getBooks(2, [], []))
		end2Books = len(self.getBooks(2, [card], []))

		fourBooksUtility = 0
		if start4Books == 1 and end4Books == 0:
			fourBooksUtility = 5
		elif start4Books < end4Books:
			fourBooksUtility = 1

		fourRunsUtility = 0
		if start4Runs == 0 and end4Runs > 0:
			fourRunsUtility = 4


		runsUtility = 0
		if end3Runs < 2 and end3Runs < start3Runs:		
			runsUtility = (start3Runs - end3Runs) * 2
		elif end3Runs < start3Runs:
			runsUtility = 1
		
		booksUtility = 0
		if end3Books < start3Books:
			if start4Books == 0:
				booksUtility = 2
			elif end3Books == 1:
				booksUtility = 1

		if start4Runs == 0 and start3Runs == 0 and start2Runs < end2Runs:
			runsUtility += 1

		if start4Runs == 0 and start2Runs < end2Runs:
			runsUtility += 0.5

		if start4Books == 0 and start3Books == 0 and start2Books < end2Books:
			booksUtility += 1

		if start4Books == 0 and start2Books < end2Books:
			booksUtility += 0.5


		return booksUtility + runsUtility + fourBooksUtility

	# Returns the index of the card which the computer player should remove to maximize probabilty of winning
	# Removes the card with the minimum utility 
	def cardToRemove(self):
		minUtil, minUtilIndex = -1, -1

		for i in range(len(self._stack)):
			if i == 0:
				minUtil = self._getCardUtil(self._stack[i])
				minUtilIndex = i
			else:
				util = self._getCardUtil(self._stack[i])
				if util <= minUtil:
					minUtil = util
					minUtilIndex = i

		return minUtilIndex

 	# Checks if the player has won, returns boolean
	def hasWon(self, exclude, include):	
		fourBooks = self.getBooks(4, exclude, include)
		fourRuns = self.getRuns(4, exclude, include)

		if len(fourBooks) >= 1:			
			allBooks = fourBooks[0]
			runs = self.getRuns(3, allBooks + exclude, include)
			books = self.getBooks(3, allBooks + exclude, include)
			booksWithoutRuns = self.getBooks(3, allBooks+flattenList(runs)+exclude, include)
			runsWithoutBooks = self.getRuns(3, allBooks+flattenList(books)+exclude, include)
			if len(runs) >= 2 or (len(books) == 1 and len(runsWithoutBooks) == 1) or (len(runs) == 1 and len(booksWithoutRuns) == 1):	
				return True
			elif len(fourBooks) == 2:
				allBooks = fourBooks[1]
				runs = self.getRuns(3, allBooks, include)
				books = self.getBooks(3, allBooks, include)
				booksWithoutRuns = self.getBooks(3, allBooks+flattenList(runs)+exclude, include)
				runsWithoutBooks = self.getRuns(3, allBooks+flattenList(books)+exclude, include)
				if len(runs) >= 2 or (len(books) == 1 and len(runsWithoutBooks) == 1) or (len(runs) == 1 and len(booksWithoutRuns) == 1):	
					return True
				else:
					return False
			else:
				return False
		elif len(fourRuns) >= 1:
			allRuns = fourRuns[0]
			runs = self.getRuns(3, allRuns + exclude, include)
			books = self.getBooks(3, allRuns + exclude, include)
			booksWithoutRuns = self.getBooks(3, allRuns+flattenList(runs)+exclude, include)
			runsWithoutBooks = self.getRuns(3, allRuns+flattenList(books)+exclude, include)
			if len(runs) >= 2 or (len(books) == 1 and len(runsWithoutBooks) == 1) or (len(runs) == 1 and len(booksWithoutRuns) == 1):	
				return True
			elif len(fourRuns) == 2:
				allRuns = fourRuns[1]
				runs = self.getRuns(3, allRuns, include)
				books = self.getBooks(3, allRuns, include)
				booksWithoutRuns = self.getBooks(3, allRuns+flattenList(runs)+exclude, include)
				runsWithoutBooks = self.getRuns(3, allRuns+flattenList(books)+exclude, include)
				if len(runs) >= 2 or (len(books) == 1 and len(runsWithoutBooks) == 1) or (len(runs) == 1 and len(booksWithoutRuns) == 1):	
					return True
				else:
					return False
			else:
				return False

		else:
			return False


class Game:
	def __init__(self, eventHandler):
		global images, conf, fonts, colors
		self._eventHandler = eventHandler
		self.setInitialState()		
		pygame.init()
		self.screen = pygame.display.set_mode((conf['screenWidth'], conf['screenHeight']))
		pygame.display.set_caption('Indian Rummy')
		self.screen.fill(colors['green'])		
		pygame.mouse.set_cursor(*pygame.cursors.broken_x)

		fonts['heading'] = pygame.font.Font(os.path.join('assets', 'AvenirNext.ttc'), 38)
		fonts['player'] = pygame.font.Font(os.path.join('assets', 'AvenirNext.ttc'), 24)
		fonts['hero'] = pygame.font.Font(os.path.join('assets', 'AvenirNext.ttc'), 80)

		music['bg'] = pygame.mixer.Sound(os.path.join('music', 'bg.ogg'))
		music['won'] = pygame.mixer.Sound(os.path.join('music', 'won.ogg'))
		music['lost'] = pygame.mixer.Sound(os.path.join('music', 'lost.ogg'))
		music['stack'] = pygame.mixer.Sound(os.path.join('music', 'stack.ogg'))
		music['card'] = pygame.mixer.Sound(os.path.join('music', 'card.ogg'))
		music['start'] = pygame.mixer.Sound(os.path.join('music', 'start.ogg'))

		for suit in Card.SUITS:
			for i in range(13):
				name = str(i+1) + suit
				images[name] = pygame.image.load( os.path.join('cards', name+'.png') )
				images[name].convert_alpha()
				images[name] = pygame.transform.scale(images[name], (conf['imageWidth'], conf['imageHeight']))
		
		images['back'] = pygame.image.load( os.path.join('cards', 'back.png') )
		images['back'].convert_alpha()
		images['back'] = pygame.transform.scale(images['back'], (conf['imageWidth'], conf['imageHeight']))
		
		images['none'] = pygame.image.load( os.path.join('cards', 'none.png') )
		images['none'].convert_alpha()
		images['none'] = pygame.transform.scale(images['none'], (conf['imageWidth'], conf['imageHeight']))


	def setInitialState(self):
		self._delayCount = 0		
		self._deck = CardStack()		
		self._eventHandler.removeAllElems()
		self._swapSelect = -1
		self._leader = None
		self._textBox = None

		for i in range(52):
			suit = 'H'
			if i % 4 == 1:
				suit = 'D'
			elif i % 4 == 2:
				suit = 'S'
			elif i % 4 == 3:
				suit = 'C'
			self._deck.addCard(Card(i//4 + 1, suit))	

		self._deck.shuffle()
		
		self._pile = CardStack()
		self._state = 'start'

		player1stack = CardStack()
		player2stack = CardStack()

		for i in range(Player.CARDS_NUM):			
			player1stack.addCard(copy.deepcopy(self._deck[0]))
			del self._deck[0]
			player2stack.addCard(copy.deepcopy(self._deck[0]))
			del self._deck[0]

		self._player1 = Player(player1stack)
		self._player2 = Player(player2stack, True)
		self._eventHandler.addElem('start-btn', conf['screenWidth']//2 - 200, conf['screenHeight'] - 200, 180, 60)
		self._eventHandler.addElem('leader-btn', conf['screenWidth']//2 + 20, conf['screenHeight'] - 200, 180, 60)

	
	def getName(self):
		self._state = 'nameInput'
		self._eventHandler.removeAllElems()
		self._textBox = pygame_textinput.TextInput(font_family = os.path.join('assets', 'AvenirNext.ttc'), font_size = 30, text_color=colors['darkGreen'], cursor_color=colors['darkGreen'])


	def start(self, userName):
		global conf, music
		self._eventHandler.removeAllElems()
		self._state = 'player1stack'
		deckX = conf['screenWidth'] - conf['imageWidth'] - 126
		pileX = 44
		y = 290
		
		self._textBox = None

		self._leader = LeaderRecord(userName)
		music['start'].play(0)
		self._leader.addMove()
		self._eventHandler.addElem('deck', deckX, y, conf['imageWidth'] + 90, conf['imageHeight']+66)
		self._eventHandler.addElem('pile', pileX, y, conf['imageWidth'] + 220, conf['imageHeight'])


	def over(self, player):
		assert player == 1 or player == 2, 'Invalid player number'
		self._swapSelect = -1
		self._eventHandler.removeAllElems()

		self._eventHandler.addElem('restart-btn', conf['screenWidth']//2 - 180, 440, 160, 60)
		self._eventHandler.addElem('self-analysis-btn', conf['screenWidth']//2 + 20, 440, 160, 60)

		self._state = 'player'+str(player)+'win'
		if player == 1:
			music['won'].play(0)
			self._leader.saveToFile(True)
		else:
			music['lost'].play(0)
			self._leader.saveToFile(False)

	def showLeaderBoard(self):
		self._state = 'leaderboard'
		self._eventHandler.removeAllElems()
		self._eventHandler.addElem('home-btn', conf['screenWidth']//2 - 90, conf['screenHeight'] - 120, 180, 60)
		self._leader = getLeaderBoard()		
		col4x, y = 4 * conf['screenWidth']//5, 175

		for i in range(len(self._leader)):
			eventHandler.addElem('analysis-'+str(i), col4x - 70, y + 65*i + 30 , 140, 50)

	def update(self):
		if len(self._deck) == 0:
			self._deck = self._pile
			self._pile = CardStack()
			self._deck.shuffle()

		if self._state == 'player2stack' and self._delayCount == 7:

			if len(self._pile) != 0:
				addFromPile = self._player2.chooseCard(copy.deepcopy(self._pile[len(self._pile) - 1]))
				if addFromPile:
					self._player2.addCard(copy.deepcopy(self._pile[len(self._pile) - 1]))
					del self._pile[len(self._pile) - 1]
				else: 
					self._player2.addCard(copy.deepcopy(self._deck[len(self._deck) - 1]))
					del self._deck[len(self._deck) - 1]
			else:
				self._player2.addCard(copy.deepcopy(self._deck[len(self._deck) - 1]))
				del self._deck[len(self._deck) - 1]

			removeIndex = self._player2.cardToRemove()
			removed = self._player2.getCard(removeIndex)
			self._pile.addCard(removed)
			self._player2.removeCard(removeIndex)
			self._state = 'player1stack'
			self._delayCount = 0
			if self._player2.hasWon([], []):
				self.over(2)
				return
			self._leader.addMove()				
			
			return
		elif self._state == 'player2stack':
			self._delayCount += 1	
		elif self._state == 'nameInput':
			if self._textBox.update(pygame.event.get()):
				name = self._textBox.get_text().strip()
				if len(name) > 0:
					self.start(name)


		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				game.close()
			if e.type == pygame.MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()	
				elem = self._eventHandler.getClick(x, y)
				if self._state == 'player1stack':

					if elem == 'deck' and len(self._deck) > 0:
						self._player1.addCard(copy.deepcopy(self._deck[len(self._deck) - 1]))
						del self._deck[len(self._deck) - 1]
						self._state = 'player1card'
						self._swapSelect = -1
						self._leader.setMoveStack('deck')
						music['stack'].play(0)
						break
					elif elem == 'pile' and len(self._pile) > 1:
						self._player1.addCard(copy.deepcopy(self._pile[len(self._pile) - 1]))
						del self._pile[len(self._pile) - 1]
						self._state = 'player1card'
						self._leader.setMoveStack('pile')
						music['stack'].play(0)
						self._swapSelect = -1
						break

				elif self._state == 'player1card':
					if elem[0:4] == 'card':
						cardIndex = int(elem[5:])						
						card = self._player1.getCard(cardIndex)
						self._player1.removeCard(cardIndex)
						self._pile.addCard(card)
						self._leader.setMoveTime()
						if self._player1.hasWon([], []):
							self.over(1)
							return							
						
						music['card'].play(0)
						self._state = 'player2stack'
						break
				elif self._state == 'start':
					if elem == 'start-btn':
						self.getName()						
					if elem == 'leader-btn':
						self.showLeaderBoard()
				elif self._state == 'leaderboard':
					if elem == 'home-btn':
						self.setInitialState()
					elif elem[:8] == 'analysis':
						i = int(elem[9:])
						self._leader[i].genPDF()
						openPDF()						

				elif self._state == 'player1win' or self._state == 'player2win':
					if elem == 'restart-btn':
						self.setInitialState()
					elif elem == 'self-analysis-btn':
						self._leader.genPDF()
						openPDF()

			elif e.type == pygame.KEYDOWN and (self._state == 'player1stack' or self._state == 'player1card'):
				pressed = -1
				
				if e.key >= 49 and e.key <= 57:
					pressed = e.key - 49
				elif e.key >= 97 and e.key < 97 + (self._player1.getCurrentCardsNum() - 9):
					pressed = e.key - 88
				elif e.key >= 65 and e.key < 65 + (self._player1.getCurrentCardsNum() - 9):
					pressed = e.key - 66

				if pressed != -1:					
					if self._swapSelect == -1:
						self._swapSelect = pressed
					else:
						self._player1.swapStack(self._swapSelect, pressed)
						self._swapSelect = -1




	def render(self):
		global conf, fonts, images, colors	
		self.screen.fill((48,195,136))	
		if self._state == 'player1stack' or self._state == 'player1card' or self._state == 'player2stack':
			if self._state == 'player1stack':
		 		headingText = 'Your Move: Choose Between Deck and Pile'
			elif self._state == 'player1card':
				headingText = 'Click the card to remove'
			elif self._state == 'player2stack':
				headingText = 'Player 2\'s Turn'


			text(headingText, 'heading', 'white', conf['screenWidth'] // 2, 70, self.screen)
			
			self._player1.render(self.screen, self._eventHandler)
			self._player2.render(self.screen, self._eventHandler)

			deckX = conf['screenWidth'] - conf['imageWidth'] - 126
			pileX = 44
			y = 290

			if (self._state == 'player1card' or self._state == 'player1stack') and self._swapSelect != -1:
				if self._swapSelect < 9:
					swapCard = self._swapSelect + 1
				else:
					swapCard = chr(56 + self._swapSelect)
				swapText = fonts['player'].render('Press the key for the card you wish to swap number "'+str(swapCard)+'" with:', True, colors['white']) 
				swapTextRect = swapText.get_rect()  
				swapTextRect.center = (conf['screenWidth'] // 2, 480) 
				self.screen.blit(swapText, swapTextRect)			

			
			if len(self._pile) == 0:				
				self.screen.blit(images['none'], (pileX, y))
			else: 
				for i in range(len(self._pile)-1):
					self.screen.blit(images['back'], (pileX + i*7, y))

				lastPile = self._pile[len(self._pile) - 1]
				lastPileName = str(lastPile.getRank()) + lastPile.getSuit()
				pileImg = images[lastPileName]
				self.screen.blit(pileImg, (pileX + (len(self._pile)-1)*7 , y))			

			for i in range(len(self._deck)):
				self.screen.blit(images['back'], (deckX + 2*i, y))
			
		elif self._state == 'start':
			text('Indian', 'hero', 'white', conf['screenWidth'] // 2, conf['screenHeight']//2 - 100, self.screen)
			text('Rummy', 'hero', 'darkGreen', conf['screenWidth'] // 2, conf['screenHeight']//2, self.screen)
			
			pygame.draw.rect(self.screen, colors['white'],(conf['screenWidth']//2 - 200,conf['screenHeight'] - 200,180,60))
			text('GO', 'player', 'green', conf['screenWidth'] // 2 - 110, conf['screenHeight'] - 170, self.screen)

			pygame.draw.rect(self.screen, colors['darkGreen'],(conf['screenWidth']//2 + 20,conf['screenHeight'] - 200,180,60))
			text('Leaderboard', 'player', 'white', conf['screenWidth'] // 2 + 110, conf['screenHeight'] - 170, self.screen)
			
	
		elif self._state == 'player1win' or self._state == 'player2win':
			if self._state == 'player1win':
				text('You won!', 'heading', 'white', conf['screenWidth'] // 2, 400, self.screen)						
			else:
				text('Computer player won!', 'heading', 'white', conf['screenWidth'] // 2, 400, self.screen)						
			
			self._player1.render(self.screen)
			self._player2.render(self.screen)

			pygame.draw.rect(self.screen, colors['white'],(conf['screenWidth']//2 - 180, 440, 160, 60))
			pygame.draw.rect(self.screen, colors['darkGreen'],(conf['screenWidth']//2 + 20, 440, 160, 60))
			text('HOME', 'player', 'green', conf['screenWidth']//2 - 100, 470, self.screen)
			text('Analysis', 'player', 'white', conf['screenWidth']//2 + 100, 470, self.screen)
		
			
		elif self._state == 'leaderboard':
			headingText = fonts['heading'].render('LEADERBOARD', True, colors['white']) 			
			headingTextRect = headingText.get_rect()
			headingTextRect.center = (conf['screenWidth'] // 2, 75)
			self.screen.blit(headingText, headingTextRect)
			
			col1x, col2x, col3x, col4x = conf['screenWidth']//5, 2 * conf['screenWidth']//5, 3 * conf['screenWidth']//5, 4 * conf['screenWidth']//5
			y = 175

			if len(self._leader) == 0:
				text('No leaders yet.', 'heading', 'darkGreen', conf['screenWidth']//2, conf['screenHeight']//2 - 50, self.screen)
				text('Play and be the first one here!', 'heading', 'white', conf['screenWidth']//2, conf['screenHeight']//2 + 10, self.screen)
			else:
				text('Rank', 'player', 'darkGreen', col1x, y, self.screen)
				text('Name', 'player', 'darkGreen', col2x, y, self.screen)
				text('Time', 'player', 'darkGreen', col3x, y, self.screen)
				text('Report', 'player', 'darkGreen', col4x, y, self.screen)

			for i in range(len(self._leader)):
				l = self._leader[i]
				text(str(i+1), 'player', 'white', col1x, y + 65*i + 55, self.screen)
				if len(l.name) <= 32:
					text(l.name, 'player', 'white', col2x, y + 65*i + 55, self.screen)
				else:
					text(l.name[:30]+'...', 'player', 'white', col2x, y + 65*i + 55, self.screen)

				text(str(round(l.gameTime, 2)) + ' s', 'player', 'white', col3x, y + 65*i + 55, self.screen)
				pygame.draw.rect(self.screen, colors['darkGreen'],(col4x - 70, y + 65*i + 30 , 140, 50))
				text('Analysis', 'player', 'white', col4x, y + 65*i + 55, self.screen)


			pygame.draw.rect(self.screen, colors['darkGreen'],(conf['screenWidth']//2 - 90, conf['screenHeight'] - 120, 180, 60))
			homeText = fonts['player'].render('BACK', True, colors['white'])
			homeTextRect = homeText.get_rect()  
			homeTextRect.center = (conf['screenWidth'] // 2, conf['screenHeight'] - 90)
			self.screen.blit(homeText, homeTextRect)			
		elif self._state == 'nameInput':			
			text('Enter your name', 'heading', 'white', conf['screenWidth']//2, 200, self.screen)
			self.screen.blit(self._textBox.get_surface(), (conf['screenWidth']//2 - len(self._textBox.get_text())*8, conf['screenHeight']//2 - 100))



	def close(self):
		self._state = 'quit'

	def getState(self):
		return self._state



eventHandler = EventHandler()
game = Game(eventHandler)
music['bg'].set_volume(0.3)
music['bg'].play(-1)

while game.getState() != 'quit':
	game.update()
	game.render()	
	pygame.display.update()