#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "matplotlib",
# ]
# ///
"""
Simulate the polycausality model.

The key model (from the blog post):
  U(Z, C) = U_{Z,C} + U_Z + U_C + U

where U_Z is a sum of n_other_events standard normals (one per other event × choice),
and U_{Z,C} is a single standard normal (the focal cross-term).

The breakpoint probability simplifies to:
  p = (U_{XB} - U_{YB} + U_X - U_Y) / (U_{XB} - U_{YB} - U_{XA} + U_{YA})

The denominator only involves the 4 focal cross-terms, while the numerator also
includes U_X - U_Y which grows in variance with n_other_events — making p less
likely to land in [0, 1] as n_other_events increases.
"""

import numpy as np
import argparse
import matplotlib.pyplot as plt


def simulate(
    n_other_events: int,
    n_other_decisions: int,
    n_samples: int,
    seed: int | None,
    verbose: bool,
):
    rng = np.random.default_rng(seed)

    print(
        f"Parameters: n_other_events={n_other_events}, n_other_decisions={n_other_decisions}, n_samples={n_samples}"
    )
    print()

    if verbose:
        header = f"{'U(X,A)':>9} {'U(X,B)':>9} {'U(Y,A)':>9} {'U(Y,B)':>9} {'u_XA':>7} {'u_XB':>7} {'u_YA':>7} {'u_YB':>7} {'UX-UY':>9} {'numer':>9} {'denom':>9} {'p':>9} in[0,1]"
    else:
        header = f"{'U(X,A)':>9} {'U(X,B)':>9} {'U(Y,A)':>9} {'U(Y,B)':>9} {'p_break':>9} in[0,1]"
    print(header)
    print("-" * len(header))

    # Each entry: (p_break, denom, U_XA, U_XB, U_YA, U_YB, u_X, u_Y)
    in_range_samples = []

    for _ in range(n_samples):
        # Focal cross-terms: single U_{Z_i*, C_j*} for each (choice, outcome) pair
        u_XA = rng.standard_normal()
        u_XB = rng.standard_normal()
        u_YA = rng.standard_normal()
        u_YB = rng.standard_normal()

        # Choice-only components: U_X = sum_{j != j*} U_{X, C_j}  (n_other_events terms)
        u_X = rng.standard_normal() * n_other_events ** 0.5
        u_Y = rng.standard_normal() * n_other_events ** 0.5

        # Outcome-only components: U_A = sum_{i != i*} U_{Z_i, A}  (n_other_decisions terms)
        u_A = rng.standard_normal() * n_other_decisions ** 0.5
        u_B = rng.standard_normal() * n_other_decisions ** 0.5

        # Independent component: sum over all other (i, j) pairs
        u_indep = rng.standard_normal() * (n_other_events * n_other_decisions) ** 0.5

        # Full composite U(Z, C) values
        U_XA = u_XA + u_X + u_A + u_indep
        U_XB = u_XB + u_X + u_B + u_indep
        U_YA = u_YA + u_Y + u_A + u_indep
        U_YB = u_YB + u_Y + u_B + u_indep

        # Breakpoint formula: p = (U(X,B) - U(Y,B)) / (U(X,B) - U(Y,B) - U(X,A) + U(Y,A))
        # Simplifies to: numer = u_XB - u_YB + (u_X - u_Y),  denom = u_XB - u_YB - u_XA + u_YA
        numer = U_XB - U_YB  # == u_XB - u_YB + u_X - u_Y
        denom = (
            U_XB - U_YB - U_XA + U_YA
        )  # == u_XB - u_YB - u_XA + u_YA  (u_A, u_B, u_indep cancel)

        if abs(denom) < 1e-10:
            p = float("nan")
            in_range = False
        else:
            p = numer / denom
            in_range = 0.0 <= p <= 1.0

        if in_range:
            in_range_samples.append((p, denom, U_XA, U_XB, U_YA, U_YB))
            tag = "YES"
            if verbose:
                print(
                    f"{U_XA:>9.3f} {U_XB:>9.3f} {U_YA:>9.3f} {U_YB:>9.3f}"
                    f" {u_XA:>7.3f} {u_XB:>7.3f} {u_YA:>7.3f} {u_YB:>7.3f}"
                    f" {u_X - u_Y:>9.3f} {numer:>9.3f} {denom:>9.3f} {p:>9.3f} {tag}"
                )
            else:
                print(
                    f"{U_XA:>9.3f} {U_XB:>9.3f} {U_YA:>9.3f} {U_YB:>9.3f} {p:>9.3f} {tag}"
                )

    in_range_count = len(in_range_samples)
    print("-" * len(header))
    print(
        f"Fraction in [0,1]: {in_range_count}/{n_samples} = {in_range_count / n_samples:.1%}"
    )

    if in_range_count > 0:
        in_range_values = [s[0] for s in in_range_samples]
        plot_cdf(in_range_values, n_other_events)
        plot_expected_utility(in_range_samples, n_other_events)


