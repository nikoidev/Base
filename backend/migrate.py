"""
Database migration management script.
Use this to apply or create migrations easily.
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str]) -> int:
    """Run a command and return exit code."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python migrate.py upgrade      # Apply all pending migrations")
        print("  python migrate.py downgrade    # Rollback one migration")
        print("  python migrate.py current      # Show current revision")
        print("  python migrate.py history      # Show migration history")
        print('  python migrate.py create "message"  # Create new migration')
        print('  python migrate.py auto "message"    # Auto-generate migration')
        sys.exit(1)

    command = sys.argv[1]

    if command == "upgrade":
        target = sys.argv[2] if len(sys.argv) > 2 else "head"
        exit_code = run_command(["alembic", "upgrade", target])

    elif command == "downgrade":
        target = sys.argv[2] if len(sys.argv) > 2 else "-1"
        exit_code = run_command(["alembic", "downgrade", target])

    elif command == "current":
        exit_code = run_command(["alembic", "current"])

    elif command == "history":
        exit_code = run_command(["alembic", "history", "--verbose"])

    elif command == "create":
        if len(sys.argv) < 3:
            print("Error: Migration message required")
            sys.exit(1)
        message = sys.argv[2]
        exit_code = run_command(["alembic", "revision", "-m", message])

    elif command == "auto":
        if len(sys.argv) < 3:
            print("Error: Migration message required")
            sys.exit(1)
        message = sys.argv[2]
        exit_code = run_command(
            ["alembic", "revision", "--autogenerate", "-m", message]
        )

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
