# [My thoughts on prediction market platform design](https://thequantummilkman.substack.com/p/my-thoughts-on-prediction-market)

<!-- Originally started May 21, 2022. 5:35pm Eastern Time -->

_a manifesto expressing my personal preferences and learnings_

This is an old draft on a collection of items I would like to see in a prediction market platform. I am revisiting it now in celebration of the return of Manifold to being [a strictly play-money platform](https://manifoldmarkets.notion.site/Mana-forever-19154492ea7a80c08410ea8c64fac67e). It's from my own perspective, which might be described as "[literalist episteme](https://manifold.markets/BoltonBailey/spiritualistliteralist-gameepisteme)"

This post only deals with the backend of the platform. I have another post on the frontend which I will hopefully publish soon.

## Two outcomes only on the Backend

There are a variety of ways to structure a prediction market that are more complicated than the generic two-outcome either or market. These include:

- Markets to predict a real number.
  - Date prediction markets.
  - Amount prediction markets.
  - Markets that "resolve-to-fraction".
- "Multi"-Markets to predict which of a number of candidate possibilities will come to fruition.
  - Markets on political nominees are a common example of this.
- "Conditional" Markets to predict the outcome of one event given the outcome of another.
  - These revert all trades if the condition is not met.

Note though, that all of these can be approximated fairly well by collections of binary markets.

- Markets for predicting numbers can be converted into a number of markets on whether the predicted number will be above a certain value.
- Markets on candidate possibilities can be constructed via one binary market for each outcome (and perhaps another market to track "outcomes not considered").
- Conditional markets can be constructed by binary markets on the conjunction of the two events.

It is better to let the core logic of the platform express all of these options purely from binary markets.

Note that I am expressly **not** saying that user-facing interfaces for other market types should be avoided or removed. It is simply better to let the implementations of these interfaces be built on top of an underlying binary market logic. This is for a few reasons:

- It provides the simplest API for users who only want to interact with one market type.
  - Perhaps because they are made of silicon and are simpler to construct if they don't need to interact with complex interfaces.
- It allows power users to express their beliefs richly.
- It also lays the groundwork for more complex machinery to be built on top, as we will discuss below.

## Interest rates

Interest rates are a natural enemy of prediction markets. If I believe that a share in YES has a 50% chance of being worth one currency unit in a year, but I ascribe a time-value to my currency of 10%, then I am not motivated to correct a price for that share between 45% and 55%. If rational people are not motivated to correct the price within a particular range, then there is no reason to believe that the price will be correct to within that range.

Therefore, a system which accounts for interest rates should be implemented. There should be a variety of tokens which represent claims on the basic unit of account in the system which mature on a certain date. Instead of buying shares directly with the currency, shares in markets that resolve on a certain date should be bought with claims for that date, with 1 YES and 1 NO share fungible with 1 claim. It should be possible to directly exchange earlier claims for equal numbers of later claims, but the opposite should only be possible at a discount, if at all.

I anticipate and address the following problems:

- Users would require a liquid exchange for claims.
  - Bots and AMMs could be made to ensure there is a liquid exchange for claim tokens for any given date.
  - They could be optimized for a variety of interest rates, so that the market itself would determine the correct rate.
- There would as many types of claims as there are dates, fragmenting liquidity.
  - We might institute a system where markets can only resolve at discrete times, which get more frequent as the date approaches.
    - e.g. One can make markets that resolve on any date in the next month, on any Monday in the next six months, on any first Monday of the month in the next two years, &c.
- How can we edit resolution times?
  - Markets can be resolved earlier than expected by simply paying out the claims early (this does not change the date on the claims).
  - If a market must be resolved later than expected, the date on the claims can be made later. The loss that holders incur is considered a penalty for trading in a market with ill-defined resolution time.

## Convex Liquidity

[Angeris et al.](https://arxiv.org/pdf/2107.12484.pdf) point out that for agents whose preferences on portfolios are concave, optimal trades among those agents can be computed by convex optimization (i.e. in polynomial time).

The backend design should make it possible to create such agents. Practically speaking, these agents would be the equivalent of limit orders, but for multiple markets. The orders would be expressed as convex preferences over sets of shares. The backend would then maintain a graph of which orders are interested in which markets. When a human user requests a quote, the backend should analyze the market network in the vicinity of the market in question, solve the convex optimization problem, and give the user the best price that it can on the shares they want to buy which satisfying the order stipulations.

Such a system would synergize with other features:

### Logical Composition of Preexisting Markets

For any collection of markets, one can make more markets on combinations of outcomes of the collection. In the case of two markets A and B, this looks like

- A market on whether A and B will both resolve YES
- A market on whether A will resolve YES and B will resolve NO
- A market on whether A will resolve NO and B will resolve YES
- A market on whether A and B will both resolve NO

In fact, the price for any one of these markets, along with the prices for A and B themselves, determine the prices for each of the other markets.

Creation of these combinatorial markets should be standardized, resolution should be automatic, and it should be possible to identify such markets programmatically. This then lets the power user:

- Arbitrage the prices of A and B against the combinations, ensuring that updates to the prices of one market are reflected in the prices of others.
- Understand and analyze the conditional relationships between markets.
  - I could write a lot more on this and how it allows information to flow, just like price data flows for [complementary goods](https://en.wikipedia.org/wiki/Complementary_good) in traditional markets.
- Determine the market's estimate of the metric on events defined as d(E1, E2) = Pr[E1YES != E2YES]
  - Inconsistencies with the triangle inequality can be arbitraged away.
  - We can use the metric to find the nearest neighbors of each market, and cluster markets into categories.
- Compute the covariance for returns on a pair of markets from the tensor market price and use [modern portfolio theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory) to make bets more conservatively
  - Potentially even hedging using the conjunction market itself.

### Low-liquidity low-fee AMMs for Bots

The main benefit of bots to prediction market platforms is scale. While a human user might only be able to look at hundreds of markets and make a few trades a day, a bot can scan look at millions and make thousands. Given this, we should consider that the economics of the platform for bots will be different from those for humans. In particular, fees have a much larger impact on bots. On the other side of the coin, bots have much less need for liquidity than humans do, because the cost of their analysis is much lower, and they therefore don't need to make as much profit on each trade.

It should therefore be possible to create bot-friendly markets with extremely low liquidity and fees. Potentially it should even be possible to have a zero-liquidity market as a placeholder for bots to reference. Even if these markets aren't displayed to human users, bots will trade on them and gain information which will help them correct visible markets. The low-fee AMM is important to incentivize precise pricing - there is no incentive to bring the price of a market to an accurate value if fees negate the profits at the margin.

This doesn't have to impact fees at the human scale: AMMs providing bots liquidity can exist alongside much higher-fee, higher-liquidity AMMs if a market creator/subsidy provider wants. Users of both species could then trade against the two AMMs simultaneously (with the aid of the convex optimization above).

### Opening/Frequent Batch Auctions

In many prediction markets, much of the profit goes to whoever reacts to news first. This "high frequency trading" is a bad thing - It means that the people who have the most influence on the prices may not be the best predictors, but rather the best clickers.

How can we prevent it from happening? One way might be to limit the times at which people can interact with a market (to something like, say, once every five minutes or once every day). But then we have everyone making transactions at once, and we have to decide what order in which to execute these transactions.

Instead, we can execute orders "simultaneously". In such a ["batch auction"](https://www.investopedia.com/terms/b/batchtrading.asp) system, everyone submits a limit price and a max volume (maybe hidden initially, and then revealed after all orders are in). Then, we can just match trades against the AMM(s) and each other via, again, convex optimization.

## Play Money

Prediction markets should be based on play money, rather than real money.

One reason for this is ethics, broadly construed. Play-money prediction markets are much less likely to do financial harm to their participants, and for that reason, a play-money market is much more likely to be considered ethical. This, in turn, makes it much easier to operate a large-scale prediction market legally. While there are a spectrum of views on the ethics of gambling, even those who take a more liberal view can admit that the pervasiveness of anti-gambling views poses a significant barrier to the adoption of prediction markets.

The most common argument I hear in favor of real-money prediction markets over play-money ones is that having real money at stake makes people consider their bets more carefully. I think there are several problems with this way of thinking:

- Many people gamble in venues which are well understood to be negative EV. This is a testament to the fact that people don't always primarily consider profitability when real money is at stake.
- With respect to "motivation" - the fact that the money is play rather than real doesn't mean that the user isn't motivated to obtain more of it. Certainly the lesson of video games is that artificial goals can be powerful motivators. And after all, if they didn't want to "win", why would play-money prediction market users be there in the first place?
- More than that, the "stake" line of thinking seems to assume that real-money somehow focuses the mind on maximizing profit in a way that play money does not. Perhaps for some people, this is true. But I would venture that for others, having real money at stake induces anxiety and a psychological need to limit risk. Poker players often talk about not bringing more money to the table than they can afford to lose. If this is to be applied to prediction markets, then we might expect the opinion of the market to be biased according to this risk aversion.
- The information-processing view of prediction markets, which I expounded on [here](https://thequantummilkman.substack.com/p/prediction-markets-eat-bayes), shows that a prediction market doesn't have to comprise only predictors with high skill. Eventually, wealth gravitates to the best predictors, and the market is dominated by them. This is true in play-money markets as well as real-money markets, and in fact, it is potentially even more true in play-money markets, depending on whether willingness to bring real money to the table is correlated with predictive skill.
