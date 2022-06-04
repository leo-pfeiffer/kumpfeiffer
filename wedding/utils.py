import os
import string
import random
import csv


def invite_code_generator() -> str:
    """
    Generate an alphanumeric invite code of length 6
    :return: invite code
    """
    alphabet = string.ascii_letters + string.digits
    code = []
    for i in range(6):
        code.append(random.choice(alphabet))
    return "".join(code)


def read_guest_csv(path: str) -> list:
    """
    Read guest list from a csv file.
    Columns must be: name, email
    Header: None
    :param path: path to the csv file
    :return: list containing a list of two elements for each row
    """
    assert os.path.exists(path)
    with open(path, "r") as file:
        reader = csv.reader(file)
        rows = []
        for row in reader:
            clean_row = [word.strip() for word in row]
            assert len(clean_row) == 2
            rows.append(clean_row)
    return rows