def plot_expected_utility(
    samples, n_other_events, p_true_values=(0.0, 0.25, 0.5, 0.75, 1.0), n_prices=200
):
    """For each market prediction price p, compute total expected utility across
    all filtered samples, where each consumer rationally picks the option with
    higher expected utility given the quoted market price."""
    prices = np.linspace(0, 1, n_prices)
    # One utility accumulator per p_true scenario
    total_utility = {pt: np.zeros(n_prices) for pt in p_true_values}

    for p_break, denom, U_XA, U_XB, U_YA, U_YB in samples:
        # Expected utility of each choice as a function of the market price.
        # d/dp[eu_X - eu_Y] = (U_XA - U_YA) - (U_XB - U_YB) = -denom
        # So when denom < 0: eu_X - eu_Y increases with p → choose X when p > p_break
        #    when denom > 0: eu_X - eu_Y decreases with p → choose X when p < p_break
        eu_X_at_p = prices * U_XA + (1 - prices) * U_XB
        eu_Y_at_p = prices * U_YA + (1 - prices) * U_YB
        chooses_X = eu_X_at_p >= eu_Y_at_p
        # Assert the consumer's rational choice indeed has higher EU at each price
        assert np.all(eu_X_at_p[chooses_X] >= eu_Y_at_p[chooses_X] - 1e-9), (
            f"Consumer with p_break={p_break:.4f} chose X but eu_X < eu_Y at some price"
        )
        assert np.all(eu_Y_at_p[~chooses_X] >= eu_X_at_p[~chooses_X] - 1e-9), (
            f"Consumer with p_break={p_break:.4f} chose Y but eu_Y < eu_X at some price"
        )
        for pt in p_true_values:
            # Sum utility at this p_true (the true expected outcome)
            eu_X = pt * U_XA + (1 - pt) * U_XB
            eu_Y = pt * U_YA + (1 - pt) * U_YB
            total_utility[pt] += np.where(chooses_X, eu_X, eu_Y)

    n = len(samples)
    plt.figure(figsize=(8, 5))
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
    for pt, color in zip(p_true_values, colors):
        y = total_utility[pt] / n
        plt.plot(prices, y, color=color, label=f"p_true = {pt}")
        coeffs = np.polyfit(prices, y, 2)
        print(f"  p_true={pt}: a={coeffs[0]:.4f}, b={coeffs[1]:.4f}, c={coeffs[2]:.4f}")
        plt.plot(prices, np.polyval(coeffs, prices), color=color, linewidth=0.8, linestyle=":")
        plt.axvline(pt, color=color, linestyle="--", alpha=0.5)
    plt.title(
        f"Mean expected utility vs market price (n_other_events={n_other_events})"
    )
    plt.xlabel("Market prediction p")
    plt.ylabel("Mean expected utility per filtered consumer")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)

    filename = f"expected_utility_n{n_other_events}.png"
    plt.savefig(filename)
    print(f"Expected utility plot saved to {filename}")


def plot_cdf(values, n_other_events):
    data = np.sort(values)
    y = np.arange(1, len(data) + 1) / len(data)

    plt.figure(figsize=(8, 5))
    plt.step(data, y, where="post")
    plt.title(f"CDF of p_break (n_other_events={n_other_events})")
    plt.xlabel("p_break")
    plt.ylabel("Cumulative Probability")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.xlim(0, 1)
    plt.ylim(0, 1.05)

    filename = f"cdf_n{n_other_events}.png"
    plt.savefig(filename)
    print(f"CDF plot saved to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Simulate breakpoint probability distribution under polycausality"
    )
    parser.add_argument(
        "--n-other-events",
        type=int,
        default=10,
        help="Number of other events beyond the focal event j* (default: 10)",
    )
    parser.add_argument(
        "--n-other-decisions",
        type=int,
        default=10,
        help="Number of other decisions beyond the focal decision i* (default: 10)",
    )
    parser.add_argument(
        "--n-samples",
        type=int,
        default=2000,
        help="Number of consumer samples to generate (default: 2000)",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Also show focal cross-terms and U_X - U_Y decomposition",
    )
    args = parser.parse_args()

    simulate(
        args.n_other_events,
        args.n_other_decisions,
        args.n_samples,
        args.seed,
        args.verbose,
    )


if __name__ == "__main__":
    main()
