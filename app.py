import os
import sys


def main():
    print(sys.argv)
    if len(sys.argv) > 1:
        exec(sys.argv[1])
    else:
        print('hello')


if __name__ == '__main__':
    main()
