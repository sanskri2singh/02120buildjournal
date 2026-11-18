"""Run the ocean carbon model and print how carbon changes over time."""

from carbon import exact_solution, simulate

def main() -> None:
    Mi, F, k = 1.0, 0.5, 0.1
    t_end, dt = 10, 0.01

    times, carbonamounts, _ = simulate(Mi, F, k, t_end, dt)

    print(exact_solution(times[-1], Mi, F, k))
    print(carbonamounts[-1])

if __name__ == "__main__":
    main()
