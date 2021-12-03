from sys import argv, exit
from os import system


def run_linter(report_file="lint_report.html"):
    lint_command = "pylint $(git ls-files '*.py') | cat > " + report_file
    system(lint_command)
    return report_file


def get_result(file):
    with open(file, "r") as f:
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

    line = get_result(run_linter())
    mark = parse_result(line)
    if mark >= min_rate:
        exit(0)
    else:
        exit(line)


if __name__ == "__main__":
    check_rate()
