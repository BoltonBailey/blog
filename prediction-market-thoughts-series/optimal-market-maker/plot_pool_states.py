#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "matplotlib",
# ]
# ///
"""
Plot the YES/NO pool states for the uniform-liquidity AMM.

x = 1/2 + 1/2 * (t - 1/2) * (t + 1/2)   (NO pool)
y = (1-t) + 1/2 * (t - 1/2) * (t + 1/2)  (YES pool)

x is minimised at t=0 (x_min = 3/8), y is minimised at t=1 (y_min = 3/8).
We show t from slightly below 0 to slightly above 1 so the full curve is visible
including the turn-arounds at each minimum.
"""

import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 4000)

x = t**2        # NO pool  (= 2 * (1/2 + currency - 3/8))
y = (1 - t)**2  # YES pool

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(x, y, color="tab:blue", linewidth=2)

# Label the vertex (t=0.5)
ax.plot(1/4, 1/4, "ko", markersize=6, zorder=5)
ax.annotate("$(1/4,\\,1/4)$", xy=(1/4, 1/4), xytext=(1/4 + 0.04, 1/4 + 0.04), fontsize=10)

ax.set_xlabel("$x$ = NO pool", fontsize=12)
ax.set_ylabel("$y$ = YES pool", fontsize=12)
ax.set_title("YES/NO Pool States as Price Varies", fontsize=13)
ax.set_aspect("equal")
ax.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
filename = "pool_states.png"
plt.savefig(filename, dpi=150)
print(f"Saved {filename}")
