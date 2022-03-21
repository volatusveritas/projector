from sys import argv

import projector




def projector_help():
    pass



def start_file(filename):
    try:
        with open(filename) as file:
            for raw_expression in file.read().split(';'):
                print(projector.evaluate(raw_expression))
    except:
        print(f"Unable to open file '{filename}'")


def start_interactive():
    pass


def start_expression(full_expression):
    for raw_expression in full_expression.split(';'):
        print(projector.evaluate(raw_expression))




# Ignore program name
del argv[0]

if not argv:
    start_interactive()
else:
    if argv[0] in ["-i", "--interactive"]:
        start_interactive()
    elif argv[0] in ["-h", "--help"]:
        projector_help()
    elif argv[0] in ["-e", "--expression"]:
        if not len(argv) > 1:
            print("Missing argument: expression")

        start_expression(argv[1])
    elif argv[0] in ["-f", "--file"]:
        if not len(argv) > 1:
            print("Missing argument: file")

        start_file(argv[1])
    else:
        start_file(argv[0])
