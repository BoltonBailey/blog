#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "tqdm",
# ]
# ///

import random
from collections import Counter
from importlib import import_module
from pathlib import Path


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


def distinguishing_pairs_list(
    allowed_guesses: list[str], possible_solutions: list[str]
) -> list[tuple[int, str, str]]:
    total_solutions = len(possible_solutions)
    distinguishing_pairs: list[tuple[int, str, str]] = []
    tqdm = import_module("tqdm").tqdm

    for guess in tqdm(allowed_guesses, desc="Scoring guesses", unit="guess"):
        feedbacks = [get_feedback(solution, guess) for solution in possible_solutions]
        feedback_counts = Counter(feedbacks)

        for solution, feedback in zip(possible_solutions, feedbacks):
            distinguishing_size = total_solutions - feedback_counts[feedback]
            distinguishing_pairs.append((distinguishing_size, solution, guess))

    return sorted(distinguishing_pairs)


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


def count_pairs_distinguished_by(
    word: str, possible_solutions: list[str]
) -> int:
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
    GREEN  = "\033[42;30m"
    YELLOW = "\033[43;30m"
    GRAY   = "\033[100;37m"
    RESET  = "\033[0m"
    COLOR  = {"G": GREEN, "Y": YELLOW, "B": GRAY}

    print(f"    Undistinguished: '{solution}' vs '{other}'")
    for word in selected_words:
        feedback = get_feedback(solution, word)  # identical for `other` as answer
        colored = " ".join(f"{COLOR[fb]}{letter.upper()}{RESET}" for letter, fb in zip(word, feedback))
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
            print(f"Step {step}: no word distinguishes remaining {undistinguished:,} pairs — stopping")
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


def load_word_list(path: Path) -> list[str]:
    with path.open() as f:
        return [line.strip() for line in f if line.strip()]


def main() -> None:
    data_dir = Path(__file__).with_name("data")
    allowed_guesses = load_word_list(data_dir / "allowed.txt")
    possible_solutions = load_word_list(data_dir / "answers.txt")

    print("Greedy distinguishing cover:")
    greedy_distinguishing_cover(allowed_guesses, possible_solutions)


if __name__ == "__main__":
    main()
