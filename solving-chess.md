
<!-- 
title: "Solving Chess"
creation date: 2021-01-18T15:12:27-08:00
-->

# Solving Chess

https://x.com/Kasparov63/status/2022016470826545287?s=20

Chess has a [game tree size](https://en.wikipedia.org/wiki/Game_complexity#Complexities_of_some_well-known_games) of about `10^123`, so it will never be possible to solve chess by brute force search of the game tree. Could we use cleverer techniques to obtain an [ultra-weak solution](https://en.wikipedia.org/wiki/Solved_game#Ultra-weak_solution) (i.e. simply prove what the result is with perfect play)?

https://manifold.markets/IsaacKing/will-chess-be-solved-by-2040

Since the [consensus](https://chess.stackexchange.com/questions/12470/if-there-was-perfect-play-from-both-sides-will-it-be-draw-or-win-for-one) seems to be that chess is a draw with perfect play, let's assume that this is the case and think about how we might go about proving the game is a draw for black.

## Preliminaries

Clearly we will not be able to use a conventional chess engine directly to solve the problem. However, evaluations of particular positions by such engines, or something like them, could prove useful indirectly.

I use here the example of Stockfish evaluated with a [node count](https://official-stockfish.github.io/docs/stockfish-wiki/UCI-&-Commands.html#nodes-x) of 10 million (henceforth `Stockfish(node=1e7)`) as a deterministic, reasonably fast, often accurate assessment of a position. Of course, one could choose a different depth, or a different engine, such as the NNUE style engines that are in vogue these days. Perhaps even an engine that has been engineered to make it easier to prove the specific guarantees we want to prove (some useful properties could be: An engine that always explores nodes following captures, or always explores all nodes that would have been explored in previous positions), or with a heuristic fine-tuned to the type of position we expect to be most critical.

## Limiting the search space

### There are fewer FEN-notatable positions than there are games

A first thing to note is that while there may be `10^123` different chess games, there will be far fewer chess *positions*. The [Forsyth-Edwards-Notation](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation) accounts for everything that could be relevant to strategy at a particular point in a chess game in 5 fields (technically there is also a 6th "whole move clock" field which is irrelevant to strategy):

* The configuration of the board, indicating for each of the 64 squares which color and type of piece occupies it, or if it is empty. If you had an unlimited supply of each of the 6 types of pieces of both colors, you would have `(1 + 2 * 6)^64 = 13^64` ways of placing them on the squares, each of which would be notatable.
* Which of the two (`2`) players has the turn.
* For each of the four starting squares for rooks, whether there is a rook there that can castle. There are `2^4` values this field can take
* En passant rights. There are 16 squares on which an en passant capture can take place, and en passant is sometimes not allowed, leading to `17` values
* "Half-move clock". A number below `100` indicating how many ply have elapsed since the last capture or pawn move, which is necessary for enforcing the 50-move rule.

This accounting gives `13^64 * 2 * 2^4 * 17 * 100 < 1.067 * 10^76` FEN notation values.

### There are fewer legal positions than there are FEN-notatable positions

Of course, not every FEN notation makes sense as a legal position that a chess engine could analyze:

* There must be exactly one location with a white king and one other location with a black king. This on its own reduces the `13^64` board states to `64 * 63 * 11^62`.
* It does not make sense to have available castling rights if the corresponding king and rook do not occupy their starting squares.
* It does not make sense to have en passant capture available if there is no pawn in front of the square that such a capture would remove.
* Pawns cannot occupy the first or eighth ranks.

An AI-coded python script tells me that these factors reduce the count to below `3.247 * 10^*69`. There are also further restrictions that are harder to enumerate, such as:

* Kings cannot be on adjacent squares. More generally, the player who has just moved cannot be in check.

### There are fewer legally-reachable positions than legal positions

Even if a position is technically analyzable by a chess engine, this doesn't necessarily mean it can be reached in a legally-played game:

* There can be at most 15 non-king pieces of each color on the board at a time.
* For each piece type and color, there cannot be more "excess pieces" of that type than is possible when accounting for starting piece counts and pawn promotion.
  * Similarly with bishops and the color of the square they occupy.
  * More precisely, 
    * each player starts with 
      * one queen,
      * one light-square bishop,
      * one dark-square bishop,
      * two knights,
      * two rooks.
    * The only way to increase any of these counts is to promote.
    * So if we take the "excess piece count" of any piece type/color combo to be the number of additional pieces of that type/color above the starting amount, the total of the excess piece counts of a color must not be more than the number of missing pawns of that color.
* It does not make sense to have en passant available if the last move could not have been a pawn move through that square (i.e. there must be a pawn in front of the square and also the square itself and the square behind should be empty.).

Even the above logic does not account for every type of position that cannot be legally reached. For example, one can imagine a position with a white bishop on c1, pawns on b2 and d2, and rooks on a1 and b2.

![example board, FEN: rnbqkbpr/pppppppp/8/8/8/8/PPPPPPPP/RRBQKBNN](https://chessboardimage.com/rnbqkbprpppppppp8888PPPPPPPPRRBQKBNN.png)

The pawns cannot have moved since they are on their starting squares, and therefore the bishop cannot have moved either. But given this, there is no way for two rooks to be on a1 and b1, since to get to these squares, they would have had to have moved through a piece of the same color. Determining whether a particular position can be legally reached is apparently [hard](https://drops.dagstuhl.de/storage/00lipics/lipics-vol181-isaac2020/LIPIcs.ISAAC.2020.17/LIPIcs.ISAAC.2020.17.pdf), at least on large chessboards. 

Of course, if you are willing to program some high-level rules and solve edge cases by hand (perhaps you are a fan of Raymond Smullyan's puzzles) you can estimate the number of legally reachable positions statistically. A prior [analysis](https://github.com/tromp/ChessPositionRanking) along these lines found that there were less than `5 * 10^44` legally reachable positions.

### There are fewer sensible positions than positions that are legally reachable

Even having ruled out the above, many remaining positions involve weird configurations of pieces that you would never see in a game of chess played even remotely rationally.

Here are three pictures of boards from games played on [lichess](https://lichess.org/), and three pictures of boards generated by random moves. 

| Board Pair 1: Which is the real game? | Board Pair 2 : Which is the real game? | Board Pair 3 : Which is the real game? |
| ------------------------------------- | -------------------------------------- | -------------------------------------- |
| ![real board FEN: 2kr1bnr/1pp2ppp/p1pqb3/4p3/2N1P3/5N2/PPPPQPPP/R1B2RK1 b - - 7 8](https://chessboardimage.com/2kr1bnr1pp2pppp1pqb34p32N1P35N2PPPPQPPPR1B2RK1.png) | ![real board FEN: r1b1kb1r/p3pppp/1pn1qn2/2p3N1/8/3PB1P1/PPP1QP1P/RN2KB1R b KQkq - 1 8](https://chessboardimage.com/r1b1kb1rp3pppp1pn1qn22p3N183PB1P1PPP1QP1PRN2KB1R.png) | ![randomboard3](https://chessboardimage.com/rnb1k1nrp1qp3p2p4b1p2Ppp1P1P3P14PP21P2Q2PRNB1KBNR.png) |
| ![randomboard1](https://chessboardimage.com/1nbqkbnr2pppp28Qp1Pr1Bp87NPPP1PPPPRN2KB1R.png) | ![randomboard2](https://chessboardimage.com/rnbqkbr1p2p1pp12p3Nn1p2p34P1PpP4P21PPPB2PRNBQK2R.png) | ![real board FEN: rnbq1rk1/ppp1b1pp/4pn2/3p1p2/2PP1B2/6PN/PPQ1PPBP/RN3RK1 b - - 7 8](https://chessboardimage.com/rnbq1rk1ppp1b1pp4pn23p1p22PP1B26PNPPQ1PPBPRN3RK1.png) |

If you're an experienced player, you can probably spot the odd ones out pretty easily: Why would white develop their queen this way? Why are so many pieces hanging? This illustrates that an important tool in solving chess is identifying which positions are even possible to occur in a game of perfect chess.

Technically, we are proving that Black can draw the game with perfect play. So even if our proof was going to take the form of a list of positions that black could stay in to force a draw, we do not have to consider any position that can only arise from black making at least one suboptimal move. One could hope that in addition to black being able to draw, black is able to draw without allowing either player to promote more than 2 pawns over the course of the game, or at least without allowing any player to accumulate an "excess piece count" of more than 2.

Still, the assumption means this is not a *proof* about the number of positions we need to consider (technically, even if we knew how many positions we needed to consider in theory, we still might have to consider more positions if we didn't know which positions those were). In lieu of a proof, here is a market about the total:

https://manifold.markets/BoltonBailey/size-of-the-smallest-number-of-posi-2n5yN9hI26

If we wanted a near-term rough upper bound, we could do some statistics to take advantage of an assumption that: What fraction of possible positions admit an incoming trajectory where `Stockfish(node=1e7)` never makes a move as black it judges to be in the worst 3 moves / a blunder of more than 4 points.

<!-- 
For reference, [Claude says of checkers](https://claude.ai/chat/e751b684-ce5a-43f3-8333-8293042497cd):

When Jonathan Schaeffer and his team at the University of Alberta solved checkers in 2007, they determined:

5 × 10²⁰ — the approximate number of positions in the search space
~3.9 × 10¹³ (39 trillion) — the number of positions they actually had to solve to prove the game is a draw with perfect play

 -->

## Approaches for avoiding brute-force DAG-search

The previous section discusses the size of the DAG that would be needed to prove a win/draw for black. But perhaps it is possible to use general reasoning to eliminate large parts of this DAG at once.

### Accuracy of strong advantage evaluations by `Stockfish(node=1e7)`

Here's a hypothesis that, if provable, could be substantially helpful for a chess solution.

> If `Stockfish(node=1e7)` evaluates a position at a score of -10 or lower, then such a position is always at least a draw for black with perfect play.

The primary benefit of being able to assume such statements would be that in the brute-force phase, we can immediately discount sequences of very bad moves by white without following them to their conclusion, by simply evaluating them heuristically.

#### Is this even true?

I'm not certain. There are cases of positions that trick weak chess engines, but as far as I can tell, these usually have to do with making the engine carry out an unfavorable pawn break in a close to equal position. 10^45 is a big number though, and so there is perhaps room for some kind of incomprehensible adversarial example.

On the other hand, 10 points is such a strong advantage that it feels like this might be intuitively true. [This](https://www.melonimarco.it/en/2021/03/08/Stockfish-and-lc0-test-at-different-number-of-nodes/) page shows a chart which suggests that strength somehow levels out at very high node counts, and makes me wonder if Stockfish might not be perfect with a few more OOMs of compute.

Even if there is some extremely strange edge case that causes this proposition to fail, perhaps it would succeed for a version of Stockfish fine-tuned to play very conservatively with an advantage, or for a version of Stockfish programmed with a specific set of exceptions.

#### How could we find out if its true?

Consider chess positions in terms of two variables:

* Total material of both players, as a proxy for the stage of the game (78 possible values).
* The `Stockfish(node=1e7)` score discretized to the nearest 0.1, clipped to +-15.0.

These variables partition all chess positions into one of ~24,000 buckets. 
The fraction/number of positions in each bin should be estimable by statistics.
One might compute the dynamics of a game with respect to these buckets by

* selecting random positions
* If white is to move, choosing the next position by the `Stockfish(node=1e10)` best line
* If black is to move, choosing the next position by the `Stockfish(node=1e7)` best line

You can then compute the transition probability matrix between buckets, and create a Markov chain. This allows you to estimate the fraction of positions in a particular bucket that result in a win for white (where black is `Stockfish(node=1e7)` skill and white is `Stockfish(node=1e10)`). We can then increase `k` and try to extrapolate out points where the expected probability of losing is less than the reciprocal of the number of games in the bucket.

<!-- TODO code this -->

#### How could we prove a statement like this true

Here's a followup with more carefully constructed collection of statements, each of which implies the one before it, so that the provability of our first statmeent is reduced to the provabilty of the last

1. If `Stockfish(node=1e7)` evaluates a position at a score of -10 or lower, then such a position is always at least a draw for black with perfect play.
2. consider the position evaluation function along the lines of "depth 20 Stockfish", but with a +0.1 point penalty for every point of material white has remaining, and the claim that if this evaluation function gives a -6 score or lower for black, then black wins or draws with perfect play. 
3. Equivalently, if `Stockfish(n=1e7)+0.1*white_material < -6.0`, then black has some play that can reach another position where this condition holds.

The plausibility of statements 2 and 3 depends on the fact that in the normal course of playing sensible Stockfish moves, black will be able to capture white's pieces, and thereby get a better score, even if white is selecting perfect moves.

The idea now is to prove statement 3 by casework: If statement 3 were false, there would necessarily be some position which Stockfish evaluated as a substantial advantage, but which when Stockfish is evaluated on child positions, found the advantage was less, presumably due to some capture or tactic.

We could then try to do AI powered analysis of possibilities for this part of the game tree that the Stockfish instance considers: 

* What are the components of the heuristic that caused black to have such a high score.
* What tactic happened that the score went down so much? What piece was captured where, and by what?
* What could have been done to avoid this? Why was that option not minimax?

The casework might be substantial, but the point is that if this can be done for less than the cost of the main brute-force search, then it can save on the cost of compute.

<!-- A trick might be to work our way down to 10 from some higher number as an intermediate result, or from other specially trained evaluation functions -->

### Method of comparison

The [method of comparison](https://chessentials.com/how-to-use-chess-engines-the-method-of-comparison/) is a technique that human chess players employ. The idea is to consider the difference between two similar moves when evaluating the game tree, and consider points at which it will later become better to have made one move over the other.

Chess engines seem not to use this method, but it could have useful applications to solving chess. 

Suppose I need to prove a particular move in a particular chess position is suboptimal. I might do this by replacing the chess position with a position in a different game, which I might call "comparison chess".

- In comparison chess, the "board" consists of two chess boards/gamestates
- To compare two moves in a chess position, start these boards with the position after the two moves.
- I play the position I think is better of the two on the board where that move was made. On the other board, I play the other color.
- At any time, if it is my turn on one of the boards, I can play a move on that board. I can also choose to make my opponent move on a board where it's their turn.
- I can win by:
  - Winning on either board.
  - Drawing on both boards.
  - Reaching the same chess-subgame state on both boards (if I reach such a position, I can win by strategy-stealing, but this rule allows me to short circuit)

The point being that a double chess game being a win for me is logically equivalent to my preferred move on the regular chess board being at least as good as my dispreferred move. But it is easier to prove a win in comparison chess by the short-circuit rule.

There are a few ways we could integrate this into our analysis.

* It could be directly used during the brute-force search phase to rule out moves by white.
* If the "Accuracy of strong advantage evaluations" doesn't work well for regular chess, perhaps it can be proved to work well for comparison chess, by virtue of being able to train a heuristic that values keeping positions on the two boards very similar. If so, perhaps it can be used as a fast way of ruling out extremely bad moves to prune the search space of the `Stockfish(node=1e7)`.

This game may take longer, but perhaps that is offset by

- I have the benefit of being able to partially copy opponent's moves.
- At any time I can switch to focusing on one board.
- I can win by reaching the same board state (transposing)
- It is easier to assess positions in this game because I can do close comparisons.

<!-- 
### Oracles for broad classes of positions

In order to solve chess we will have to develop some computational notions of which positions are draws and which are losses. Chess engines do this, but the key difference here is that an engine can rely on heuristics that are sometimes inaccurate, while a program to formally solve chess will need to be much more precise about which positions it evaluates as wins, draws or losses, and which positions it cannot properly evaluate without more computational power than it has. Taking this into account, consider the problem of making an *incomplete chess oracle*: A program that takes a chess position and returns "Black wins or Draws" in some (but not necessarily all) positions where this is the case, and returns "Unknown" otherwise.

An endgame tablebase is an example of an incomplete chess oracle: It returns the result of endgames, and is agnostic about positions outside of its tablebase. Another example would be a chess engine which only returns an answer if it finds a forced mate or draw.

We can ask what the most effective incomplete chess oracle under constraints:

* The program must run in under 1 second on a laptop (or some formal model of a computing system with about this much power).
* The program must minimize the number of [realistically reachable chess positions](#weak-solution) for which it returns "Unknown".

Since this optimization question ranges over all algorithms, it is impossible to know exactly what the solution is. I would conjecture however, that the answer looks something like the following:

*Run `Stockfish(time=0.99s)`, then return "Black Wins or Draws" if the score is at least -7.0 in Black's favor. Build a list of positions for which this result is incorrect, and use the remaining time to check that the given position is not in that list before returning.* 
-->



## Final Thoughts

* Consider the chess variant where:
  * Ranging pieces can jump over or capture pieces of the same color as themselves
  * There is no concept of stalemate or "check": the king is just a piece that can be captured, first player to lose their king loses.
  * This variant seems to have the property that it is straightforward to prove by induction that it is better to have a piece than not. Does this make it easier to analyze by comparison?
* Can we identify any concrete examples of grandmaster/engine play where the player selects a move provably suboptimal by the method of comparison?