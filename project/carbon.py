import math

def exact_solution(t: float, Mi: float, F: float, k: float) -> float:
    return (F / k) + ((Mi - (F / k)) * (math.e ** (-1 * k * t)))


def simulate(Mi: float, F: float, k: float, t_end: float, dt: float,
             d_i: float = 0.0, d_F: float = -5.0) -> tuple[list[float], list[float], list[float]]:
    M = Mi
    d = d_i
    t = 0.0
    rate = findrate(F, k, M)
    steps = round(t_end / dt)
    times = [t]
    carbonamounts = [Mi]
    deltas = [d_i]

    for i in range(1, steps + 1):
        t = i * dt
        times.append(t)

        # burial takes carbon out at the ocean's own d13C, so d is unchanged by it
        remaining = M - (k * M * dt)
        # volcanoes add F*dt of carbon at d_F
        added = F * dt
        if remaining + added > 0:
            d = mix(remaining, d, added, d_F)
        deltas.append(d)

        M += (rate * dt)
        carbonamounts.append(M)
        rate = findrate(F, k, M)

    return times, carbonamounts, deltas

def findrate(F: float, k: float, M: float) -> float:
    return F - (k * M)

def mix(M_ocean: float, d_ocean: float, M_added: float, d_added: float) -> float:
    return ((M_ocean * d_ocean) + (M_added * d_added)) / (M_ocean + M_added)

