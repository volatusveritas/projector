import sys

from projector import exceptions
from projector import interpret
from projector import meta




def projector_help():
    print(
"Usage: python -m [pyoptions] projector [initmethod]\n"
"\nPyOptions: any number of Python options\n"
"\nInitMethods:\n"
"  -h, --help  show this help message and exit\n"
"  [-f, --file] <file>  execute the contents of <file>\n"
"  [-i, --interactive]  start interactive mode\n"
"  -e, --expression <expressions>  execute <expressions>\n"
"\nIf no initmethod is given, interactive mode is assumed"
    )

    sys.exit()



def start_file(filename):
    try:
        with open(filename) as file:
            for raw_expression in file.read().split(';'):
                result = interpret.evaluate(raw_expression)

                if not result is None:
                    print(result)
    except:
        raise exceptions.ProjectorCantOpenFileError(filename)

    sys.exit()


def start_interactive():
    print(f"ProjectOr v{meta.VERSION}, {meta.RELEASE_YEAR}.")
    print("Entering interactive mode. Type 'quit', 'exit', 'stop' to stop.")

    while True:
        raw_input = input(">>> ")

        for raw_expression in raw_input.split(';'):
            result = interpret.evaluate(raw_expression)

            if not result is None:
                print(result)


def start_expression(full_expression):
    for raw_expression in full_expression.split(';'):
        result = interpret.evaluate(raw_expression)

        if not result is None:
            print(result)

    sys.exit()



def consume_argument():
    match sys.argv[0]:
        case "-i" | "--interactive":
            start_interactive()
        case "-h" | "--help":
            projector_help()
        case "-e" | "--expression":
            if not len(sys.argv) > 1:
                raise exceptions.ProjectorMissingInitArgError("expression")

            start_expression(sys.argv[1])
        case "-f" | "--file":
            if not len(sys.argv) > 1:
                raise exceptions.ProjectorMissingInitArgError("file")

            start_file(sys.argv[1])
        case _:
            start_file(sys.argv[0])




del sys.argv[0]  # Ignore program name

if not sys.argv:
    start_interactive()
else:
    while sys.argv: consume_argument()
