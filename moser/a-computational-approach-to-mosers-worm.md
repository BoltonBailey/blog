# [A Computational Approach to Moser's Worm Lower bounds](https://thequantummilkman.substack.com/p/a-computational-approach-to-mosers)

A Moser set is a subset $M$ of the plane such that for any "worm" (path of length 1), an isometry[^1] of $M$ covers the worm.
[A longstanding problem](https://en.wikipedia.org/wiki/Moser%27s_worm_problem) asks: "What is the minimal area of a convex Moser set?".
The best lower bound that Wikipedia cites is 0.232239 from [this 2011/2013 paper of Khandhawit, Pagonakis, and Sriswasdi](https://arxiv.org/abs/1101.5638).

Recently [this website](https://teorth.github.io/optimizationproblems/) of Tao's for tracking optimization constants [added the problem](https://teorth.github.io/optimizationproblems/constants/13a.html).
I have been interested in ways we could increase the lower bound the size of a convex Moser set, so I will take the opportunity in this post will discuss my thoughts.

## Summary of the 2013 KPS paper

The paper mentioned above works on a simple principle - Any convex Moser set must contain a copy of any Moser worm, and moreover, the convex hull of any worm.
In particular it must contain specific hulls, like:

- A unit length line segment
- An equilateral triangle of side length 1/2
- Any rectangle with three sides having total length 1
- "The broadworm" (a particular worm I don't have a picture of that was apparently described in a previous paper).

TODO insert image

The paper then proceeds to do some reasoning about possible paramters for and relative locations of these figures to arrive at the bound.

## Pushing this approach with computation

The KPS paper does all of its reasoning essentially by hand, and as such is only able to consider a few worms.
I propose to describe a way we could automate the procedure of improving the lower bound by computationally searching over worms, and tracking the areas of sets that must contain them.

### The basic strategy

Here is the broad-strokes strategy I imagine:

We initialize $S := \{ Hull((-1/6,-1/6), (-1/6,+1/6), (+1/6,-1/6), (+1/6,+1/6)) \}$ as the set containing the square of side length 1/3 centered at the origin.
Since there is a worm that surrounds three sides of this square, any convex Moser set must contain this square or an isometry of it.

We then seek to manipulate S while preserving the following invariants:

- $S$ is a finite set of (convex polygonal) subsets of the plane.
- Every element of $S$ contains (an isometry of) the square.
- For any convex Moser set $M$ of area $\le 0.232240$, there is an element $s$ of $S$ such that $s$ is isometric to a subset of $M$.

Our goal will be to carry out such manipulations until $S$ is empty, thus proving that all Moser sets have area at least $0.232240$.

### Manipulations we can perform on $S$

We describe a number of manipulations of $S$ that preserve the invariant.

- Big set removal: If there is $s \in S$ with area $\ge 0.232240$, we may remove this $s$ from $S$
  - This preserves the invariant since any Moser set that contains $s$ must already have area $\ge 0.232240$.
- Hull taking: If there is a set $s \in S$ which is not convex, we may replace it with its convex hull.
  - This preserves the invariant since any Moser set containing $s$ must contain its hull.
  - In fact, if we wanted to, we could add the stipultation that $S$ contain only convex sets, and take the hull before adding.
- Distance removal.
  If there is a set $s \in S$ containing a point with distance $x \ge 6 \cdot 0.232240 = 1.39344$ from $(0,0)$, $s$ can be removed.
  - This follows from the previous two principles: The square contains a circle of radius $1/6$ centered at $(0,0)$.
    If there is any point $x \in s$ at distance $r$ from the center, then the hull of $\{x\} \cup \{ (-1/6,-1/6), (-1/6,+1/6), (+1/6,-1/6), (+1/6,+1/6) \}$ contains a triangle with a diameter of the circle (i.e. 1/3) as a base, and height $r$.
    The area of this triangle is $(1/2)bh = (1/2)(1/3)r \ge 0.232240$, and it can therefore be removed as too large.
- Worm adding: Given a worm, any M must contain an isometry to the hull of the worm.
  While the set of isometries of hulls of a worm is uncountable, for any $\epsilon > 0$ we can create a discrete subset of the set of isometries so that for any isometry, all points of the hull are within $\epsilon$ of the corresponding point in a hull in the discretized set (for example, by discretizing the space of rotations, vertical translations, and horizontal translations to within $\epsilon/3$).
  If we shrink the sides of the hulls in the discrete subset inward by $\epsilon$, any hull of an isometry of the worm will contain one of the shrunken hulls in the discrete set.
  Thus, for a given worm, $\epsilon$, and set $s \in S$, we can remove $s$ and replace it with all $s \cup X$ for $X$ in the set shrunken hulls.
  We may, from the previous point, consider only $X$ fully contained within distance $1.39344$ of the origin, so only finitely many sets are added in this replacement.

The last transformation is key because it allows us to replace a set by sets of strictly larger area.
Roughly, our goal will be to find good worms with which to carry out this operation, making the size of the minimal remaining set bigger and bigger, until the big set removal allows us to remove them all.

There are also some optional transformations that do not directly advance the goal of increasing the size of the minimal set in $S$, but could be indirectly helpful in managing things.

- Intersection taking (optional): Remove $s, s'$ from $S$ and replace with $s \cap s'$.
  We may apply isometries before the intersection.
  If two sets overlap almost exactly, and taking their intersection doesn't result in an area below the smallest area, then this allows us to manage the size of our set.
- Subset removal (optional): Remove $s$ from $S$ if $s$ is a subset of (an isometry of) some other element of $S$.
  In other words, intersection taking but in the case where one set is a strict subset of another.
  Clearly this is good to do if possible, since any operations we do to the smaller set could just be replicated on the larger.
- Subset taking (optional): Remove $s$ from $S$ and replace with a subset of $s$.
  This might be useful for simplifying the representation of these sets, for example, by replacing a convex set represented as the hull of points in $\mathbb{Q}^2$ by the hull of a smaller set of points, or decreasing the size of the memory needed to store the rationals.

To summarize with some pseudocode:

1. While True:
2. Identify the smallest-area $s \in S$
3. Search through (worm, epsilon) pairs until a pair is identified such that the Worm-adding operation produces only strictly larger sets.
4. Replace $s$ using the operation.
5. Carry out hull taking and big set removal on the resulting sets.

### Finding worms with which to perform the replacement

We require a way to find worms.

One way would just be to enumerate this generically as a countable structure (i.e. enumerate 3-, 4-, 5- vertex worms by generating rational points, and then dovetail over these lengths).
But this seems unlikely to give good worms, not the least because there are many worms that are too long, or repeatedly self-intersect so much that they produce too a small set to successfully increase the size of $s$.

We can solve both problems at once by realizing that what we are interested in is not the worm, but its hull.
Given a hull, we can find the smallest worm that fits in it.
Then we can rescale so that the worm is just under length 1.

This leaves us with the question of how to enumerate hulls.
Note that any convex set can be approximated by an equiangular polygon.
So we can just enumerate side length counts, and given a side length count, assume perimeter 1 and enumerate ways to partition perimeters among the angles

The nice thing about this is it gives common polygons like the ones considered by KPS quickly.

Optional augmentations:

- Do some sort of optimization to find good worm-hulls before trying them.
  - ["The Worm Problem of Leo Moser" by Norwood et     al.](https://link.springer.com/content/pdf/10.1007/BF02187832.pdf) suggests some worms in the last paragraph.
  - Use the algorithm below to determine if a worm-hull fits inside some $s$.
    If it does, it won't work at all.
    If it doesn't, choose $\epsilon$ so that $\epsilon$-shinkings of the hull still don't fit inside.
- Perhaps we can tailor the selection of the worm to the specific set we are trying to push by guessing points on the boundary of the set where the worm would stick out if we tried to cram it in, and taking those as our hull points.
  - In principle, the question "does there exist a unit length k-joint polygonal worm that does not fit in this convex polygon?"
    is a question of the first-order theory of the reals, and is therefore [decidable](https://en.wikipedia.org/wiki/Decidability_of_first-order_theories_of_the_real_numbers).
  - Indeed, we could theoretically determine the k-joint worm that "sticks out the most".
  - But that doesn't mean there is a fast solution.

### Fiddly computational geometry

I think there's a few computational geomtery subroutines we would need

#### Finding the minimal worm in a hull

Technically, this is an instance of TSP.
Bu I think this can be found in polynomial time for sets which are vertices of convex polygons!
Note that in Eulcidean TSP, the path can't cross itself.
Thus, it seems we can't visit any node which isn't a neighbor of one we've already visited, since otherwise we would be forced to loop back and cross our own path.
This means there are only two options at any juncture, and I think we can perform dynamic programming.

#### A potentially useful algorithm for determining if one convex polygon fits inside another

It seems convenient to short-circuit the discretizing procedure if the worm is already contained in the set.
Can we determine if a particular convex polygon is isometrically contained in another?

One thing that seems convenient here is: I think that if there is a containment, there should be one where there are multiple incidences of vertices of the contained polygon on edges of the outer polygon, by manipluating degrees of freedom.
So perhaps we can case on these and reduce the problem to algebra.

## Further thoughts

The tricky part of all of this is the inherent trickiness in ensuring you have a sound implementation.
Luckily, [I have actually formalized a statement of the 2013 bound](https://github.com/google-deepmind/formal-conjectures/blob/9e5c532b541d85b4418fa5360f52f7011a680a23/FormalConjectures/Wikipedia/MoserWorm.lean#L113), so maybe that could be a helpful grounding for a Lean implementation of this.

Also worth exploring the links on the Moser Worm Problem wiki page.
I think everyhting in this post applies equally well to the Lesbegue universal covering problem https://arxiv.org/abs/1502.01251

[^1]: Technically it is supposed to be "direct isometry"/"rigid motion" - reflections are not included.
    I was confused about this initially, it is sad there is not a shorter term for this, so I will just say "isometry".
