"""Checks for carbon.py, from section 3 of the project proposal.

Run with:  python3 project/test_carbon.py
"""

from carbon import exact_solution, simulate

# Example parameters in arbitrary units.
M0 = 1.0      # starting ocean carbon
F = 0.5       # volcanic input per unit time
K = 0.1       # burial rate constant
T_END = 50.0  # how long to run


def test_matches_exact_solution():
    """The simulation must match M(t) = F/k + (M0 - F/k) e^(-kt)."""
    times, amounts = simulate(M0, F, K, T_END, dt=0.001)
    worst_error = max(
        abs(M - exact_solution(t, M0, F, K)) for t, M in zip(times, amounts)
    )
    assert worst_error < 1e-3, f"off from exact solution by {worst_error}"


def test_halving_time_step_barely_changes_results():
    """Check 3: halving dt should barely change the final answer."""
    _, coarse = simulate(M0, F, K, T_END, dt=0.01)
    _, fine = simulate(M0, F, K, T_END, dt=0.005)
    change = abs(coarse[-1] - fine[-1])
    assert change < 1e-3, f"halving dt changed the result by {change}"


def test_steady_source_growth_slows_down():
    """Rothman's point: a steady source makes carbon grow more and more slowly."""
    _, amounts = simulate(M0, F, K, T_END, dt=0.01)
    growth = [later - earlier for earlier, later in zip(amounts, amounts[1:])]
    assert all(g > 0 for g in growth), "carbon should keep rising"
    assert all(
        later < earlier for earlier, later in zip(growth, growth[1:])
    ), "growth should keep slowing down"


if __name__ == "__main__":
    tests = [
        test_matches_exact_solution,
        test_halving_time_step_barely_changes_results,
        test_steady_source_growth_slows_down,
    ]
    for test in tests:
        test()
        print(f"PASS  {test.__name__}")
    print(f"All {len(tests)} checks passed.")
