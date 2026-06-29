# Which prediction markets are best?

Readers of this blog will likely be familiar with prediction markets.
A creator specifies an event that may or may not happen in the future.
Traders buy and sell shares that pay out a fixed amount if the event occurs, and nothing otherwise.
The share price reflects traders' beliefs about the event's likelihood, which we can observe directly.
If a share that pays out $1 upon the event's occurrence is trading for $0.50, the market is predicting a 50% chance of the event.
We can often assume this probability is a good estimate of the event's actual likelihood.

Implicit in the belief that people should be excited about prediction markets is the idea that knowing these probabilities is somehow *good* or *useful*.
Perhaps it seems obvious that this should be the case: After all, isn't more knowledge always better than less?
But given the costs of prediction markets (pecuniary, attentional, and operational) it is worth asking questions like:

- How useful are prediction markets?
- What makes one prediction market more useful than another, or useful enough to be worth creating or funding?
- How can we identify these factors to better allocate our finite resources to the most useful markets?

## The Obstacles

Unfortunately, a few factors make these questions hard to answer.

## Information markets as a public good problem

Prediction markets are [sometimes called "information markets"](https://en.wikipedia.org/wiki/Prediction_market), which is a [term that can also refer](https://en.wikipedia.org/wiki/Information_market), more simply, to any market where information is bought and sold.
This terminological overlap rightly suggests that prediction markets are places where the market creators are essentially buying information about events by providing liquidity to them.
There is reason to think the ordinary economic logic of markets works well for this exchange:
The markets where people are willing to pay for more liquidity will attract more traders and therefore more accuracy, and we could say that this makes these markets "better".

But this picture becomes complicated when multiple people get involved.
In ["Should Prediction Markets be Charities?"](https://www.overcomingbias.com/p/should_predictihtml),\footnote{ [h/t this spreadsheet](https://docs.google.com/spreadsheets/d/1JUGUY_Atq56pmGyMtdadwedGSN7jKb8BKC-ERkrA_h8/edit?gid=0#gid=0).}
Peter McCluskey advocates viewing prediction markets as public goods.
Many forecastable questions of public life are ones in which large numbers of people have a stake in the outcome, and therefore stand to benefit from increased accuracy.

Unfortunately, when we combine this view with the "information market" view, we get the classic public goods ["free-rider problem"](https://en.wikipedia.org/wiki/Free-rider_problem).
Everyone might want a market to be made, but no individual might want this enough to do it themselves, and no one might want to come forward in support of it in fear of being saddled with its costs.
So unfortunately, while there are good reasons to think private provision of liquidity will bring some social benefits, there are also resons to think this will be suboptimal.

## Disagreement about information spectra

Besides the problem of assessing *which* markets are socially valuable, there is also the problem of assessing *how* the information from markets can be valuable.

Consider the [Brier Score](https://en.wikipedia.org/wiki/Brier_score).
It's probably the most common way of "scoring" the accuracy of a prediction or batch of predictions.
But is it better than other common scoring methods, like the [logarithmic score](https://en.wikipedia.org/wiki/Scoring_rule#Logarithmic_score) or [spherical score](https://en.wikipedia.org/wiki/Scoring_rule#Spherical_score)?

<!--
Question (should be pretty easy): What is the distribution for log score?

Note: If the density of shares offered at price point x is D(x) then the density of spending offered is x D(x) 
-->

To answer this question by relating these concepts to liquidity and markets, here is another way of viewing the Brier score:
It's linearly related to the profit you would make if you were offered a multitude of very small bets
with shares distributed uniformly across the probability space,
and you accepted exactly those bets your prediction told you were profitable.
In fact, any [proper](https://en.wikipedia.org/wiki/Scoring_rule#Propriety_and_consistency) scoring rule can be conceptualized in this framework
of calculating the profit from a collection of offered bets.
So if we think about this from the perspective of the liquidity provider from the previous section,
we might think that the best scoring system is the one that corresponds to the distribution of bets the liquidity provider most wants to make.

This framing highlights that perhaps *neither* the Brier score nor the log score is consistently more important - we could have some totally different liquidity profile that is best suited to a particular prediction.

For example, say [I was funding a prediction market for whether someone would quickly lease my apartment if I chose to let it go](https://manifold.markets/BoltonBailey/if-i-dont-renew-my-apartment-will-i),
because I was deciding whether I should renew my lease.
In this case, the usefulness of the market is in its ability to help me make a decision \footnote{of course there are also causality concerns here, see previous posts and links for more details}.
If the probability of losing the apartment is high enough, I would want to renew.
The best liquidity profile wouldn't be the brier profile or the log profile or any other standard "score" - it would really be a single massive limit order at exactly the probability point where my decision would change.
But this means that to provide liquidity optimally, I would have to figure out exactly what that point was.

This is all to say that even liquidity provision on a single market can be a complicated question.

## The value of liquidity

But suppose we knew perfectly well how much we valued accuracy for each probability set point on each of our proposed prediction market topics, and all we wanted to do was to allocate a shared public liquidity pool to these markets.
We would then be left with the optimization problem of allocating the pool to maximize the weighted sum of these accuracies.

Unfortunately, it is not clear that even this problem has a straightforward answer.
Presumably, increasing the amount of liquidity has diminishing returns on accuracy.
But to know at what point those diminishing returns drop below the marginal value of increases to liquidity elsewhere requires understanding the psychology of traders\footnote{be they human or machine} and how they detect and respond to liquidity.

Further complicating this is the fact that liquidity provided at particular price points has a salutary effect on nearby price points.
If I want to know whether the chance of an event is greater than 60%, and there are already big limit orders at 59% and 61%, I am already in a pretty good spot, and more liquidity might not be needed.

*Even further* complicating this is the possibility of interrelations between markets.
If there are liquid markets on the chances of various candidates winning an election, then an arbitrageur should be able to give a good price quote on the party of the elected candidate, which means that providing liquidity on this other outcome might be less important.

## Goodhart's law for market performance metrics

As a final point, let's consider the correlation issue.
It seems especially interesting, since it suggests that even though the situation is complicated,
there could be great benefit from identifying and leveraging related markets.

Previously, [I ran a competition](https://thequantummilkman.substack.com/p/the-markets-for-markets-competition-603) to incentivize and study the art of making markets that could help us better predict the outcome of more-popular later-resolving markets.
To judge the competition, I needed a metric which respected the underlying uncertainty in the linked markets, while incentivizing correlation (I was looking specifically at metrics that could be computed from the price charts of joint outcomes).

But I noticed that whatever metric I chose, it would be subject to a form of [Goodhart's](https://en.wikipedia.org/wiki/Goodhart%27s_law)/[Campbell's](https://en.wikipedia.org/wiki/Campbell%27s_law) law.
If you try hard to create a source market that "predicts" the target according to a metric like this, then you will want to make a market based on as much information on the target market's outcome as is available at resolution time.
But in theory, all of that information is integrated into the target market itself.
The optimal source market therefore turns out to be a direct derivative of the price chart of the target market; something like "Will the price of the target market be above x% at close time?".
I could try to ban specific kinds of markets like this, but I fear that would precipitate an arms race to find the optimal market structure that wasn't banned, or else cleverly phrase criteria to avoid detection.
This seems like an obstacle to a larger or more official version of this kind of competition.

Footnote: I used [Mutual information](https://en.wikipedia.org/wiki/Mutual_information#Relation_to_conditional_and_joint_entropy), but there are many other information-theoretic measures of relatedness, like [Conditional entropy](https://en.wikipedia.org/wiki/Conditional_entropy#Chain_rule), [Variation of information](https://en.wikipedia.org/wiki/Mutual_information#Metric), and [KL-Divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence).

## Paths forward

So to summarize, I think there are many complicated issues related to assessing the value of and providing liquidity for prediction markets.
Perhaps there are two paths forward for the prediction market platform that wants to address these issues.

### Embrace the complexity

The problems I have discussed in this post are technical, but I don't think they are the kind of technical problems that are unsolvable.
We could approach many of these problems by doing things like:

- Designing incentive-compatible mechanisms to let users communicate their preferences on valuable markets and price points.
- Using [network science](https://en.wikipedia.org/wiki/Network_science) to identify "naturally central" markets.
- [Dogfooding](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) decision markets about the expected benefits of different liquidity provisions (footnote: a further complication is that the existence of a market like this might itself create arbitrage opportunities and change the liquidity structure).

The downside of these approaches is the implementation effort required.

### Friendly agreement

On the other hand, maybe there are things we can do that don't raise the complexity bar while tapping into some of the same benefits.

- Community votes/surveys to boost well-liked markets.
- Gathering statistics on revealed user preferences through metrics like page visits and boosting markets based on those.
- Making simpler derivative markets that don't precisely reflect mathematical models of optimal information gathering, but still broadly inform traders.

Many platforms already implement some of these, so I would encourage a path of picking the low-hanging fruit while looking for opportunities to refine the process where it's most expedient.
