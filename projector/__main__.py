import sys

from projector import exceptions
from projector import interpret
from projector import meta




debug_mode = False
tokenizer_only = False




def projector_help():
    print(
"Usage: python -m [pyoptions] projector [projoptions] [initmethod]\n"
"\n"
"PyOptions: any number of Python options\n"
"\n"
"ProjOptions:\n"
"  -d, --debug  start projector in debug mode\n"
"  -t, --token  run only the tokenizer\n"
"\n"
"InitMethods:\n"
"  -h, --help  show this help message and exit\n"
"  [-f, --file] <file>  execute the contents of <file>\n"
"  [-i, --interactive]  start interactive mode\n"
"  -e, --expression <expressions>  execute <expressions>\n"
"\n"
"  If no initmethod is given, interactive mode is assumed\n"
    )

    sys.exit()



def start_file(filename):
    try:
        with open(filename) as file:
            for raw_expression in file.read().split(';'):
                result = interpret.evaluate(
                    raw_expression, debug_mode, tokenizer_only
                )

                if not result is None:
                    print(result)
    except:
        raise exceptions.CantOpenFileError(filename)

    sys.exit()


def start_interactive():
    print(f"ProjectOr v{meta.VERSION}, {meta.RELEASE_YEAR}.")
    print("Entering interactive mode. Type 'quit', 'exit', 'stop' to stop.")

    while True:
        raw_input = input(">>> ")

        for raw_expression in raw_input.split(';'):
            result = interpret.evaluate(
                raw_expression, debug_mode, tokenizer_only
            )

            if not result is None:
                print(result)


def start_expression(full_expression):
    for raw_expression in full_expression.split(';'):
        result = interpret.evaluate(raw_expression, debug_mode, tokenizer_only)

        if not result is None:
            print(result)

    sys.exit()



def consume_argument():
    match sys.argv[0]:
        case "-d" | "--debug":
            global debug_mode
            debug_mode = True

            del sys.argv[0]
        case "-t" | "--token":
            global tokenizer_only
            tokenizer_only = True

            del sys.argv[0]
        case "-i" | "--interactive":
            start_interactive()
        case "-h" | "--help":
            projector_help()
        case "-e" | "--expression":
            if not len(sys.argv) > 1:
                raise exceptions.MissingInitArgError("expression")

            start_expression(sys.argv[1])
        case "-f" | "--file":
            if not len(sys.argv) > 1:
                raise exceptions.MissingInitArgError("file")

            start_file(sys.argv[1])
        case _:
            start_file(sys.argv[0])




if __name__ == "__main__":
    del sys.argv[0]  # Ignore program name

    while (True):
        if not sys.argv:
            start_interactive()

        consume_argument()
