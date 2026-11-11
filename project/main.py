"""Run the ocean carbon model and print how carbon changes over time."""

from carbon import exact_solution, simulate

M0 = 1.0      # starting ocean carbon (arbitrary units)
F = 0.5       # volcanic input per unit time
K = 0.1       # burial rate constant
T_END = 50.0
DT = 0.01


def main() -> None:
    times, amounts = simulate(M0, F, K, T_END, DT)
    print(f"Steady volcanic source F={F}, burial k={K}, steady state F/k={F / K}")
    print(f"{'time':>6}  {'simulated':>10}  {'exact':>10}")
    for t, M in list(zip(times, amounts))[:: round(5 / DT)]:
        print(f"{t:6.1f}  {M:10.4f}  {exact_solution(t, M0, F, K):10.4f}")


if __name__ == "__main__":
    main()
