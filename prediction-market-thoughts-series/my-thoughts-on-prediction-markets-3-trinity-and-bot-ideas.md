# Prediction Market Thoughts part 3: The Holy Trinity of Bots

I previously posted my thoughts on [backend](https://thequantummilkman.substack.com/p/my-thoughts-on-prediction-market) and [frontend](https://thequantummilkman.substack.com/p/my-thoughts-on-prediction-markets) features I'd like to see in prediction markets.
This post will cover my thoughts on bots.

## The three types of bot participation in prediction markets

This post is partially inspired by Ozzie Gooen's post [here](https://forum.effectivealtruism.org/posts/pLkFmWP3xmGG8YvjP/ai-for-resolving-forecasting-questions-an-early-exploration) on using bots to resolve questions.
This is a cool post, but I feel like it's only one part of the puzzle.
In my mind, there are three main types of bots that could be useful in prediction markets:

1. Question Creation Bots.
   These bots define resolution criteria for markets.
2. Trading Bots.
   Bots that make trades.
3. Question Resolution Bots.
   Bots that resolve questions, as Gooen discusses.

I feel strongly not just that each of these avenues for bots is underexplored, but that **having all three types together in a single ecosystem realizes some important synergies**:

- Scale: A theme of this blog is that [prediction markets are information-theoretical constructs with the ability to learn](https://thequantummilkman.substack.com/p/prediction-markets-eat-bayes).
  But learning requires lots of data to learn from, which means lots of markets and predictions.
  If we can have prediction market platform that functions end-to-end without human intervention, we can potentially get to a new level of scale.
- Inconsistency: Bot-generated market can be uninteresting or ambiguous, and bot resolutions can be incorrect, which makes these markets unappealing to humans.
  But bot traders don't care about this type of friction and can potentially learn to adjust to it better than humans can.
- Retrodiction: If an LLM has a data-cutoff date, we have good reason to believe a bot based on that LLM would not have any special advantage in predicting events after that date.
  Similarly, that any markets proposed by such a bot would not, by their existence on the platform, offer predictive power.
  This leads to the intriguing possiblity of letting a variety of such bots compete in a retrospective simulation of a prediction market over a period of years before the present, where the bots in the market are gradually fed news from news sources one date at a time.

To paint with a broad brush: Systems optimized for machines are different from systems optimized for humans, so we should explore what a reorientation of the prediction market ecosystem would look like as a radical change of design space.

<!-- This isn't to rule out human involvement in prediction platforms that orient towards bots - I think a human factor could help to keep things on track. Of course, there's also a balancing act to be played, since if the AI generated markets are too "sloppy", humans won't want to participate. Hopefully a happy medium can be reached where humans who don't mind LLM-speak can surface the best written markets for the rest of the community. -->

## Question Creation Bot Idea

Manifold already offers AI assistance in creating markets, but this usually starts with human prompting.
What could a more autonomous market creation engine look like?

Most prediction markets pertain to events covered in the news.
Consider a bot that works on something like the following prompts:

> You are a master prediction market creator.
> It is your job to create prediction markets that are interesting, have clear resolution criteria, and which are relevant to events in the news.
> Today, you will be creating a title for a prediction market based on the following news article.
>
> **Insert news article here.**
>
> Please brainstorm a future event that might or might not come to pass relevant to the content of this article.
> Here are some examples of the types of events you might track, based on previous articles
>
> **Insert zero-shot examples**
>
> All the information relevant to decide if the market has resolved yes or no should be publicly available by **Date**.
>

> Here is a title and date for a prospective prediction market.
>
> **Title and date**
>
> Now please write resolution criteria for the market you have just titled.
> The resolution should be clear and unambiguous: Anyone who is familiar with the events in question after the resolution date should be able to agree on how the market should resolve.
> Please also include a list of URL sources that could be accessed on the resolution date that could be used to resolve the market.

## Trading Bot Ideas

There is a nice post [here](https://www.alignmentforum.org/posts/uGkRcHqatmPkvpGLq/contra-papers-claiming-superhuman-ai-forecasting) that criticizes [some](https://arxiv.org/pdf/2402.19379) [prior](https://arxiv.org/pdf/2402.18563) [literature](https://drive.google.com/file/d/1Tc_xY1NM-US4mZ4OpzxrpTudyo1W4KsE/view) [on AI forecasting](https://www.arxiv.org/pdf/2408.12036).
As far as I can tell, the forecasting bots in these articles all work by a straightforward RAG pipeline where they request news articles from a search engine and then are prompted to base a prediction off of the articles.

The post highlights three things that the AIs have problems with \footnote{and a fourth way which just creates noise, namely data leakage}:

- The AI fails to find up-to-date information on the questions
- The AI finds only low-quality information on the questions
- The AI lacks high-quality quantitative reasoning

Given the architecture of the bots in question, these problems seem pretty unsurprising.
But perhaps this leaves the door open for more sophisticated bots that work better.

In particular, I notice that many of the strategies I personally use to trade are amenable to replication by a bot, but probably not by a bot of the type described above.
So consider this section my alpha dump.

### Using price data from other markets to inform trades

I very frequently use prices of other markets to help me determine trades.
Sometimes this involves determining a price for a thinly traded market by taking averages of similar big markets.
Other times it involves directly arbitraging markets against each other.
Strategies of this type clearly fight back against the out-of-date-info and no-quantitative-info problems.

I could imagine both a "soft" form which identifies markets which are similar-but-not-the-same and analyzes correlations to keep the price vector close to its principal components, and a "hard" version which locates and rigorously vets identical markets or markets where an outcome on one implies an outcome on the other and arbitrages these directly.

<!-- 
Consider the following strategy for a bot.

1. Identify the top markets on the platform by volume/liquidity.
2. For each pair of markets, ask the LLM if they are correlated or anticorrelated.
3. Take some of the pairs that score highly on the volume/liquidity/LLM-assessed correlation.
4. Make a private 2x2 combinatorial market on the two markets.
5. Initialize the prices of the 2x2 market so that the marginal prices of the two markets as the main markets predict, and so the events are almost, but not totally, correlated. There should be a slight correlation in the direction the LLM suggests.
6. As time goes on, arbitrage the markets against each other.

I feel there's a chance this could be profitable, on the basis of how it would be able to use information from one market on another. -->

### Identify markets that experience time decay

Many prediction markets can be expressed with titles of the form "Will X happen by Y date?".
It does not seem too hard to get an LLM/regex to consistently identify markets of this form.
We can then look at the price: If a market like this is unresolved and not at an extremely high price, it is usually a safe bet that "X" has not happened yet.
The prices of such markets should then decay over time, but one often finds (at least on Manifold) markets that haven't been traded in a while.
This suggests that a bot could trade on the information of the previous price.

A typical way to model this might be to assume that "X" events happen according to a Poisson process.
We can then infer the rate of this process from the time and price of the last trade, and extrapolate what the price should be now.
Of course, there is the risk that the event is more likely to happen on certain dates than others - perhaps this could also be dealt with by asking the LLM a question like, "which of these dates is the most likely for X to happen?"
and using that to inform the model.

### Calibration Bots

In an [earlier post](https://thequantummilkman.substack.com/i/167659639/going-meta-why-predict-rather-than-aggregate) I advocated avoiding calibration analysis in favor of analysis of particular trading strategies.
Perhaps the synthesis of this is: We should have more calibration bots - bots which specifically analyze calibration and make bets to correct miscalibration.
There are a few possible flavors:

- Sitewide calibration
- Topic-by-topic calibration
- User-by-user calibration (i.e. identify fish)
  - The Manifold house bot once did this, which is in retrospect somewhat ironic, since this seems like one of the worst ways to make a profit in terms of keeping new users interested.
    But this is less of a problem in a bot-centric platform.

<!-- 
- System to arb between duplicated markets on other platforms?
  - like
    - [Polymarket](https://polymarket.com/)
    - [PlayMoney](https://playmoney.dev/)
  - How to ensure profitability? An interesting question.
- Smooth out the curve of limit orders. 
-->

## Market Resolution Bot Ideas

Much is already covered in the [post](https://forum.effectivealtruism.org/posts/pLkFmWP3xmGG8YvjP/ai-for-resolving-forecasting-questions-an-early-exploration) I mentioned above.
I'll try to keep to ideas not discussed there.

### Combinatorial Markets

I have already written about these [here](https://thequantummilkman.substack.com/i/163818132/a-bot-to-automatically-manage-combinatorial-markets) and [here](https://thequantummilkman.substack.com/i/157285480/logical-composition-of-pre-existing-markets).
But it's imporant to realise that this is a type of market resolution strategy that is totally automatic, yet relatively rare on most platforms today.

### Combinatorial choice of LLMs and Resolution Sources

To extend this idea: In designing an LLM/RAG based resolution bot, one might consider questions of which LLM or data source is best, or if there are effective ways of aggregating multiple choices into a single resolver.
But another approach is to simply create multiple different markets, each with a different combination of LLM or data source choice.
From here, we can already implement simple aggregation schemes like majority vote using combinatorial market over the individual resolutions.
Ideally, traders would have the chance to learn more about the nuances of the different systems, and the "best" resolvers (in terms of the usefulness of their resolution decisions in predicting further outcomes) would win market share.

### Lazy resolution

Already on Manifold there are [many](https://manifold.markets/IsaacKing/is-the-wolf-and-sheep-chess-variant) [examples](https://manifold.markets/BoltonBailey/how-many-prime-factors-does-the-180) of [questions](https://manifold.markets/BoltonBailey/how-many-multiplications-are-requir) which are "decidable" in the computational sense.
And one could imagine much more technologically useful questions than these (for example, about whether certain training regimes for ML models will produce certain levels of performance).

The downside of such markets is their uncertain resolution date.
But as time goes on and compute becomes cheaper, markets like these will only become easier to resolve.
One could imagine that joint markets over the time of resolution and the answer could be insightful.
One can even think of integrating formal proof into the resolution procedure to allow for the avoidance of "brute force", but that's best left to a future post.
