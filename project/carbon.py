"""Ocean carbon model: one reservoir, a steady volcanic source, and burial.

The ocean holds an amount of carbon M. Volcanoes add carbon at a steady
rate F, and burial removes it at a rate proportional to M:

    dM/dt = F - k * M

This is the smallest version of the model in the project proposal.
Isotopes and the microbial source come next.
"""

import math


def exact_solution(t: float, M0: float, F: float, k: float) -> float:
    """Exact answer to dM/dt = F - k*M, starting from M0 at t = 0."""
    steady_state = F / k
    return steady_state + (M0 - steady_state) * math.exp(-k * t)


def rate_of_change(M: float, F: float, k: float) -> float:
    """dM/dt: carbon added by volcanoes minus carbon removed by burial."""
    return F - k * M


def simulate(M0: float, F: float, k: float, t_end: float, dt: float):
    """Step the model forward from t = 0 to t_end in steps of dt.

    Uses Euler's method: the next value is the current value plus
    (rate of change) * dt. Returns two lists: times and carbon amounts.
    """
    steps = round(t_end / dt)
    times = [0.0]
    amounts = [M0]
    M = M0
    for step in range(1, steps + 1):
        M = M + rate_of_change(M, F, k) * dt
        times.append(step * dt)
        amounts.append(M)
    return times, amounts
