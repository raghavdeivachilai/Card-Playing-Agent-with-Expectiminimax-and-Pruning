# Card Playing Agent with Expectiminimax and Pruning:

I programmed an agent to play trick taking games such as Hearts,
Spades, and Bridge. I have used a game engine to run the program and compete with other players.

## Simple Trick Taking Game :
This game is played with 4 players and a standard 52 card deck. There are four ​ suits ​ , Spades ♠,
Hearts ​ ♥ ​ , Diamonds ​ ♦ ​ , and Clubs ♣. Each suit has 13 cards with ​ ranks ​ 2, 3, 4, 5, 6, 7, 8, 9, 10, J
(Jack), Q (Queen), K (King), and A (Ace), with 2 being the lowest rank and A being the highest.
To begin, deal 13 cards to each player. The player to the left of the dealer will place any card
from their hand face up on the table. This player is the ​ lead ​ .
Play continues clockwise with each player selecting a card from their hand to play. If a player
can play a card that matches the suit of the lead, they must. Otherwise, they may play any card
from their hand that they wish. This is called ​ discarding ​ . Play stops when all four players have
played a card, completing the ​ trick.
The winner of the trick is the player who played the highest ranked card that matches the lead
suit. They collect the trick and keep the cards face down in front of them. This player then
becomes the new lead and selects a card to begin the next trick.
Once all 13 tricks have been played. Players count one point for each trick they won to get their
score. These scores carry over to the next hand and the players keep playing hands until one
player scores 100 points. At this point the player with the most points wins.

## Approach:
We started thinking in terms of the different positions our agent would play and apply techniques which wouldhelp our agent in choosing the optimal card to play for that position. Considering the large possibilities our agent needs to encounter when it plays first or second, Reinforcement Learning was our firsthand choice, but it did not work out well and our agent was extremely slow in performance. We then shifted to an Expectiminimax approach which would also be favorable in this position. However, we soon realized that our agent could take a lot of time trying to compute the next best possible move considering the search space. To overcome this challenge and to make our agent significantly faster, we have reduced the lookahead only to the next card and have used heuristic pruning to prune the tree according to the suite and by comparing the highest card in that suite with the cards we have. This enabled us to reduce the search space and choose the optimum card to play in a quick time. When our agent plays third or fourth, we went with a rule-based approach instead of continuing with the Expectiminimax as the future possibilities are less and we can be sure of a card to play. Our rule-based system keeps track of the cards that the opponents have already played and plays the game accordingly.


