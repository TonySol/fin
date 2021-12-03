"""Pylint all .py files in repo and rise 1 exit code only on pylint rate less than input.

Linter curses with exit codes a lot, the script parses the linter result
and shouts exit code 1 only if linter rate passes threshold – min_rate.

report file: changes the lint result destination
min_rate: can be passes on script call, default to 7
"""

from sys import argv, exit
from os import system


def run_linter(report_file="lint_report.html"):
    lint_command = "pylint $(git ls-files '*.py') | cat > " + report_file
    system(lint_command)
    return report_file


def get_result(file, print_me=False):
    with open(file, "r") as f:
        if print_me:
            print(f.read())
        else:
            for line in f:
                if "Your code has been rated" in line:
                    return line


def parse_result(line):
    start = line.find("at ")
    finish = line.find("/")
    mark = line[start + 3:finish]
    return round(float(mark))


def check_rate(min_rate=7):
    try:
        if argv[1]:
            min_rate = int(argv[1])
    except IndexError:
        pass
    file = run_linter()
    line = get_result(file)
    mark = parse_result(line)
    if mark >= min_rate:
        exit(0)
    else:
        get_result(file, True)
        exit(1)


if __name__ == "__main__":
    check_rate()
