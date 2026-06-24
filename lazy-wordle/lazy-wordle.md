# Lazy Wordle

[Many](https://jonathanolson.net/experiments/optimal-wordle-solutions) have [done](https://rimonim.github.io/blog/wordle/) computational [analyses](https://www.youtube.com/watch?v=v68zYyaEmEA) of [Wordle](https://www.nytimes.com/games/wordle/index.html) and optimal ways to [play](https://tomjohnston.co.uk/blog/2022-02-07-optimal-wordle-strategies.html) it.^[I also like [this video about compression of the word list](https://www.youtube.com/watch?v=JYN25TeM5kI)]

But most such analyses aren't oriented towards helping humans play and win.

## TL;DR

Use these five words as your first guesses

'crine', 'devel', 'faugh', 'spalt', 'womby'

Then find an answer consistent with the information you gain from these guesses.
You will have about a 99.2% chance to win.^[Technically there is a wrinkle here: You might have narrowed down to a single wordle-answer-legal possibility, but the set of allowed wordle guesses is larger than the set of allowed answers.
If you guess consistent letter sequences at random, you might accidentally hit a word on the guess-list but not the solution list.
For simplicity I will discount this possibility, and assume that you are smart enough to consider solutions in your head and judge which are "normal" enough to be on the solution list.]

## My goal

I am interested in extremely-simple-to-memorize strategies that help me win.
If I'm only interested in winning (rather than winning in minimal guesses or making all my guesses consistent) then my strategy boils down to choosing an five guesses that maximize the chance I get my sixth and final guess right.
This strategy could be dynamic, but to be simple as possible, it ideally wouldn't be.

This leads directly to the following **Question**:

> Does there exist a set of five initial wordle guesses such that I can always tell what the solution will be from the information those guesses?

Examining the logical structure of this question, we can rephrase it as:

> Does there exist a set of five initial wordle guesses such that for any true solution and any other false solution, at least one of the five guesses provides information that distinguishes the true solution from the false solution?

What we have here is an instance of the [set cover problem](https://en.wikipedia.org/wiki/Set_cover_problem).
I have \~10000 words on the guess list and each of these corresponds to a subset of the universe of \~5000000 pairs of words from the answer list.

The set cover problem is [infamously](https://en.wikipedia.org/wiki/Karp%27s_21_NP-complete_problems) NP-Hard.
Still, there are approaches we might take to optimizing our set the best we can.

## Greedy

One strategy for obtaining a good set of five guesses is greedy optimization: We find the word that distinguishes the most pairs, then the word that distinguishes the most pairs that remain, et cetera.
This gives us

'roate', 'linds', 'bumph', 'gawcy', 'fleek'

which distinguishes all but 42 pairs, for a 98.2% chance of victory.

## Reweighted greedy

Next I tried dynamic reweighting.
This starts with greedy optimization, but after a set of 5 words is derived, I upweighted all pairs that weren't distinguished and downweighted all pairs that were.
The hope with this approach is that easily distinguishable pairs will be consistently covered and get downweighted so that the greedy algorithm focuses on choices that distinguish difficult pairs.

The best I got out of this approach was

'vampy', 'whift', 'rungs', 'adobo', 'creel'

which distinguishes all but 23 pairs, for a 99.0% chance of victory

## Beam Search

Next I tried [beam search](https://en.wikipedia.org/wiki/Beam_search) with wider and wider beam widths.
The last few rounds went as:

```
width   512: explored     2,049 states | best leaves   21 pairs | ['bever', 'corse', 'daint', 'fugly', 'whomp'] *new best*
width  1024: explored     4,097 states | best leaves   18 pairs | ['crine', 'devel', 'faugh', 'spalt', 'womby'] *new best*
width  2048: explored     8,193 states | best leaves   18 pairs | ['crine', 'devel', 'faugh', 'spalt', 'womby']
```

Does the fact that going from 1024 to 2048 didn't change the best answer mean that this is likely optimal?
Hard to say, but this is the best I was able to find before my computer program crashed.

## [LP relaxation](https://en.wikipedia.org/wiki/Linear_programming_relaxation)

One trick we can do to approximate a solution is LP relaxation.
Instead of every word either being in or out of the list, we allow a guess to be "fractionally" in the list and then say that pairs are covered if the sum of the weights of the words that distinguish them is at least 1.

This actually seems more useful for getting lower bounds on the number of exceptions than upper bounds.
The optimum is 4.9119 fractional words to distinguish all pairs, which doesn't quite let us prove that it's impossible to distinguish every pair with five guesses.
But we can use the weights to refine our reasoning: We can do casework on the high-weight words and rule them out by doing LPs with those words with their weight pinned to 1 and seeing that the result requires total weight over 5.0.
We can repeatedly rule out words in this way, until we establish that no 5 words sequence can distinguish all pairs.

In fact, this works after only several rule-outs, so we can answer our question above in the negative.

## Cutting plane methods

The "casework on the high-weight words" strategy is a kind of ["cutting plane method"](https://en.wikipedia.org/wiki/Cutting-plane_method), so named because it's as if I am cutting through the 10000 dimensional hypercube of possible solutions with a pair of planes separating the solutions that include a word from the solutions that don't.

We can extend out approach to rule out solutions with k undistinguished pairs for low k by adding a slack parameter to our relaxed LP which adds a total of k weight to arbitrary solutions, and then using cutting plane methods to prove the resulting progam infeasible.
I was able to use this rule out solution with 4 exceptions, but it seems like it gets harder as we push it further.

## Summary and Future Work

So we have a lower bound of 4 and an upper bound of 18.
I'd be interested to know if anyone else can push either of these bounds, perhaps a good next approaches could be to combine the beam search and reweighting approches, or maybe rig an industrial solver to attack the problem.
I'd also be interested in dynamic strategies that get to 100% winrate but are still pretty simple, maybe along the lines of a fixed set of 4 initial guesses, followed by a simple algorithm to pick from a handful of fifth guesses.
