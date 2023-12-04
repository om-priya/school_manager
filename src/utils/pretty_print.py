"""This File is responsible for printing pretty message to the console"""
from tabulate import tabulate


def pretty_print(res_data, headers):
    """
    Pretty prints tabular data to the console.

    Parameters:
    - res_data (list of lists): The data to be printed in tabular form.
    - headers (list): The headers for the columns in the table.

    Returns:
    None
    """
    print(tabulate(res_data, headers=headers, tablefmt="rounded_outline"))
