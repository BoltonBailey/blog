#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "tqdm",
#   "numpy",
#   "scipy",
# ]
# ///

import os

# Force single-threaded BLAS/OpenMP *before* numpy/scipy import. The branch-and-bound runs
# tens of thousands of tiny scipy.linprog (HiGHS) solves; each would otherwise spin up an
# OpenMP thread pool, and on macOS those semaphores leak ("resource_tracker: leaked
# semaphore objects") and pile up until the process stalls. Single-threaded is also faster
# here, since the LPs are far too small to benefit from parallelism.
for _var in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ.setdefault(_var, "1")

import random  # noqa: E402  (imports kept below the thread-limit env setup above)
from collections import Counter  # noqa: E402
from importlib import import_module  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402


def get_feedback(true_solution, guess) -> str:
    """
    `get_feedback(true_solution, guess)` is the function which takes in a true solution and a guess and returns the feedback string that would be given in Wordle.
    The feedback string is a string of length 5 where each character is either "G", "Y", or "B" corresponding to Green, Yellow, and Black feedback respectively.

    Note, from wikipedia: "If a guessed word contains multiple instances of the same letter—such as the "o"s in "robot"—those letters will be marked green or yellow only if the answer also contains them multiple times. If not, extra occurrences will be marked gray."
    """
    feedback = ["B"] * 5
    true_solution_list = list(true_solution)

    # First pass for Green
    for i in range(5):
        if guess[i] == true_solution[i]:
            feedback[i] = "G"
            true_solution_list[i] = None  # Mark this letter as used

    # Second pass for Yellow
    for i in range(5):
        if feedback[i] == "B" and guess[i] in true_solution_list:
            feedback[i] = "Y"
            true_solution_list[true_solution_list.index(guess[i])] = (
                None  # Mark this letter as used
            )

    return "".join(feedback)


def is_consistent(true_solution, prior_guess, potential_solution) -> bool:
    """
    `is_consistent(true_solution, prior_guess, potential_solution)`
     is the ternary relation on words which describes the statement,
     "if `true_solution` is the true solution and `prior_guess` is guessed so that the information about letters from `prior_guess` is known, is `potential_solution` consistent with those revelations"
    """
    feedback = get_feedback(true_solution, prior_guess)
    return get_feedback(potential_solution, prior_guess) == feedback


def pairs_distinguished_by(
    word: str, possible_solutions: list[str]
) -> list[tuple[str, str]]:
    """
    Given a word, returns all ordered (s1, s2) pairs of distinct solutions that `word`
    distinguishes — i.e., get_feedback(s1, word) != get_feedback(s2, word).
    """
    by_feedback: dict[str, list[str]] = {}
    for s in possible_solutions:
        by_feedback.setdefault(get_feedback(s, word), []).append(s)

    pairs = []
    feedbacks = list(by_feedback.items())
    for i, (_, group1) in enumerate(feedbacks):
        for _, group2 in feedbacks[i + 1 :]:
            for s1 in group1:
                for s2 in group2:
                    pairs.append((s1, s2))
    return pairs


def count_pairs_distinguished_by(word: str, possible_solutions: list[str]) -> int:
    counts: Counter[str] = Counter(get_feedback(s, word) for s in possible_solutions)
    n = len(possible_solutions)
    same_fb = sum(v * (v - 1) for v in counts.values())
    return n * (n - 1) - same_fb


def words_by_pairs_distinguished(
    allowed_guesses: list[str], possible_solutions: list[str]
) -> list[tuple[int, str]]:
    tqdm = import_module("tqdm").tqdm
    return sorted(
        (count_pairs_distinguished_by(w, possible_solutions), w)
        for w in tqdm(allowed_guesses, desc="Scoring words", unit="word")
    )


def render_undistinguished_pair(
    selected_words: list[str],
    solution: str,
    other: str,
) -> None:
    GREEN = "\033[42;30m"
    YELLOW = "\033[43;30m"
    GRAY = "\033[100;37m"
    RESET = "\033[0m"
    COLOR = {"G": GREEN, "Y": YELLOW, "B": GRAY}

    print(f"    Undistinguished: '{solution}' vs '{other}'")
    for word in selected_words:
        feedback = get_feedback(solution, word)  # identical for `other` as answer
        colored = " ".join(
            f"{COLOR[fb]}{letter.upper()}{RESET}" for letter, fb in zip(word, feedback)
        )
        print(f"      {word}: {colored}")


def sample_undistinguished_pairs(
    sol_class: list[int],
    possible_solutions: list[str],
    k: int = 3,
) -> list[tuple[str, str]]:
    sol_by_class: dict[int, list[str]] = {}
    for i, c in enumerate(sol_class):
        sol_by_class.setdefault(c, []).append(possible_solutions[i])

    active = [sols for sols in sol_by_class.values() if len(sols) >= 2]
    random.shuffle(active)

    seen: set[tuple[str, str]] = set()
    samples: list[tuple[str, str]] = []
    for sols in active:
        shuffled = random.sample(sols, len(sols))
        for i, s1 in enumerate(shuffled):
            for s2 in shuffled[i + 1 :]:
                if (s1, s2) not in seen:
                    seen.add((s1, s2))
                    samples.append((s1, s2))
                    if len(samples) >= k:
                        return samples
    return samples


