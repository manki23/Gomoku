# Gomoku
*Summary: The goal of this project is to make an AI capable of beating human players
at Gomoku*

## Subject Requirements:
In the context of this projet:
- Gomoku will be played on a 19x19 Goban
- Number of stones is infinite
- We will consider an alignment of 5 or more to be a win.

## Mandatory additional rules:
### Capture
(As in the Ninuki-renju or Pente variants)
```
You can remove a pair of your opponent’s stones from the board by flanking them with your own stones.
This rule adds a win condition : If you manage to capture ten of your opponent’s stones, you win the game.
  =>  note that one can not move into a capture
```

### Game-ending capture
```
A player that manages to align five stones only wins if the opponent can not break this alignment by capturing a pair,
or if he has already lost four pairs and the opponent can capture one more, therefore winning by capture.
There is no need for the game to go on if there is no possibility of this happening.
```
### No double-threes
```
It is forbidden to play a move that introduces two free-three alignments,
which would guarantee a win by alignment.
  => It is important to note that it is not forbidden to introduce a
double-three by capturing a pair.
```
## Additional subject requirements
- Against your program mode
- Against another human player on the same computer (hotseat), but with a move suggestion feature.
- A timer that counts how much time your AI takes to find its next move. (should always be under 500ms)

***
***
***

## Possible Bonuses:
### Bonus: Define starting position
1. Standard
```
Free starting position
```
2. Pro
```
The first player's first stone must be placed in the center of the board.
The second player's first stone may be placed anywhere on the board.
The first player's second stone must be placed at least three intersections away from the first stone
(two empty intersections in between the two stones).
```
3. Long Pro
```
The first player's first stone must be placed in the center of the board.
The second player's first stone may be placed anywhere on the board.
The first player's second stone must be placed at least four intersections away from the first stone
(three empty intersections in between the two stones).
```
4. Swap
```
The tentative first player places three stones (two black, and one white) anywhere on the board.
The tentative second player then choses which color to play as.
Play proceeds from there as normal with white playing their second stone.
```
5. Swap2
```
The tentative first player places
three stones on the board, two black and one white.
The tentative second player then has three options:
1. They can chose to play as black
2. They can choose to play as white and place a second white stone
3. 0r they can place two more stones, one black and one white,
and pass the choice of which color to play back to the tentative first player.
```
### Bonus: Choose the game size
1. Default: 19x19
2. 15x15
3. Free m*n, k (with m*n the dimensions of the board (from 3 to 19) and k the number of stones to align (from 3 to 5)

### Bonus: Change the set of rules
1. Subject requirements
2. Freestyle
3. Renju
```
It is played on a 15x15 board, with the rules of three and three, four and four, and overlines applied to Black only.
```
4. Caro
```
In Caro, the winner must have an overline or an unbroken row of five stones that is not blocked at either end (overlines are immune to this rule). This makes the game more balanced and provides more power for White to defend.
```
5. Omok
```
Omok is similar to Freestyle gomoku; however, it is played on a 19×19 board and includes the rule of three and three.
```
6. Ninuki-renju
```
Also called Wu, Ninuki Renju is a variant which adds capturing to the game; A pair of stones of the same color may be captured by the opponent by means of custodial capture (sandwiching a line of two stones lengthwise). The winner is the player either to make a perfect five in a row, or to capture five pairs of the opponent's stones. It uses a 15x15 board and the rules of three and three and overlines. It also allows the game to continue after a player has formed a row of five stones if their opponent can capture a pair across the line.
```
7. Pente
```
Pente is related to Ninuki-Renju, and has the same custodial capture method, but is most often played on a 19x19 board and does not use the rules of three and three, four and four, or overlines.
```

### Reminder
#### The rule of three and three
```
The rule of three and three bans a move that simultaneously forms two open rows of three stones
(rows not blocked by an opponent's stone at either end).
```
#### The rule of four and four
```
The rule of four and four bans a move that simultaneously forms two rows of four stones (open or not).
```
#### Overlines
```
Overlines prevent a plaver from winning if thev form a line of 6 or more stones.
```
