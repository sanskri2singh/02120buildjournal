"""Run the ocean carbon model and print how carbon changes over time."""

from carbon import exact_solution, simulate

def main() -> None:
    times, carbonamounts = simulate(1.0, 0.5, 0.1, 10, 0.01)
    print(exact_solution(10, 1.0, 0.5, 0.1))
    print(carbonamounts[-1])

if __name__ == "__main__":
    main()
