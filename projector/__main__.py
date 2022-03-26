from sys import argv

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

    exit()



def start_file(filename):
    try:
        with open(filename) as file:
            for raw_expression in file.read().split(';'):
                result = interpret.evaluate(raw_expression)

                if not result is None:
                    print(result)
    except:
        raise exceptions.ProjectorCantOpenFileError(filename)

    exit()


def start_interactive():
    print(f"ProjectOr v{meta.VERSION}, {meta.RELEASE_YEAR}.")
    print("Entering interactive mode. Type 'quit', 'exit', or 'stop' to stop.")

    while True:
        raw_input = input(">>> ")

        if raw_input in ["quit", "stop", "exit"]:
            break

        for raw_expression in raw_input.split(';'):
            result = interpret.evaluate(raw_expression)

            if not result is None:
                print(result)

    exit()


def start_expression(full_expression):
    for raw_expression in full_expression.split(';'):
        result = interpret.evaluate(raw_expression)

        if not result is None:
            print(result)

    exit()



def consume_argument():
    match argv[0]:
        case "-i" | "--interactive":
            start_interactive()
        case "-h" | "--help":
            projector_help()
        case "-e" | "--expression":
            if not len(argv) > 1:
                raise exceptions.ProjectorMissingInitArgError("expression")

            start_expression(argv[1])
        case "-f" | "--file":
            if not len(argv) > 1:
                raise exceptions.ProjectorMissingInitArgError("file")

            start_file(argv[1])
        case _:
            start_file(argv[0])




del argv[0]  # Ignore program name

if not argv:
    start_interactive()
else:
    while argv: consume_argument()
