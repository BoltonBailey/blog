# Computability of Moser's Worm Constant

[Previous post on Moser's worm problem here](./a-computational-approach-to-mosers-worm.md).
In that post I didn't give very strong justification for why the approach I described would successfully make progress on the problem.
Mostly my intuition for why this should be true was that it seemed like the approach was just a straightforward extension of the approach that previous lower bounds had used, but with the ability to take it farther by writing code to do it automatically.

Thinking about the problem computationally raises the **Question** of whether the number we are looking for is [computable](https://en.wikipedia.org/wiki/Computable_number) in the sense that there is an algorithm to approximate it to within any desired positive accuracy.
I haven't been able to find an explicit answer to this question in the literature, but I think I have a proof that the answer is yes (maybe it's just considered obvious enough that writers don't discuss it).
This post will describe the algorithm and hopefully give a better sense of what it would actually take to improve a bound.

## The Blaschke selection theorem

The [Blaschke selection theorem](https://en.wikipedia.org/wiki/Blaschke_selection_theorem) is used to prove that the minimal area in the Moser worm problem is obtained.

> A succinct statement of the theorem is that the metric space of convex bodies is locally compact.

Inspired by this, perhaps we should think in terms of covering the space of *worms* compactly.
That is, we should show that it is possible to find (computably, as a list of polygonal worms with rational vertices) a finite set of worms so that any worm is within ε of some worm in the set.

## An ε-net of worms

My claim is that the set of polygonal worms with at most k vertices belonging the grid of points δℤ × δℤ, with k, δ sufficiently (large / small) satisfies this (in the sense that any worm is contained in the ε-thickening of such a worm)^[Technically I think the notion of distance in the Blaschke theorem is Hausdorff metric, but this is the notion we want here].
There are only finitely many such worms up to translation because there are only finitely many grid points within 1 of the origin.
Let's see why this works.

Treating length-1 worms as 1-Lipschitz functions from the unit interval, take a worm f: [0,1] → ℝ².
Consider f̃ defined by taking f̃(n/k) for n ∈ {0, ..., k} to be the nearest δ-grid point to f(n/k), and f̃(x) defined on other values by linearly interpolating between these points.
Then f is contained within the 1/2k + δ/√2 thickening of f̃: For any point x in the unit interval, x is within 1/2k of some number of the form n/k, so by Lipschitzness f(x) is within 1/2k of f(n/k), which is within δ/√2 of f̃(n/k).

Now, the nearest-grid-point operation unfortunately might make the length of any segment as large as 1/k + √2 δ.
So the Lipschitz constant of f̃ is 1 + √2 δk rather than 1 as desired.
But this should not be a big deal - we can just shrink f̃ towards the origin by a factor 1 + √2 δk.
As long as we choose δ much smaller than k is large (and leave some portion of our ε to account for the change in location of the points arising from this shrinkage) the shrinkage factor will be small and the resulting worm will still be very near the original worm.
This results in a grid with a new slightly smaller δ, where the grid-vertex-worms cover everything.

<!-- Now for any x ∈ [0,1], the distance from f(x) to the corresponding point f̃(x) is at most 2δk + δ + 1/k < ε. Therefore, we may choose k > 2/ε and δ sufficiently small that the point in the original worm is within ε of the point in the new worm.
∎ -->

## Why is this covering useful for computing the Moser constant?

Instead of the minimal convex cover for the set of all worms, we could try to compute the minimal convex cover of just the worms in a set S_ε with this property that any worm (with one endpoint on the origin, say) is contained in the ε-thickening of some worm in S_ε.
Suppose we could successfully compute this minimal convex cover and its area.
We then have an upper and a lower bound on the Moser's convex worm cover constant:

- The area itself would be a lower bound, because any Moser set must cover the worms in S.
- The area of the ε-thickening of the cover would be an upper-bound, because if we ε-thicken the cover, the result will cover the ε-thickenings of every worm in S_ε, and therefore cover every worm.

And we also know these bounds are close: By the [Minkowski-Steiner formula for convex plane sets](https://en.wikipedia.org/wiki/Minkowski%E2%80%93Steiner_formula#Convex_sets), the area of the thickening of any convex set is exactly `ε × perimeter_of_cover + π ε²` more than the area of the set itself.
If we do our trick from last time of assuming the sidelength 1/3 square is in the set S_ε, then the minimal cover can't contain a point at distance π/2 from the center of this square without becoming larger than the previously established upper bound on Moser set size.
Thus, the perimeter is at most π², and we can explicitly bound the difference in sizes by

ε π² + π ε²

The current gap between the best known lower and upper bounds is

π/12 − 0.232239 = 0.02956

So to get ε π² + π ε² this small, we would need ε ≈ 0.0029.
Perhaps this is good evidence that this length scale is close to the precision we need in our numerics.

## Putting it all together

Thus, to compute the Moser solution to within an accuracy:

1. Find ε such that ε π² + π ε² < accuracy.
2. Compute an S_ε.
3. Compute the area A of a minimal cover of S_ε of and take A, A + accuracy as the bounds on the convex Moser covering constant.

The last step is the only one we haven't explained: The point is that whether A is the minimal area of the hull of congruent copies of S_ε is a proposition that can be expressed as a formula in the first order theory of the reals.
Computing A exactly as an algebraic number is therefore possible using real quantifier elimination / [the Tarski-Seidenberg theorem](https://en.wikipedia.org/wiki/Tarski%E2%80%93Seidenberg_theorem).

## How practical is this for actual progress?

As described above, this is not very practical.
The best algorithm for real-quantifier elimination has [doubly-exponential complexity](https://en.wikipedia.org/wiki/Cylindrical_algebraic_decomposition).
On top of this,
we have given justification that the number of worms we have to consider is finite, but still combinatorially explosive in ε.

Still, I think it's nice to prove the fact that the constant is computable because the proof tells us where to look.
It raises a few **Question**s

- What is the size of the smallest 0.0029-net of worms?
- What are the asymptotics in ε of the size of the smallest ε-net of worms?
- What if we consider worm hulls instead?
  Does that make a difference?
- The previous post was about using casework to include larger sets in the set of hulls that need covering.
  Does the inclusion of these impact the size of the net?
- There is some [prior work](https://www.researchgate.net/publication/220453014_Covering_n-Segment_Unit_Arcs_Is_Not_Sufficient) asserting that for any n, there is a cover of the n-segment worms which does not cover all worms.
  I guess the implication is that this means the minimal cover for the class of n-segment worms might always be less than the Moser cover.
  But if you read it carefully, you notice that "there is a cover of n-segment polygonal worms which does not cover all worms" is not the same as "the minimal cover of n-segment worms is not the minimal cover of all worms".
  So is the weak version of this conjecture open?
- It's also the case that this paper makes use of the "broadworm" which we mentioned last time.
  The broadworm turns out to be constructed from segments and circular arcs, so maybe we could consider worms in this class instead?
  - Is it the case that we just need to consider the broadworm + n-segment polygonal worms?
  - It it the case that we just need to consider n-segment worms where the segments can either be linear or circular arcs?
- Are there faster algorithms than CAD to compute the smallest convex hull of isometries from a set?

## More thoughts on finding nets of worms

Even if it turns out to be hard to prove there are small ε-net of worms, perhaps we can still find such nets computationally.
We could do this by branch and bound:

- Start with a selection of common worms (like the straight worm and a polygonalization of the broadworm)
- Then do casework on the set of possible worm hulls:
  - We initially have a root node in our search tree representing worms that contain the origin
  - Such worms cannot contain points outside the unit disc, so we make a polygonal approximation of the unit disc to represent the set of points that could possibly be in the worm.
  - We therefore represent nodes in our search tree by a hull of points that are definitely in the worm, and a polygon of points that are maybe in the worm.
  - To descend the search tree we select a point (perhaps randomly?)
    in the polygon of maybe-points but outside the hull of definitely-points.
    We case on whether or not to add this point to the definitely-set or exclude it from the maybe-set.
    - If we decide the point is included in the worm-hull:
      - we consider the other points in this branch that are in the worm and see if the worm has to be more than length-1, and if so, kill the branch.
      - If the worm is valid, then we check if the worm fails to be contained in the ε/2 thickening of worms in the net.
        If it fails to be contained in all of them, we reason that it is probably a good worm and add it to the net.
    - If we decide the point is not in the worm-hull.
      - We then restrict the polygon using convexity rules.
      - If the polygon is now contained in the ε-thickening of some worm in the net, then all child nodes will be covered by the ε-net, so we can kill the branch.
- We could also do better than random descent by looking at high-leverage points.

## How to determine if a hull is contained in a worm/Find the minimal worm containing a hull

I think last time I said this was just TSP, but it might be more complicated than that, because for some shapes, it consumes less length to actually use points off the hull.
For example, for a regular pentagon of unit side length, the minimal TSP of the vertices will be 4.
But we can actually find a sorter worm that contains the pentagon in its hull by dropping perpendiculars to the line containing one side from the two vertices nearest to the line that aren't on it.

TODO Image

Still, this problem seems simple enough that I figure it's probably in P (modulo weird square-root-sum concerns).
I think you can probably say something like "the minimal worm that contains a point set only includes at most two vertices not in the set, namely the endpoints" and then argue that these two points fall on the intersection of lines coindicent with sides of the hull and do polynomial casework over these.

<!-- 
Here a (potentially useful?) lemma:

**Lemma** For any set of $n$ points, if it is in the hull of some length-1 worm, then it is in the hull of a polygonal worm of length \le 1 and at most 3n vertices.

*Proof*. Let $S$ be a set of $n$ points and let $W$ be a (not necessarily polygonal) worm such that $S \subset hull(W)$. By Carathéodory's Theorem, each $x \in S$ is in the hull of at most 3 points in W. So choose $S' \subset W$ a set of size $3n$ points so that $S \subset hull(S')$. But since each point in $S'$ is in $W$, we can form a worm $W'$ by connecting the points in $S'$ by line segments in the same order they are connected in $W$. The length of the resulting worm is at most 1, since segments connecting adjacent points will be no longer than whatever path there is between them in $W$.
 -->

<!-- 
### Can we determine a function ε(n) so that all worms are within ε-thickening of some n-segment worm?

Consider an arbitrary worm W.
There are n+1 contact points of the supporting hyperplanes of hull(W) at angles 2πk/(n+1) for k ranging from 0 to n.
Now, these contact points are each in hull(W), so by Carathéodory's Theorem, each is in the hull of at most 3 points in W.
This gives us at most 3n+3 points on W such that all the contact points are in their hull.
We can make a ≤ 3n+2 segment worm W′ by connecting these 3n+3 points in the same order they are connected in W by line segments (this never increases the length, because the shortest distance is a straight line).
But the ε thickening of hull(W′) contains hull(W) for some ε which is small in n, because if we have two adjacent supporting points, we can't get much outside the angle due to limitations on the diameter.
And furthermore, we can probably discretize the supporting lines to distance of ε/2
 -->
