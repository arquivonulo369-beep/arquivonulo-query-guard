import argparse
from engine.guard import run_guard
from engine.logger import log_result
from engine.config import LOG_PATH


def main():
    parser = argparse.ArgumentParser(description="Query Guard CLI")

    parser.add_argument("--sql", required=True, help="SQL query to execute")
    parser.add_argument("--name", required=True, help="Query name identifier")
    parser.add_argument("--environment", default="dev", help="Environment (dev/prod)")
    parser.add_argument("--threshold", type=float, default=None, help="Override threshold in GB")
    parser.add_argument("--simulate", action="store_true", help="Simulate execution without running query")

    args = parser.parse_args()

    result = run_guard(
        sql=args.sql,
        query_name=args.name,
        environment=args.environment,
        cli_threshold=args.threshold,
        simulate=args.simulate
    )

    log_result(result, LOG_PATH)
    print(result)


if __name__ == "__main__":
    main()

