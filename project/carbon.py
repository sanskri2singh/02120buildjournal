import math

def exact_solution(t: float, Mi: float, F: float, k: float) -> float:
    return (F / k) + ((Mi - (F / k)) * (math.e ** (-1 * k * t)))


def simulate(Mi: float, F: float, k: float, t_end: float, dt: float) -> tuple[list[float], list[float]]:
    M = Mi
    t = 0.0
    rate = findrate(F, k, M)
    steps = round(t_end / dt)
    times = [t]
    carbonamounts = [Mi]

    for i in range(1, steps + 1):
        t = i * dt
        times.append(t)
        M += (rate * dt)
        carbonamounts.append(M)
        rate = findrate(F, k, M)

    return times, carbonamounts

def findrate(F: float, k: float, M: float) -> float:
    return F - (k * M)

