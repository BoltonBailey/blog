# Computability of Moser's Worm Constant

[Previous post on Moser's worm problem here](./a-computational-approach-to-mosers-worm.md).
In that post I didn't give very strong justification for why the approach I described would successfully make progress on the problem.
Mostly my intuition for why this should be true was that it seemed like the approach was just a straightforward extension of the approach that previous lower bounds had used, but with the ability to take it farther by writing code to do it automatically.

Thinking about the problem computationally raises the **Question** of whether the number we are looking for is [computable](https://en.wikipedia.org/wiki/Computable_number) in the sense that there is an algorithm to approximate it to within any desired positive epsilon.
I haven't been able to find an explicit answer to this question in the literature, but I think I have a proof that the answer is yes (maybe it's just considered obvious enough that writers don't discuss it).
This post will describe the algorithm and hopefully give a better sense of what it would actually take to improve a bound.

## The Blaschke selection theorem

The [Blaschke selection theorem](https://en.wikipedia.org/wiki/Blaschke_selection_theorem) is used to prove that the minimal area in the Moser worm problem is obtained.

> A succinct statement of the theorem is that the metric space of convex bodies is locally compact.

Inspired by this, perhaps we should think in terms of covering the space of *worms* compactly.
That is, we should show that it is possible to find (computably, as a list of polygonal worms with rational vertices) a finite set of worms so that any worm is within epsilon in of some worm in the set.

## An $\epsilon$-net of worms

My claim is that the set of polygonal worms with at most $k$ vertices belonging the grid of points $\delta \ZZ \times \delta \ZZ$, with $k, \delta$ sufficiently (large / small) satisfies this (in the sense that any worm is contained in the epsilon thickening of such a worm)^[Technically I think the notion of distance in the Blaschke theorem is Hausdorff metric, but this is the notion we want here].

Treating length-1 worms as 1-Lipschitz functions from the unit interval, take a worm $f: [0,1] \to \RR^2$.
Consider $\tilde{f}$ defined by taking $\tilde{f}(n/k)$ for $n \in {0, ..., k} to be the nearest grid point to $f(n/k)$, and linearly interpolating between these points.
Then $f$ is contained within the $1/2k + \delta/\sqrt{2}$ thickening of $\tilde{f}$: For any point $x$ in the unit interval, $x$ is within $1/2k$ of some number of the form $n/k$, so $f(k)$ is within $1/2k$ of f(n/k)$, which is within $\delta/\sqrt{2}$ of $\tilde{f}(n/k)$.

Now, the nearest-grid-point operation might make the length of any segment as large as $1/k + \sqrt{2} \delta$.
So the Lipschitz constant of $\tilde{f}$ is $1 + \sqrt{2} \delta k$ rather than 1 as desired.
But this should not be a big deal - we can just shrink $\tilde{f}$ by a factor $1 + \sqrt{2} \delta k$ and make sure to choose $\delta$ much smaller than $k$ is large, (and leave some portion of our $\epsilon$ to account for the change in location of the points arising from this shrinkage).
This results in a grid with a new slightly smaller $\delta$, where the grid-vertex-worms cover everything.
There are only finitely many such worms up to translation because there are only finitely many grid points within 1 of the origin.

<!-- Now for any $x \in [0,1]$, the distance from $f(x)$ to the corresponding point $\tilde{f}(x)$ is at most $2\delta k + \delta + 1/k < \epsilon $. Therefore, we may choose $k > 2/\epsilon$ and $\delta$ sufficiently small that the point in the original worm is within $\epsilon$ of the point in the new worm.
\qed -->

## Why is this covering useful for computing the Moser constant?

Instead of the minimal convex cover for the set of all worms, we could try to compute the minimal convex cover of just the worms in a set $S_\epsilon$ with this property that any worm (with one endpoint on the origin, say) is contained in the epsilon thickening of some worm in $S\_\epsilon$.
Suppose we could successfully compute this minimal convex cover and its area $A_\epsilon$.
We then have an upper and a lower bound on the Moser covering constant:

- $A_\epsilon$ itself would be a lower bound, because any moser set must cover the worms in S.
- We have an upper bound in the area of the epsilon thickening of the cover, because if we epsilon thicken the cover, the result will cover the epsilon-thickenings of every worm in S, and therefore cover every worm.

And we also know these bounds are close: By the [Minkowski-Steiner formula for convex plane sets](https://en.wikipedia.org/wiki/Minkowski%E2%80%93Steiner_formula#Convex_sets), the area of the thickening of the cover is exactly `epsilon * perimeter_of_cover + pi epsilon^2` more than the area of the cover.
If we do our trick from last time of assuming the sidelength 1/3 square is in the set $S_\epsilon$, then the minimal cover can't contain a point at distance \pi/2 from the center of this square without becoming larger that previous established upper bound on Moser set size.
Thus, the perimeter is at most \pi^2, and we can explicitly bound the difference in sizes by

$$
  \epsilon \pi^2 + \pi \epsilon^2
$$

The current gap between the best known lower and upper bounds is

$$
  \pi/12 - 0.232239 = 0.02956
$$

So to get $\epsilon \pi^2$ this small, we would need $\epsilon' \approx 0.003$.
Perhaps this is good evidence that this length scale is close to the precision we need in our numerics.

## Putting it all together

Thus, to compute the Moser solution to within $\epsilon$:

1. Find $epsilon'$ such that $\epsilon' \pi^2 + \pi \epsilon'^2 < \epsilon$.
2. Compute an $S_\epsilon'$.
3. Compute the area $A$ of the minimal cover of $S_\epsilon'$ and take $A, A + \epsilon$ as the bounds.

The last step is the only one we haven't explained: The point is that whether that value $A$ is the area of the hull of a set of polygons $S_\epsilon'$ is a proposition that can be expressed as a formula in the first order theory of the reals.
Computing A exactly as an algebraic number is therefore possible using real quantifier elimination / [the Tarski-Seidenberg theorem](https://en.wikipedia.org/wiki/Tarski%E2%80%93Seidenberg_theorem).
The algorithm is superexponential, but nevertheless exists.

## How practical is this for actual progress?

As described above, this is not very practical.
We have given justification that the number of worms we have to consider is finite, but still combinatorially explosive in $\epsilon$.
And real quantifier elimination algorithms are themselves super slow.

Still, I think it's nice to prove the fact that the constant is computable because the proof tells us where to look.
It raises a few **Question**s

- What is the (asymptotics of) the size of the smallest $\epsilon$-net of worms for any $\epsilon$?
  - What if we consider worm hulls instead?
  - In the previous post, we discussed a way of using casework to include larger sets in the set of hulls that need covering.
    How does the inclusion of these impact the size of the net?
  - There is some [prior work](https://www.researchgate.net/publication/220453014_Covering_n-Segment_Unit_Arcs_Is_Not_Sufficient) asserting that for any n, there is a cover of the n-segment worms which does not cover all worms.
    I guess the implication is that this means the minimal cover for the class of n segment worms might always be less than the moser cover.
    - can we determine a function \epsilon(n) so that all worms are within \epsilon thickening of some n-segment worm?
      - Consider an arbitrary worm $W$.
        Consider the n+1 contact points of the supporting hyperplanes of $hull(W)$ at angles $2\pi k/n+1$ for k ranging from 0 to n.
        Now, these contact points are each in $hull(W)$, so by Carathéodory's Theorem, each is in the hull of at most 3 points in $W$.
        This gives us at most $3n+3$ points on W such that all the contact points are in their hull.
        We can make a \le 3n+2 segment worm $W'$ by connecting these $3n+3$ points in the same order they are connected in $W$ by line segments (this never increases the length, because the shortest distance is a straight line).
        But the $epsilon$ thickening of $hull(W')$ contains $hull(W)$ for some epsilon which is small in $n$, because if we have two adjacent supporting points, we can't get much outside the angle due to limitations on the diameter.
      - And furthermore, we can probably discretize the supporting lines to distance of \eps/2
    - It's also the case that this paper makes use of the "broadworm" which we mentioned last time.
      The broadworm turns out to be constructed from segments and circular arcs, so maybe we could consider worms in this class instead?
- How fast do particular quantifier-elimination-type algorithms like CAD run on instances of the form "compute the smallest convex hull of isometries from this set"?
- Are there faster algorithms for this class of problems in particular?
  What is the best time complexity for this problem?

## More thoughts on finding good worms

It seems like an important subproblem, more than just enumerating worms, is finding *good* worms that violate particular hulls or sets of thickenings of hulls.

Perhaps we can do this by branch and bound.
Let's say that we want to compute an epsilon-cover of worms.

- Start with a selection of common worms (like the straight worm and a poylgonalization of the broadworm)
- Then do casework on the set of possible worm hulls:
  - We initially have a root node in our serch tree representing worms that contain the origin
  - Such worms cannot contain points outside the unit disc, so we make a polygonal approximation of the unit disc to represent the set of points that could possibly be in the worm.
  - We therefore represent nodes in our search tree by a hull of points that are definitely in the worm, and a polygon of points that are maybe in the worm.
  - To descend the search tree we select a point (perhaps randomly?)
    in the polygon of maybe-points but outside the hull of definitely-points.
    We case on whether or not to add this point to the definitely-set or not.
  - If we decide the point is in the worm:
    - we consider the other points in this branch that are in the worm and see if the worm has to be more than length-1, and if so, kill the branch.
    - If the worm is valid, then we check if the worm fails to be contained in the epsilon/2 thickening of worms in the net.
      If it fails to be contained in all of them, we add it to the net.
  - If we decide the point is not in the worm.
  - We then restrict the polygon using convexity rules.
  - If the polygon is now contained in the epsilon-thickening of some worm in the net, then all child nodes will be covered by the epsilon net, so we can kill the branch.
- We could also do better than random descent by looking at high-leverage points.

## How to determine if a hull is contained in a worm/Find the minimal worm containing a hull

I think last time I said this was just TSP, but it might be more complicated than that, because for some shapes, it consumes less length to actually use points off the hull.
For example, for a regular 100-gon of unit radius, the minimal TSP of the vertices will be about the same as the circumference of the circumscribed circle \approx 2 \pi.
But we can actually find a worm that contains the 100-gon in its hull with a smaller radius by taking the segments (1, -1) to (1,0) and (-1, -1) to (-1, 0) and joining them by the arc on the upper half, for a total length \approx 2 + \pi.
