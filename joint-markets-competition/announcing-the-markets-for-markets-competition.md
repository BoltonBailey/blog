
# Announcing the Markets-for-Markets Competition

*This post is about Prediction markets run by [Manifold](https://manifold.markets/home). If you don't know what a prediction market is, you might want to learn about them [here](https://docs.manifold.markets/faq).*

As a part of Manifold's recent effort to subsidize high-interest markets, I am running a competition. This competition will involve the design of market criteria to help learn more about events that Manifold users consider interesting and important. The tournament will have a prize fund of Ṁ8000, with a total of Ṁ5000 going to the winner.

A few words about the motivation for this competition. Prediction markets are, by their nature, *quantitative* sources of information. They elicit information that traders possess by offering to buy and sell shares, and they continually process new trades to update a numerical probability for the event they track. But what this system lacks is a reflection of what was behind the trades. What information did the traders use to make their decisions? What factors did they consider the most important?

## Manifold's Great Strength: User-generated markets

Part of what makes the Manifold platform so great is that they have a built-in solution for this: Manifold users can make their own markets. When I see people ask questions and give explanations in the comments of a large market, my first reaction is often "they should make a market about that idea". Often, someone will make that market.

But there's a further step which I don't see taken as often, and this comes to the heart of the competition I am announcing today. When we make additional markets as part of an investigative process, we should make sure that that market is connected to the event we started with. In my opinion, the best way of doing this is through what I call a "joint market".

## Conditional and Joint Markets

Joint markets are related to conditional markets. Conditional markets are common seen around manifold - the title of one of these markets is usually phrased as "If \<such-and-such-event-happens> will \<other-event-happen>?". Here is an example:

<iframe src="https://manifold.markets/embed/NcyRocks/if-biden-wins-in-2024-will-he-serve" title="If Biden wins in 2024, will he serve a full second term?" frameborder="0" width="600" height="300"></iframe>

The point of a conditional market is to understand how one outcome impacts another. If event A happens, then the market resolves as normal. If event A does not happen, the market resolves N/A which means all trades are reverted and users get back any money they spent on the market. Users can therefore bet on the market as if they were certain that A would happen.

Conditional market track conditional probabilities. By analogy, joint market track joint probabilities. The simplest form of joint market is a multi-choice market with four outcomes, which correspond to outcomes from two other Yes/No markets. Here is an example of one of my joint markets:

<iframe src="https://manifold.markets/embed/BoltonBailey/will-a-democrat-win-the-2024-us-pre-f7bdb63135a1" title="Will a Democrat win the 2024 US Presidential Election? // In Pennsylvania?" frameborder="0" width="600" height="300"></iframe>

You can go even further and have a joint market on three or more outcomes:

<iframe src="https://manifold.markets/embed/MartinRandall/trump-vs-biden-2024" title="Trump vs Biden 2024" frameborder="0" width="600" height="300"></iframe>

There are pros and cons to using joint markets over conditional markets, but I think that joint markets are usually better. One key reason for this is that for any position you hold in a conditional market, it's possible to take a position in a joint market which is *identical in value, no matter the outcome*. Simply track how much your payoff or refund would be in the conditional market and buy the same amount of YES in shares of the joint market outcomes. By the same token, a joint market on events A and B lets you know the same information that any conditional market on the same event gives you.

## The competition

With that, let met get into the details of the competition I am hosting. In one sentence, the competition is about who can make the best joint probability market.

### How do I enter?

Enter by making a joint probability market and posting it in the comments of the main tournament market.

<iframe src="https://manifold.markets/embed/BoltonBailey/who-will-win-my-joint-markets-conte" title="Who will win my joint markets contest?" frameborder="0" width="600" height="300"></iframe>

As an additional bonus incentive to make more joint markets, I will be using most of the Ṁ50000 fund to subsidize any joint market linked there (even ones that don't meet the additional criteria to be considered for the prize). If you want to participate, but you don't want to spend the mana you can also ask me to make the joint market for you, and I will do so out using the fund.

### How will I decide which joint markets win prizes?

There are a few baseline criteria I am setting for markets to be eligible for a prize, mainly to ensure that the tournament can be concluded in a somewhat objective fashion by the end of the year.

* The joint market have four outcomes that must directly reference two other Yes/No manifold markets, both of which must resolve (or be obviously intended to resolve) "Yes" or "No" rather than "N/A" or "Prob".
* The first of these markets to resolve must resolve on or before 2024-01-01 anywhere on earth.
* The second of these markets to resolve must resolve *no earlier than* 2024-07-01 and have at least 100 distinct traders by 2024-01-01.
* The markets shouldn't be overly artificial. This is somewhat subjective, but a market phrased as "This market resolves YES with probability equal to \<some-criterion-that-maximises-performance>" would be DQ'ed for this reason.

Among joint markets that meet these criteria, I will rank which ones are the best by averaging the [mutual information](https://en.wikipedia.org/wiki/Mutual_information) implied by the joint market over the November - December timeframe. Rather than give a full summary of the math behind this metric, I'll just let curious people read that linked Wikipedia article. For people who don't want to read the article, I'll summarize the key points.

* It's calculated as a mathematical formula of the four joint market probabilities
* It's higher when the two related markets are highly *uncertain* (that is, closer to 50%)
* It's lower when the two related markets are *unrelated*

So try to find an event to make a market about which is both itself uncertain, while at the same time being predictive of the popular market you are targeting.

The prize pool will be distributed as follows:

* First place gets Ṁ5000
* Second place gets Ṁ2000
* Third place gets Ṁ1000
