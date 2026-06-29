# [Prediction Markets Eat Bayes, part 2: Risk-free profits](https://thequantummilkman.substack.com/p/prediction-markets-eat-bayes-part)

When can't Kelly Fail?

A compelling post about the Kelly Criterion [hit Hacker News](https://news.ycombinator.com/item?id=42466676) last December: ["Kelly Can't Fail" by John Mount](https://win-vector.com/2024/12/19/kelly-cant-fail/).
This article gives a counterintuitive example of a situation where betting according to Kelly Criterion "can't fail".
I noticed some similarities between the analysis in Mount's post and the ideas I covered in [my previous post](https://thequantummilkman.substack.com/p/prediction-markets-eat-bayes) on the relationship between Kelly Criterion and Bayes' Rule.
So I am writing this follow-up post to explore the connection further.

## Kelly Can't Fail

I encourage you to read [Mount's post itself](https://win-vector.com/2024/12/19/kelly-cant-fail/), but I'll summarize the key points here:

- The post describes a betting game where a player is shown cards from a standard deck, one at a time, without replacement.
  The player can choose to bet any portion of their bankroll at even odds on whether the next card will be red or black.
- The post analyzes what happens if the player bets according to the Kelly Criterion in this game.
- The post shows, perhaps surprisingly, that the player **always makes the exact same amount of money, no matter the order of the deck**.
  In particular, they always increase their bankroll by a factor of about 9.08.

## Interpreting the result with the Kelly-Bayes theorem

The article gives its own sketch of a proof of this fact, based on the concept of a "portfolio strategy".
They show that betting according to the Kelly Criterion is equivalent to splitting your bankroll into $\binom{52}{26}$ parts, and betting with each part on a particular arrangement of red and black cards.

But I would argue that, with the Kelly-Bayes theorem, this proof could be made even simpler!
In fact, the equivalence between the Kelly Strategy and the portfolio strategy is a straightforward application of [section 2 of my previous post](https://thequantummilkman.substack.com/i/149861175/a-complicated-kelly-bayes-agent-is-equivalent-to-multiple-simpler-kelly-bayes-agents), so if you know this result, no further justification of the equivalence is needed.
Really, you can think of the entire game as a scenario where the player is betting against a whale with much more starting capital who thinks that every card is equally likely to be red or black, regardless of previously shown cards.
The player, whose prior is uniform over the $\binom{52}{26}$ arrangements of red and black cards that are actually possible, will increase their money by a factor equal to the Bayesian likelihood ratio of the whale's prior to their own prior.
This factor is $2^{52}/\binom{52}{26} \approx x9.08$, which is exactly the factor that Mount computes.

## Generalizing: When can't Kelly Fail?

Why does the result in this post feel so surprising?
For me, I think it's because I conceptualize the Kelly criterion as itself being inherently risky.
I think when many people first learn about the Kelly criterion, it's presented as an alternative to the "all-in" strategy of betting your entire bankroll on every +EV bet you find.
Kelly is a way of being more conservative, but it still doesn't advocate sticking your head in the sand and refusing to bet on anything.
After all, there are more conservative strategies than Kelly, like the "fractional Kelly" strategy advocated [here](https://www.lesswrong.com/posts/TNWnK9g2EeRnQA8Dg/never-go-full-kelly).
So it feels like the Kelly criterion is a kind of optimal tradeoff between risk and reward.
This makes it surprising to see a situation where Kelly is zero variance - shouldn't I accept some risk for a bit more expected value?

To understand this better, I wanted to think through what it was about the game in Mount's post that made it so special.
To my further surprise, I found that the class of games where Kelly can't fail is actually quite broad!
Again the Kelly-Bayes theorem is the key to understanding this - One can prove a corollary to the theorem that describes exactly which situations lead to zero variance under Kelly betting:

> (Zero-Variance Kelly-Bayes Corollary) If one individual and the "rest of the market" both act as Kelly-Bayes agents over a sequential series of markets, then the individual's final payroll has positive expected value and zero variance if and only if:
>
> 1. The individual assigns zero probability to some events to which the market assigns positive probability.
> 2. For the events that the individual and the market both assign positive probability, the individual assigns probabilities that are proportional to the market's probabilities.
>   Furthermore, the individual's bankroll will increase by a factor equal to the Bayesian likelihood ratio of the market's prior probability to the individual's on the events individual assigns positive probability to.

### Worked example

Let's work through a simple election-themed example to illustrate this.
Suppose there are two prediction markets, one for the outcome of the POTUS election in Florida and one for the outcome in Pennsylvania.
Now, Florida is redder than Pennsylvania, so suppose that the market thinks that there is a 10% chance that the Democrat wins Florida and lose Pennsylvania, and a 30% each for the other three possibilities.
But suppose further that I am much more confident than the market in the relative partisanship: I am certain that if Democrats win Florida, they will also win Pennsylvania.
Like the market, I think that the other three possibilities are equally likely.

The market is initially at 60% that R wins FL and 60% that D wins PA.
Florida's vote counting system is very fast, so I know that market will resolve first, and that's the first market I bet in.
Since my probability for a Republican win is 2/3, my first Kelly bet is (2/3) - (1/3)(0.6/0.4) = 1/6 of my bankroll.

From here there are two possibilities:

- If the Republican wins, then I end up with 5/6 + (1/6)x(1/0.6) = 10/9 of my initial bankroll.
  The Pennsylvania market then updates to 50/50, according to the conditional probabilities.
  This is exactly my conditional probability, so following Kelly, I don't bet on the PA outcome and I end up with **10/9**.
- On the other hand, if the Democrat wins Florida, then I have lost, and I go down to 5/6 of my initial wealth.
  But now I am again certain that PA will go D, and I Kelly-bet all my money on that outcome.
  The market's conditional probability that Pennsylvania goes blue is 0.3/(0.3+0.1) = 3/4.
  So when I win this bet, as I am certain I will, I go up to (5/6)(4/3)=**10/9**, just as if I had won the first bet.

This demonstrates the corollary: I have zero variance in my final outcome, and I increase my wealth by a factor of 10/9, which is exactly the inverse of 90% - the likelihood that the market assigns to the events I considered possible.

## Takeaways

I have a few takeaways from this analysis:

- The Kelly-Bayes theorem is yet again a powerful tool for understanding the relationship between betting strategies and beliefs about the world.
- For a Kelly-Bayes agent to experience zero variance, they must have a very specific relationship with the market's beliefs.
  In some sense, the only thing that they "know" is that certain events are impossible, and on everything else, they believe the market.
  This makes a kind of sense, since if you are betting on a "sure thing", you should not feel like you are risking anything.
- In the example above, as well as in Mount's post, there is a combinatorial explosion in the number of possible outcomes for all the markets.
  Yet this doesn't affect the Kelly-Bayes agent's money-making strategy at all.
  This raises further questions for me about the value of "joint markets"\footnote{also known in the literature as "combinatorial markets", another [Hanson topic](https://mason.gmu.edu/~rhanson/combobet.pdf).}
  like the ones I discussed in my [first](https://thequantummilkman.substack.com/p/announcing-the-markets-for-markets) [few](https://thequantummilkman.substack.com/p/the-markets-for-markets-competition) [blogs](https://thequantummilkman.substack.com/p/the-markets-for-markets-competition-603) on this website.
  If these don't help the market learn, are they good for anything?
  The answers to these questions will have to wait to a future post!
