#!python

from colorama import Fore, init
from klongpy import KlongInterpreter


def info() -> None:
    print()
    print(f"{Fore.GREEN}Welcome to klongpy REPL")
    print(f"{Fore.BLUE}author: Brian Guarraci")
    print(f"{Fore.BLUE}repo  : https://github.com/briangu/klongpy")
    print(f"{Fore.YELLOW}crtl-c to quit")
    print()


init(autoreset=True)


success = lambda input: f"{Fore.GREEN}{input}"
failure = lambda input: f"{Fore.RED}{input}"

# https://dev.to/amal/building-the-python-repl-3468
def repl() -> None:
    info()
    try:
        klong = KlongInterpreter()
        while True:
            try:
                _in = input("?> ")
                for p in klong.prog(_in)[1]:
                    o = klong.call(p)
                    if o is not None:
                        print(success(o))
                else:
                    print()
            except Exception as e:
                print(failure(f"Error: {e}"))
                import traceback
                traceback.print_exc(e)
                raise e
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    repl()

