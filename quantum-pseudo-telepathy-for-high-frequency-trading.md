# Quantum Pseudo-Telepathy for High Frequency Traders

## What is quantum pseudo-telepathy?

You may have heard of the concept of "entanglement" [from science media](https://www.quantamagazine.org/tag/entanglement/), but not much about what concretely means for engineers. [Quantum pseudo-telepathy](https://en.wikipedia.org/wiki/Quantum_pseudo-telepathy) is the quintessential capability that entanglement lets you achieve. It can seem paradoxical, in that it appears to allow users to communicate instantaneously, potentially even at latencies faster than the speed-of-light barrier would allow. And in fact, this led Einstein to reject quantum mechanics as a complete description of physics.

But despite its seeming paradoxicality, pseudo-telepathy is ultimately quite simple to explain, so much so that I am somewhat surprised it's not discussed more explicitly in popular coverage of quantum computing. This post explains what pseudo-telepathy allows you to do (completely avoiding the matrix algebra that more thorough descriptions usually use), and ponders potential applications.

## The non-local boxes

Imagine two boxes, connected by a wire. Each box has a left button and a right button, and two lights, one blue and one orange.

As a one-time use feature, when one of the buttons on one box is pressed, one of the two lights on that box will light up at random:

- No matter which button you press, the blue and the orange light will each have a 50%/50% chance of turning on.

TODO image

So far, this is not impressive, so we explain further: There is also an effect of one light result on the other which influences the _correlation_ between the two lights, when buttons are pressed on both boxes (although this does not affect the fact that, for each box individually, the chance of each light is 50%).

- If 0 is pressed on either box, the lights will be the same color with probability 85%.
- If 1 is pressed on both boxes, the lights will be different colors with probability 85%.

TODO image

Note that as described, there is still no paradox here. One could imagine the box working this way: Whenever a button is first pressed on either box, a random color is chosen to light up on that box, and a signal is sent down the wire noting which button was pressed and which color was chosen. Then, when someone presses a button on the second box, it is determined if both presses were 1s and thus whether the lights should be more likely to be the same or different. A random number generator then determines if the 85% outcome should happen or the 15% outcome should happen.

The paradox is this: Using quantum information to construct the box, we do not need the wire, nor any form of communication between the boxes, and they will still work the same way.

## Obligatory Mid-Post Q+A

### How do we really know no communication is going on? Couldn't it be that there are just special particles that we can't isolate, but which are transmitting the same information that the wire would?

The point is that even if the boxes are light years apart and the buttons are pressed simultaneously, the lights behave the same. Relativistically speaking, there would be no possible way for any particle or other signal to move this fast to send this information.

### But wait, isn't what you're describing impossible? Couldn't you use this to send a message back in time and create a paradox?

While I have said this effect seems paradoxical, I haven't said it actually is paradoxical. The key is that from the perspective of someone with just one box, the result is always 50/50 random, it contains no information on its own. It's only when you later see the outputs from both boxes that you see the correlation.

### What is this 85% number, where does it come from?

Technically it's $\cos^2(\pi/8)$, if you want to get into the matrix algebra there is some math you can do to show why you can get this, and some more slightly more complicated math you can do to show you can't do better. There are also a variety of different versions of all this with different numbers of boxes, different numbers of lights or buttons per box, different probabilities, &c. but these are beyond the scope of this post.

## Applications in High Frequency Trading

Computer scientists have come up with a variety of examples of situations where using boxes lets you do better than you would otherwise be able to, without communication. But these "non-local games" tend to be very contrived. Can we come up with a practical application of pseudo-telepathy?

Such an application would have to:

- Involve cooperating parties making decisions sufficiently simultaneously[^1], that the speed of light prevents their communication. If we aren't considering outer space, this means sub-second times between decisions.
- Focus on providing enough value to offset the cost of setting up the equipment. Whoever we pitch our pseudo-telepathy device to, they should probably already be paying a lot for classical communication channels with extremely low latency.

These criteria suggest a very specific application: High Frequency Trading (HFT). This seems like a natural fit, since these firms do try to send messages as fast as possible, and the highly abstract nature of their job makes it easy to make an example of something a quant[^2] might want to do which benefits from pseudo-telepathy.

### The scenario

<!-- Analogy with CHSH
CHSH referee gives x to alice y to bob
if a xor b = x and y, they win

Analogy
x and y = both companies want merger = merger will happen

Under merger conditions investments will be correlated, we want to be involved in exactly one investment (because we want the gains of appreciation, but not to take too much risk)
Under nomerger conditions investments will be anticorrelated, we want to be involved in both or neither  (since no appreciation, but we don't want risk)

(why not just buy half of both)

Let us say that
under merger, the prices will both be m1 w.p. 50% and m2 w.p. 50%
under no merger, the prices will be m3 and m4, with 50% of assigning each to each company

So working backwards:

Under merger, if we buy 2,
    expected log holdings are 0.5 log (2m_1) + 0.5 log (2m_2)
    we doylistly want the Expected log(holdings) to end up at 1
    thus
    0.5 log (2m_1) + 0.5 log (2m_2) = 1
    2 + log (m1m2) = 2
    log(m1m2) = 0
    m1m2 = 1


Under merger, if we buy 1,
    expected log holdings are 0.5 log (1+m_1) + 0.5 log (1+m_2)
    we doylistly want the Expected log(holdings) to end up at 1.208
    thus
    0.5 log (1+m_1) + 0.5 log (1+m_2) = 1.208
    log ((1+m_1)(1+m_2)) = 2.416
    (1+m_1)(1+m_2) = 5.337
    1 + m_1 + m_2 + m_1m_2 = 5.337
    m_1 + m_2 + m_1m_2 = 4.337
    m1 + m_2 = 3.337


Under merger, if we buy 0,
    expected log holdings are log(2)
    we doylistly want the Expected log(holdings) to end up at 1
    check

Solving for m1 and m2, we get 3 and 1/3



Under no merger, if we buy 2,
    expected log holdings are log (m_3 + m_4)
    we doylistly want the Expected log(holdings) to end up at 1
    thus
    log (m_3 + m_4) = 1
    m_3 + m_4 = 2

Under no merger, if we buy 1,
    expected log holdings are 0.5 log (1 + m3) + 0.5 log(1 + m4)
    we doylistly want the Expected log(holdings) to end up at 0.792
    thus
    0.5 log (1 + m3) + 0.5 log(1 + m4) = 0.5 log(3) = 0.792
    log ((1 + m3)(1 + m4)) = log(3)
    (1 + m3)(1 + m4) = 3
    1 + m3 + m4 + m3m4 = 3
    m3 + m4 + m3m4 = 2
    m3m4 = 0



Under no merger, if we buy 0,
    expected log holdings are log(2)
    we doylistly want the Expected log(holdings) to end up at 1
    check

Solving for m3 and m4, we get 2 and 0



 -->

Consider the following scenario: We are a trading firm with offices in New York City and Chicago. We are looking forward to some releases that two competing companies (one based in each city) we have analyzed will be making. Both companies are looking to hire new CEOs specializing in mergers. We have determined that if both companies successfully hire such a CEO, it is certain that the two companies will merge in the near future, and their stock prices will be highly correlated moving forward. On the other hand, if one of the companies fails to hire, then a merge won't happen, and at least one company will likely soon go bankrupt and cede their market share to the other, so the stock prices will be anticorrelated.

When our AI analyst reads these reports, which will release simultaneously in the two different cities, it will know in microseconds whether each company will be hiring such a CEO. In each case, we think that there's a 50% chance the hire happens.

Each office's AI will then have to decide whether to buy stock in the nearby company. It will have only microseconds to do so, since we expect that

If the companies do merge, we'd ideally like to be invested in just one of them, since the stock will be interchangeable anyway

<!-- We have $1M in each exchange available to invest in trying to buy this opportunity. Since we are in this business for the long term, we are interested in [maximizing the expected logarithm of our total wealth. Luckily, we know](https://en.wikipedia.org/wiki/Kelly_criterion) that the best thing to do when we have a 50% chance to triple our wealth is to spend 25% of our bankroll.

But complicating things further, other firms may have already known about this information, and if so, they will almost certainly have traded the stock up in either New York, Chicago, or both, in the milliseconds before the press release went public. If they have done this, it will be obviously reflected in the price, but it will remove any opportunity for expected profit. We assume that there's a 50/50 chance that by the time we communicate with our office in NYC, the buying opportunity will still be available, and independently, a 50/50 chance that it will be available in Chicago. -->

### Without the non-local boxes

Let's first examine our best strategy when we don't have access to the boxes.

In this case, our only decision is how much to spend in each location, if the buying opportunity is still available. We can optimize over the four outcomes

### With the non-local boxes

## Open questions

[^1]: "Spacelike interval" in the parlance of special relativity.
[^2]: Pun intended
