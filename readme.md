<h1>Indian Rummy</h1>
The game is a unique version of Indian Rummy. The game has 2 players, each with a deck of 11 cards. The player who makes a specific combo of 10 cards first, wins the game.

<h2>Playing instructions</h2>
There are 2 stacks of cards: Deck and Pile. Deck contains down-facing random cards while the pile has up-facing cards which have been put by players’ stack into the pile after the player’s turn. Each player is dealt a stack with 11 random cards at start. When it’s their turn, the player must choose either the last up-facing pile card or the last down facing card from the deck. After doing so, they will now have 12 cards and the player must remove a card from their stack to get their cards back to 11. The said removed card will now become the last up-facing Pile card. The player must a specific combo of cards (described later) first to win. The second player is controlled by the computer. Once the deck is completely empty, all the cards from the pile are shuffled and added back to the deck.
<br><br>
Once the game loads, click on the “Go” button to start the game. Your must enter your name in the terminal and hit enter on the keyboard to start the game. 
<br><br>
When it’s your turn, select either the face-up Pile or face-down Deck by simply clicking on the respective stack. Now, click on the card you wish to remove from your stack. Once your turn is over, the computer will make the move and then, it’ll be your turn again. Cards can also be reordered: when it is your turn, press the keyboard button corresponding to the cards (displayed above each card) to swap 2 cards. The card number range from 1-9 for the first 9 cards and A, B, C for the 10th, 11th and 12th card respectively. 
For example, pressing 1 and 6 will swap the first and sixth card. Pressing 4 and B on the keyboard will swap card 4 and card 11
<br><br>
If either you or the computer has achieved the required combo of cards(described later), the player will automatically win (there’s no need to declare anything).
<br><br>

<h2>Winning Combos</h2>
A <b>Run</b> is a set of consecutive cards numbers of the same suit
Eg: A of hearts, 2 of Hearts, 3 of Hearts
9 of diamonds, 10 of diamonds, Jack of diamonds

A <b>Book</b> consists of cards of same number but different suits 
Eg: 3 of hearts, 3 spades and 3 of diamonds 

To win, the player must have a 
Run of 4 cards OR A book of 4 cards 
AND additionally 
(A book or 3 cards and a run of 3 cards) OR (2 Runs of 3 cards)

<h2>Extra features </h2>

<h3>Leaderboard</h3>
The top 7 players, sorted by the amount of time used to win the game, will be displayed on the leaderboard. Only players who have won will be up on the leaderboard. Additionally, the player must also be in the top 7 players to be up on the leaderboard. 

<h3>Analysis</h3>
After every game, the player can see a detailed analysis of the game by clicking on the “Analysis” button after the game is over. The analysis is an auto generated PDF that may be used by the player to analyze their moves to improve their performance in the game. The report also includes graphic analysis (using pylab). Additionally, the leaderboard players can also see their analysis anytime by going to the leaderboard and clicking on “Analysis” button next to their name on the leaderboard. The analysis PDF can be saved by the user for future reference. 

<h2>Dependancies</h2>

<h4>PRE-INSTALLED / Python Standard Library</h4>
1. <code>os</code><br>
2. <code>time</code><br>
3. <code>random</code><br>
4. <code>platform</code><br>
5. <code>pickle</code><br>
6. <code>copy</code><br>
7. <code>subprocess</code><br>

<h4>EXTERNAL / Need to be installed</h4>
1. PyGame
2. FPDF
3. Numpy
4. PyLab

<h2>Installation and Running the Game</h2>
1. Install the above mentioned dependencies <br>
2. Clone the Github repo or download the repo as .ZIP and extract it at a location for which you have Read and Write permissions<br>
3. Run the game with python3 by running the game.py file (<code>python3 game.py</code>)<br>
