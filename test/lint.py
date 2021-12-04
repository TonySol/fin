"""Pylint all .py files in repo and rise 1 exit code only on pylint rate less than input.

Linter curses with exit codes a lot, the script parses the linter result
and shouts exit code 1 only if linter rate passes threshold – min_rate.

report_name: changes the lint result destination
min_rate: can be passes on script call, default to 7
"""

from sys import argv, exit
from os import system


def run_linter(report_name="lint_report.txt"):
    lint_command = "pylint $( git ls-files '*.py') | cat > " + report_name
    system(lint_command)
    return report_name


def read_report(file):
    with open(file, "r") as f:
        for line in f:
            if "Your code has been rated" in line:
                return line


def parse_report(line):
    start = line.find("at ")
    finish = line.find("/")
    rate = line[start + 3:finish]
    return round(float(rate))


def check_rate(min_rate=7):
    try:
        if argv[1]:
            min_rate = int(argv[1])
    except IndexError:
        pass

    file = run_linter()
    line = read_report(file)
    rate = parse_report(line)

    if rate >= min_rate:
        exit(0)
    else:
        # with open(file, "r") as f:
        #     print(f.read())
        print(f'{line.strip()} below required {min_rate} rate.')
        exit(1)


if __name__ == "__main__":
    check_rate()
