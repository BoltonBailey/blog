# Slightly less lazy wordle

This is a follow-up to my [earlier post on how to win at Wordle while memorizing as little as possible and making a maximal number of guesses](https://thequantummilkman.substack.com/p/lazy-wordle).
At the end of that post, I alluded to cutting plane methods as a possible approach for finding such strategies.
This entry will do more analysis along these lines, with the goal of a procedure requiring only slightly more memorization but enabling us to win wordle 100% of the time.

## A new solution concept

We found last time that no 5-guess collection was capable of disambiguating all pairs, or even all but four pairs (in fact, after some further exploration using the ideas discussed below, I found that the exact optimum is 10).
Given this, we can ask: "What is the next-most simple type of strategy which isn't just memorizing 5 words and regurgitating them?"

Perhaps the answer is: Memorize n<5 words and regurgitate them, and then conditionally guess one of two other sets of memorized words conditional on a simple-to-check outcome from the first guesses.
Maybe a good conditional is "is there an 'E' present in the word?", which is true for 46% of answers.

For solutions of this type, the minimum number of guesses would be to have 4 initial guesses and two additional conditional guesses, but if 5 guesses leaves ten undisambiguated pairs, it seems unl

## Wordle Information

It is worth thinking a bit more about what information you actually get from a Wordle guess.
Clearly you get a green for a correctly placed letter and a yellow for a letter in the word but in the wrong place.
But what if you have multiple copies of a letter?
In this case, Wordle will color in your letters only as many times as that letter appears in the word (with greens being colored in first).
Thus, you can think of the information you get from a wordle guess as consisting of:

- The greens, if there are any.
- For any letter you use n times in the guess, information about whether or not that letter appears at least that many times in the word, and if not, the exact number of times it does appear.

We can therefore consider there to be the 260 following bits of information available from guesses.

- For each letter (26) and word position (5) we can be informed if that letter is in that position in the solution.
- For each letter (26) and nonzero number of times a letter can appear in a word (5 but technically less as most letters appear 3-4 times max in a valid guess) we can be informed if there are at least that many copies of the letter in the solution.

Any guess will provide some of these bits, and for any solution pair, in order to disambiguate, we will need to obtain one of the bits that disambiguates the pair.

### Eliminating redundant pairs

If we want to disambiguate all pairs, then there's no point in tracking pairs whise differentiating bitsets are equal to or superset of other bitsets already covered by another pair.
This lets us do an elimination:

```
Answer pairs by number of disambiguating bits (before -> after dominance):
    4 bits:     2,441 ->     1,070  ( 43.8% kept)
    6 bits:     1,599 ->     1,447  ( 90.5% kept)
    8 bits:    18,846 ->     3,989  ( 21.2% kept)
   10 bits:    30,461 ->    12,268  ( 40.3% kept)
   12 bits:   122,569 ->    28,443  ( 23.2% kept)
   14 bits:   219,438 ->    51,323  ( 23.4% kept)
   16 bits:   414,791 ->    58,055  ( 14.0% kept)
   18 bits:   369,333 ->    24,430  (  6.6% kept)
   20 bits:   169,473 ->     2,472  (  1.5% kept)
    total: 1,348,951 ->   183,497  ( 13.6% kept)
```

## A fine-grained relaxed LP

Previously, our ILP just checked for each guess and each solution pair whether the guess disambiguated the solution pair.

But this new solution concept and new information idea, we can create a new ILP where:

1. We create a variable for each word whether it should be included in the initial four guesses.
2. We constrain these to contain an "E".
2. We also create variables for each word whether it should be the fifth guess if there is/is not an e in the solution.
3. We create variables for which of the 260 bits of information will be available (conditional if there is/is not an e in the solution).
4. We constrain these variables to be consistent with the content of the guesses.
5. We also constrain the information variables to disambiguate all solution

TODO run analysis
