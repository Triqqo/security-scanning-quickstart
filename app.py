import os
import sys


def main():
    print(sys.argv)
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    if os.getenv("SOME_INSECURE_VAR"):
        exec(os.getenv("SOME_INSECURE_VAR"))
    print('hello')


if __name__ == '__main__':
    main()