def greedy_distinguishing_cover(
    allowed_guesses: list[str], possible_solutions: list[str]
) -> list[tuple[str, int, int]]:
    """
    Greedy set-cover: repeatedly select the word that distinguishes the most remaining
    undistinguished (solution, guess) pairs. Returns list of (word, pairs_newly_distinguished,
    pairs_remaining) for each step.

    Two words s and g are "indistinguishable" so far if every selected word produces the same
    feedback whether s or g is the true answer. We track this via an integer class ID per word;
    words share a class iff their feedback fingerprints (over all selected words) match.
    """
    tqdm = import_module("tqdm").tqdm

    n_sol = len(possible_solutions)
    sol_class = [0] * n_sol
    current_total = n_sol * (n_sol - 1)  # ordered solution-solution pairs
    undistinguished = current_total

    result: list[tuple[str, int, int]] = []
    selected_words: list[str] = []

    while undistinguished > 0:
        step = len(result) + 1
        scores: list[tuple[int, str]] = []

        for w in tqdm(allowed_guesses, desc=f"Step {step}", unit="word"):
            new_sol = Counter(
                (sol_class[i], get_feedback(possible_solutions[i], w))
                for i in range(n_sol)
            )
            new_total = sum(v * (v - 1) for v in new_sol.values())
            scores.append((current_total - new_total, w))

        scores.sort()
        best_score, best_word = scores[-1]

        if best_score == 0:
            print(
                f"Step {step}: no word distinguishes remaining {undistinguished:,} pairs — stopping"
            )
            for s1, s2 in sample_undistinguished_pairs(sol_class, possible_solutions):
                render_undistinguished_pair(selected_words, s1, s2)
            break

        n = len(scores)
        print(f"\nStep {step}: '{best_word}' distinguishes {best_score:,} new pairs")
        print("Percentiles of pairs newly distinguished by each candidate word:")
        for p in range(0, 101, 10):
            idx = min(p * n // 100, n - 1)
            cnt, word = scores[idx]
            print(f"  P{p:3d}: {word}  ({cnt:,})")

        # Refine the class partition using best_word
        selected_words.append(best_word)
        class_map: dict[tuple, int] = {}
        next_id = 0

        new_sol_class: list[int] = []
        for i in range(n_sol):
            key = (sol_class[i], get_feedback(possible_solutions[i], best_word))
            if key not in class_map:
                class_map[key] = next_id
                next_id += 1
            new_sol_class.append(class_map[key])

        sol_class = new_sol_class
        current_total = sum(v * (v - 1) for v in Counter(sol_class).values())
        undistinguished = current_total

        print(f"  {undistinguished:,} pairs remaining:")
        for s1, s2 in sample_undistinguished_pairs(sol_class, possible_solutions):
            render_undistinguished_pair(selected_words, s1, s2)

        result.append((best_word, best_score, undistinguished))

    print("\nFull greedy cover sequence:")
    for word, distinguished, remaining in result:
        print(f"  {word}: +{distinguished:,} distinguished, {remaining:,} remaining")

    return result


# ---------------------------------------------------------------------------
# Fast vectorized feedback + weighted greedy search
# ---------------------------------------------------------------------------

_POWERS = (3 ** np.arange(5)).astype(np.uint16)


def encode_words(words: list[str]) -> np.ndarray:
    """Encode a list of 5-letter words as an (n, 5) int8 array of 0..25 letter codes."""
    arr = np.frombuffer("".join(words).encode(), dtype=np.uint8).reshape(len(words), 5)
    return (arr - ord("a")).astype(np.int8)


def _feedback_codes_for_guess(guess_code: np.ndarray, sol: np.ndarray) -> np.ndarray:
    """
    Vectorized Wordle feedback for one guess against all solutions.

    `guess_code` is a (5,) array of letter codes; `sol` is an (n, 5) array.
    Returns an (n,) uint8 array of feedback codes in 0..242, where the code packs
    five base-3 digits (B=0, Y=1, G=2), digit i weighted by 3**i. Matches
    `get_feedback` exactly (greens first, then yellows left-to-right by remaining counts).
    """
    n = sol.shape[0]
    green = sol == guess_code  # (n, 5)

    avail = np.zeros((n, 26), dtype=np.int16)
    for c in range(26):
        avail[:, c] = (sol == c).sum(1)
    for i in range(5):
        g = int(guess_code[i])
        avail[green[:, i], g] -= 1  # greens consume a letter occurrence

    fb = np.zeros((n, 5), dtype=np.uint8)
    fb[green] = 2  # G
    for i in range(5):
        g = int(guess_code[i])
        can_yellow = (~green[:, i]) & (avail[:, g] > 0)
        fb[can_yellow, i] = 1  # Y
        avail[can_yellow, g] -= 1

    return (fb.astype(np.uint16) * _POWERS).sum(1).astype(np.uint8)


def build_feedback_matrix(
    allowed_guesses: list[str],
    possible_solutions: list[str],
    cache_path: Path | None = None,
) -> np.ndarray:
    """
    Build (and optionally disk-cache) the (n_guesses, n_solutions) uint8 matrix of
    feedback codes. Cell [g, s] is the feedback when guessing `allowed_guesses[g]`
    against true answer `possible_solutions[s]`.
    """
    G, n = len(allowed_guesses), len(possible_solutions)
    if cache_path is not None and cache_path.exists():
        fb = np.load(cache_path)
        if fb.shape == (G, n):
            return fb

    tqdm = import_module("tqdm").tqdm
    sol = encode_words(possible_solutions)
    guesses = encode_words(allowed_guesses)
    fb = np.empty((G, n), dtype=np.uint8)
    for gi in tqdm(range(G), desc="Building feedback matrix", unit="guess"):
        fb[gi] = _feedback_codes_for_guess(guesses[gi], sol)

    if cache_path is not None:
        np.save(cache_path, fb)
    return fb


def _same_group_ordered_count(sol_class: np.ndarray, fb_row: np.ndarray, n: int) -> int:
    """Number of ordered distinct solution pairs sharing both their current class and
    their feedback under one guess: sum over groups of cnt*(cnt-1)."""
    key = sol_class.astype(np.int64) * 243 + fb_row
    counts = np.unique(key, return_counts=True)[1]
    return int((counts * counts).sum()) - n


def _refine(sol_class: np.ndarray, fb_row: np.ndarray) -> np.ndarray:
    """Refine the class partition by splitting each class on the guess's feedback."""
    key = sol_class.astype(np.int64) * 243 + fb_row
    return np.unique(key, return_inverse=True)[1].astype(np.int64)


def _residual_scores(
    sol_class: np.ndarray, fb: np.ndarray, n: int, chunk: int = 2048
) -> np.ndarray:
    """
    For every guess at once, the number of ordered solution pairs left undistinguished if
    that guess is added to the current partition: pairs sharing both their current class and
    the guess's feedback. Lower is better. This is `_same_group_ordered_count` vectorized
    across all guesses, computed in row chunks to bound memory.

    For each guess row we sort the combined key (class*243 + feedback), so equal keys form
    contiguous runs; the residual is sum(run_len**2) - n (subtracting the n self-pairs).
    """
    G = fb.shape[0]
    out = np.empty(G, dtype=np.int64)
    cls = sol_class.astype(np.int64) * 243
    cols = np.arange(n)
    for s in range(0, G, chunk):
        e = min(s + chunk, G)
        m = e - s
        key = cls[None, :] + fb[s:e]  # (m, n) int64
        key.sort(axis=1)

        change = np.empty((m, n), dtype=bool)
        change[:, 0] = True
        np.not_equal(key[:, 1:], key[:, :-1], out=change[:, 1:])

        # Start column of the run each position belongs to (running max of change positions).
        start = np.where(change, cols[None, :], 0)
        np.maximum.accumulate(start, axis=1, out=start)

        # A position ends a run if the next position starts a new one (or it is the last).
        is_end = np.empty((m, n), dtype=bool)
        is_end[:, -1] = True
        is_end[:, :-1] = change[:, 1:]

        run_len = (cols[None, :] - start + 1).astype(np.int64)
        rl = np.where(is_end, run_len, 0)
        out[s:e] = (rl * rl).sum(axis=1) - n
    return out


def beam_search_cover(
    fb: np.ndarray,
    budget: int = 5,
    beam_width: int = 20,
    branch: int = 20,
    progress: bool = False,
) -> tuple[tuple[int, ...], int, int]:
    """
    Beam search for a `budget`-word guess set distinguishing as many answer pairs as possible
    — a constructive upper bound complementing the LP lower bound.

    A *state* is a set of chosen guesses plus the partition of answers into classes still
    mutually indistinguishable by those guesses (carried as `sol_class`, since the partition
    depends only on the set, not the order). From the empty set, at each of `budget` levels we
    expand every beam state by its `branch` best next words (those leaving the fewest
    undistinguished ordered pairs), then keep the globally best `beam_width` resulting states,
    deduplicated by word set so permutations don't crowd the beam. Plain greedy is the special
    case beam_width = branch = 1; widening either lets the search escape greedy's local optima.

    Takes the prebuilt feedback matrix `fb` (shape (G, n)). Returns
    (best_word_indices, best_residual_ordered_undistinguished, states_explored).
    """
    G, n = fb.shape
    total_ordered = n * (n - 1)
    branch = min(branch, G)

    # A beam entry is (residual_ordered_undistinguished, chosen_idx_tuple, sol_class).
    beam: list[tuple[int, tuple[int, ...], np.ndarray]] = [
        (total_ordered, (), np.zeros(n, dtype=np.int64))
    ]
    best: tuple[int, tuple[int, ...]] = (total_ordered, ())
    states_explored = 0

    for level in range(1, budget + 1):
        states = tqdm_iter(beam, progress, desc=f"width {beam_width} level {level}")
        # Best state per distinct word set reached at this level.
        candidates: dict[frozenset[int], tuple[int, tuple[int, ...], np.ndarray]] = {}
        for _residual, chosen, sol_class in states:
            states_explored += 1
            scores = _residual_scores(sol_class, fb, n)
            if chosen:
                scores[list(chosen)] = total_ordered + 1  # never re-pick a chosen word
            for g in np.argpartition(scores, branch - 1)[:branch].tolist():
                new_chosen = tuple(sorted(chosen + (g,)))
                key = frozenset(new_chosen)
                if key in candidates:
                    continue  # residual is set-determined; same set -> same residual
                candidates[key] = (
                    int(scores[g]),
                    new_chosen,
                    _refine(sol_class, fb[g]),
                )

        beam = sorted(candidates.values(), key=lambda t: t[0])[:beam_width]
        lvl_residual, lvl_chosen, _ = beam[0]
        if lvl_residual < best[0]:
            best = (lvl_residual, lvl_chosen)

    return best[1], best[0], states_explored


def tqdm_iter(iterable, enabled: bool, **kwargs):
    """Wrap `iterable` in tqdm only when `enabled`, so quiet runs stay quiet."""
    if not enabled:
        return iterable
    return import_module("tqdm").tqdm(iterable, **kwargs)


def weighted_greedy_cover_search(
    allowed_guesses: list[str],
    possible_solutions: list[str],
    budget: int = 5,
    iterations: int = 50,
    decay: float = 1.0 / 1.0001,
    cache_path: Path | None = None,
    seed: int | None = None,
) -> tuple[list[str], int]:
    """
    Find a `budget`-word set distinguishing as many solution pairs as possible, via a
    multiplicative-weights / Lagrangian heuristic.

    Each unordered solution pair carries a weight, starting at 1. We run weighted greedy
    set-cover to pick `budget` words, each step choosing the word that distinguishes the
    most *weighted* still-undistinguished pairs. After a full pass we update every pair's
    weight: a pair still undistinguished (a "hit") has its weight raised by 1 (additive),
    while a pair that got distinguished (a "miss") has its whole weight multiplied by
    `decay` (< 1). So persistently-hard pairs accrue weight and pull subsequent passes
    toward covering them, while the bulk of always-distinguished pairs decay together. We
    track the best word set by the true (unweighted) number of pairs distinguished.

    `decay` is the multiplicative factor applied to a distinguished pair's weight each
    pass; hits always add 1.

    Implementation note: every never-hit pair has the same weight (the running `baseline`,
    = decay ** passes), so only ever-hit pairs need explicit storage.

    Returns (best_words, best_pairs_distinguished) where the count is ordered pairs.
    """
    tqdm = import_module("tqdm").tqdm
    rng = random.Random(seed)

    n = len(possible_solutions)
    total_ordered = n * (n - 1)
    fb = build_feedback_matrix(allowed_guesses, possible_solutions, cache_path)
    G = len(allowed_guesses)

    # Full per-pair weights. Every never-hit pair shares `baseline` (= decay ** passes,
    # starting at 1), so only ever-hit pairs need an explicit entry in `weight`.
    weight: dict[tuple[int, int], float] = {}
    baseline = 1.0

    best_words: list[str] = []
    best_distinguished = -1

    for it in range(1, iterations + 1):
        # Snapshot the tracked (ever-hit) pairs and their weights for this pass.
        if weight:
            items = list(weight.items())
            hp_i = np.array([p[0] for (p, _) in items], dtype=np.int64)
            hp_j = np.array([p[1] for (p, _) in items], dtype=np.int64)
            hp_w = np.array([w for (_, w) in items], dtype=np.float64)
        else:
            hp_i = hp_j = np.empty(0, dtype=np.int64)
            hp_w = np.empty(0, dtype=np.float64)

        sol_class = np.zeros(n, dtype=np.int64)
        chosen: list[int] = []

        for step in range(budget):
            # Tracked pairs still undistinguished (same current class) are the only ones
            # whose weight a guess can affect this step.
            if hp_i.size:
                active = sol_class[hp_i] == sol_class[hp_j]
                aI, aJ, aW = hp_i[active], hp_j[active], hp_w[active]
            else:
                aI = aJ = np.empty(0, dtype=np.int64)
                aW = np.empty(0, dtype=np.float64)

            # count[g] = ordered same-group pairs left if we add guess g. Every such pair
            # carries weight `baseline`, except tracked pairs which carry their own weight.
            count = np.empty(G, dtype=np.float64)
            guess_iter = tqdm(
                range(G), desc=f"Iter {it} step {step + 1}", unit="guess", leave=False
            )
            for g in guess_iter:
                count[g] = _same_group_ordered_count(sol_class, fb[g], n)

            # weighted same-group "cost" S(g): smaller is better (distinguishes more).
            score = baseline * count
            if aW.size:
                same_fb = fb[:, aI] == fb[:, aJ]  # (G, A)
                # correct tracked pairs from `baseline` to their own weight (×2: ordered).
                score = score + 2.0 * (same_fb * (aW - baseline)).sum(1)

            # argmin with random tie-breaking for exploration across passes. Relative
            # tolerance, since absolute scores shrink as `baseline` decays.
            best_val = score.min()
            tol = 1e-9 * (abs(best_val) + 1e-300)
            ties = np.flatnonzero(score <= best_val + tol)
            g = int(ties[rng.randrange(len(ties))])

            chosen.append(g)
            sol_class = _refine(sol_class, fb[g])

        # True objective for this pass (unweighted).
        counts = np.bincount(sol_class)
        undistinguished = int((counts * counts).sum()) - n
        distinguished = total_ordered - undistinguished
        words = [allowed_guesses[g] for g in chosen]

        new_best = distinguished > best_distinguished
        if new_best:
            best_distinguished = distinguished
            best_words = words

        best_pairs_left = (total_ordered - best_distinguished) // 2
        line = (
            f"Iter {it:3d}: {words}  distinguishes all but {undistinguished // 2} pairs "
            f"| best {best_pairs_left}"
        )
        if new_best:
            line = f"\033[33m{line}\033[0m"  # yellow for a new best
        print(line)

        # Weight update. Collect this pass's leftover ("hit") pairs.
        leftover: set[tuple[int, int]] = set()
        big = np.flatnonzero(counts >= 2)
        for c in big:
            members = np.flatnonzero(sol_class == c)
            for a in range(len(members)):
                for b in range(a + 1, len(members)):
                    leftover.add((int(members[a]), int(members[b])))

        # Update weights. Tracked pairs: +1 if a hit, ×decay if a miss.
        for pair in list(weight.keys()):
            if pair in leftover:
                weight[pair] += 1.0
            else:
                weight[pair] *= decay

        # Newly-hard pairs (still at `baseline`, never tracked before): +1, now tracked.
        for pair in leftover:
            if pair not in weight:
                weight[pair] = baseline + 1.0

        # The bulk of never-hit pairs are all distinguished again: decay the baseline.
        baseline *= decay

    print(f"\nBest {budget}-word set: {best_words}")
    print(
        f"Distinguishes {best_distinguished:,} of {total_ordered:,} ordered pairs "
        f"({(total_ordered - best_distinguished) // 2} unordered pairs left undistinguished)"
    )
    return best_words, best_distinguished


# ---------------------------------------------------------------------------
# LP relaxation of the distinguishing set-cover
# ---------------------------------------------------------------------------


def _pair_base(n: int) -> np.ndarray:
    """Row offsets for the upper-triangular pair index: lin(i, j) = base[i] + (j-i-1)
    for i < j, enumerating unordered pairs in row-major order."""
    i = np.arange(n, dtype=np.int64)
    return i * (2 * n - i - 1) // 2


def _class_pair_lins(members: np.ndarray, base: np.ndarray) -> np.ndarray:
    """Linear indices of every unordered pair drawn from one class's member indices."""
    a, b = np.triu_indices(len(members), k=1)
    mi, mj = members[a], members[b]
    return base[mi] + (mj - mi - 1)


def _lin_to_ij(lins: np.ndarray, base: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Invert _pair_base: map linear pair indices back to (i, j) with i < j."""
    i = np.searchsorted(base, lins, side="right") - 1
    j = lins - base[i] + i + 1
    return i, j


def _greedy_cover_word_indices(fb: np.ndarray, n: int) -> list[int]:
    """Fast plain greedy: pick words minimizing remaining same-class pairs until every
    solution pair is distinguished. Returns the chosen guess indices (a feasible cover)."""
    tqdm = import_module("tqdm").tqdm
    G = fb.shape[0]
    sol_class = np.zeros(n, dtype=np.int64)
    chosen: list[int] = []
    while True:
        counts = np.bincount(sol_class)
        if int((counts * counts).sum()) - n == 0:
            break
        best_g, best_val = 0, None
        for g in tqdm(
            range(G),
            desc=f"Seed greedy step {len(chosen) + 1}",
            unit="guess",
            leave=False,
        ):
            v = _same_group_ordered_count(sol_class, fb[g], n)
            if best_val is None or v < best_val:
                best_val, best_g = v, g
        chosen.append(best_g)
        sol_class = _refine(sol_class, fb[best_g])
    return chosen


def lp_relaxation_cover(
    allowed_guesses: list[str],
    possible_solutions: list[str],
    cache_path: Path | None = None,
    max_rounds: int = 100,
    add_per_round: int = 4000,
    tol: float = 1e-6,
    forced_words: list[str] | None = None,
) -> tuple[np.ndarray, float]:
    """
    Solve the LP relaxation of the distinguishing set-cover:

        minimize   sum_g x_g                          (total fractional word weight)
        subject to sum_{g distinguishes p} x_g >= 1   for every solution pair p
                   0 <= x_g <= 1

    i.e. each pair must be "covered" (to a total of 1) by the words that distinguish it.
    The optimum is a lower bound on the integer number of words needed to distinguish
    every pair of answers.

    There are ~n^2/2 pair constraints, far too many to materialize, but the binding ones
    are the *hard* pairs (distinguished by few words). We use lazy constraint generation:
    seed with the hardest pairs, solve, then repeatedly add any pair whose coverage is
    still < 1 under the current solution until none remain.

    Returns (x, objective) where x is the length-`len(allowed_guesses)` weight vector.
    """
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix

    fb = build_feedback_matrix(allowed_guesses, possible_solutions, cache_path)
    G, n = fb.shape
    base = _pair_base(n)

    # Seed: a greedy cover, then take the pairs its words distinguish fewest times.
    seed_words = _greedy_cover_word_indices(fb, n)
    print(
        f"Seed greedy cover uses {len(seed_words)} words: "
        f"{[allowed_guesses[g] for g in seed_words]}"
    )
    undist_count = np.zeros(n * (n - 1) // 2, dtype=np.int32)
    for g in seed_words:
        cls = fb[g]
        for c in np.unique(cls):
            members = np.flatnonzero(cls == c)
            if members.size >= 2:
                np.add.at(undist_count, _class_pair_lins(members, base), 1)
    # A pair distinguished by k of the seed words has undist_count = len(seed_words) - k.
    seed_lins = np.flatnonzero(undist_count >= len(seed_words) - 2)
    print(f"Seeding LP with {seed_lins.size:,} hard pair constraints")

    # Working constraint set, stored as accumulated sparse COO plus a membership set.
    rows: list[np.ndarray] = []
    cols: list[np.ndarray] = []
    in_working: set[int] = set()
    ncon = 0

    def add_constraints(lins: np.ndarray) -> int:
        nonlocal ncon
        ii, jj = _lin_to_ij(lins, base)
        added = 0
        for lin, i, j in zip(lins.tolist(), ii.tolist(), jj.tolist()):
            if lin in in_working:
                continue
            dist = np.flatnonzero(fb[:, i] != fb[:, j])
            rows.append(np.full(dist.size, ncon, dtype=np.int64))
            cols.append(dist)
            in_working.add(lin)
            ncon += 1
            added += 1
        return added

    add_constraints(seed_lins)

    c = np.ones(G, dtype=np.float64)
    bounds = [(0.0, 1.0)] * G
    for w in forced_words or []:
        bounds[allowed_guesses.index(w)] = (1.0, 1.0)  # pin word to weight 1
    x = np.zeros(G)

    tqdm = import_module("tqdm").tqdm
    for rnd in range(1, max_rounds + 1):
        A = csr_matrix(
            (
                np.full(sum(r.size for r in rows), -1.0),
                (np.concatenate(rows), np.concatenate(cols)),
            ),
            shape=(ncon, G),
        )
        res = linprog(c, A_ub=A, b_ub=-np.ones(ncon), bounds=bounds, method="highs")
        if not res.success:
            raise RuntimeError(f"LP failed in round {rnd}: {res.message}")
        x = res.x
        S = float(x.sum())

        # Separation: only pairs left together by some weighted word can be uncovered
        # (since S >= 1 once any constraint exists). Accumulate their non-distinguishing
        # weight U(p); coverage(p) = S - U(p).
        support = np.flatnonzero(x > tol)
        U = np.zeros(n * (n - 1) // 2, dtype=np.float64)
        for g in tqdm(
            support, desc=f"Round {rnd} separation", unit="word", leave=False
        ):
            cls = fb[g]
            for cc in np.unique(cls):
                members = np.flatnonzero(cls == cc)
                if members.size >= 2:
                    np.add.at(U, _class_pair_lins(members, base), x[g])
        violated = np.flatnonzero(U > S - 1.0 + tol)
        # Keep only genuinely new violations, hardest (largest U) first.
        violated = violated[np.argsort(-U[violated])]
        violated = np.array(
            [v for v in violated.tolist() if v not in in_working], dtype=np.int64
        )

        print(
            f"Round {rnd}: objective {S:.4f}  ({ncon:,} constraints, "
            f"|support|={support.size}, {violated.size:,} violated)"
        )

        if violated.size == 0:
            break
        add_constraints(violated[:add_per_round])

    support = np.flatnonzero(x > tol)
    order = sorted(support.tolist(), key=lambda g: allowed_guesses[g])
    print(f"\nLP optimum: {x.sum():.4f} words to distinguish all pairs")
    print(f"Support ({len(order)} words with weight > {tol}):")
    for g in order:
        print(f"  {allowed_guesses[g]}: {x[g]:.4f}")
    return x, float(x.sum())


def verify_no_cover_in_k(
    allowed_guesses: list[str],
    possible_solutions: list[str],
    k: int = 5,
    cache_path: Path | None = None,
    max_rounds: int = 200,
    add_per_round: int = 4000,
    tol: float = 1e-6,
    word_limit: int | None = None,
) -> list[tuple[str, float]]:
    """
    Try to prove that no `k`-word integer set distinguishes every pair of answers.

    Any k-word cover must contain some first word w; pinning x_w = 1 then admits that
    cover as a feasible integer point of objective k, so the pinned LP optimum is <= k.
    Therefore, if for EVERY word w the pinned LP optimum exceeds k, no k-word cover exists.
    (Sound but not complete: a fractional optimum <= k does not imply an integer cover.)

    We solve the LP once per word, sharing a single growing pool of hard-pair constraints
    (cached as a sparse matrix, rebuilt only when it grows) and exiting early as soon as
    the relaxed objective exceeds k (it only rises as constraints are added).

    Returns the list of (word, optimum) NOT ruled out (optimum <= k). Empty list => proof
    that k words are insufficient.
    """
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix

    tqdm = import_module("tqdm").tqdm
    fb = build_feedback_matrix(allowed_guesses, possible_solutions, cache_path)
    G, n = fb.shape
    base = _pair_base(n)
    npairs = n * (n - 1) // 2

    rows: list[np.ndarray] = []
    cols: list[np.ndarray] = []
    in_working: set[int] = set()
    ncon = 0

    def add_constraints(lins: np.ndarray) -> None:
        nonlocal ncon
        ii, jj = _lin_to_ij(np.asarray(lins, dtype=np.int64), base)
        for lin, i, j in zip(np.asarray(lins).tolist(), ii.tolist(), jj.tolist()):
            if lin in in_working:
                continue
            dist = np.flatnonzero(fb[:, i] != fb[:, j])
            rows.append(np.full(dist.size, ncon, dtype=np.int64))
            cols.append(dist)
            in_working.add(lin)
            ncon += 1

    # Seed the pool with the hardest pairs from a greedy cover.
    seed_words = _greedy_cover_word_indices(fb, n)
    undist_count = np.zeros(npairs, dtype=np.int32)
    for g in seed_words:
        cls = fb[g]
        for cc in np.unique(cls):
            members = np.flatnonzero(cls == cc)
            if members.size >= 2:
                np.add.at(undist_count, _class_pair_lins(members, base), 1)
    add_constraints(np.flatnonzero(undist_count >= len(seed_words) - 2))
    print(f"Seeded shared pool with {ncon:,} hard-pair constraints")

    # Cached constraint matrix; rebuilt only when the pool grows.
    A_cache = None
    A_ncon = -1

    def get_A():
        nonlocal A_cache, A_ncon
        if A_ncon != ncon:
            A_cache = csr_matrix(
                (
                    np.full(sum(r.size for r in rows), -1.0),
                    (np.concatenate(rows), np.concatenate(cols)),
                ),
                shape=(ncon, G),
            )
            A_ncon = ncon
        return A_cache

    def separate(x: np.ndarray, S: float) -> np.ndarray:
        U = np.zeros(npairs, dtype=np.float64)
        for g in np.flatnonzero(x > tol):
            cls = fb[g]
            for cc in np.unique(cls):
                members = np.flatnonzero(cls == cc)
                if members.size >= 2:
                    np.add.at(U, _class_pair_lins(members, base), x[g])
        violated = np.flatnonzero(U > S - 1.0 + tol)
        violated = violated[np.argsort(-U[violated])]
        return np.array(
            [v for v in violated.tolist() if v not in in_working], dtype=np.int64
        )

    c = np.ones(G, dtype=np.float64)
    bounds = [(0.0, 1.0)] * G

    nwords = G if word_limit is None else min(word_limit, G)
    not_ruled_out: list[tuple[str, float]] = []
    worst_lb = (np.inf, None)  # smallest optimum/bound seen, with its word
    prev_pin = None

    for w in tqdm(range(nwords), desc=f"Pinning words (k={k})", unit="word"):
        if prev_pin is not None:
            bounds[prev_pin] = (0.0, 1.0)
        bounds[w] = (1.0, 1.0)
        prev_pin = w

        final_obj = float("inf")
        ruled_out = False
        for _ in range(max_rounds):
            res = linprog(
                c, A_ub=get_A(), b_ub=-np.ones(ncon), bounds=bounds, method="highs"
            )
            if not res.success:
                raise RuntimeError(
                    f"LP failed pinning {allowed_guesses[w]}: {res.message}"
                )
            final_obj = float(res.fun)
            if final_obj > k + tol:  # relaxed objective is a lower bound -> optimum > k
                ruled_out = True
                break
            new = separate(res.x, float(res.x.sum()))
            if new.size == 0:  # converged at true optimum <= k
                break
            add_constraints(new[:add_per_round])

        if final_obj < worst_lb[0]:
            worst_lb = (final_obj, allowed_guesses[w])
        tag = "ruled out  " if ruled_out else "NOT RULED OUT"
        tqdm.write(f"  {allowed_guesses[w]}: bound {final_obj:.4f}  [{tag}]")
        if not ruled_out:
            not_ruled_out.append((allowed_guesses[w], final_obj))

    print(f"\nShared pool ended with {ncon:,} constraints.")
    print(f"Lowest pinned optimum/bound: {worst_lb[1]} = {worst_lb[0]:.4f}")
    if not_ruled_out:
        print(
            f"{len(not_ruled_out)} word(s) NOT ruled out for a {k}-word cover "
            f"(LP cannot prove impossibility):"
        )
        for word, opt in sorted(not_ruled_out, key=lambda t: t[1]):
            print(f"  {word}: {opt:.4f}")
    elif nwords < G:
        print(
            f"No {k}-word cover among the first {nwords:,} pinned words — but "
            f"{G - nwords:,} words were NOT checked (word_limit set), so this is NOT "
            f"a proof. Re-run with word_limit=None."
        )
    else:
        print(
            f"PROVED: no {k}-word set can distinguish all pairs — all {G:,} words "
            f"pinned, every pinned LP optimum > {k}."
        )
    return not_ruled_out


def verify_no_cover_in_k_by_exclusion(
    allowed_guesses: list[str],
    possible_solutions: list[str],
    k: int = 5,
    cache_path: Path | None = None,
    max_rounds: int = 1000,
    max_excluded: int | None = None,
    add_per_round: int = 4000,
    tol: float = 1e-6,
    slack_budget: float = 0.0,
) -> tuple[bool, list[int]]:
    """
    Prove no `k`-word integer set distinguishes every pair, by greedy exclusion.

    Repeatedly: solve the LP over the still-allowed words. If its optimum exceeds `k`,
    no cover within those words costs <= k, so no k-word cover exists -> PROVED. Otherwise
    take the highest-weight word, rule it out by pinning it to 1 (a separate LP whose
    optimum > k means no k-cover contains it), then pin it to 0 ("exclude") for all later
    LPs. Only useful words ever need excluding, so this typically stops far sooner than
    pinning all ~10k words.

    `slack_budget` allows a total of that much coverage slack to be spread across pairs
    (one slack variable s_p >= 0 per constraint, sum_p s_p <= slack_budget, contributing
    to each pair's coverage at zero objective cost). slack_budget=1 thus models "a k-word
    set is allowed to leave up to 1 pair undistinguished": proving the optimum still
    exceeds k rules out any such near-miss solution too. slack_budget=0 is the exact cover.

    Returns (proved, excluded_word_indices) where `proved` is True iff impossibility
    was established for this `slack_budget`.
    """
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix, identity, hstack, vstack

    tqdm = import_module("tqdm").tqdm
    fb = build_feedback_matrix(allowed_guesses, possible_solutions, cache_path)
    G, n = fb.shape
    base = _pair_base(n)
    npairs = n * (n - 1) // 2

    rows: list[np.ndarray] = []
    cols: list[np.ndarray] = []
    in_working: set[int] = set()
    ncon = 0

    def add_constraints(lins: np.ndarray) -> None:
        nonlocal ncon
        ii, jj = _lin_to_ij(np.asarray(lins, dtype=np.int64), base)
        for lin, i, j in zip(np.asarray(lins).tolist(), ii.tolist(), jj.tolist()):
            if lin in in_working:
                continue
            dist = np.flatnonzero(fb[:, i] != fb[:, j])
            rows.append(np.full(dist.size, ncon, dtype=np.int64))
            cols.append(dist)
            in_working.add(lin)
            ncon += 1

    seed_words = _greedy_cover_word_indices(fb, n)
    undist_count = np.zeros(npairs, dtype=np.int32)
    for g in seed_words:
        cls = fb[g]
        for cc in np.unique(cls):
            members = np.flatnonzero(cls == cc)
            if members.size >= 2:
                np.add.at(undist_count, _class_pair_lins(members, base), 1)
    add_constraints(np.flatnonzero(undist_count >= len(seed_words) - 2))
    print(f"Seeded shared pool with {ncon:,} hard-pair constraints")

    A_cache = None
    A_ncon = -1

    def get_A():
        nonlocal A_cache, A_ncon
        if A_ncon != ncon:
            A_word = csr_matrix(
                (
                    np.full(sum(r.size for r in rows), -1.0),
                    (np.concatenate(rows), np.concatenate(cols)),
                ),
                shape=(ncon, G),
            )
            if slack_budget > 0.0:
                # Append one slack var per constraint (-s_p in its row) and a budget
                # row sum_p s_p <= slack_budget.
                top = hstack([A_word, -identity(ncon, format="csr")], format="csr")
                budget = hstack(
                    [csr_matrix((1, G)), csr_matrix(np.ones((1, ncon)))], format="csr"
                )
                A_cache = vstack([top, budget], format="csr")
            else:
                A_cache = A_word
            A_ncon = ncon
        return A_cache

    def separate(x: np.ndarray, S: float) -> np.ndarray:
        U = np.zeros(npairs, dtype=np.float64)
        for g in np.flatnonzero(x > tol):
            cls = fb[g]
            for cc in np.unique(cls):
                members = np.flatnonzero(cls == cc)
                if members.size >= 2:
                    np.add.at(U, _class_pair_lins(members, base), x[g])
        violated = np.flatnonzero(U > S - 1.0 + tol)
        violated = violated[np.argsort(-U[violated])]
        return np.array(
            [v for v in violated.tolist() if v not in in_working], dtype=np.int64
        )

    c = np.ones(G, dtype=np.float64)

    def solve(bounds) -> tuple[float, np.ndarray | None, bool]:
        """Constraint-generate until converged or the objective provably exceeds k.
        Returns (objective, x, exceeded). Infeasible counts as exceeded (no cover).
        `bounds` are the length-G word bounds; slack vars (if any) are appended here."""
        obj, x = float("inf"), None
        for _ in range(max_rounds):
            if slack_budget > 0.0:
                c_full = np.concatenate([c, np.zeros(ncon)])
                b_ub = np.concatenate([-np.ones(ncon), [slack_budget]])
                full_bounds = bounds + [(0.0, None)] * ncon
            else:
                c_full, b_ub, full_bounds = c, -np.ones(ncon), bounds
            res = linprog(
                c_full, A_ub=get_A(), b_ub=b_ub, bounds=full_bounds, method="highs"
            )
            if not res.success:  # infeasible: no cover at all within these words
                return float("inf"), None, True
            x = res.x[:G]  # word weights; res.fun = sum x_g (slack has zero cost)
            obj = float(res.fun)
            if obj > k + tol:  # lower bound on true optimum already exceeds k
                return obj, x, True
            new = separate(x, float(x.sum()))
            if new.size == 0:  # converged at true optimum <= k
                return obj, x, False
            add_constraints(new[:add_per_round])
        return obj, x, False

    bounds = [(0.0, 1.0)] * G
    excluded: list[int] = []

    while True:
        obj, x, exceeded = solve(bounds)
        if exceeded:
            print(
                f"\nPROVED: LP over the {G - len(excluded):,} remaining words = "
                f"{obj:.4f} > {k}. No {k}-word set can distinguish all pairs "
                f"(slack {slack_budget:g}; {len(excluded)} words excluded along the way)."
            )
            return True, excluded
        if max_excluded is not None and len(excluded) >= max_excluded:
            print(
                f"\nStopped after excluding {len(excluded)} words; unpinned LP still "
                f"{obj:.4f} <= {k}."
            )
            return False, excluded
        assert x is not None  # not exceeded => solve converged with a solution

        # Highest-weight allowed word first; rule out the first one we can.
        order = [
            g for g in np.argsort(-x).tolist() if x[g] > tol and bounds[g] != (0.0, 0.0)
        ]
        picked = None
        for cand in order:
            bounds[cand] = (1.0, 1.0)
            oc, _, exc = solve(bounds)
            bounds[cand] = (0.0, 1.0)
            tqdm.write(
                f"  test {allowed_guesses[cand]} (w={x[cand]:.3f}): "
                f"pinned LP {oc:.4f} -> {'RULE OUT' if exc else 'cannot rule out'}"
            )
            if exc:
                picked = cand
                break

        if picked is None:
            print(
                f"\nCannot prove: unpinned LP = {obj:.4f} <= {k} but no weighted word "
                f"could be ruled out. Candidate first-words:"
            )
            for g in order[:20]:
                print(f"  {allowed_guesses[g]}: weight {x[g]:.4f}")
            return False, excluded

        bounds[picked] = (0.0, 0.0)
        excluded.append(picked)
        print(
            f"Excluded #{len(excluded)}: {allowed_guesses[picked]} "
            f"(unpinned LP was {obj:.4f}, {ncon:,} constraints)"
        )


def _undistinguished_pair_count(fb: np.ndarray, n: int, word_idxs: list[int]) -> int:
    """Unordered pairs of solutions left undistinguished by the given set of guesses."""
    sol_class = np.zeros(n, dtype=np.int64)
    for g in word_idxs:
        sol_class = _refine(sol_class, fb[g])
    counts = np.bincount(sol_class)
    return int((counts * (counts - 1) // 2).sum())


def verify_no_cover_recursive(
    allowed_guesses: list[str],
    possible_solutions: list[str],
    k: int = 5,
    slack_budget: float = 0.0,
    cache_path: Path | None = None,
    max_rounds: int = 1000,
    add_per_round: int = 4000,
    tol: float = 1e-6,
    verbose_depth: int = 2,
) -> tuple[bool, list[int] | None]:
    """
    Exact branch-and-bound: prove no `k`-word set leaves <= `slack_budget` pairs
    undistinguished, OR return a concrete counterexample set.

    At each node a subset of words is fixed IN (pinned to 1) and OUT (pinned to 0). The
    LP relaxation over the free words bounds the node: if its optimum > k, no completion
    is feasible -> prune. Otherwise we branch on the highest-weight free word w:
      - w IN: recurse (one fewer word of budget, residual pairs shrink) — the recursive
        "rule out w" the flat method couldn't do with a single LP;
      - w OUT: exclude w and continue the loop, exactly as before.
    The loop's early stop (LP over free words > k) closes all remaining "out" branches at
    once. Bottoming out with k words pinned and a feasible LP yields an integer
    counterexample: those k words leave <= slack_budget pairs undistinguished.

    Returns (proved, counterexample_word_indices_or_None).
    """
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix, identity, hstack, vstack

    tqdm = import_module("tqdm").tqdm
    fb = build_feedback_matrix(allowed_guesses, possible_solutions, cache_path)
    G, n = fb.shape
    base = _pair_base(n)
    npairs = n * (n - 1) // 2

    rows: list[np.ndarray] = []
    cols: list[np.ndarray] = []
    in_working: set[int] = set()
    ncon = 0

    def add_constraints(lins: np.ndarray) -> None:
        nonlocal ncon
        ii, jj = _lin_to_ij(np.asarray(lins, dtype=np.int64), base)
        for lin, i, j in zip(np.asarray(lins).tolist(), ii.tolist(), jj.tolist()):
            if lin in in_working:
                continue
            dist = np.flatnonzero(fb[:, i] != fb[:, j])
            rows.append(np.full(dist.size, ncon, dtype=np.int64))
            cols.append(dist)
            in_working.add(lin)
            ncon += 1

    seed_words = _greedy_cover_word_indices(fb, n)
    undist_count = np.zeros(npairs, dtype=np.int32)
    for g in seed_words:
        cls = fb[g]
        for cc in np.unique(cls):
            members = np.flatnonzero(cls == cc)
            if members.size >= 2:
                np.add.at(undist_count, _class_pair_lins(members, base), 1)
    add_constraints(np.flatnonzero(undist_count >= len(seed_words) - 2))
    print(f"Seeded shared pool with {ncon:,} hard-pair constraints")

    A_cache = None
    A_ncon = -1

    def get_A():
        nonlocal A_cache, A_ncon
        if A_ncon != ncon:
            A_word = csr_matrix(
                (
                    np.full(sum(r.size for r in rows), -1.0),
                    (np.concatenate(rows), np.concatenate(cols)),
                ),
                shape=(ncon, G),
            )
            if slack_budget > 0.0:
                top = hstack([A_word, -identity(ncon, format="csr")], format="csr")
                budget = hstack(
                    [csr_matrix((1, G)), csr_matrix(np.ones((1, ncon)))], format="csr"
                )
                A_cache = vstack([top, budget], format="csr")
            else:
                A_cache = A_word
            A_ncon = ncon
        return A_cache

    def separate(x: np.ndarray, S: float) -> np.ndarray:
        U = np.zeros(npairs, dtype=np.float64)
        for g in np.flatnonzero(x > tol):
            cls = fb[g]
            for cc in np.unique(cls):
                members = np.flatnonzero(cls == cc)
                if members.size >= 2:
                    np.add.at(U, _class_pair_lins(members, base), x[g])
        violated = np.flatnonzero(U > S - 1.0 + tol)
        violated = violated[np.argsort(-U[violated])]
        return np.array(
            [v for v in violated.tolist() if v not in in_working], dtype=np.int64
        )

    c = np.ones(G, dtype=np.float64)

    def solve(bounds) -> tuple[float, np.ndarray | None, bool]:
        obj, x = float("inf"), None
        for _ in range(max_rounds):
            if slack_budget > 0.0:
                c_full = np.concatenate([c, np.zeros(ncon)])
                b_ub = np.concatenate([-np.ones(ncon), [slack_budget]])
                full_bounds = bounds + [(0.0, None)] * ncon
            else:
                c_full, b_ub, full_bounds = c, -np.ones(ncon), bounds
            res = linprog(
                c_full, A_ub=get_A(), b_ub=b_ub, bounds=full_bounds, method="highs"
            )
            if not res.success:
                return float("inf"), None, True
            x = res.x[:G]
            obj = float(res.fun)
            if obj > k + tol:
                return obj, x, True
            new = separate(x, float(x.sum()))
            if new.size == 0:
                return obj, x, False
            add_constraints(new[:add_per_round])
        return obj, x, False

    bounds = [(0.0, 1.0)] * G
    free = (0.0, 1.0)
    nodes = 0
    counterexample: list[int] | None = None

    def prove(in_count: int, depth: int) -> bool:
        """True iff no feasible k-set extends the current IN set (using free words)."""
        nonlocal nodes, counterexample
        local_changes: list[tuple[int, tuple]] = []
        try:
            while True:
                obj, x, exceeded = solve(bounds)
                nodes += 1
                if exceeded:  # LP over free words > k -> no completion feasible
                    return True
                assert x is not None
                order = [
                    g
                    for g in np.argsort(-x).tolist()
                    if x[g] > tol and bounds[g] == free
                ]
                if in_count >= k or not order:
                    # Feasible with <= k integer words -> genuine counterexample.
                    counterexample = [g for g in range(G) if bounds[g] == (1.0, 1.0)]
                    return False
                w = order[0]
                if depth < verbose_depth:
                    tqdm.write(
                        "  " * depth + f"[d{depth}] in={in_count} obj={obj:.3f} "
                        f"branch on {allowed_guesses[w]} (w={x[w]:.3f})"
                    )
                old = bounds[w]
                bounds[w] = (1.0, 1.0)  # case: w IN
                local_changes.append((w, old))
                if not prove(in_count + 1, depth + 1):
                    return False  # counterexample found in the w-IN subtree
                bounds[w] = (0.0, 0.0)  # case: w OUT, continue loop
        finally:
            for idx, old in local_changes:
                bounds[idx] = old

    proved = prove(0, 0)
    if proved:
        print(
            f"PROVED (recursive): no {k}-word set leaves <= {slack_budget:g} pairs "
            f"undistinguished. Explored {nodes:,} LP nodes."
        )
        return True, None
    assert counterexample is not None
    left = _undistinguished_pair_count(fb, n, counterexample)
    print(
        f"COUNTEREXAMPLE ({nodes:,} nodes): {[allowed_guesses[g] for g in counterexample]} "
        f"leaves {left} pairs undistinguished (<= slack {slack_budget:g})."
    )
    return False, counterexample


def verify_no_cover_cut_and_branch(
    allowed_guesses: list[str],
    possible_solutions: list[str],
    k: int = 5,
    slack_budget: float = 0.0,
    cache_path: Path | None = None,
    max_rounds: int = 1000,
    add_per_round: int = 4000,
    node_cap: int = 2_000_000,
    tol: float = 1e-6,
    verbose_depth: int = 3,
) -> tuple[bool, list[int] | None]:
    """
    Exact branch-and-bound that branches on a *set* (hyperplane) instead of one variable.

    At each node, solve the LP. If its optimum > k, prune (infeasible). If the solution is
    integral, it is a concrete counterexample. Otherwise gather the highest-weight
    fractional words until their weights sum past 0.5 into a set S, and branch on the
    integer-valid disjunction:
        sum_{g in S} x_g <= 0   (none of S chosen: pin all of S to 0), or
        sum_{g in S} x_g >= 1   (at least one chosen: add that row as a path-local cut).
    Both branches cut off the current fractional point, so each makes progress. Excluding a
    whole batch at once (the <=0 branch) and the strong >=1 cut typically shrink the tree
    versus single-variable branching.

    Returns (proved, counterexample_word_indices_or_None).
    """
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix, identity, hstack, vstack

    tqdm = import_module("tqdm").tqdm
    fb = build_feedback_matrix(allowed_guesses, possible_solutions, cache_path)
    G, n = fb.shape
    base = _pair_base(n)
    npairs = n * (n - 1) // 2

    rows: list[np.ndarray] = []
    cols: list[np.ndarray] = []
    in_working: set[int] = set()
    ncon = 0

    def add_constraints(lins: np.ndarray) -> None:
        nonlocal ncon
        ii, jj = _lin_to_ij(np.asarray(lins, dtype=np.int64), base)
        for lin, i, j in zip(np.asarray(lins).tolist(), ii.tolist(), jj.tolist()):
            if lin in in_working:
                continue
            dist = np.flatnonzero(fb[:, i] != fb[:, j])
            rows.append(np.full(dist.size, ncon, dtype=np.int64))
            cols.append(dist)
            in_working.add(lin)
            ncon += 1

    seed_words = _greedy_cover_word_indices(fb, n)
    undist_count = np.zeros(npairs, dtype=np.int32)
    for g in seed_words:
        cls = fb[g]
        for cc in np.unique(cls):
            members = np.flatnonzero(cls == cc)
            if members.size >= 2:
                np.add.at(undist_count, _class_pair_lins(members, base), 1)
    add_constraints(np.flatnonzero(undist_count >= len(seed_words) - 2))
    print(f"Seeded shared pool with {ncon:,} hard-pair constraints")

    # Cached global pair-constraint block (with slack columns, no budget row).
    A_cache = None
    A_ncon = -1

    def global_A():
        nonlocal A_cache, A_ncon
        if A_ncon != ncon:
            A_word = csr_matrix(
                (
                    np.full(sum(r.size for r in rows), -1.0),
                    (np.concatenate(rows), np.concatenate(cols)),
                ),
                shape=(ncon, G),
            )
            if slack_budget > 0.0:
                A_cache = hstack([A_word, -identity(ncon, format="csr")], format="csr")
            else:
                A_cache = A_word
            A_ncon = ncon
        return A_cache

    def separate(x: np.ndarray, S: float) -> np.ndarray:
        U = np.zeros(npairs, dtype=np.float64)
        for g in np.flatnonzero(x > tol):
            cls = fb[g]
            for cc in np.unique(cls):
                members = np.flatnonzero(cls == cc)
                if members.size >= 2:
                    np.add.at(U, _class_pair_lins(members, base), x[g])
        violated = np.flatnonzero(U > S - 1.0 + tol)
        violated = violated[np.argsort(-U[violated])]
        return np.array(
            [v for v in violated.tolist() if v not in in_working], dtype=np.int64
        )

    c = np.ones(G, dtype=np.float64)

    def solve(bounds, path_cuts) -> tuple[float, np.ndarray | None, bool]:
        """LP over free words with the global pair pool plus the path-local `>=1` cuts
        (each a list of word indices). Returns (objective, x, exceeded)."""
        obj, x = float("inf"), None
        for _ in range(max_rounds):
            ncols = G + (ncon if slack_budget > 0.0 else 0)
            blocks = [global_A()]
            b_parts = [-np.ones(ncon)]
            if path_cuts:
                cr, cc_ = [], []
                for ri, Sset in enumerate(path_cuts):
                    cr.extend([ri] * len(Sset))
                    cc_.extend(Sset)
                blocks.append(
                    csr_matrix(
                        (np.full(len(cr), -1.0), (cr, cc_)),
                        shape=(len(path_cuts), ncols),
                    )
                )
                b_parts.append(-np.ones(len(path_cuts)))
            if slack_budget > 0.0:
                budget = csr_matrix(
                    (
                        np.ones(ncon),
                        (np.zeros(ncon, dtype=int), np.arange(G, G + ncon)),
                    ),
                    shape=(1, ncols),
                )
                blocks.append(budget)
                b_parts.append(np.array([slack_budget]))
                c_full = np.concatenate([c, np.zeros(ncon)])
                full_bounds = bounds + [(0.0, None)] * ncon
            else:
                c_full, full_bounds = c, bounds
            A = vstack(blocks, format="csr")
            res = linprog(
                c_full,
                A_ub=A,
                b_ub=np.concatenate(b_parts),
                bounds=full_bounds,
                method="highs",
            )
            if not res.success:
                return float("inf"), None, True
            x = res.x[:G]
            obj = float(res.fun)
            if obj > k + tol:
                return obj, x, True
            new = separate(x, float(x.sum()))
            if new.size == 0:
                return obj, x, False
            add_constraints(new[:add_per_round])
        return obj, x, False

    bounds = [(0.0, 1.0)] * G
    path_cuts: list[list[int]] = []
    nodes = 0
    counterexample: list[int] | None = None

    def prove(depth: int) -> bool:
        """True iff this branch is infeasible (no k-set with <= slack uncovered)."""
        nonlocal nodes, counterexample
        nodes += 1
        if nodes > node_cap:
            raise RuntimeError(f"node cap {node_cap} exceeded")
        obj, x, exceeded = solve(bounds, path_cuts)
        if exceeded:
            return True
        assert x is not None

        frac = [g for g in range(G) if tol < x[g] < 1.0 - tol]
        if not frac:  # integral solution with objective <= k -> counterexample
            counterexample = [g for g in range(G) if x[g] > 1.0 - tol]
            return False

        # Build S: highest-weight fractional words until their weights sum past 0.5.
        order = sorted(frac, key=lambda g: -x[g])
        S, tot = [], 0.0
        for g in order:
            S.append(g)
            tot += x[g]
            if tot > 0.5:
                break
        if depth < verbose_depth:
            tqdm.write(
                "  " * depth + f"[d{depth}] obj={obj:.3f} branch on sum of "
                f"{[allowed_guesses[g] for g in S]} (={tot:.3f})"
            )

        # Branch 1: sum_S <= 0  -> pin every word of S to 0.
        saved = [(g, bounds[g]) for g in S]
        for g in S:
            bounds[g] = (0.0, 0.0)
        none_ok = prove(depth + 1)
        for g, old in saved:
            bounds[g] = old
        if not none_ok:
            return False

        # Branch 2: sum_S >= 1  -> add a path-local cut.
        path_cuts.append(S)
        some_ok = prove(depth + 1)
        path_cuts.pop()
        return some_ok

    proved = prove(0)
    if proved:
        print(
            f"PROVED (cut & branch): no {k}-word set leaves <= {slack_budget:g} pairs "
            f"undistinguished. Explored {nodes:,} nodes."
        )
        return True, None
    assert counterexample is not None
    left = _undistinguished_pair_count(fb, n, counterexample)
    print(
        f"COUNTEREXAMPLE ({nodes:,} nodes): "
        f"{[allowed_guesses[g] for g in counterexample]} leaves {left} pairs "
        f"undistinguished (<= slack {slack_budget:g})."
    )
    return False, counterexample


def verify_no_cover_letter_branch(
    allowed_guesses: list[str],
    possible_solutions: list[str],
    k: int = 5,
    slack_budget: float = 0.0,
    cache_path: Path | None = None,
    max_rounds: int = 1000,
    add_per_round: int = 4000,
    node_cap: int = 2_000_000,
    sb_width: int = 6,
    tol: float = 1e-6,
    verbose_depth: int = 10,
) -> tuple[bool, list[int] | None]:
    """
    Exact branch-and-bound that branches on *letter presence* instead of individual words.

    The combinatorial hook: k=5 words of five letters each contain at most 25 distinct
    letters, so every 5-word set omits at least one letter of the alphabet. "Letter l is
    present" (some chosen word contains l) is therefore a natural binary decision, and it maps
    onto the same primitives as the word-set cut & branch:
        l ABSENT   -> pin x_g = 0 for every word g containing l   (a bounds change), or
        l PRESENT  -> add the cut  sum_{g contains l} x_g >= 1     (a path-local >=1 cut).
    Both branches cut off the current fractional point as long as the letter's presence weight
    P_l = sum_{g contains l} x_g lies strictly in (0, 1); we branch on the heaviest such letter.
    Forcing many letters present drives the bound up on its own: m present letters give
    sum_g x_g >= m/5 (each word has <= 5 letters), so the all-present region (m -> 26) is
    pruned without ever enumerating words. When no letter is fractional we fall back to the
    word-set disjunction, which keeps the search complete.

    Returns (proved, counterexample_word_indices_or_None), same contract as the other provers.
    """
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix, identity, hstack, vstack

    tqdm = import_module("tqdm").tqdm
    fb = build_feedback_matrix(allowed_guesses, possible_solutions, cache_path)
    G, n = fb.shape
    base = _pair_base(n)
    npairs = n * (n - 1) // 2

    # Per-letter branching forms over the guesses. For each letter a..z:
    #   letter_idx[l]  - indices of guesses containing the letter (>= 1 time),
    #   letter_unit[l] - all-ones coeffs -> the form counts the NUMBER OF GUESSES with l,
    #   letter_occ[l]  - coeffs = occurrences of l per guess -> the form counts the TOTAL
    #                    COUNT of l across the chosen guesses (a double letter counts twice).
    letter_idx: list[np.ndarray] = []
    letter_unit: list[np.ndarray] = []
    letter_occ: list[np.ndarray] = []
    for ell in range(26):
        ch = chr(ord("a") + ell)
        idx = [g for g, w in enumerate(allowed_guesses) if ch in w]
        letter_idx.append(np.array(idx, dtype=np.int64))
        letter_unit.append(np.ones(len(idx), dtype=np.float64))
        letter_occ.append(
            np.array([allowed_guesses[g].count(ch) for g in idx], dtype=np.float64)
        )

    rows: list[np.ndarray] = []
    cols: list[np.ndarray] = []
    in_working: set[int] = set()
    ncon = 0

    # Packing-prune candidates. Every answer pair is distinguished by hundreds-to-thousands
    # of words, so the disjoint-packing certificate can only fire *deep* in the tree, once
    # letter-absent branches have removed most words and the *available* distinguisher sets
    # shrink. We therefore track all pairs and let the per-node availability mask do the
    # work; PACK_CAP only bounds per-node cost if a pair somehow had a huge full set.
    PACK_CAP = 10_000
    pack_pool: list[int] = []

    def add_constraints(lins: np.ndarray) -> None:
        nonlocal ncon
        ii, jj = _lin_to_ij(np.asarray(lins, dtype=np.int64), base)
        for lin, i, j in zip(np.asarray(lins).tolist(), ii.tolist(), jj.tolist()):
            if lin in in_working:
                continue
            dist = np.flatnonzero(fb[:, i] != fb[:, j])
            rows.append(np.full(dist.size, ncon, dtype=np.int64))
            cols.append(dist)
            if dist.size <= PACK_CAP:
                pack_pool.append(ncon)
            in_working.add(lin)
            ncon += 1

    seed_words = _greedy_cover_word_indices(fb, n)
    undist_count = np.zeros(npairs, dtype=np.int32)
    for g in seed_words:
        cls = fb[g]
        for cc in np.unique(cls):
            members = np.flatnonzero(cls == cc)
            if members.size >= 2:
                np.add.at(undist_count, _class_pair_lins(members, base), 1)
    add_constraints(np.flatnonzero(undist_count >= len(seed_words) - 2))
    print(f"Seeded shared pool with {ncon:,} hard-pair constraints")

    A_cache = None
    A_ncon = -1

    def global_A():
        nonlocal A_cache, A_ncon
        if A_ncon != ncon:
            A_word = csr_matrix(
                (
                    np.full(sum(r.size for r in rows), -1.0),
                    (np.concatenate(rows), np.concatenate(cols)),
                ),
                shape=(ncon, G),
            )
            if slack_budget > 0.0:
                A_cache = hstack([A_word, -identity(ncon, format="csr")], format="csr")
            else:
                A_cache = A_word
            A_ncon = ncon
        return A_cache

    def separate(x: np.ndarray, S: float) -> np.ndarray:
        U = np.zeros(npairs, dtype=np.float64)
        for g in np.flatnonzero(x > tol):
            cls = fb[g]
            for cc in np.unique(cls):
                members = np.flatnonzero(cls == cc)
                if members.size >= 2:
                    np.add.at(U, _class_pair_lins(members, base), x[g])
        violated = np.flatnonzero(U > S - 1.0 + tol)
        violated = violated[np.argsort(-U[violated])]
        return np.array(
            [v for v in violated.tolist() if v not in in_working], dtype=np.int64
        )

    c = np.ones(G, dtype=np.float64)

    def lp_once(bounds, path_cuts) -> tuple[float, np.ndarray | None, bool]:
        """One LP solve over the current pair pool plus the path-local `>=1` cuts (each a
        list of word indices), no separation. Returns (objective, x_words, feasible)."""
        ncols = G + (ncon if slack_budget > 0.0 else 0)
        blocks = [global_A()]
        b_parts = [-np.ones(ncon)]
        if path_cuts:
            # Each path cut is (idx, coeffs, sense, rhs): "sum coeffs*x[idx]  sense  rhs",
            # sense in {">=", "<="}. linprog wants <= rows, so ">=" flips the sign.
            cr, cc_, vals, rhs_vec = [], [], [], []
            for ri, (idx, coeffs, sense, rhs) in enumerate(path_cuts):
                s = -1.0 if sense == ">=" else 1.0
                cr.extend([ri] * len(idx))
                cc_.extend(np.asarray(idx).tolist())
                vals.extend((s * np.asarray(coeffs, dtype=np.float64)).tolist())
                rhs_vec.append(-rhs if sense == ">=" else rhs)
            blocks.append(csr_matrix((vals, (cr, cc_)), shape=(len(path_cuts), ncols)))
            b_parts.append(np.array(rhs_vec, dtype=np.float64))
        if slack_budget > 0.0:
            budget = csr_matrix(
                (np.ones(ncon), (np.zeros(ncon, dtype=int), np.arange(G, G + ncon))),
                shape=(1, ncols),
            )
            blocks.append(budget)
            b_parts.append(np.array([slack_budget]))
            c_full = np.concatenate([c, np.zeros(ncon)])
            full_bounds = bounds + [(0.0, None)] * ncon
        else:
            c_full, full_bounds = c, bounds
        res = linprog(
            c_full,
            A_ub=vstack(blocks, format="csr"),
            b_ub=np.concatenate(b_parts),
            bounds=full_bounds,
            method="highs",
        )
        if not res.success:
            return float("inf"), None, False
        return float(res.fun), res.x[:G], True

    def lp_bound(bounds, path_cuts) -> float:
        """Cheap single-LP lower bound on a child (current pool only); inf if infeasible.
        Used to score strong-branching candidates without the separation loop."""
        return lp_once(bounds, path_cuts)[0]

    def solve(bounds, path_cuts) -> tuple[float, np.ndarray | None, bool]:
        """Constraint-generate to convergence (or until the bound exceeds k). Returns
        (objective, x, exceeded)."""
        obj, x = float("inf"), None
        for _ in range(max_rounds):
            obj, x, feasible = lp_once(bounds, path_cuts)
            if not feasible or x is None:
                return float("inf"), None, True
            if obj > k + tol:
                return obj, x, True
            new = separate(x, float(x.sum()))
            if new.size == 0:
                return obj, x, False
            add_constraints(new[:add_per_round])
        return obj, x, False

    bounds = [(0.0, 1.0)] * G
    path_cuts: list = []  # entries: (idx, coeffs, sense, rhs) weighted >=/<= cuts
    nodes = 0
    pack_prunes = 0
    slack_floor = int(slack_budget + tol)  # whole pairs that may be sacrificed
    counterexample: list[int] | None = None

    def packing_prune(depth: int) -> bool:
        """LP-free infeasibility certificate. Among the available words (not pinned to 0),
        greedily pack hard pairs whose distinguisher sets are mutually disjoint (smallest
        first; a pair with no available distinguisher is a forced sacrifice). If more than
        k + slack_floor such pairs exist, every covered one needs its own distinct word and
        at most slack_floor can be sacrificed, so no k-word solution fits -> prune."""
        nonlocal pack_prunes
        avail = np.fromiter((b[1] > 0.0 for b in bounds), dtype=bool, count=G)
        cand = []
        for cidx in pack_pool:
            cset = cols[cidx]
            d = cset[avail[cset]]
            cand.append((d.size, d))
        cand.sort(key=lambda t: t[0])

        used = np.zeros(G, dtype=bool)
        m = 0
        need = k + slack_floor
        for sz, d in cand:
            if sz == 0:  # no available word distinguishes it -> must be sacrificed
                m += 1
            elif not used[d].any():
                used[d] = True
                m += 1
            if m > need:
                pack_prunes += 1
                if depth < verbose_depth:
                    tqdm.write(
                        "  "
                        * depth
                        + f"[depth {depth}] PRUNED without an LP: found {m} "
                        f"answer-pairs whose remaining distinguishing guesses are all "
                        f"disjoint, so covering all but {slack_floor} of them already "
                        f"needs {m - slack_floor} distinct guesses > {k}. No solution here."
                    )
                return True
        return False

    def with_pinned(idx: np.ndarray, fn):
        """Run fn() with every word in idx pinned to 0, then restore the bounds."""
        saved = [(g, bounds[g]) for g in idx.tolist()]
        for g in idx.tolist():
            bounds[g] = (0.0, 0.0)
        try:
            return fn()
        finally:
            for g, old in saved:
                bounds[g] = old

    def child_bound(idx, coeffs, t: int, high: bool) -> float:
        """Single-LP bound for one child of a form-threshold split on `sum coeffs*x[idx]`.
        high=False: `<= t-1`; high=True: `>= t`. The t==1 low child is `<= 0`, i.e. pin
        idx to 0 (keeps the packing prune's availability exact)."""
        if high:
            path_cuts.append((idx, coeffs, ">=", t))
            b = lp_bound(bounds, path_cuts)
            path_cuts.pop()
            return b
        if t == 1:
            return with_pinned(idx, lambda: lp_bound(bounds, path_cuts))
        path_cuts.append((idx, coeffs, "<=", t - 1))
        b = lp_bound(bounds, path_cuts)
        path_cuts.pop()
        return b

    def branch_form(depth: int, idx, coeffs, t: int) -> bool:
        """Branch on the linear form `sum coeffs*x[idx]` at threshold t: explore the low
        child (`<= t-1`) then the high child (`>= t`). Both cut off the current LP point
        when the form's value is fractional around t."""
        if t == 1:
            low_ok = with_pinned(idx, lambda: prove(depth + 1))
        else:
            path_cuts.append((idx, coeffs, "<=", t - 1))
            low_ok = prove(depth + 1)
            path_cuts.pop()
        if not low_ok:
            return False
        path_cuts.append((idx, coeffs, ">=", t))
        high_ok = prove(depth + 1)
        path_cuts.pop()
        return high_ok

    def prove(depth: int) -> bool:
        """True iff this branch is infeasible (no k-set with <= slack uncovered)."""
        nonlocal nodes, counterexample
        nodes += 1
        if nodes > node_cap:
            raise RuntimeError(f"node cap {node_cap} exceeded")
        if packing_prune(depth):  # cheap LP-free certificate before the slow LP
            return True
        obj, x, exceeded = solve(bounds, path_cuts)
        if exceeded:
            return True
        assert x is not None

        frac_words = [g for g in range(G) if tol < x[g] < 1.0 - tol]
        if not frac_words:  # integral solution with objective <= k -> counterexample
            counterexample = [g for g in range(G) if x[g] > 1.0 - tol]
            return False

        # Branching candidates: for each letter, two linear forms over the chosen words --
        # WORD count (unit coeffs: how many guesses contain the letter) and OCCURRENCE
        # count (coeffs = occurrences per guess: how many times the letter appears in
        # total, so a doubled letter counts twice). A form whose LP value v is fractional
        # is split at t = floor(v)+1; both children (<= t-1 and >= t) cut the current point.
        cands = []  # (balance, kind, ell, idx, coeffs, t, v)
        for ell in range(26):
            idx = letter_idx[ell]
            if idx.size == 0:
                continue
            xi = x[idx]
            for kind, coeffs in (
                ("words", letter_unit[ell]),
                ("count", letter_occ[ell]),
            ):
                v = float(coeffs @ xi)
                t = int(np.floor(v + tol)) + 1
                fracpart = v - (t - 1)
                if tol < fracpart < 1.0 - tol:
                    cands.append(
                        (min(fracpart, 1.0 - fracpart), kind, ell, idx, coeffs, t, v)
                    )

        if cands:
            # Strong branching: shortlist the most balanced forms (value near a half-integer,
            # so both children move most), then pick the one whose *weaker* child has the
            # highest single-LP bound -- max of min(low, high). Since the proof must close
            # both children, the weaker child is what matters.
            cands.sort(key=lambda cterm: -cterm[0])
            best = None
            for _bal, kind, ell, idx, coeffs, t, v in cands[:sb_width]:
                lo = child_bound(idx, coeffs, t, high=False)
                hi = child_bound(idx, coeffs, t, high=True)
                score = min(lo, hi)
                if best is None or score > best[0]:
                    best = (score, kind, ell, idx, coeffs, t, v, lo, hi)
            assert best is not None
            score, kind, ell, idx, coeffs, t, v, lo, hi = best
            if depth < verbose_depth:
                L = chr(ord("a") + ell)
                what = (
                    f"the number of guesses containing '{L}'"
                    if kind == "words"
                    else f"the total number of '{L}'s across the guesses "
                    "(a doubled letter counts twice)"
                )
                tqdm.write(
                    "  " * depth + f"[depth {depth}] this node needs >= {obj:.2f} "
                    f"guesses. Splitting on {what} (LP puts it at {v:.2f}): "
                    f"[<= {t - 1} -> needs >= {lo:.2f} guesses] vs "
                    f"[>= {t} -> needs >= {hi:.2f} guesses]. Ruling the node out needs "
                    f"BOTH cases above {k}; the weaker side is {score:.2f} "
                    f"(best of {min(sb_width, len(cands))} candidate cuts)."
                )
            return branch_form(depth, idx, coeffs, t)

        # Fallback: every letter form is integral but x is still fractional -> branch on a
        # word group (highest-weight fractional guesses whose weights sum past 0.5).
        order = sorted(frac_words, key=lambda g: -x[g])
        S, tot = [], 0.0
        for g in order:
            S.append(g)
            tot += x[g]
            if tot > 0.5:
                break
        S_idx = np.array(S, dtype=np.int64)
        if depth < verbose_depth:
            tqdm.write(
                "  " * depth + f"[depth {depth}] this node needs >= {obj:.2f} guesses. "
                f"No letter form is fractional, so splitting on the guess group "
                f"{[allowed_guesses[g] for g in S]}: [none chosen] vs [at least one chosen]."
            )
        return branch_form(depth, S_idx, np.ones(len(S)), 1)

    proved = prove(0)
    if proved:
        print(
            f"PROVED (letter branch): no {k}-word set leaves <= {slack_budget:g} pairs "
            f"undistinguished. Explored {nodes:,} nodes "
            f"({pack_prunes:,} closed by packing, {ncon:,} pool constraints)."
        )
        return True, None
    assert counterexample is not None
    left = _undistinguished_pair_count(fb, n, counterexample)
    print(
        f"COUNTEREXAMPLE ({nodes:,} nodes, {pack_prunes:,} packing prunes): "
        f"{[allowed_guesses[g] for g in counterexample]} leaves {left} pairs "
        f"undistinguished (<= slack {slack_budget:g})."
    )
    return False, counterexample


def climb_slack_lower_bound(
    allowed_guesses: list[str],
    possible_solutions: list[str],
    k: int = 5,
    cache_path: Path | None = None,
    sb_width: int = 6,
    max_rounds: int = 1000,
    add_per_round: int = 4000,
    node_cap: int = 2_000_000,
    tol: float = 1e-6,
    verbose_depth: int = 10,
) -> int:
    """
    Fix the number of guesses at `k` and push a lower bound on the *slack* -- the number of
    answer pairs any k-guess set must leave undistinguished -- as high as it will go.

    The per-node LP (relaxation, over a growing subset of pairs) is

        minimize   sum_p s_p                                  (pairs left undistinguished)
        s.t.       sum_{g distinguishes p} x_g + s_p >= 1     for every pooled pair p
                   sum_g x_g <= k                             (hard guess budget)
                   0 <= x_g <= 1,   s_p >= 0

    whose optimum lower-bounds the integer minimum slack. We prove `min slack >= target` for
    target = 1, 2, 3, ... by branch-and-bound: a node is pruned once its LP slack bound
    rounds up to >= target, and an integral k-set with slack < target is a counterexample.
    Branching is on letter forms (number of guesses with a letter, and total count of a
    letter) chosen by strong branching, exactly as in the dual `verify_no_cover_letter_branch`
    -- only the LP's objective and the budget constraint are swapped. The first target that
    yields a counterexample pins the exact minimum slack (= target - 1). Returns that minimum.
    """
    from scipy.optimize import linprog
    from scipy.sparse import csr_matrix, identity, hstack, vstack

    tqdm = import_module("tqdm").tqdm
    fb = build_feedback_matrix(allowed_guesses, possible_solutions, cache_path)
    G, n = fb.shape
    base = _pair_base(n)
    npairs = n * (n - 1) // 2

    # Per-letter branching forms (see verify_no_cover_letter_branch for the rationale).
    letter_idx: list[np.ndarray] = []
    letter_unit: list[np.ndarray] = []
    letter_occ: list[np.ndarray] = []
    for ell in range(26):
        ch = chr(ord("a") + ell)
        idx = [g for g, w in enumerate(allowed_guesses) if ch in w]
        letter_idx.append(np.array(idx, dtype=np.int64))
        letter_unit.append(np.ones(len(idx), dtype=np.float64))
        letter_occ.append(
            np.array([allowed_guesses[g].count(ch) for g in idx], dtype=np.float64)
        )

    # Growing pool of pair-coverage rows: cols[c] = words distinguishing pooled pair c.
    rows: list[np.ndarray] = []
    cols: list[np.ndarray] = []
    in_working: set[int] = set()
    ncon = 0

    def add_constraints(lins: np.ndarray) -> None:
        nonlocal ncon
        ii, jj = _lin_to_ij(np.asarray(lins, dtype=np.int64), base)
        for lin, i, j in zip(np.asarray(lins).tolist(), ii.tolist(), jj.tolist()):
            if lin in in_working:
                continue
            dist = np.flatnonzero(fb[:, i] != fb[:, j])
            rows.append(np.full(dist.size, ncon, dtype=np.int64))
            cols.append(dist)
            in_working.add(lin)
            ncon += 1

    # Seed with the hardest pairs of a greedy cover.
    seed_words = _greedy_cover_word_indices(fb, n)
    undist_count = np.zeros(npairs, dtype=np.int32)
    for g in seed_words:
        cls = fb[g]
        for cc in np.unique(cls):
            members = np.flatnonzero(cls == cc)
            if members.size >= 2:
                np.add.at(undist_count, _class_pair_lins(members, base), 1)
    add_constraints(np.flatnonzero(undist_count >= len(seed_words) - 2))
    print(f"Seeded shared pool with {ncon:,} hard-pair constraints")

    # Coverage block [A_word | -I]: row c is -sum_{g in cols[c]} x_g - s_c <= -1.
    A_cache = None
    A_ncon = -1

    def coverage_block():
        nonlocal A_cache, A_ncon
        if A_ncon != ncon:
            A_word = csr_matrix(
                (
                    np.full(sum(r.size for r in rows), -1.0),
                    (np.concatenate(rows), np.concatenate(cols)),
                ),
                shape=(ncon, G),
            )
            A_cache = hstack([A_word, -identity(ncon, format="csr")], format="csr")
            A_ncon = ncon
        return A_cache

    def separate(x: np.ndarray) -> np.ndarray:
        """Pairs (not yet pooled) that the current x leaves with coverage < 1; adding them
        raises the slack objective. coverage(p) = sum_g x_g - U(p), U = non-distinguishers."""
        S = float(x.sum())
        U = np.zeros(npairs, dtype=np.float64)
        for g in np.flatnonzero(x > tol):
            cls = fb[g]
            for cc in np.unique(cls):
                members = np.flatnonzero(cls == cc)
                if members.size >= 2:
                    np.add.at(U, _class_pair_lins(members, base), x[g])
        violated = np.flatnonzero(U > S - 1.0 + tol)
        violated = violated[np.argsort(-U[violated])]
        return np.array(
            [v for v in violated.tolist() if v not in in_working], dtype=np.int64
        )

    def lp_once(bounds, path_cuts) -> tuple[float, np.ndarray]:
        """Minimize total slack over the current pool. Always feasible (x=0, s=1). Returns
        (slack_objective, x_words)."""
        ncols = G + ncon
        blocks = [coverage_block()]
        b_parts = [-np.ones(ncon)]
        if path_cuts:
            cr, cc_, vals, rhs_vec = [], [], [], []
            for ri, (idx, coeffs, sense, rhs) in enumerate(path_cuts):
                s = -1.0 if sense == ">=" else 1.0
                cr.extend([ri] * len(idx))
                cc_.extend(np.asarray(idx).tolist())
                vals.extend((s * np.asarray(coeffs, dtype=np.float64)).tolist())
                rhs_vec.append(-rhs if sense == ">=" else rhs)
            blocks.append(csr_matrix((vals, (cr, cc_)), shape=(len(path_cuts), ncols)))
            b_parts.append(np.array(rhs_vec, dtype=np.float64))
        # Hard guess budget: sum_g x_g <= k.
        blocks.append(
            csr_matrix(
                (np.ones(G), (np.zeros(G, dtype=int), np.arange(G))), shape=(1, ncols)
            )
        )
        b_parts.append(np.array([float(k)]))
        c_full = np.concatenate([np.zeros(G), np.ones(ncon)])
        full_bounds = bounds + [(0.0, None)] * ncon
        res = linprog(
            c_full,
            A_ub=vstack(blocks, format="csr"),
            b_ub=np.concatenate(b_parts),
            bounds=full_bounds,
            method="highs",
        )
        if not res.success:
            raise RuntimeError(f"slack LP failed: {res.message}")
        return float(res.fun), res.x[:G]

    def lp_bound(bounds, path_cuts) -> float:
        return lp_once(bounds, path_cuts)[0]

    def solve(bounds, path_cuts, target) -> tuple[float, np.ndarray, bool]:
        """Constraint-generate until converged or the slack bound rounds up to >= target.
        Returns (objective, x, exceeded); exceeded => node's min slack >= target."""
        obj, x = 0.0, np.zeros(G)
        for _ in range(max_rounds):
            obj, x = lp_once(bounds, path_cuts)
            if (
                obj > target - 1.0 + tol
            ):  # ceil(obj) >= target -> every integer >= target
                return obj, x, True
            new = separate(x)
            if new.size == 0:
                return obj, x, False
            add_constraints(new[:add_per_round])
        return obj, x, False

    bounds = [(0.0, 1.0)] * G
    path_cuts: list = []  # (idx, coeffs, sense, rhs) weighted >=/<= cuts on x
    nodes = 0
    counterexample: list[int] | None = None

    def with_pinned(idx: np.ndarray, fn):
        saved = [(g, bounds[g]) for g in idx.tolist()]
        for g in idx.tolist():
            bounds[g] = (0.0, 0.0)
        try:
            return fn()
        finally:
            for g, old in saved:
                bounds[g] = old

    def child_bound(idx, coeffs, t: int, high: bool) -> float:
        if high:
            path_cuts.append((idx, coeffs, ">=", t))
            b = lp_bound(bounds, path_cuts)
            path_cuts.pop()
            return b
        if t == 1:
            return with_pinned(idx, lambda: lp_bound(bounds, path_cuts))
        path_cuts.append((idx, coeffs, "<=", t - 1))
        b = lp_bound(bounds, path_cuts)
        path_cuts.pop()
        return b

    def branch_form(depth, idx, coeffs, t, target) -> bool:
        if t == 1:
            low_ok = with_pinned(idx, lambda: prove(depth + 1, target))
        else:
            path_cuts.append((idx, coeffs, "<=", t - 1))
            low_ok = prove(depth + 1, target)
            path_cuts.pop()
        if not low_ok:
            return False
        path_cuts.append((idx, coeffs, ">=", t))
        high_ok = prove(depth + 1, target)
        path_cuts.pop()
        return high_ok

    def prove(depth: int, target: int) -> bool:
        """True iff every k-set in this node leaves >= target pairs undistinguished."""
        nonlocal nodes, counterexample
        nodes += 1
        if nodes > node_cap:
            raise RuntimeError(f"node cap {node_cap} exceeded")
        obj, x, exceeded = solve(bounds, path_cuts, target)
        if exceeded:
            return True

        frac_words = [g for g in range(G) if tol < x[g] < 1.0 - tol]
        if not frac_words:  # integral k-set, fully separated -> obj is its true slack
            chosen = [g for g in range(G) if x[g] > 1.0 - tol]
            counterexample = chosen
            return False

        cands = []  # (balance, kind, ell, idx, coeffs, t, v)
        for ell in range(26):
            idx = letter_idx[ell]
            if idx.size == 0:
                continue
            xi = x[idx]
            for kind, coeffs in (
                ("words", letter_unit[ell]),
                ("count", letter_occ[ell]),
            ):
                v = float(coeffs @ xi)
                t = int(np.floor(v + tol)) + 1
                fracpart = v - (t - 1)
                if tol < fracpart < 1.0 - tol:
                    cands.append(
                        (min(fracpart, 1.0 - fracpart), kind, ell, idx, coeffs, t, v)
                    )

        # Also offer the single heaviest fractional guess as a plain 0/1 inclusion split:
        # a one-word form at threshold 1 (low child pins x_g = 0, high child forces x_g = 1).
        gmax = max(frac_words, key=lambda g: x[g])
        cands.append(
            (
                min(x[gmax], 1.0 - x[gmax]),
                "guess",
                gmax,
                np.array([gmax], dtype=np.int64),
                np.ones(1),
                1,
                x[gmax],
            )
        )

        if cands:
            cands.sort(key=lambda cterm: -cterm[0])
            best = None
            for _bal, kind, ell, idx, coeffs, t, v in cands[:sb_width]:
                lo = child_bound(idx, coeffs, t, high=False)
                hi = child_bound(idx, coeffs, t, high=True)
                score = min(lo, hi)
                if best is None or score > best[0]:
                    best = (score, kind, ell, idx, coeffs, t, v, lo, hi)
            assert best is not None
            score, kind, ell, idx, coeffs, t, v, lo, hi = best
            if depth < verbose_depth:
                L = chr(ord("a") + ell)
                if kind == "words":
                    what = f"the number of guesses containing '{L}'"
                elif kind == "count":
                    what = (
                        f"the total number of '{L}'s across the guesses "
                        "(a doubled letter counts twice)"
                    )
                else:  # single-guess 0/1 inclusion
                    what = f"whether guess '{allowed_guesses[int(idx[0])]}' is used"
                split = (
                    f"[exclude -> slack >= {lo:.2f}] vs [include -> slack >= {hi:.2f}]"
                    if kind == "guess"
                    else f"[<= {t - 1} -> slack >= {lo:.2f}] vs "
                    f"[>= {t} -> slack >= {hi:.2f}]"
                )
                tqdm.write(
                    "  " * depth + f"[depth {depth}] LP slack bound {obj:.2f} "
                    f"(proving >= {target}). Splitting on {what} (LP at {v:.2f}): "
                    f"{split}; weaker side {score:.2f} "
                    f"(best of {min(sb_width, len(cands))})."
                )
            return branch_form(depth, idx, coeffs, t, target)

        order = sorted(frac_words, key=lambda g: -x[g])
        S, tot = [], 0.0
        for g in order:
            S.append(g)
            tot += x[g]
            if tot > 0.5:
                break
        if depth < verbose_depth:
            tqdm.write(
                "  " * depth + f"[depth {depth}] LP slack bound {obj:.2f} "
                f"(proving >= {target}). No fractional letter form; splitting on guesses "
                f"{[allowed_guesses[g] for g in S]}: [none] vs [>= 1]."
            )
        return branch_form(
            depth, np.array(S, dtype=np.int64), np.ones(len(S)), 1, target
        )

    # Climb the target: prove min slack >= 1, >= 2, ... until a counterexample appears.
    best_lb = 0
    target = 1
    while True:
        bounds[:] = [(0.0, 1.0)] * G
        path_cuts.clear()
        nodes = 0
        counterexample = None
        print(f"\n--- Proving every {k}-guess set leaves >= {target} pair(s) ---")
        proved = prove(0, target)
        if proved:
            best_lb = target
            print(
                f">>> PROVED: every {k}-guess set leaves >= {target} pairs undistinguished "
                f"({nodes:,} nodes, {ncon:,} pool constraints)."
            )
            target += 1
            continue
        assert counterexample is not None
        left = _undistinguished_pair_count(fb, n, counterexample)
        print(
            f">>> COUNTEREXAMPLE ({nodes:,} nodes): "
            f"{[allowed_guesses[g] for g in counterexample]} leaves only {left} pairs "
            f"undistinguished. So the minimum slack is exactly {best_lb} "
            f"(proved >= {best_lb}, achieved {left})."
        )
        return best_lb


def load_word_list(path: Path) -> list[str]:
    with path.open() as f:
        return [line.strip() for line in f if line.strip()]


def main() -> None:
    data_dir = Path(__file__).with_name("data")
    allowed_guesses = load_word_list(data_dir / "allowed.txt")
    possible_solutions = load_word_list(data_dir / "answers.txt")

    # Fix the guess budget at 5 and push the lower bound on the slack (number of pairs left
    # undistinguished) as high as it goes, until it meets a concrete 5-guess set -- which
    # pins the exact minimum slack.
    print(
        "\n=== Minimum slack of any 5-guess set (fixed budget, rising slack bound) ==="
    )
    best = climb_slack_lower_bound(
        allowed_guesses,
        possible_solutions,
        k=5,
        cache_path=data_dir / "feedback_cache.npy",
    )
    print(f"\nMinimum pairs left undistinguished by any 5-guess set: {best}")


if __name__ == "__main__":
    main()
