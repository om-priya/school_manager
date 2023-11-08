"""This File is responsible for printing pretty message to the console"""
from tabulate import tabulate


def pretty_print(res_data, headers):
    """This Function is responsible to print data to console"""
    print(tabulate(res_data, headers=headers, tablefmt="rounded_outline"))
