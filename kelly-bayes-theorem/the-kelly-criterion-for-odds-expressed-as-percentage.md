# In-your-head Kelly calculation for prediction markets

If you follow this blog, you will have already read about the [Kelly criterion](https://en.wikipedia.org/wiki/Kelly_criterion), which is a strategy for choosing what fraction of your bankroll to allocate to a bet or investment.
This post is to highlight a formula for calculating the Kelly fraction when you are making a bet on a liquid prediction market (binary option/arrow-debreu security).
In such a situation, you know the current market price $p_{market}$, and your own assessment of the correct price $p$.
The Kelly fraction in such a case is:

$$
  f^{*} = \frac{p-p_{market}}{1-p_{market}}
$$

In other words, you take the difference between your assessment of the probability of YES and the market's assessment of the probability of YES, and you divide by the difference.
If you are comfortable conceptualizing the "difference between assessments" into a single variable, you could write this even more simply as

$$
  f^{*} = \frac{\Delta p}{q_{market}}
$$

## How to remember this

This seems easy to remember by the following approach: If my assessment of the probability was $p=1$ (i.e. if I thought the market was 100% about to resolve YES) there would be no reason not to put all of my money into the market, and I would choose a Kelly fraction of $1$.
If my assessment of the probability was $p=p_{\market}$ (i.e. if I thought the market price was correct and there was no expected profit to be made by betting) there would be no reason not to bet at all, and I would choose a Kelly fraction of $0$.
If my probability is between these two extremes, the Kelly fraction is just the coefficient for the linear interpolation.

## Worked examples

Let's say the market is at 60%, and I think that the true probability is 70%.
I know that 70% is one-quarter of the way between 60% and 100%.
So the Kelly fraction is 1/4.
Let's say the market is at 33%, and I think that the true probability is 67%.
I know 67% is halfway between 33% and 100%.
So the Kelly fraction is 1/2.
Let's say the market is at 95%, and I think that the true probability is 98%.
I know 99% is 4/5 between 95% and 100%.
So the Kelly fraction is 4/5.

## Derivation

The more common way(s) of presenting the formula are variants of $f^* = p - q/b$, where $b$ is an odds ratio for the bet.
Let's derive the formula above from the formula as [presented on wikipedia](https://en.wikipedia.org/wiki/Kelly_criterion#Investment_formula):

> A more general form of the Kelly formula allows for partial losses, which is relevant for investments:

$$
  f^{*} = \frac{p}{l}-\frac{q}{g}
$$

where:

- $f^{*}$ is the fraction of the assets to apply to the security.
- $p$ is the probability that the investment increases in value.
- $q$ is the probability that the investment decreases in value ($q = 1 - p$).
- $g$ is the fraction that is gained in a positive outcome.
  If the security price rises 10%, then $g = \frac{\text{final value} - \text{original value}}{\text{original value}} = \frac{1.1 - 1}{1} = 0.1$.
- $l$ is the fraction that is lost in a negative outcome.
  If the security price falls 10%, then $l = \frac{\text{original value} - \text{final value}}{\text{original value}} = \frac{1 - .9}{1} = 0.1$

> Note that the Kelly criterion is valid only for ''known'' outcome probabilities, which is not the case with investments.
> In addition, risk averse investors should not invest the full Kelly fraction.

(Note that Wikipedia also has a ["Gambling Formula"](https://en.wikipedia.org/wiki/Kelly_criterion#Gambling_Formula) which is structure exactly as the above, except that $l$ is taken to be 1, and $g$ is notated as $b$, I don't get why the redundancy is needed.)

In the case of prediction markets, we have

- $p$ is the (true/my/the bettor's) probability that the event occurs (the investment increases in value)
- $q = 1 - p$
- $l = 1$, since in a prediction market, if you lose the bet, you receive no payout.
- $\text{original value} = p_{market}$, since this is the cost of a share
- $\text{final value} = 1$, since shares pay out 1 if they resolve YES.
- Therefore $g = \frac{1 - p_{market}}{p_{market}}$

Then we plug in and get

$$
  f^{*} = \frac{p}{1}-\frac{(1-p)}{\frac{1 - p_{market}}{p_{market}}}
$$
$$
  f^{*} = \frac{p}{1}-\frac{(1-p) p_{market}}{1 - p_{market}}
$$
$$
  = \frac{p (1 - p_{market}) - (1 - p) p_{market}}{1 - p_{market}}
$$
$$
  = \frac{p - p p_{market} - (p_{market} - p p_{market}) }{1 - p_{market}}
$$
$$
  = \frac{p-p_{market}}{1-p_{market}}
$$

Which is the formula I wrote.

## Is it really that simple?

As I write this post, I feel like I am going a little crazy.
People have [made](https://www.albionresearch.com/tools/kelly) [websites](https://kellycriterioncalculator.com/) to help you calculate the Kelly criterion, and there is even [one for Manifold](https://github.com/Will-Howard/manifolio/).
[Other](https://www.investopedia.com/terms/k/kellycriterion.asp) [explainers](https://thezvi.substack.com/p/the-kelly-criterion) I [found](https://streetfins.com/the-kelly-criterion-explained/) tend to state the formula in terms of win-loss ratio, as Wikipedia does.
I somehow assumed that this meant that calculating the Kelly fraction was a hard task that required translating back and forth between probabilities and odds ratios at least once.
I had been thinking about writing a post to give the explicit formula solely in terms of probabilities for a while as a reference for doing this,
but I somehow never realized until today that the formula was this simple and easy to remember.

I also like percentages better than odds ratios in general because you don't have to figure out/remember whether 12-to-1 odds means 1/12 or 1/13 or 1/13 or 12/13.

## Bonus: Fractional Kelly

Here's a tie in to my previous post on the relationship between [Bayes' rule and market pricing](https://thequantummilkman.substack.com/p/prediction-markets-eat-bayes).
In that post, [I referenced](https://thequantummilkman.substack.com/p/prediction-markets-eat-bayes) the post ["Never Go Full Kelly"](https://thequantummilkman.substack.com/i/149861175/no-seriously-never-go-full-kelly), which notes that "fractional Kelly betting" with parameter $\alpha$ can be interpreted as betting on the Bayesian meta-prior that there is a $1-\alpha$ chance that the market probability is right, and an $\alpha$ chance that you are right.
The formula here gives us the chance to check that the two interpretations are consistent: If I update my probability estimate in this way, I am indeed exactly changing the $\Delta p$ by a factor of $\alpha$, so the Kelly fraction changes multiplicatively.
In fact, reading "Never Go Full Kelly" more closely, I see it actually presents Kelly using the percentage formula and not the odds formula!
So I think this is another compelling case for both reading that post and viewing market pricing as linked to Bayesian reasoning.

<!-- 

### Kelly criterion for a dependent/exclusive multi-outcome event

What if there is a liquid market analogous to a Manifold multi-choice, where only one of the outcomes can occur?

This seems like it might be complicated - you obviously don't want to buy any yes in shares where your probability is less than the market's probability.

See [this ref](https://vegapit.com/article/kelly-criterion-multiple-mutually-exclusive-outcomes).
 (Is the math there right? Seems like the partial derivative calculus is wrong)

 TODO 
-->
