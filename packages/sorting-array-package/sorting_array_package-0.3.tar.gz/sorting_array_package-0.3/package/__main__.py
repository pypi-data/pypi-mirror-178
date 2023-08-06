"""
КИ22-16/1Б
Савельев Александр
Вариант 28
Selection_sort function
"""
from listfunc.funcs import selection_sort, random_list
import argparse
from pytest import main as pytest


def main():
    parser = argparse.ArgumentParser(description="sort list")
    parser.add_argument('-l', '--list', type=int, nargs='+', dest='list',
                        default=[5, 4, 3, 2, 1], help='input a list numbers separated by space')

    parser.add_argument('-r', '--random', type=int, nargs='+', dest='random',
                        help='input a size of list, then left and right borders of random numbers')

    parser.add_argument('-t', '--test', dest='test', action=argparse.BooleanOptionalAction,
                        help="Wanna enter in test mode?")

    args = parser.parse_args()
    numbers = args.list
    random = args.random
    start_test = args.test
    if start_test:
        pytest(['-v', r'package\tests\test_selection_sort.py'], )
        return

    if random:
        print(f'{(random_numbers := random_list(random))}')
        print(selection_sort(random_numbers))
    else:
        print(numbers)
        print(selection_sort(numbers))


if __name__ == '__main__':
    main()
