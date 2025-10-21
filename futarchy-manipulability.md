
# Futarchy and Manipulability

I recently made a contribution to the ongoing [futarchy](https://mason.gmu.edu/~rhanson/futarchy.html) debate, lately focused on causal structure, with a post about the underdiscussed question of decision market payout structure.

There is yet another criticism of futarchy which has to do with incentives and manipulability, which was brought up in the [comments](https://manifold.markets/post/futarchy-would-be-better-with-combi#89luNZOu). Since I'm on a roll here, I'll discuss my thoughts on this today.

## Links to arguments (and TL;DR)

Here's [a previous mooting of this objection from blogger Sunil Suri](https://sunilsuri.substack.com/p/futarchy) and [Hanson responding](https://www.overcomingbias.com/p/response-to-suri-re-futarchyhtml):

> > (The rich) could buy policies that advantage them outside the realm of the speculative market. They can do this by purchasing yes options en masse and shorting selling no options.

> This is [the](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.359.9664&rep=rep1&type=pdf) [famous](https://marginalrevolution.com/?s=manipulation) [problem](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-0335.2008.00734.x) of “manipulative traders”, which has been addressed repeatedly by theory, lab experiments, and field experiments. Actually, the more traders expect manipulators to try to influence prices, the more accurate that prices get.

<!-- First link is also paywalled, but I think it's https://arxiv.org/abs/2204.13424 -->

[Here is a non-paywalled version of Hanson's last link](https://mason.gmu.edu/~rhanson/biashelp.pdf), to his paper "A Manipulator Can Aid Prediction Market Accuracy".

## My thoughts

Hanson's comment doesn't really resolve my concerns about this. As far as I can tell, the papers he links don't discuss markets that potentially revert their trades, which I think is key to the best version of the objection being raised here. Unfortunately, the post from Suri isn't really clear, so to spell it out: Rather than *both* buying YES in the pro-rich market and NO in the anti-rich market, what the rich could do would be to *only* buy NO in the anti-rich market. If the coalition that does this has enough money, then no other pool can brong the price of the market back up to its correct value, and so the market does not revert, and no one in the coalition loses money. So nothing changes, and the futarchy can get perpetually stuck in a suboptimal condition.

Would the wealthy short a particular option en masse if they won't profit from it? Perhaps they could do so for the same reasons that people vote in democracies, even though it takes time and an individual is unlikely to personally benefit from it. People feel that they should act in a way to benefit others like them. They might not even think that they are mispricing the anti-rich market - they might believe, as many do, that what's good for people of their class will be good for the country in the long term.

Wouldn't the same biases also cause them to buy YES in the "pro-rich" market and lose money that way? Maybe so. But we could posit that "pro-rich" policies are the status quo, and that everyone feels confident they are correctly priced for that reason.

## A model using risk

But if we want to rule out bias, I think it's plausible that such a coalition could arise naturally due to the desire to hedge risk.

Let me spell out a model of the problem in more detail:

1. There is some choice between A and B that the Futarchy must make, to optimize some objective around the general propsperity of the nation. 
2. Choice A would be better to the futarchy overall compared to B if implemented, but would impact the rich more negatively. 
   1. For a blatant example, "A" might be "raise taxes on the rich". Let us say the probabilities are
      1. If taxes are raised on the rich, 51% that general national prosperity will go up and 49% that it will go down
      2. If taxes are not raised on the rich, 49% that general national prosperity will go up and 51% that it will go down.
3. The rich consider ways to hedge their wealth on the futarchy markets. 
   1. Due to [convexity of preferences](https://en.wikipedia.org/wiki/Convex_preferences), their primary concern is mitigating the very worst possible outcome. The worst possible outcome for the rich is that taxes will be raised and general prosperity will go down. They find it much worse to be taxed in the case where prosperity goes down than not, because this prevents them from having the money they need to best isolate themselves from the day-to-day effects of low prosperity.
   3. Therefore, they buy shares disproportionately in the outcome that prosperity goes down if the wealth tax is raised, because this prevents the bad outcome where they are in a low prosperity environment without money.
   4. This lowers the futarchy's perception of the probability that raising taxes on the rich will help GDP to 47%.
   5. Even if the non-wealthy do the analogous thing and bet on taxes not being raised and GDP going down, because the poor have less total money, they do not distort the raise taxes market as much as the rich distort the flat taxes market.
   6. Because all this happens on such a wide scale, no one individual, or even a moderately sized interest group (of rich individuals or otherwise), has enough money to correct the prices

This model doesn't seem too hard to mathematize - however you do it, it seems like (for at least some values of 51%) the hedging activity of the wealthy will drive the policy "raise taxes on the rich" below "don't raise taxes on the rich" in the futarchy's decision calculus. So taxes aren't changed, even though this is objectively worse.

## Interpretations

I think there are a few possible reactions to this.

### The anarcho-capitalist view

The anarcho-capitalist view is that people hedging against the outcomes of the futarchy is actually a good thing: It lets people mitigate or prevent the worst outcomes for them using money. If the wealthy are the ones who are most able to do this, then that is their right - after all, isn't the whole point of having a system of money to reward those who do the most to acquire it by engaging in mutually gainful economic activity with the ability to spend it on what they choose?

Putting aside philosophical disagreement with that position, the only trouble is that when you buy things with money in an anarcho-capitalist system, you are generally supposed to lose the money you pay. The wealthy haven't paid here, because their trades are reverted.

### Switching wealth for non-wealth

In the example, I frame the two groups as "the wealthy" and "the non-wealthy". But if you pay close attention, you'll notice that the key feature needed for the argument to work isn't that the individuals who make up the group in favor of policy B are wealthy, but simply that they make up a majority of wealth. So, you could potentially flip the script and instead divide society into "the masses" and "the 0.1%" or "the majority" and "the minority".

Is this reasonable? Maybe one reason why this feels less intuitive is that it seems like this hedging activity seems like a procedure that would only be available to someone from a social class with bandwidth to spend on abstruse financial procedures - perhaps this is the real dividing line here. But it also seems like whoever sets the policy options also gets influence over how these dividing lines are drawn, and so perhaps they have a lot of power in a futarchic system.

### Transfer

Perhaps part of why this is a bad showing for futarchy is that the problem we are looking at seems to deal with wealth transfer, so it's inherently setting up a kind of game that is largely zero-sum, and which is possible to contrive in ways that turn out badly. [Hanson has written some about situations like this here](https://www.overcomingbias.com/p/futarchy-and-the-transfer-problem) - perhaps a more complex structure for the futarchy could lead to a solution?

<!-- 
Math?
1. There is some choice between A and B that the Futarchy must make, to optimize some objective. 
   1. Let us assume that this is a combinatorial futarchy as described in my previous post.
   2. To further dispense with questions of causality, let's suppose we use
2. There are two classes to which traders belong "wealthy" $X$ or "non-wealthy" $Y$.
   1. All traders have an initial wealth level $w_{x}, w_{y}$ and an interest in the decision which can be quantified in monetary terms $v_{x,A}, v_{x,B}, v_{y,A}, v_{y,B}$, all determined by their class. 
   2. The utility of any given trader is given by the logarithm of the sum of their final wealth level and their interest in the decision made.
   3. Traders trade in such a way as to maximize their expected utility at market clearing prices.
-->






