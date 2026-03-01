
# Simplifying Go Rules Even Further

<!-- ---
title: "Simplifying Go Rules Even Further"
date: 2020-02-18T19:03:00-05:00
draft: false
toc: false
images:
tags:
  - games
  - go
--- -->

The ["Logical Rules"](https://tromp.github.io/go.html) of the game Go were produced by Tromp and Taylor: They distill the rules of the game into 10 short but mathematically precise sentences. The wording of these rules was intended to be "as simple and elegant as possible", and they do a good job of it:

## The Tromp-Taylor Logical Rules

01. Go is played on a 19x19 square grid of points, by two players called Black and White.
02. Each point on the grid may be colored black, white or empty.
03. A point P, not colored C, is said to *reach* C, if there is a path of (vertically or horizontally) adjacent points of P's color from P to a point of color C.
04. *Clearing* a color is the process of emptying all points of that color that don't reach empty.
05. Starting with an empty grid, the players alternate turns, starting with Black.
06. A turn is either a pass; or a move that doesn't repeat an earlier grid coloring.
07. A move consists of coloring an empty point one's own color; then clearing the opponent color, and then clearing one's own color.
08. The game ends after two consecutive passes.
09. A player's score is the number of points of her color, plus the number of empty points that reach only her color.
10. The player with the higher score at the end of the game is the winner. Equal scores result in a tie.

After seeing this formulation of the rules, I began to believe that the popularity and endurance of Go through the ages might have a lot to do with the way that it evolves complex strategy from very simple rules. Indeed, I think it would be challenging to design a game as strategically rich as Go with rules as succinct as the Tromp-Taylor rules. I wondered if there might be a way to simplify the Go rules further, potentially modifying the game, but ultimately producing a game which was just as complex.

## Modified Logical Rules of Pseudo-Go

Here's what I came up with:

01. Go is played on a 19x19 square grid of points, by two players called Black and White.
02. Each point on the grid may be colored black, white or empty.
03. A point P, not colored C, is said to *reach* C, if there is a path of (vertically or horizontally) adjacent points of P's color from P to a point of color C.
04. *Clearing* a color is the process of emptying all points of that color that don't reach empty.
05. Starting with an empty grid, the players alternate turns, starting with Black.
06. A turn is ~~either a pass; or~~ a move that doesn't repeat an earlier grid coloring.
07. A move consists of coloring an empty point one's own color; then clearing the opponent color, and then clearing one's own color.
08. The game ends **when the player on turn has no legal moves. That player loses.** ~~after two consecutive passes.~~
09. ~~A player's score is the number of points of her color, plus the number of empty points that reach only her color.~~
10. ~~The player with the higher score at the end of the game is the winner. Equal scores result in a tie.~~

That's it! Essentially all I have done is to disallow passing the turn, and instead of relying on the usual scoring, I rely on the ko rule to end the game. I think this concept of the game ending when the player to move has no legal moves is pretty common in combinatorial game theory. It has the benefit that the usual recursive definition of the evaluation of a position holds for terminal game states.

Despite the differences from real Go, I believe my version is, strategically, a very similar game: One player's ability to beat another in my game should be largely dependent on their relative skill at traditional Go. Here is my mental model for how a game of pseudo-Go would play out:

1. The two players would first play an essentially regular game of Go, reaching the point where the game would usually end, with most territory surrounded by one player or the other.
2. At this point, the players would have no choice but to continue playing stones. They would play stones in their opponent's territory to waste time, until the only empty points left would be singletons.
3. Since the "positional superko" rule (note the Tromp-Taylor rules distinction from normal ko) prevents playing single-stone suicides, players would then be forced to start filling in their own eyes.
4. Eventually, one player (likely the player with less territory at the end of step 1, the player who, as we shall see, is destined to lose) would be forced to fill in one of the last eyes of one of their groups.
5. The winning player may now capture that group. Both players now scramble for territory in the empty space left, but since the stones surrounding the space are the winning player's, the winning player should come out ahead in this step in terms of territory.
6. Steps 2-5 are repeated until the losing player runs out of groups to sacrifice. Eventually we reach a board state where all the stones that remain are the winning player's and the only empty spaces for the loser are eyes of living groups. Since any move now is a suicide, which is disallowed by the ko rule, the game finishes.

There are a few key differences from traditional Go: It is better strategically for two large chains to be connected, even if they are alive individually, since connecting them gives an additional space to be filled during step 3. There is also the "endgame" phase from step 2, where there may be some strategic ways to play in your opponent's territory to force them to fill their territory in a way that gives them fewer eyes moving in to phase 3. Ultimately, I think this endgame phase only makes the game richer. I don't think that it really changes the strategy of the regular game much, since creating territory you have good control over is the key there, just as in normal Go.

One of the downsides of this system of rules is that the game is decided long before it actually ends: One should be able to predict the winner at the end of step 1 fairly easily, but if the game is to be played to completion, you still have a long way to go from that point. In polite company, this can be resolved by [game-agnostic meta-rules](./game-agnostic-meta-rules.md) such as allowing the loser to concede or introducing a doubling cube, but in some contexts it could cause problems. Another downside is that since the notion of points has been done away with, there can now be no notion of "komi" which is one way to introduce a handicap into the game. However, it is still possible to handicap by giving the weaker player by changing the starting position, as in traditional Go. Interestingly, instead of "points" being the natural heuristic for how well one is doing, this might change to "eyes" (e.g. "How many eyes can I get out of this territory, and to what extent can I prevent my opponent from creating more eyes?").
