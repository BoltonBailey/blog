# Approximating Moser's Worm Constant

[Previous post on Moser's worm problem here](./a-computational-approach-to-mosers-worm.md).
In that post I didn't give very strong justification for why the approach I described would successfully make progress on the problem.
Mostly my intuition for why this should be true was that it seemed like the approach was just a straightforward extension of the approach that previous lower bounds had used, but with the ability to take it farther by writing code to do it automatically.

Thinking about the problem computationally raises the **Question** of whether the number we are looking for is [computable](https://en.wikipedia.org/wiki/Computable_number) in the sense that there is an algorithm to approximate it to within any desired positive epsilon.
I haven't been able to find an explicit answer to this question in the literature, but I think I have a proof that the answer is yes, and this post will describe the algorithm and hopefully give a better sense of what it would actually take to improve a bound.

## The Blaschke selection theorem

The [Blaschke selection theorem](https://en.wikipedia.org/wiki/Blaschke_selection_theorem) is used to prove that the minimal area in the Moser worm problem is obtained.

> A succinct statement of the theorem is that the metric space of convex bodies is locally compact.

Inspired by this, perhaps we should think in terms of covering the space of *worms* compactly.
That is, we should show that it is possible to find (computably, as a list of polygonal worms with rational vertices) a finite set of worms so that any worm is within epsilon in of some worm in the set.

## An $\epsilon$-net of worms

My claim is that the set of polygonal worms with at most $k$ vertices belonging the grid of points $\delta \ZZ \times \delta \ZZ$, with $k, \delta$ sufficiently (large / small) satisfies this (in the sense that any worm is contained in the epsilon thickening of such a worm)^[Technically I think the notion of distance in the Blaschke theorem is Hausdorff metric, but this is the notion we want here] .

Treating length-1 worms as 1-Lipschitz functions from the unit interval, take a worm $f: [0,1] \to \RR^2$.
Consider $\tilde{f}$ defined by taking $\tilde{f}(n/k)$ for $n \in {0, ..., k} to be the nearest grid point to $f(n/k)$, and linearly interpolating between these points.
Then $f$ is contained within the $1/2k + \delta/\sqrt{2}$ thickening of $\tilde{f}$: For any point $x$ in the unit interval, $x$ is within $1/2k$ of some number of the form $n/k$, so $f(k)$ is within $1/2k$ of f(n/k)$, which is within $\delta/\sqrt{2}$ of $\tilde{f}(n/k)$.

Now, the nearest-grid-point operation might make the length of any segment as large as $1/k + \sqrt{2} \delta$.
So the Lipschitz constant of $\tilde{f}$ is $1 + \sqrt{2} \delta k$ rather than 1 as desired.
But this should not be a big deal - we can just shrink $\tilde{f}$ by a factor $1 + \sqrt{2} \delta k$ and make sure to choose $\delta$ much smaller than $k$ is large, (and leave some portion of our $\epsilon$ to account for the change in location of the points arising from this shrinkage).
This results in a grid with a new slightly smaller $\delta$, where the gird-vertex-worms cover everything.
There are only finitely many such worms up to translation because there are only finitely many grid points within 1 of the origin.

<!-- Now for any $x \in [0,1]$, the distance from $f(x)$ to the corresponding point $\tilde{f}(x)$ is at most $2\delta k + \delta + 1/k < \epsilon $. Therefore, we may choose $k > 2/\epsilon$ and $\delta$ sufficiently small that the point in the original worm is within $\epsilon$ of the point in the new worm.
\qed -->

## Why is this covering useful for computing the Moser constant?

Consider the minimal convex cover of all worms in a set $S_\epsilon$ with this property that any worm (with one endpoint on the origin, say) is contained in the epsilon thickening of some worm in $S\_\epsilon$
(Note we can compute the minimal cover by (i.e. minimum over all translation-rotations of the elements of S of the area of the hull of the union) this can be done by quantifier elimination and maybe by convex optimization?)
we have an upper and a lower bound on the Moser number:

- We have a lower bound in the area of the cover, because any moser set must cover the worms in S.
- We have an upper bound in the area of the epsilon thickening of the cover, because if we epsilon thicken the cover, that will cover the thickenings of every worm in S, and therefore cover every worm.

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

Thus, to compute the Moser soltuion to within $\epsilon$:

1. Find $epsilon'$ such that $\epsilon' \pi^2 + \pi \epsilon'^2 < \epsilon$.
2. Compute an $S_\epsilon'$ that satisfies this epsilon.
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
- How fast do particular quantifier-elimination-type algorithms like CAD run on instances of the form "compute the smallest convex hull of isometries from this set"?
- Are there faster algorithms for this class of problems in particular?
  What is the best time complexity for this problem?

## More thoughts on finding good worms

It seems like an important subproblem, more than just enumerating worms, is finding *good* worms that violate particular hulls or sets of thickenings of hulls.

Perhaps we can do this by branch and bound:

- Start with a subset of a worm hull (initially just one point)
- Given a subset of a worm hull, we know that if that worm hull needs length $L$ to cover just the points in that set, then there can be no other point in the worm a distance of 1-L from the hull.
- If we have a hull of points definitely in the worm and a polygon of points outside the worm, then we can take an arbitrary point in the polygon but outside the hull and case on whether it should be included in the worm.
  This either restricts the polygon or expands the worm.
- We can determine high-leverage points to case on by how much they restrict the difference in area.
- At any time, we can ask if the polygon is covered by a set of interest, and drop the case if it is.
- At any time, we can determine that the worm is not covered by any set of interest and we have found a good worm.

We could also maybe take the view that a convex polygon is defined, up to rescaling, by a probability distribution on angles, and try to run the algorithm for minimal worm length through this.

<!-- 
## Constant Thickening Approach

After thinking some more, maybe here is another approach better than the first:

Suppose I have a set K of area less than the true value of the moser constant $M_C$.
Then if I thicken K by $t$ to area $(|K| + M_c)/2$, the resulting $K^{+t}$ will not be a Moser set.
I can prove this by finding a worm not contained in it.
I now know that any moser set containing K must also contain some point not in $K^{+t}$.
So if I thicken $K$ by $t/2 to $K^{+t/2}$, and I move a hull point around the border of $K^{+t}$ and track which points on the border $K^{+t/2}$ are contained in it, I can find a finite number of points on the border of $K^{+t/2}$, one of which must be contained in any moser set containing $K$.

TODO complete analysis.

 -->
