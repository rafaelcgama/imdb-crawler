# List of basic statistics functions


# Calculate mean
def mean(my_list):
    return sum(my_list) / len(my_list)


# Calculate median
def median(my_list):
    n = len(my_list)
    my_list.sort()
    if len(my_list) % 2 == 0:
        return (my_list[(n // 2) - 1] + my_list[n // 2]) / 2
    else:
        return (my_list[n // 2])


# Calculate Standard Deviation
def stdv(my_list, type=1):
    """
    This is a calculates the standard deviation.

    Attributes:
        my_list (list): list of numbers .
        type (str): population = 0 or sample = 1.
    """
    num = 0
    for i in my_list:
        num += (i - mean(my_list))**2
    return (num / (len(my_list) - type) ) ** (1/2)


# Calculate the variance
def var(my_list, type=1):
    return (stdv(my_list, type)) ** 2


# Calculate Standard Error
def st_error(my_list, type=1):
    return stdv(my_list) / (len(my_list)) ** (1/2)

