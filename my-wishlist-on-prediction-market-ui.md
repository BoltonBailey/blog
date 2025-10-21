# Prediction Market UI wishlist

I [previously](https://thequantummilkman.substack.com/p/my-thoughts-on-prediction-market) posted my thoughts on what overhauls to [Manifold](https://manifold.markets/) or other prediction market backends I might like to see. Here I will describe my thoughts on the other side of the coin: Tools/reskins that deal exclusively with the frontend. The exciting thing about these ideas is that they could be created without touching the platform itself, via external websites and browser extensions. Of course, I am too lazy to make these myself, so I am putting them out there (in rough order of implementation ease) in the hopes that someone else will. Developers, take inspiration!

## Chart displays that reflect liquidity

Price charts in today's prediction markets typically simply show price against time, potentially with within-bin variance data in the case of candle charts. This leaves out a key piece of data that some might like to use to assess the reliability of the price-probability: The [depth of the market](https://www.investopedia.com/terms/m/marketdepth.asp).

Here's a straightforward way one could include this information in a chart: In addition to the price plot, include plots above and below the price line which indicate, for any point in time, the price that would have resulted from a buy or sell order of a fixed size. One could even create multiple bands of lines at different orders of magnitude of order size. This would let traders see how much liquidity there is in the market at any given time, and how much they would be able to move the market by placing a buy or sell order. They might also find it useful to see how the liquidity changed at key points in the history (e.g. if the liquidity changed in response to certain pieces of news).

Another helpful feature along these lines would be depth charts that reflect AMM liquidity. [Here](https://discord.com/channels/915138780216823849/1190060347005075507/1190060347005075507) is a nice mockup by user @Wasabipesto on the Manifold discord.

![Depth chart image](https://media.discordapp.net/attachments/1190060347005075507/1190108113366425703/unknown.png?ex=68234ccd&is=6821fb4d&hm=8e151ea29038fc3977165ee3f931e7b9169f8bef903b3ade655c98b6b1c4bee2&=&format=webp&quality=lossless)

## Using Profits as a Comment Karma System

Many prediction markets (real-money political markets in particular, I have found) have toxic comment sections. The majority of posts in these comment sections are highly partisan. This makes the platform unpleasant to use. What could be done to ensure that the comments we see are predominantly well-thought-out, rational, and objective?

One way to do this might be to optionally prioritize comment visibility from users who have a certain level of profit on the platform. This reflects the philosophy that the best traders have the clearest view of events, and that their voices are the ones the public should listen to. A karma system was made to value in particular profit made on markets in the category in question could, in particular, help amplify the voices of specialists. It could also be made customizable (i.e., by letting users choose the karma level below which they want comments to be hidden).

## Slider for round-number price points/share purchases

As far as I can tell, the standard way to communicate a buy order on most prediction markets is:

- Input the share type you want and the amount of platform currency you want to spend. The platform then tells you how many shares this will buy and what this will move the market to.

There are two other modes one could imagine:

- The user could instead input the number of shares they wish to purchase, and get the cost and final price from that.
- They could input the probability they want to drive the market to, and get a read-out of how much it would cost and how much they stand to gain.

There are good reasons one might want to specify trades in terms of the latter quantities. A trader looking to arbitrage two equivalent markets might want to buy the same number of shares in both. A researcher might have a precise estimate of a probability and want to move the market to it.

I think the ideal user interface lets you choose between these three modes seamlessly. For a keypad interface, this would mean being able to enter a number in any of the three separate fields and have the other fields repopulate. For a slider interface, this would mean that different positions of the slider would clip to round numbers in each of the different buying modes, rather than only one (i.e. instead of different positions on the slider corresponding to only 1,2,5,10 units spent, there would also be positions on the slider for 1,2,5,10 shares bought, and for moving to 20%, 33%, 50%, 66%, 80% probabilities).

## Baskets

[Manifolio](https://manifol.io) is a great tool for trading on Manifold, using the [Kelly Criterion](https://www.princeton.edu/~wbialek/rome/refs/kelly_56.pdf). I feel that a similar interface could be used for placing bets on multiple markets at once.

The flow would work like this:

1. I input a (perhaps weighted) list of shares, to be treated as a basket. (A key use case is arbitrage, where I group a YES share in one market and a NO share in an identical market to create an asset I know is worth 1 unit.)
2. The interface shows the price of buying different numbers of copies of the basket (or number of shares for a certain amount of money, see previous section).
3. I can provide an API key and buy these baskets.

For bonus points, the interface could also:

- Save these baskets in my local storage for later use.
- Alerts me when the price of the basket is below a certain threshold.
- Or better yet, let me place limit orders on the basket.
- Integrate with Manifolio to Kelly bet on baskets.

## Debates-in-Markets

[Metaculus](https://www.metaculus.com) has put forward the concept of ["fortified essays"](https://www.metaculus.com/project/ai-fortified-essay-contest/): pieces of writing which integrate discuss and contribute to market predictions.

This idea can be taken further. Do you disagree with the public on a market? Don't just trade on that market - create new markets which explain why you think the current market is wrong _by their logical relation to preexisting markets_.

Example: The market thinks candidate A has a 50% chance of winning. But it's a year before the election, and you think that even if they were nominated, which you put at a 50% chance, it's still far too early to say who would win the general election. So you make two new markets, one for whether the candidate will be nominated, and one for whether their party will win the general. If these are independent, the market has to put a 70% probability on at least one of these in order to rationally keep the main market at 50%. So you set up a bot to arbitrage inefficiencies and place limit orders on both markets. You write this all up in a post with special formatting to display the markets, their relationships, and the orders supporting your argument.

## Standardized grading of Informal Predictions

As nice as it would be if every pundit in the world would put their predictions on a prediction market, the reality is that most of them will find an excuse not to. Part of the reason for this is that quantitative predictions are easier to criticize, so that those who make them stand more to lose than to gain.

Perhaps rather than trying to convince these commentators to risk their reputations in a quantitative way, we can pass the buck to them directly by quantifying their predictions for them. I propose a website that tracks the writings of public intellectuals as they are published, and attempts to convert those predictions into trades (either automatically, or through a consensus of humans) made by a bot specific to them. Thus, for every public figure we track, we can analyze their track record by looking at the profits and losses of the corresponding bot.

I anticipate that many public figures, confronted with serious losses from the predictions their bot has made, would attempt to distance themselves from the predictions made by the bot. I think there are a few rejoinders to this:

- The bots should be calibrated to translate informally stated probabilities into numbers accurately on the basis [of studies that analyze this](https://hbr.org/2018/07/if-you-say-something-is-likely-how-likely-do-people-think-it-is). This way the bot can be seen as objective in its assessment of the public figure's predictions.
- Percentages that are directly quoted in the article should be taken as the public figure's own probability estimates. Thus, all a public figure should have to do to get their bot to predict accurately is to quote numbers in their articles.
- Of course, at any time, the public figure can request to assume direct control of the bot, so the locus of control is ultimately directly in their hands.

## Modern Portfolio Theory

[I have made much](https://thequantummilkman.substack.com/p/prediction-markets-eat-bayes) of the benefits of the Kelly Criterion as a risk management system. But perhaps an even better mathematical theory of financial risk is Modern Portfolio Theory. MPT focuses on covariances between assets, making it more mathematically clean. Using [combinatorial markets](https://thequantummilkman.substack.com/p/announcing-the-markets-for-markets), it is possible to make assets that relate to variance, and potentially use these to trade. For example:

- You could make a bot that repositions your holdings by marginally trading on joint outcomes to lower the variance of your portfolio.
- You could search for holdings that are provably irrational from the perspective of risk in the MPT framework and alert the user to them.

These features could be added to the Manifolio UI I described above, or to a separate UI that analyzes a users account without making trades.

## Automatically selling high-value shares

Prediction market users are (usually) not allowed to place purchases that exceed their balance of in-platform currency. This leads to an annoying workflow where to buy a profitable share, you need to first search your portfolio for shares that can be sold to provide the cash.

Why not automate this process? Here's what I propose:

1. When the user inputs an order that would send them to a negative balance, their portfolio is searched for shares closest in value to 1.
2. The user is alerted that their trade will result in the sale of some of these shares.
3. The user will be shown a price as if the value of the shares being sold was 1. For example, if I am selling shares at 99 cents, then the shares I am buying should be shown as being 1% more expensive than they would be if I had a full balance.

<!-- - Artificial unlinked multi markets / binary markets by composing/decomposing other answers.
  - That automatically resolve/re-resolve when the submarkets do.
  - Comes with a bot that trades to keep the prices consistent.
  - [Link](https://discord.com/channels/915138780216823849/1175890970810781697/1199318722456846418). -->

<!-- ### Kelly Buying

Just because bots can see some things faster than humans can, doesn't mean humans can't bring value to the table. Humans have insight into the complex attitudes of other humans which can affect outcomes in markets, elections, &c.

Prediction markets should therefore do everything they can to assist humans to make good decisions. A key part of this is including UIs to Kelly-bet. Humans input an assessed probability, and the UI automatically buys an appropriate amount of that new market. The Kelly-bet interface might even allow for:

- Accepting information on which events a human thinks are independent, or nearly independent.
  - Indeed, this "near independence" could be expressed as an assertion that the joint outcome is within a certain total variation distance of independent, which could then be traded on tensor product markets.
- Rebalance other positions according to new correlation information.
  - Take into account resolution dates when rebalancing, focusing on markets with high profits that resolve soon.

The gold standard would be a UI that allows the user to put in as much information as they like on probability ranges for events, and then automatically computes the portfolio that minimaxes the expected outcome over those probability ranges. -->
