# It's Sometimes Sunny in Philadelphia

[Futarchy](https://en.wikipedia.org/wiki/Futarchy) is a proposed system of government in which prediction markets are used to determine which policies are best.
I have written some prior posts on futarchy and the issues it has with causality.
But this line of criticism is pretty niche - it's far more common to see people dismiss futarchy simply just because it's so radical.
Is it really serious to imagine upending a centuries old political system like American democracy in favor of the idea of one academic economist?

Maybe a good response to this is that instead of upending the system, prediction markets could instead help to improve it from within.
Individuals could use prediction markets to better figure out who to vote for without letting them control policy unilaterally.

But this makes the causal connection between the market prediction and the election outcome even less clear!
This post is partially inspired by this [ACX section on causality](https://www.astralcodexten.com/i/184065379/conditional-markets-a-modest-proposal), which essentially proposes focusing on on the predicted outcomes just before election night to minimize the ability of events to impact post-election outcomes without also being visible to the outcome of the election itself.
This is nice, but as the posts notes, it doesn't handle the possibility that there are economically good things happening the week or month before election day which don't yet show up in polls or statistics, but which nevertheless induce noncausal correlation between good outcomes and election outcomes.
So I'd like to find some approaches that might be more complicated but also more causally sound.
I'll focus on ideas in [quasi-experiment](https://en.wikipedia.org/wiki/Quasi-experiment) which I think is a good conceptual fit for this.

## What is Quasi-experimental design and why is it relevant?

We can think of combinatorial prediction markets as giving us an accurate survey of likelihoods for different combinations of future possibilities, but without the ability to affect these possibilities actively.
The setting of quasi-experimental design is analogous, but for the past instead of the future.
Essentially, a quasi-experiment is just an experiment where we don't have the ability or inclination to assign experimental conditions randomly.
We can only learn about how conditions affect outcomes from observing and trying to reason about the relationship of these and other possible confounding variables.

## Example 1 [Regression Discontinuity Design](https://en.wikipedia.org/wiki/Regression_discontinuity_design)

A good way to explain Regression Discontinuity Design (RDD) is by example, so I'll summarize this [example from an online causal inference textbook](https://mixtape.scunning.com/06-regression_discontinuity) covering [this paper](https://hceconomics.uchicago.edu/sites/default/files/events/Hoekstra_2009_REStat_v91_n4.pdf).

We want to determine if going to college is having a good effect on students.
The trouble is, only the students who perform the best on the SAT go to college, so it might just be that these were good students to begin with and they ended up doing well because of that.
So to figure out what's going on, we chart out the performance of students who didn't get good enough scores to get into the state school and plot a trendline for them and separately plot a trendline for the students who do get the scores.
We notice there's a jump between where we would expect a student who barely missed the admission cutoff to end up, and a student who made the cutoff.
We take it that this is because college itself is causing the students to get better results (after all, why else would there be a jump right at the decision point).

![](https://mixtape.scunning.com/graphics/rdd_hoekstra2.jpg)

Regression discontinuity design seems like a great application to elections.
Election results have a built-in discontinuity: If a candidate gets 47%, 48%, or 49% of the vote, they don't win the office, and if they get 51%, 52%, or 53% of the vote, they do.
It therefore seems like we could easily run an RDD on the prediction market predictions conditioned on vote share to figure out what a candidate's impact would be.

This only captures candidate effects in worlds where the election was really close.
Maybe there's some black swan event which would totally change who would be right for the job, and also totally change who's likely to win.
But I think that this is OK, and maybe even good actually, because it's only in worlds where the election is really close that individual votes will matter at all.

Maybe a concern is that if you get really really close to 50%, all outcomes turn out bad because there is controversy over the election outcome.
This seems like a legitimate concern, but one we could maybe head off by basing our regressions only on scenarios with a vote discrepancy of at least 1% or something.

Another concern might be that you have to create not just a few market combinations for who will win, but markets for each margin, fragmenting liquidity and increasing resolution overhead.
This is legitimate, but prediction markets already seem to like to make markets for margin of victory, so perhaps there is already enough interest in this type of market to make creating them worthwhile.

## Example 2 [Difference-in-differences](https://en.wikipedia.org/wiki/Difference_in_differences)

There's [some](https://journals.sagepub.com/doi/10.1177/1532673X17745631) [studies](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.00929/full) that say that the weather on election day influences voting patterns (turnout, but candiate preference too).
Maybe this looms large in my memory because of that one West Wing episode where the characters all want it to rain on election day.

Weather is subject to collected statistics, which means it should be easy to give a probability over possible states of weather for a city months in advance, but it's also [chaotic](https://en.wikipedia.org/wiki/Butterfly_effect) so it should not be possible to improve much on these models with sophisticated simulation.
This should mean we can make liquid markets on election day weather in important cities in swing states as a basis for conditional markets on election outcomes and policy outcomes.

We can therefore use these markets to look at the difference in multi-year policy outcome predictions for good and bad weather on election day.
Perhaps some of this will be due to how the election is impacted, and some of it is due to mundane concerns like a marginally better or worse crop yield.
But we can also do the exact same process to look at the difference in multi-year policy outcome predictions for good and bad weather on the day *after* election day.
If these are different (i.e. there is a difference-in-difference) then we might posit that the only way that could be is that the election day weather has the special lever of impacting the election that the other weather does not.
Thus, if predicts-party-X-wins-when-it-happens-on-election-day weather also seems to be predicts-particluarly-good-multi-year-outcomes-when-it-happens-on-election-day weather, that is an indication to vote for party X.
