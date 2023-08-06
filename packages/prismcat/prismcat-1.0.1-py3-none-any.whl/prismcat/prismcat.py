import re
import sys
from ansi2html import Ansi2HTMLConverter


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def check(pattern, line):
    try:
        if re.match(pattern, line):
            return True
        else:
            return False
    except Exception:
        raise Exception(f'Check your regex: "{pattern}"')


def main(
    file,
    outfile,
    red: str,
    yellow: str,
    green: str,
    blue: str,
    purple: str,
    error: str,
    abbr: bool = False,
) -> bool:
    out = []
    args = {}
    for line in file:
        f_line = None
        if purple and check(purple, line):
            color = bcolors.HEADER
            f_line = color + line
            args["purple"] = {"regex": purple, "color": color}
        if blue and check(blue, line):
            color = bcolors.OKBLUE
            f_line = color + line
            args["blue"] = {"regex": blue, "color": color}
        if green and check(green, line):
            color = bcolors.OKGREEN
            f_line = color + line
            args["green"] = {"regex": green, "color": color}
        if yellow and check(yellow, line):
            color = bcolors.WARNING
            f_line = color + line
            args["yellow"] = {"regex": yellow, "color": color}
        if red and check(red, line):
            color = bcolors.FAIL
            f_line = color + line
            args["red"] = {"regex": red, "color": color}
        if error and check(error, line):
            color = bcolors.FAIL + bcolors.UNDERLINE
            f_line = color + line
            args["error"] = {"error": red, "color": color}
        if f_line:
            formatted_line = f_line + bcolors.ENDC
            out.append(formatted_line)
        elif not abbr:
            out.append(line)

    out = "".join(out)
    if outfile:
        header = f"{bcolors.OKBLUE}Original File: {file.name}{bcolors.ENDC}\n"
        for key in args:
            print(key)
            print(type(key))
            header += f"{args[key]['color']}{key}: \
                \"{args[key]['regex']}\"{bcolors.ENDC}\n"
        header = (
            "++++++++++++++++++++++++++++++++++\n"
            + header
            + "++++++++++++++++++++++++++++++++++\n\n"
        )

        htmlout = header + out

        conv = Ansi2HTMLConverter()
        html = conv.convert(htmlout)
        outfile.write(html)

    print(out)

    return True


def cli():
    import argparse

    parser = argparse.ArgumentParser(
        prog="prism",
        description="""
        parse input, highlight lines with regex, color priority
         follows the rainbow RYGBV(P) -- Red Yellow Green Blue
          Purple with Red as top priority""",
    )
    parser.add_argument("-r", "--red")
    parser.add_argument("-y", "--yellow")
    parser.add_argument("-g", "--green")
    parser.add_argument("-b", "--blue")
    parser.add_argument("-p", "--purple")
    parser.add_argument("-e", "--error")
    parser.add_argument("-a", "--abbreviate", action="store_true")
    parser.add_argument("-o", "--outfile", type=argparse.FileType("w"))
    parser.add_argument(
        "input",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )

    args = parser.parse_args()
    if not args.input:
        parser.print_help()
    else:
        main(
            args.input,
            args.outfile,
            args.red,
            args.yellow,
            args.green,
            args.blue,
            args.purple,
            args.error,
            args.abbreviate,
        )


if __name__ == "__main__":
    sys.exit(cli())
