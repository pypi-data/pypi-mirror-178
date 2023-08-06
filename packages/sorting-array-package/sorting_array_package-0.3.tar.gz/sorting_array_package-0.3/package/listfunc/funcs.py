import random


def list_input():
    """
    Input a list of numbers
    :return: list of numbers
    """
    while True:
        try:
            return list(map(int, input().split()))
        except ValueError as text_error:
            print(text_error)


def selection_sort(numbers):
    """
    Sorting an array with selection method

    >>> selection_sort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> selection_sort(([5, 5, 5, 6, 6, 7, 7, 4, 4, 2, 1, 3]))
    [1, 2, 3, 4, 4, 5, 5, 5, 6, 6, 7, 7]
    >>>selection_sort([4, 5, 6, 1, 2, 3])
    [1, 2, 3, 4, 5, 6]
    :param numbers: list of int numbers
    :return: sorted list
    """
    for i in range(len(numbers)):
        reserved_index = i
        for j in range(len(numbers) - i):
            if numbers[i + j] < numbers[reserved_index]:
                reserved_index = i + j
        numbers[i], numbers[reserved_index] = numbers[reserved_index], numbers[i]
    return numbers


def random_list(list_info):
    """
    Returns a list of random numbers of the specified size and range
    :param list_info: range borders
    :return: list =
    """
    return [random.randint(min(list_info[1:]), max(list_info[1:])) for _ in range(list_info[0])]


if __name__ == "main":
    import doctest

    doctest.testmod()
