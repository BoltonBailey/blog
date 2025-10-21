
# [Prediction Markets Eat Bayes](https://thequantummilkman.substack.com/p/prediction-markets-eat-bayes)

This post covers the paper ["Learning Performance of Prediction Markets with Kelly Bettors" by Beygelzimer, Langford, and Pennock](https://people.cs.umass.edu/~wallach/workshops/nips2011css/papers/Beygelzimer.pdf). It's a short paper (4 pages main body, 3 pages appendix), and it doesn't use any calculus, so I encourage you to read it yourself. The main conclusion of the paper is a market equilibrium theorem stated in section 4.1 \footnote{the authors did not state this as a theorem in the sense of not using latex theorem environment for this, for some reason I don't really understand}. I would verbalize the theorem this way:

> For a group of participants in a series of prediction markets engaging in Kelly betting at market-clearing prices, the proportion of wealth held by a participant at any time reflects the probability that their beliefs are correct according to Bayes' law, under a prior that assigns credence to each participant's beliefs proportional to their initial balance.

Despite the apparent massive relevance of this paper to the interests of the extended Manifold community, I haven't been able to find any discussion about it on Manifold, its discord, or [any](https://abstraction.substack.com/p/forecast-scoring-methods) of the [blogs](https://www.astralcodexten.com/p/prediction-market-faq) or [websites](https://www.lesswrong.com/tag/prediction-markets) I usually associate with prediction markets and Bayesian reasoning. In this post I'll discuss the implications of this "Kelly-Bayes" theorem, both those discussed in the paper, and my own thoughts.

## A complicated Kelly-Bayes Agent is equivalent to multiple simpler Kelly-Bayes Agents

Suppose we wanted to set up a computer program to automatically make trades on a prediction market. In light of the results of this paper, what would be the best way to go about this?

One lesson we could take is that we should make a Bayesian model, and Kelly bet according to the predictions of that model. In the interest of capturing all possibilities, perhaps we would choose to make our model a broad mixture of simpler Bayesian models. Every time a market resolved we would update the probabilities of each of our sub models according to Bayes rule to better predict future outcomes.

But if our holdings in the market are really just an analog of the Bayes factor of our metamodel, we can conceptually simplify our program by taking the logic of the Kelly-Bayes theorem a step further: Instead of creating a single agent, we can create several agents to independently trade on the market, one for each of our simpler models. If we assign each of these sub-agents a starting balance proportional to our prior for them, those balances will update according to Bayes law. At any given time, each sub-agent's fraction of the overall wealth among all traders will be the product of their credence in your metamodel with your metamodel's credence in the market-wide model. This means that your wealth accumulation will be unaffected by factoring out your model among multiple bots.

This doesn't make you richer, of course. But it does potentially make it easier for you or other participants on your prediction market platform of choice to understand what you are doing. Popping out of the frame of programmatic trading, this suggests that making multiple accounts to trade on different "theses" could be helpful to let you realize more quickly which ideas are panning out and which aren't.

### Market Friction and Computational efficiency

An exception to the above logic might be if there are significant per-transaction fees in the market. Then, you would be better off having your metamodel make all its trades in a single transaction to amortize the fee, leaving you with slightly more money.

But on another level, perhaps this discrepancy is telling us something. Transaction fees exist\footnote{in theory} to offset the computational costs of recording and managing the transactions you send. If we take this at face value, then we can view these fees as the price of offloading the cost of managing the relative probabilities of the sub-models onto the prediction market platform. After all, if we pretend that we don't have to store credential information for each of the sub-agents markets, then we have saved hard-drive space with this approach!

If we do find that a particular hypothesis is not making enough in profit to cover its transaction fees\footnote{["Paying rent"](https://www.lesswrong.com/tag/making-beliefs-pay-rent) as it were}, perhaps that is a good signal that this hypothesis is not worth the computer power/brain time taken to consider it. After all, for any given real-world outcome being predicted, there can be hundreds of factors influencing that outcome. Perhaps another lesson here is that instead of creating a model with complexity increasing exponentially in the number of factors you try to account for, the market mechanism could be used to decide which factors are most important.

### No Seriously, [Never go Full Kelly](https://www.lesswrong.com/posts/TNWnK9g2EeRnQA8Dg/never-go-full-kelly)

[This post](https://www.lesswrong.com/posts/TNWnK9g2EeRnQA8Dg/never-go-full-kelly) by SimonM gives some compelling reasons why the Kelly criterion is perhaps too aggressive in most cases. It advocates the strategy of fractional Kelly betting, where you make Kelly bets as if your bankroll were only a fraction of what it really is. It also gives a justification for this in terms of "respecting your counterparty".

The Kelly-Bayes theorem gives us an interpretation of this strategy. We know that dividing your money into two piles and adopting different strategies with those piles is equivalent to adopting two Bayesian hypotheses, assigning each a prior, and then betting according to a mixture of those hypotheses. In this case, the two beliefs are "My model of the world is right (so I should bet full Kelly)" and "The market's model of the world is right (so I should not bet)". The fraction of your belief assigned to the former is your Kelly fraction.

This lines up neatly with the "Never go Full Kelly" description of the Kelly fraction as a ratio between our information and the market's information. One additional perspective that the Kelly-Bayes interpretation gives is an idea of how to update your Kelly fraction on a certain topic over time - you should treat your full winnings from the portion of your bankroll you are Kelly betting with as your full bankroll for your next Kelly bet.

## Prediction markets are only as bad as their best participant

It's a dictum of the prediction market ethos that they ["will always be at least as good as the best expert"](https://www.astralcodexten.com/i/91718311/why-believe-prediction-markets-are-accurate). The Kelly-Bayes theorem gives a mathematical justification for this claim.

Prediction generators are often graded by their ["log loss"](https://en.wikipedia.org/wiki/Cross-entropy) (you can read the technical definition at the link). It's a convenient concept because of its connections to learning theory. In this case, those connections pay off in the form of a corollary to the Kelly-Bayes theorem:

> (BLP Theorem 1): For all sequences of participant predictions, and all sequences of revealed outcomes, the log loss of the market predictions is approximately\footnote{where the approximation factor is the logarithm of that participant's starting wealth share} no more than the log loss of any participant.

This follows by drawing a connection between the participant's wealth relative to the rest of the market, and their Bayes factor relative to the market's predictions.

## Quantifying the tension between prediction markets and modelers

Prediction markets are pitched as a way of aggregating expert forecasts to get at the truth. Yet often, the markets give probabilities that are directionally discrepant from experts. Consider the 2020 presidential election, when [538 gave Biden 89%](https://projects.fivethirtyeight.com/2020-election-forecast/), the [Economist gave 97%](https://projects.economist.com/us-2020-forecast/president) and the [Harvard Political review gave 99.96%](https://harvardpolitics.com/hpr-2020-presidential-election-forecast/), but [Predict It gave <70%](https://www.predictit.org/markets/detail/3698/Who-will-win-the-2020-US-presidential-election) and [Polymarket gave <75%](https://www.predictit.org/markets/detail/3698/Who-will-win-the-2020-US-presidential-election). How can prediction markets aggregate expert forecasts when their predictions lie outside the full range of expert opinion?

Let's look at the extended context of the quote above (from Scott Alexander's the Prediction Markets FAQ):

> You can prove that one of two things must be true. Either over a long timescale, a prediction market will always be at least as good as the best expert, authoritative organization, or other information source. Or you can get rich quick.

The "long timescale" part is the key factor here \footnote{I might suggest amending the last part to "you can get rich slowly"}. While the Kelly-Bayes theorem tells us that the market learns at an optimal rate, nobody says that that rate has to be particularly fast. In particular, large prediction market platforms without betting caps like Polymarket have only been around for a few election cycles, so we can't expect them to predict incredibly accurately now.

The silver lining is that we can anticipate the rate at which the market improves. One view is that many traders on political prediction markets have a political bias that leads them to bet in favor of one party. If we take Nate Silver's prediction as the ground truth and assume some distribution on the degree of bias of different participants, we could compute how much bankroll was lost at each degree of bias and simulate the discrepancy between the market and the expert going forward. I'll leave this to another post.

There are a few final lessons to be taken:

1. It takes time for money in the market to pass into the hands of those betting the expert forecasts. You can potentially profit by betting according to these forecasts yourself and speeding the process along.
2. The market naturally learns slowly in domains where data comes slowly.
3. The less biased a particular view is, the more slowly the market learns to disregard it.