# The Last Few Seconds of the 2022 Speed Chess Championship

*This is a post I wrote around two weeks after the match happened, but never got around to posting.
I found it again recently and am putting it out now.*

Hikaru Nakamura beat Magnus Carlsen in the 2022 Speed Chess championship recently.
You can see the final few seconds of the match [here](https://youtu.be/djyXtbyi03I?t=14561).

Notice I didn't say "final minute".
Although Magnus wins the last game, Hikaru had "won" the match around 45 seconds beforehand.

## How did Hikaru win, even though he lost the last game?

This is because of the rules of the tournament: The match clock in the upper corner indicates the time remaining before no new games can be started.
Magnus is two points behind, so he must not only win this game, he must do so before the timer runs out in order to get a chance in a final game to send the match to a tiebreak.
If the game ends after the timer runs out, even if Magnus wins, the match will end with Hikaru up one point.

In the final seconds, Hikaru knows his position is losing, but each additional move he plays adds a second to his own clock, and the match timer continues to tick down even on Magnus's time.
If he can get his own game clock above the match clock, he can just wait out the rest of the game and lose on time after the match is officially over.

## Some puzzles

Here is the position where Hikaru realizes the match timer has about 1.5 more seconds on it than his clock and declares victory:

![](https://www.chess.com/dynboard?fen=2Q2K2/5R2/8/8/1Q6/8/1kr5/8%20b%20-%20-%202%2075&board=brown&piece=classic&size=3)

Imagine instead that when Hikaru checked his clock here, he had found that the match timer was not yet above his clock.

Could he have won the match?
The answer might depend on a number of factors, like the reaction times of the players and the potential use of the [premove](https://www.chess.com/terms/premove-chess) mechanic.

Like Hikaru, you only have 40 seconds to strategize.

### Warm-up

Suppose Hikaru's clock precedes the match clock by 0.5 seconds.
How can Hikaru guarantee the win?

<details>
<summary>Answer</summary>

If Hikaru has less than a second to burn, then the play to win the match would be 75. ... Ka1. This is the only move which doesn't result in mate in 1, [as analysis shows](https://www.chess.com/analysis/game/master/16347469/analysis?move=148). After playing this move, he would have an additional second on his clock, and therefore would be able to wait out the match clock.
</details>

### Puzzle

Suppose Hikaru's clock precedes the match clock by 1.5 seconds.
Suppose Magnus's speed-chess abilities allow him to decide to optionally make a premove before each of Hikaru's moves, and if he doesn't take a premove (or if his premove is cancelled as illegal) to make a regular move in 1 second.
What is Hikaru's best strategy?

<details>
<summary>Answer</summary>
  
Let's enumerate cases for possible premoved mate sequences:

1. Hikaru moves, Magnus does not premove (mate) -> Magnus wins game before match is over
2. Hikaru moves, Magnus successfully premoves (mate) -> Magnus wins game before match is over
3. Hikaru moves, Magnus does not premove (not mate), -> Hikaru has a 0.5 advantage on the clock and wins the tournament
4. Hikaru moves, Magnus successfully premoves (not mate), 
   1. Hikaru moves, Magnus does not premove (mate) -> Magnus wins game before match is over
   2. Hikaru moves, Magnus successfully premoves (mate) -> Magnus wins game before match is over
   3. Hikaru moves, Magnus does not premove (not mate), -> Hikaru has a 1.5 advantage on the clock and wins the tournament
   4. Hikaru moves, Magnus successfully premoves (not mate), -> Hikaru has a 0.5 advantage on the clock and wins the tournament
    
So Hikaru is looking to either have Magnus fail the first premove without mating, or survive his second move without mate-in-1 for Magnus on the board.

Hikaru's three legal moves are Ka1, Ka2, Kc1. We note that

* If Magnus doesn't premove, Magnus will be able to quickly mate in 1 only if Hikaru plays Ka2 or Kc1 (by playing Qa6 or Rf1 resp.)
* In fact, a premoved Qa6-Rf1 will result in a fast win for Magnus, but only if Hikaru plays Ka1 or Ka2
* Additionally, a premoved Rf1-Qa6 will result in a fast win for Magnus only if Hikaru plays Ka1 or Kc1
* There is no premove from Magnus that wins in all three cases.

We therefore have the following optimal strategies: Hikaru should play a move at random, and Magnus should decide between Qa6, Rf1, or waiting. Hikaru has a 1/3 chance of winning.
  
</details>

## Why is this interesting?

I think this is interesting because it's a clear example of "[metagame](https://en.wikipedia.org/wiki/Metagame)": Due to the tournament rules, the optimal thing to do requires using reasoning that a conventional chess engine wouldn't be capable of.
Indeed it requires mixing, which is a strategy class that would usually not be optimal in chess, or any perfect-information deterministic strategy game.

I'd be interested to hear from reader in the comments about other potential examples of more-complex metagame strategies evolving out of simple in-game rules.
