import carbon

def test_matches_exact_solution() -> float:
    Mi, F, k = 1.0, 0.5, 0.1
    times, carbonamounts = carbon.simulate(Mi, F, k, 10, 0.01)

    difference = 0.0
    for t, M in zip(times, carbonamounts):
        gap = abs(carbon.exact_solution(t, Mi, F, k) - M)
        if gap > difference:
            difference = gap

    assert difference < 0.001, f"simulate is off from exact_solution by {difference}"
    return difference

def test_halving_dt() -> float:
    Mi, F, k = 1.0, 0.5, 0.1
    _, coarse = carbon.simulate(Mi, F, k, 10, 0.01)
    _, fine = carbon.simulate(Mi, F, k, 10, 0.005)

    change = abs(coarse[-1] - fine[-1])

    assert change < 0.001, f"halving dt changed the final carbon by {change}"
    return change


def test_growth_slows() -> int:
    Mi, F, k = 1.0, 0.5, 0.1
    _, carbonamounts = carbon.simulate(Mi, F, k, 50, 0.01)

    increases = []
    for i in range(1, len(carbonamounts)):
        increases.append(carbonamounts[i] - carbonamounts[i - 1])

    for i in range(1, len(increases)):
        assert increases[i] > 0, f"carbon stopped rising at step {i}"
        assert increases[i] < increases[i - 1], f"growth sped up at step {i}"
    return len(increases)


if __name__ == "__main__":
    biggest = test_matches_exact_solution()
    print(f"passed: largest difference is {biggest}")

    change = test_halving_dt()
    print(f"passed: halving dt changed the final carbon by {change}")

    steps = test_growth_slows()
    print(f"passed: growth slowed down at every one of {steps} steps")
    