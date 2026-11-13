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


if __name__ == "__main__":
    biggest = test_matches_exact_solution()
    print(f"passed: largest difference is {biggest}")