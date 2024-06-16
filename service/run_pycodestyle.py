# run_pycodestyle.py
import subprocess
import sys


def run_pycodestyle(paths):
    args = ["pycodestyle"] + paths
    result = subprocess.run(args)
    return result.returncode


def run_autopep8(paths):
    args = ["autopep8", "--in-place", "--aggressive"] + paths
    result = subprocess.run(args)
    return result.returncode


def main():
    paths = ["start.py", "src"]

    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        returncode = run_autopep8(paths)
    else:
        returncode = run_pycodestyle(paths)

    sys.exit(returncode)


if __name__ == "__main__":
    main()
