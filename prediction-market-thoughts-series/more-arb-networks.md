# More Combinatorial Arbitrage Networks

[In a previous post](https://thequantummilkman.substack.com/p/some-prediction-markets-for-the-2024) I described a collection of prediction markets I set up in advance of the 2024 US Presidential election.
These markets were designed to capture several aspects of several individual markets that people were interested in (on particular swing state outcomes, overall outcomes, electoral vote counts, etc.) and tie them together into combinations that could be arbitraged against each other.

This post will put forward more ideas for combinations of linked markets and give examples of ways they can be usefully synthesized into more granular combinations of outcomes.
The idea is to create derivative markets which are both

1. Easy to resolve based on the outcomes of underlying markets, so that they can be safely arbitraged and allow differences of opinion across related markets to confront one another.
2. Are themselves independently interesting, or which could easily be analyzed using the standard toolbox for predictions in the relevant domain.

<!-- 
The electoral vote count w/ variance described in [this post](https://thequantummilkman.substack.com/p/some-prediction-markets-for-the-2024), but I will not describe here to not repeat myself
-->

## Primary candidates

The state-by-state breakdown I mentioned before seems like a good approach with the general election only a few months away,
but on longer timescales other dimensions of uncertainty overshadow this framework.
"Primary" amoing these is the question of which individuals will be the major party candidates.

A combinatorial market that captures the two major party candidates and the party which ultimately wins the election seems useful.
Besides being arbitragable against markets on the three marginal probabilities, this market structure is also near-arbitragable against:

1. Markets on the ultimate identity of the general election winner (2024 notwithstanding)
2. Conditional markets on the likelihood of an individual winning if nominated
3. Conditional markets on the likelihood of an individual winning in a particular head-to-head matchup.

Point 2 seems particularly relevant to national discussion, because parties want to win,
and information about which candidates are most likely to make that happen could help primary voters make their decision.
From the point of view of a trader, market 3 seems familiar: Assessing the relative strength of two competitors is a longstanding task of prediction markets (e.g. as in sports betting).
One could imagine an "Elo-bot" which trades on the assumption that candidates have Elo scores that dictate their win likelihood in matchups.

A combinatorial market of this type would require O(mn), where m and n are the number of candidates in the two parties.
One could also imagine a O(mn(m+n)) combination which allows for the possibility that the eventual winner might not be either of the nominees, due to replacement.
More markets require more total liquidity, but hopefully much of this could come from people betting on the proposition that replacements are unlikely.

[Link to market](https://manifold.markets/BoltonBailey/2028-potus-party-nominees-and-winne)

## Traingular mesh for numerical predictions

In finance, we are often concerned with collections of ratios of future asset prices.
For example, we might ask questions like:

- What will the USD-denominated value of a NVIDIA share be at such-and-such?
- What will the USD-denominated value of a Google share be at that time?
- What will the ratio of the prices for these stocks be?

These three values have a multiplicative relationship - the first is just the product of the second two.
Besides this,
there are probably many factors in the real world that could cause outcomes for these ratios to be related, and for that reason,
many traders will think about more than one of these at the same time.
But the multiplicativity is useful because it means we can draw a two-dimensional ("log-log") chart to capture all three values.
Here the vertical axis represents NVDA price, horizontal represents GOOG price, and the diagonal lines represent lines of common ratios between the stocks.

Image

This suggests a combinatorial market which has an outcome for each triangle.

[Link to market](https://manifold.markets/BoltonBailey/nvda-vs-goog-performance-20280101)

While the individual triangles seem less likely to be directly traded against, many kinds of bets can be represented by combinations of the triangles, like

- Bets that a price or ratio will be above a certain point
- Bets that a price or ratio will fall within a certain range

From the market maker's perspective, a straightforward generalization of the [Black-Scholes model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model) to multiple dimensions can model the prices and help provide liquidity.

It's also worth noting that this applies beyond finance, really to any multiplicatively / additively / linearly related combination of variables.
Some ideas:

- Quantity X growth over time period t0 to t1 \* Quantity X growth over time period t1 to t2 = Quantity X growth over time period t0 to t2
- Time until X technological milestone is reached = Time until Y preliminary milestone is reached + Time to develop X once we have Y
- Average value of quantity X over large set A, (partitioned into B and C) = (Size of B) \* Average value X over B + (Size of C) \* Average value of X over C

Some open questions for me about this design include how well it scales to even higher dimensions,
and how best to deal with the situation where different traders want the lines drawn in different places (perhaps unevenly spaced).
Of course, we could just partition the space into the regions and make markets for each one, but this could fragment liquidity more than is necessary.

<!-- [Video](https://www.youtube.com/watch?v=tCsl6ZcY9ag) relevant? -->

## Causality

Discussions on Manifold last year about Futarchy / decision markets have [gotten me interested](https://manifold.markets/BoltonBailey/futarchys-fundamental-flaw-the-mark) in our ability to understand causal relationships through prediction markets.

My perception of the primary obstacle we face in this endeavor is this:
The gold standard for establishing causality is a controlled experiment,
but the framework of such an experiment is difficult to set up or simulate within the ontology of a prediction market.
For one thing, prediction markets often try to forecast one-off or infrequent events, which makes the [data collection process slow](https://thequantummilkman.substack.com/i/149861175/quantifying-the-tension-between-prediction-markets-and-modelers).
For another, prediction markets in themselves don't tend to impact real world events; when they do, it tends to be in distasteful ways (see chaotic instances of direct manipulation of Polymarket outcomes), and even in cases where the market is carefully designed to be attached to some randomized causal mechanism (like a decision market with small chance of randomly chosen outcome) the randomization necessarily trades off our knowledge against the impact that the knowledge can have.

We can instead look to techniques from social science for understanding cause-and-effect in cases where a controlled experiment is infeasible.
These techniques include:

- Listing off large numbers of variables that we think could plausibly affect outcomes, and control for those, hoping that this captures the major confounding variables at play.
- Looking for "natural experiments", where there is some intrinsic randomness that allows us to do causal inference.

So here are rapid-fire ideas along these lines.

- If we have a number of variables and we want to know which ones are most important for predicting an outcome (perhaps to put more liquidity into), one way of evaluating this is the [Shapley value](https://en.wikipedia.org/wiki/Shapley_value), which [can be determined](https://shap.readthedocs.io/en/latest/example_notebooks/overviews/An%20introduction%20to%20explainable%20AI%20with%20Shapley%20values.html) from the predictive accuracy of subsets of the variables.
  Because this determination is linear, it can be arbitraged against Shapley values for these subsets.
- Taking "natural experiments" in the literal sense :grin:: How does the weather impact the event in question?
  - For example, voting behavior is sometimes said to be impacted by the weather.
    To find out the causal effect of a president's policies, you could condition outcomes on the chance of rain on election day.

[Link to market](https://manifold.markets/BoltonBailey/marginal-weather-in-the-tipping-poi)
